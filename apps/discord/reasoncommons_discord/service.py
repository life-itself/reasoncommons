"""Transport-independent reasoning turns with deterministic persistence guards."""
import asyncio
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from functools import lru_cache
import importlib
import json
from pathlib import Path
import shutil
import sys
import time
import uuid

import yaml

from .store import Store, atomic_write, digest


@lru_cache
def helper_modules(scripts):
    sys.path.insert(0, scripts)
    return importlib.import_module("update_views"), importlib.import_module("render_view")


def helpers(config):
    return helper_modules(str(config.scripts))[0]


@lru_cache
def sync_helper(scripts):
    sys.path.insert(0, scripts)
    return importlib.import_module("feedback_sync")


@dataclass(frozen=True)
class Invocation:
    id: str
    guild: int
    channel: int
    user: str
    text: str
    mode: str = "ask"
    source: dict | None = None
    standing: str | None = None
    feedback: dict | None = None


def index(state):
    return {item["id"]: (tree, category, item)
            for tree, data in state["trees"].items()
            for category in ("nodes", "links") for item in data[category]}


def fragment(state, ids):
    items = index(state)
    selected = set(ids)
    for ident in list(selected):
        if ident not in items:
            raise ValueError(f"Unknown reasoning ID: {ident}")
        _, category, item = items[ident]
        if category == "links":
            selected.update(item["from"] + [item["to"]])
    if not selected:
        raise ValueError("Review needs at least one reasoning item.")
    return {ident: {"tree": items[ident][0], "category": items[ident][1], "item": items[ident][2]}
            for ident in sorted(selected)}


def fragment_hash(items):
    return digest(json.dumps(items, sort_keys=True, ensure_ascii=False))


def describe(items):
    lines = []
    for ident, entry in items.items():
        item, tree = entry["item"], entry["tree"].replace("_", " ").title()
        role = item.get("kind", "Link · " + item.get("relation", "")).replace("_", " ")
        statement = item.get("text") or (" AND ".join(item["from"]) + " → " + item["to"])
        lines.append(f"{tree} · {role} · {item.get('status', 'proposed')} — {ident}: {statement}")
        for key in ("assumptions", "challenges"):
            for note in item.get(key, []):
                lines.append(f"  {key} ({note['by']}): {note['text']}")
    return "\n".join(lines)


def guard_capture(before, after, authors):
    """Enforce attribution/endorsement boundaries independently of model prose."""
    for key in set(before) | set(after):
        if key not in {"trees", "driver", "active_tree", "feedback_requests"} and before.get(key) != after.get(key):
            raise ValueError(f"Capture cannot change project metadata or receipts: {key}")
    # Validate append-only commitments and authenticated outcome reports separately.
    from . import feedback
    feedback.core().guard_transition(before, after, authors)
    old, new = index(before), index(after)
    if not old.keys() <= new.keys():
        raise ValueError("Capture must preserve existing IDs; revise or challenge the item.")
    for ident, (tree, category, item) in new.items():
        prior = old.get(ident)
        if prior and prior[:2] != (tree, category):
            raise ValueError("Capture cannot move an existing ID to another role or tree.")
        was = prior[2] if prior else {}
        prior_contributions = was.get("contributions", [])
        contributions = item.get("contributions", [])
        if contributions[:len(prior_contributions)] != prior_contributions:
            raise ValueError("Capture must retain previous contributor records.")
        if any(c["by"] not in authors | {"assistant"} for c in contributions[len(prior_contributions):]):
            raise ValueError("New attribution must come from the invoker or authenticated message author.")
        if item.get("accepted_by", []) != was.get("accepted_by", []):
            raise ValueError("Only explicit version-bound endorsement may add endorsers.")
        if item.get("endorsement_evidence", []) != was.get("endorsement_evidence", []):
            raise ValueError("Capture cannot rewrite endorsement evidence.")
        for key in ("assumptions", "challenges"):
            for note in item.get(key, []):
                if note not in was.get(key, []) and note["by"] not in authors | {"assistant"}:
                    raise ValueError("New assumption/challenge attribution requires an authenticated author.")
        if item.get("status") == "accepted":
            meaning = {k: v for k, v in item.items() if k != "contributions"}
            previous_meaning = {k: v for k, v in was.items() if k != "contributions"}
            if was.get("status") != "accepted" or meaning != previous_meaning:
                raise ValueError("Capture cannot create or revise accepted reasoning; save the revision as proposed.")
        if was and item.get("text") != was.get("text") and len(contributions) == len(prior_contributions):
            raise ValueError("A revised statement needs its contributor recorded.")


