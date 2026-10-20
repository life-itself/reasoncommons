#!/usr/bin/env python3
"""Share feedback through an explicitly authorised Git destination.

Only feedback commitments, reports and their derived review work are published.
The normal checkout, index and unrelated reasoning changes are left alone.
"""
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

import yaml

import feedback
import update_views


class SyncError(ValueError):
    pass


def git(repo, *args, data=None, env=None, raw=False):
    try:
        result = subprocess.run(["git", "-C", str(repo), *args], input=data.encode() if data is not None else None,
                                capture_output=True, timeout=30, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise SyncError("Git did not finish; feedback remains saved locally.") from exc
    if result.returncode:
        # Git diagnostics can contain credential-bearing URLs or helper output.
        raise SyncError("Git " + args[0] + " failed; check access, connectivity or conflicting updates.")
    output = result.stdout.decode("utf-8")
    return output if raw else output.strip()


def local_dir(state):
    return state.parent / ("." + state.stem)


def atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".feedback-sync-", dir=path.parent)
    try:
        if path.exists():
            os.fchmod(fd, path.stat().st_mode & 0o777)
        with os.fdopen(fd, "w") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def state_lock(state):
    """Use the Discord host's existing lock for this actual state file."""
    path = local_dir(state) / "discord.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise SyncError("The shared state is busy; retry sync after its current writer finishes.") from exc
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def load_text(text):
    state = yaml.load(text, Loader=update_views.StateLoader)
    update_views.validate(state)
    return state


def destination(state, policy):
    repo = Path(git(state.parent, "rev-parse", "--show-toplevel")).resolve()
    relative = state.relative_to(repo).as_posix()
    if relative != policy["path"] or str(repo) != policy["repo"]:
        raise SyncError("The state moved; authorise its new location explicitly.")
    if git(repo, "remote", "get-url", policy["remote"]) != policy["url"]:
        raise SyncError("The configured remote changed; authorise the new destination explicitly.")
    return repo, relative


def fetch(repo, policy):
    ident = hashlib.sha256((policy["path"] + policy["url"] + policy["branch"]).encode()).hexdigest()[:20]
    ref = "refs/reason-commons/feedback/" + ident
    # No force update: rewritten remote ancestry requires explicit reconciliation.
    git(repo, "fetch", "--no-tags", policy["remote"], "refs/heads/" + policy["branch"] + ":" + ref)
    tip = git(repo, "rev-parse", ref)
    mode = git(repo, "ls-tree", tip, "--", policy["path"]).split()
    if not mode or mode[0] not in {"100644", "100755"}:
        raise SyncError("The shared state must already be a regular committed file.")
    text = git(repo, "show", tip + ":" + policy["path"], raw=True)
    load_text(text)
    return tip, text, mode[0]


def configure(state, remote, branch, by, source_text):
    """Call once per checkout after the human authorises this destination."""
    state = Path(state).expanduser().resolve()
    current = load_text(state.read_text())
    if by not in current["participants"] or not source_text.strip():
        raise SyncError("Configuration needs a known human and their actual standing authorisation.")
    repo = Path(git(state.parent, "rev-parse", "--show-toplevel")).resolve()
    if remote.startswith("-") or remote not in git(repo, "remote").splitlines():
        raise SyncError("Choose an existing named Git remote.")
    git(repo, "check-ref-format", "refs/heads/" + branch)
    policy = {"repo": str(repo), "path": state.relative_to(repo).as_posix(), "remote": remote,
              "url": git(repo, "remote", "get-url", remote), "branch": branch, "by": by,
              "source_text": source_text, "recorded_at": datetime.now(timezone.utc).isoformat()}
    with state_lock(state):
        tip, text, _ = fetch(repo, policy)
        ancestor = git(repo, "merge-base", "HEAD", tip)
        base_text = git(repo, "show", ancestor + ":" + policy["path"], raw=True)
        # Validate compatibility before enabling any future writes.
        reconcile(load_text(base_text), current, load_text(text))
        atomic(local_dir(state) / "feedback-sync.json", json.dumps(policy, indent=2) + "\n")
        atomic(local_dir(state) / "feedback-sync-base.json", json.dumps({"commit": ancestor, "text": base_text}) + "\n")
    return {"state": "configured", "message": "Standing feedback sync configured for " + remote + "/" + branch + "."}


def definitions(state):
    result = deepcopy(state)
    for key in ("feedback_requests", "driver", "active_tree"):
        result.pop(key, None)
    for tree in result["trees"].values():
        tree["backlog"] = [task for task in tree["backlog"] if task.get("work") != "review_outcome_feedback"]
    return result


