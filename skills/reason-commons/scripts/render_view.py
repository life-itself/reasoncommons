#!/usr/bin/env python3
"""Render the reasoning trees for reading, straight from the YAML.

The default view is a text tree read from the top node down, for an overview in
a chat reply or a terminal: glyph shape names the role, glyph fill names the
standing (solid accepted, hollow proposed, ✕ disputed) and the rail names the
link standing (│ accepted, ┊ proposed, ┆ disputed). Every standing is shown; a
highlight dims the rest. Each tree and statement name links to a graphical
diagram of the full tree: a tree name opens it fitted to the whole tree, and a
statement name opens it centred and zoomed on that statement, ready to pan and
zoom.

  render_view.py STATE --counts                         view-menu counts per tree
  render_view.py STATE --tree T                         linked nested list for a chat reply
  render_view.py STATE --tree T --format tree-text      terminal text with OSC 8 links
  render_view.py STATE --focus NODE [--format …]        zoomed to NODE's path and branch
  render_view.py STATE --page [DIR]                     write the diagram pages and list them
  render_view.py STATE --tree T --standing S --format widget|markdown|mermaid|text
                                                        one-standing Mermaid views, on request only
  render_view.py --wrap --heading "LAST CHANGE: PROPOSED · …" < diagram.mmd
                                                        any Mermaid source in the frame

Widget and Markdown output is complete: pass it unchanged to the host's widget
tool or return it unchanged in the reply. The text trees write the diagram pages
beside the state, DIR/trees/<tree>.html and DIR/nodes/<node-id>.html, unless
--page-url names a published copy. Separate pages mean no link depends on a URL
anchor. Counts, topology and standing markers come from the state, so the
conversation never has to count or lay out nodes by hand.
"""

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from urllib.parse import quote
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_views import load, validate  # noqa: E402

PEOPLE = {}
STANDINGS = ("accepted", "proposed", "disputed")
MARK = {"accepted": "A", "proposed": "P", "disputed": "D"}
TREE_ORDER = ("goal", "current_reality", "conflict", "future_reality", "prerequisite", "transition")


def status(item):
    return item.get("status", "proposed")


def title(tree):
    return tree.replace("_", " ").capitalize()


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def ordered(trees):
    return sorted(trees, key=lambda t: TREE_ORDER.index(t) if t in TREE_ORDER else len(TREE_ORDER))


def counts(state):
    lines = []
    for name in ordered(state["trees"]):
        nodes = state["trees"][name]["nodes"]
        if not nodes:
            continue
        parts = [f"{sum(status(n) == s for n in nodes)} {s}" for s in STANDINGS]
        lines.append(f"{title(name)} ({' · '.join(p for p in parts if not p.startswith('0 '))})")
    return "\n".join(lines) or "There are no trees to view yet."


def default_standing(tree):
    return "accepted" if any(status(n) == "accepted" for n in tree["nodes"]) else "proposed"


def select(tree, standing):
    """Nodes and links of one standing, plus nodes of other standings as context."""
    nodes = {n["id"]: n for n in tree["nodes"]}
    shown = [n["id"] for n in tree["nodes"] if status(n) == standing]
    links = [l for l in tree["links"] if status(l) == standing]
    context = []
    for link in links:
        for ident in link["from"] + [link["to"]]:
            if status(nodes[ident]) != standing and ident not in context:
                context.append(ident)
    return nodes, shown, context, links


def label(node, standing, tree, multiline=True):
    metadata = f"[{MARK[status(node)]}] {title(tree).upper()} · {title(node['kind']).upper()}"
    separator = "\n" if multiline else ": "
    text = f"{metadata}{separator}{node['text'].strip()}"
    if standing == "disputed":
        for c in node.get("challenges", []):
            text += f"\nObjection ({PEOPLE.get(c['by'], c['by'])}): {c['text'].strip()}"
    return text


def escape(text):
    for raw, code in (("&", "#amp;"), ('"', "#quot;"), ("<", "#lt;"), (">", "#gt;")):
        text = text.replace(raw, code)
    return text.replace("\n", "<br/>")


def heading(name, standing, shown, links, context=()):
    extra = f"; {len(context)} nodes of other standings as context" if context else ""
    return f"{title(name).upper()} — {standing.upper()} ONLY ({plural(len(shown), 'node')}, {plural(len(links), 'link')}{extra})"


def not_shown(tree, standing):
    others = [(s, sum(status(n) == s for n in tree["nodes"])) for s in STANDINGS if s != standing]
    others = [(s, n) for s, n in others if n]
    if not others:
        return "Nothing else in this tree."
    return "Not shown: " + ", ".join(f"{n} {s}" for s, n in others) + ". Say " + " or ".join(f"“show {s}”" for s, _ in others) + "."


def relations(links):
    names = {l["relation"] for l in links}
    return names.pop().replace("_", " ") if len(names) == 1 else None


def mermaid(name, tree, standing):
    nodes, shown, context, links = select(tree, standing)
    common = relations(links)
    short = {ident: f"n{i}" for i, ident in enumerate(shown + context, 1)}
    linked = {i for l in links for i in l["from"] + [l["to"]]}
    loose = [i for i in shown if i not in linked]
    out = ["flowchart BT"]
    for ident in [i for i in shown + context if i not in loose]:
        out.append(f'  {short[ident]}["{escape(label(nodes[ident], standing, name))}"]')
    if loose and links:
        out.append('  subgraph loose["Not yet linked"]')
        out += [f'    {short[i]}["{escape(label(nodes[i], standing, name))}"]' for i in loose]
        out.append("  end")
    else:
        out += [f'  {short[i]}["{escape(label(nodes[i], standing, name))}"]' for i in loose]
    for j, link in enumerate(links, 1):
        tag = [] if common else [link["relation"].replace("_", " ")]
        if status(link) == "disputed":
            tag.insert(0, "disputed")
        solid = status(link) == "accepted"
        plain = "-->" if solid else "-.->"
        tagged = f"-- {' · '.join(tag)} -->" if solid else f"-. {' · '.join(tag)} .->"
        arrow = tagged if tag else plain
        target = short[link["to"]]
        if len(link["from"]) > 1:
            out.append(f'  j{j}(("AND"))')
            out += [f"  {short[s]} {plain} j{j}" for s in link["from"]]
            out.append(f"  j{j} {arrow} {target}")
        else:
            out.append(f"  {short[link['from'][0]]} {arrow} {target}")
    out += [
        "  classDef proposed stroke-dasharray:4 3,stroke:#BA7517",
        "  classDef accepted stroke:#1D9E75,stroke-width:2px",
        "  classDef disputed stroke:#E24B4A,stroke-width:2px",
        "  classDef context stroke-dasharray:2 2,opacity:0.6",
    ]
    if shown:
        out.append(f"  class {','.join(short[i] for i in shown)} {standing}")
    if context:
        out.append(f"  class {','.join(short[i] for i in context)} context")
    return "\n".join(out), shown, links, common, context


