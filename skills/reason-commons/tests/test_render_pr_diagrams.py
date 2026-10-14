"""Behavioral invariants for generated PR diagrams on the remote-work gold fixture."""

from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/render_pr_diagrams.py"
SPEC = importlib.util.spec_from_file_location("pr_diagrams", SCRIPT)
render = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render)


def node(ident, text, standing="proposed"):
    return {"id": ident, "kind": "observation", "text": text, "status": standing,
            "contributions": [{"by": "alice", "attribution": "explicit", "mode": "text"}]}


def link(ident, sources, target, standing="proposed", relation="limits_scope"):
    return {"id": ident, "from": sources, "to": target, "relation": relation, "status": standing,
            "contributions": [{"by": "alice", "attribution": "explicit", "mode": "text"}]}


def document(nodes=(), links=()):
    return {"fixture.yaml": {"trees": {"current_reality": {"nodes": list(nodes), "links": list(links), "backlog": []}}}}


class PRDiagramTests(unittest.TestCase):
    def setUp(self):
        self.gain = node("gain", "The call-centre study reported a 13% productivity gain on solo call-handling tasks.")
        self.scope = node("scope", "The result may not generalise to creative and collaborative knowledge work.")
        self.limits = link("limits", ["gain"], "scope")

    def test_added_link_includes_actual_endpoints_and_metadata(self):
        before = document([self.gain, self.scope])
        after = document([self.gain, self.scope], [self.limits])
        fragments = render.fragments(before, after)
        self.assertEqual(len(fragments), 1)
        self.assertEqual(fragments[0]["node_ids"], ["gain", "scope"])
        self.assertEqual(fragments[0]["link_ids"], ["limits"])
        source = fragments[0]["source"]
        self.assertIn("[P] CURRENT REALITY · OBSERVATION", source)
        self.assertIn("ADDED · [P] limits scope", source)
        self.assertIn("may not generalise", source)
        self.assertIn("CONTEXT", source)

    def test_changed_statement_shows_previous_and_new_qualifications(self):
        before = document([self.gain])
        revised = deepcopy(self.gain)
        revised["text"] = "The reported gain partially reversed when workers chose to return to the office."
        source = render.fragments(before, document([revised]))[0]["source"]
        self.assertIn('%% node "gain" old', source)
        self.assertIn('%% node "gain" new', source)
        self.assertIn("PREVIOUS", source)
        self.assertIn("CHANGED", source)
        self.assertIn(self.gain["text"], source.replace("<br/>", " "))
        self.assertIn(revised["text"], source.replace("<br/>", " "))

    def test_removal_uses_previous_standing_and_statement(self):
        old = deepcopy(self.scope)
        old["status"] = "accepted"
        before = document([self.gain, old], [self.limits])
        fragment = render.fragments(before, document([self.gain]))[0]
        self.assertIn("REMOVED<br/>[A]", fragment["source"])
        self.assertIn("may not generalise", fragment["source"])
        self.assertEqual(fragment["link_ids"], ["limits"])

    def test_joint_link_keeps_old_and_new_topology(self):
        tasks = node("tasks", "The reported gain concerns solo call-handling tasks specifically.")
        before = document([self.gain, self.scope, tasks], [self.limits])
        joint = deepcopy(self.limits)
        joint["from"] = ["gain", "tasks"]
        joint["relation"] = "qualifies"
        source = render.fragments(before, document([self.gain, self.scope, tasks], [joint]))[0]["source"]
        self.assertIn('%% link "limits" old', source)
        self.assertIn('%% link "limits" new', source)
        self.assertEqual(source.count('(("AND"))'), 1)
        self.assertIn("PREVIOUS · [P] limits scope", source)
        self.assertIn("CHANGED · [P] qualifies", source)

    def test_context_does_not_expand_to_unrelated_branches(self):
        remote = node("other", "An unrelated study result.")
        extra = link("extra", ["scope"], "other")
        before = document([self.gain, self.scope, remote], [self.limits, extra])
        revised = deepcopy(self.gain)
        revised["text"] += " The study was specific to that setting."
        fragment = render.fragments(before, document([revised, self.scope, remote], [self.limits, extra]))[0]
        self.assertEqual(fragment["node_ids"], ["gain", "scope"])
        self.assertEqual(fragment["link_ids"], ["limits"])
        self.assertNotIn("unrelated", fragment["source"])

    def test_disconnected_nodes_stay_disconnected_and_split_into_readable_fragments(self):
        fragments = render.fragments({}, document([self.gain, self.scope]))
        self.assertEqual(len(fragments), 2)
        for fragment in fragments:
            self.assertEqual(len(fragment["node_ids"]), 1)
            self.assertEqual(fragment["link_ids"], [])
            self.assertNotIn("-->", fragment["source"])
            self.assertNotIn(".->", fragment["source"])

    def test_labels_escape_markup_and_opaque_ids_do_not_control_roles(self):
        item = node('end " odd', 'A "quoted" finding & <scope> may apply.')
        item["kind"] = "goal"
        after = document()
        after["fixture.yaml"]["trees"] = {"goal": {"nodes": [item], "links": [], "backlog": []}}
        source = render.fragments({}, after)[0]["source"]
        self.assertIn("[P] GOAL · GOAL", source)
        self.assertIn("#quot;quoted#quot;", source)
        self.assertIn("#amp; #lt;scope#gt;", source)
        self.assertIn('n0["', source)

    def test_rendering_is_deterministic_and_never_changes_state(self):
        after = document([self.gain, self.scope], [self.limits])
        original = deepcopy(after)
        first = render.markdown({}, after)
        self.assertEqual(after, original)
        after["fixture.yaml"]["trees"]["current_reality"]["nodes"].reverse()
        self.assertEqual(first, render.markdown({}, after))

    def test_receipts_and_backlog_do_not_fabricate_tree_changes(self):
        before = document([self.gain])
        after = deepcopy(before)
        after["fixture.yaml"]["change_acceptances"] = [{"scope": "Fixture approval"}]
        after["fixture.yaml"]["trees"]["current_reality"]["backlog"] = [{"ref": "gain", "work": "test_scope"}]
        self.assertEqual(render.fragments(before, after), [])
        self.assertNotIn("```mermaid", render.markdown(before, after))


if __name__ == "__main__":
    unittest.main()