def merge_requests(local, remote):
    """Union immutable versions and report IDs; conflicting identities stop sync."""
    merged = deepcopy(remote.get("feedback_requests", []))
    seen = {feedback.key(request): request for request in merged}
    for request in local.get("feedback_requests", []):
        ident = feedback.key(request)
        if ident not in seen:
            merged.append(deepcopy(request))
            seen[ident] = merged[-1]
            continue
        other = seen[ident]
        if {k: v for k, v in request.items() if k != "reports"} != {k: v for k, v in other.items() if k != "reports"}:
            raise SyncError("Conflicting prediction version; both copies were preserved for reconciliation.")
        reports = {report["id"]: report for report in other["reports"]}
        for report in request["reports"]:
            if report["id"] in reports:
                if reports[report["id"]] != report:
                    raise SyncError("Conflicting feedback report ID; both copies were preserved.")
            else:
                other["reports"].append(deepcopy(report))
                reports[report["id"]] = report
        # A deterministic total order keeps independent assessments and deferrals
        # chronological even when two checkouts push in opposite order.
        other["reports"].sort(key=lambda r: (feedback.timestamp(r["recorded_at"]), r["id"]))
    return merged


def reconcile(base, local, remote):
    feedback.guard_transition(base, local)
    feedback.guard_transition(base, remote)
    local_def, remote_def, base_def = definitions(local), definitions(remote), definitions(base)
    if local_def != base_def and remote_def != base_def and local_def != remote_def:
        raise SyncError("Reasoning definitions changed in both copies; reconcile them before sharing feedback.")
    publication = deepcopy(remote)
    publication["feedback_requests"] = merge_requests(local, remote)
    # New predictions can be shared only when their referenced definitions have
    # been shared already. Never publish local implementation reasoning by accident.
    feedback.guard_transition(remote, publication)
    for request in publication["feedback_requests"]:
        for report in request["reports"]:
            feedback.retain_review_work(publication, request, report)
    working = deepcopy(local if local_def != base_def else remote)
    working["feedback_requests"] = deepcopy(publication["feedback_requests"])
    for key in ("driver", "active_tree"):
        if key in local:
            working[key] = local[key]
    for request in working["feedback_requests"]:
        for report in request["reports"]:
            feedback.retain_review_work(working, request, report)
    update_views.validate(publication)
    update_views.validate(working)
    # Reports may be reordered by chronology, but no original prediction/report
    # content may be rewritten or removed.
    feedback.guard_transition(local, working)
    return publication, working


def render(template, target):
    """Replace only feedback, derived backlog and local focus blocks in YAML."""
    original = load_text(template)
    if original == target:
        return template
    root = yaml.compose(template)
    edits = []

    def replace(mapping, key, value):
        pairs = {k.value: (i, k, v) for i, (k, v) in enumerate(mapping.value)}
        if key in pairs:
            i, mark, _ = pairs[key]
            end = mapping.value[i + 1][0].start_mark if i + 1 < len(mapping.value) else mapping.end_mark
            start_index = mark.start_mark.index - mark.start_mark.column
            end_index = end.index - end.column
            indent = mark.start_mark.column
        else:
            end = mapping.end_mark
            start_index = end_index = end.index - end.column
            indent = mapping.start_mark.column
        dumped = yaml.safe_dump({key: value}, sort_keys=False, allow_unicode=True, width=100000)
        replacement = "".join(" " * indent + line if line.strip() else line for line in dumped.splitlines(keepends=True))
        edits.append((start_index, end_index, replacement))

    for key in ("feedback_requests", "driver", "active_tree"):
        if original.get(key) != target.get(key):
            replace(root, key, target[key])
    root_pairs = {k.value: v for k, v in root.value}
    trees = {k.value: v for k, v in root_pairs["trees"].value}
    for name, tree in target["trees"].items():
        if original["trees"][name]["backlog"] != tree["backlog"]:
            replace(trees[name], "backlog", tree["backlog"])
    result = template
    for start, end, text in sorted(edits, reverse=True):
        result = result[:start] + text + result[end:]
    if load_text(result) != target:
        raise SyncError("Sync would change unrelated YAML content; no file was replaced.")
    return result


