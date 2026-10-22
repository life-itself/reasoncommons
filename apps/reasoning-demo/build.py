#!/usr/bin/env python3
"""Build the read-only site of commons from reviewed public projections.

Ordinary builds and CI use the snapshot pinned in each publication registry. Refreshing
our commons requires an explicit, authorized working-state path and the existing allowlist;
the fictional example refreshes from its own public working file. No working-state path,
approval receipt, private note or unselected reasoning is published.
"""
import argparse
from copy import deepcopy
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEST = ROOT / "website/demos/reason-commons-in-use"
sys.path.insert(0, str(HERE))
import diagrams  # noqa: E402
import pages  # noqa: E402

TREE_KINDS = {
    "goal": {"goal", "critical_success_factor", "necessary_condition"},
    "current_reality": {"undesirable_effect", "cause"},
    "conflict": {"objective", "need", "prerequisite"},
    "future_reality": {"injection", "existing_condition", "predicted_effect", "desirable_effect", "undesirable_effect"},
    "prerequisite": {"objective", "obstacle", "intermediate_objective"},
    "transition": {"existing_condition", "need", "action", "expected_effect"},
}
KINDS = set().union(*TREE_KINDS.values()) | {"observation"}
RELATIONS = {"necessary_for", "contributes_to"}
NODE_FIELDS = {"id", "kind", "text", "label", "status", "accepted_by", "contributors", "acceptance_context"}
LINK_FIELDS = {"id", "from", "to", "relation", "status", "accepted_by", "contributors", "acceptance_context"}
TRACES = ("addresses", "derived_from", "implements")
NODE_FIELDS_V2 = NODE_FIELDS | {"assumptions", "challenges", *TRACES}
LINK_FIELDS_V2 = LINK_FIELDS | {"assumptions", "challenges"}
STANDINGS = {"proposed", "accepted", "disputed"}
VERDICTS = {"observed", "not_observed", "unclear", "not_assessed", "unavailable"}
READINESS = {"experienced", "not_yet", "cannot_assess"}
CHANGE_TYPES = {"added", "revised", "disputed", "accepted", "removed", "report"}
UNKNOWN = {"name": "Original contributor not identified", "role": "unknown"}
ASSISTANT = {"name": "AI assistant", "role": "assistant"}


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


