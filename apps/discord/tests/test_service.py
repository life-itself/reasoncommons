import asyncio
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from reasoncommons_discord.agent import Reply
from reasoncommons_discord.config import Config
from reasoncommons_discord.service import Invocation, Service, fragment, fragment_hash

REPO = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).parent / "fixtures/remote-work.yaml"


class FakeAgent:
    def __init__(self, action=None, ids=None):
        self.action = action
        self.ids = ids or []
        self.calls = []

    async def run(self, **kwargs):
        self.calls.append(kwargs)
        if self.action:
            result = self.action(kwargs)
            if asyncio.iscoroutine(result):
                await result
        return Reply("Type: Answer\nThe reported gain concerns the studied call-centre conditions.",
                     self.ids, ["r-productivity-gain"], "fixture-skill")


class FakeRenderer:
    async def render(self, *args):
        return None, "Fixture tree view"


def add_capture(kwargs):
    path = kwargs["state_path"]
    state = yaml.safe_load(path.read_text())
    state["trees"]["current_reality"]["nodes"].append({
        "id": "r-return", "kind": "observation",
        "text": "The gain partially reversed when workers chose to return to the office.",
        "status": "proposed",
        "contributions": [{"by": kwargs["person"], "attribution": "explicit", "mode": "text"}],
    })
    path.write_text(yaml.safe_dump(state, sort_keys=False))


class ServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state = self.root / "reason-commons.yaml"
        self.state.write_bytes(FIXTURE.read_bytes())
        self.config = Config(REPO, self.state, self.root / "runtime", 10, frozenset({20}),
                             {"100": "alice", "200": "bob"}, model="fixture", budget_usd=0.01)
        self.agent = FakeAgent()
        self.service = Service(self.config, self.agent, FakeRenderer())

    def tearDown(self):
        self.temp.cleanup()

    def request(self, ident="1", mode="ask", user="100", text="What do we know?"):
        return Invocation(ident, 10, 20, user, text, mode)

    def read(self):
        return yaml.safe_load(self.state.read_text())

    async def review(self):
        self.agent.ids = ["r-scope"]
        response = await self.service.handle(self.request("review", "review"))
        self.service.store.publish(response["review_token"], "https://discord.com/channels/10/20/300")
        return response["review_token"]

    async def test_question_grounded_read_only_and_restart_context(self):
        original = self.state.read_bytes()
        response = await self.service.handle(self.request())
        self.assertIn("r-productivity-gain", response["text"])
        self.assertEqual(original, self.state.read_bytes())
        resumed = Service(self.config, self.agent, FakeRenderer())
        await resumed.handle(self.request("2"))
        self.assertEqual(self.agent.calls[-1]["history"][0]["by"], "alice")
        self.assertIn("unavailable", self.agent.calls[-1]["task_context"])

    async def test_duplicate_is_cached_across_restart(self):
        first = await self.service.handle(self.request())
        resumed = Service(self.config, self.agent, FakeRenderer())
        self.assertEqual(first, await resumed.handle(self.request()))
        self.assertEqual(len(self.agent.calls), 1)
        with self.assertRaisesRegex(ValueError, "reused"):
            await resumed.handle(self.request(text="Different question"))

    async def test_access_checked_before_cached_result(self):
        await self.service.handle(self.request())
        for request in (replace(self.request(), channel=999), replace(self.request(), guild=999),
                        replace(self.request(), user="999")):
            with self.assertRaises(ValueError):
                await self.service.handle(request)
        self.assertEqual(len(self.agent.calls), 1)

    async def test_capture_attributed_and_not_endorsed(self):
        self.agent.action = add_capture
        await self.service.handle(self.request(mode="capture", user="200"))
        state = self.read()
        node = state["trees"]["current_reality"]["nodes"][-1]
        self.assertEqual(node["status"], "proposed")
        self.assertEqual(node["contributions"][0]["by"], "bob")
        self.assertEqual(node["contributions"][0]["discord_reference"]["invoker_id"], "200")
        self.assertEqual(state["driver"], "bob")
        self.assertFalse(list((self.config.runtime / "jobs").iterdir()))

    async def test_question_cannot_write(self):
        original = self.state.read_bytes()
        self.agent.action = add_capture
        with self.assertRaisesRegex(ValueError, "cannot mutate"):
            await self.service.handle(self.request())
        self.assertEqual(original, self.state.read_bytes())

    async def test_forged_endorsement_rejected(self):
        def forge(kwargs):
            state = yaml.safe_load(kwargs["state_path"].read_text())
            state["trees"]["current_reality"]["nodes"][-1].update(status="accepted", accepted_by=["alice"])
            kwargs["state_path"].write_text(yaml.safe_dump(state))
        self.agent.action = forge
        with self.assertRaisesRegex(ValueError, "endorsers"):
            await self.service.handle(self.request(mode="capture"))

    async def test_capture_cannot_rewrite_an_accepted_claim(self):
        def change(kwargs):
            state = yaml.safe_load(kwargs["state_path"].read_text())
            state["trees"]["current_reality"]["nodes"][0]["text"] = "Applies to everybody."
            kwargs["state_path"].write_text(yaml.safe_dump(state))
        self.agent.action = change
        with self.assertRaisesRegex(ValueError, "accepted reasoning"):
            await self.service.handle(self.request(mode="capture"))

    async def test_duplicate_contribution_retains_authorship_without_endorsement(self):
        def duplicate(kwargs):
            state = yaml.safe_load(kwargs["state_path"].read_text())
            state["trees"]["current_reality"]["nodes"][0]["contributions"].append(
                {"by": "bob", "attribution": "explicit", "mode": "text"})
            kwargs["state_path"].write_text(yaml.safe_dump(state))
        self.agent.action = duplicate
        await self.service.handle(self.request(mode="capture", user="200"))
        node = self.read()["trees"]["current_reality"]["nodes"][0]
        self.assertEqual(node["accepted_by"], ["alice"])
        self.assertEqual(node["contributions"][-1]["by"], "bob")
        self.assertEqual(node["status"], "accepted")

    async def test_spoofed_speaker_and_metadata_rejected(self):
        def spoof(kwargs):
            add_capture(kwargs)
            state = yaml.safe_load(kwargs["state_path"].read_text())
            state["trees"]["current_reality"]["nodes"][-1]["contributions"][0]["by"] = "bob"
            kwargs["state_path"].write_text(yaml.safe_dump(state))
        self.agent.action = spoof
        with self.assertRaisesRegex(ValueError, "attribution"):
            await self.service.handle(self.request(mode="capture"))
        def metadata(kwargs):
            state = yaml.safe_load(kwargs["state_path"].read_text())
            state["project"] = "A new project"
            kwargs["state_path"].write_text(yaml.safe_dump(state))
        self.agent.action = metadata
        with self.assertRaisesRegex(ValueError, "metadata"):
            await self.service.handle(self.request(mode="capture"))

    async def test_explicit_endorsement_includes_endpoints_and_real_endorser(self):
        token = await self.review()
        self.assertNotIn("accepted_by", self.read()["trees"]["current_reality"]["nodes"][-1])
        response = await self.service.handle(self.request("accept", "accept", user="200", text=token))
        state = self.read()
        self.assertEqual(state["trees"]["current_reality"]["nodes"][-1]["accepted_by"], ["bob"])
        self.assertEqual(state["trees"]["current_reality"]["links"][0]["accepted_by"], ["bob"])
        evidence = state["trees"]["current_reality"]["nodes"][-1]["endorsement_evidence"][0]
        self.assertEqual(evidence["discord_user_id"], "200")
        self.assertEqual(evidence["review_message"], "https://discord.com/channels/10/20/300")
        self.assertEqual(len(self.agent.calls), 1)  # endorsement never delegates to the model
        self.assertIn("Bob", response["text"])
        with self.assertRaisesRegex(ValueError, "already endorsed"):
            await self.service.handle(self.request("accept-again", "accept", text=token))

    async def test_unpublished_review_cannot_be_endorsed(self):
        self.agent.ids = ["r-productivity-gain"]
        result = await self.service.handle(self.request("review", "review"))
        with self.assertRaisesRegex(ValueError, "displayed"):
            await self.service.handle(self.request("accept", "accept", text=result["review_token"]))

    async def test_stale_review_rejected(self):
        token = await self.review()
        state = self.read()
        state["trees"]["current_reality"]["nodes"][-1]["text"] += " Revised."
        self.state.write_text(yaml.safe_dump(state))
        with self.assertRaisesRegex(ValueError, "fragment changed"):
            await self.service.handle(self.request("accept", "accept", text=token))

    async def test_unrelated_changes_do_not_invalidate_review(self):
        token = await self.review()
        state = self.read()
        state["trees"]["current_reality"]["backlog"].append({"ref": "r-scope", "work": "other_work"})
        self.state.write_text(yaml.safe_dump(state))
        await self.service.handle(self.request("accept", "accept", text=token))

    async def test_disputed_review_requires_resolution(self):
        state = self.read()
        node = state["trees"]["current_reality"]["nodes"][-1]
        node.update(status="disputed", challenges=[{"by": "bob", "text": "Is the scope accurate?"}])
        self.state.write_text(yaml.safe_dump(state))
        token = await self.review()
        with self.assertRaisesRegex(ValueError, "objection"):
            await self.service.handle(self.request("accept", "accept", text=token))

    async def test_external_edit_is_preserved(self):
        original = self.state.read_text()
        def external(kwargs):
            add_capture(kwargs)
            self.state.write_text(original + "\n# External work\n")
        self.agent.action = external
        with self.assertRaisesRegex(ValueError, "YAML changed"):
            await self.service.handle(self.request(mode="capture"))
        self.assertTrue(self.state.read_text().endswith("# External work\n"))
        self.assertNotIn("r-return", self.state.read_text())

    async def test_concurrent_duplicate_serialized(self):
        async def slow(kwargs):
            await asyncio.sleep(0.03)
            add_capture(kwargs)
        self.agent.action = slow
        a, b = await asyncio.gather(self.service.handle(self.request(mode="capture")),
                                    self.service.handle(self.request(mode="capture")))
        self.assertEqual(a, b)
        self.assertEqual(len(self.agent.calls), 1)
        self.assertEqual(sum(n["id"] == "r-return" for n in self.read()["trees"]["current_reality"]["nodes"]), 1)

    async def test_recovery_after_yaml_replace_before_sqlite_complete(self):
        self.agent.action = add_capture
        with patch.object(self.service.store, "complete", side_effect=OSError("power loss")):
            with self.assertRaisesRegex(ValueError, "journaled"):
                await self.service.handle(self.request(mode="capture"))
        self.assertIn("r-return", self.state.read_text())
        resumed = Service(self.config, self.agent, FakeRenderer())
        await resumed.handle(self.request(mode="capture"))
        self.assertEqual(len(self.agent.calls), 1)
        self.assertFalse(resumed.store.prepared())

    async def test_recovery_before_yaml_replace(self):
        self.agent.action = add_capture
        with patch("reasoncommons_discord.service.atomic_write", wraps=__import__("reasoncommons_discord.store", fromlist=["atomic_write"]).atomic_write) as write:
            def fail_state(path, data):
                if Path(path) == self.state:
                    raise OSError("power loss")
                from reasoncommons_discord.store import atomic_write
                return atomic_write(path, data)
            write.side_effect = fail_state
            with self.assertRaisesRegex(ValueError, "journaled"):
                await self.service.handle(self.request(mode="capture"))
        self.assertNotIn("r-return", self.state.read_text())
        await self.service.handle(self.request(mode="capture"))
        self.assertIn("r-return", self.state.read_text())
        self.assertEqual(len(self.agent.calls), 1)

    async def test_recovery_refuses_unrelated_external_state(self):
        self.agent.action = add_capture
        with patch.object(self.service.store, "complete", side_effect=OSError("power loss")):
            with self.assertRaises(ValueError):
                await self.service.handle(self.request(mode="capture"))
        self.state.write_text(self.state.read_text() + "\n# New external change\n")
        with self.assertRaisesRegex(ValueError, "conflicts"):
            await self.service.handle(self.request("later"))
        self.assertIn("New external change", self.state.read_text())

    async def test_timeout_discards_staging(self):
        async def hang(kwargs):
            add_capture(kwargs)
            await asyncio.sleep(1)
        service = Service(replace(self.config, timeout=0.01), FakeAgent(hang), FakeRenderer())
        before = self.state.read_bytes()
        with self.assertRaises(asyncio.TimeoutError):
            await service.handle(self.request(mode="capture"))
        self.assertEqual(before, self.state.read_bytes())

    async def test_tree_does_not_use_model_or_write_state(self):
        before = self.state.read_bytes()
        response = await self.service.handle(self.request(mode="tree", text="current_reality"))
        self.assertIn("Tree view", response["text"])
        self.assertEqual(before, self.state.read_bytes())
        self.assertFalse(self.agent.calls)

    async def test_crlf_question_preserves_exact_bytes(self):
        self.state.write_bytes(self.state.read_bytes().replace(b"\n", b"\r\n"))
        before = self.state.read_bytes()
        await self.service.handle(self.request())
        self.assertEqual(before, self.state.read_bytes())

    async def test_authenticated_selected_message_author_can_be_attributed(self):
        def source_capture(kwargs):
            add_capture(kwargs)
            state = yaml.safe_load(kwargs["state_path"].read_text())
            state["trees"]["current_reality"]["nodes"][-1]["contributions"][0]["by"] = "bob"
            kwargs["state_path"].write_text(yaml.safe_dump(state))
        self.agent.action = source_capture
        request = replace(self.request(mode="capture"), source={
            "by": "bob", "discord_user_id": "200",
            "url": "https://discord.com/channels/10/20/456", "text": "The gain partly reversed."})
        await self.service.handle(request)
        contribution = self.read()["trees"]["current_reality"]["nodes"][-1]["contributions"][0]
        self.assertEqual(contribution["by"], "bob")
        self.assertEqual(contribution["discord_reference"]["source_message"], request.source["url"])

    def test_fragment_retains_full_qualifications_and_and(self):
        selected = fragment(self.read(), ["r-scope"])
        self.assertEqual(len(selected), 4)
        self.assertIn("under its studied conditions", selected["r-productivity-gain"]["item"]["text"])
        self.assertEqual(len(selected["r-scope"]["item"]["from"]), 2)
        self.assertEqual(fragment_hash(selected), fragment_hash(deepcopy(selected)))
