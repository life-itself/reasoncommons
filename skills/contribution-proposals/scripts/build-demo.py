#!/usr/bin/env python3
"""Build the Demo C review page from an LTP model and a proposals file.

Reads a target `ltp-model.yaml` and a `proposals.yaml` written against it,
validates every reference, and renders one self-contained HTML page with the
model and the proposals embedded. Nothing here writes to the model: the whole
point of the artifact is that the tree on disk is untouched until a person
decides otherwise.

    python3 build-demo.py --model ltp/ltp-model.yaml \
        --proposals talk/2r-research-group/demo-c/proposals.yaml \
        --out talk/2r-research-group/demo-c/index.html

Add --check to validate and print the plan without writing anything.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import pathlib
import sys

try:
    import yaml
except ImportError:  # pragma: no cover - environment problem, not a data problem
    sys.exit("PyYAML is required: pip3 install pyyaml")

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "templates" / "demo.html"

# Which placement fields each operation needs. Everything else is optional.
REQUIRED_PLACEMENT = {
    "add_entity": ("view", "connects_to", "relation"),
    "support_entity": ("view", "connects_to"),
    "challenge_entity": ("view", "connects_to"),
    "challenge_link": ("view", "link"),
    "add_link": ("view", "from", "to", "relation"),
    "unplaced": (),
}


class Problem(Exception):
    pass


def load_yaml(path: pathlib.Path):
    if not path.exists():
        raise Problem(f"{path} does not exist")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def compact_model(model: dict) -> dict:
    """Keep only what the page draws. Evidence and assumptions stay behind."""
    entities = {}
    for ent in model.get("entities") or []:
        entities[ent["id"]] = {
            "id": ent["id"],
            "type": ent.get("type", "unknown"),
            "statement": ent.get("statement", ""),
            "status": ent.get("status", ""),
        }
    links = {}
    for link in model.get("links") or []:
        links[link["id"]] = {
            "id": link["id"],
            "from": link["from"],
            "to": link["to"],
            "relation": link.get("relation", ""),
        }
    views = {}
    for key, view in (model.get("views") or {}).items():
        views[key] = {
            "key": key,
            "title": view.get("title", key),
            "purpose": view.get("purpose", ""),
            "entities": list(view.get("entities") or []),
            "links": list(view.get("links") or []),
        }
    return {
        "project": (model.get("project") or {}).get("name", "LTP model"),
        "entities": entities,
        "links": links,
        "views": views,
    }


def validate(bundle: dict, proposals: list, strict: bool) -> list:
    """Return the list of problems found. Raises nothing itself."""
    problems = []
    seen_ids = set()
    entities, links, views = bundle["entities"], bundle["links"], bundle["views"]

    # A proposal may hang off a claim an earlier proposal introduces, so that a
    # second contribution can build on one the room has just accepted. Only
    # backwards: the tree has to make sense read in order.
    added_by = {}

    for index, item in enumerate(proposals, start=1):
        pid = item.get("id") or f"#{index}"

        def bad(msg):
            problems.append(f"{pid}: {msg}")

        if not item.get("id"):
            bad("no id")
        elif item["id"] in seen_ids:
            bad("duplicate id")
        else:
            seen_ids.add(item["id"])

        source = item.get("source") or {}
        if not (source.get("text") or "").strip():
            bad("source.text is empty — the participant's own words are the one thing this cannot invent")
        if not (source.get("contributor") or "").strip():
            bad("source.contributor is empty")
        if not ((item.get("interpretation") or {}).get("statement") or "").strip():
            bad("interpretation.statement is empty")

        prop = item.get("proposal") or {}
        op = prop.get("operation")
        if op not in REQUIRED_PLACEMENT:
            bad(f"unknown operation {op!r} — one of {', '.join(REQUIRED_PLACEMENT)}")
            continue
        if not (prop.get("rationale") or "").strip():
            bad("proposal.rationale is empty")
        if prop.get("confidence") not in ("high", "medium", "low"):
            bad(f"confidence must be high, medium or low (got {prop.get('confidence')!r})")

        placement = prop.get("placement") or {}
        for field in REQUIRED_PLACEMENT[op]:
            if not placement.get(field):
                bad(f"{op} needs placement.{field}")

        view_key = placement.get("view")
        if view_key and view_key not in views:
            bad(f"view {view_key!r} is not in the model (have: {', '.join(sorted(views))})")
            view_key = None

        for field in ("connects_to", "from", "to"):
            ref = placement.get(field)
            if not ref:
                continue
            if field == "connects_to" and ref in added_by:
                earlier_view = added_by[ref]
                if view_key and earlier_view != view_key:
                    bad(f"placement.connects_to {ref!r} is a claim proposed in view "
                        f"{earlier_view!r}, not {view_key!r}")
                continue
            if ref not in entities:
                hint = ""
                if ref in seen_ids:
                    hint = " (that proposal does not add a claim to hang this from)"
                elif ref.startswith("PROP-"):
                    hint = " (a proposal id may only be used once that proposal has appeared, and only if it adds a claim)"
                bad(f"placement.{field} {ref!r} is not an entity in the model" + hint)
            elif view_key and ref not in views[view_key]["entities"]:
                msg = f"placement.{field} {ref!r} is not in view {view_key!r}, so it will not be on screen"
                if strict:
                    bad(msg)
                else:
                    problems.append(f"{pid}: WARNING {msg}")

        link_ref = placement.get("link")
        if link_ref:
            if link_ref not in links:
                bad(f"placement.link {link_ref!r} is not a link in the model")
            elif view_key and link_ref not in views[view_key]["links"]:
                bad(f"placement.link {link_ref!r} is not in view {view_key!r}")

        if op == "add_entity":
            entity = prop.get("entity") or {}
            if not (entity.get("statement") or "").strip():
                bad("add_entity needs proposal.entity.statement")
            if not entity.get("type"):
                bad("add_entity needs proposal.entity.type")
            if item.get("id"):
                added_by[item["id"]] = view_key
        elif prop.get("entity"):
            bad(f"{op} should not carry proposal.entity")

        for alt in prop.get("alternatives") or []:
            if alt.get("target") and alt["target"] not in entities:
                bad(f"alternative target {alt['target']!r} is not an entity in the model")

        review = item.get("review") or {}
        if review.get("status", "pending") != "pending":
            bad("review.status must be pending — accept and reject happen in the room, not on disk")

    return problems


def build(args) -> int:
    model_path = pathlib.Path(args.model)
    proposals_path = pathlib.Path(args.proposals)

    model_raw = model_path.read_bytes()
    model = yaml.safe_load(model_raw.decode("utf-8"))
    doc = load_yaml(proposals_path)

    if not isinstance(doc, dict) or "proposals" not in doc:
        raise Problem(f"{proposals_path} has no top-level `proposals:` list")

    proposals = doc["proposals"] or []
    bundle = compact_model(model)

    problems = validate(bundle, proposals, strict=args.strict)
    hard = [p for p in problems if "WARNING" not in p]
    for p in problems:
        print(("  ! " if "WARNING" not in p else "  ~ ") + p, file=sys.stderr)
    if hard:
        raise Problem(f"{len(hard)} problem(s) in {proposals_path}")

    meta = dict(doc.get("meta") or {})
    meta.setdefault("title", "Contribution proposals")
    meta.setdefault("attribution", "numbered")
    meta["model_source"] = meta.get("model_source") or str(model_path)
    meta["model_sha256"] = hashlib.sha256(model_raw).hexdigest()[:12]
    meta["generated"] = _dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")

    # Only ship the views the proposals actually point at, plus goal-tree as the
    # opening establishing shot. A projector does not need the other four.
    used = {
        (p.get("proposal") or {}).get("placement", {}).get("view")
        for p in proposals
    }
    used.discard(None)
    if not used:
        used = {"goal-tree"}
    bundle["views"] = {k: v for k, v in bundle["views"].items() if k in used}

    counts = {}
    for p in proposals:
        op = (p.get("proposal") or {}).get("operation", "?")
        counts[op] = counts.get(op, 0) + 1
    print(f"  {len(proposals)} proposals across {len(used)} view(s): "
          + ", ".join(f"{n}× {op}" for op, n in sorted(counts.items())))

    if args.check:
        print("  check only — nothing written")
        return 0

    payload = json.dumps(
        {"meta": meta, "model": bundle, "proposals": proposals},
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,  # YAML turns a bare 2026-09-04 into a date object
    )
    # </script> inside a data string would end the block early.
    payload = payload.replace("</", "<\\/")

    template = TEMPLATE.read_text(encoding="utf-8")
    if "/*__DATA__*/null" not in template:
        raise Problem(f"{TEMPLATE} has no /*__DATA__*/null placeholder")
    html = template.replace("/*__DATA__*/null", payload)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out} ({len(html) // 1024} KB, self-contained)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="ltp/ltp-model.yaml")
    ap.add_argument("--proposals", default="talk/2r-research-group/demo-c/proposals.yaml")
    ap.add_argument("--out", default="talk/2r-research-group/demo-c/index.html")
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--strict", action="store_true",
                    help="treat 'target not in view' as an error rather than a warning")
    args = ap.parse_args()
    try:
        return build(args)
    except Problem as exc:
        print(f"build-demo: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
