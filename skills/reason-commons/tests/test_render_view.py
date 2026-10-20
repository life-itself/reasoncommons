"""Checks for the in-chat view renderer on a small fixture."""

import importlib.util
import json
import os
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
        self.assertIn("[A] CURRENT REALITY · CAUSE<br/>No customers", source)
        self.assertRegex(source, r"class n2 context")
        self.assertIn("-.->", source)

    def test_disputed_view_names_the_objector(self):
        source = render.mermaid("current_reality", self.tree, "disputed")[0]
        self.assertIn("Objection (Bob): Superseded", source)

    def test_node_metadata_comes_from_tree_and_kind_and_preserves_statement(self):
        examples = {
            "goal": "necessary_condition",
            "current_reality": "undesirable_effect",
            "conflict": "prerequisite",
            "future_reality": "injection",
            "prerequisite": "obstacle",
            "transition": "expected_effect",
        }
        for tree, kind in examples.items():
            with self.subTest(tree=tree, kind=kind):
                # The ID deliberately does not encode the tree or kind.
                item = node("opaque-id", 'A qualified statement: sometimes "this" holds.', "proposed", kind=kind)
                content = {"nodes": [item], "links": [], "backlog": []}
                source = render.mermaid(tree, content, "proposed")[0]
                metadata = f"[P] {tree.replace('_', ' ').upper()} · {kind.replace('_', ' ').upper()}"
                self.assertIn(metadata + "<br/>", source)
                self.assertIn(render.escape(item["text"]), source)
                outline = render.text_outline(tree, content, "proposed")
                self.assertIn(metadata + ": " + item["text"], outline)

    def test_markdown_view_preserves_topology_and_scope_for_each_standing(self):
        for standing in render.STANDINGS:
            with self.subTest(standing=standing):
                source, shown, links, common, context = render.mermaid("current_reality", self.tree, standing)
                response = render.markdown("current_reality", self.tree, standing)
                embedded = response.split("```mermaid\n", 1)[1].split("\n```", 1)[0]
                self.assertEqual(embedded, source)
                self.assertEqual(response.splitlines()[0], render.heading("current_reality", standing, shown, links, context))
                self.assertTrue(response.endswith(render.not_shown(self.tree, standing)))
                if common:
                    self.assertIn(f"Each arrow reads “{common}”.", response)

    def test_text_outline_lists_each_link_once(self):
        outline = render.text_outline("current_reality", self.tree, "accepted")
        self.assertTrue(outline.startswith("CURRENT REALITY — ACCEPTED ONLY (6 nodes, 3 links)"))
        self.assertIn("AND( [A] CURRENT REALITY · CAUSE: No customers + [A] CURRENT REALITY · CAUSE: Funding not applied for )", outline)
        self.assertEqual(outline.count("<- "), 3)
        self.assertIn("Not yet linked:\n  [A] CURRENT REALITY · CAUSE: Loose accepted fact", outline)
        self.assertTrue(outline.endswith("Not shown: 1 proposed, 1 disputed. Say “show proposed” or “show disputed”."))

    def test_widget_embeds_source_safely(self):
        page = render.frame('flowchart LR\n  a["</script> `${x}`"]', "HEAD <b>")
        embedded = re.search(r"mermaid\.render\('rc-[0-9a-f]+', (.*)\);", page).group(1)
        self.assertNotIn("</script>", embedded)
        self.assertEqual(json.loads(embedded.replace("<\\/", "</")), 'flowchart LR\n  a["</script> `${x}`"]')
        self.assertIn("HEAD &lt;b&gt;", page)
        self.assertNotIn("__", page)

    def test_cli_mermaid_formats_default_to_accepted_and_refuse_empty_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.yaml"
            path.write_text(yaml.safe_dump(state(), allow_unicode=True))
            run = lambda *a: subprocess.run([sys.executable, str(SCRIPT), str(path), *a], capture_output=True, text=True)
            out = run("--tree", "current_reality", "--format", "widget")
            native = run("--tree", "current_reality", "--format", "markdown")
            self.assertEqual(native.returncode, 0, native.stderr)
            self.assertEqual(native.stdout.strip(), render.markdown("current_reality", self.tree, "accepted"))
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn("CURRENT REALITY — ACCEPTED ONLY (6 nodes, 3 links)", out.stdout)
            self.assertIn("ti-arrows-maximize", out.stdout)
            out = run("--tree", "goal", "--format", "widget")
            self.assertNotEqual(out.returncode, 0)
            self.assertIn("no statements yet", out.stderr)