def text_outline(name, tree, standing):
    """Plain-text fallback: every link once, grouped by its effect; loose nodes last."""
    nodes, shown, context, links = select(tree, standing)
    common = relations(links)
    lines = [heading(name, standing, shown, links, context)]
    if common:
        lines.append(f"Each arrow reads “{common}”.")
    by_target = {}
    for link in links:
        by_target.setdefault(link["to"], []).append(link)
    for target, incoming in by_target.items():
        lines.append("")
        lines.append(label(nodes[target], standing, name, multiline=False).replace("\n", "\n    "))
        for link in incoming:
            causes = [label(nodes[s], standing, name, multiline=False).split("\nObjection (", 1)[0] for s in link["from"]]
            via = "" if common else f" ({link['relation'].replace('_', ' ')})"
            joined = causes[0] if len(causes) == 1 else "AND( " + " + ".join(causes) + " )"
            lines.append(f"  <-{via} {joined}")
    linked = {i for l in links for i in l["from"] + [l["to"]]}
    loose = [i for i in shown if i not in linked]
    if loose:
        lines += ["", "Not yet linked:"] + [f"  {label(nodes[i], standing, name, multiline=False)}" for i in loose]
    lines += ["", not_shown(tree, standing)]
    return "\n".join(lines)


WIDGET = """<style>
#rcv{position:relative;height:380px;border:0.5px solid var(--border);border-radius:12px;overflow:hidden;cursor:grab;touch-action:none;background:var(--surface-1)}
#rcv.drag{cursor:grabbing}
#rcv svg{width:100%;height:100%;max-width:none!important}
.rcb{position:absolute;top:8px;right:8px;display:flex;gap:4px}
.rcb button{width:30px;height:30px;border:0.5px solid var(--border-strong);border-radius:var(--radius);background:var(--surface-2);color:var(--text-primary);cursor:pointer;font-size:16px;line-height:1}
</style>
<h2 class="sr-only">__HEADING__, with pan and zoom</h2>
<p style="margin:0 0 8px;font-size:13px;color:var(--text-secondary)">__HEADING__ · drag to pan · pinch or ⌘/Ctrl+scroll to zoom</p>
<div id="rcv"><div id="rc" style="width:100%;height:100%"></div>
<div class="rcb"><button id="zin" aria-label="Zoom in"><i class="ti ti-plus" aria-hidden="true"></i></button><button id="zout" aria-label="Zoom out"><i class="ti ti-minus" aria-hidden="true"></i></button><button id="zfit" aria-label="Fit to view"><i class="ti ti-arrows-maximize" aria-hidden="true"></i></button></div></div>
<p style="margin:8px 0 0;font-size:13px;color:var(--text-secondary)">__NOT_SHOWN__</p>
<script type="module">
import mermaid from 'https://esm.sh/mermaid@11/dist/mermaid.esm.min.mjs';
const mode = document.documentElement.dataset.mode;
const dark = mode ? mode === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
await document.fonts.ready;
mermaid.initialize({startOnLoad: false, theme: 'base', fontFamily: '"anthropic-sans", sans-serif',
  themeVariables: {darkMode: dark, fontSize: '13px', fontFamily: '"anthropic-sans", sans-serif',
    lineColor: dark ? '#9c9a92' : '#73726c', textColor: dark ? '#c2c0b6' : '#3d3d3a',
    primaryColor: dark ? '#2C2C2A' : '#F1EFE8', primaryBorderColor: dark ? '#888780' : '#5F5E5A'}});
const { svg } = await mermaid.render('__RENDER_ID__', __SOURCE__);
const host = document.getElementById('rc'); host.innerHTML = svg;
const el = host.querySelector('svg'); el.removeAttribute('style'); el.setAttribute('width','100%'); el.setAttribute('height','100%');
const [fx,fy,fw,fh] = el.getAttribute('viewBox').split(/[\\s,]+/).map(Number);
const pad = 16, fit = {x:fx-pad,y:fy-pad,w:fw+2*pad,h:fh+2*pad};
let v = {...fit};
const set = () => el.setAttribute('viewBox', `${v.x} ${v.y} ${v.w} ${v.h}`);
const scale = () => { const r = el.getBoundingClientRect(); return Math.max(v.w/r.width, v.h/r.height); };
const zoom = (f, cx, cy) => { const r = el.getBoundingClientRect(); const s = scale();
  const px = cx==null ? v.x+v.w/2 : v.x + (cx-r.left)*s - (s*r.width-v.w)/2;
  const py = cy==null ? v.y+v.h/2 : v.y + (cy-r.top)*s - (s*r.height-v.h)/2;
  const nw = Math.min(Math.max(v.w*f, fit.w/8), fit.w*4); const k = nw/v.w;
  v = {x:px-(px-v.x)*k, y:py-(py-v.y)*k, w:v.w*k, h:v.h*k}; set(); };
set();
const box = document.getElementById('rcv');
document.getElementById('zin').onclick = () => zoom(0.8);
document.getElementById('zout').onclick = () => zoom(1.25);
document.getElementById('zfit').onclick = () => { v = {...fit}; set(); };
box.addEventListener('wheel', e => { if (!(e.ctrlKey || e.metaKey)) return; e.preventDefault(); zoom(Math.exp(e.deltaY*0.01), e.clientX, e.clientY); }, {passive:false});
let last = null;
box.addEventListener('pointerdown', e => { if (e.target.closest('button')) return; last = [e.clientX,e.clientY]; box.setPointerCapture(e.pointerId); box.classList.add('drag'); });
box.addEventListener('pointermove', e => { if (!last) return; const s = scale(); v.x -= (e.clientX-last[0])*s; v.y -= (e.clientY-last[1])*s; last = [e.clientX,e.clientY]; set(); });
const end = () => { last = null; box.classList.remove('drag'); };
box.addEventListener('pointerup', end); box.addEventListener('pointercancel', end);
</script>
"""


def markdown(name, tree, standing):
    """Complete native Mermaid response, with the same scope and context as a widget."""
    source, shown, links, common, context = mermaid(name, tree, standing)
    lines = [heading(name, standing, shown, links, context)]
    if common:
        lines.append(f"Each arrow reads “{common}”.")
    lines += ["", "```mermaid", source, "```", "", not_shown(tree, standing)]
    return "\n".join(lines)


def widget(name, tree, standing):
    source, shown, links, common, context = mermaid(name, tree, standing)
    relation = f" · each arrow reads “{common}”" if common else ""
    return frame(source, heading(name, standing, shown, links, context) + relation, not_shown(tree, standing))


def frame(source, head, footer=""):
    page = WIDGET if footer else WIDGET.replace('<p style="margin:8px 0 0;font-size:13px;color:var(--text-secondary)">__NOT_SHOWN__</p>\n', "")
    for key, value in (
        ("__HEADING__", html.escape(head, quote=False)),
        ("__NOT_SHOWN__", html.escape(footer, quote=False)),
        ("__RENDER_ID__", f"rc-{uuid.uuid4().hex[:8]}"),
        ("__SOURCE__", json.dumps(source).replace("</", "<\\/")),
    ):
        page = page.replace(key, value)
    return page



# ---------------------------------------------------------------------------
# Text-tree views: the default view of a tree.
#
# One nested model per tree, read top-down. Glyph shape names the role, fill
# names the standing (solid accepted, hollow proposed, ✕ disputed) and the rail
# names the link standing (│ accepted, ┊ proposed, ┆ disputed). Every standing
# is shown; highlighting dims the rest instead of removing it. A statement with
# several parents is drawn in full once and as an ↑ back-reference elsewhere.
# ---------------------------------------------------------------------------

