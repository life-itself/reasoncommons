#!/usr/bin/env python3
"""Check a pull request's stated tree updates against its changes to the reasoning YAML.

    check_pr_trees.py --base origin/main --body-file pr.md reason-commons.yaml
    check_pr_trees.py --base origin/main --suggest reason-commons.yaml

The body's "Reasoning this serves" section names existing node or link IDs; its "Tree
updates" section lists every node and link the branch adds, changes or removes, optionally
starting with the verb. Each is one list item whose first backticked ID is the claim.

The check fails when a stated update has no matching YAML change, a YAML change is
unstated, a served ID does not exist, or the pull request names no reasoning at all.
--suggest prints the Tree updates list instead.

Compares the working tree with the merge base of --base and HEAD.
"""

import argparse
from pathlib import Path
import re
import subprocess
import sys

import yaml

SERVES = "reasoning this serves"
UPDATES = "tree updates"
VERBS = ("added", "changed", "removed")
ID = re.compile(r"`([A-Za-z0-9][\w-]*)`")


def items(state):
    """Every node and link by ID, with its tree and category."""
    found = {}
    for tree, content in ((state or {}).get("trees") or {}).items():
        for category in ("nodes", "links"):
            for item in (content or {}).get(category) or []:
                found[item["id"]] = (tree, category, item)
    return found


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def load_states(paths, base, cwd):
    """Items at the merge base and in the working tree, across all state files."""
    result = git(cwd, "merge-base", base, "HEAD")
    if result.returncode:
        raise SystemExit(f"Cannot find the merge base of {base} and HEAD: {result.stderr.strip()}")
    merge_base = result.stdout.strip()
    before, after = {}, {}
    for path in paths:
        old = git(cwd, "show", f"{merge_base}:{path}")
        before.update(items(yaml.safe_load(old.stdout) if old.returncode == 0 else None))
        current = Path(cwd or ".") / path
        after.update(items(yaml.safe_load(current.read_text()) if current.exists() else None))
    return before, after


def changes(before, after):
    """(verb, id, tree, category, item) for each added, changed or removed item, in file order."""
    found = []
    for id_, (tree, category, item) in after.items():
        if id_ not in before:
            found.append(("added", id_, tree, category, item))
        elif before[id_][2] != item:
            found.append(("changed", id_, tree, category, item))
    for id_, (tree, category, item) in before.items():
        if id_ not in after:
            found.append(("removed", id_, tree, category, item))
    return found


def sections(body):
    """Section text keyed by lower-cased heading, with HTML comments removed."""
    body = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)
    found, heading = {}, None
    for line in body.splitlines():
        match = re.match(r"\s*#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            heading = match.group(1).strip().lower()
            found[heading] = []
        elif heading is not None:
            found[heading].append(line)
    return {heading: "\n".join(lines) for heading, lines in found.items()}


def claims(text):
    """(verb or None, id) per line: the first backticked ID, and a verb that starts the list item.

    Later IDs on a line, such as a link's endpoints, are description rather than claims.
    """
    found = []
    for line in (text or "").splitlines():
        id_ = ID.search(line)
        if not id_:
            continue
        verb = re.match(r"\s*(?:[-*+]|\d+[.)])?\s*(\w+)", line)
        verb = verb.group(1).lower() if verb and verb.group(1).lower() in VERBS else None
        found.append((verb, id_.group(1)))
    return found


def describe(change):
    verb, id_, tree, category, item = change
    if category == "nodes":
        detail = f"{tree}, {item.get('kind')}, {item.get('status')}): {item.get('text')}"
    else:
        sources = " + ".join(f"`{source}`" for source in item.get("from") or [])
        detail = f"{tree} link, {item.get('status')}): {sources} {item.get('relation', '').replace('_', ' ')} `{item.get('to')}`"
    return f"- {verb} `{id_}` ({detail}"


def check(body, before, after):
    """Problems with the body's claims, as a list of messages."""
    parts = sections(body)
    serves = [id_ for _, id_ in claims(parts.get(SERVES))]
    stated = claims(parts.get(UPDATES))
    actual = {change[1]: change[0] for change in changes(before, after)}
    problems = []
    if UPDATES not in parts:
        problems.append('The description has no "Tree updates" section. Write "None" there if the pull request changes no reasoning.')
    if not serves and not stated:
        problems.append('The pull request names no reasoning. List the node or link it serves under "Reasoning this serves", or the reasoning it adds under "Tree updates".')
    for id_ in serves:
        if id_ not in after:
            problems.append(f"Serves `{id_}`, which is not a node or link in the reasoning YAML.")
    stated_ids = {}
    for verb, id_ in stated:
        stated_ids.setdefault(id_, verb)
    for id_, verb in stated_ids.items():
        if id_ not in actual:
            problems.append(f"Lists `{id_}` as a tree update, but the YAML does not change it.")
        elif verb and verb != actual[id_]:
            problems.append(f"Lists `{id_}` as {verb}, but the YAML shows it {actual[id_]}.")
    for id_, verb in actual.items():
        if id_ not in stated_ids:
            problems.append(f"The YAML {verb} `{id_}`, but the Tree updates section does not list it.")
    return problems


def main(argv=None, cwd=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("states", nargs="+", help="reasoning YAML files, relative to the repository root")
    parser.add_argument("--base", required=True, help="base branch or commit, such as origin/main")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--body-file", help="file holding the pull request description")
    mode.add_argument("--suggest", action="store_true", help="print the Tree updates list for this branch")
    args = parser.parse_args(argv)
    before, after = load_states(args.states, args.base, cwd)
    if args.suggest:
        found = changes(before, after)
        print("\n".join(describe(change) for change in found) if found else "None")
        return 0
    body = Path(args.body_file).read_text()
    problems = check(body, before, after)
    if problems:
        print("Tree check failed:")
        print("\n".join(f"- {problem}" for problem in problems))
        return 1
    serves = [id_ for _, id_ in claims(sections(body).get(SERVES))]
    print(f"Tree check passed: serves {len(serves)} existing item(s); {len(changes(before, after))} tree update(s) match the YAML.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
