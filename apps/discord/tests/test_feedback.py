"""No network/model calls: actual YAML queue, service journal and delivery boundaries."""
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import subprocess
import unittest
from unittest.mock import AsyncMock, patch

import yaml

from reasoncommons_discord.agent import Reply
from reasoncommons_discord.config import Config
from reasoncommons_discord.feedback import core, dispatch_once, session_prompt
from reasoncommons_discord.service import Invocation, Service, guard_capture
from reasoncommons_discord.store import Store

REPO = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).parent / "fixtures/remote-work.yaml"


def toy():
    state = yaml.safe_load(FIXTURE.read_text())
    contribution = [{"by": "alice", "attribution": "explicit", "mode": "text"}]
    state["trees"]["future_reality"] = {"nodes": [
        {"id": ident, "text": text, "kind": kind, "status": "proposed", "contributions": deepcopy(contribution)}
        for ident, kind, text in (
            ("trial", "injection", "Try a comparable remote call-handling shift."),
            ("gain", "predicted_effect", "More comparable calls are completed."),
            ("risk", "undesirable_effect", "Obtaining assistance may become harder."))], "links": [], "backlog": []}
    state["feedback_requests"] = [core().new_request(state, "trial-feedback", "trial", ["gain"], ["risk"], ["bob"], "alice",
        recorded_at="2026-10-20T00:00:00Z", ready_when="After experiencing the trial.")]
    return state


class FakeAgent:
    def __init__(self):
        self.calls = []
        self.action = None

    async def run(self, **kwargs):
        self.calls.append(kwargs)
        if self.action:
            state = yaml.safe_load(kwargs["state_path"].read_text())
            kwargs["state_path"].write_text(yaml.safe_dump(self.action(state)))
        return Reply("Type: Answer\nThe study scope remains limited.", [], ["r-productivity-gain"], "fixture")


class FeedbackServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.state = self.root / "state.yaml"
        self.state.write_text(yaml.safe_dump(toy(), sort_keys=False))
        self.config = Config(REPO, self.state, self.root / "runtime", 10, frozenset({20}),
                             {"100": "alice", "200": "bob"}, feedback_channel=20)
        self.agent = FakeAgent()
        self.service = Service(self.config, self.agent, None)

    def tearDown(self):
        self.temp.cleanup()

    def request(self, ident="one", **data):
        return Invocation(ident, 10, 20, "200", data.pop("text", "More calls completed; I have not assessed access to help."),
                          "feedback", feedback={"request_id": "trial-feedback", "revision": 1, **data})

    def read(self):
        return yaml.safe_load(self.state.read_text())

    async def test_request_displays_both_predictions_without_changing_state(self):
        original = self.state.read_bytes()
        response = await self.service.handle(self.request())
        self.assertIn("More comparable calls are completed.", response["text"])
        self.assertIn("Obtaining assistance may become harder.", response["text"])
        self.assertEqual(self.state.read_bytes(), original)
        self.assertEqual(self.agent.calls, [])

    async def test_authenticated_feedback_saved_in_canonical_yaml_with_partial_status(self):
        await self.service.handle(self.request(submit=True, benefit="observed"))
        state = self.read()
        report = state["feedback_requests"][0]["reports"][0]
        self.assertEqual(report["by"], "bob")
        self.assertEqual(report["source"]["discord_user_id"], "200")
        self.assertEqual(core().queue(state, "bob")[0]["pending"], ["risk"])
        self.assertEqual(self.agent.calls, [])
        self.assertEqual(state["trees"]["future_reality"]["nodes"], toy()["trees"]["future_reality"]["nodes"])
        self.assertEqual(state["trees"]["future_reality"]["backlog"][0]["work"], "review_outcome_feedback")

    async def test_benefit_and_reservation_can_be_reported_together(self):
        await self.service.handle(self.request(submit=True, benefit="observed", reservation="not_observed"))
        self.assertEqual(core().queue(self.read(), "bob"), [])

    async def test_reported_harm_is_explicit_and_requires_reasoning_review(self):
        response = await self.service.handle(self.request(submit=True, reservation="observed", text="Getting help was harder."))
        self.assertIn("Possible harm reported", response["text"])
        self.assertEqual(self.read()["trees"]["future_reality"]["backlog"][0]["work"], "review_outcome_feedback")
        self.assertEqual(core().queue(self.read(), "bob")[0]["pending"], ["gain"])

    async def test_unassigned_person_cannot_submit_or_inspect_request(self):
        with self.assertRaisesRegex(ValueError, "not assigned"):
            await self.service.handle(replace(self.request(submit=True, benefit="observed"), user="100"))

    async def test_duplicate_submission_is_cached_after_restart(self):
        request = self.request(submit=True, benefit="observed")
        first = await self.service.handle(request)
        restarted = Service(self.config, self.agent, None)
        self.assertEqual(await restarted.handle(request), first)
        self.assertEqual(len(self.read()["feedback_requests"][0]["reports"]), 1)

    async def test_not_yet_and_deferral_leave_outcomes_unassessed(self):
        date = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()
        await self.service.handle(self.request(submit=True, readiness="not_yet", defer_until=date, text="I have not tried it."))
        self.assertEqual(core().queue(self.read(), "bob"), [])
        self.assertEqual(core().queue(self.read(), "bob", include_waiting=True)[0]["pending"], ["gain", "risk"])

    async def test_old_version_feedback_remains_attached_to_original(self):
        state = self.read()
        state["trees"]["future_reality"]["nodes"][1]["text"] = "More calls are completed over two shifts."
        state["feedback_requests"].append(core().new_request(state, "trial-feedback", "trial", ["gain"], ["risk"], ["bob"], "alice"))
        self.state.write_text(yaml.safe_dump(state))
        await self.service.handle(self.request(submit=True, benefit="observed"))
        state = self.read()
        self.assertEqual(len(state["feedback_requests"][0]["reports"]), 1)
        self.assertEqual(state["feedback_requests"][1]["reports"], [])
        self.assertEqual(state["feedback_requests"][0]["benefits"][0]["text"], "More comparable calls are completed.")

    async def test_interrupted_feedback_save_recovers_without_duplicate(self):
        request = self.request(submit=True, benefit="observed")
        with patch.object(self.service, "_views", side_effect=OSError("interrupted")):
            with self.assertRaisesRegex(ValueError, "journaled"):
                await self.service.handle(request)
        restarted = Service(self.config, self.agent, None)
        await restarted.handle(request)
        self.assertEqual(len(self.read()["feedback_requests"][0]["reports"]), 1)

    async def test_session_entry_surfaces_feedback_first_and_keeps_requested_answer(self):
        response = await self.service.handle(Invocation("ask-1", 10, 20, "200", "What should I do next?"))
        self.assertTrue(response["text"].startswith("Type: Feedback request"))
        self.assertIn("The study scope remains limited.", response["text"])
        response = await self.service.handle(Invocation("ask-2", 10, 20, "200", "Continue"))
        self.assertTrue(response["text"].startswith("Type: Answer"))

    async def test_native_session_report_is_seen_by_discord_queue(self):
        state = self.read()
        report = {"id": "native-session-report", "by": "bob", "recorded_at": datetime.now(timezone.utc).isoformat(),
                  "readiness": "experienced", "text": "Both effects assessed.", "evidence_type": "self_report",
                  "outcomes": [{"ref": ref, "verdict": verdict, "note": "My trial experience."}
                               for ref, verdict in (("gain", "observed"), ("risk", "not_observed"))]}
        self.state.write_text(yaml.safe_dump(core().add_report(state, "trial-feedback", 1, report)))
        response = await self.service.handle(Invocation("native-resume", 10, 20, "200", "Continue"))
        self.assertTrue(response["text"].startswith("Type: Answer"))

    async def test_proactive_delivery_once_across_restart_does_not_answer_outcomes(self):
        send = AsyncMock(return_value="https://discord.com/channels/10/20/300")
        self.assertEqual(await dispatch_once(self.service, send), 1)
        self.assertEqual(await dispatch_once(Service(self.config, self.agent, None), send), 0)
        self.assertEqual(send.call_count, 1)
        self.assertEqual(send.call_args.args[0], "200")
        self.assertEqual(core().queue(self.read(), "bob")[0]["pending"], ["gain", "risk"])
        self.assertEqual(self.service.store.feedback_deliveries()[0]["state"], "sent")

    async def test_uncertain_delivery_is_not_automatically_repeated(self):
        send = AsyncMock(side_effect=RuntimeError("possibly delivered"))
        self.assertEqual(await dispatch_once(self.service, send), 0)
        self.assertEqual(await dispatch_once(self.service, send), 0)
        self.assertEqual(send.call_count, 1)
        row = self.service.store.feedback_deliveries()[0]
        self.assertEqual(row["state"], "uncertain")
        with self.assertRaises(ValueError):
            self.service.store.retry_feedback_delivery(row["id"])
        self.service.store.finish_feedback_delivery(row["id"], "failed")
        self.service.store.retry_feedback_delivery(row["id"])
        self.assertEqual(await dispatch_once(self.service, AsyncMock(return_value="verified-url")), 1)

    async def test_unscheduled_feedback_is_dispatched_and_deferred_feedback_is_not(self):
        await self.service.handle(self.request(submit=True, readiness="not_yet", defer_until=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat()))
        send = AsyncMock()
        self.assertEqual(await dispatch_once(self.service, send), 0)
        send.assert_not_called()

    async def test_disabled_dispatch_has_no_network_call(self):
        self.service.config = replace(self.config, feedback_channel=None)
        send = AsyncMock()
        self.assertEqual(await dispatch_once(self.service, send), 0)
        send.assert_not_called()

    async def test_multiple_requests_do_not_create_a_burst_for_one_participant(self):
        state = self.read()
        state["feedback_requests"].append(core().new_request(state, "another-trial", "trial", ["gain"], ["risk"], ["bob"], "alice"))
        self.state.write_text(yaml.safe_dump(state))
        send = AsyncMock(return_value="delivered-url")
        self.assertEqual(await dispatch_once(self.service, send), 1)
        self.assertEqual(await dispatch_once(self.service, send), 0)
        self.assertEqual(send.call_count, 1)
        self.assertEqual(len(core().queue(self.read(), "bob")), 2)

    async def test_dated_deferral_creates_one_new_prompting_opportunity(self):
        send = AsyncMock(return_value="delivered-url")
        await dispatch_once(self.service, send)
        future = datetime.now(timezone.utc) + timedelta(days=1)
        await self.service.handle(self.request(submit=True, readiness="not_yet", defer_until=future.isoformat()))
        self.assertEqual(await dispatch_once(self.service, send), 0)
        with patch.object(core(), "utc_now", return_value=future + timedelta(seconds=1)):
            self.assertEqual(await dispatch_once(self.service, send), 1)
            self.assertEqual(await dispatch_once(self.service, send), 0)
        self.assertEqual(send.call_count, 2)

    def test_capture_allows_commitments_but_not_impersonation_or_prediction_rewrite(self):
        before = self.read()
        report = {"id": "capture-report", "by": "bob", "recorded_at": datetime.now(timezone.utc).isoformat(),
                  "readiness": "not_yet", "text": "Not tried yet.", "evidence_type": "self_report", "outcomes": []}
        after = core().add_report(before, "trial-feedback", 1, report)
        guard_capture(before, after, {"bob"})
        with self.assertRaises(ValueError):
            guard_capture(before, after, {"alice"})
        after = deepcopy(before)
        after["feedback_requests"][0]["benefits"][0]["text"] = "Easier after seeing outcomes"
        with self.assertRaises(ValueError):
            guard_capture(before, after, {"bob"})

    async def test_natural_capture_appends_feedback_with_host_provenance_and_actual_words(self):
        def capture(state):
            return core().add_report(state, "trial-feedback", 1, {
                "id": "natural-report", "by": "bob", "recorded_at": datetime.now(timezone.utc).isoformat(),
                "readiness": "experienced", "text": "Model summary replaced by actual contribution.", "evidence_type": "self_report",
                "outcomes": [{"ref": "gain", "verdict": "observed", "note": "More comparable calls completed."}]})
        self.agent.action = capture
        actual = "For trial-feedback revision 1, I completed more calls; I have not checked the concern."
        await self.service.handle(Invocation("natural-capture", 10, 20, "200", actual, "capture"))
        report = self.read()["feedback_requests"][0]["reports"][0]
        self.assertEqual(report["text"], actual)
        self.assertEqual(report["source"]["invocation_id"], "natural-capture")
        self.assertEqual(core().queue(self.read(), "bob")[0]["pending"], ["risk"])

    def git(self, repo, *args):
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()

    def sharing_setup(self):
        from reasoncommons_discord.service import sync_helper
        remote = self.root / "shared.git"
        self.git(self.root, "init", "--bare", "--initial-branch=main", str(remote))
        self.git(self.root, "init", "--initial-branch=main")
        self.git(self.root, "config", "user.name", "Fixture participant")
        self.git(self.root, "config", "user.email", "fixture@example.invalid")
        self.git(self.root, "add", "state.yaml")
        self.git(self.root, "commit", "-m", "Shared fictional expectation")
        self.git(self.root, "remote", "add", "origin", str(remote))
        self.git(self.root, "push", "origin", "main")
        module = sync_helper(str(self.config.scripts))
        module.configure(self.state, "origin", "main", "alice", "Share feedback automatically to this origin/main.")
        return remote, module

    async def test_feedback_is_journaled_then_shared_without_model_or_duplicate(self):
        remote, module = self.sharing_setup()
        request = self.request(submit=True, benefit="observed")
        response = await self.service.handle(request)
        self.assertIn("Shared successfully", response["text"])
        shared = yaml.safe_load(self.git(remote, "show", "main:state.yaml"))
        self.assertEqual(len(shared["feedback_requests"][0]["reports"]), 1)
        restarted = Service(self.config, self.agent, None)
        await restarted.handle(request)
        self.assertEqual(self.git(remote, "rev-list", "--count", "main"), "2")
        self.assertEqual(self.agent.calls, [])
        self.assertEqual(core().queue(shared, "bob")[0]["pending"], ["risk"])

    async def test_offline_sharing_keeps_capture_complete_and_defers_proactive_prompt(self):
        remote, module = self.sharing_setup()
        offline = self.root / "offline.git"
        remote.rename(offline)
        response = await self.service.handle(self.request(submit=True, benefit="observed"))
        self.assertIn("Saved locally; sharing incomplete", response["text"])
        self.assertEqual(len(self.read()["feedback_requests"][0]["reports"]), 1)
        self.assertEqual(self.service.store.prepared(), [])
        send = AsyncMock()
        self.assertEqual(await dispatch_once(self.service, send), 0)
        send.assert_not_called()
        offline.rename(remote)
        await self.service.handle(self.request(submit=True, benefit="observed"))
        shared = yaml.safe_load(self.git(remote, "show", "main:state.yaml"))
        self.assertEqual(len(shared["feedback_requests"][0]["reports"]), 1)

    async def test_reordered_reports_do_not_rewrite_existing_host_provenance(self):
        state = self.read()
        state["feedback_requests"][0]["feedback_from"].append("alice")
        previous = {"id": "bob-original", "by": "bob", "recorded_at": "2026-10-20T10:00:00Z",
                    "readiness": "not_yet", "text": "I have not tried it.", "evidence_type": "self_report", "outcomes": [],
                    "source": {"surface": "original-session"}}
        state = core().add_report(state, "trial-feedback", 1, previous)
        self.state.write_text(yaml.safe_dump(state))

        def capture(staged):
            staged = core().add_report(staged, "trial-feedback", 1, {"id": "alice-new", "by": "alice", "recorded_at": datetime.now(timezone.utc).isoformat(),
                "readiness": "not_yet", "text": "Pending", "evidence_type": "self_report", "outcomes": []})
            staged["feedback_requests"][0]["reports"].reverse()
            return staged

        self.agent.action = capture
        await self.service.handle(Invocation("reordered", 10, 20, "100", "I also have not tried it.", "capture"))
        records = {r["id"]: r for r in self.read()["feedback_requests"][0]["reports"]}
        self.assertEqual(records["bob-original"], previous)
        self.assertEqual(records["alice-new"]["text"], "I also have not tried it.")

    def test_feedback_channel_must_be_allowed_and_interval_bounded(self):
        with self.assertRaisesRegex(ValueError, "configured reasoning channel"):
            replace(self.config, feedback_channel=999).validate()
        with self.assertRaisesRegex(ValueError, "at least 30"):
            replace(self.config, feedback_interval=0).validate()


if __name__ == "__main__":
    unittest.main()
