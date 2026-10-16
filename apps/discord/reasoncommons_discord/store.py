"""Single-host durable journal, context and versioned reviews.

The journal bridges SQLite and the YAML file: prepare before replacement, then
complete after views. Recovery recognizes either hash and never blindly replays.
"""
import asyncio
from contextlib import asynccontextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import time


def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".discord-", dir=path.parent)
    try:
        if path.exists():
            os.fchmod(fd, path.stat().st_mode & 0o777)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data if isinstance(data, bytes) else data.encode())
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class Store:
    def __init__(self, runtime, state):
        self.root, self.state = Path(runtime), Path(state).resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.db = self.root / "store.sqlite"
        # Same configured state means the same lock even with different runtimes.
        self.lock_path = self.state.parent / f".{self.state.stem}" / "discord.lock"
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        owner = self.lock_path.parent / "discord-runtime.json"
        # Publish a complete ownership record exclusively, never a partial file.
        fd, temporary = tempfile.mkstemp(dir=self.lock_path.parent)
        try:
            with os.fdopen(fd, "w") as stream:
                json.dump({"runtime": str(self.root.resolve())}, stream)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, owner)
            except FileExistsError:
                pass
            if json.loads(owner.read_text())["runtime"] != str(self.root.resolve()):
                raise ValueError("This state is bound to another runtime directory. Reuse its journal/context; do not start a second ledger.")
        finally:
            os.unlink(temporary)
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS requests (
                    id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, status TEXT NOT NULL,
                    before_hash TEXT NOT NULL, after_hash TEXT NOT NULL,
                    after_text TEXT NOT NULL, payload TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS reviews (
                    token TEXT PRIMARY KEY, data TEXT NOT NULL, published TEXT, consumed TEXT);
                CREATE TABLE IF NOT EXISTS context (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT UNIQUE NOT NULL,
                    channel TEXT NOT NULL, data TEXT NOT NULL);
            """)

    def connect(self):
        db = sqlite3.connect(self.db, timeout=30)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA synchronous=FULL")
        return db

    @asynccontextmanager
    async def lock(self, wait_seconds=120):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a") as stream:
            started = time.monotonic()
            while True:
                try:
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() - started >= wait_seconds:
                        raise ValueError("Another reasoning turn is still running; try again shortly.")
                    await asyncio.sleep(0.05)
            try:
                yield
            finally:
                fcntl.flock(stream, fcntl.LOCK_UN)

    def request(self, ident, fingerprint=None):
        with self.connect() as db:
            row = db.execute("SELECT * FROM requests WHERE id=?", (ident,)).fetchone()
        if row and fingerprint is not None and row["fingerprint"] != fingerprint:
            raise ValueError("Invocation ID was reused with different content or identity.")
        return dict(row) if row else None

    def prepared(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM requests WHERE status='prepared' ORDER BY rowid")]

    def prepare(self, ident, fingerprint, before, after, payload):
        with self.connect() as db:
            db.execute("INSERT INTO requests VALUES (?,?,?,?,?,?,?)",
                       (ident, fingerprint, "prepared", digest(before), digest(after), after,
                        json.dumps(payload, ensure_ascii=False)))

    def complete(self, row):
        payload = json.loads(row["payload"])
        with self.connect() as db:
            review = payload.get("review")
            if review:
                db.execute("INSERT OR IGNORE INTO reviews(token,data) VALUES (?,?)",
                           (review["token"], json.dumps(review)))
            if payload.get("consume"):
                db.execute("UPDATE reviews SET consumed=? WHERE token=?",
                           (row["id"], payload["consume"]))
            db.execute("INSERT OR IGNORE INTO context(request_id,channel,data) VALUES (?,?,?)",
                       (row["id"], payload["channel"], json.dumps(payload["context"])))
            db.execute("UPDATE requests SET status='completed' WHERE id=?", (row["id"],))

    def history(self, channel):
        with self.connect() as db:
            rows = db.execute("SELECT data FROM context WHERE channel=? ORDER BY seq DESC LIMIT 12",
                              (str(channel),)).fetchall()
        return [json.loads(r["data"]) for r in reversed(rows)]

    def review(self, token):
        with self.connect() as db:
            row = db.execute("SELECT * FROM reviews WHERE token=?", (token,)).fetchone()
        if not row:
            raise ValueError("Unknown review token; ask for a review first.")
        return {**json.loads(row["data"]), "published": row["published"], "consumed": row["consumed"]}

    def publish(self, token, message_url):
        with self.connect() as db:
            db.execute("UPDATE reviews SET published=? WHERE token=?", (message_url, token))

    def task_context(self):
        path = self.root / "tasks.json"
        if not path.exists():
            return "Task snapshot unavailable. Do not infer current ownership or completion from YAML alone."
        try:
            data = json.loads(path.read_text())
            age = max(0, time.time() - data["refreshed_unix"])
        except (ValueError, KeyError, TypeError):
            return "Task snapshot invalid. Refresh it explicitly; ownership/completion is unverified."
        standing = "STALE" if age > 86400 else "snapshot, not a live query"
        encoded = json.dumps(data, ensure_ascii=False)
        return (f"Tasks: {standing}; age {age / 3600:.1f}h. " + encoded[:40000] +
                ("\nTRUNCATED: omitted records are unavailable; absence is not evidence of no task." if len(encoded) > 40000 else ""))