GLYPHS = {
    "goal": "◉◎", "objective": "◉◎",
    "critical_success_factor": "◆◇", "need": "◆◇", "intermediate_objective": "◆◇",
    "necessary_condition": "■□", "observation": "■□", "existing_condition": "■□",
    "undesirable_effect": "▼▽", "obstacle": "▼▽",
    "cause": "◀◁",
    "injection": "★☆",
    "action": "▶▷", "prerequisite": "▶▷",
    "desirable_effect": "▲△",
    "predicted_effect": "●○", "expected_effect": "●○",
}
TREE_INFO = {
    "goal": ("Goal tree", "Goal", "◉", "What must be true for us to reach the goal?", "Read down: each line is what the line above it needs."),
    "current_reality": ("Current reality tree", "Reality", "▼", "Why are we not there yet?", "Read down: each line is part of why the line above it happens, or the evidence for it."),
    "conflict": ("Conflict cloud", "Cloud", "⚡", "What conflict keeps us stuck?", "Read down: each line is what the line above it needs. The actions at the bottom conflict."),
    "future_reality": ("Future reality tree", "Future", "★", "If we change this, will it work?", "Read down: each effect, then the changes expected to produce it."),
    "prerequisite": ("Prerequisite tree", "Prereq", "◆", "What stands in the way, and what comes first?", "Read down: each objective, what blocks it, and what clears the block."),
    "transition": ("Transition tree", "Transition", "▶", "What exactly do we do next?", "Read down: each action, what it should produce, and what comes after it."),
}
TOP_KINDS = {
    "goal": ["goal", "critical_success_factor", "necessary_condition"],
    "current_reality": ["undesirable_effect", "cause", "observation"],
    "conflict": ["objective", "need", "prerequisite"],
    "future_reality": ["desirable_effect", "undesirable_effect", "predicted_effect", "injection", "existing_condition"],
    "prerequisite": ["objective", "obstacle", "intermediate_objective"],
    "transition": ["action", "expected_effect", "existing_condition", "need"],
}
# relation -> (end drawn as the parent, word on the child row, drawn as a cross-reference)
RELATION_ROWS = {
    "necessary_for": ("to", "needs", False),
    "causes": ("to", "because", False),
    "contributes_to": ("to", "partly because", False),
    "may_contribute_to": ("to", "possibly partly because", False),
    "supports": ("to", "supported by", False),
    "challenges": ("to", "challenged by", False),
    "supersedes": ("from", "replaces", False),
    "blocks": ("to", "blocked by", False),
    "overcomes": ("to", "cleared by", False),
    "precedes": ("from", "then", False),
    "conflicts_with": ("from", "conflicts with", True),
}
# A relation drawn from its source, read the other way when several sources act together.
INVERSE_WORDS = {"expect": "produced by", "then": "after", "replaces": "replaced by"}
TRACE_WORDS = {"addresses": "addresses", "implements": "implements", "derived_from": "from"}
QUIET_WORK = {"review_relation", "test_causality"}


def tree_info(name):
    return TREE_INFO.get(name, (title(name), title(name), "•", "", "Read down."))


def relation_row(tree_name, relation):
    if relation == "produces":
        return ("from", "expect", False) if tree_name == "transition" else ("to", "produced by", False)
    # A relation with no wording of its own hangs its target under its source, so the row reads in the link's direction.
    return RELATION_ROWS.get(relation, ("from", relation.replace("_", " "), False))


def glyph(node):
    if node.get("group"):
        return "∧"
    pair = GLYPHS.get(node["kind"], "•◦")
    mark = pair[0] if node["standing"] == "accepted" else pair[1]
    return ("✕" if node["standing"] == "disputed" else "") + mark


def tree_model(state, name):
    """Nested display model for one tree; every node and link appears, or ValueError."""
    tree = state["trees"][name]
    where = {n["id"]: t for t, content in state["trees"].items() for n in content["nodes"]}
    nodes = {n["id"]: n for n in tree["nodes"]}
    links = tree.get("links", [])
    backlog = {}
    for task in tree.get("backlog", []):
        backlog.setdefault(task["ref"], []).append(task)
    struck = {l["to"] for l in links if l["relation"] == "supersedes"}
    kids, has_parent, cross = {}, set(), []
    for l in links:
        end, verb, is_cross = relation_row(name, l["relation"])
        if is_cross:
            cross.append(l)
            continue
        if end == "to":
            parent, children = l["to"], list(l["from"])
        elif len(l["from"]) == 1:
            parent, children = l["from"][0], [l["to"]]
        else:
            # Joint sources, such as a condition and an action that together produce an effect, are grouped under the target.
            parent, children, verb = l["to"], list(l["from"]), INVERSE_WORDS.get(verb, f"← {verb}")
        kids.setdefault(parent, []).append((l, children, verb))
        has_parent.update(children)

    def link_info(l):
        return {"id": l["id"], "relation": l["relation"], "standing": status(l)}

    def base(ident):
        n = nodes[ident]
        return {
            "id": ident, "kind": n["kind"], "standing": status(n), "text": " ".join(n["text"].split()),
            "by": n.get("accepted_by") or [],
            "challenges": [{"by": c.get("by"), "text": " ".join(c["text"].split())} for c in n.get("challenges") or []],
            "flags": [{"work": t["work"].replace("_", " "), "note": t.get("note", "")} for t in backlog.get(ident, []) if t["work"] not in QUIET_WORK],
            "refs": [{"rel": word, "id": r, "tree": where.get(r)} for key, word in TRACE_WORDS.items() for r in n.get(key) or []],
            "struck": ident in struck, "children": [],
        }

    placed, full, seen = set(), {}, set()

    def entry(ident, l, verb):
        if ident in placed:
            item = base(ident)
            item["ref"] = True
        else:
            item = build(ident)
        item["verb"], item["link"] = verb, link_info(l)
        return item

    def build(ident):
        placed.add(ident)
        item = full[ident] = base(ident)
        for l, children, verb in kids.get(ident, []):
            seen.add(l["id"])
            if len(children) == 1:
                item["children"].append(entry(children[0], l, verb))
            else:
                group = {"group": True, "id": l["id"], "kind": "and", "standing": status(l), "text": "all of these together",
                         "verb": verb, "link": link_info(l), "by": [], "challenges": [], "flags": [], "refs": [], "struck": False}
                group["children"] = [entry(c, l, "") for c in children]
                item["children"].append(group)
        return item

    rank = {k: i for i, k in enumerate(TOP_KINDS.get(name, []))}
    linked = {i for l in links for i in list(l["from"]) + [l["to"]]}
    tops = sorted((i for i in nodes if i in linked and i not in has_parent), key=lambda i: rank.get(nodes[i]["kind"], len(rank)))
    roots = [build(i) for i in tops if i not in placed]
    roots += [build(i) for i in nodes if i in linked and i not in placed]  # only reachable through a cycle
    for l in cross:
        seen.add(l["id"])
        full[l["from"][0]]["children"].append(entry(l["to"], l, relation_row(name, l["relation"])[1]))
    loose = [base(i) for i in nodes if i not in linked]
    missing = [l["id"] for l in links if l["id"] not in seen] + [i for i in nodes if i not in placed and i not in {n["id"] for n in loose}]
    if missing:
        raise ValueError(f"{title(name)}: not drawn: {', '.join(missing)}")
    tally = lambda items: {s: sum(status(x) == s for x in items) for s in STANDINGS}
    return {"roots": roots, "loose": loose, "nodes": len(nodes), "links": len(links), "standing": tally(tree["nodes"]), "link_standing": tally(links)}


