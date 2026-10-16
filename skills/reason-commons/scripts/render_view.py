#!/usr/bin/env python3
"""Render the reasoning trees for reading, straight from the YAML.

The default view is a text tree read from the top node down: glyph shape names
the role, glyph fill names the standing (solid accepted, hollow proposed,
✕ disputed) and the rail names the link standing (│ accepted, ┊ proposed,
┆ disputed). Every standing is shown; a highlight dims the rest.

  render_view.py STATE --counts                         view-menu counts per tree
  render_view.py STATE --tree T                         inline widget HTML (all trees, opened on T)
  render_view.py STATE --tree T --format tree-markdown  linked nested list for a chat reply
  render_view.py STATE --tree T --format tree-text      terminal text with OSC 8 links
  render_view.py STATE --focus NODE [--format …]        zoomed to NODE's path and branch
  render_view.py STATE --page [PATH]                    write the all-trees page and list its links
  render_view.py STATE --tree T --standing S --format widget|markdown|mermaid|text
                                                        one-standing Mermaid views, on request only
  render_view.py --wrap --heading "LAST CHANGE: PROPOSED · …" < diagram.mmd
                                                        any Mermaid source in the frame

Widget and Markdown output is complete: pass it unchanged to the host's widget
tool or return it unchanged in the reply. Tree-markdown and tree-text link every
tree and statement name to PAGE#<tree> or PAGE#<node-id>, which opens the page
zoomed to that statement; they write the page beside the state unless
--page-url names a published copy. Counts, topology and standing markers come
from the state, so the conversation never has to count or lay out nodes by hand.
"""

import argparse
import html
import json
import os
from pathlib import Path
import shutil
import sys
import textwrap
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
    "supports": ("to", "supported by", False),
    "challenges": ("to", "challenged by", False),
    "supersedes": ("from", "replaces", False),
    "blocks": ("to", "blocked by", False),
    "overcomes": ("to", "cleared by", False),
    "precedes": ("from", "then", False),
    "conflicts_with": ("from", "conflicts with", True),
}
TRACE_WORDS = {"addresses": "addresses", "implements": "implements", "derived_from": "from"}
QUIET_WORK = {"review_relation", "test_causality"}


def tree_info(name):
    return TREE_INFO.get(name, (title(name), title(name), "•", "", "Read down."))


def relation_row(tree_name, relation):
    if relation == "produces":
        return ("from", "expect", False) if tree_name == "transition" else ("to", "produced by", False)
    return RELATION_ROWS.get(relation, ("to", relation.replace("_", " "), False))


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
        else:
            if len(l["from"]) != 1:
                raise ValueError(f"{l['id']}: a {l['relation']} link cannot start from joint conditions")
            parent, children = l["from"][0], [l["to"]]
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
    """The tree as indented text; ANSI styling and OSC 8 links into the page are optional."""
    model = tree_model(state, name)
    rows = flatten(model)
    keep = focus_rows(model, rows, focus)
    head, _, _, question, reading = tree_info(name)
    verb_width = max([len(r["n"].get("verb", "")) for r in rows] + [4])
    sty = lambda kind, s: f"\x1b[{ANSI[kind]}m{s}\x1b[0m" if ansi and kind and s else s
    url = lambda ident: f"{link_base}#{ident}" if link_base else None
    osc = lambda target, s: f"\x1b]8;;{target}\x1b\\{s}\x1b]8;;\x1b\\" if target else s
    pipe = lambda st: "   " if st is None else {"accepted": "│  ", "disputed": "┆  "}.get(st, "┊  ")
    rail_char = lambda st: {"accepted": "│", "disputed": "┆"}.get(st, "┊")
    out = [osc(url(name), sty("bold", head.upper())) + sty("dim", "  " + question), sty("dim", counts_line(model)),
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
    """A nested Markdown list in which every tree and statement name is a link into the page."""
    model = tree_model(state, name)
    rows = flatten(model)
    keep = focus_rows(model, rows, focus)
    head, _, _, question, _ = tree_info(name)
    href = lambda ident: f"{link_base}#{ident}"
    out = [f"**[{head}]({href(name)})** · {question}", ""]

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
        out += ["", f"Zoomed to {plural(len(focus), 'statement')}, with the path from the top and the whole branch. [Show the whole tree]({href(name)})."]
    return "\n".join(out)


def page_path(state_path):
    state_path = Path(state_path)
    return state_path.parent / f".{state_path.stem}" / "trees.html"


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


def page_data(state, state_path=None, start_tree=None, focus=(), highlight=None, standalone=True):
    order = [t for t in ordered(state["trees"]) if state["trees"][t]["nodes"]]
    return {
        "rid": f"rct-{uuid.uuid4().hex[:8]}",
        "standalone": standalone,
        "order": order,
        "trees": {t: tree_model(state, t) for t in order},
        "info": {t: tree_info(t) for t in order},
        "glyphs": GLYPHS,
        "people": dict(PEOPLE),
        "records": record_links(state, state_path) if state_path else {},
        "start": {"tree": start_tree or (order[0] if order else None), "focus": list(focus), "highlight": highlight or "all"},
    }


def tree_widget(state, name, state_path=None, focus=(), highlight=None):
    """Self-contained HTML fragment for a host's inline widget tool: all trees, opened on one."""
    data = page_data(state, state_path, name, focus, highlight, standalone=False)
    return TREE_VIEW.replace("__RID__", data["rid"]).replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))


