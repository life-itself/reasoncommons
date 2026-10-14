#!/usr/bin/env python3
"""Generate compact Mermaid diagrams of a PR's complete conversational YAML diff.

Normally called through check_pr_trees.py --suggest --format markdown.
Standalone: render_pr_diagrams.py --base origin/main path/to/reason-commons.yaml
No files, reasoning standing, snapshots or views are changed.
"""

import argparse
import importlib.util
import json
from pathlib import Path
import textwrap


TREE_ORDER = ("goal", "current_reality", "conflict", "future_reality", "prerequisite", "transition")
MARK = {"accepted": "A", "proposed": "P", "disputed": "D"}
STYLES = {
    "added": "fill:#eef9f0,stroke:#238636,color:#17212e,stroke-width:2px",
    "changed": "fill:#eef5ff,stroke:#0969da,color:#17212e,stroke-width:2px",
    "removed": "fill:#fff1f0,stroke:#cf222e,color:#17212e,stroke-dasharray:5 3",
    "previous": "fill:#f6f8fa,stroke:#6e7781,color:#17212e,stroke-dasharray:3 3",
    "context": "fill:#f6f8fa,stroke:#8c959f,color:#17212e",
}
LEGEND = "ADDED / CHANGED / REMOVED describe this PR; PREVIOUS shows the earlier version; CONTEXT is unchanged neighboring reasoning. [P] proposed · [A] accepted for now · [D] disputed. Arrows show the recorded relation; joint conditions use AND."


def escape(value):
    for raw, code in (("&", "#amp;"), ('"', "#quot;"), ("<", "#lt;"), (">", "#gt;")):
        value = value.replace(raw, code)
    return value.replace("\n", "<br/>")


def trees(documents):
    result = {}
    for state in documents.values():
        for name, tree in (state or {}).get("trees", {}).items():
            current = result.setdefault(name, {"nodes": {}, "links": {}})
            for category in current:
                for item in tree[category]:
                    if item["id"] in current[category]:
                        raise ValueError(f"Duplicate {category} ID: {item['id']}")
                    current[category][item["id"]] = item
    return result


def differences(old, new):
    return {ident for ident in old.keys() | new.keys() if old.get(ident) != new.get(ident)}


def ends(link):
    return set(link["from"] + [link["to"]])


def components(nodes, links):
    adjacency = {ident: set() for ident in nodes}
    for link in links:
        members = ends(link)
        for ident in members:
            adjacency[ident].update(members - {ident})
    remaining = set(nodes)
    groups = []
    while remaining:
        group, pending = set(), [min(remaining)]
        while pending:
            ident = pending.pop()
            if ident not in group:
                group.add(ident)
                pending.extend(adjacency[ident] - group)
        groups.append(group)
        remaining -= group
    return groups


def node_label(name, item, operation):
    standing = item.get("status", "proposed")
    metadata = f"[{MARK[standing]}] {name.replace('_', ' ').upper()} · {item['kind'].replace('_', ' ').upper()}"
    lines = [operation.upper(), metadata]
    lines += textwrap.wrap(item["text"], 38, break_long_words=False, break_on_hyphens=False)
    for objection in item.get("challenges", []) if standing == "disputed" else []:
        lines += textwrap.wrap(f"Objection ({objection['by']}): {objection['text']}", 38, break_long_words=False)
    return escape("\n".join(lines))