def commit(repo, policy, tip, mode, text):
    # A private index avoids staging, committing or resetting the user's index.
    with tempfile.TemporaryDirectory(prefix="reason-commons-sync-") as directory:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(directory) / "index")}
        git(repo, "read-tree", tip, env=env)
        blob = git(repo, "hash-object", "-w", "--stdin", data=text)
        git(repo, "update-index", "--add", "--cacheinfo", mode, blob, policy["path"], env=env)
        tree = git(repo, "write-tree", env=env)
        ident = git(repo, "commit-tree", tree, "-p", tip, data="Record shared Reason Commons feedback\n")
        git(repo, "update-ref", "refs/reason-commons/pending-feedback/" + ident, ident)
        return ident


def _sync(state):
    directory = local_dir(state)
    policy_path = directory / "feedback-sync.json"
    if not policy_path.exists():
        return {"state": "local", "message": "Saved locally; feedback sharing is not configured."}
    policy = json.loads(policy_path.read_text())
    repo, _ = destination(state, policy)
    if policy["by"] not in load_text(state.read_text())["participants"]:
        raise SyncError("The standing authorisation no longer names a project participant.")
    checkpoint = json.loads((directory / "feedback-sync-base.json").read_text())
    for _ in range(2):
        before_text = state.read_text()
        local = load_text(before_text)
        tip, remote_text, mode = fetch(repo, policy)
        base = load_text(checkpoint["text"])
        publication, working = reconcile(base, local, load_text(remote_text))
        working_template = before_text if definitions(local) != definitions(base) else remote_text
        working_text = render(working_template, working)
        publication_text = render(remote_text, publication)
        if state.read_text() != before_text:
            raise SyncError("The state changed during sync; preserve both versions and retry.")
        if working_text != before_text:
            atomic(state, working_text)
            update_views.update(state)
        # Cache the verified remote baseline before attempting a push. The actual
        # YAML retains unsent contributions even if this process is interrupted.
        checkpoint = {"commit": tip, "text": remote_text}
        atomic(directory / "feedback-sync-base.json", json.dumps(checkpoint) + "\n")
        if publication == load_text(remote_text):
            return {"state": "shared", "commit": tip, "message": "Feedback verified in shared Git state."}
        ident = commit(repo, policy, tip, mode, publication_text)
        try:
            git(repo, "push", policy["remote"], ident + ":refs/heads/" + policy["branch"])
        except SyncError:
            # A push may have succeeded despite a lost response. Fetch and derive
            # the next attempt from records, rather than resubmitting a report.
            continue
        verified, verified_text, _ = fetch(repo, policy)
        shared = load_text(verified_text)
        feedback.guard_transition(publication, shared)
        # Another writer may have added reports between our push and verification.
        # Incorporate them before advancing the baseline, or a later session would
        # mistake the older working file for deletion of those reports.
        _, refreshed = reconcile(load_text(remote_text), working, shared)
        template = working_text if definitions(working) != definitions(load_text(remote_text)) else verified_text
        refreshed_text = render(template, refreshed)
        if state.read_text() != working_text:
            raise SyncError("The state changed while sharing was verified; its local edits were preserved. Retry sync.")
        if refreshed_text != working_text:
            atomic(state, refreshed_text)
            update_views.update(state)
        atomic(directory / "feedback-sync-base.json", json.dumps({"commit": verified, "text": verified_text}) + "\n")
        return {"state": "shared", "commit": verified, "message": "Feedback committed, pushed and verified in shared Git state."}
    raise SyncError("Sharing could not be verified after two attempts; feedback remains saved locally. Retry sync later.")


def sync(state, *, locked=False):
    """Return an explicit delivery state; a transport failure never undoes capture."""
    state = Path(state).resolve()
    try:
        if locked:
            result = _sync(state)
        else:
            with state_lock(state):
                result = _sync(state)
    except (ValueError, OSError, KeyError, TypeError, yaml.YAMLError) as exc:
        message = str(exc) if isinstance(exc, SyncError) else "Feedback sync needs reconciliation; the local file was preserved."
        result = {"state": "local", "message": message}
    result["checked_at"] = datetime.now(timezone.utc).isoformat()
    atomic(local_dir(state) / "feedback-sync-status.json", json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    setup = sub.add_parser("configure")
    for name in ("remote", "branch", "by", "source-text"):
        setup.add_argument("--" + name, required=True)
    sub.add_parser("sync")
    sub.add_parser("disable")
    args = parser.parse_args()
    state = args.state.expanduser().resolve()
    try:
        if args.command == "configure":
            result = configure(state, args.remote, args.branch, args.by, args.source_text)
        elif args.command == "disable":
            with state_lock(state):
                (local_dir(state) / "feedback-sync.json").unlink(missing_ok=True)
            result = {"state": "local", "message": "Automatic sharing disabled; the reasoning file was retained."}
        else:
            result = sync(state)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
