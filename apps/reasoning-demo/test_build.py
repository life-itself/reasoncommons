"""Meaning, layout and publication-boundary checks; no private repository is needed."""
from copy import deepcopy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urljoin, urlparse

spec = importlib.util.spec_from_file_location("demo_build", Path(__file__).with_name("build.py"))
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
diagrams, pages = build.diagrams, build.pages

try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ModuleNotFoundError:
    HAVE_YAML = False


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


def toy_tree(state, registry):
    tree = build.project(state, registry)["trees"]["goal"]
    return {"name": "goal", "backlog": [], "nodes": tree["nodes"], "links": tree["links"]}


def draw(tree):
    pieces, loose = diagrams.components(tree)
    label = lambda kind: pages.kind_label(tree["name"], kind)
    shapes = [diagrams.geometry(tree, p["ids"], p["links"], label) for p in pieces]
    nodes = {n["id"]: n for n in tree["nodes"]}
    return pieces, shapes, loose, "".join(diagrams.svg(s, nodes, lambda i: f"#{i}", "Toy") for s in shapes)


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

    def test_unreviewed_fields_in_pinned_public_snapshot_fail(self):
        state, registry = fixture()
        data = build.project(state, registry)
        data["trees"]["goal"]["nodes"][0]["private_note"] = "hidden"
        with self.assertRaisesRegex(ValueError, "Unreviewed public fields"):
            build.validate_projection(data, registry)


