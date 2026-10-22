"""Meaning and publication-boundary checks; no private repository is needed."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("demo_build", Path(__file__).with_name("build.py"))
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def node(ident, text="A useful condition.", status="accepted"):
    return {"id": ident, "kind": "goal" if ident == "goal" else "necessary_condition", "text": text, "status": status,
            "accepted_by": ["david"], "acceptance_source": "Accepted in the toy review.",
            "contributions": [{"by": "david", "attribution": "explicit", "mode": "text"}]}


def fixture():
    state = {"schema_version": 1, "trees": {"goal": {"nodes": [node("goal"), node("first"), node("second"), node("loose")],
             "links": [{"id": "joint", "from": ["first", "second"], "to": "goal", "relation": "necessary_for", "status": "accepted",
                        "accepted_by": ["david"], "acceptance_source": "Accepted in the toy review.",
                        "contributions": [{"by": "assistant", "attribution": "assistant", "mode": "text"}]}], "backlog": []}}}
    registry = {"registry_version": 1, "release": {"release_id": "toy.1", "snapshot_date": "2026-10-22", "title": "Toy project"},
                "people": {"david": "David Joseph"}, "selection": {"goal": {"nodes": ["goal", "first", "second", "loose"], "links": ["joint"]}}}
    return state, registry


class ExportTests(unittest.TestCase):
    def test_only_explicitly_selected_accepted_fields_cross_boundary(self):
        state, registry = fixture()
        state["change_acceptances"] = [{"source_text": "RECEIPT_CANARY"}]
        state["trees"]["goal"]["nodes"].extend([node("private-accepted", "ACCEPTED_CANARY"), node("private-proposed", "PROPOSED_CANARY", "proposed"), node("private-disputed", "DISPUTED_CANARY", "disputed")])
        for item in state["trees"]["goal"]["nodes"]:
            item.update(source={"path": "/PRIVATE_PATH_CANARY"}, assumptions=[{"text": "ASSUMPTION_CANARY"}], challenges=[{"text": "CHALLENGE_CANARY"}])
            item["contributions"][0]["note"] = "NOTE_CANARY"
        state["trees"]["goal"]["backlog"] = [{"note": "BACKLOG_CANARY"}]
        output = json.dumps(build.project(state, registry))
        self.assertNotIn("CANARY", output)

    def test_selected_downgrade_fails_instead_of_publishing_stale_acceptance(self):
        for standing in ("proposed", "disputed"):
            state, registry = fixture()
            state["trees"]["goal"]["nodes"][1]["status"] = standing
            with self.assertRaisesRegex(ValueError, "no longer accepted"):
                build.project(state, registry)

    def test_connection_downgrade_fails(self):
        state, registry = fixture()
        state["trees"]["goal"]["links"][0]["status"] = "proposed"
        with self.assertRaisesRegex(ValueError, "no longer accepted"):
            build.project(state, registry)

    def test_partial_joint_connection_fails(self):
        state, registry = fixture()
        registry["selection"]["goal"]["nodes"].remove("second")
        with self.assertRaisesRegex(ValueError, "Missing accepted endpoint"):
            build.project(state, registry)

    def test_missing_source_id_fails(self):
        state, registry = fixture()
        registry["selection"]["goal"]["nodes"].append("missing")
        with self.assertRaisesRegex(ValueError, "missing"):
            build.project(state, registry)

    def test_unknown_versions_fail(self):
        state, registry = fixture()
        state["schema_version"] = 20
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            build.project(state, registry)

    def test_unknown_names_are_not_silently_published(self):
        state, registry = fixture()
        state["trees"]["goal"]["nodes"][0]["accepted_by"] = ["not-selected"]
        with self.assertRaisesRegex(ValueError, "Unselected endorser"):
            build.project(state, registry)

    def test_unknown_original_contributor_is_not_the_driver(self):
        state, registry = fixture()
        state["trees"]["goal"]["nodes"][0]["contributions"] = [{"by": "david", "attribution": "driver_default", "mode": "unknown"}]
        output = build.project(state, registry)["trees"]["goal"]["nodes"][0]
        self.assertEqual(output["contributors"], [{"name": "Original contributor not identified", "role": "unknown"}])
        self.assertEqual(output["accepted_by"], ["David Joseph"])

    def test_ai_origin_and_human_endorsement_are_separate(self):
        state, registry = fixture()
        link = build.project(state, registry)["trees"]["goal"]["links"][0]
        self.assertEqual(link["contributors"], [{"name": "AI assistant", "role": "assistant"}])
        self.assertEqual(link["accepted_by"], ["David Joseph"])

    def test_unknown_channel_does_not_erase_explicit_authorship(self):
        state, registry = fixture()
        state["trees"]["goal"]["nodes"][0]["contributions"][0]["mode"] = "unknown"
        item = build.project(state, registry)["trees"]["goal"]["nodes"][0]
        self.assertEqual(item["contributors"], [{"name": "David Joseph", "role": "human"}])

    def test_joint_graph_preserves_and_and_disconnected_statement(self):
        state, registry = fixture()
        tree = build.project(state, registry)["trees"]["goal"]
        graph = build.graph(tree, "goal")
        self.assertEqual(graph.count('class="and-junction"'), 1)
        self.assertEqual(graph.count('marker-end='), 1)
        self.assertIn('Not yet connected', graph)
        self.assertIn('data-item="loose"', graph)

    def test_text_is_escaped_in_cards_and_diagrams(self):
        state, registry = fixture()
        state["trees"]["goal"]["nodes"][0]["text"] = '<script>alert("x")</script>'
        tree = build.project(state, registry)["trees"]["goal"]
        output = build.item_card(tree["nodes"][0], "goal") + build.graph(tree, "goal")
        self.assertNotIn('<script>', output)
        self.assertIn('&lt;script&gt;', output)

    def test_unreviewed_fields_in_pinned_public_snapshot_fail(self):
        state, registry = fixture()
        data = build.project(state, registry)
        data["trees"]["goal"]["nodes"][0]["private_note"] = "hidden"
        with self.assertRaisesRegex(ValueError, "Unreviewed public fields"):
            build.validate_projection(data, registry)


class ReviewedSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.registry = build.read_json(build.HERE / "publication.json")

    def test_approved_totals_and_all_connections_are_closed(self):
        data = self.registry["snapshot"]
        build.validate_projection(data, self.registry)
        self.assertEqual(sum(len(t["nodes"]) for t in data["trees"].values()), 50)
        self.assertEqual(sum(len(t["links"]) for t in data["trees"].values()), 14)
        self.assertEqual([k for k,t in data["trees"].items() if t["links"]], ["goal", "current_reality"])

    def test_snapshot_tampering_fails(self):
        self.registry["snapshot"]["trees"]["goal"]["nodes"][0]["text"] = "A changed statement."
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            build.build_files(self.registry)

    def test_inline_public_json_cannot_close_its_script_element(self):
        import re
        self.registry["snapshot"]["trees"]["goal"]["nodes"][0]["text"] = '</script><script>alert("CANARY")</script>'
        self.registry["snapshot_sha256"] = build.digest(self.registry["snapshot"])
        output = build.build_files(self.registry)["index.html"]
        inline = re.search(r'<script type="application/json" id="public-record">(.*?)</script>', output, re.S).group(1)
        self.assertNotIn('<script>', inline)
        self.assertEqual(json.loads(inline), self.registry["snapshot"])

    def test_generated_page_has_complete_script_free_record(self):
        output = build.build_files(self.registry)["index.html"]
        for tree in self.registry["snapshot"]["trees"].values():
            for item in tree["nodes"] + tree["links"]:
                self.assertIn(f'id="item-{item["id"]}"', output)
        self.assertIn('Original contributor not identified', output)
        self.assertIn('No outcome reports in this selection', output)
        self.assertNotIn('<!-- OVERVIEW -->', output)

    def test_public_artifacts_exclude_internal_state_and_mock_content(self):
        outputs = build.build_files(self.registry)
        text = '\n'.join(outputs.values())
        for forbidden in ('Calder', '1,284', '2,390', 'change_acceptances', 'feedback_requests', '/Users/', 'driver_default', 'funding/research/', 'r-e-rufus-feedback-hard'):
            self.assertNotIn(forbidden, text)


if __name__ == '__main__':
    unittest.main()