class Service:
    def __init__(self, config, agent, renderer):
        self.config, self.agent, self.renderer = config, agent, renderer
        self.store = Store(config.runtime, config.state)
        self.helper = helpers(config)

    def authorize(self, request):
        if request.guild != self.config.guild_id or request.channel not in self.config.channels:
            raise ValueError("This guild/channel is not configured for reasoning.")
        if request.user not in self.config.participants:
            raise ValueError("Your Discord ID has not been mapped to a project participant.")
        if request.mode not in {"ask", "capture", "review", "accept", "tree", "feedback"}:
            raise ValueError("Unknown invocation mode.")
        return self.config.participants[request.user]

    def _views(self):
        self.helper.update(self.config.state)

    async def sync_feedback(self):
        """Called under the state lock, after prepared saves are recovered."""
        policy = self.config.state.parent / ("." + self.config.state.stem) / "feedback-sync.json"
        if not policy.exists():
            return None
        module = sync_helper(str(self.config.scripts))
        worker = asyncio.create_task(asyncio.to_thread(module.sync, self.config.state, locked=True))
        try:
            return await asyncio.shield(worker)
        except asyncio.CancelledError:
            # Keep the caller's state lock until the Git worker actually finishes.
            # Cancelling to_thread alone would release it while writes continue.
            await asyncio.shield(worker)
            raise

    def delivery_response(self, response, delivery, changed=False):
        result = deepcopy(response)
        if delivery:
            label = "Shared successfully" if delivery["state"] == "shared" else ("Saved locally; sharing incomplete" if changed else "Shared feedback may be stale")
            result["text"] += "\n\n" + label + ": " + delivery["message"]
        elif changed:
            result["text"] += "\n\nSaved locally; automatic feedback sharing is not configured."
        return result

    def _finish(self, row):
        current = self.config.state.read_bytes()
        if digest(current) == row["before_hash"]:
            # Recheck immediately before replacement; external writers should share
            # this lock or keep the runtime as the sole writer (see README).
            if self.config.state.read_bytes() != current:
                raise ValueError("State changed during recovery; no overwrite performed.")
            if row["before_hash"] != row["after_hash"]:
                atomic_write(self.config.state, row["after_text"])
        elif digest(current) != row["after_hash"]:
            raise ValueError("A prepared save conflicts with external edits. Preserve both versions and reconcile the journal before continuing.")
        if row["before_hash"] != row["after_hash"]:
            self._views()
        self.store.complete(row)
        return json.loads(row["payload"])["response"]

    async def handle(self, request):
        person = self.authorize(request)
        if len(request.text) > 12000:
            raise ValueError("Please keep one invocation within 12,000 characters.")
        fingerprint = digest(json.dumps(asdict(request), sort_keys=True))
        async with self.store.lock():
            # Finish prior interrupted saves before any later turn. No model rerun.
            for row in self.store.prepared():
                self._finish(row)
            delivery = await self.sync_feedback()
            previous = self.store.request(request.id, fingerprint)
            if previous:
                return self.delivery_response(json.loads(previous["payload"])["response"], delivery,
                                              previous["before_hash"] != previous["after_hash"])
            before_text = self.config.state.read_bytes().decode("utf-8")
            before = self.helper.load(self.config.state)
            self.helper.validate(before)
            response, after, review, consume = await self._turn(request, person, before, before_text)
            self.helper.validate(after)
            after_text = before_text if after == before else yaml.safe_dump(after, sort_keys=False, allow_unicode=True, width=100000)
            if self.config.state.read_bytes().decode("utf-8") != before_text:
                raise ValueError("The YAML changed while this turn ran. No bot update was saved; retry against the current state.")
            context = {"by": person, "mode": request.mode, "text": request.text,
                       "source": request.source, "reply": response["text"][:12000],
                       "invocation": request.id,
                       "recorded_at": datetime.now(timezone.utc).isoformat()}
            payload = {"response": response, "channel": str(request.channel), "context": context,
                       "review": review, "consume": consume}
            self.store.prepare(request.id, fingerprint, before_text, after_text, payload)
            try:
                result = self._finish(self.store.request(request.id))
            except Exception as exc:
                raise ValueError("The turn is journaled but not fully finalized. No model rerun is needed; the next invocation will attempt recovery. " + str(exc)) from exc
            # The capture journal is complete before remote reconciliation. A push
            # failure cannot make the submitted observation appear unsaved.
            changed = before_text != after_text
            if changed:
                delivery = await self.sync_feedback()
            return self.delivery_response(result, delivery, changed)

    async def _turn(self, request, person, before, before_text):
        after, review, consume = deepcopy(before), None, None
        if request.mode == "feedback":
            from .feedback import feedback_turn
            response, after = feedback_turn(before, request, person)
            return response, after, None, None
        if request.mode == "accept":
            review = self.store.review(request.text.strip())
            if review["channel"] != str(request.channel) or not review["published"]:
                raise ValueError("Endorsement requires a review displayed in this channel.")
            if review["consumed"]:
                raise ValueError("This review was already endorsed; request a fresh review to add another endorsement.")
            if time.time() - review["created"] > 86400:
                raise ValueError("This review expired; request a fresh review.")
            current = fragment(before, review["ids"])
            if fragment_hash(current) != review["version"]:
                raise ValueError("The displayed fragment changed; inspect a fresh review before endorsing it.")
            if any(e["item"].get("status") == "disputed" for e in current.values()):
                raise ValueError("Resolve the displayed objection before endorsement.")
            for ident in current:
                item = index(after)[ident][2]
                item["status"] = "accepted"
                item["accepted_by"] = list(dict.fromkeys(item.get("accepted_by", []) + [person]))
                item.setdefault("endorsement_evidence", []).append({
                    "by": person, "mode": "text", "command": "reason-accept",
                    "options": {"fragment": review["token"]}, "invocation_id": request.id,
                    "guild_id": str(request.guild), "channel_id": str(request.channel),
                    "discord_user_id": request.user, "fragment_version": review["version"],
                    "review_message": review["published"],
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                })
            after["driver"] = person
            consume, review = review["token"], None
            response = {"text": "Type: Capture result\nAccepted for now by " + before["participants"][person] +
                        ":\n" + describe(fragment(after, list(current))) +
                        "\nEndorsement records this person's working position, not unanimity or proof.",
                        "attachments": []}
            return response, after, review, consume
        if request.mode == "tree":
            tree = request.text
            if tree not in before["trees"]:
                raise ValueError("Choose an existing tree: " + ", ".join(before["trees"]))
            path, description = await self.renderer.render(self.config.state, tree, request.standing, request.id)
            return {"text": "Type: Tree view\n" + description, "attachments": [str(path)] if path else []}, after, None, None
        job = self.config.runtime / "jobs" / uuid.uuid4().hex
        job.mkdir(parents=True, mode=0o700)
        stage = job / "reason-commons.yaml"
        atomic_write(stage, before_text)
        try:
            reply = await asyncio.wait_for(self.agent.run(
                request=request, person=person, state_path=stage,
                history=self.store.history(request.channel), task_context=self.store.task_context()),
                timeout=self.config.timeout)
            staged = self.helper.load(stage)
            self.helper.validate(staged)
            if request.mode == "capture":
                authors = {person}
                if request.source:
                    author = request.source.get("by")
                    if author not in self.config.participants.values():
                        raise ValueError("Source author must have a configured identity.")
                    authors.add(author)
                guard_capture(before, staged, authors)
                from .feedback import core
                previous_requests = {core().key(r): r for r in before.get("feedback_requests", [])}
                for commitment in staged.get("feedback_requests", []):
                    previous_reports = {report["id"] for report in previous_requests.get(core().key(commitment), {}).get("reports", [])}
                    for report in (report for report in commitment["reports"] if report["id"] not in previous_reports):
                        report["recorded_at"] = datetime.now(timezone.utc).isoformat()
                        report["source"] = {"surface": "discord", "invocation_id": request.id,
                            "invoker_id": request.user, "guild_id": str(request.guild), "channel_id": str(request.channel)}
                        if request.source and report["by"] == request.source["by"]:
                            report["text"] = request.source["text"]
                            report["source"]["source_message"] = request.source["url"]
                        else:
                            report["text"] = request.text
                        core().retain_review_work(staged, commitment, report)
                old = index(before)
                for ident, (_, _, item) in index(staged).items():
                    previous = old.get(ident, (None, None, {}))[2].get("contributions", [])
                    for contribution in item["contributions"][len(previous):]:
                        contribution["discord_reference"] = {
                            "invocation_id": request.id, "invoker_id": request.user,
                            "guild_id": str(request.guild), "channel_id": str(request.channel),
                        }
                        if request.source and contribution["by"] == request.source["by"]:
                            contribution["discord_reference"]["source_message"] = request.source["url"]
                after = staged
                after["driver"] = person
            elif staged != before:
                raise ValueError("Questions and reviews cannot mutate reasoning.")
            for ident in reply.reasoning_ids:
                if ident not in index(after):
                    raise ValueError("The answer cites an unknown reasoning ID.")
            text = reply.text.strip()
            if not text:
                raise ValueError("The agent returned an empty answer.")
            if reply.reasoning_ids:
                text += "\nReasoning: " + ", ".join(reply.reasoning_ids)
            text += "\nState version: " + digest(before_text)[:12]
            response = {"text": text, "attachments": [], "skill_version": reply.skill_version}
            # A new participant session sees their outstanding feedback first.
            # Explicit tree, endorsement and feedback operations keep their purpose.
            if request.mode == "ask":
                from .feedback import session_prompt
                prompt = session_prompt(before, person, self.store.history(request.channel))
                if prompt:
                    response["text"] = prompt + "\n\n---\n\nRequested answer:\n" + response["text"]
            if request.mode == "review" and reply.review_ids:
                items = fragment(before, reply.review_ids)
                token = "review-" + uuid.uuid4().hex[:16]
                review = {"token": token, "version": fragment_hash(items), "ids": list(items),
                          "channel": str(request.channel), "created": time.time()}
                response["text"] += ("\n\nInspectable fragment (version " + review["version"][:12] + "):\n" +
                                     describe(items) + "\nTo endorse exactly this version, type /reason-accept fragment:" + token)
                response["review_token"] = token
            if request.mode == "capture":
                response["text"] += "\nSaved as a capture; no endorsement was inferred. Use /reason mode:review to inspect a fragment."
            return response, after, review, consume
        finally:
            # Durable context and prepared journal retain the useful result; no
            # unbounded accumulation of staged YAML or provider sessions.
            shutil.rmtree(job)
