"""Toy-case checks in a throwaway Git repository; no real project data is read or changed."""

from contextlib import redirect_stdout
from copy import deepcopy
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_pr_trees.py"
SPEC = importlib.util.spec_from_file_location("check_pr_trees", SCRIPT)
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)

STATE = "reason-commons.yaml"


def receipt(ref="fixture-change", paths=None):
    return {"proposal_ref": ref, "proposal_revision": 1, "by": "alice",
            "recorded_at": "2026-10-14T12:00:00Z", "timezone": "UTC", "mode": "text",
            "source": "conversation", "source_text": "yes, I accept the fixture proposal",
            "scope": "Update the fixture README and remote-work scope reasoning.",
            "node_ids": ["n1", "n2"], "link_ids": ["l1"],
            "approved_paths": [STATE, "README.md"] if paths is None else paths}


def toy():
    # Observations from claim-tree-annotation.md, not invented CRT symptoms.
    contribution = [{"by": "alice", "attribution": "explicit", "mode": "text"}]
    texts = ["13% productivity gain for remote workers", "Study covers call centre workers only"]
    nodes = [{"id": f"n{i}", "kind": "observation", "text": text, "status": "proposed", "contributions": deepcopy(contribution)} for i, text in enumerate(texts, 1)]
    return {"schema_version": 1, "project": "Remote-work toy fixture", "driver": "alice", "participants": {"alice": "Alice"}, "active_tree": "current_reality", "trees": {"current_reality": {"nodes": nodes, "links": [], "backlog": []}}, "change_acceptances": [receipt()]}


def with_link(state):
    state["trees"]["current_reality"]["links"].append({"id": "l1", "from": ["n2"], "to": "n1", "relation": "limits_scope", "status": "proposed", "contributions": [{"by": "alice", "attribution": "explicit", "mode": "text"}]})
    return state