class DiagramTests(unittest.TestCase):
    def test_joint_connection_meets_at_one_and_with_one_arrow(self):
        pieces, shapes, loose, svg = draw(toy_tree(*fixture()))
        self.assertEqual(svg.count('<a class="j '), 1)
        self.assertEqual(svg.count('class="e-head"'), 1)
        self.assertEqual(loose, ["loose"])
        self.assertNotIn('data-id="loose"', svg)

    def test_text_is_escaped_in_cards_diagrams_and_outlines(self):
        state, registry = fixture()
        state["trees"]["goal"]["nodes"][0]["text"] = '<script>alert("x")</script>'
        tree = toy_tree(state, registry)
        pieces, shapes, loose, svg = draw(tree)
        outline = diagrams.outline(tree, pieces[0]["ids"], pieces[0]["links"], lambda i: f"#{i}", lambda k: k)
        for output in (svg, outline):
            self.assertNotIn("<script>", output)
            self.assertIn("&lt;script&gt;", output)

    def test_cycles_are_refused_rather_than_redrawn(self):
        tree = {"name": "current_reality", "nodes": [{"id": i, "kind": "cause", "text": i, "status": "accepted"} for i in "ab"],
                "links": [{"id": "ab", "from": ["a"], "to": "b", "relation": "contributes_to", "status": "accepted"},
                          {"id": "ba", "from": ["b"], "to": "a", "relation": "contributes_to", "status": "accepted"}]}
        with self.assertRaisesRegex(ValueError, "cycle"):
            draw(tree)

    def test_wrapping_never_exceeds_the_box(self):
        for line in diagrams.wrap("Supercalifragilisticexpialidocious-and-then-some " * 3, 120):
            self.assertLessEqual(diagrams.text_width(line, diagrams.TEXT_SIZE, diagrams.TEXT_WEIGHT), 120)


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site, cls.commons = build.load_site()
        cls.outputs = build.build_files(cls.site, cls.commons)
        cls.by_kind = {c["entry"]["kind"]: c for c in cls.commons}
        cls.real, cls.example = cls.by_kind["real"], cls.by_kind["example"]

    def trees(self):
        for c in self.commons:
            for name, tree in build.normalize(c)["trees"].items():
                yield c, name, tree

    def test_outputs_are_exactly_the_approved_files(self):
        pages_ = ["index", "map", "goal", "in-the-way", "conflict", "change", "prerequisites", "actions", "items", "changes", "about"]
        fonts = ["alegreya-sans-400.woff2", "alegreya-sans-500.woff2", "alegreya-sans-700.woff2", "alegreya-sans-400-italic.woff2", "OFL.txt"]
        expected = {"index.html", "how-it-works.html", "styles.css", "app.js", "reasoning.json", *(f"fonts/{f}" for f in fonts),
                    *(f"reason-commons/{p}.html" for p in pages_), "reason-commons/reasoning.json",
                    *(f"example-willow-lane/{p}.html" for p in pages_ + ["questions", "learning"]), "example-willow-lane/reasoning.json",
                    *(f"gandhi-2-0/{p}.html" for p in pages_ + ["questions"]), "gandhi-2-0/reasoning.json"}
        self.assertEqual(set(self.outputs), expected)

    def test_our_reviewed_snapshot_is_unchanged(self):
        data = self.real["data"]
        self.assertEqual(sum(len(t["nodes"]) for t in data["trees"].values()), 50)
        self.assertEqual(sum(len(t["links"]) for t in data["trees"].values()), 14)
        self.assertEqual([k for k, t in data["trees"].items() if t["links"]], ["goal", "current_reality"])
        self.assertEqual(json.loads(self.outputs["reasoning.json"]), data)
        self.assertEqual(json.loads(self.outputs["reason-commons/reasoning.json"]), data)

    def test_snapshot_tampering_fails(self):
        registry = deepcopy(self.real["registry"])
        registry["snapshot"]["trees"]["goal"]["nodes"][0]["text"] = "A changed statement."
        build.validate_projection(registry["snapshot"], registry)
        self.assertNotEqual(build.digest(registry["snapshot"]), registry["snapshot_sha256"])

    def test_every_published_link_is_drawn_once_and_nothing_else(self):
        for c, name, tree in self.trees():
            pieces, loose = diagrams.components(tree)
            label = lambda kind, name=name: pages.kind_label(name, kind)
            svg = "".join(diagrams.svg(diagrams.geometry(tree, p["ids"], p["links"], label), {n["id"]: n for n in tree["nodes"]}, lambda i: i, name) for p in pieces)
            drawn = set(re.findall(r'<a class="e [^"]*" href="[^"]*" data-id="([^"]+)"', svg))
            self.assertEqual(drawn, {l["id"] for l in tree["links"]}, (c["entry"]["slug"], name))
            heads = sum(1 for l in tree["links"] if l["relation"] != "conflicts_with")
            self.assertEqual(svg.count('class="e-head"'), heads, (c["entry"]["slug"], name))
            self.assertEqual(svg.count('<a class="j '), sum(len(l["from"]) > 1 for l in tree["links"]), (c["entry"]["slug"], name))
            self.assertEqual(set(loose) | {i for p in pieces for i in p["ids"]}, {n["id"] for n in tree["nodes"]})

    def test_trees_without_accepted_links_draw_no_arrows(self):
        for name in ("conflict", "future_reality", "prerequisite", "transition"):
            page = self.outputs[f'reason-commons/{pages.TREES[name]["slug"]}.html']
            self.assertNotIn('class="e-head"', page, name)
            self.assertNotIn('<a class="j ', page, name)

    def test_boxes_never_overlap_and_text_fits(self):
        for c, name, tree in self.trees():
            label = lambda kind, name=name: pages.kind_label(name, kind)
            pieces, loose = diagrams.components(tree)
            shapes = [diagrams.geometry(tree, p["ids"], p["links"], label) for p in pieces]
            if not tree["links"] and name == "conflict":
                shapes.append(diagrams.geometry(tree, [n["id"] for n in tree["nodes"]], [], label))
            for shape in shapes:
                boxes = list(shape["nodes"].values())
                for i, a in enumerate(boxes):
                    for line in a["lines"]:
                        self.assertLessEqual(diagrams.text_width(line, diagrams.TEXT_SIZE, diagrams.TEXT_WEIGHT), a["w"] - 2 * diagrams.PAD_X)
                    self.assertGreaterEqual(a["x"], 0)
                    self.assertLessEqual(a["x"] + a["w"], shape["w"])
                    for b in boxes[i + 1:]:
                        apart = a["x"] + a["w"] <= b["x"] or b["x"] + b["w"] <= a["x"] or a["y"] + a["h"] <= b["y"] or b["y"] + b["h"] <= a["y"]
                        self.assertTrue(apart, (c["entry"]["slug"], name))

    def test_cloud_places_each_position_beside_the_need_it_serves(self):
        tree = build.normalize(self.example)["trees"]["conflict"]
        shape = diagrams.geometry(tree, [n["id"] for n in tree["nodes"]], tree["links"], lambda k: k)
        middle = lambda i: shape["nodes"][i]["y"] + shape["nodes"][i]["h"] / 2
        self.assertAlmostEqual(middle("wl-c-close"), middle("wl-c-need-safe"), delta=12)
        self.assertAlmostEqual(middle("wl-c-keep-open"), middle("wl-c-need-trade"), delta=12)

    def test_every_example_page_is_labelled_fictional_and_ours_never_is(self):
        for name, value in self.outputs.items():
            if not name.endswith(".html"):
                continue
            if name.startswith("example-willow-lane/"):
                self.assertIn('class="example-banner"', value, name)
                self.assertIn("Fictional example", value, name)
            elif name.startswith("reason-commons/"):
                self.assertNotIn("example-banner", value, name)
                self.assertNotIn("Willow Lane", value, name)
        self.assertTrue(json.loads(self.outputs["example-willow-lane/reasoning.json"])["is_example"])

    def test_every_item_is_readable_without_script(self):
        for c in self.commons:
            page = self.outputs[f'{c["entry"]["slug"]}/items.html']
            for tree in c["data"]["trees"].values():
                for item in tree["nodes"] + tree["links"]:
                    self.assertIn(f' id="{item["id"]}"', page)  # Not a diagram's data-id.
                    if "text" in item:
                        self.assertIn(build.esc(item["text"]), page)
        self.assertIn("Original contributor not identified", self.outputs["reason-commons/items.html"])

    def test_prior_endorsement_of_a_disputed_item_is_not_current_acceptance(self):
        page = self.outputs["example-willow-lane/items.html"]
        article = page[page.index(' id="wl-c-rel-open"'):page.index(' id="wl-c-rel-clash"')]
        facts = article[article.index('class="item-facts"'):article.index("</aside>")]
        self.assertIn("Disputed; earlier accepted by Tomasz", facts)
        self.assertNotIn("Accepted for now", facts)  # Its endpoints' cards may still be accepted.

    def test_learning_keeps_awaiting_unclear_and_not_assessed_apart(self):
        page = self.outputs["example-willow-lane/learning.html"]
        for word in ("Awaiting report", "Unclear", "Not assessed", "Not observed", "Observed"):
            self.assertIn(word, page)
        self.assertIn("Still to report: Amara", page)

    def test_internal_links_and_anchors_resolve(self):
        class Collect(HTMLParser):
            def __init__(self):
                super().__init__()
                self.links, self.ids = [], set()

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if attrs.get("id"):
                    self.ids.add(attrs["id"])
                if attrs.get("href"):
                    self.links.append(attrs["href"])
        parsed = {}
        for name, value in self.outputs.items():
            if name.endswith(".html"):
                parsed[name] = Collect()
                parsed[name].feed(value)
        for name, page in parsed.items():
            for href in page.links:
                url = urlparse(href)
                if url.scheme or href.startswith("/"):
                    continue  # Site-wide routes are checked by scripts/check-website.py.
                target = urljoin(name, url.path) if url.path else name
                self.assertTrue(target in self.outputs, (name, href))
                if url.fragment and target.endswith(".html"):
                    self.assertIn(url.fragment, parsed[target].ids, (name, href))

    def test_legacy_query_routes_redirect_to_the_new_pages(self):
        home = self.outputs["index.html"]
        for fragment in ("q.get('view')", "q.get('item')", "items.html#", "about.html", "location.replace"):
            self.assertIn(fragment, home)

    def test_public_artifacts_exclude_internal_state_and_mock_content(self):
        text = "\n".join(v for v in self.outputs.values() if isinstance(v, str))
        for forbidden in ("Calder", "1,284", "2,390", "change_acceptances", "feedback_requests", "/Users/", "driver_default", "funding/research/", "r-e-rufus-feedback-hard"):
            self.assertNotIn(forbidden, text)


class ExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        site, commons = build.load_site()
        cls.entry, cls.registry, cls.data = next((c["entry"], c["registry"], c["data"]) for c in commons if c["entry"]["kind"] == "example")
        cls.real_ids = {i["id"] for c in commons if c["entry"]["kind"] == "real" for t in c["data"]["trees"].values() for i in t["nodes"] + t["links"]}

    @unittest.skipUnless(HAVE_YAML, "PyYAML is needed to read the example's working file")
    def test_working_file_passes_the_skill_validator_and_matches_the_snapshot(self):
        module = build.skill_helpers()
        state = module.load(build.HERE / self.entry["source"])
        module.validate(state)
        self.assertEqual(build.project_v2(state, self.registry), self.data)

    def test_example_holds_every_standing_and_kind_of_qualification(self):
        items = [i for t in self.data["trees"].values() for i in t["nodes"] + t["links"]]
        self.assertEqual({i["status"] for i in items}, {"accepted", "proposed", "disputed"})
        self.assertTrue(any(i.get("assumptions") for i in items) and any(i.get("challenges") for i in items))
        self.assertTrue(any(len(i.get("from", [])) > 1 for i in items))
        self.assertTrue(all(t["links"] for t in self.data["trees"].values()))
        self.assertEqual(len(self.data["history"]), 3)

    def test_example_ids_never_collide_with_ours(self):
        ids = {i["id"] for t in self.data["trees"].values() for i in t["nodes"] + t["links"]}
        self.assertFalse(ids & self.real_ids)
        self.assertTrue(all(i.startswith("wl-") for i in ids))

    def test_accepted_link_needs_accepted_endpoints(self):
        data = deepcopy(self.data)
        link = next(l for l in data["trees"]["future_reality"]["links"] if l["id"] == "wl-f-rel-fewer")
        target = next(n for n in data["trees"]["future_reality"]["nodes"] if n["id"] == link["to"])
        target.update(status="proposed", accepted_by=[])
        with self.assertRaisesRegex(ValueError, "accepted endpoints"):
            build.validate_v2(data, self.registry)

    def test_history_cannot_mention_unpublished_material(self):
        data = deepcopy(self.data)
        data["history"][0]["changes"][0]["refs"].append("wl-not-published")
        with self.assertRaisesRegex(ValueError, "unpublished"):
            build.validate_v2(data, self.registry)

    def test_projection_two_is_reserved_for_the_labelled_example(self):
        registry = deepcopy(self.registry)
        registry["is_example"] = False
        with self.assertRaisesRegex(ValueError, "fictional example"):
            build.validate_v2(self.data, registry)


class ReconstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site, cls.commons = build.load_site()
        cls.record = next(c for c in cls.commons if c["entry"]["kind"] == "reconstruction")
        cls.registry, cls.data = cls.record["registry"], cls.record["data"]
        cls.outputs = build.build_files(cls.site, cls.commons)

    @unittest.skipUnless(HAVE_YAML, "PyYAML is needed for the public working file")
    def test_public_working_file_validates_and_matches_exactly(self):
        helper = build.skill_helpers()
        state = helper.load(build.HERE / self.record["entry"]["source"])
        helper.validate(state)
        self.assertEqual(build.project_reconstruction(state, self.registry), self.data)
        self.assertEqual(sum(len(t["nodes"]) for t in self.data["trees"].values()), 42)
        self.assertEqual(sum(len(t["links"]) for t in self.data["trees"].values()), 35)

    def test_existing_reviewed_snapshots_remain_byte_for_byte_the_same(self):
        expected = {"real": "994c61a3deda57223fb20a363897d00c999bdf3244294d2601ee1fe100c39cfd",
                    "example": "f4319cd397cb6b7562f4399f7425d8613190a78aedf936304be63b0003597c1e"}
        for record in self.commons:
            if record["entry"]["kind"] in expected:
                self.assertEqual(build.digest(record["data"]), expected[record["entry"]["kind"]])

    def test_reconstruction_cannot_imply_endorsement_or_direct_human_authorship(self):
        for change, expected in [({"status": "accepted", "accepted_by": ["David Joseph"]}, "remain proposed"),
                                 ({"contributors": [{"name": "David Joseph", "role": "human"}]}, "participant authorship")]:
            data = deepcopy(self.data)
            data["trees"]["goal"]["nodes"][0].update(change)
            with self.assertRaisesRegex(ValueError, expected):
                build.validate_reconstruction(data, self.registry)

    def test_every_item_requires_a_known_source_and_an_explicit_basis(self):
        for refs in [[], [{"source_id": "invented", "locator": "p. 2", "basis": "reconstruction"}],
                     [{"source_id": "analysis-v2", "locator": "", "basis": "inference"}],
                     [{"source_id": "analysis-v2", "locator": "p. 2", "basis": "verified"}]]:
            data = deepcopy(self.data)
            data["trees"]["goal"]["nodes"][0]["source_refs"] = refs
            with self.assertRaisesRegex(ValueError, "source locator"):
                build.validate_reconstruction(data, self.registry)

    def test_feedback_and_earlier_endorsement_cannot_be_invented(self):
        data = deepcopy(self.data)
        data["feedback"] = [{"reports": [{"text": "It worked"}]}]
        with self.assertRaisesRegex(ValueError, "feedback commitments or reports"):
            build.validate_reconstruction(data, self.registry)
        data = deepcopy(self.data)
        data["history"][0]["changes"][0]["type"] = "accepted"
        with self.assertRaisesRegex(ValueError, "prior endorsement or results"):
            build.validate_reconstruction(data, self.registry)

    @unittest.skipUnless(HAVE_YAML, "PyYAML is needed for the public working file")
    def test_only_selected_public_fields_cross_the_reconstruction_boundary(self):
        state = build.skill_helpers().load(build.HERE / self.record["entry"]["source"])
        state["change_acceptances"] = [{"source_text": "PRIVATE_CANARY"}]
        for tree in state["trees"].values():
            for item in tree["nodes"] + tree["links"]:
                item.update(private_note="PRIVATE_CANARY", source={"path": "/PRIVATE_CANARY"})
                item["contributions"][0]["note"] = "PRIVATE_CANARY"
        self.assertNotIn("PRIVATE_CANARY", json.dumps(build.project_reconstruction(state, self.registry)))
        data = deepcopy(self.data)
        data["trees"]["goal"]["nodes"][0]["source"] = {"path": "/PRIVATE_CANARY"}
        with self.assertRaisesRegex(ValueError, "Unreviewed public fields"):
            build.validate_reconstruction(data, self.registry)

    def test_every_reconstruction_page_is_labelled_and_sources_are_inspectable(self):
        for name, value in self.outputs.items():
            if name.startswith("gandhi-2-0/") and name.endswith(".html"):
                self.assertIn('class="reconstruction-banner"', value, name)
                self.assertIn("participants have not endorsed", value, name)
                self.assertNotIn("Fictional example", value, name)
        items = self.outputs["gandhi-2-0/items.html"]
        forum = next(s for s in self.data["sources"] if "posts" in s)
        for tree in self.data["trees"].values():
            for item in tree["nodes"] + tree["links"]:
                for ref in item["source_refs"]:  # A forum credit links its post; anything else names its locator.
                    self.assertIn(pages.esc(f'{forum["url"]}/{ref["post"]}') if "post" in ref else pages.esc(ref["locator"]), items)
        for source in self.data["sources"]:
            self.assertIn(f'id="source-{source["id"]}"', self.outputs["gandhi-2-0/about.html"])
        self.assertIn("Inferred by the AI", items)
        self.assertIn("Paraphrased by the AI from this post", items)

    def test_overview_and_briefs_keep_the_trial_and_participation_provisional(self):
        overview = self.outputs["gandhi-2-0/index.html"]
        for wording in ("First step · Unassigned", "No trial is recorded here", "What would change our minds?", "suppress"):
            self.assertIn(wording, overview)
        self.assertNotIn("The change chosen", overview)
        c = pages.Commons(build.normalize(self.record))
        for ident in c.order:
            brief = pages.brief(c, ident, self.site)
            self.assertIn("Sources:", brief)
            self.assertIn("participants have not endorsed", brief)
            self.assertIn("Copying this brief submits nothing", brief)
        self.assertNotIn("gandhi-2-0/learning.html", self.outputs)

    def test_source_text_is_escaped_and_does_not_execute_markup(self):
        registry = deepcopy(self.registry)
        data = deepcopy(self.data)
        payload = '<img src=x onerror="alert(1)">'
        data["sources"][0]["title"] = payload
        registry["sources"][0]["title"] = payload
        data["trees"]["goal"]["nodes"][0]["source_refs"][-1]["locator"] = payload  # The analysis locator, after the forum credits.
        build.validate_reconstruction(data, registry)
        c = pages.Commons(build.normalize({**self.record, "data": data, "registry": registry}))
        for rendered in (pages.about_page(c, self.site), pages.items_page(c, self.site)):
            self.assertNotIn(payload, rendered)
            self.assertIn(pages.esc(payload), rendered)

    def test_conflict_outline_names_the_conflict_instead_of_implying_a_sequence(self):
        clashes = [l["id"] for l in self.data["trees"]["conflict"]["links"] if l["relation"] == "conflicts_with"]
        self.assertEqual(len(clashes), 5)
        for file, expected in (("gandhi-2-0/index.html", clashes[:1]), ("gandhi-2-0/conflict.html", clashes)):
            self.assertNotIn('class="o-then">then', self.outputs[file])
            for ident in expected:
                self.assertIn(f'href="items.html#{ident}">conflicts with</a>', self.outputs[file])

    def broken(self, change, registry_too=False):
        """Validate a copy of the release after one change, expecting refusal."""
        data, registry = deepcopy(self.data), deepcopy(self.registry)
        change(data)
        if registry_too:
            change(registry)
        return lambda: build.validate_reconstruction(data, registry)

    def ref(self, data, ident, source_id):
        item = next(i for t in data["trees"].values() for i in t["nodes"] + t["links"] if i["id"] == ident)
        return next(r for r in item["source_refs"] if r["source_id"] == source_id)

    def test_a_credit_must_name_the_author_of_the_cited_post(self):
        self.assertEqual(self.ref(self.data, "g2-c-optional", "forum"), {"source_id": "forum", "post": 30, "author": "robert", "basis": "paraphrase"})
        swap = self.broken(lambda d: self.ref(d, "g2-c-optional", "forum").update(author="leif"))
        self.assertRaisesRegex(ValueError, "author of post 30", swap)

    def test_credits_need_a_real_post_or_locator_and_a_basis_that_fits_the_source(self):
        for change in (lambda r: r.update(post=99), lambda r: r.update(post="30"), lambda r: r.update(basis="cited"),
                       lambda r: r.update(quote="Words lifted from the post"), lambda r: r.pop("author")):
            check = self.broken(lambda d, change=change: change(self.ref(d, "g2-c-optional", "forum")))
            self.assertRaisesRegex(ValueError, "source locator", check)
        essay = self.broken(lambda d: self.ref(d, "g2-c-k5-objective", "last-first").update(basis="paraphrase"))
        self.assertRaisesRegex(ValueError, "source locator", essay)

    def test_a_document_must_be_shared_in_a_post_by_its_author(self):
        def move(record):
            next(s for s in record["sources"] if s["id"] == "paradox")["shared_in_post"] = 30  # Robert's post.
        self.assertRaisesRegex(ValueError, "shared in a post by its author", self.broken(move, registry_too=True))

    def test_views_cover_every_statement_and_never_split_a_conflict(self):
        def drop(record):
            record["views"]["conflict"][0]["nodes"].remove("g2-c-k1-distribute")
        self.assertRaisesRegex(ValueError, "splits the connection", self.broken(drop, registry_too=True))
        def lose(record):
            del record["views"]["conflict"][4]
        self.assertRaisesRegex(ValueError, "must appear in a view", self.broken(lose, registry_too=True))

    def test_all_five_conflicts_draw_as_clouds_with_credit_lines_that_fit(self):
        c = pages.Commons(build.normalize(self.record))
        tree = c.trees["conflict"]
        for view in c.views["conflict"]:
            nodes = {n["id"]: n for n in tree["nodes"] if n["id"] in view["nodes"]}
            links = [l for l in tree["links"] if l["to"] in nodes]
            self.assertIsNotNone(diagrams.cloud_roles(nodes, links), view["id"])
            shape = diagrams.geometry(tree, view["nodes"], links, lambda k: pages.kind_label("conflict", k))
            for placed in shape["nodes"].values():
                self.assertTrue(placed["credit"])
                for line in placed["credit"]:
                    self.assertLessEqual(diagrams.text_width(line, diagrams.CREDIT_SIZE, diagrams.CREDIT_WEIGHT), placed["w"] - 2 * diagrams.PAD_X)
            self.assertIn(f'id="view-{view["id"]}"', self.outputs["gandhi-2-0/conflict.html"])
        page = self.outputs["gandhi-2-0/conflict.html"]
        self.assertEqual(page.count("e-conflict"), 5)
        self.assertIn('class="n-credit"', page)
        self.assertIn("From Robert Bunge", page)

    def test_every_credited_post_is_linked_and_people_are_counted(self):
        forum = next(s for s in self.data["sources"] if "posts" in s)
        cited = {r["post"] for t in self.data["trees"].values() for i in t["nodes"] + t["links"] for r in i["source_refs"] if "post" in r}
        items = self.outputs["gandhi-2-0/items.html"]
        for post in cited:
            self.assertIn(f'href="{forum["url"]}/{post}"', items)
        overview = self.outputs["gandhi-2-0/index.html"]
        self.assertIn('id="credits"', overview)
        for name in ("Leif Eriksson", "Robert Bunge", "The supplied analysis alone"):
            self.assertIn(name, overview)
        self.assertNotIn(">Justin<", overview)  # Listed as a thread author, but nothing in this release draws on his post.

    def test_conflict_line_is_styled_apart_from_proposed_lines(self):
        css = self.outputs["styles.css"]
        proposed = css.index(".rc-diagram .e.is-proposed .e-line{")
        conflict = css.index(".rc-diagram .e.e-conflict .e-line{stroke:var(--clay)")
        self.assertGreater(conflict, proposed)  # Equal specificity, so the later rule wins.

    def test_release_is_readable_without_a_download_or_script(self):
        about = self.outputs["gandhi-2-0/about.html"]
        self.assertIn('id="release-json"', about)
        self.assertIn(pages.esc(build.normalize(self.record)["json"]), about)
        self.assertIn("Read or copy this release", about)
        self.assertNotIn(" download", about)


if __name__ == '__main__':
    unittest.main()