def flatten(model):
    """Rows in reading order with rail instructions, parents and branch extents."""
    rows = []
    child_style = lambda c: c["link"]["standing"] if c.get("link") else "proposed"

    def walk(n, depth, rails, last, cont, parent):
        row = {"n": n, "depth": depth, "rails": rails, "last": last, "parent": parent, "idx": len(rows)}
        rows.append(row)
        kids = n["children"]
        row["kid_style"] = child_style(kids[0]) if kids else None
        for i, c in enumerate(kids):
            is_last = i == len(kids) - 1
            walk(c, depth + 1, [] if depth == 0 else rails + [None if last else cont], is_last, None if is_last else child_style(kids[i + 1]), row)
        row["end"] = len(rows)

    for root in model["roots"]:
        walk(root, 0, [], True, None, None)
    return rows


def focus_rows(model, rows, focus):
    """Keys of rows to keep when zoomed to some nodes: each node's path from the top and its whole branch."""
    if not focus:
        return None
    keep, loose = set(), {n["id"] for n in model["loose"]}
    for ident in focus:
        if ident in loose:
            keep.add(("loose", ident))
            continue
        row = next((r for r in rows if r["n"]["id"] == ident and not r["n"].get("ref") and not r["n"].get("group")), None)
        if row is None:
            raise ValueError(f"--focus {ident} is not in this tree")
        p = row
        while p:
            keep.add(p["idx"])
            p = p["parent"]
        keep.update(range(row["idx"], row["end"]))
    return keep


def initials(node):
    if node["standing"] != "accepted" or not node["by"]:
        return ""
    order = [p for p in ("rufus", "david") if p in PEOPLE] + [p for p in PEOPLE if p not in ("rufus", "david")]
    return "+".join(PEOPLE.get(p, p)[0].upper() for p in order if p in node["by"]) or "+".join(p[0].upper() for p in node["by"])


def matches(node, highlight):
    if not highlight or highlight == "all":
        return True
    if highlight == "open":
        return bool(node["flags"]) or node["standing"] == "disputed"
    return node["standing"] == highlight


OBJECTION_LENSES = ("disputed", "open")


def objection(challenge):
    by = challenge.get("by")
    return f"objection{f' ({PEOPLE.get(by, by)})' if by else ''}: {challenge['text']}"


def counts_line(model):
    nodes = ", ".join(f"{n} {s}" for s, n in model["standing"].items() if n)
    links = ", ".join(f"{n} {s}" for s, n in model["link_standing"].items() if n) or "none"
    return f"{plural(model['nodes'], 'statement')} ({nodes}) · {plural(model['links'], 'link')} ({links})"


def ref_label(ref):
    return f"↗ {ref['rel']} {tree_info(ref['tree'])[1] if ref['tree'] else '?'}"


ANSI = {"dim": "2", "bold": "1", "accepted": "32", "proposed": "33", "disputed": "31", "flag": "33", "strike": "2;9"}


def text_tree(state, name, ansi=False, link_base=None, highlight=None, focus=(), width=80, ids=False):
    """The tree as indented text; ANSI styling and OSC 8 links to the diagram pages are optional."""
    model = tree_model(state, name)
    rows = flatten(model)
    keep = focus_rows(model, rows, focus)
    head, _, _, question, reading = tree_info(name)
    verb_width = max([len(r["n"].get("verb", "")) for r in rows] + [4])
    sty = lambda kind, s: f"\x1b[{ANSI[kind]}m{s}\x1b[0m" if ansi and kind and s else s
    url = lambda ident: page_href(link_base, "nodes", ident) if link_base else None
    tree_url = page_href(link_base, "trees", name) if link_base else None
    osc = lambda target, s: f"\x1b]8;;{target}\x1b\\{s}\x1b]8;;\x1b\\" if target else s
    pipe = lambda st: "   " if st is None else {"accepted": "│  ", "disputed": "┆  "}.get(st, "┊  ")
    rail_char = lambda st: {"accepted": "│", "disputed": "┆"}.get(st, "┊")
    out = [osc(tree_url, sty("bold", head.upper())) + sty("dim", "  " + question), sty("dim", counts_line(model)),
           sty("dim", "Shape = role · filled accepted, hollow proposed, ✕ disputed · rails │ accepted ┊ proposed ┆ disputed"),
           sty("dim", reading)]
    folded = 0

    def flush():
        nonlocal folded
        if folded:
            out.append(sty("dim", f"⋯ {plural(folded, 'row')} folded"))
            folded = 0

    def draw(row):
        n = row["n"]
        root = row["depth"] == 0
        dim = not matches(n, highlight) and not n.get("group")
        paint = (lambda kind, s: s) if dim else sty  # a dimmed row is dim throughout, not reset by inner styles
        pre = "".join(pipe(st) for st in row["rails"])
        conn = ""
        if not root:
            st = n["link"]["standing"]
            conn = ("└" if row["last"] else "├") + {"accepted": "─ ", "disputed": "┄ "}.get(st, "╌ ")
        verb = "" if root else n.get("verb", "").ljust(verb_width) + " "
        mark = glyph(n) + (" ↑" if n.get("ref") else "")
        suffix = []
        if not n.get("ref") and not n.get("group"):
            if initials(n):
                suffix.append(("accepted", "✓" + initials(n), None))
            if n["standing"] == "disputed":
                suffix.append(("disputed", "disputed", None))
            suffix += [("flag", "⚑ " + f["work"], None) for f in n["flags"]]
            suffix += [("dim", ref_label(r), url(r["id"])) for r in n["refs"]]
        if ids and not n.get("group"):
            suffix.append(("dim", n["id"], None))
        lead = pre + conn + verb + mark + " "
        avail = max(24, width - len(lead))
        lines = textwrap.wrap(n["text"], avail, break_long_words=False, break_on_hyphens=False) or [""]
        cont = pre + ("" if root else ("   " if row["last"] else pipe(n["link"]["standing"])))
        kid = rail_char(row["kid_style"]) if row["kid_style"] else " "
        cont_lead = cont + kid + " " * max(0, len(lead) - len(cont) - 1)
        tail_plain = "  ".join(s for _, s, _ in suffix)
        own_line = tail_plain and len(lines[-1]) + 2 + len(tail_plain) > avail
        tail = "  ".join(osc(target, paint(kind, s)) for kind, s, target in suffix)
        mark_style = "dim" if n.get("group") else n["standing"]
        text_style = "strike" if n["struck"] else ("dim" if n.get("ref") or n.get("group") else ("bold" if root else None))
        target = None if n.get("group") else url(n["id"])
        drawn = []
        for i, piece in enumerate(lines):
            prefix = paint("dim", pre + conn + verb) + paint(mark_style, mark) + " " if i == 0 else paint("dim", cont_lead)
            body = osc(target, paint(text_style, piece))
            drawn.append(prefix + body + ("  " + tail if i == len(lines) - 1 and tail and not own_line else ""))
        if own_line:
            drawn.append(paint("dim", cont_lead) + tail)
        if highlight in OBJECTION_LENSES and not n.get("ref"):
            for c in n["challenges"]:
                for piece in textwrap.wrap(objection(c), avail, break_long_words=False, break_on_hyphens=False):
                    drawn.append(paint("dim", cont_lead) + paint("disputed", piece))
        return [sty("dim", line) if dim else line for line in drawn]

    for row in rows:
        if keep is not None and row["idx"] not in keep:
            folded += 1
            continue
        flush()
        if row["depth"] == 0:
            out.append("")
        out += draw(row)
    loose = [n for n in model["loose"] if keep is None or ("loose", n["id"]) in keep]
    folded += len(model["loose"]) - len(loose)
    flush()
    if loose:
        out += ["", sty("dim", "NOT LINKED TO ANYTHING YET")]
        for n in loose:
            out += draw({"n": n, "depth": 0, "rails": [], "last": True, "kid_style": None})
    flush()
    return "\n".join(out)


