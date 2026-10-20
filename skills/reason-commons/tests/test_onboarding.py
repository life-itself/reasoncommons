"""First-session introduction with fictional participants; no network or shared-file writes."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import onboarding
from test_feedback import toy


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


class OnboardingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state = self.root / "reason-commons.yaml"
        self.state.write_text(yaml.safe_dump(toy(), sort_keys=False, width=100000))

    def test_shown_once_per_participant_then_on_request(self):
        first = onboarding.show(self.state, "alice")
        self.assertIn("**Type: Introduction**", first)
        self.assertIn("Welcome, Alice. This is Reason Commons for **Fictional remote-work trial**", first)
        self.assertIn("You share it with Bob.", first)
        self.assertIsNone(onboarding.show(self.state, "alice"))
        self.assertIsNotNone(onboarding.show(self.state, "bob"))
        self.assertIsNotNone(onboarding.show(self.state, "alice", again=True))
        self.assertEqual(set(json.loads(onboarding.seen_file(self.state.resolve()).read_text())), {"alice", "bob"})

    def test_every_message_type_says_what_it_asks(self):
        text = onboarding.show(self.state, "alice")
        for kind in ("Feedback request", "Change proposal", "Next step", "Change result", "Answer", "Tree view", "Capture result"):
            self.assertIn(f"**{kind}**", text)
        self.assertIn('"not yet"', text)
        self.assertIn("Silence is never taken as an answer", text)

    def test_waiting_count_matches_the_feedback_queue(self):
        self.assertIn("**Waiting for you:** 1 feedback request. It comes next.", onboarding.show(self.state, "alice"))
        state = toy()
        state["participants"]["carol"] = "Carol"
        self.state.write_text(yaml.safe_dump(state, sort_keys=False, width=100000))
        self.assertIn("**Waiting for you:** nothing right now.", onboarding.show(self.state, "carol"))

    def test_sharing_line_reflects_this_checkout_without_configuring_it(self):
        self.assertIn("not available", onboarding.show(self.state, "alice"))
        git(self.root, "init", "-q", "-b", "main")
        text = onboarding.show(self.state, "alice", again=True)
        self.assertIn("**Sharing:** off in this checkout", text)
        self.assertIn(f"{self.state.resolve()} configure --remote origin --branch main --by alice", text)
        policy = onboarding.feedback_sync.local_dir(self.state.resolve()) / "feedback-sync.json"
        self.assertFalse(policy.exists())
        policy.write_text(json.dumps({"remote": "origin", "branch": "main"}))
        self.assertIn("**Sharing:** on.", onboarding.show(self.state, "alice", again=True))

    def test_shared_reasoning_is_only_read(self):
        before = self.state.read_bytes()
        onboarding.show(self.state, "alice")
        onboarding.show(self.state, "bob", again=True)
        self.assertEqual(self.state.read_bytes(), before)

    def test_unknown_participant_is_refused_and_not_recorded(self):
        with self.assertRaisesRegex(ValueError, "Unknown participant"):
            onboarding.show(self.state, "mallory")
        self.assertFalse(onboarding.seen_file(self.state.resolve()).exists())

    def test_cli_prints_once(self):
        command = [sys.executable, str(Path(onboarding.__file__)), str(self.state), "--participant", "alice"]
        self.assertIn("**Type: Introduction**", subprocess.run(command, capture_output=True, text=True, check=True).stdout)
        self.assertEqual(subprocess.run(command, capture_output=True, text=True, check=True).stdout, "")


if __name__ == "__main__":
    unittest.main()
