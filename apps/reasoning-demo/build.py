#!/usr/bin/env python3
"""Build the deliberately selected, accepted-only Reason Commons demonstration.

Ordinary builds and CI use the reviewed public snapshot in publication.json.
Refreshing it requires an explicit working-state path and the existing allowlist.
No working-state path, approval receipt, notes or hidden reasoning is published.
"""
import argparse
from collections import defaultdict, deque
from copy import deepcopy
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import sys
import textwrap

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEST = ROOT / "website/demos/reason-commons-in-use"
TREES = {
    "goal": ("Our goal and conditions", "What does the goal depend on?", "Goal tree"),
    "current_reality": ("What stands in the way", "What is happening, and why?", "Current Reality Tree"),
    "conflict": ("Where needs pull two ways", "Which needs are we trying to meet?", "Conflict Cloud"),
    "future_reality": ("The change we have chosen", "What direction have we accepted?", "Future Reality Tree"),
    "prerequisite": ("Obstacles and prerequisites", "What would have to happen first?", "Prerequisite Tree"),
    "transition": ("Actions to take", "What actions have been recorded?", "Transition Tree"),
}
KINDS = {
    "goal": "Goal", "critical_success_factor": "Critical success factor",
    "necessary_condition": "Necessary condition", "undesirable_effect": "Undesirable effect",
    "cause": "Cause", "observation": "Observation", "objective": "Objective",
    "need": "Need", "prerequisite": "Prerequisite", "injection": "Change",
    "existing_condition": "Existing condition", "predicted_effect": "Predicted effect",
    "desirable_effect": "Desired effect", "obstacle": "Obstacle",
    "intermediate_objective": "Intermediate objective", "action": "Action",
    "expected_effect": "Expected effect",
}
RELATIONS = {"necessary_for": "is necessary for", "contributes_to": "contributes to"}
NODE_FIELDS = {"id", "kind", "text", "label", "status", "accepted_by", "contributors", "acceptance_context"}
LINK_FIELDS = {"id", "from", "to", "relation", "status", "accepted_by", "contributors", "acceptance_context"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def esc(value):
    return html.escape(str(value), quote=True)


def read_json(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            require(key not in obj, f"Duplicate key: {key}")
            obj[key] = value
        return obj
    return json.loads(path.read_text(), object_pairs_hook=unique)


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def contributors(item, people):
    result = []
    for contribution in item["contributions"]:
        who = contribution["by"]
        if contribution["attribution"] == "driver_default":
            entry = {"name": "Original contributor not identified", "role": "unknown"}
        elif who == "assistant":
            entry = {"name": "AI assistant", "role": "assistant"}
        else:
            require(who in people, f"Unselected contributor: {who}")
            entry = {"name": people[who], "role": "human"}
        if entry not in result:
            result.append(entry)
    return result


def project(state, registry):
    """Only explicit IDs and explicit fields cross the publication boundary."""
    require(state.get("schema_version") == 1, "Unsupported working-state version")
    people = registry["people"]
    result = {"projection_version": 1, **deepcopy(registry["release"]), "trees": {}}
    for name, selection in registry["selection"].items():
        require(name in TREES and name in state["trees"], f"Unknown tree: {name}")
        source = state["trees"][name]
        output = {"nodes": [], "links": []}
        for key in ("nodes", "links"):
            indexed = {item["id"]: item for item in source[key]}
            for ident in selection[key]:
                require(ident in indexed, f"Selected item is missing: {ident}")
                item = indexed[ident]
                require(item.get("status") == "accepted", f"Selected item is no longer accepted: {ident}")
                require(item.get("accepted_by"), f"Missing endorsement: {ident}")
                require(all(p in people for p in item["accepted_by"]), f"Unselected endorser: {ident}")
                public = {"id": ident, "status": "accepted",
                          "accepted_by": [people[p] for p in item["accepted_by"]],
                          "contributors": contributors(item, people),
                          "acceptance_context": item.get("acceptance_source", "No acceptance date was recorded.")}
                if key == "nodes":
                    public.update(kind=item["kind"], text=item["text"])
                    if item.get("label"):
                        public["label"] = item["label"]
                else:
                    public.update({field: deepcopy(item[field]) for field in ("from", "to", "relation")})
                output[key].append(public)
        result["trees"][name] = output
    validate_projection(result, registry)
    return result


def validate_projection(data, registry):
    require(data.get("projection_version") == 1, "Unsupported projection version")
    require(set(data) == {"projection_version", "release_id", "snapshot_date", "title", "trees"}, "Unexpected public field")
    require(set(data["trees"]) == set(registry["selection"]), "Selection/tree mismatch")
    approved_names = set(registry["people"].values())
    seen = set()
    for name, tree in data["trees"].items():
        ids = {n["id"] for n in tree["nodes"]}
        for key, allowed in (("nodes", NODE_FIELDS), ("links", LINK_FIELDS)):
            require([i["id"] for i in tree[key]] == registry["selection"][name][key], f"Selection mismatch: {name}.{key}")
            for item in tree[key]:
                ident = item["id"]
                require(ident not in seen and re.fullmatch(r"[a-z0-9-]+", ident), f"Invalid/duplicate ID: {ident}")
                seen.add(ident)
                require(set(item) <= allowed, f"Unreviewed public fields: {ident}")
                require(item.get("status") == "accepted", f"Unaccepted public item: {ident}")
                require(item.get("accepted_by") and set(item["accepted_by"]) <= approved_names, f"Invalid endorsers: {ident}")
                require(item.get("contributors"), f"Missing attribution: {ident}")
                for c in item["contributors"]:
                    require(set(c) == {"name", "role"}, f"Invalid attribution fields: {ident}")
                    require(c in ({"name": "Original contributor not identified", "role": "unknown"},
                                  {"name": "AI assistant", "role": "assistant"}) or
                            (c["role"] == "human" and c["name"] in approved_names), f"Unselected contributor: {ident}")
                require(isinstance(item.get("acceptance_context"), str), f"Missing recorded context: {ident}")
                if key == "nodes":
                    require(item.get("kind") in KINDS and isinstance(item.get("text"), str) and item["text"].strip(), f"Invalid statement: {ident}")
                else:
                    require(item.get("relation") in RELATIONS, f"Unsupported relationship: {ident}")
                    require(isinstance(item.get("from"), list) and item["from"] and len(set(item["from"])) == len(item["from"]), f"Invalid sources: {ident}")
                    require(set(item["from"] + [item["to"]]) <= ids, f"Missing accepted endpoint: {ident}")


def url(view="reasoning", tree="goal", item=None, mode=None):
    value = f"?view={view}&amp;tree={tree}"
    if item:
        value += f"&amp;item={esc(item)}"
    if mode:
        value += f"&amp;mode={mode}"
    return value + (f"#item-{esc(item)}" if item else f"#{view}")


def badge():
    return '<span class="standing"><span aria-hidden="true">✓</span> Accepted for now</span>'


def counted(number, noun):
    return f'{number} {noun}{"" if number == 1 else "s"}'


def item_card(node, name, compact=False):
    return (f'<a class="statement-card {"compact" if compact else ""}" href="{url(tree=name, item=node["id"])}" data-item="{node["id"]}">'
            f'<span class="item-kind">{esc(KINDS[node["kind"]])}</span><p>{esc(node["text"])}</p>'
            f'<span class="card-footer">Accepted by {esc(" and ".join(node["accepted_by"]))}<span aria-hidden="true">↗</span></span></a>')


def overview(data):
    nodes = {n["id"]: n for t in data["trees"].values() for n in t["nodes"]}
    goal = nodes["g-e-ltp-used-in-world"]
    factors = [n for n in data["trees"]["goal"]["nodes"] if n["kind"] == "critical_success_factor"]
    cards = ''.join(item_card(n, "goal") for n in factors)
    difficulty = ''.join(item_card(nodes[i], "current_reality", True) for i in
                         ("r-e-david-demo-confidence", "r-e-david-user-testing-held-back"))
    chosen = item_card(nodes["f-e-use-while-building"], "future_reality")
    actions = ''.join(item_card(nodes[i], "transition", True) for i in
                      ("t-e-act-friction-log", "t-e-act-own-question", "t-e-act-agreement"))
    perspectives = ''.join(f'<a class="perspective" href="{url(tree=name)}" data-route><span class="perspective-number">0{i}</span>'
                          f'<h3>{esc(title)}</h3><p>{esc(question)}</p><span class="perspective-count">{counted(len(data["trees"][name]["nodes"]), "statement")} · '
                          f'{counted(len(data["trees"][name]["links"]), "connection")} <span aria-hidden="true">↗</span></span></a>'
                          for i, (name, (title, question, _)) in enumerate(TREES.items(), 1))
    return f'''<section class="goal-panel" aria-labelledby="goal-heading"><div class="section-heading"><span class="eyebrow">Our recorded goal</span>{badge()}</div>
<h2 id="goal-heading">Help people think and act better together.</h2><p class="editorial-note">An introduction to the goal below.</p>
<blockquote>{esc(goal["text"])}</blockquote><div class="goal-bottom"><span>Accepted by Rufus Pollock and David Joseph</span><a class="text-link" href="{url(item=goal["id"])}" data-item="{goal["id"]}">Inspect this goal <span aria-hidden="true">↗</span></a></div></section>
<section class="section-block" aria-labelledby="conditions-heading"><div class="section-heading"><div><span class="eyebrow">A direction we can inspect</span><h2 id="conditions-heading">What the goal depends on</h2></div><a class="text-link" href="{url(mode="diagram")}" data-route>See the connections ↗</a></div>
<p class="section-intro">Four conditions are recorded as necessary for the goal. Open one to see the statement, who accepted it, and its connection.</p><div class="condition-grid">{cards}</div></section>
<div class="two-column"><section class="section-block" aria-labelledby="difficulty-heading"><span class="eyebrow">The reason for this demonstration</span><h2 id="difficulty-heading">A difficulty we have named</h2><p class="section-intro">David’s September contribution, accepted for now in October. The connection says “contributes to.”</p>
<div class="mini-thread">{difficulty[:difficulty.find('</a>')+4]}<a class="thread-connection" href="{url(tree="current_reality",item="r-rel-david-demo-confidence-holds-back-testing")}" data-item="r-rel-david-demo-confidence-holds-back-testing">contributes to ↓ <span>Inspect connection</span></a>{difficulty[difficulty.find('</a>')+4:]}</div>
<div class="qualification"><span class="eyebrow">A separately accepted observation</span><p>{esc(nodes["r-e-david-willing-test-coherent-demo"]["text"])}</p><a class="text-link" href="{url(tree="current_reality",item="r-e-david-willing-test-coherent-demo")}" data-item="r-e-david-willing-test-coherent-demo">Read David’s contribution ↗</a></div></section>
<section class="section-block" aria-labelledby="chosen-heading"><span class="eyebrow">A direction to work with</span><h2 id="chosen-heading">Use it while we develop it</h2><p class="section-intro">Rufus accepted this direction. That records a choice, rather than evidence that it worked.</p>{chosen}<div class="quiet-note"><span class="note-dot" aria-hidden="true"></span><p>This page puts the project’s own reasoning in view. Building the demonstration does not resolve the difficulties it records.</p></div></section></div>
<section class="section-block" aria-labelledby="actions-heading"><div class="section-heading"><div><span class="eyebrow">From thinking towards action</span><h2 id="actions-heading">Actions in the record</h2></div><a class="text-link" href="{url(tree="transition")}" data-route>See all six ↗</a></div><p class="section-intro">These are accepted action statements. Their acceptance does not tell us whether they were completed, and their expected effects have no accepted connections in this selection.</p><div class="action-grid">{actions}</div></section>
<section class="section-block perspectives-section" aria-labelledby="perspectives-heading"><span class="eyebrow">One record, different questions</span><h2 id="perspectives-heading">Find your way through the thinking</h2><p class="section-intro">Each view shows the same published selection. Where no connections have been accepted, statements stay separate.</p><div class="perspective-grid">{perspectives}</div></section>'''


def graph(tree, name):
    """Draw actual relationships, in separate components; never manufacture bridges."""
    nodes = {n["id"]: n for n in tree["nodes"]}
    links = tree["links"]
    if not links:
        return '<div class="empty-state"><span class="empty-icon" aria-hidden="true">○ ○ ○</span><h3>Accepted statements. No accepted connections yet.</h3><p>Read the statements below. Drawing arrows between them would add reasoning that has not been accepted.</p></div>' + '<div class="loose-grid">' + ''.join(item_card(n, name) for n in tree["nodes"]) + '</div>'
    adjacent = defaultdict(set)
    for link in links:
        for source in link["from"]:
            adjacent[source].add(link["to"])
            adjacent[link["to"]].add(source)
    components, visited = [], set()
    for ident in nodes:
        if ident in visited or not adjacent[ident]:
            continue
        group, todo = [], [ident]
        while todo:
            current = todo.pop(0)
            if current in visited:
                continue
            visited.add(current)
            group.append(current)
            todo.extend(sorted(adjacent[current] - visited))
        components.append(group)
    pieces = []
    for index, group in enumerate(components):
        relations = [l for l in links if l["to"] in group]
        incoming, outgoing, ranks = defaultdict(int), defaultdict(list), defaultdict(int)
        for link in relations:
            for source in link["from"]:
                incoming[link["to"]] += 1
                outgoing[source].append(link["to"])
        todo = deque(i for i in group if not incoming[i])
        count = 0
        while todo:
            ident = todo.popleft()
            count += 1
            for target in outgoing[ident]:
                ranks[target] = max(ranks[target], ranks[ident] + 1)
                incoming[target] -= 1
                if not incoming[target]:
                    todo.append(target)
        require(count == len(group), "A cycle needs explicit layout support; do not silently alter topology")
        layers = defaultdict(list)
        for ident in nodes:
            if ident in group:
                layers[ranks[ident]].append(ident)
        positions, heights, lines = {}, {}, {}
        for ident in group:
            lines[ident] = textwrap.wrap(nodes[ident].get("label") or nodes[ident]["text"], 33, break_long_words=False)
            heights[ident] = 82 + len(lines[ident]) * 19
        total = max(sum(heights[i] + 30 for i in layer) - 30 for layer in layers.values())
        for rank, layer in layers.items():
            y = 22 + (total - sum(heights[i] + 30 for i in layer) + 30) / 2
            for ident in layer:
                positions[ident] = (22 + rank * 430, y)
                y += heights[ident] + 30
        width, height = 344 + max(layers) * 430, total + 44
        marker = f"arrow-{name}-{index}"
        parts = [f'<svg class="reasoning-svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="graph-title-{name}-{index}"><title id="graph-title-{name}-{index}">{esc(TREES[name][0])}: {len(group)} accepted statements and {len(relations)} accepted connections. The reading view provides the same content.</title><defs><marker id="{marker}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#47705b"/></marker></defs>']
        for link in relations:
            tx, ty = positions[link["to"]]
            ty += heights[link["to"]] / 2
            label = RELATIONS[link["relation"]]
            if len(link["from"]) > 1:
                jx, jy = tx - 50, ty
                for source in link["from"]:
                    sx, sy = positions[source]
                    sx += 300
                    sy += heights[source] / 2
                    parts.append(f'<path class="graph-edge" d="M{sx},{sy} C{sx+55},{sy} {jx-60},{jy} {jx},{jy}"/>')
                parts.append(f'<circle class="and-junction" cx="{jx}" cy="{jy}" r="18"/><text class="and-label" x="{jx}" y="{jy+4}" text-anchor="middle">AND</text>')
                sx, sy = jx + 18, jy
            else:
                sx, sy = positions[link["from"][0]]
                sx += 300
                sy += heights[link["from"][0]] / 2
            parts.append(f'<a href="{url(tree=name,item=link["id"])}" data-item="{link["id"]}" aria-label="Inspect accepted connection: {label}"><path class="graph-edge graph-edge-hit" d="M{sx},{sy} C{sx+50},{sy} {tx-50},{ty} {tx-5},{ty}"/><path class="graph-edge" d="M{sx},{sy} C{sx+50},{sy} {tx-50},{ty} {tx-5},{ty}" marker-end="url(#{marker})"/><text class="graph-relation" x="{(sx+tx)/2}" y="{(sy+ty)/2-10}" text-anchor="middle">{esc(label)}</text></a>')
        for ident in group:
            node = nodes[ident]
            x, y = positions[ident]
            label = f'Accepted for now · {KINDS[node["kind"]]}: {node["text"]}'
            parts.append(f'<a href="{url(tree=name,item=ident)}" data-item="{ident}" aria-label="{esc(label)}"><rect class="graph-node" x="{x}" y="{y}" width="300" height="{heights[ident]}" rx="10"/><text class="graph-standing" x="{x+18}" y="{y+24}">[Accepted]</text><text class="graph-kind" x="{x+18}" y="{y+44}">{esc(KINDS[node["kind"]])}</text><text class="graph-statement" x="{x+18}" y="{y+72}">')
            parts.extend(f'<tspan x="{x+18}" dy="{0 if j==0 else 19}">{esc(line)}</tspan>' for j, line in enumerate(lines[ident]))
            parts.append('</text></a>')
        parts.append('</svg>')
        pieces.append(f'<div class="graph-component"><div class="graph-scroll" tabindex="0" role="region" aria-label="Scrollable diagram {index+1}. Use the arrow keys to scroll.">{"".join(parts)}</div></div>')
    loose = [n for n in tree["nodes"] if n["id"] not in visited]
    if loose:
        pieces.append('<div class="unconnected"><h3>Not yet connected</h3><p>These accepted statements have no accepted connections in this selection.</p><div class="loose-grid">' + ''.join(item_card(n, name, True) for n in loose) + '</div></div>')
    return ''.join(pieces)


def relationship_card(link, nodes, name):
    sources = ''.join(f'<li><a href="{url(tree=name,item=i)}" data-item="{i}">{esc(nodes[i]["text"])}</a></li>' for i in link['from'])
    both = '<span class="joint-label">All of these together (AND)</span>' if len(link['from']) > 1 else ''
    return f'<a class="connection-open" href="{url(tree=name,item=link["id"])}" data-item="{link["id"]}">Inspect accepted connection ↗</a>{both}<ul class="connection-sources">{sources}</ul><span class="relation-word">{esc(RELATIONS[link["relation"]])} ↓</span><p class="connection-target"><a href="{url(tree=name,item=link["to"])}" data-item="{link["to"]}">{esc(nodes[link["to"]]["text"])}</a></p><p class="connection-endorsement">Accepted by {esc(" and ".join(link["accepted_by"]))}</p>'


def reasoning(data):
    tabs = ''.join(f'<a class="tree-tab" href="{url(tree=name)}" data-route data-tree-tab="{name}"><span>0{i}</span>{esc(title)}<span class="tab-count">{len(data["trees"][name]["nodes"])}</span></a>' for i, (name, (title, _, _)) in enumerate(TREES.items(), 1))
    sections = []
    for name, tree in data["trees"].items():
        nodes = {n['id']: n for n in tree['nodes']}
        articles = []
        for node in tree['nodes']:
            incoming = [l for l in tree['links'] if l['to'] == node['id']]
            outgoing = [l for l in tree['links'] if node['id'] in l['from']]
            refs = incoming + outgoing
            connections = ''.join(f'<a class="related-link" href="{url(tree=name,item=l["id"])}" data-item="{l["id"]}">{"Incoming" if l in incoming else "Outgoing"} · {esc(RELATIONS[l["relation"]])} ↗</a>' for l in refs)
            if not refs:
                connections = '<p class="no-connections">No accepted connections in this published selection.</p>'
            authors = ' · '.join(c['name'] for c in node['contributors'])
            articles.append(f'<article class="reading-item" id="item-{node["id"]}" data-node="{node["id"]}"><div class="section-heading"><span class="item-kind">{esc(KINDS[node["kind"]])}</span>{badge()}</div><h4><a href="{url(tree=name,item=node["id"])}" data-item="{node["id"]}">{esc(node["text"])}</a></h4><dl class="provenance"><div><dt>Accepted by</dt><dd>{esc(" and ".join(node["accepted_by"]))}</dd></div><div><dt>Contribution</dt><dd>{esc(authors)}</dd></div><div><dt>Recorded context</dt><dd>{esc(node["acceptance_context"])}</dd></div></dl><div class="related-links">{connections}</div><a class="text-link" href="{url(tree=name,item=node["id"])}" data-item="{node["id"]}">Inspect and prepare a contribution ↗</a></article>')
        link_cards = ''.join(f'<article class="connection-card" id="item-{l["id"]}" data-connection="{l["id"]}">{relationship_card(l,nodes,name)}</article>' for l in tree['links'])
        empty = '<p class="scope-notice">No connections in this view have been accepted. The statements below remain separate.</p>' if not tree['links'] else ''
        link_section = f'<h3 class="connections-heading">The accepted connections</h3><div class="connections-list">{link_cards}</div>' if link_cards else ''
        sections.append(f'<section class="tree-content" data-tree="{name}" aria-labelledby="heading-{name}"><div class="section-heading tree-heading"><div><span class="eyebrow">{esc(TREES[name][2])}</span><h3 id="heading-{name}">{esc(TREES[name][0])}</h3></div><span class="tree-count">{counted(len(tree["nodes"]), "statement")} · {counted(len(tree["links"]), "connection")}</span></div>{empty}<div class="diagram-mode" data-diagram>{graph(tree,name)}</div><div class="reading-mode" data-reading><div class="reading-list">{"".join(articles)}</div>{link_section}</div></section>')
    return f'<div class="section-heading"><div><span class="eyebrow">Read the reasoning</span><h2>One statement at a time.<br>Connections you can inspect.</h2></div></div><p class="section-intro">Only accepted statements and accepted connections are included. The selection preserves who accepted each item and its original wording.</p><div class="reasoning-controls"><label class="search-label" for="reasoning-search">Search this view<input id="reasoning-search" type="search" placeholder="Try “product” or “using”…" autocomplete="off" /></label><div class="mode-switch" aria-label="Display mode"><a href="{url()}" data-mode="reading" data-route>Reading</a><a href="{url(mode="diagram")}" data-mode="diagram" data-route>Diagram</a></div></div><p id="search-status" class="search-status" role="status" aria-live="polite"></p><div class="reasoning-layout"><nav class="tree-navigation" aria-label="Six perspectives">{tabs}</nav><div class="tree-sections">{"".join(sections)}<p id="search-empty" class="empty-state" hidden>No matching statements or connections in this view. Try another word or clear the search.</p></div></div>'


def record(data):
    counts = ''.join(f'<tr><th scope="row">{esc(TREES[name][0])}</th><td>{len(t["nodes"])}</td><td>{len(t["links"])}</td></tr>' for name,t in data['trees'].items())
    return f'''<div class="record-intro"><span class="eyebrow">A record you can inspect</span><h2>What this demonstration can tell you</h2><p class="section-intro">This is one selected snapshot of real collaboration reasoning, prepared on 22 October 2026. It is not a live progress dashboard.</p></div>
<div class="two-column record-columns"><section><h3>Acceptance has a specific meaning</h3><p>Named people are willing to build on a statement or connection for now. A statement accepted by Rufus alone is shown that way; one accepted by David alone is shown that way too. Acceptance does not establish truth or unanimity.</p><h3>Older statements keep their context</h3><p>Many statements were recorded in September 2026. Their original wording is preserved, including references to the product at that time. The detail view shows the recorded acceptance context. Continued acceptance in the source does not establish that a condition is still current.</p><h3>Contribution and endorsement are separate</h3><p>Some imported statements have no identified original contributor. Those entries say so. An AI-originated connection is attributed to the AI, with its human endorsers listed separately.</p></section>
<section class="record-summary"><span class="eyebrow">This published selection</span><div class="record-totals"><span><strong>50</strong> accepted statements</span><span><strong>14</strong> accepted connections</span></div><div class="table-wrap"><table><caption class="sr-only">Accepted content by perspective</caption><thead><tr><th>Perspective</th><th>Statements</th><th>Connections</th></tr></thead><tbody>{counts}</tbody></table></div><a class="text-link" href="./reasoning.json" download>Download this public selection ↓</a><p class="small-note">Release {esc(data["release_id"])}. The download contains the same selection as the page.</p></section></div>
<div class="record-limits"><article><span class="eyebrow">Learning</span><h3>No outcome reports in this selection</h3><p>This accepted-only snapshot contains no selected outcome reports or measurements. An accepted action is not a completed action; a chosen direction is not an observed benefit.</p></article><article><span class="eyebrow">Changes</span><h3>One public snapshot so far</h3><p>This is the first release of this demonstration. Original acceptance context is available on each item. There are no earlier public releases here to compare.</p></article></div>'''


def build_files(registry):
    data = registry["snapshot"]
    validate_projection(data, registry)
    require(registry.get("snapshot_sha256") == digest(data), "Public snapshot fingerprint changed; review and refresh explicitly")
    template = (HERE / "index.html").read_text()
    for token, content in (("<!-- OVERVIEW -->", overview(data)), ("<!-- REASONING -->", reasoning(data)), ("<!-- RECORD -->", record(data))):
        require(template.count(token) == 1, f"Missing/duplicate template marker: {token}")
        template = template.replace(token, content)
    # A non-executable, escaped copy also works inside sandboxed preview frames.
    inline = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    require(template.count('<!-- PUBLIC_DATA -->') == 1, "Missing public-data marker")
    template = template.replace('<!-- PUBLIC_DATA -->', f'<script type="application/json" id="public-record">{inline}</script>')
    return {"index.html": template, "reasoning.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            "styles.css": (HERE / "styles.css").read_text(), "app.js": (HERE / "app.js").read_text()}


def refresh(registry, source):
    helper = ROOT / "skills/reason-commons/scripts/update_views.py"
    spec = importlib.util.spec_from_file_location("rc_views", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    state = module.load(source)
    module.validate(state)
    snapshot = project(state, registry)
    # Approval selects IDs, not whatever might be accepted by a future build.
    registry = deepcopy(registry)
    registry["snapshot"] = snapshot
    registry["snapshot_sha256"] = digest(snapshot)
    return registry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", type=Path, help="Explicit authorized working YAML; refresh only selected public fields")
    parser.add_argument("--check", action="store_true", help="Read-only check of the reviewed snapshot and generated files")
    args = parser.parse_args()
    require(not (args.refresh and args.check), "Refresh and check are separate operations")
    path = HERE / "publication.json"
    registry = read_json(path)
    if args.refresh:
        registry = refresh(registry, args.refresh)
    outputs = build_files(registry)
    if args.check:
        drift = [name for name, value in outputs.items() if not (DEST/name).is_file() or (DEST/name).read_text() != value]
        require(not drift, "Generated demo drift: " + ", ".join(drift))
        print("Accepted-only snapshot and all four generated files: current")
    else:
        if args.refresh:
            path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
        DEST.mkdir(parents=True, exist_ok=True)
        for name, value in outputs.items():
            (DEST / name).write_text(value)
        print(f"Built {DEST.relative_to(ROOT)} from reviewed public snapshot")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print(f"Demo build failed: {error}", file=sys.stderr)
        sys.exit(1)
