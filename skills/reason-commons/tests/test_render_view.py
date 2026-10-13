"""Checks for the in-chat view renderer on a small fixture."""

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/render_view.py"
SPEC = importlib.util.spec_from_file_location("render_view", SCRIPT)
render = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render)


def node(ident, text, status="accepted", **extra):
    item = {"id": ident, "kind": "cause", "text": text, "status": status, "contributions": [{"by": "alice", "attribution": "explicit", "mode": "text"}], **extra}
    if status == "accepted":
        item["accepted_by"] = ["alice"]
    return item


def link(ident, sources, target, status="accepted"):
    item = {"id": ident, "from": sources, "to": target, "relation": "contributes_to", "status": status, "contributions": [{"by": "alice", "attribution": "explicit", "mode": "text"}]}
    if status == "accepted":
        item["accepted_by"] = ["alice"]
    return item


def state():
    nodes = [
        node("a", "Sales is hard"),
        node("b", "No product-market fit"),
        node("c", "No customers"),
        node("d", "Only own time"),
        node("e", "Funding not applied for"),
        node("f", "Loose accepted fact"),
        node("g", "A proposed cause", "proposed"),
        node("h", "A disputed claim", "disputed", challenges=[{"text": "Superseded", "by": "bob"}]),
    ]
    links = [
        link("l1", ["a"], "c"),
        link("l2", ["b"], "c"),
        link("l3", ["c", "e"], "d"),
        link("l4", ["g"], "c", "proposed"),
    ]
    tree = {"nodes": nodes, "links": links, "backlog": []}
    return {"schema_version": 1, "driver": "alice", "participants": {"alice": "Alice", "bob": "Bob"}, "active_tree": "current_reality", "trees": {"current_reality": tree, "goal": {"nodes": [], "links": [], "backlog": []}}}


class RenderViewTests(unittest.TestCase):
    def setUp(self):
        render.PEOPLE.update(alice="Alice", bob="Bob")
        self.tree = state()["trees"]["current_reality"]

    def test_counts_skip_empty_trees_and_zero_standings(self):
        self.assertEqual(render.counts(state()), "Current reality (6 accepted · 1 proposed · 1 disputed)")

    def test_accepted_view_keeps_each_node_once_and_joint_causes_joint(self):
        source, shown, links, common, context = render.mermaid("current_reality", self.tree, "accepted")
        self.assertEqual((len(shown), len(links), context), (6, 3, []))
        self.assertEqual(common, "contributes to")
        labels = re.findall(r'\["(\[A\][^"]*)"\]', source)
        self.assertEqual(len(labels), len(set(labels)), "a node was drawn twice")
        self.assertIn('j3(("AND"))', source)
        self.assertNotIn("A proposed cause", source)
        self.assertIn('subgraph loose["Not yet linked"]', source)

    def test_proposed_view_shows_other_standing_endpoints_as_context(self):
        source, shown, links, _, context = render.mermaid("current_reality", self.tree, "proposed")
        self.assertEqual((shown, context), (["g"], ["c"]))
        self.assertIn("[A] No customers", source)
        self.assertRegex(source, r"class n2 context")
        self.assertIn("-.->", source)

    def test_disputed_view_names_the_objector(self):
        source = render.mermaid("current_reality", self.tree, "disputed")[0]
        self.assertIn("Objection (Bob): Superseded", source)

    def test_text_outline_lists_each_link_once(self):
        outline = render.text_outline("current_reality", self.tree, "accepted")
        self.assertTrue(outline.startswith("CURRENT REALITY — ACCEPTED ONLY (6 nodes, 3 links)"))
        self.assertIn("AND( [A] No customers + [A] Funding not applied for )", outline)
        self.assertEqual(outline.count("<- "), 3)
        self.assertIn("Not yet linked:\n  [A] Loose accepted fact", outline)
        self.assertTrue(outline.endswith("Not shown: 1 proposed, 1 disputed. Say “show proposed” or “show disputed”."))

    def test_widget_embeds_source_safely(self):
        page = render.frame('flowchart LR\n  a["</script> `${x}`"]', "HEAD <b>")
        embedded = re.search(r"mermaid\.render\('rc-[0-9a-f]+', (.*)\);", page).group(1)
        self.assertNotIn("</script>", embedded)
        self.assertEqual(json.loads(embedded.replace("<\\/", "</")), 'flowchart LR\n  a["</script> `${x}`"]')
        self.assertIn("HEAD &lt;b&gt;", page)
        self.assertNotIn("__", page)

    def test_cli_defaults_to_accepted_and_refuses_empty_standing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.yaml"
            path.write_text(yaml.safe_dump(state(), allow_unicode=True))
            run = lambda *a: subprocess.run([sys.executable, str(SCRIPT), str(path), *a], capture_output=True, text=True)
            out = run("--tree", "current_reality")
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn("CURRENT REALITY — ACCEPTED ONLY (6 nodes, 3 links)", out.stdout)
            self.assertIn("ti-arrows-maximize", out.stdout)
            out = run("--tree", "goal")
            self.assertNotEqual(out.returncode, 0)


if __name__ == "__main__":
    unittest.main()
