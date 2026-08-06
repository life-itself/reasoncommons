#!/usr/bin/env python3
"""Synchronize transition-tree actions with GitHub Issues.

Division of authority, so the two never become rival sources of truth:

- ``ltp/ltp-model.yaml`` owns the *logic* of an action: its statement, the
  effect it should produce, the conditions it advances, its prerequisites,
  verification, risk, and rollback. That content flows model -> GitHub.
- The GitHub issue owns the *execution state*: open or closed, who picked it
  up, when it last moved. That state flows GitHub -> ``ltp/github-sync.yaml``.

Nothing else crosses. This script never opens, closes, or reassigns an issue,
and it never edits the causal model. Anything that cannot be resolved under
that rule is reported as drift for a human to settle.

The durable link between a tree node and an issue is the marker comment in the
issue body, not the ledger file, so ``ltp/github-sync.yaml`` can be deleted and
rebuilt from GitHub at any time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Optional, Sequence

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - environment guard
    print(
        "error: this script needs PyYAML. Install it with 'python3 -m pip install pyyaml'.",
        file=sys.stderr,
    )
    raise SystemExit(2)


DEFAULT_VIEW = "transition-tree"
DEFAULT_LABEL = "ltp-action"
LABEL_COLOR = "1d76db"
LABEL_DESCRIPTION = "Tracks one action node of the project-ltp transition tree"
TITLE_LIMIT = 100
MARKER_RE = re.compile(r"<!--\s*project-ltp:action=([A-Za-z0-9][\w.-]*)\s*-->")
ACTION_TYPES = {"action"}
ISSUE_FIELDS = (
    "number,title,body,state,stateReason,url,assignees,labels,updatedAt,closedAt"
)

# Drift classifications, in report order.
CREATE = "create"
UPDATE = "update"
IN_SYNC = "in-sync"
ISSUE_EDITED = "issue-edited"
CONFLICT = "conflict"
MISSING_REMOTE = "missing-remote"


class SyncError(RuntimeError):
    """A condition the operator has to resolve before syncing can continue."""


# --------------------------------------------------------------------------
# Model reading and issue rendering
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RenderedIssue:
    action_id: str
    title: str
    body: str

    @property
    def title_digest(self) -> str:
        return digest(self.title)

    @property
    def body_digest(self) -> str:
        return digest(self.body)


@dataclass(frozen=True)
class RemoteIssue:
    number: int
    title: str
    body: str
    state: str
    url: str
    state_reason: Optional[str] = None
    assignees: tuple[str, ...] = ()
    labels: tuple[str, ...] = ()
    updated_at: Optional[str] = None
    closed_at: Optional[str] = None

    @property
    def action_id(self) -> Optional[str]:
        return marker_action(self.body)


def digest(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:32]


def issue_number_from_url(url: str) -> Optional[int]:
    match = re.search(r"/issues/(\d+)\s*$", url.strip())
    return int(match.group(1)) if match else None


def marker_action(body: Optional[str]) -> Optional[str]:
    match = MARKER_RE.search(body or "")
    return match.group(1) if match else None


def load_model(path: Path) -> dict:
    if not path.is_file():
        raise SyncError(
            f"Missing {path}. Run Project LTP first, or point --project at a directory "
            "containing ltp/ltp-model.yaml."
        )
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("entities"), list):
        raise SyncError(f"{path} is not a Project LTP model.")
    return data


def action_ids(model: dict, view: str = DEFAULT_VIEW) -> list[str]:
    """Action entity IDs in the given view, in the order the view lists them."""
    entities = {
        entity["id"]: entity
        for entity in model.get("entities", [])
        if isinstance(entity, dict) and entity.get("id")
    }
    view_definition = (model.get("views") or {}).get(view)
    if not view_definition:
        raise SyncError(
            f"The model has no '{view}' view. Build the transition tree before syncing issues."
        )
    ids = [
        entity_id
        for entity_id in view_definition.get("entities", [])
        if entities.get(entity_id, {}).get("type") in ACTION_TYPES
    ]
    if not ids:
        raise SyncError(f"The '{view}' view contains no action entities to track.")
    return ids


def _entity(model: dict, entity_id: str) -> dict:
    for entity in model.get("entities", []):
        if isinstance(entity, dict) and entity.get("id") == entity_id:
            return entity
    return {}


def _outgoing(model: dict, entity_id: str, view: str) -> list[dict]:
    view_links = set((model.get("views") or {}).get(view, {}).get("links", []))
    return [
        link
        for link in model.get("links", [])
        if link.get("from") == entity_id and (not view_links or link.get("id") in view_links)
    ]


def _bullet(model: dict, entity_id: str) -> str:
    statement = _entity(model, entity_id).get("statement", "").strip()
    return f"- `{entity_id}` — {statement}" if statement else f"- `{entity_id}`"


def _section(heading: str, body: str) -> str:
    return f"### {heading}\n\n{body.strip()}\n"


def issue_title(action_id: str, statement: str, limit: int = TITLE_LIMIT) -> str:
    prefix = f"{action_id} — "
    room = limit - len(prefix)
    statement = " ".join(statement.split())
    if len(statement) <= room:
        return prefix + statement
    clipped = statement[: room - 1].rsplit(" ", 1)[0].rstrip(",;:.")
    return prefix + clipped + "…"


def render_issue(model: dict, action_id: str, view: str = DEFAULT_VIEW) -> RenderedIssue:
    """Render one action as a deterministic issue title and body.

    Determinism matters: re-rendering an unchanged model must produce a
    byte-identical body, otherwise every run would report false drift.
    """
    action = _entity(model, action_id)
    if not action:
        raise SyncError(f"{action_id} is not an entity in the model.")
    statement = action.get("statement", "").strip()
    project_name = (model.get("project") or {}).get("name", "this project")

    parts: list[str] = [
        f"<!-- project-ltp:action={action_id} -->",
        f"**Transition `{action_id}`** in the {view.replace('-', ' ')} of **{project_name}**.",
        "",
        statement,
        "",
    ]

    effects = _outgoing(model, action_id, view)
    if effects:
        lines = []
        for link in effects:
            lines.append(_bullet(model, link["to"]))
            for onward in _outgoing(model, link["to"], view):
                target = _entity(model, onward["to"]).get("statement", "").strip()
                relation = str(onward.get("relation", "advances")).replace("_", " ")
                lines.append(f"  - {relation} `{onward['to']}` — {target}")
        parts.append(_section("Expected effect", "\n".join(lines)))

    prerequisites = action.get("prerequisites") or []
    if prerequisites:
        parts.append(
            _section(
                "Prerequisites",
                "\n".join(_bullet(model, item) for item in prerequisites),
            )
        )

    for heading, key in (
        ("Verification", "verification"),
        ("Risk", "risk"),
        ("Rollback", "rollback"),
        ("Likely scope", "likely_scope"),
        ("Why this is in the model", "reasoning"),
    ):
        value = str(action.get(key) or "").strip()
        if value:
            parts.append(_section(heading, value))

    parts.append(
        "---\n\n"
        "Tracked by `project-ltp`. The transition tree owns this issue's content: edit "
        "`ltp/ltp-model.yaml` and re-run `sync_github_issues.py push` rather than editing "
        "the body here. This issue owns whether the work is open, assigned, or done — the "
        "sync never changes that.\n"
    )
    return RenderedIssue(action_id=action_id, title=issue_title(action_id, statement), body="\n".join(parts))


# --------------------------------------------------------------------------
# Ledger
# --------------------------------------------------------------------------


@dataclass
class LedgerEntry:
    issue: Optional[int] = None
    url: Optional[str] = None
    state: Optional[str] = None
    state_reason: Optional[str] = None
    assignees: list[str] = field(default_factory=list)
    updated_at: Optional[str] = None
    closed_at: Optional[str] = None
    pushed_title_digest: Optional[str] = None
    pushed_body_digest: Optional[str] = None
    pushed_at: Optional[str] = None
    sync_status: Optional[str] = None

    def to_yaml(self) -> dict:
        data = {
            "issue": self.issue,
            "url": self.url,
            "state": self.state,
            "state_reason": self.state_reason,
            "assignees": list(self.assignees),
            "updated_at": self.updated_at,
            "closed_at": self.closed_at,
            "pushed_title_digest": self.pushed_title_digest,
            "pushed_body_digest": self.pushed_body_digest,
            "pushed_at": self.pushed_at,
            "sync_status": self.sync_status,
        }
        return {key: value for key, value in data.items() if value not in (None, [])}

    @classmethod
    def from_yaml(cls, data: object) -> "LedgerEntry":
        if not isinstance(data, dict):
            return cls()
        return cls(
            issue=data.get("issue"),
            url=data.get("url"),
            state=data.get("state"),
            state_reason=data.get("state_reason"),
            assignees=list(data.get("assignees") or []),
            updated_at=data.get("updated_at"),
            closed_at=data.get("closed_at"),
            pushed_title_digest=data.get("pushed_title_digest"),
            pushed_body_digest=data.get("pushed_body_digest"),
            pushed_at=data.get("pushed_at"),
            sync_status=data.get("sync_status"),
        )


@dataclass
class Ledger:
    repo: Optional[str] = None
    view: str = DEFAULT_VIEW
    label: str = DEFAULT_LABEL
    synced_at: Optional[str] = None
    actions: dict[str, LedgerEntry] = field(default_factory=dict)
    untracked_issues: list[dict] = field(default_factory=list)
    orphan_issues: list[dict] = field(default_factory=list)

    def entry(self, action_id: str) -> LedgerEntry:
        return self.actions.get(action_id, LedgerEntry())


def load_ledger(path: Path) -> Ledger:
    if not path.is_file():
        return Ledger()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SyncError(f"{path} is not a sync ledger.")
    return Ledger(
        repo=data.get("repo"),
        view=data.get("view", DEFAULT_VIEW),
        label=data.get("label", DEFAULT_LABEL),
        synced_at=data.get("synced_at"),
        actions={
            key: LedgerEntry.from_yaml(value)
            for key, value in (data.get("actions") or {}).items()
        },
        untracked_issues=list(data.get("untracked_issues") or []),
        orphan_issues=list(data.get("orphan_issues") or []),
    )


LEDGER_HEADER = """\
# Generated by skills/project-ltp/scripts/sync_github_issues.py — do not hand-edit.
# Derived state only: the issue body marker is the durable action <-> issue link,
# so deleting this file loses nothing that a `pull` cannot rebuild.
"""


def dump_ledger(ledger: Ledger, path: Path) -> None:
    payload = {
        "repo": ledger.repo,
        "view": ledger.view,
        "label": ledger.label,
        "synced_at": ledger.synced_at,
        "actions": {key: value.to_yaml() for key, value in ledger.actions.items()},
    }
    if ledger.untracked_issues:
        payload["untracked_issues"] = ledger.untracked_issues
    if ledger.orphan_issues:
        payload["orphan_issues"] = ledger.orphan_issues
    body = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(LEDGER_HEADER + body, encoding="utf-8")


# --------------------------------------------------------------------------
# GitHub access
# --------------------------------------------------------------------------

Runner = Callable[[Sequence[str], Optional[str]], str]


def _subprocess_runner(args: Sequence[str], stdin: Optional[str], cwd: Path) -> str:
    try:
        completed = subprocess.run(
            ["gh", *args],
            input=stdin,
            cwd=str(cwd),
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:  # pragma: no cover - environment guard
        raise SyncError(
            "The GitHub CLI ('gh') is not installed. Install it and run 'gh auth login'."
        ) from error
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        raise SyncError(f"gh {' '.join(args)} failed: {detail}")
    return completed.stdout


class GitHub:
    """Every GitHub call this script makes, behind one injectable runner."""

    def __init__(self, repo: Optional[str], cwd: Path, runner: Optional[Runner] = None):
        self._cwd = cwd
        self._runner: Runner = runner or (lambda args, stdin: _subprocess_runner(args, stdin, cwd))
        self.repo = repo or self._detect_repo()

    def _run(self, args: Sequence[str], stdin: Optional[str] = None) -> str:
        return self._runner(list(args), stdin)

    def _detect_repo(self) -> str:
        output = self._run(["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]).strip()
        if not output:
            raise SyncError(
                "Could not determine the GitHub repository. Pass --repo OWNER/NAME."
            )
        return output

    def list_issues(self, label: str) -> list[RemoteIssue]:
        output = self._run(
            [
                "issue", "list",
                "--repo", self.repo,
                "--label", label,
                "--state", "all",
                "--limit", "500",
                "--json", ISSUE_FIELDS,
            ]
        )
        raw = json.loads(output or "[]")
        return [_remote_from_json(item) for item in raw]

    def view_issue(self, number: int) -> RemoteIssue:
        output = self._run(
            ["issue", "view", str(number), "--repo", self.repo, "--json", ISSUE_FIELDS]
        )
        return _remote_from_json(json.loads(output))

    def ensure_label(self, label: str) -> None:
        self._run(
            [
                "label", "create", label,
                "--repo", self.repo,
                "--description", LABEL_DESCRIPTION,
                "--color", LABEL_COLOR,
                "--force",
            ]
        )

    def create_issue(self, rendered: RenderedIssue, label: str) -> str:
        return self._run(
            [
                "issue", "create",
                "--repo", self.repo,
                "--title", rendered.title,
                "--label", label,
                "--body-file", "-",
            ],
            stdin=rendered.body,
        ).strip()

    def edit_issue(self, number: int, rendered: RenderedIssue) -> None:
        self._run(
            [
                "issue", "edit", str(number),
                "--repo", self.repo,
                "--title", rendered.title,
                "--body-file", "-",
            ],
            stdin=rendered.body,
        )


def _remote_from_json(item: dict) -> RemoteIssue:
    # `gh` reports COMPLETED / NOT_PLANNED where the REST API the dashboard
    # reads says completed / not_planned. Normalize so one vocabulary reaches
    # the ledger whichever path filled it.
    return RemoteIssue(
        number=int(item["number"]),
        title=item.get("title") or "",
        body=item.get("body") or "",
        state=str(item.get("state") or "").lower(),
        url=item.get("url") or "",
        state_reason=(str(item["stateReason"]).lower() if item.get("stateReason") else None),
        assignees=tuple(a.get("login", "") for a in item.get("assignees") or []),
        labels=tuple(label.get("name", "") for label in item.get("labels") or []),
        updated_at=item.get("updatedAt"),
        closed_at=item.get("closedAt"),
    )


# --------------------------------------------------------------------------
# Planning
# --------------------------------------------------------------------------


@dataclass
class ActionPlan:
    action_id: str
    kind: str
    rendered: RenderedIssue
    remote: Optional[RemoteIssue] = None
    reasons: list[str] = field(default_factory=list)

    @property
    def needs_human(self) -> bool:
        return self.kind in {CONFLICT, ISSUE_EDITED, MISSING_REMOTE}


@dataclass
class SyncPlan:
    repo: str
    label: str
    view: str
    actions: list[ActionPlan]
    untracked: list[RemoteIssue] = field(default_factory=list)
    orphans: list[RemoteIssue] = field(default_factory=list)

    def of_kind(self, *kinds: str) -> list[ActionPlan]:
        return [plan for plan in self.actions if plan.kind in kinds]

    @property
    def is_clean(self) -> bool:
        return (
            not self.of_kind(CREATE, UPDATE, CONFLICT, ISSUE_EDITED, MISSING_REMOTE)
            and not self.untracked
            and not self.orphans
        )


def build_plan(
    model: dict,
    ledger: Ledger,
    remote_issues: Iterable[RemoteIssue],
    *,
    repo: str,
    view: str = DEFAULT_VIEW,
    label: str = DEFAULT_LABEL,
) -> SyncPlan:
    """Classify every action and every labelled issue without touching either side."""
    ids = action_ids(model, view)
    by_action: dict[str, RemoteIssue] = {}
    untracked: list[RemoteIssue] = []
    duplicates: list[RemoteIssue] = []
    for issue in remote_issues:
        action = issue.action_id
        if action is None:
            untracked.append(issue)
        elif action in by_action:
            # Two issues claim one node. Keep the lower number; report the other.
            first = by_action[action]
            keep, extra = (first, issue) if first.number <= issue.number else (issue, first)
            by_action[action] = keep
            duplicates.append(extra)
        else:
            by_action[action] = issue

    orphans = [issue for action, issue in by_action.items() if action not in ids]
    orphans.extend(duplicates)
    orphans.sort(key=lambda issue: issue.number)

    plans: list[ActionPlan] = []
    for action_id in ids:
        rendered = render_issue(model, action_id, view)
        entry = ledger.entry(action_id)
        remote = by_action.get(action_id)
        if remote is None:
            if entry.issue:
                plans.append(
                    ActionPlan(
                        action_id,
                        MISSING_REMOTE,
                        rendered,
                        None,
                        [
                            f"the ledger records issue #{entry.issue} but no labelled issue "
                            "carries this action's marker — it may have been deleted, "
                            "transferred, or unlabelled"
                        ],
                    )
                )
            else:
                plans.append(ActionPlan(action_id, CREATE, rendered, None, ["no issue tracks this action"]))
            continue

        remote_rendered = RenderedIssue(action_id, remote.title, remote.body)
        model_matches_remote = (
            rendered.title_digest == remote_rendered.title_digest
            and rendered.body_digest == remote_rendered.body_digest
        )
        if not entry.pushed_body_digest:
            # Adopted issue: no recorded push, so attribute nothing to either side.
            kind = IN_SYNC if model_matches_remote else UPDATE
            reasons = [] if model_matches_remote else ["adopted issue whose content differs from the model"]
            plans.append(ActionPlan(action_id, kind, rendered, remote, reasons))
            continue

        model_changed = (
            rendered.body_digest != entry.pushed_body_digest
            or rendered.title_digest != entry.pushed_title_digest
        )
        remote_changed = (
            remote_rendered.body_digest != entry.pushed_body_digest
            or remote_rendered.title_digest != entry.pushed_title_digest
        )
        if model_changed and remote_changed:
            kind, reasons = CONFLICT, ["the tree node and the issue body have both changed since the last push"]
        elif model_changed:
            kind, reasons = UPDATE, ["the tree node changed since the last push"]
        elif remote_changed:
            kind, reasons = ISSUE_EDITED, ["the issue body was edited on GitHub since the last push"]
        else:
            kind, reasons = IN_SYNC, []
        plans.append(ActionPlan(action_id, kind, rendered, remote, reasons))

    return SyncPlan(
        repo=repo,
        label=label,
        view=view,
        actions=plans,
        untracked=sorted(untracked, key=lambda issue: issue.number),
        orphans=orphans,
    )


def apply_remote_state(ledger: Ledger, plan: SyncPlan) -> Ledger:
    """Fold the observed GitHub state into the ledger. Execution state only."""
    ledger.repo = plan.repo
    ledger.view = plan.view
    ledger.label = plan.label
    ledger.synced_at = now()
    for action_plan in plan.actions:
        entry = ledger.actions.setdefault(action_plan.action_id, LedgerEntry())
        entry.sync_status = action_plan.kind
        remote = action_plan.remote
        if remote is None:
            continue
        entry.issue = remote.number
        entry.url = remote.url
        entry.state = remote.state
        entry.state_reason = remote.state_reason
        entry.assignees = list(remote.assignees)
        entry.updated_at = remote.updated_at
        entry.closed_at = remote.closed_at
    for stale in set(ledger.actions) - {p.action_id for p in plan.actions}:
        del ledger.actions[stale]
    ledger.actions = {p.action_id: ledger.actions[p.action_id] for p in plan.actions}
    ledger.untracked_issues = [
        {"issue": issue.number, "url": issue.url, "title": issue.title} for issue in plan.untracked
    ]
    ledger.orphan_issues = [
        {
            "issue": issue.number,
            "url": issue.url,
            "title": issue.title,
            "action": issue.action_id,
        }
        for issue in plan.orphans
    ]
    return ledger


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

KIND_LABELS = {
    CREATE: "needs an issue",
    UPDATE: "issue is behind the tree",
    ISSUE_EDITED: "issue was edited on GitHub",
    CONFLICT: "conflict — both sides changed",
    MISSING_REMOTE: "recorded issue not found",
    IN_SYNC: "in sync",
}


def format_report(plan: SyncPlan, *, applied: bool = False) -> str:
    lines = [f"{plan.repo} · {plan.view} · label {plan.label}", ""]
    for action_plan in plan.actions:
        remote = action_plan.remote
        where = f"#{remote.number}" if remote else "—"
        state = ""
        if remote:
            state = f" [{remote.state}{'/' + remote.state_reason if remote.state_reason else ''}]"
            if remote.assignees:
                state += f" @{', @'.join(remote.assignees)}"
        lines.append(
            f"  {action_plan.action_id:<8} {where:>5}{state}  {KIND_LABELS[action_plan.kind]}"
        )
        for reason in action_plan.reasons:
            lines.append(f"           ↳ {reason}")

    if plan.untracked:
        lines += ["", "Labelled issues with no tree node (add a node, or drop the label):"]
        lines += [f"  #{issue.number} {issue.title}" for issue in plan.untracked]
    if plan.orphans:
        lines += ["", "Issues whose action is not in the tree, or duplicates:"]
        lines += [f"  #{issue.number} ({issue.action_id}) {issue.title}" for issue in plan.orphans]

    counts = {kind: len(plan.of_kind(kind)) for kind in KIND_LABELS}
    summary = ", ".join(f"{count} {KIND_LABELS[kind]}" for kind, count in counts.items() if count)
    lines += ["", f"{'Applied' if applied else 'Summary'}: {summary or 'nothing to do'}."]
    if not applied and (counts[CREATE] or counts[UPDATE]):
        lines.append("Run with 'push --apply' to write these to GitHub.")
    if counts[CONFLICT] or counts[ISSUE_EDITED]:
        lines.append(
            "Resolve edited or conflicting issues by hand, or overwrite them with "
            "'push --apply --force' once the tree says what you want."
        )
    return "\n".join(lines)


def plan_as_json(plan: SyncPlan) -> str:
    return json.dumps(
        {
            "repo": plan.repo,
            "view": plan.view,
            "label": plan.label,
            "clean": plan.is_clean,
            "actions": [
                {
                    "action": action_plan.action_id,
                    "kind": action_plan.kind,
                    "issue": action_plan.remote.number if action_plan.remote else None,
                    "url": action_plan.remote.url if action_plan.remote else None,
                    "state": action_plan.remote.state if action_plan.remote else None,
                    "assignees": list(action_plan.remote.assignees) if action_plan.remote else [],
                    "reasons": action_plan.reasons,
                }
                for action_plan in plan.actions
            ],
            "untracked_issues": [
                {"issue": issue.number, "title": issue.title, "url": issue.url}
                for issue in plan.untracked
            ],
            "orphan_issues": [
                {"issue": issue.number, "action": issue.action_id, "url": issue.url}
                for issue in plan.orphans
            ],
        },
        indent=2,
    )


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Context:
    model_path: Path
    ledger_path: Path
    model: dict
    ledger: Ledger
    github: GitHub
    view: str
    label: str


def build_context(args: argparse.Namespace, runner: Optional[Runner] = None) -> Context:
    project = args.project.expanduser().resolve()
    # --model / --ledger let the sync run against a published snapshot of a
    # model that lives in another repository, so a dashboard can show issue
    # state without a local clone of the analyzed project.
    model_path = (args.model or project / "ltp" / "ltp-model.yaml").expanduser()
    ledger_path = (
        args.ledger
        or (args.model.with_name("github-sync.yaml") if args.model else project / "ltp" / "github-sync.yaml")
    ).expanduser()
    model = load_model(model_path)
    ledger = load_ledger(ledger_path)
    label = args.label or ledger.label or DEFAULT_LABEL
    view = args.view or ledger.view or DEFAULT_VIEW
    repo = args.repo or ledger.repo
    if args.model and not repo:
        # Detecting the repo from the working directory would find whichever
        # repo holds the snapshot, not the one the model's work lives in.
        raise SyncError("--model needs an explicit --repo OWNER/NAME.")
    github = GitHub(repo, project, runner)
    return Context(model_path, ledger_path, model, ledger, github, view, label)


def _plan_from_github(context: Context, confirm: Iterable[int] = ()) -> SyncPlan:
    issues = context.github.list_issues(context.label)
    # The label-filtered list is served from a search index that lags a second
    # or two behind a write, so an issue this run just touched can be missing
    # from it. Fetch those by number instead of reporting them as absent.
    seen = {issue.number for issue in issues}
    for number in confirm:
        if number not in seen:
            issues.append(context.github.view_issue(number))
    return build_plan(
        context.model,
        context.ledger,
        issues,
        repo=context.github.repo,
        view=context.view,
        label=context.label,
    )


def command_status(context: Context, args: argparse.Namespace) -> int:
    plan = _plan_from_github(context)
    print(plan_as_json(plan) if args.json else format_report(plan))
    return 0 if plan.is_clean else 1


def command_pull(context: Context, args: argparse.Namespace) -> int:
    plan = _plan_from_github(context)
    ledger = apply_remote_state(context.ledger, plan)
    context.ledger_path.parent.mkdir(parents=True, exist_ok=True)
    dump_ledger(ledger, context.ledger_path)
    if args.json:
        print(plan_as_json(plan))
    else:
        print(format_report(plan))
        print(f"\nWrote {context.ledger_path}.")
    # Recording reality is a success even when reality is messy. Use `status`
    # when the exit code should gate on drift.
    return 0


def command_push(context: Context, args: argparse.Namespace) -> int:
    plan = _plan_from_github(context)
    kinds = [CREATE, UPDATE] + ([ISSUE_EDITED, CONFLICT] if args.force else [])
    pending = plan.of_kind(*kinds)
    if args.only:
        selected = set(args.only)
        unknown = selected - {action_plan.action_id for action_plan in plan.actions}
        if unknown:
            raise SyncError(f"--only names actions that are not in the view: {', '.join(sorted(unknown))}")
        held_back = [p.action_id for p in pending if p.action_id not in selected]
        pending = [p for p in pending if p.action_id in selected]
        if held_back:
            print(f"--only: holding back {', '.join(held_back)}.\n")

    blocked = plan.of_kind(CONFLICT, ISSUE_EDITED, MISSING_REMOTE)
    if not args.apply:
        print(format_report(plan))
        if pending:
            print("\nDry run. Nothing was written to GitHub.")
        return 0 if not pending and not blocked else 1

    if pending:
        context.github.ensure_label(context.label)
    applied: list[str] = []
    touched: list[int] = []
    for action_plan in pending:
        if action_plan.remote is None:
            url = context.github.create_issue(action_plan.rendered, context.label)
            number = issue_number_from_url(url)
            if number:
                touched.append(number)
            applied.append(f"  created {action_plan.action_id} → {url}")
        else:
            context.github.edit_issue(action_plan.remote.number, action_plan.rendered)
            touched.append(action_plan.remote.number)
            applied.append(
                f"  updated {action_plan.action_id} → #{action_plan.remote.number}"
            )
        entry = context.ledger.actions.setdefault(action_plan.action_id, LedgerEntry())
        entry.pushed_title_digest = action_plan.rendered.title_digest
        entry.pushed_body_digest = action_plan.rendered.body_digest
        entry.pushed_at = now()

    # Re-read GitHub so the ledger records issue numbers and state as they now are.
    final_plan = _plan_from_github(context, confirm=touched)
    context.ledger_path.parent.mkdir(parents=True, exist_ok=True)
    dump_ledger(apply_remote_state(context.ledger, final_plan), context.ledger_path)
    print(format_report(final_plan, applied=True))
    if applied:
        print("\n" + "\n".join(applied))
    print(f"\nWrote {context.ledger_path}.")
    # Deliberately held-back actions are not a failure; drift that stopped a
    # write is. Use `status` to gate on everything else.
    return 1 if final_plan.of_kind(CONFLICT, ISSUE_EDITED, MISSING_REMOTE) else 0


COMMANDS = {"status": command_status, "pull": command_pull, "push": command_push}


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Keep GitHub Issues and the transition-tree actions of a Project LTP model "
            "in step. The model owns what an action is; the issue owns whether it is done."
        )
    )
    parser.add_argument("command", choices=sorted(COMMANDS), help="status, pull, or push")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Analyzed project root")
    parser.add_argument(
        "--model",
        type=Path,
        help="Model file to sync against, instead of <project>/ltp/ltp-model.yaml",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        help="Where to write the sync ledger (default: github-sync.yaml beside the model)",
    )
    parser.add_argument("--repo", help="GitHub repository as OWNER/NAME (default: the project's origin)")
    parser.add_argument("--view", help=f"Model view to sync (default: {DEFAULT_VIEW})")
    parser.add_argument("--label", help=f"Issue label marking tracked actions (default: {DEFAULT_LABEL})")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="push only: actually write to GitHub. Without it, push is a dry run.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="push only: overwrite issues edited on GitHub, losing those edits.",
    )
    parser.add_argument(
        "--only",
        action="append",
        metavar="ACTION_ID",
        help="push only: restrict writes to these action IDs. Repeatable.",
    )
    parser.add_argument("--json", action="store_true", help="Emit the plan as JSON")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    try:
        context = build_context(args)
        return COMMANDS[args.command](context, args)
    except SyncError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