def md_escape(text):
    return "".join("\\" + c if c in "\\`*_[]<>" else c for c in text)


def markdown_tree(state, name, link_base, focus=(), highlight=None):
    """A nested Markdown list in which every tree and statement name links to its diagram page."""
    model = tree_model(state, name)
    rows = flatten(model)
    keep = focus_rows(model, rows, focus)
    head, _, _, question, _ = tree_info(name)
    href = lambda ident: page_href(link_base, "nodes", ident)
    tree_href = page_href(link_base, "trees", name)
    out = [f"**[{head}]({tree_href})** · {question}", ""]

    def item(n, depth):
        verb = f"*{n['verb']}* " if n.get("verb") else ""
        if n.get("group"):
            label = "*all of these together*"
        else:
            text = md_escape(n["text"])
            text = f"~~{text}~~" if n["struck"] else text
            label = ("↑ " if n.get("ref") else "") + f"[{text}]({href(n['id'])})"
        extra = []
        if not n.get("ref") and not n.get("group"):
            if initials(n):
                extra.append("✓" + initials(n))
            if n["standing"] == "disputed":
                extra.append("disputed")
            extra += [f"⚑ {f['work']}" for f in n["flags"]]
            extra += [f"[{ref_label(r)}]({href(r['id'])})" for r in n["refs"]]
            if highlight in OBJECTION_LENSES:
                extra += [md_escape(objection(c)) for c in n["challenges"]]
        return "  " * depth + f"- {verb}{glyph(n)} {label}" + (" · " + " · ".join(extra) if extra else "")

    for row in rows:
        if keep is None or row["idx"] in keep:
            out.append(item(row["n"], row["depth"]))
    loose = [n for n in model["loose"] if keep is None or ("loose", n["id"]) in keep]
    if loose:
        out += ["", "*Not linked to anything yet*"] + [item(n, 0) for n in loose]
    if keep is not None:
        out += ["", f"Zoomed to {plural(len(focus), 'statement')}, with the path from the top and the whole branch. [Show the whole tree]({tree_href})."]
    return "\n".join(out)