def skill_helpers():
    helper = ROOT / "skills/reason-commons/scripts/update_views.py"
    spec = importlib.util.spec_from_file_location("rc_views", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contributors(item, people):
    result = []
    for contribution in item["contributions"]:
        who = contribution["by"]
        if contribution["attribution"] == "driver_default":
            entry = dict(UNKNOWN)
        elif who == "assistant":
            entry = dict(ASSISTANT)
        else:
            require(who in people, f"Unselected contributor: {who}")
            entry = {"name": people[who], "role": "human"}
        if entry not in result:
            result.append(entry)
    return result


# ---------------------------------------------------------------- projection 1: our accepted-only selection

def project(state, registry):
    """Only explicit IDs and explicit fields cross the publication boundary."""
    require(state.get("schema_version") == 1, "Unsupported working-state version")
    people = registry["people"]
    result = {"projection_version": 1, **deepcopy(registry["release"]), "trees": {}}
    for name, selection in registry["selection"].items():
        require(name in TREE_KINDS and name in state["trees"], f"Unknown tree: {name}")
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


def validate_attribution(item, approved, ident):
    require(item.get("contributors"), f"Missing attribution: {ident}")
    for c in item["contributors"]:
        require(set(c) == {"name", "role"}, f"Invalid attribution fields: {ident}")
        require(c in (UNKNOWN, ASSISTANT) or (c["role"] == "human" and c["name"] in approved), f"Unselected contributor: {ident}")


def validate_projection(data, registry):
    require(data.get("projection_version") == 1, "Unsupported projection version")
    require(set(data) == {"projection_version", "release_id", "snapshot_date", "title", "trees"}, "Unexpected public field")
    require(set(data["trees"]) == set(registry["selection"]), "Selection/tree mismatch")
    approved = set(registry["people"].values())
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
                require(item.get("accepted_by") and set(item["accepted_by"]) <= approved, f"Invalid endorsers: {ident}")
                validate_attribution(item, approved, ident)
                require(isinstance(item.get("acceptance_context"), str), f"Missing recorded context: {ident}")
                if key == "nodes":
                    require(item.get("kind") in KINDS and isinstance(item.get("text"), str) and item["text"].strip(), f"Invalid statement: {ident}")
                else:
                    require(item.get("relation") in RELATIONS, f"Unsupported relationship: {ident}")
                    require(isinstance(item.get("from"), list) and item["from"] and len(set(item["from"])) == len(item["from"]), f"Invalid sources: {ident}")
                    require(set(item["from"] + [item["to"]]) <= ids, f"Missing accepted endpoint: {ident}")


# ---------------------------------------------------------------- projection 2: the fictional example, every standing

def person(who, people):
    if who == "assistant":
        return ASSISTANT["name"]
    require(who in people, f"Unselected participant: {who}")
    return people[who]


def project_v2(state, registry):
    """A selection that keeps standings, qualifications, open work, outcome reports and history."""
    require(state.get("schema_version") == 1, "Unsupported working-state version")
    people = registry["people"]
    public_nodes = {i for selection in registry["selection"].values() for i in selection["nodes"]}
    result = {"projection_version": 2, "is_example": registry["is_example"], **deepcopy(registry["release"]),
              "people": [{"name": people[k], "role": registry["roles"][k]} for k in people],
              "trees": {}, "feedback": [], "history": deepcopy(registry["history"])}
    for name, selection in registry["selection"].items():
        require(name in TREE_KINDS and name in state["trees"], f"Unknown tree: {name}")
        source = state["trees"][name]
        output = {"nodes": [], "links": [], "backlog": []}
        for key in ("nodes", "links"):
            indexed = {item["id"]: item for item in source[key]}
            for ident in selection[key]:
                require(ident in indexed, f"Selected item is missing: {ident}")
                item = indexed[ident]
                public = {"id": ident, "status": item.get("status", "proposed"),
                          "accepted_by": [person(p, people) for p in item.get("accepted_by", [])],
                          "contributors": contributors(item, people)}
                if item.get("acceptance_source"):
                    public["acceptance_context"] = item["acceptance_source"]
                if key == "nodes":
                    public.update(kind=item["kind"], text=item["text"])
                    if item.get("label"):
                        public["label"] = item["label"]
                    for trace in TRACES:
                        refs = [r for r in item.get(trace, []) if r in public_nodes]
                        if refs:
                            public[trace] = refs
                else:
                    public.update({field: deepcopy(item[field]) for field in ("from", "to", "relation")})
                for note in ("assumptions", "challenges"):
                    if item.get(note):
                        public[note] = [{"text": n["text"], "by": person(n["by"], people)} for n in item[note]]
                output[key].append(public)
        chosen = set(selection["nodes"]) | set(selection["links"])
        output["backlog"] = [{k: task[k] for k in ("ref", "work", "label", "note") if k in task}
                             for task in source.get("backlog", []) if task["ref"] in chosen]
        result["trees"][name] = output
    for request in state.get("feedback_requests", []):
        if request["id"] not in registry["feedback"]:
            continue
        public = {key: deepcopy(request[key]) for key in ("id", "revision", "recorded_at", "about", "benefits", "reservations") if key in request}
        public.update(created_by=person(request["created_by"], people), feedback_from=[person(p, people) for p in request["feedback_from"]])
        if request.get("ready_when"):
            public["ready_when"] = request["ready_when"]
        public["reports"] = [{"id": r["id"], "by": person(r["by"], people), "recorded_at": r["recorded_at"], "readiness": r["readiness"],
                              "text": r["text"], "evidence_type": r["evidence_type"], "outcomes": deepcopy(r["outcomes"])}
                             for r in request["reports"]]
        result["feedback"].append(public)
    validate_v2(result, registry)
    return result


def validate_v2(data, registry):
    require(data.get("projection_version") == 2, "Unsupported projection version")
    require(set(data) == {"projection_version", "is_example", "release_id", "snapshot_date", "title", "people", "trees", "feedback", "history"}, "Unexpected public field")
    require(data["is_example"] is registry["is_example"] is True, "Projection 2 is reserved for the labelled fictional example")
    require(set(data["trees"]) == set(registry["selection"]), "Selection/tree mismatch")
    approved = set(registry["people"].values())
    names = approved | {ASSISTANT["name"]}
    require([p["name"] for p in data["people"]] == list(registry["people"].values()), "People mismatch")
    seen, nodes_by_id = set(), {}
    for name, tree in data["trees"].items():
        require(set(tree) == {"nodes", "links", "backlog"}, f"Unexpected tree fields: {name}")
        for key, allowed in (("nodes", NODE_FIELDS_V2), ("links", LINK_FIELDS_V2)):
            require([i["id"] for i in tree[key]] == registry["selection"][name][key], f"Selection mismatch: {name}.{key}")
            for item in tree[key]:
                ident = item["id"]
                require(ident not in seen and re.fullmatch(r"[a-z0-9-]+", ident), f"Invalid/duplicate ID: {ident}")
                seen.add(ident)
                require(set(item) <= allowed, f"Unreviewed public fields: {ident}")
                require(item.get("status") in STANDINGS, f"Invalid standing: {ident}")
                require(set(item.get("accepted_by", [])) <= approved, f"Invalid endorsers: {ident}")
                require(item["status"] != "accepted" or item["accepted_by"], f"Accepted item needs named endorsers: {ident}")
                require(item["status"] != "proposed" or not item["accepted_by"], f"Proposed item cannot list endorsers: {ident}")
                validate_attribution(item, approved, ident)
                for note in ("assumptions", "challenges"):
                    for entry in item.get(note, []):
                        require(set(entry) == {"text", "by"} and entry["by"] in names and entry["text"].strip(), f"Invalid {note}: {ident}")
                if key == "nodes":
                    require(item.get("kind") in TREE_KINDS[name] | {"observation"} and item.get("text", "").strip(), f"Invalid statement: {ident}")
                    nodes_by_id[ident] = item
        local = {n["id"]: n for n in tree["nodes"]}
        for link in tree["links"]:
            require(re.fullmatch(r"[a-z_]+", link.get("relation", "")), f"Unsupported relationship: {link['id']}")
            require(link["from"] and len(set(link["from"])) == len(link["from"]) and set(link["from"] + [link["to"]]) <= set(local), f"Missing endpoint: {link['id']}")
            if link["status"] == "accepted":
                require(all(local[i]["status"] == "accepted" for i in link["from"] + [link["to"]]), f"Accepted link needs accepted endpoints: {link['id']}")
        ids = set(local) | {l["id"] for l in tree["links"]}
        for task in tree["backlog"]:
            require(task["ref"] in ids and set(task) <= {"ref", "work", "label", "note"}, f"Invalid open work in {name}")
    for node in nodes_by_id.values():
        for trace in TRACES:
            require(set(node.get(trace, [])) <= set(nodes_by_id), f"Unpublished trace: {node['id']}")
    reports = set()
    for request in data["feedback"]:
        outcomes = [o["ref"] for o in request["benefits"] + request["reservations"]]
        for snap in [request["about"]] + request["benefits"] + request["reservations"]:
            require(snap["ref"] in nodes_by_id and snap.get("standing") in STANDINGS, f"Unpublished feedback statement: {snap['ref']}")
        require(set(request["feedback_from"]) <= approved and request["created_by"] in names, "Unselected feedback people")
        for report in request["reports"]:
            require(report["by"] in request["feedback_from"] and report["readiness"] in READINESS, f"Invalid report: {report['id']}")
            require(report["evidence_type"] == "self_report", f"Reports are attributed self-reports: {report['id']}")
            for answer in report["outcomes"]:
                require(answer["ref"] in outcomes and answer["verdict"] in VERDICTS, f"Invalid outcome: {report['id']}")
            reports.add(report["id"])
    for release in data["history"]:
        require(set(release) == {"release_id", "date", "title", "summary", "changes"}, "Unexpected history fields")
        for change in release["changes"]:
            require(change["type"] in CHANGE_TYPES and set(change) <= {"type", "refs", "note", "before"}, "Unexpected change entry")
            require(set(change["refs"]) <= seen | reports, f"History refers to unpublished material in {release['release_id']}")
    require(data["history"] and data["history"][-1]["release_id"] == data["release_id"], "The latest history entry must be this release")


# ---------------------------------------------------------------- site

def load_site():
    site = read_json(HERE / "site.json")
    commons = []
    for entry in site["commons"]:
        registry = read_json(HERE / entry["registry"])
        data = registry["snapshot"]
        if data.get("projection_version") == 1:
            require(entry["kind"] == "real", "Our accepted-only projection is the real commons")
            validate_projection(data, registry)
        else:
            require(entry["kind"] == "example", "Only the labelled example uses projection 2")
            validate_v2(data, registry)
        require(registry.get("snapshot_sha256") == digest(data), f"Public snapshot fingerprint changed for {entry['slug']}; review and refresh explicitly")
        commons.append({"entry": entry, "registry": registry, "data": data})
    return site, commons


def normalize(item):
    """One reading of either projection for the pages; nothing is added that the projection lacks."""
    entry, data = item["entry"], item["data"]
    trees = {}
    for name in pages.TREE_ORDER:
        if name not in data["trees"]:
            continue
        source = data["trees"][name]
        nodes = [{"assumptions": [], "challenges": [], **n} for n in source["nodes"]]
        links = [{"assumptions": [], "challenges": [], **l} for l in source["links"]]
        trees[name] = {"name": name, "nodes": nodes, "links": links, "backlog": source.get("backlog", [])}
    if data["projection_version"] == 1:
        people = [{"name": n, "role": ""} for n in item["registry"]["people"].values()]
        history = [{"release_id": data["release_id"], "date": data["snapshot_date"], "title": "First publication",
                    "summary": "Accepted statements and connections, selected from the working record with their original wording, named endorsers and recorded context.",
                    "changes": [{"type": "added", "refs": [i["id"] for t in trees.values() for i in t["nodes"] + t["links"]]}]}]
        feedback = []
    else:
        people, history, feedback = data["people"], data["history"], data["feedback"]
    return {**entry, "is_example": entry["kind"] == "example", "release_id": data["release_id"], "date": data["snapshot_date"],
            "title": data["title"], "people": people, "trees": trees, "feedback": feedback, "history": history,
            "json": json.dumps(data, ensure_ascii=False, indent=2) + "\n"}


def build_files(site, commons):
    normalized = [normalize(c) for c in commons]
    outputs = pages.render(site, normalized)
    real = next(c for c in commons if c["entry"]["kind"] == "real")
    outputs["reasoning.json"] = json.dumps(real["data"], ensure_ascii=False, indent=2) + "\n"  # The earlier download path stays.
    for c in normalized:
        outputs[f'{c["slug"]}/reasoning.json'] = c["json"]
    outputs["styles.css"] = (HERE / "styles.css").read_text()
    outputs["app.js"] = (HERE / "app.js").read_text()
    for font in sorted((HERE / "fonts").iterdir()):
        outputs[f"fonts/{font.name}"] = font.read_bytes()
    return outputs


def refresh(registry, source):
    module = skill_helpers()
    state = module.load(source)
    module.validate(state)
    snapshot = project(state, registry)
    # Approval selects IDs, not whatever might be accepted by a future build.
    registry = deepcopy(registry)
    registry["snapshot"] = snapshot
    registry["snapshot_sha256"] = digest(snapshot)
    return registry


def refresh_example(entry, registry):
    module = skill_helpers()
    state = module.load(HERE / entry["source"])
    module.validate(state)
    registry = deepcopy(registry)
    registry["snapshot"] = project_v2(state, registry)
    registry["snapshot_sha256"] = digest(registry["snapshot"])
    return registry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", type=Path, help="Explicit authorized working YAML; refresh only our selected public fields")
    parser.add_argument("--refresh-example", action="store_true", help="Re-project the fictional example from its public working file")
    parser.add_argument("--check", action="store_true", help="Read-only check of the reviewed snapshots and generated files")
    args = parser.parse_args()
    require(not ((args.refresh or args.refresh_example) and args.check), "Refresh and check are separate operations")
    site = read_json(HERE / "site.json")
    for entry in site["commons"]:
        path = HERE / entry["registry"]
        if entry["kind"] == "real" and args.refresh:
            path.write_text(json.dumps(refresh(read_json(path), args.refresh), ensure_ascii=False, indent=2) + "\n")
        if entry["kind"] == "example" and args.refresh_example:
            path.write_text(json.dumps(refresh_example(entry, read_json(path)), ensure_ascii=False, indent=2) + "\n")
    site, commons = load_site()
    if args.check:
        for c in commons:  # The example must still be exactly what its working file projects to.
            if c["entry"]["kind"] == "example":
                try:
                    fresh = refresh_example(c["entry"], c["registry"])["snapshot"]
                except ModuleNotFoundError:
                    print("PyYAML unavailable: example working file not re-projected", file=sys.stderr)
                else:
                    require(fresh == c["data"], "Example snapshot no longer matches its working file; run --refresh-example")
    outputs = build_files(site, commons)
    if args.check:
        drift = [name for name, value in outputs.items()
                 if not (DEST / name).is_file() or (DEST / name).read_bytes() != (value if isinstance(value, bytes) else value.encode())]
        extra = sorted(str(p.relative_to(DEST)) for p in DEST.rglob("*") if p.is_file() and str(p.relative_to(DEST)) not in outputs)
        require(not drift, "Generated site drift: " + ", ".join(drift))
        require(not extra, "Unexpected files in the published folder: " + ", ".join(extra))
        print(f"Reviewed snapshots and all {len(outputs)} generated files: current")
    else:
        for name, value in outputs.items():
            target = DEST / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(value, bytes):
                target.write_bytes(value)
            else:
                target.write_text(value)
        print(f"Built {DEST.relative_to(ROOT)}: {len(outputs)} files from reviewed public snapshots")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print(f"Demo build failed: {error}", file=sys.stderr)
        sys.exit(1)