class TreeViewTests(unittest.TestCase):
    """The default view: a text tree read from the top node down."""

    def setUp(self):
        render.PEOPLE.clear()
        render.PEOPLE.update(alice="Alice", bob="Bob")
        self.state = state()

    def variant(self):
        """The fixture plus a second parent for a and a supersedes link from h to f."""
        changed = state()
        tree = changed["trees"]["current_reality"]
        tree["links"].append(link("l5", ["a"], "e", "proposed"))
        tree["links"].append({**link("l6", ["h"], "f", "disputed"), "relation": "supersedes"})
        return changed

    def drawn(self, model):
        found = []
        walk = lambda n: (found.append(n["id"]) if not n.get("ref") and not n.get("group") else None, [walk(c) for c in n["children"]])
        for n in model["roots"]:
            walk(n)
        return found

    def test_model_draws_every_statement_once_and_every_link(self):
        for current in (self.state, self.variant()):
            with self.subTest(links=len(current["trees"]["current_reality"]["links"])):
                model = render.tree_model(current, "current_reality")
                drawn = self.drawn(model) + [n["id"] for n in model["loose"]]
                self.assertEqual(sorted(drawn), list("abcdefgh"))
                self.assertEqual(model["links"], len(current["trees"]["current_reality"]["links"]))
        model = render.tree_model(self.state, "current_reality")
        self.assertEqual([n["id"] for n in model["roots"]], ["d"])
        self.assertEqual([n["id"] for n in model["loose"]], ["f", "h"])
        self.assertEqual(model["standing"], {"accepted": 6, "proposed": 1, "disputed": 1})

    def test_text_tree_marks_role_standing_and_joint_conditions(self):
        text = render.text_tree(self.state, "current_reality", width=100)
        self.assertTrue(text.startswith("CURRENT REALITY TREE  Why are we not there yet?\n8 statements (6 accepted, 1 proposed, 1 disputed)"))
        self.assertIn("◀ Only own time", text)
        self.assertRegex(text, r"└─ partly because\s+∧ all of these together")
        self.assertRegex(text, r"╌ partly because\s+◁ A proposed cause")
        self.assertIn("✕◁ A disputed claim  disputed", text)
        self.assertIn("NOT LINKED TO ANYTHING YET", text)
        self.assertIn("✓A", text)
        self.assertNotIn("\x1b", text)

    def test_second_parent_is_a_back_reference_and_superseded_text_is_struck(self):
        changed = self.variant()
        text = render.text_tree(changed, "current_reality", width=100)
        self.assertEqual(text.count("Sales is hard"), 2)
        self.assertIn("◀ ↑ Sales is hard", text)
        model = render.tree_model(changed, "current_reality")
        f = next(c for c in model["roots"][1]["children"] if c["id"] == "f")
        self.assertTrue(f["struck"])
        self.assertEqual(f["verb"], "replaces")
        self.assertIn("~~Loose accepted fact~~", render.markdown_tree(changed, "current_reality", "page.html"))

    def test_terminal_links_and_colour_are_opt_in(self):
        plain = render.text_tree(self.state, "current_reality")
        self.assertNotIn("\x1b]8;;", plain)
        linked = render.text_tree(self.state, "current_reality", link_base="file:///x/")
        self.assertIn("\x1b]8;;file:///x/nodes/c.html\x1b\\No customers\x1b]8;;\x1b\\", linked)
        self.assertIn("\x1b]8;;file:///x/trees/current_reality.html\x1b\\", linked)
        self.assertNotIn("#", linked)
        self.assertNotRegex(linked, r"\x1b\[[0-9;]*m")

    def test_highlight_dims_other_rows_throughout(self):
        text = render.text_tree(self.state, "current_reality", ansi=True, highlight="proposed", width=100)
        dimmed = next(line for line in text.splitlines() if "Sales is hard" in line)
        self.assertEqual(re.findall(r"\x1b\[[0-9;]*m", dimmed), ["\x1b[2m", "\x1b[0m"])
        lit = next(line for line in text.splitlines() if "A proposed cause" in line)
        self.assertIn("\x1b[33m◁", lit)

    def test_objections_show_when_disputed_items_are_highlighted(self):
        self.assertNotIn("Superseded", render.text_tree(self.state, "current_reality"))
        for lens in ("disputed", "open"):
            with self.subTest(lens=lens):
                self.assertIn("objection (Bob): Superseded", render.text_tree(self.state, "current_reality", highlight=lens))
                self.assertIn("· objection (Bob): Superseded", render.markdown_tree(self.state, "current_reality", "p.html", highlight=lens))

    def test_markdown_tree_is_a_linked_list_not_a_code_block(self):
        md = render.markdown_tree(self.state, "current_reality", "file:///x/")
        self.assertNotIn("```", md)
        self.assertTrue(md.startswith("**[Current reality tree](file:///x/trees/current_reality.html)**"))
        for ident in "abcdefgh":
            self.assertIn(f"](file:///x/nodes/{ident}.html)", md)
        self.assertIn("\n  - *partly because* ∧ *all of these together*", md)
        changed = state()
        changed["trees"]["current_reality"]["nodes"][0]["text"] = "Sales *is* [hard]"
        self.assertIn("[Sales \\*is\\* \\[hard\\]](file:///x/nodes/a.html)", render.markdown_tree(changed, "current_reality", "file:///x/"))

    def test_focus_keeps_the_path_from_the_top_and_the_branch(self):
        text = render.text_tree(self.state, "current_reality", focus=("c",), width=100)
        for kept in ("Only own time", "all of these together", "No customers", "Sales is hard", "A proposed cause"):
            self.assertIn(kept, text)
        for folded in ("Funding not applied for", "Loose accepted fact", "A disputed claim"):
            self.assertNotIn(folded, text)
        self.assertIn("⋯ 3 rows folded", text)
        md = render.markdown_tree(self.state, "current_reality", "p/", focus=("c",))
        self.assertNotIn("Funding not applied for", md)
        self.assertIn("[Show the whole tree](p/trees/current_reality.html)", md)
        self.assertIn("A disputed claim", render.text_tree(self.state, "current_reality", focus=("h",)))
        with self.assertRaises(ValueError):
            render.text_tree(self.state, "current_reality", focus=("nope",))

    def test_joint_sources_of_a_relation_drawn_from_its_source_group_under_the_target(self):
        changed = state()
        changed["trees"]["transition"] = {
            "nodes": [{**node("x", "The prototype passes its tests"), "kind": "existing_condition"},
                      {**node("y", "Configure the live channel"), "kind": "action"},
                      {**node("z", "Live evidence exists"), "kind": "expected_effect"}],
            "links": [{**link("t1", ["x", "y"], "z"), "relation": "produces"}], "backlog": []}
        model = render.tree_model(changed, "transition")
        group = model["roots"][0]["children"][0]
        self.assertEqual((model["roots"][0]["id"], group["verb"], [c["id"] for c in group["children"]]), ("z", "produced by", ["x", "y"]))
        self.assertRegex(render.text_tree(changed, "transition", width=100), r"produced by\s+∧ all of these together")

    def test_relations_without_their_own_wording_read_in_the_links_direction(self):
        changed = state()
        tree = changed["trees"]["current_reality"]
        tree["links"] += [{**link("l5", ["e"], "b", "proposed"), "relation": "may_contribute_to"},
                          {**link("l6", ["f"], "h", "proposed"), "relation": "enables"}]
        text = render.text_tree(changed, "current_reality", width=100)
        self.assertRegex(text, r"No product-market fit[^\n]*\n[^\n]*possibly partly because\s+◀ Funding not applied for")
        model = render.tree_model(changed, "current_reality")
        f = next(n for n in model["roots"] if n["id"] == "f")
        self.assertEqual((f["children"][0]["id"], f["children"][0]["verb"]), ("h", "enables"))

    def test_diagram_source_marks_every_standing_and_keeps_joint_conditions(self):
        source, short = render.diagram_source("current_reality", self.state["trees"]["current_reality"])
        self.assertTrue(source.splitlines()[1] == "flowchart BT")
        for mark in ("[A] CURRENT REALITY · CAUSE<br/>Sales is hard", "[P] CURRENT REALITY · CAUSE", "[D] CURRENT REALITY · CAUSE"):
            self.assertIn(mark, source)
        self.assertIn("Objection (Bob): Superseded", source)
        self.assertIn('j3(("AND"))', source)
        self.assertIn(f"{short['c']} --> j3", source)
        self.assertIn(f"j3 -- contributes to --> {short['d']}", source)
        self.assertIn(f"{short['g']} -. contributes to .-> {short['c']}", source)
        self.assertIn('subgraph loose["Not linked to anything yet"]', source)
        self.assertIn(f"class {short['g']} proposed", source)

    def write_state(self, tmp):
        path = Path(tmp) / "state.yaml"
        path.write_text(yaml.safe_dump(self.state, allow_unicode=True, sort_keys=False))
        return path

    def page_data(self, page):
        start = page.index("const D = ") + len("const D = ")
        return json.JSONDecoder().raw_decode(page[start:].replace("<\\/", "</"))[0]

    def test_pages_without_chrome_draw_themselves_and_open_on_their_statement(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_state(tmp)
            (Path(tmp) / ".state" / "nodes").mkdir(parents=True)
            (Path(tmp) / ".state" / "nodes" / "gone.html").write_text("stale")
            (Path(tmp) / ".state" / "trees.html").write_text("retired")
            root = render.write_pages(self.state, path, chrome=None)
            self.assertEqual(root, Path(tmp) / ".state")
            self.assertEqual(sorted(p.name for p in (root / "nodes").iterdir()), [f"{i}.html" for i in "abcdefgh"])
            self.assertEqual([p.name for p in (root / "trees").iterdir()], ["current_reality.html"])
            self.assertFalse((root / "trees.html").exists())
            page = (root / "nodes" / "c.html").read_text()
            self.assertTrue(page.startswith("<!doctype html>"))
            self.assertNotIn("__", page.split("<script")[0])
            data = self.page_data(page)
            source, short = render.diagram_source("current_reality", self.state["trees"]["current_reality"])
            self.assertEqual((data["focus"], data["source"], data["mermaid"]), (short["c"], source, render.MERMAID_JS))
            self.assertIn("Centred on: No customers", page)
            line = path.read_text().splitlines().index("    - id: c") + 1
            self.assertIn(f'href="{path.resolve().as_uri()}#L{line}"', page)
            whole = self.page_data((root / "trees" / "current_reality.html").read_text())
            self.assertIsNone(whole["focus"])

    def test_pages_drawn_once_embed_the_diagram_and_open_centred(self):
        drawing = {"svg": '<svg id="rc-current_reality" width="1000" style="max-width: 1000px;" viewBox="0 0 1000 800"><g class="node" id="flowchart-n3-2"></g></svg>',
                   "full": [0, 0, 1000, 800], "nodes": {f"n{i}": [100 * i, 200, 300, 120] for i in range(1, 9)}}
        calls = []
        original = render.prerender
        render.prerender = lambda sources, chrome: calls.append(sorted(sources)) or {t: drawing for t in sources}
        try:
            with tempfile.TemporaryDirectory() as tmp:
                path = self.write_state(tmp)
                root = render.write_pages(self.state, path, chrome="chrome")
                render.write_pages(self.state, path, chrome="chrome")  # unchanged trees reuse the drawing
                self.assertEqual(calls, [["current_reality"]])
                page = (root / "nodes" / "c.html").read_text()
                data = self.page_data(page)
                self.assertIsNone(data["source"])
                # c is n3: its box centre (450, 260) opens in a 1500-by-940 view, widened to 16:10.
                self.assertIn('viewBox="-302 -210 1504 940"', page)
                self.assertNotIn('width="1000"', page)
                self.assertIn('<rect class="rc-focus" x="294" y="194" width="312" height="132"', page)
                # The whole tree, padded by 40 on each side, then widened to 16:10.
                self.assertIn('viewBox="-204 -40 1408 880"', (root / "trees" / "current_reality.html").read_text())
        finally:
            render.prerender = original

    @unittest.skipUnless(os.environ.get("REASON_COMMONS_TEST_CHROME"), "set REASON_COMMONS_TEST_CHROME=1 to draw with a real Chrome and network")
    def test_real_chrome_draws_every_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_state(tmp)
            root = render.write_pages(self.state, path)
            page = (root / "nodes" / "c.html").read_text()
            self.assertIn("<svg", page)
            self.assertIn('class="rc-focus"', page)

    def test_cli_defaults_to_the_linked_tree_for_chat(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write_state(tmp)
            env = {**os.environ, "REASON_COMMONS_CHROME": "none"}
            run = lambda *a, cwd=None: subprocess.run([sys.executable, str(SCRIPT), str(path.resolve()), *a], capture_output=True, text=True, env=env, cwd=cwd)
            root = (Path(tmp) / ".state").resolve().as_uri() + "/"
            out = run("--tree", "current_reality")
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertTrue(out.stdout.startswith(f"**[Current reality tree]({root}trees/current_reality.html)**"))
            self.assertIn(f"]({root}nodes/c.html)", out.stdout)
            self.assertTrue((Path(tmp) / ".state" / "nodes" / "c.html").exists())
            out = run("--tree", "current_reality", cwd=tmp)
            self.assertIn("](.state/nodes/c.html)", out.stdout)
            out = run("--format", "tree-markdown", "--page-url", "https://example.org/t")
            self.assertIn("](https://example.org/t/nodes/c.html)", out.stdout)
            out = run("--format", "tree-text", "--focus", "c")
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertTrue(out.stdout.startswith("CURRENT REALITY TREE"))
            self.assertNotIn("\x1b", out.stdout)
            out = run("--format", "tree-text", "--links", "always")
            self.assertIn(f"\x1b]8;;{root}nodes/a.html\x1b\\", out.stdout)
            out = run("--page")
            self.assertEqual(out.stdout.splitlines()[0], root)
            self.assertIn(f"Current reality tree: {root}trees/current_reality.html", out.stdout)
            self.assertNotEqual(run("--tree", "goal").returncode, 0)
            self.assertNotEqual(run("--focus", "nope").returncode, 0)
            self.assertIn("is not a statement in the current reality tree", run("--focus", "nope", "--tree", "current_reality").stderr)


if __name__ == "__main__":
    unittest.main()
