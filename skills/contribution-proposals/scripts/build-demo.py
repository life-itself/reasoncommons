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

While you are still working out whether the reading is any good, build to the
test route instead and look at it in a browser:

    python3 build-demo.py --proposals <anywhere>.yaml --test --serve

That writes talk/2r-research-group/demo-c-test/, stamps the page as a test build
so it can never be mistaken for the real one, serves the repo, and opens the
page. The test route is gitignored and excluded from the published site. When
the batch is right, --promote copies it onto the live route and rebuilds.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import http.server
import json
import pathlib
import shutil
import socketserver
import sys
import threading
import webbrowser

try:
    import yaml
except ImportError:  # pragma: no cover - environment problem, not a data problem
    sys.exit("PyYAML is required: pip3 install pyyaml")

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "templates" / "demo.html"

# The two routes. LIVE is what ships and gets published; TEST is the loop you
# work in, gitignored and excluded from the site, so a half-read batch can never
# reach an audience by accident.
LIVE_ROUTE = pathlib.Path("talk/2r-research-group/demo-c")
TEST_ROUTE = pathlib.Path("talk/2r-research-group/demo-c-test")

# Where the live route ends up once it is merged. The trailing index.html is not
# optional: a bare folder URL 404s on this site, because Flowershow only
# resolves those for markdown pages.
SITE = "https://reasoncommons.com"

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


def resolve_paths(args) -> None:
    """Work out which route we are building to, and fill in the defaults."""
    route = TEST_ROUTE if args.test else LIVE_ROUTE
    if args.proposals is None:
        args.proposals = str(route / "proposals.yaml")
    if args.out is None:
        args.out = str(route / "index.html")


def serve(path: pathlib.Path, port: int, open_browser: bool) -> None:
    """Serve the repo root so the page can be looked at, and stay up."""
    root = pathlib.Path.cwd()
    url = f"http://localhost:{port}/{path.as_posix()}"

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(root), **kw)

        def log_message(self, fmt, *a):
            # A 200 for every asset is noise. A miss is worth knowing about.
            if a and str(a[1]).startswith(("4", "5")):
                sys.stderr.write("  %s %s\n" % (a[1], a[0]))

    class Reusable(socketserver.TCPServer):
        allow_reuse_address = True
        daemon_threads = True

    try:
        httpd = Reusable(("127.0.0.1", port), Handler)
    except OSError as exc:
        raise Problem(f"cannot serve on port {port}: {exc}. Try --port with another number.")

    print(f"\n  serving here   {url}", flush=True)
    print(f"                 from {root} — ctrl-c to stop", flush=True)
    if open_browser:
        threading.Timer(0.4, webbrowser.open, args=(url,)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped")
    finally:
        httpd.server_close()


def promote() -> int:
    """Copy the test batch onto the live route and rebuild it there."""
    src = TEST_ROUTE / "proposals.yaml"
    if not src.exists():
        raise Problem(f"nothing to promote: {src} does not exist. Build with --test first.")
    LIVE_ROUTE.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, LIVE_ROUTE / "proposals.yaml")
    print(f"  copied {src} -> {LIVE_ROUTE / 'proposals.yaml'}")
    return 0


def report(out: pathlib.Path, is_test: bool) -> None:
    """Say, in as many words, where this page can now be opened.

    Every build ends here. Somebody running this an hour before a talk should
    not have to work out the URL, and should not be able to confuse the route
    that publishes with the route that never does.
    """
    print()
    print(f"  open it now    file://{out.resolve()}")

    try:
        rel = out.resolve().relative_to(pathlib.Path.cwd().resolve())
    except ValueError:
        print("  (built outside the repo, so it has no published address)")
        return

    url = f"{SITE}/{rel.as_posix()}"
    if is_test:
        print(f"  will NOT publish — {url}")
        print("                   returns 404 by design: the test route is gitignored")
        print("                   and excluded from the site. Use --promote when it is right.")
    else:
        print(f"  published at   {url}")
        print("                 once this is committed and merged to main (a minute or two).")
        print("                 Keep the /index.html — the bare folder URL 404s.")


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
    meta["mode"] = "test" if args.test else "live"
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

    if args.test:
        kept = TEST_ROUTE / "proposals.yaml"
        if proposals_path.resolve() != kept.resolve():
            kept.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(proposals_path, kept)
            print(f"  kept a copy at {kept} — edit that and rebuild, then --promote")
        print("  TEST BUILD — stamped on the page, gitignored, not published")

    report(out, args.test)

    if args.serve:
        serve(out, args.port, not args.no_open)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="ltp/ltp-model.yaml")
    ap.add_argument("--proposals", default=None,
                    help=f"defaults to {LIVE_ROUTE}/proposals.yaml, or the test route's under --test")
    ap.add_argument("--out", default=None,
                    help=f"defaults to {LIVE_ROUTE}/index.html, or the test route's under --test")
    ap.add_argument("--test", action="store_true",
                    help=f"build to {TEST_ROUTE}/ and stamp the page as a test build — "
                         "gitignored and excluded from the published site")
    ap.add_argument("--serve", action="store_true",
                    help="after building, serve the repo and open the page in a browser")
    ap.add_argument("--port", type=int, default=8731, help="port for --serve (default 8731)")
    ap.add_argument("--no-open", action="store_true", help="with --serve, do not open a browser")
    ap.add_argument("--promote", action="store_true",
                    help="copy the test batch onto the live route and rebuild it there")
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--strict", action="store_true",
                    help="treat 'target not in view' as an error rather than a warning")
    args = ap.parse_args()

    try:
        if args.promote:
            if args.test:
                raise Problem("--promote and --test are opposites; pick one")
            promote()
            args.proposals = args.proposals or str(LIVE_ROUTE / "proposals.yaml")
        resolve_paths(args)
        return build(args)
    except Problem as exc:
        print(f"build-demo: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
