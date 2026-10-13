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


def toy():
    # Observations from claim-tree-annotation.md, not invented CRT symptoms.
    contribution = [{"by": "alice", "attribution": "explicit", "mode": "text"}]
    texts = ["13% productivity gain for remote workers", "Study covers call centre workers only"]
    nodes = [{"id": f"n{i}", "kind": "observation", "text": text, "status": "proposed", "contributions": deepcopy(contribution)} for i, text in enumerate(texts, 1)]
    return {"schema_version": 1, "project": "Remote-work toy fixture", "driver": "alice", "participants": {"alice": "Alice"}, "active_tree": "current_reality", "trees": {"current_reality": {"nodes": nodes, "links": [], "backlog": []}}}


def with_link(state):
    state["trees"]["current_reality"]["links"].append({"id": "l1", "from": ["n2"], "to": "n1", "relation": "limits_scope", "status": "proposed", "contributions": [{"by": "alice", "attribution": "explicit", "mode": "text"}]})
    return state


def body(serves="", updates="None"):
    return f"## What this changes\n\nSomething.\n\n## Reasoning this serves\n\n{serves}\n\n## Tree updates\n\n{updates}\n"


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "toy@example.com")
        self.git("config", "user.name", "Toy")
        self.write(toy())
        self.git("add", STATE)
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


if __name__ == "__main__":
    unittest.main()