def body(serves="", updates="None", acceptances="- `fixture-change` revision 1 by `alice`"):
    return f"## What this changes\n\nSomething.\n\n## Reasoning this serves\n\n{serves}\n\n## Tree updates\n\n{updates}\n\n## Accepted change proposals\n\n{acceptances}\n"


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "toy@example.com")
        self.git("config", "user.name", "Toy")
        self.write(toy())
        (self.repo / "README.md").write_text("The study reports a productivity gain.\n")
        self.git("add", STATE, "README.md")
        self.git("commit", "-q", "-m", "base")
        self.git("checkout", "-q", "-b", "change")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True)

    def write(self, state):
        (self.repo / STATE).write_text(yaml.safe_dump(state, sort_keys=False))

    def run_check(self, *args, text=None):
        if text is not None:
            (self.repo / "pr.md").write_text(text)
            args = ("--body-file", str(self.repo / "pr.md"), *args)
        out = io.StringIO()
        with redirect_stdout(out):
            code = check.main(["--base", "main", *args, STATE], cwd=self.repo)
        return code, out.getvalue()

    def test_stated_updates_matching_the_yaml_pass(self):
        self.write(with_link(toy()))
        code, out = self.run_check(text=body(updates="- added `l1` — `n2` limits the scope of `n1`"))
        self.assertEqual(code, 0, out)
        self.assertIn("1 tree update(s) match", out)

    def test_suggested_list_passes_as_written(self):
        state = with_link(toy())
        state["trees"]["current_reality"]["nodes"][0]["status"] = "accepted"
        state["trees"]["current_reality"]["nodes"][0]["accepted_by"] = ["alice"]
        self.write(state)
        code, suggestion = self.run_check("--suggest")
        self.assertEqual(code, 0)
        self.assertIn("- changed `n1`", suggestion)
        self.assertIn("- added `l1`", suggestion)
        code, out = self.run_check(text=body(updates=suggestion))
        self.assertEqual(code, 0, out)

    def test_unstated_yaml_change_fails(self):
        self.write(with_link(toy()))
        code, out = self.run_check(text=body(serves="- `n1`"))
        self.assertEqual(code, 1)
        self.assertIn("The YAML added `l1`", out)

    def test_stated_update_without_yaml_change_fails(self):
        code, out = self.run_check(text=body(updates="- changed `n2`"))
        self.assertEqual(code, 1)
        self.assertIn("does not change it", out)

    def test_wrong_verb_fails(self):
        self.write(with_link(toy()))
        code, out = self.run_check(text=body(updates="- changed `l1`"))
        self.assertEqual(code, 1)
        self.assertIn("shows it added", out)

    def test_removed_item_must_be_stated(self):
        state = toy()
        del state["trees"]["current_reality"]["nodes"][1]
        self.write(state)
        self.assertEqual(self.run_check(text=body(updates="- removed `n2`"))[0], 0)
        self.assertEqual(self.run_check(text=body(serves="- `n1`"))[0], 1)

    def test_serving_existing_reasoning_without_updates_passes(self):
        code, out = self.run_check(text=body(serves="- `n1` — the claim this fix supports"))
        self.assertEqual(code, 0, out)

    def test_serving_unknown_id_fails(self):
        code, out = self.run_check(text=body(serves="- `n9`"))
        self.assertEqual(code, 1)
        self.assertIn("Serves `n9`", out)

    def test_no_reasoning_at_all_fails(self):
        code, out = self.run_check(text=body())
        self.assertEqual(code, 1)
        self.assertIn("names no reasoning", out)

    def test_missing_tree_updates_section_fails(self):
        code, out = self.run_check(text="## Reasoning this serves\n\n- `n1`\n")
        self.assertEqual(code, 1)
        self.assertIn('no "Tree updates" section', out)

    def test_template_comments_are_ignored(self):
        text = body(serves="<!-- e.g. `n9` -->", updates="<!-- - added `n8` -->\nNone")
        code, out = self.run_check(text=text)
        self.assertEqual(code, 1)
        self.assertNotIn("n9", out)
        self.assertNotIn("n8", out)

    def test_missing_acceptance_section_or_reference_fails(self):
        text = body(serves="- `n1`").split("## Accepted change proposals")[0]
        code, out = self.run_check(text=text)
        self.assertEqual(code, 1)
        self.assertIn('no "Accepted change proposals" section', out)
        code, out = self.run_check(text=body(serves="- `n1`", acceptances="<!-- - `fixture-change` revision 1 by `alice` -->"))
        self.assertEqual(code, 1)
        self.assertIn("List at least one recorded acceptance", out)

    def test_unknown_proposal_version_or_participant_fails(self):
        for reference in ("- `unknown` revision 1 by `alice`", "- `fixture-change` revision 2 by `alice`", "- `fixture-change` revision 1 by `bob`"):
            with self.subTest(reference=reference):
                code, out = self.run_check(text=body(serves="- `n1`", acceptances=reference))
                self.assertEqual(code, 1)
                self.assertIn("No recorded acceptance", out)

    def test_malformed_or_duplicate_reference_fails(self):
        for reference in ("yes", "- `fixture-change` revision 0 by `alice`", "- `fixture-change` revision 1 by `alice`\n- `fixture-change` revision 1 by `alice`"):
            with self.subTest(reference=reference):
                code, out = self.run_check(text=body(serves="- `n1`", acceptances=reference))
                self.assertEqual(code, 1)
                self.assertIn("acceptance reference", out)

    def test_malformed_receipt_metadata_fails(self):
        for field, value in (("mode", "voice"), ("by", "assistant"), ("recorded_at", "2026-10-14T12:00:00"), ("scope", ""), ("proposal_revision", True)):
            with self.subTest(field=field):
                state = toy()
                state["change_acceptances"][0][field] = value
                self.write(state)
                code, out = self.run_check(text=body(serves="- `n1`"))
                self.assertEqual(code, 1)
                self.assertIn("Invalid state", out)

    def test_legacy_receipt_without_paths_cannot_cover_a_pr(self):
        state = toy()
        del state["change_acceptances"][0]["approved_paths"]
        self.write(state)
        code, out = self.run_check(text=body(serves="- `n1`"))
        self.assertEqual(code, 1)
        self.assertIn("has no approved_paths", out)

    def test_uncovered_tracked_file_fails(self):
        (self.repo / "extra.md").write_text("Extra change\n")
        self.git("add", "extra.md")
        code, out = self.run_check(text=body(serves="- `n1`"))
        self.assertEqual(code, 1)
        self.assertIn("outside the cited approved scope: extra.md", out)

    def test_unrelated_untracked_files_are_not_part_of_the_pr(self):
        (self.repo / "private-draft.md").write_text("Not included\n")
        (self.repo / "README.md").write_text("The study's scope is call-centre tasks.\n")
        self.assertEqual(self.run_check(text=body(serves="- `n1`"))[0], 0)

    def test_code_only_change_does_not_endorse_reasoning(self):
        (self.repo / "README.md").write_text("The study's scope is call-centre tasks.\n")
        self.assertEqual(self.run_check(text=body(serves="- `n1`"))[0], 0)
        state = yaml.safe_load((self.repo / STATE).read_text())
        self.assertTrue(all(n["status"] == "proposed" for n in state["trees"]["current_reality"]["nodes"]))
        self.assertFalse(any("accepted_by" in n for n in state["trees"]["current_reality"]["nodes"]))

    def test_uncovered_node_or_link_fails_even_when_pr_lists_it(self):
        for category, item in (("nodes", dict(toy()["trees"]["current_reality"]["nodes"][0], id="n3")),
                               ("links", dict(with_link(toy())["trees"]["current_reality"]["links"][0], id="l2"))):
            with self.subTest(category=category):
                state = toy()
                state["trees"]["current_reality"][category].append(item)
                self.write(state)
                code, out = self.run_check(text=body(updates=f"- added `{item['id']}`"))
                self.assertEqual(code, 1)
                self.assertIn(f"outside the cited approved scope: {item['id']}", out)

    def test_multiple_cited_proposals_cover_staged_and_committed_files(self):
        state = toy()
        state["change_acceptances"].append(receipt("extra-change", ["extra.md"]))
        self.write(state)
        (self.repo / "extra.md").write_text("Another approved change\n")
        self.git("add", STATE, "extra.md")
        text = body(serves="- `n1`", acceptances="- `fixture-change` revision 1 by `alice`\n- `extra-change` revision 1 by `alice`")
        self.assertEqual(self.run_check(text=text)[0], 0)
        self.git("commit", "-q", "-m", "approved changes")
        self.assertEqual(self.run_check(text=text)[0], 0)
        self.assertEqual(self.run_check(text=body(serves="- `n1`"))[0], 1)

    def test_rename_requires_approval_for_both_paths(self):
        self.git("mv", "README.md", "renamed.md")
        state = toy()
        state["change_acceptances"].append(receipt("rename", [STATE, "renamed.md"]))
        self.write(state)
        text = body(serves="- `n1`", acceptances="- `rename` revision 1 by `alice`")
        code, out = self.run_check(text=text)
        self.assertEqual(code, 1)
        self.assertIn("outside the cited approved scope: README.md", out)
        text = body(serves="- `n1`", acceptances="- `fixture-change` revision 1 by `alice`\n- `rename` revision 1 by `alice`")
        self.assertEqual(self.run_check(text=text)[0], 0)

    def test_changed_or_removed_earlier_receipt_fails(self):
        for remove in (False, True):
            with self.subTest(remove=remove):
                state = toy()
                if remove:
                    state["change_acceptances"] = []
                else:
                    state["change_acceptances"][0]["source_text"] = "a rewritten reply"
                state["change_acceptances"].append(receipt("new-change"))
                self.write(state)
                code, out = self.run_check(text=body(serves="- `n1`", acceptances="- `new-change` revision 1 by `alice`"))
                self.assertEqual(code, 1)
                self.assertIn("Earlier acceptance receipt was changed or removed", out)

    def test_duplicate_yaml_keys_fail_before_checking_approval(self):
        with (self.repo / STATE).open("a") as handle:
            handle.write("change_acceptances: []\n")
        code, out = self.run_check(text=body(serves="- `n1`"))
        self.assertEqual(code, 1)
        self.assertIn("Duplicate YAML key", out)


if __name__ == "__main__":
    unittest.main()
