import asyncio
import json
from pathlib import Path
import tempfile
import time
import unittest

from reasoncommons_discord.store import Store, atomic_write, digest


class StoreTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state = self.root / "reason-commons.yaml"
        self.state.write_text("fixture")
        self.store = Store(self.root / "runtime", self.state)

    def tearDown(self):
        self.temp.cleanup()

    def test_atomic_replacement_preserves_mode(self):
        self.state.chmod(0o640)
        atomic_write(self.state, "new")
        self.assertEqual(self.state.read_text(), "new")
        self.assertEqual(self.state.stat().st_mode & 0o777, 0o640)
        self.assertFalse(list(self.root.glob(".discord-*")))

    def test_task_snapshot_availability_and_staleness_are_explicit(self):
        self.assertIn("unavailable", self.store.task_context())
        atomic_write(self.root / "runtime/tasks.json", json.dumps({"refreshed_unix": time.time() - 90000, "issues": []}))
        self.assertIn("STALE", self.store.task_context())
        atomic_write(self.root / "runtime/tasks.json", "invalid JSON")
        self.assertIn("invalid", self.store.task_context())

    def test_prepare_and_complete_is_durable_and_idempotent(self):
        payload = {"response": {"text": "Answer"}, "channel": "20", "context": {"by": "alice"}}
        self.store.prepare("one", "fingerprint", "before", "after", payload)
        reopened = Store(self.root / "runtime", self.state)
        row = reopened.prepared()[0]
        self.assertEqual(row["after_hash"], digest("after"))
        reopened.complete(row)
        reopened.complete(row)
        self.assertEqual(len(reopened.history(20)), 1)
        self.assertEqual(reopened.request("one")["status"], "completed")

    def test_second_runtime_cannot_start_an_independent_ledger_for_same_state(self):
        with self.assertRaisesRegex(ValueError, "another runtime"):
            Store(self.root / "other", self.state)

    async def test_two_instances_share_the_state_lock(self):
        second = Store(self.root / "runtime", self.state)
        entered = []
        async def other():
            async with second.lock():
                entered.append(True)
        async with self.store.lock():
            task = asyncio.create_task(other())
            await asyncio.sleep(0.02)
            self.assertFalse(entered)
        await task
        self.assertEqual(entered, [True])