def write_page(state, state_path, out=None):
    """Write the all-trees page; a link to PAGE#<tree> or PAGE#<node-id> opens it there."""
    target = Path(out) if out else page_path(state_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    data = page_data(state, state_path)
    body = TREE_VIEW.replace("__RID__", data["rid"]).replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    target.write_text(
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{html.escape(str(state.get('project') or 'Reasoning trees'))} · trees</title></head>\n<body>\n{body}\n</body></html>\n"
    )
    return target


TREE_FORMATS = ("tree", "tree-markdown", "tree-text")
MERMAID_FORMATS = ("widget", "markdown", "mermaid", "text")

TREE_VIEW = r"""<style>
.rct{--ink:var(--text-primary,#1a1e1c);--ink-2:var(--text-secondary,#4f5753);--ink-3:var(--text-tertiary,#7d8681);--panel:var(--surface-1,#ffffff);--rule:var(--border,#dfe3e0);--rail:#a3aba7;
  --acc:#1d7a5c;--pro:#a7600c;--dis:#c13d36;--flag:#8a5a00;--sel:#e8eff7;--focus:#2d5b8c;
  font:15px/1.5 var(--font-sans,system-ui,-apple-system,"Segoe UI",sans-serif);color:var(--ink);background:var(--panel);border:1px solid var(--rule);border-radius:10px;overflow:hidden;max-width:1100px;margin:0 auto}
@media (prefers-color-scheme:dark){.rct{--ink:var(--text-primary,#e4e8e5);--ink-2:var(--text-secondary,#aab3ae);--ink-3:var(--text-tertiary,#78837e);--panel:var(--surface-1,#181c1a);--rule:var(--border,#2c322f);--rail:#5b6560;--acc:#4fc497;--pro:#e2a246;--dis:#f0726a;--flag:#e2b55a;--sel:#1d2833;--focus:#8db6e6;color-scheme:dark}}
:root[data-mode="dark"] .rct{--rail:#5b6560;--acc:#4fc497;--pro:#e2a246;--dis:#f0726a;--flag:#e2b55a;--sel:#1d2833;--focus:#8db6e6}
.rct *{box-sizing:border-box}
.rct a{color:inherit}
.rct .tabs{display:flex;overflow-x:auto;border-bottom:1px solid var(--rule)}
.rct .tabs a{flex:0 0 auto;text-decoration:none;padding:10px 13px 8px;font-size:14px;color:var(--ink-2);border-bottom:2px solid transparent;white-space:nowrap}
.rct .tabs a b{font-family:ui-monospace,Menlo,Consolas,monospace;margin-right:6px;color:var(--ink-3);font-weight:500}
.rct .tabs a small{display:block;font:11px/1.3 ui-monospace,Menlo,Consolas,monospace;color:var(--ink-3)}
.rct .tabs a[aria-current="page"]{color:var(--ink);border-bottom-color:var(--ink)}
.rct .bar{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;padding:9px 14px;border-bottom:1px solid var(--rule);font-size:13px;color:var(--ink-2)}
.rct .seg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--rule);border-radius:7px;overflow:hidden}
.rct .seg button{font:500 12.5px/1 inherit;font-family:inherit;color:var(--ink-2);background:transparent;border:0;border-right:1px solid var(--rule);padding:7px 9px;cursor:pointer}
.rct .seg button:last-child{border-right:0}
.rct .seg button[aria-pressed="true"]{background:var(--ink);color:var(--panel)}
.rct button:focus-visible,.rct .row:focus-visible,.rct a:focus-visible{outline:2px solid var(--focus);outline-offset:1px}
.rct .legend{display:flex;flex-wrap:wrap;gap:3px 14px;padding:8px 14px;border-bottom:1px solid var(--rule);font-size:12.5px;color:var(--ink-2)}
.rct .legend b{font:500 14px ui-monospace,Menlo,Consolas,monospace;color:var(--ink);margin-right:4px}
.rct .legend .note{flex-basis:100%;color:var(--ink-3)}
.rct .stage{padding:14px 14px 10px;max-height:min(72vh,860px);overflow:auto;overscroll-behavior:contain}
.rct .head .q{font-weight:600;font-size:17px}
.rct .head .q small{font-weight:400;font-size:14px;color:var(--ink-2);margin-left:6px}
.rct .head .counts{font:12px/1.5 ui-monospace,Menlo,Consolas,monospace;color:var(--ink-2);margin:2px 0 10px}
.rct .fbar{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;margin:0 0 10px;padding:7px 10px;border-radius:7px;background:var(--sel);font-size:13px;color:var(--ink-2)}
.rct .fbar:empty{display:none}
.rct .fbar b{color:var(--ink)}
.rct .btn{font:500 12.5px inherit;font-family:inherit;background:var(--panel);color:var(--ink);border:1px solid var(--rule);border-radius:6px;padding:4px 9px;cursor:pointer}
.rct .row{display:flex;align-items:stretch;border-radius:5px}
.rct .row:hover{background:color-mix(in srgb,var(--sel) 55%,transparent)}
.rct .row.sel{background:var(--sel);box-shadow:inset 3px 0 0 var(--focus)}
.rct .row.root{margin-top:12px}
.rct .row.first{margin-top:0}
.rct .row.dim{opacity:.28}
.rct .gap{font:12px ui-monospace,Menlo,Consolas,monospace;color:var(--ink-3);padding:2px 0 2px 2px}
.rct .rail{flex:0 0 1.35em;position:relative}
.rct .rail::before,.rct .rail::after{content:"";position:absolute}
.rct .rail.pipe::before,.rct .rail.tee::before{left:.45em;top:0;bottom:0;border-left:1.5px var(--ls,dashed) var(--rail)}
.rct .rail.elbow::before{left:.45em;top:0;height:.78em;border-left:1.5px var(--ls,dashed) var(--rail)}
.rct .rail.tee::after,.rct .rail.elbow::after{left:.45em;top:.78em;width:.8em;border-top:1.5px var(--ls,dashed) var(--rail)}
.rct .rail.accepted{--ls:solid}
.rct .rail.disputed{--ls:dotted}
.rct .verb{flex:0 0 auto;width:var(--vw);font:500 10.5px/2.15 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-3);padding-left:.25em;white-space:nowrap}
.rct .glyph{flex:0 0 1.5em;font:500 15px/1.5 ui-monospace,Menlo,Consolas,monospace;text-align:center}
.rct .glyph.accepted{color:var(--acc)}.rct .glyph.proposed{color:var(--pro)}.rct .glyph.disputed{color:var(--dis)}.rct .glyph.and{color:var(--ink-3)}
.rct .body{flex:1 1 auto;min-width:0;padding:0 .4em .1em .2em}
.rct .root>.body{font-weight:600}
.rct .struck{text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--dis) 70%,transparent);color:var(--ink-2)}
.rct .ref .body{font-weight:400;color:var(--ink-2)}
.rct .ref .body a{text-decoration-color:var(--rail);text-underline-offset:3px}
.rct .group .body{font-style:italic;color:var(--ink-3);font-weight:400}
.rct .meta{display:inline-flex;flex-wrap:wrap;gap:4px;margin-left:6px;vertical-align:1px;font-weight:400}
.rct .chip{font:500 11px/1 ui-monospace,Menlo,Consolas,monospace;padding:3px 5px;border-radius:4px;border:1px solid var(--rule);color:var(--ink-2);white-space:nowrap;text-decoration:none}
.rct a.chip:hover{border-color:var(--ink-3);color:var(--ink)}
.rct .chip.by{border-color:color-mix(in srgb,var(--acc) 45%,var(--rule));color:var(--acc)}
.rct .chip.by i{font-style:normal;opacity:.35}
.rct .chip.flag{border-color:color-mix(in srgb,var(--flag) 45%,var(--rule));color:var(--flag)}
.rct .chip.dis{border-color:color-mix(in srgb,var(--dis) 45%,var(--rule));color:var(--dis)}
.rct .id{font:12px ui-monospace,Menlo,Consolas,monospace;color:var(--ink-3);margin-left:6px;font-weight:400}
.rct .loosehead{font:500 11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin:20px 0 6px}
.rct .detail{border-top:1px solid var(--rule);padding:9px 14px 11px;font-size:13px;color:var(--ink-2);min-height:56px}
.rct .detail b{color:var(--ink);font-weight:600}
.rct .detail .dl{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:2px 12px}
.rct .detail .dl>span:nth-child(odd){font:500 10.5px/1.9 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.rct .detail a{color:var(--focus)}
@media (max-width:560px){.rct .verb{display:none}.rct .stage{max-height:none}}
</style>
<div class="rct" id="__RID__">
<nav class="tabs" aria-label="Trees"></nav>
<div class="bar"><span>Highlight</span><span class="seg lens"><button data-v="all">Everything</button><button data-v="accepted">Accepted</button><button data-v="proposed">Proposed</button><button data-v="disputed">Disputed</button><button data-v="open">Open work</button></span><span>IDs</span><span class="seg ids"><button data-v="off">Hide</button><button data-v="on">Show</button></span></div>
<div class="legend"></div>
<div class="stage" tabindex="-1"></div>
<div class="detail" aria-live="polite"></div>
</div>
<script>
(() => {
const D = __DATA__;
const root = document.getElementById(D.rid), $ = s => root.querySelector(s);
const S = {tree: D.start.tree, lens: D.start.highlight || "all", ids: "off", sel: null, focus: false};
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const kname = k => k === "and" ? "conditions acting together" : k.replace(/_/g, " ");
const glyph = n => { if (n.group) return "∧"; const g = D.glyphs[n.kind] || "•◦"; return (n.standing === "disputed" ? "✕" : "") + (n.standing === "accepted" ? g[0] : g[1]); };
const ORDER = ["rufus", "david"].filter(p => p in D.people).concat(Object.keys(D.people).filter(p => p !== "rufus" && p !== "david" && p !== "assistant"));
const ini = p => (D.people[p] || p)[0].toUpperCase();
const INDEX = {}, ROWS = {};
for (const t of D.order) {
  const walk = n => { if (!n.ref && !n.group && !INDEX[n.id]) INDEX[n.id] = {tree: t, n}; n.children.forEach(walk); };
  D.trees[t].roots.forEach(walk); D.trees[t].loose.forEach(walk);
}
function rows(t) {
  if (ROWS[t]) return ROWS[t];
  const out = [], st = c => c.link ? c.link.standing : "proposed";
  const walk = (n, depth, rails, last, cont, parent) => {
    const r = {n, depth, rails, last, parent, idx: out.length};
    r.key = n.ref ? n.id + "~" + out.length : (n.group ? "and~" + n.id : n.id);
    out.push(r);
    const kids = n.children; r.kidStyle = kids.length ? st(kids[0]) : null;
    kids.forEach((c, i) => { const l = i === kids.length - 1; walk(c, depth + 1, depth === 0 ? [] : rails.concat([last ? null : cont]), l, l ? null : st(kids[i + 1]), r); });
    r.end = out.length;
  };
  D.trees[t].roots.forEach(n => walk(n, 0, [], true, null, null));
  const loose = D.trees[t].loose.map(n => ({n, depth: 0, rails: [], last: true, key: n.id, loose: true, parent: null}));
  return ROWS[t] = {main: out, loose};
}
const allRows = t => [...rows(t).main, ...rows(t).loose];
function matches(r) {
  const n = r.n;
  if (S.lens === "all") return true;
  if (n.group) { const m = rows(S.tree).main; for (let i = r.idx + 1; i < r.end; i++) if (matches(m[i])) return true; return false; }
  if (S.lens === "open") return n.flags.length > 0 || n.standing === "disputed";
  return n.standing === S.lens;
}
function visible(t) {
  if (!S.focus || !S.sel) return null;
  const {main, loose} = rows(t), r = main.find(x => x.key === S.sel);
  if (!r) return loose.some(x => x.key === S.sel) ? new Set(["__loose__", S.sel]) : null;
  const v = new Set(); for (let p = r; p; p = p.parent) v.add(p.key);
  for (let i = r.idx; i < r.end; i++) v.add(main[i].key);
  return v;
}
function counts(t) {
  const m = D.trees[t], f = o => Object.entries(o).filter(([, n]) => n).map(([s, n]) => n + " " + s).join(", ");
  return `${m.nodes} statements (${f(m.standing)}) · ${m.links} links (${f(m.link_standing) || "none"})`;
}
const refLabel = rf => `↗ ${rf.rel} ${INDEX[rf.id] ? glyph(INDEX[rf.id].n) : ""} ${rf.tree ? D.info[rf.tree][1] : "?"}`;
function drawTree(t) {
  const {main, loose} = rows(t), vis = visible(t);
  const el = document.createElement("div");
  el.style.setProperty("--vw", (Math.max(4, ...main.map(r => (r.n.verb || "").length)) * 0.72 + 0.6) + "em");
  let folded = 0, first = true;
  const gap = () => { if (folded) { const d = document.createElement("div"); d.className = "gap"; d.textContent = `⋯ ${folded} row${folded === 1 ? "" : "s"} folded`; el.appendChild(d); folded = 0; } };
  const mk = r => {
    const n = r.n, row = document.createElement("div");
    row.className = "row" + (r.depth === 0 && !r.loose ? " root" : "") + (r.depth === 0 && first ? " first" : "") + (matches(r) ? "" : " dim") + (S.sel === r.key ? " sel" : "") + (n.ref ? " ref" : "") + (n.group ? " group" : "");
    if (r.depth === 0) first = false;
    row.tabIndex = 0; row.dataset.key = r.key; row._r = r;
    r.rails.forEach(st => { const c = document.createElement("span"); c.className = "rail" + (st ? " pipe " + st : ""); row.appendChild(c); });
    if (r.depth > 0) {
      const c = document.createElement("span"); c.className = "rail " + (r.last ? "elbow " : "tee ") + n.link.standing; row.appendChild(c);
      const v = document.createElement("span"); v.className = "verb"; v.textContent = n.verb || ""; row.appendChild(v);
    }
    const g = document.createElement("span"); g.className = "glyph " + (n.group ? "and" : n.standing); g.textContent = glyph(n); g.setAttribute("aria-label", n.standing + " " + kname(n.kind)); row.appendChild(g);
    const b = document.createElement("span"); b.className = "body";
    b.innerHTML = n.ref ? `↑ <a href="#${esc(n.id)}" title="Go to where this statement is drawn in full">${esc(n.text)}</a>` : `<span class="${n.struck ? "struck" : ""}">${esc(n.text)}</span>`;
    if (!n.ref && !n.group) {
      const m = [];
      if (n.standing === "accepted" && n.by.length) m.push(`<span class="chip by" title="Accepted by ${esc(n.by.map(p => D.people[p] || p).join(" and "))}">${ORDER.map(p => n.by.includes(p) ? ini(p) : `<i>${ini(p)}</i>`).join(" ")}</span>`);
      if (n.standing === "disputed") m.push(`<span class="chip dis">disputed</span>`);
      n.flags.forEach(f => m.push(`<span class="chip flag" title="${esc(f.note)}">⚑ ${esc(f.work)}</span>`));
      n.refs.forEach(rf => m.push(`<a class="chip" href="#${esc(rf.id)}" title="${esc(INDEX[rf.id] ? INDEX[rf.id].n.text : rf.id)}">${esc(refLabel(rf))}</a>`));
      if (m.length) b.insertAdjacentHTML("beforeend", `<span class="meta">${m.join("")}</span>`);
    }
    if (S.ids === "on" && !n.group) b.insertAdjacentHTML("beforeend", `<span class="id">${esc(n.id)}</span>`);
    row.appendChild(b);
    return row;
  };
  main.forEach(r => { if (vis && !vis.has(r.key)) { folded++; return; } gap(); el.appendChild(mk(r)); });
  const shown = vis && !vis.has("__loose__") ? [] : loose.filter(r => !vis || vis.has(r.key));
  if (!shown.length) folded += loose.length;
  gap();
  if (shown.length) {
    el.insertAdjacentHTML("beforeend", `<div class="loosehead">Not linked to anything yet</div>`);
    shown.forEach(r => el.appendChild(mk(r)));
    folded += loose.length - shown.length; gap();
  }
  return el;
}
function detail(r) {
  const d = $(".detail");
  if (!r) { d.textContent = "Click a row, or focus one and use ↑ ↓, to see its ID, its links and where it was recorded. Enter zooms to its branch; Esc zooms out."; return; }
  const n = r.n, t = S.tree, rec = D.records[n.id], out = [];
  if (n.group) out.push(["Link", `<b>conditions acting together</b> · <code>${esc(n.id)}</code> · ${n.standing}`]);
  else out.push(["Statement", `<b>${esc(kname(n.kind))}</b> in the <a href="#${t}">${esc(D.info[t][0])}</a> · ${n.standing}${n.standing === "accepted" && n.by.length ? " by " + esc(n.by.map(p => D.people[p] || p).join(" and ")) : ""} · <code>${esc(n.id)}</code>`]);
  if (n.ref) out.push(["Drawn in full", `<a href="#${esc(n.id)}">under its first parent</a>`]);
  if (n.link) out.push(["Link", `${n.verb ? esc(n.verb) + " the row above" : "part of the group above"} · <code>${esc(n.link.id)}</code> · ${n.link.standing}`]);
  n.challenges.forEach(c => out.push(["Challenge", esc(c.text) + (c.by ? ` <span style="color:var(--ink-3)">· ${esc(D.people[c.by] || c.by)}</span>` : "")]));
  n.flags.forEach(f => out.push(["Open work", `<b>${esc(f.work)}</b>${f.note ? " · " + esc(f.note) : ""}`]));
  n.refs.forEach(rf => out.push([rf.rel, `<a href="#${esc(rf.id)}">${esc(INDEX[rf.id] ? INDEX[rf.id].n.text : rf.id)}</a> <span style="color:var(--ink-3)">· ${rf.tree ? esc(D.info[rf.tree][0]) : "unknown tree"}</span>`]));
  if (rec) out.push(["Recorded in", `<a href="${esc(rec.yaml)}">${esc(rec.yaml_label)}</a>${rec.source ? ` · source <a href="${esc(rec.source)}">${esc(rec.source_label)}</a>` : ""}`]);
  d.innerHTML = `<div class="dl">${out.map(([k, v]) => `<span>${esc(k)}</span><span>${v}</span>`).join("")}</div>`;
}
function fbar() {
  const fb = $(".fbar"), r = S.sel ? allRows(S.tree).find(x => x.key === S.sel) : null;
  if (!fb) return;
  if (!r) { fb.innerHTML = ""; return; }
  const label = esc(glyph(r.n)) + " " + esc(r.n.text.length > 90 ? r.n.text.slice(0, 88) + "…" : r.n.text);
  fb.innerHTML = S.focus ? `<span>Zoomed to <b>${label}</b>: its path from the top and its whole branch.</span><button class="btn" data-act="out">Show whole tree</button>`
    : `<span>Selected <b>${label}</b></span><button class="btn" data-act="in">Zoom to its branch</button>`;
}
function render(center) {
  const t = S.tree, st = $(".stage");
  $(".tabs").innerHTML = D.order.map(x => `<a href="#${x}" ${x === t ? 'aria-current="page"' : ""}><b>${D.info[x][2]}</b>${esc(D.info[x][0])}<small>${D.trees[x].nodes} statements</small></a>`).join("");
  const kinds = new Set(), walk = n => { if (!n.group) kinds.add(n.kind); n.children.forEach(walk); };
  D.trees[t].roots.forEach(walk); D.trees[t].loose.forEach(walk);
  $(".legend").innerHTML = [...kinds].map(k => `<span><b>${(D.glyphs[k] || "•◦")[0]} ${(D.glyphs[k] || "•◦")[1]}</b>${esc(kname(k))}</span>`).join("")
    + `<span><b style="color:var(--acc)">●</b>accepted</span><span><b style="color:var(--pro)">○</b>proposed</span><span><b style="color:var(--dis)">✕</b>disputed</span><span><b>│ ┊ ┆</b>link accepted, proposed, disputed</span><span class="note">${esc(D.info[t][4])}</span>`;
  st.innerHTML = `<div class="fbar"></div><div class="head"><div class="q"><a href="#${t}" style="text-decoration:none">${esc(D.info[t][0])}</a><small>${esc(D.info[t][3])}</small></div><div class="counts">${esc(counts(t))}</div></div>`;
  st.appendChild(drawTree(t));
  fbar(); detail(allRows(t).find(x => x.key === S.sel) || null);
  root.querySelectorAll(".lens button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.v === S.lens)));
  root.querySelectorAll(".ids button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.v === S.ids)));
  if (center) centre();
}
function centre() {
  const st = $(".stage"), el = S.sel ? [...st.querySelectorAll(".row")].find(x => x.dataset.key === S.sel) : null;
  if (!el) { st.scrollTop = 0; return; }
  st.scrollTop = Math.max(0, el.offsetTop - st.offsetTop - st.clientHeight / 2 + el.offsetHeight / 2);
  el.focus({preventScroll: true});
}
function select(key) {
  S.sel = key;
  root.querySelectorAll(".row.sel").forEach(x => x.classList.remove("sel"));
  const row = [...root.querySelectorAll(".row")].find(x => x.dataset.key === key); if (row) row.classList.add("sel");
  fbar(); detail(allRows(S.tree).find(x => x.key === key) || null);
  if (D.standalone && !key.includes("~")) try { history.replaceState(null, "", "#" + key); } catch (e) {}
}
function route(hash) {
  const h = decodeURIComponent((hash || "").replace(/^#/, ""));
  if (D.trees[h]) { S.tree = h; S.sel = null; S.focus = false; }
  else if (INDEX[h]) { S.tree = INDEX[h].tree; S.sel = h; S.focus = true; }
  else return false;
  render(true);
  return true;
}
root.addEventListener("click", e => {
  const a = e.target.closest('a[href^="#"]');
  if (a) { const h = a.getAttribute("href"); if (D.trees[h.slice(1)] || INDEX[h.slice(1)]) { e.preventDefault(); if (D.standalone) try { history.replaceState(null, "", h); } catch (_) {} route(h); } return; }
  const act = e.target.closest("button[data-act]"); if (act) { S.focus = act.dataset.act === "in"; render(true); return; }
  const lens = e.target.closest(".lens button"); if (lens) { S.lens = lens.dataset.v; render(!!S.sel); return; }
  const ids = e.target.closest(".ids button"); if (ids) { S.ids = ids.dataset.v; render(!!S.sel); return; }
  const row = e.target.closest(".row"); if (row) select(row.dataset.key);
});
root.addEventListener("focusin", e => { const row = e.target.closest(".row"); if (row && !row.classList.contains("sel")) select(row.dataset.key); });
root.addEventListener("keydown", e => {
  if (e.key === "Escape" && S.focus) { S.focus = false; render(true); return; }
  if (e.key === "Enter" && S.sel && !S.focus && e.target.closest(".row")) { S.focus = true; render(true); return; }
  if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
  const all = [...root.querySelectorAll(".row")], i = all.indexOf(document.activeElement); if (i < 0) return;
  e.preventDefault(); const n = all[Math.max(0, Math.min(all.length - 1, i + (e.key === "ArrowDown" ? 1 : -1)))]; n.focus(); n.scrollIntoView({block: "nearest"});
});
if (D.standalone) window.addEventListener("hashchange", () => route(location.hash));
if (!(D.standalone && route(location.hash))) {
  const f = D.start.focus[0];
  if (f && INDEX[f]) route("#" + f); else render(false);
}
})();
</script>"""


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
                        help="tree (default): inline widget HTML; tree-markdown: linked nested list for chat; tree-text: terminal text; "
                             "widget, markdown, mermaid, text: one-standing Mermaid views, drawn only on request")
    parser.add_argument("--standing", choices=STANDINGS, help="Mermaid formats: the one standing drawn (default accepted, or proposed when nothing is accepted); tree formats: the standing highlighted")
    parser.add_argument("--highlight", choices=("all",) + STANDINGS + ("open",), help="tree formats: dim everything else; open = disputed or flagged for work")
    parser.add_argument("--focus", action="append", default=[], metavar="NODE", help="tree formats: zoom to this statement's path and branch (repeatable)")
    parser.add_argument("--page", nargs="?", const=True, metavar="PATH", help="write the all-trees page (default .<state-stem>/trees.html beside the state); links to PAGE#tree or PAGE#node-id open it there")
    parser.add_argument("--page-url", help="tree-text and tree-markdown: link to this page address instead of writing the local page")
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
    args.format = args.format or "tree"
    tree_format = args.format in TREE_FORMATS
    if page_only:
        target = write_page(state, args.state, None if args.page is True else args.page)
        print(target.resolve().as_uri())
        for name in ordered(state["trees"]):
            if state["trees"][name]["nodes"]:
                print(f"  {tree_info(name)[0]}: {target.resolve().as_uri()}#{name}")
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
            write_page(state, args.state, None if args.page is True else args.page)
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
        page = write_page(state, args.state, None if args.page in (None, True) else args.page).resolve().as_uri() if wants_page else None
        base = args.page_url or page
        if args.format == "tree":
            print(tree_widget(state, args.tree, args.state, args.focus, highlight))
        elif args.format == "tree-markdown":
            print(markdown_tree(state, args.tree, base, args.focus, highlight))
        else:
            width = args.width or (shutil.get_terminal_size((100, 24)).columns if tty else 100)
            ansi = tty and not os.environ.get("NO_COLOR")
            print(text_tree(state, args.tree, ansi, base if links else None, highlight, args.focus, width, args.ids))
    except ValueError as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