def record_links(state, state_path):
    """Where each statement was recorded: its line in the working YAML, plus any source provenance file."""
    state_path = Path(state_path).resolve()
    lines, nested = {}, {}
    for number, line in enumerate(state_path.read_text().splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("- id:") or stripped.startswith("id:"):
            ident = stripped.split("id:", 1)[1].strip().strip("'\"")
            (lines if stripped.startswith("- ") else nested).setdefault(ident, number)
    lines = {**nested, **lines}  # a list item's own id wins over a nested reference to it
    roots = [state_path.parent, *state_path.parents]
    records = {}
    for content in state["trees"].values():
        for n in content["nodes"]:
            item = {"yaml": f"{state_path.as_uri()}#L{lines.get(n['id'], 1)}", "yaml_label": f"{state_path.name} line {lines.get(n['id'], '?')}"}
            prov = (((n.get("source") or {}).get("entity") or {}).get("provenance") or {}).get("path")
            if prov:
                file, _, anchor = prov.partition("#")
                found = next((r / file for r in roots if (r / file).exists()), None)
                if found:
                    item["source"] = found.resolve().as_uri() + (f"#{anchor}" if anchor else "")
                    item["source_label"] = prov
            records[n["id"]] = item
    return records


# ---------------------------------------------------------------------------
# Diagram pages: what the text tree's links open.
#
# Each tree is drawn once as a Mermaid flowchart with every standing marked, then
# written as one pan-and-zoom page per tree, fitted to the whole tree, and one per
# statement: the same full tree, opened centred and zoomed on that statement and
# outlined. Separate files mean no link depends on a URL anchor, which some hosts
# drop. When Chrome is available the diagram is drawn once at write time and
# embedded, so the pages work offline and open on their statement even without
# scripts; otherwise each page draws itself with mermaid.js from the network.
# ---------------------------------------------------------------------------

MERMAID_JS = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs"
FOCUS_VIEW = (1500, 940)  # diagram units shown around a statement when its page opens
CHROME_PATHS = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Chromium.app/Contents/MacOS/Chromium")
CHROME_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")


def pages_dir(state_path):
    state_path = Path(state_path)
    return state_path.parent / f".{state_path.stem}"


def page_href(base, kind, ident):
    """Link under base to a tree page (kind "trees") or a statement page (kind "nodes")."""
    return f"{base}{kind}/{quote(ident)}.html"


def pages_base(root, relative=False):
    """Base address of the pages: a path relative to the working directory when asked and possible, else a file URI."""
    root = Path(root).resolve()
    if relative:
        rel = os.path.relpath(root, Path.cwd())
        if not rel.startswith(".."):
            return quote(Path(rel).as_posix()) + "/"
    return root.as_uri() + "/"


def diagram_source(name, tree):
    """Mermaid source for the whole tree with every standing marked, and the node-ID map it uses."""
    short = {n["id"]: f"n{i}" for i, n in enumerate(tree["nodes"], 1)}
    linked = {i for l in tree["links"] for i in l["from"] + [l["to"]]}
    box = lambda n: f'{short[n["id"]]}["{escape(label(n, status(n), name))}"]'
    out = ['%%{init: {"flowchart": {"htmlLabels": true, "wrappingWidth": 300, "nodeSpacing": 40, "rankSpacing": 70}}}%%', "flowchart BT"]
    out += ["  " + box(n) for n in tree["nodes"] if n["id"] in linked]
    loose = [n for n in tree["nodes"] if n["id"] not in linked]
    if loose:
        out += ['  subgraph loose["Not linked to anything yet"]'] + ["    " + box(n) for n in loose] + ["  end"]
    for j, l in enumerate(tree["links"], 1):
        solid = status(l) == "accepted"
        tag = ("disputed · " if status(l) == "disputed" else "") + l["relation"].replace("_", " ")
        arrow = f"-- {tag} -->" if solid else f"-. {tag} .->"
        if len(l["from"]) > 1:
            out.append(f'  j{j}(("AND"))')
            out += [f"  {short[s]} {'-->' if solid else '-.->'} j{j}" for s in l["from"]]
            out.append(f"  j{j} {arrow} {short[l['to']]}")
        else:
            out.append(f"  {short[l['from'][0]]} {arrow} {short[l['to']]}")
    out += [
        "  classDef proposed stroke-dasharray:5 4,stroke:#BA7517,stroke-width:2px,fill:#fffdf7",
        "  classDef accepted stroke:#1D9E75,stroke-width:2.5px,fill:#f3fbf7",
        "  classDef disputed stroke:#E24B4A,stroke-width:2.5px,fill:#fff5f5",
    ]
    for s in STANDINGS:
        ids = [short[n["id"]] for n in tree["nodes"] if status(n) == s]
        if ids:
            out.append(f"  class {','.join(ids)} {s}")
    return "\n".join(out), short


# Shared by the write-time render and the in-page fallback: the SVG, its extent and each statement's box, in diagram units.
MEASURE_JS = r"""function rcMeasure(svg) {
  const sr = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal, k = vb.width / sr.width, nodes = {};
  for (const g of svg.querySelectorAll("g.node")) {
    const m = g.id.match(/flowchart-(n\d+)-\d+$/); if (!m) continue;
    const r = g.getBoundingClientRect();
    nodes[m[1]] = [vb.x + (r.x - sr.x) * k, vb.y + (r.y - sr.y) * k, r.width * k, r.height * k];
  }
  return { svg: svg.outerHTML, full: [vb.x, vb.y, vb.width, vb.height], nodes };
}
const rcConfig = { startOnLoad: false, securityLevel: "strict", flowchart: { useMaxWidth: false }, themeVariables: { fontSize: "16px" } };"""

RENDER_PAGE = """<!doctype html><meta charset="utf-8"><body><pre id="rc-out"></pre>
<script type="module">
__MEASURE__
const out = document.getElementById("rc-out");
try {
  const { default: mermaid } = await import(__MERMAID__);
  mermaid.initialize(rcConfig);
  const result = {};
  for (const [name, source] of Object.entries(__SOURCES__)) {
    const host = document.createElement("div"); document.body.append(host);
    host.innerHTML = (await mermaid.render("rc-" + name, source)).svg;
    result[name] = rcMeasure(host.querySelector("svg"));
  }
  out.textContent = JSON.stringify(result);
} catch (e) { out.textContent = JSON.stringify({ error: String(e) }); }
</script>"""


def chrome_path():
    """Chrome or Chromium for drawing diagrams at write time; REASON_COMMONS_CHROME=none turns it off."""
    chosen = os.environ.get("REASON_COMMONS_CHROME")
    if chosen:
        return None if chosen == "none" else chosen
    return next((p for p in CHROME_PATHS if Path(p).exists()), None) or next((shutil.which(n) for n in CHROME_NAMES if shutil.which(n)), None)


def prerender(sources, chrome):
    """Draw each tree once in headless Chrome; None when Chrome or the network is unavailable."""
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "render.html"
        page.write_text(RENDER_PAGE.replace("__MEASURE__", MEASURE_JS).replace("__MERMAID__", json.dumps(MERMAID_JS))
                        .replace("__SOURCES__", json.dumps(sources).replace("</", "<\\/")))
        try:
            run = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
                                  f"--user-data-dir={Path(tmp) / 'profile'}", "--virtual-time-budget=60000", "--dump-dom", page.as_uri()],
                                 capture_output=True, text=True, timeout=180)
        except (OSError, subprocess.TimeoutExpired):
            return None
    found = re.search(r'<pre id="rc-out">(.*?)</pre>', run.stdout, re.S)
    try:
        data = json.loads(html.unescape(found.group(1))) if found else None
    except ValueError:
        return None
    return None if not data or "error" in data else data


def drawn_trees(root, sources, chrome):
    """Write-time drawings of each tree, reused while its source is unchanged."""
    cache_file = root / "diagrams.json"
    try:
        cache = json.loads(cache_file.read_text())
    except (OSError, ValueError):
        cache = {}
    key = lambda src: hashlib.sha256((MERMAID_JS + src).encode()).hexdigest()
    missing = {t: src for t, src in sources.items() if cache.get(t, {}).get("key") != key(src)}
    if missing and chrome:
        fresh = prerender(missing, chrome) or {}
        for t, drawing in fresh.items():
            cache[t] = {"key": key(sources[t]), **drawing}
        if fresh:
            cache = {t: cache[t] for t in sources if t in cache}
            cache_file.write_text(json.dumps(cache))
    return {t: cache[t] for t in sources if cache.get(t, {}).get("key") == key(sources[t])}


def fit(box, aspect=16 / 10):
    x, y, w, h = box
    if w / h > aspect:
        y, h = y - (w / aspect - h) / 2, w / aspect
    else:
        x, w = x - (h * aspect - w) / 2, h * aspect
    return [x, y, w, h]


