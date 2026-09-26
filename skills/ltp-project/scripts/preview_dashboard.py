#!/usr/bin/env python3
"""Preview an interchange .ltp.yaml file in the Reason Commons dashboard."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Missing PyYAML. Install it with: python3 -m pip install pyyaml") from exc


REPO_ROOT = Path(__file__).resolve().parents[3]
DASHBOARD = REPO_ROOT / "dashboard"
TREE_IDS = {
    "goal": "goal-tree",
    "current_reality": "current-reality",
    "conflict": "evaporating-cloud",
    "future_reality": "future-reality",
    "prerequisite": "prerequisite-tree",
    "transition": "transition-tree",
}
ROLE_TYPES = {
    "cloud_objective": "common_objective",
    "cloud_requirement": "need",
    "cloud_prerequisite": "option",
    "intermediate_cause": "root_cause",
    "transition_existing_reality": "observation",
    "transition_need": "need",
    "transition_action": "action",
    "transition_expected_effect": "expected_effect",
}
RELATIONS = {
    "overcomes": "overcome_by",
    "requires": "requires",
    "satisfies": "satisfies",
    "precedes": "precedes",
    "invalidates_assumption": "invalidates",
    "implements": "implements",
    "supersedes": "supersedes",
    "supports": "supports",
    "challenges": "challenges",
    "refines": "refines",
    "enables": "enables",
    "necessary_for": "necessary_for",
    "causes": "causes",
    "contributes_to": "contributes_to",
    "conflicts_with": "conflicts_with",
    "produces": "produces",
}


def convert(document: dict) -> tuple[str, dict]:
    ltp = document.get("ltp")
    if not isinstance(ltp, dict):
        raise ValueError("Expected a top-level 'ltp' mapping in the .ltp.yaml file.")

    entities = {item["id"]: item for item in ltp.get("entities", [])}
    designations = ltp.get("designations", [])
    designation_roles: dict[str, str] = {}
    for designation in designations:
        designation_roles.setdefault(designation["entity_id"], designation["role"])

    assumptions = {item["id"]: item for item in ltp.get("assumptions", [])}
    evidence = {item["id"]: item for item in ltp.get("evidence", [])}
    converted_entities = []
    for entity in entities.values():
        item = {
            "id": entity["id"],
            "type": ROLE_TYPES.get(designation_roles.get(entity["id"], ""), designation_roles.get(entity["id"], "observation")),
            "statement": entity["statement"],
            "status": entity.get("status", "provisional"),
            "confidence": entity.get("confidence", "low"),
        }
        for key in ("confidence", "reasoning"):
            if key in entity:
                item[key] = entity[key]
        if "evidence_ids" in entity:
            item["evidence"] = entity["evidence_ids"]
        if "assumption_ids" in entity:
            item["assumptions"] = [
                f'{assumptions[aid]["id"]} — {assumptions[aid]["statement"]}'
                for aid in entity["assumption_ids"] if aid in assumptions
            ]
        converted_entities.append(item)

    converted_links = []
    relationship_link_ids: dict[str, list[str]] = {}
    relation_assumption = {
        item["relationship_id"]: item["id"]
        for item in assumptions.values() if item.get("relationship_id")
    }
    for relation in ltp.get("relationships", []):
        sources = relation.get("from_entity_ids", [])
        target = relation.get("to_entity_id")
        if not target or not sources:
            continue
        for index, source in enumerate(sources):
            link_id = relation["id"] if len(sources) == 1 else f'{relation["id"]}-{index + 1}'
            link = {
                "id": link_id,
                "from": source,
                "to": target,
                "relation": RELATIONS.get(relation["kind"], relation["kind"]),
            }
            if "confidence" in relation:
                link["confidence"] = relation["confidence"]
            if relation["id"] in relation_assumption:
                link["assumption"] = relation_assumption[relation["id"]]
            converted_links.append(link)
            relationship_link_ids.setdefault(relation["id"], []).append(link_id)

    evidence_rows = []
    for item in evidence.values():
        row = {key: item[key] for key in ("id", "source", "locator", "observation", "interpretation") if key in item}
        if "locator" in row:
            row["lines"] = row.pop("locator")
        evidence_rows.append(row)

    views: dict[str, dict] = {}
    for tree, view_id in TREE_IDS.items():
        view_entities = [item["id"] for item in entities.values() if item.get("tree") == tree]
        view_links = [
            link_id
            for item in ltp.get("relationships", []) if item.get("tree") == tree
            for link_id in relationship_link_ids.get(item["id"], [])
        ]
        if view_entities:
            views[view_id] = {
                "title": view_id.replace("-", " ").title(),
                "entities": view_entities,
                "links": view_links,
            }

    project_name = ltp.get("title", ltp.get("project_id", "LTP project"))
    model = {
        "project": {"name": project_name, "analysis_mode": "preview"},
        "analysis": {},
        "entities": converted_entities,
        "links": converted_links,
        "evidence": evidence_rows,
        "assumptions": [
            {key: item[key] for key in ("id", "statement", "status") if key in item}
            for item in assumptions.values()
        ],
        "views": views,
    }
    slug = "ltp-preview"
    return slug, model


def main() -> None:
    parser = argparse.ArgumentParser(description="Open an .ltp.yaml project in the local Reason Commons dashboard.")
    parser.add_argument("project", nargs="?", type=Path, help="Path to a Reason Commons .ltp.yaml file (defaults to the latest non-fixture project in this repository)")
    parser.add_argument("--port", type=int, default=8765, help="Local server port (default: 8765)")
    parser.add_argument("--no-open", action="store_true", help="Print the URL without opening a browser")
    parser.add_argument("--export-html", nargs="?", const="", metavar="PATH", help="Write a standalone HTML preview instead of starting a server; defaults beside the YAML")
    args = parser.parse_args()

    if args.project is None:
        candidates = [
            path for path in REPO_ROOT.rglob("*.ltp.yaml")
            if "skills/ltp-project/references" not in path.as_posix()
            and ".git" not in path.parts
        ]
        if not candidates:
            parser.error("no project .ltp.yaml files found; pass the path explicitly")
        args.project = max(candidates, key=lambda path: path.stat().st_mtime)
        print(f"Using latest project: {args.project.relative_to(REPO_ROOT)}")
    project_file = args.project.expanduser().resolve()
    if not project_file.is_file():
        parser.error(f"file not found: {project_file}")
    try:
        document = yaml.safe_load(project_file.read_text(encoding="utf-8"))
        slug, model = convert(document or {})
    except (OSError, yaml.YAMLError, KeyError, TypeError, ValueError) as exc:
        parser.error(f"could not read project: {exc}")

    if not (DASHBOARD / "index.html").is_file():
        parser.error(f"dashboard index not found at {DASHBOARD / 'index.html'}")

    temporary = tempfile.TemporaryDirectory(prefix="ltp-dashboard-preview-")
    root = Path(temporary.name)
    project_dir = root / "projects" / slug
    project_dir.mkdir(parents=True)
    (project_dir / "model.yaml").write_text(yaml.safe_dump(model, allow_unicode=True, sort_keys=False), encoding="utf-8")
    manifest = {"projects": [{"slug": slug, "name": model["project"]["name"], "blurb": f"Local preview of {project_file.name}", "model": f"projects/{slug}/model.yaml"}], "alignments": []}
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2)
    (root / "projects" / "manifest.json").write_text(manifest_text, encoding="utf-8")

    # The published dashboard embeds its static fixture data in the bundle and
    # prefers that map over fetch(). Replace it with our generated preview data.
    embedded_data = {
        "projects/manifest.json": manifest_text,
        f"projects/{slug}/model.yaml": yaml.safe_dump(model, allow_unicode=True, sort_keys=False),
    }
    js_object = json.dumps(embedded_data, ensure_ascii=True)
    dashboard_html = (DASHBOARD / "index.html").read_text(encoding="utf-8")
    dashboard_html, replacements = re.subn(
        r"const ME=\{.*?\};async function Yi",
        lambda _match: f"const ME={js_object};async function Yi",
        dashboard_html,
        count=1,
        flags=re.DOTALL,
    )
    if replacements != 1:
        temporary.cleanup()
        parser.error("could not locate the dashboard's embedded demo data")
    (root / "index.html").write_text(dashboard_html, encoding="utf-8")

    if args.export_html is not None:
        default_name = project_file.name.removesuffix(".ltp.yaml") + ".dashboard-preview.html"
        output = Path(args.export_html).expanduser().resolve() if args.export_html else project_file.with_name(default_name)
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / "index.html", output)
        temporary.cleanup()
        url = output.as_uri() + "#/ltp-preview"
        print(f"Exported {output}")
        print(f"Opening {url}")
        if not args.no_open:
            webbrowser.open(url)
        return

    handler = lambda *a, **kw: SimpleHTTPRequestHandler(*a, directory=str(root), **kw)
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as exc:
        temporary.cleanup()
        parser.error(f"cannot listen on port {args.port}: {exc}")

    url = f"http://127.0.0.1:{args.port}/#/ltp-preview"
    print(f"Previewing {project_file}")
    print(f"Dashboard: {url}")
    print("Press Ctrl+C to stop.")
    if not args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        temporary.cleanup()


if __name__ == "__main__":
    main()