def source(name, old, new, selected_nodes, selected_links):
    lines, aliases = ["flowchart LR"], {}
    changed_nodes = differences(old["nodes"], new["nodes"])
    for ident in sorted(selected_nodes):
        before, after = old["nodes"].get(ident), new["nodes"].get(ident)
        if before and after and ident in changed_nodes:
            variants = [("old", before, "previous"), ("new", after, "changed")]
        elif after:
            variants = [("new", after, "added" if before is None else "context")]
        else:
            variants = [("old", before, "removed")]
        for version, item, operation in variants:
            alias = f"n{len(aliases)}"
            aliases[(ident, version)] = alias
            lines.append(f"  %% node {json.dumps(ident)} {version}")
            lines.append(f'  {alias}["{node_label(name, item, operation)}"]')
            lines.append(f"  class {alias} {operation}")
    def endpoint(ident, version):
        return aliases.get((ident, version)) or aliases[(ident, "new" if version == "old" else "old")]
    junction = 0
    for ident in sorted(selected_links):
        before, after = old["links"].get(ident), new["links"].get(ident)
        if before and after and before != after:
            variants = [("old", before, "previous"), ("new", after, "changed")]
        elif before and after:
            variants = [("new", after, "context")]
            if ends(before) & changed_nodes:
                variants.insert(0, ("old", before, "previous"))
        elif after:
            variants = [("new", after, "added")]
        else:
            variants = [("old", before, "removed")]
        for version, item, operation in variants:
            mark = MARK[item.get("status", "proposed")]
            label = escape(f"{operation.upper()} · [{mark}] {item['relation'].replace('_', ' ')}")
            lines.append(f"  %% link {json.dumps(ident)} {version}")
            sources = [endpoint(n, version) for n in sorted(set(item["from"]))]
            target = endpoint(item["to"], version)
            accepted = item.get("status", "proposed") == "accepted"
            if len(sources) > 1:
                joint = f"j{junction}"
                junction += 1
                lines.append(f'  {joint}(("AND"))')
                for start in sources:
                    lines.append(f"  {start} {'-->' if accepted else '-.->'} {joint}")
                start = joint
            else:
                start = sources[0]
            lines.append(f'  {start} -- "{label}" --> {target}' if accepted else f'  {start} -. "{label}" .-> {target}')
    lines.extend(f"  classDef {operation} {style}" for operation, style in STYLES.items())
    return "\n".join(lines)


def fragments(before_documents, after_documents):
    before, after = trees(before_documents), trees(after_documents)
    empty = {"nodes": {}, "links": {}}
    result = []
    for name in sorted(before.keys() | after.keys(), key=lambda n: TREE_ORDER.index(n)):
        old, new = before.get(name, empty), after.get(name, empty)
        changed_nodes = differences(old["nodes"], new["nodes"])
        changed_links = differences(old["links"], new["links"])
        if not changed_nodes and not changed_links:
            continue
        selected_links = set(changed_links)
        selected_nodes = set(changed_nodes)
        # One hop around changed nodes, plus every changed link's old/new endpoints.
        # Context endpoints do not pull in unrelated branches of the full tree.
        for tree in (old, new):
            for ident, link in tree["links"].items():
                if ident in changed_links or ends(link) & changed_nodes:
                    selected_links.add(ident)
                    selected_nodes.update(ends(link))
        all_links = [tree["links"][ident] for tree in (old, new) for ident in selected_links if ident in tree["links"]]
        for group in components(selected_nodes, all_links):
            links = {ident for tree in (old, new) for ident in selected_links
                     if ident in tree["links"] and ends(tree["links"][ident]) <= group}
            result.append({"tree": name, "node_ids": sorted(group), "link_ids": sorted(links),
                           "source": source(name, old, new, group, links)})
    return result


def markdown(before_documents, after_documents):
    diagrams = fragments(before_documents, after_documents)
    lines = ["## Reasoning changes", ""]
    if not diagrams:
        return "\n".join(lines + ["No node/link changes; see the scope and backlog work below.", ""])
    lines += [LEGEND, ""]
    totals = {name: sum(d["tree"] == name for d in diagrams) for name in {d["tree"] for d in diagrams}}
    seen = {}
    for diagram in diagrams:
        name = diagram["tree"]
        seen[name] = seen.get(name, 0) + 1
        title = name.replace("_", " ").title()
        suffix = f" · fragment {seen[name]} of {totals[name]}" if totals[name] > 1 else ""
        lines += [f"**{title}{suffix}**", "", "```mermaid", diagram["source"], "```", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("states", nargs="+")
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("pr_check", Path(__file__).with_name("check_pr_trees.py"))
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    _, before, after = check.load_documents(args.states, args.base, None)
    for state in after.values():
        check.views.validate(state)
    print(markdown(before, after))


if __name__ == "__main__":
    main()