def diagram_page(name, source, drawing, focus=None, record=None):
    """One self-contained pan-and-zoom page for a tree, opened on the whole tree or centred on a statement."""
    head = tree_info(name)[0]
    node, short = focus or (None, None)
    data = {"focus": short, "source": None if drawing else source, "mermaid": MERMAID_JS, "view": FOCUS_VIEW}
    body = '<p class="wait">Drawing the diagram… this needs network access to load mermaid.js.</p>'
    if drawing:
        full, box = drawing["full"], drawing["nodes"].get(short) if short else None
        start = fit([box[0] + box[2] / 2 - FOCUS_VIEW[0] / 2, box[1] + box[3] / 2 - FOCUS_VIEW[1] / 2, *FOCUS_VIEW] if box else [full[0] - 40, full[1] - 40, full[2] + 80, full[3] + 80])
        svg = drawing["svg"]
        tag = re.match(r"<svg[^>]*>", svg).group(0)
        opened = re.sub(r'\s(width|height|style|viewBox)="[^"]*"', "", tag)[:-1] + f' width="100%" height="100%" preserveAspectRatio="xMidYMid meet" viewBox="{" ".join(f"{v:g}" for v in start)}">'
        outline = f'<rect class="rc-focus" x="{box[0] - 6:g}" y="{box[1] - 6:g}" width="{box[2] + 12:g}" height="{box[3] + 12:g}" rx="8" fill="none" stroke="#2563eb" stroke-width="8" pointer-events="none"/>' if box else ""
        body = svg.replace(tag, opened, 1).rpartition("</svg>")
        body = body[0] + outline + "</svg>" + body[2]
        data.update(full=full, box=box)
    title_text = f"{head} — {node['text']}" if node else f"{head} — whole tree"
    meta = ""
    if node:
        work = " · ".join("⚑ " + t["work"].replace("_", " ") for t in node.get("_work", []))
        where = f' · <a href="{html.escape(record["yaml"])}">recorded in {html.escape(record["yaml_label"])}</a>' if record else ""
        meta = (f'<div class="meta">{html.escape(title(node["kind"]))} · {status(node)} · <code>{html.escape(node["id"])}</code>'
                f'{" · " + html.escape(work) if work else ""}{where}</div>')
    statement = f'<span class="s" title="{html.escape(node["text"])}">Centred on: {html.escape(node["text"])}</span>' if node else '<span class="s">Whole tree</span>'
    page = DIAGRAM_PAGE
    for k, v in (("__TITLE__", html.escape(title_text)), ("__HEAD__", html.escape(head)), ("__STATEMENT__", statement), ("__META__", meta),
                 ("__HOME__", '<button id="home" title="Back to the statement (C)">Centre statement</button>' if node else ""),
                 ("__BODY__", body), ("__MEASURE__", MEASURE_JS), ("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))):
        page = page.replace(k, v)
    return page


def write_pages(state, state_path, out=None, chrome="auto"):
    """Write one diagram page per tree and one per statement; returns the directory holding trees/ and nodes/."""
    root = Path(out) if out else pages_dir(state_path)
    (root / "trees").mkdir(parents=True, exist_ok=True)
    (root / "nodes").mkdir(parents=True, exist_ok=True)
    names = [t for t in ordered(state["trees"]) if state["trees"][t]["nodes"]]
    built = {t: diagram_source(t, state["trees"][t]) for t in names}
    drawings = drawn_trees(root, {t: src for t, (src, _) in built.items()}, chrome_path() if chrome == "auto" else chrome)
    records = record_links(state, state_path) if state_path else {}
    keep = set()
    for t in names:
        source, short = built[t]
        tree = state["trees"][t]
        (root / "trees" / f"{t}.html").write_text(diagram_page(t, source, drawings.get(t)))
        work = {}
        for task in tree["backlog"]:
            work.setdefault(task["ref"], []).append(task)
        for n in tree["nodes"]:
            keep.add(f"{n['id']}.html")
            node = {**n, "_work": [w for w in work.get(n["id"], []) if w["work"] not in QUIET_WORK]}
            (root / "nodes" / f"{n['id']}.html").write_text(diagram_page(t, source, drawings.get(t), (node, short[n["id"]]), records.get(n["id"])))
    for stale in [*(root / "nodes").glob("*.html"), *(root / "trees").glob("*.html")]:
        if stale.parent.name == "nodes" and stale.name not in keep or stale.parent.name == "trees" and stale.stem not in names:
            stale.unlink()
    (root / "trees.html").unlink(missing_ok=True)  # the retired text-tree page
    return root


DIAGRAM_PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
html,body{margin:0;height:100%;background:#fff;color:#17212e;font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
body{display:flex;flex-direction:column}
header{flex:none;display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;padding:8px 12px;border-bottom:1px solid #e3e6ea;background:#fafbfc}
header .t{font-weight:600;margin-right:4px}
header .s{color:#3d4652;flex:1 1 20ch;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
header .meta{flex-basis:100%;color:#5b6573;font-size:12.5px}
header .meta code{font-size:12px}
header .hint{color:#5b6573;font-size:12.5px}
button{font:inherit;min-width:34px;padding:4px 10px;border:1px solid #c9ced6;border-radius:6px;background:#fff;color:inherit;cursor:pointer}
button:hover{background:#eef1f5}
#view{flex:1;min-height:0;overflow:hidden;cursor:grab;touch-action:none;user-select:none}
#view.drag{cursor:grabbing}
#view svg{display:block}
#view .wait{padding:24px;color:#5b6573}
</style></head><body>
<header><span class="t">__HEAD__</span>__STATEMENT__
<button id="zin" title="Zoom in (+)" aria-label="Zoom in">+</button><button id="zout" title="Zoom out (−)" aria-label="Zoom out">−</button>
<button id="fit" title="Whole tree (0)">Whole tree</button>__HOME__
<span class="hint">Drag to pan · scroll to move · pinch or ⌘/Ctrl-scroll to zoom</span>__META__</header>
<div id="view" role="img" aria-label="__TITLE__">__BODY__</div>
<script type="module">
__MEASURE__
const D = __DATA__, box = document.getElementById("view");
if (D.source) {
  try {
    const { default: mermaid } = await import(D.mermaid);
    mermaid.initialize(rcConfig);
    box.innerHTML = (await mermaid.render("rc-diagram", D.source)).svg;
    const m = rcMeasure(box.querySelector("svg"));
    D.full = m.full; D.box = D.focus ? m.nodes[D.focus] : null;
    const svg = box.querySelector("svg");
    for (const a of ["width", "height", "style"]) svg.removeAttribute(a);
    svg.setAttribute("width", "100%"); svg.setAttribute("height", "100%");
    if (D.box) {
      const r = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      for (const [k, v] of Object.entries({ class: "rc-focus", x: D.box[0] - 6, y: D.box[1] - 6, width: D.box[2] + 12, height: D.box[3] + 12, rx: 8, fill: "none", stroke: "#2563eb", "stroke-width": 8, "pointer-events": "none" })) r.setAttribute(k, v);
      svg.append(r);
    }
  } catch (e) { box.innerHTML = '<p class="wait">The diagram could not be drawn here: ' + String(e).replace(/</g, "&lt;") + "</p>"; throw e; }
}
const svg = box.querySelector("svg"), full = D.full;
const START = D.box ? [D.box[0] + D.box[2] / 2 - D.view[0] / 2, D.box[1] + D.box[3] / 2 - D.view[1] / 2, ...D.view] : [full[0] - 40, full[1] - 40, full[2] + 80, full[3] + 80];
let v;
const size = () => [box.clientWidth || 1, box.clientHeight || 1];
function show([x, y, w, h]) {
  const [cw, ch] = size(), a = cw / ch;
  if (w / h > a) { y -= (w / a - h) / 2; h = w / a; } else { x -= (h * a - w) / 2; w = h * a; }
  v = [x, y, w, h]; svg.setAttribute("viewBox", v.join(" "));
}
function zoom(f, px, py) {
  const [cw, ch] = size(); if (px == null) { px = cw / 2; py = ch / 2; }
  const k = Math.min(Math.max(v[2] * f, 150), full[2] * 4) / v[2];
  const ux = v[0] + px / cw * v[2], uy = v[1] + py / ch * v[3];
  show([ux - px / cw * v[2] * k, uy - py / ch * v[3] * k, v[2] * k, v[3] * k]);
}
function pan(dx, dy) { const s = v[2] / size()[0]; show([v[0] - dx * s, v[1] - dy * s, v[2], v[3]]); }
const whole = () => show([full[0] - 40, full[1] - 40, full[2] + 80, full[3] + 80]), home = () => show(START);
home();
addEventListener("resize", () => show(v));
box.addEventListener("wheel", e => {
  e.preventDefault(); const r = box.getBoundingClientRect();
  if (e.ctrlKey || e.metaKey) zoom(Math.exp(Math.max(-25, Math.min(25, e.deltaY)) * 0.01), e.clientX - r.left, e.clientY - r.top);
  else pan(-e.deltaX, -e.deltaY);
}, { passive: false });
const pts = new Map(); let span = null;
box.addEventListener("pointerdown", e => { box.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]); box.classList.add("drag"); span = null; });
box.addEventListener("pointermove", e => {
  if (!pts.has(e.pointerId)) return;
  const prev = pts.get(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]);
  if (pts.size === 1) return pan(e.clientX - prev[0], e.clientY - prev[1]);
  const [a, b] = [...pts.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]), r = box.getBoundingClientRect();
  if (span) zoom(span / d, (a[0] + b[0]) / 2 - r.left, (a[1] + b[1]) / 2 - r.top);
  span = d;
});
const up = e => { pts.delete(e.pointerId); span = null; if (!pts.size) box.classList.remove("drag"); };
box.addEventListener("pointerup", up); box.addEventListener("pointercancel", up);
document.getElementById("zin").onclick = () => zoom(1 / 1.25);
document.getElementById("zout").onclick = () => zoom(1.25);
document.getElementById("fit").onclick = whole;
const homeButton = document.getElementById("home"); if (homeButton) homeButton.onclick = home;
addEventListener("keydown", e => {
  if (e.key === "+" || e.key === "=") zoom(1 / 1.25); else if (e.key === "-") zoom(1.25);
  else if (e.key === "0") whole(); else if ((e.key === "c" || e.key === "C") && homeButton) home();
  else if (e.key.startsWith("Arrow")) pan({ ArrowLeft: 80, ArrowRight: -80 }[e.key] || 0, { ArrowUp: 80, ArrowDown: -80 }[e.key] || 0);
});
</script>
</body></html>
"""


TREE_FORMATS = ("tree-markdown", "tree-text")
MERMAID_FORMATS = ("widget", "markdown", "mermaid", "text")


def tree_of(state, ident):
    return next((t for t, content in state["trees"].items() if any(n["id"] == ident for n in content["nodes"])), None)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("state", type=Path, nargs="?")
    parser.add_argument("--wrap", action="store_true", help="wrap Mermaid source from stdin in the pan-and-zoom frame")
    parser.add_argument("--heading", help="with --wrap: the label line above the diagram")
    parser.add_argument("--footer", default="", help="with --wrap: an optional line below the diagram")
    parser.add_argument("--counts", action="store_true", help="print per-tree node counts by standing for the view menu")
    parser.add_argument("--tree", help="tree key, such as current_reality; tree views default to the tree of --focus, else the first tree with statements")
    parser.add_argument("--format", choices=TREE_FORMATS + MERMAID_FORMATS,
                        help="tree-markdown (default): linked nested list for a chat reply; tree-text: terminal text; "
                             "widget, markdown, mermaid, text: one-standing Mermaid views, drawn only on request")
    parser.add_argument("--standing", choices=STANDINGS, help="Mermaid formats: the one standing drawn (default accepted, or proposed when nothing is accepted); tree formats: the standing highlighted")
    parser.add_argument("--highlight", choices=("all",) + STANDINGS + ("open",), help="tree formats: dim everything else; open = disputed or flagged for work")
    parser.add_argument("--focus", action="append", default=[], metavar="NODE", help="tree formats: zoom to this statement's path and branch (repeatable)")
    parser.add_argument("--page", nargs="?", const=True, metavar="DIR", help="write the diagram pages, DIR/trees/<tree>.html and DIR/nodes/<node-id>.html (default DIR: .<state-stem>/ beside the state)")
    parser.add_argument("--page-url", help="tree-text and tree-markdown: link to the diagram pages published under this address instead of writing them locally")
    parser.add_argument("--links", choices=("auto", "always", "never"), default="auto", help="tree-text: OSC 8 hyperlinks (auto: only when printing to a terminal)")
    parser.add_argument("--width", type=int, help="tree-text: wrap width (default: the terminal width, else 100)")
    parser.add_argument("--ids", action="store_true", help="tree-text: show statement IDs")
    args = parser.parse_args()
    if args.wrap:
        if not args.heading:
            parser.error("--wrap needs --heading")
        print(frame(sys.stdin.read().strip(), args.heading, args.footer))
        return
    if args.state is None:
        parser.error("give a state file, or use --wrap")
    try:
        state = load(args.state)
        validate(state)
    except (OSError, ValueError) as error:
        sys.exit(f"Cannot read {args.state}: {error}")
    PEOPLE.update(state["participants"], assistant="assistant")
    if args.counts:
        print(counts(state))
        return
    page_only = args.page and not args.tree and not args.focus and args.format is None
    args.format = args.format or "tree-markdown"
    tree_format = args.format in TREE_FORMATS
    pages = lambda: write_pages(state, args.state, None if args.page in (None, True) else args.page)
    if page_only:
        root = pages()
        print(root.resolve().as_uri() + "/")
        for name in ordered(state["trees"]):
            if state["trees"][name]["nodes"]:
                print(f"  {tree_info(name)[0]}: {page_href(pages_base(root), 'trees', name)}")
        return
    if args.focus and not tree_format:
        parser.error("--focus works with the tree formats only")
    if tree_format and not args.tree:
        home = tree_of(state, args.focus[0]) if args.focus else None
        if args.focus and home is None:
            sys.exit(f"--focus {args.focus[0]} is not a statement in any tree")
        args.tree = home or next((t for t in ordered(state["trees"]) if state["trees"][t]["nodes"]), None)
        if args.tree is None:
            sys.exit("There are no trees to view yet.")
    if args.tree not in state["trees"]:
        sys.exit(f"--tree must be one of: {', '.join(ordered(state['trees']))}")
    for ident in args.focus:
        if tree_of(state, ident) != args.tree:
            sys.exit(f"--focus {ident} is not a statement in the {tree_info(args.tree)[0].lower()}")
    tree = state["trees"][args.tree]
    if not tree["nodes"]:
        sys.exit(f"{tree_info(args.tree)[0]} has no statements yet. {counts(state).replace(chr(10), '; ')}")
    if not tree_format:
        standing = args.standing or default_standing(tree)
        if not any(status(n) == standing for n in tree["nodes"]):
            sys.exit(f"{title(args.tree)} has no {standing} nodes. {not_shown(tree, standing)}")
        if args.page:
            pages()
        if args.format == "text":
            print(text_outline(args.tree, tree, standing))
        elif args.format == "markdown":
            print(markdown(args.tree, tree, standing))
        elif args.format == "mermaid":
            print(mermaid(args.tree, tree, standing)[0])
        else:
            print(widget(args.tree, tree, standing))
        return
    highlight = args.highlight or args.standing
    tty = sys.stdout.isatty()
    links = args.links == "always" or (args.links == "auto" and tty)
    wants_page = args.page or (not args.page_url and (args.format == "tree-markdown" or (args.format == "tree-text" and links)))
    try:
        root = pages() if wants_page else None
        published = args.page_url.rstrip("/") + "/" if args.page_url else None
        if args.format == "tree-markdown":
            # In a chat reply, a path relative to the working directory is what desktop apps open beside the conversation.
            print(markdown_tree(state, args.tree, published or pages_base(root, relative=True), args.focus, highlight))
        else:
            width = args.width or (shutil.get_terminal_size((100, 24)).columns if tty else 100)
            ansi = tty and not os.environ.get("NO_COLOR")
            base = published or (pages_base(root) if root else None)
            print(text_tree(state, args.tree, ansi, base if links else None, highlight, args.focus, width, args.ids))
    except ValueError as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
