from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_github_issues.py"
SPEC = importlib.util.spec_from_file_location("sync_github_issues", SCRIPT)
assert SPEC and SPEC.loader
sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync
SPEC.loader.exec_module(sync)


MODEL = """
project:
  name: Test Project
entities:
  - id: ACT-1
    type: action
    statement: Define a markdown format for a transition tree
    status: inferred
    confidence: high
    prerequisites: []
    verification: A named path holds a transition tree
    risk: The format is abandoned
    rollback: Revert the file
    likely_scope: 'repo: ltp/'
    reasoning: The notes give this as the hypothesis
  - id: ACT-2
    type: action
    statement: Open GitHub Issues linked one-to-one to transition tree nodes
    status: inferred
    confidence: high
    prerequisites: [ACT-1]
  - id: TR-1
    type: expected_effect
    statement: A canonical transition tree exists
    status: inferred
    confidence: high
  - id: NC-4
    type: necessary_condition
    statement: One canonical location
    status: inferred
    confidence: high
links:
  - id: L-1
    from: ACT-1
    to: TR-1
    relation: produces
  - id: L-2
    from: TR-1
    to: NC-4
    relation: achieves
views:
  transition-tree:
    title: The transitions
    purpose: Action to effect to condition.
    entities: [ACT-1, TR-1, NC-4, ACT-2]
    links: [L-1, L-2]
"""


def write_project(root: Path, model: str = MODEL, ledger: str | None = None) -> Path:
    project = root / "project"
    (project / "ltp").mkdir(parents=True)
    (project / "ltp" / "ltp-model.yaml").write_text(model, encoding="utf-8")
    if ledger is not None:
        (project / "ltp" / "github-sync.yaml").write_text(ledger, encoding="utf-8")
    return project


def remote(number: int, rendered: sync.RenderedIssue, **overrides) -> sync.RemoteIssue:
    defaults = dict(
        number=number,
        title=rendered.title,
        body=rendered.body,
        state="open",
        url=f"https://github.com/o/r/issues/{number}",
    )
    defaults.update(overrides)
    return sync.RemoteIssue(**defaults)


class RenderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = sync.yaml.safe_load(MODEL)

    def test_actions_come_from_the_view_in_order(self) -> None:
        self.assertEqual(sync.action_ids(self.model), ["ACT-1", "ACT-2"])

    def test_body_carries_a_parseable_marker_and_the_logic(self) -> None:
        rendered = sync.render_issue(self.model, "ACT-1")
        self.assertEqual(sync.marker_action(rendered.body), "ACT-1")
        self.assertIn("`TR-1` — A canonical transition tree exists", rendered.body)
        self.assertIn("achieves `NC-4`", rendered.body)
        self.assertIn("### Verification", rendered.body)
        self.assertIn("### Risk", rendered.body)
        self.assertTrue(rendered.title.startswith("ACT-1 — "))

    def test_rendering_is_deterministic(self) -> None:
        first = sync.render_issue(self.model, "ACT-1")
        second = sync.render_issue(sync.yaml.safe_load(MODEL), "ACT-1")
        self.assertEqual(first.body_digest, second.body_digest)

    def test_absent_optional_fields_are_omitted(self) -> None:
        rendered = sync.render_issue(self.model, "ACT-2")
        self.assertNotIn("### Verification", rendered.body)
        self.assertIn("- `ACT-1` — Define a markdown format", rendered.body)

    def test_long_statements_are_clipped_at_a_word_boundary(self) -> None:
        title = sync.issue_title("ACT-9", "word " * 40)
        self.assertLessEqual(len(title), sync.TITLE_LIMIT)
        self.assertTrue(title.endswith("…"))

    def test_a_model_without_a_transition_tree_is_refused(self) -> None:
        model = sync.yaml.safe_load(MODEL)
        model["views"] = {}
        with self.assertRaises(sync.SyncError):
            sync.action_ids(model)


class PlanTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = sync.yaml.safe_load(MODEL)
        self.act1 = sync.render_issue(self.model, "ACT-1")
        self.act2 = sync.render_issue(self.model, "ACT-2")

    def plan(self, ledger: sync.Ledger, issues: list[sync.RemoteIssue]) -> sync.SyncPlan:
        return sync.build_plan(self.model, ledger, issues, repo="o/r")

    def pushed_ledger(self) -> sync.Ledger:
        return sync.Ledger(
            repo="o/r",
            actions={
                "ACT-1": sync.LedgerEntry(
                    issue=1,
                    pushed_title_digest=self.act1.title_digest,
                    pushed_body_digest=self.act1.body_digest,
                ),
                "ACT-2": sync.LedgerEntry(
                    issue=2,
                    pushed_title_digest=self.act2.title_digest,
                    pushed_body_digest=self.act2.body_digest,
                ),
            },
        )

    def test_untracked_actions_need_an_issue(self) -> None:
        plan = self.plan(sync.Ledger(), [])
        self.assertEqual([p.kind for p in plan.actions], [sync.CREATE, sync.CREATE])
        self.assertFalse(plan.is_clean)

    def test_matching_content_is_in_sync(self) -> None:
        plan = self.plan(
            self.pushed_ledger(), [remote(1, self.act1), remote(2, self.act2)]
        )
        self.assertEqual({p.kind for p in plan.actions}, {sync.IN_SYNC})
        self.assertTrue(plan.is_clean)

    def test_a_changed_tree_node_becomes_an_update(self) -> None:
        self.model["entities"][0]["statement"] = "Define a different format"
        plan = self.plan(
            self.pushed_ledger(), [remote(1, self.act1), remote(2, self.act2)]
        )
        self.assertEqual(plan.of_kind(sync.UPDATE)[0].action_id, "ACT-1")

    def test_an_edited_issue_is_reported_not_overwritten(self) -> None:
        edited = remote(1, self.act1, body=self.act1.body + "\n\nRufus: started this.")
        plan = self.plan(self.pushed_ledger(), [edited, remote(2, self.act2)])
        edited_plan = plan.of_kind(sync.ISSUE_EDITED)[0]
        self.assertEqual(edited_plan.action_id, "ACT-1")
        self.assertTrue(edited_plan.needs_human)

    def test_changes_on_both_sides_are_a_conflict(self) -> None:
        self.model["entities"][0]["statement"] = "Define a different format"
        edited = remote(1, self.act1, body=self.act1.body + "\n\nRufus: started this.")
        plan = self.plan(self.pushed_ledger(), [edited, remote(2, self.act2)])
        self.assertEqual(plan.of_kind(sync.CONFLICT)[0].action_id, "ACT-1")

    def test_an_issue_found_by_marker_without_a_ledger_is_adopted(self) -> None:
        plan = self.plan(sync.Ledger(), [remote(7, self.act1), remote(8, self.act2)])
        self.assertEqual({p.kind for p in plan.actions}, {sync.IN_SYNC})
        self.assertEqual(plan.actions[0].remote.number, 7)

    def test_a_recorded_issue_that_disappeared_is_flagged(self) -> None:
        plan = self.plan(self.pushed_ledger(), [remote(2, self.act2)])
        missing = plan.of_kind(sync.MISSING_REMOTE)[0]
        self.assertEqual(missing.action_id, "ACT-1")
        self.assertIn("#1", missing.reasons[0])

    def test_a_labelled_issue_with_no_marker_is_untracked_work(self) -> None:
        stray = sync.RemoteIssue(
            number=9, title="Fix the header", body="No marker here", state="open", url="u"
        )
        plan = self.plan(self.pushed_ledger(), [remote(1, self.act1), remote(2, self.act2), stray])
        self.assertEqual([issue.number for issue in plan.untracked], [9])
        self.assertFalse(plan.is_clean)

    def test_an_issue_for_a_removed_node_is_an_orphan(self) -> None:
        gone = sync.RemoteIssue(
            number=11,
            title="ACT-99 — old",
            body="<!-- project-ltp:action=ACT-99 -->",
            state="open",
            url="u",
        )
        plan = self.plan(self.pushed_ledger(), [remote(1, self.act1), remote(2, self.act2), gone])
        self.assertEqual([issue.number for issue in plan.orphans], [11])

    def test_two_issues_claiming_one_node_keep_the_older(self) -> None:
        plan = self.plan(
            self.pushed_ledger(),
            [remote(1, self.act1), remote(5, self.act1), remote(2, self.act2)],
        )
        self.assertEqual(plan.actions[0].remote.number, 1)
        self.assertEqual([issue.number for issue in plan.orphans], [5])

    def test_execution_state_lands_in_the_ledger(self) -> None:
        closed = remote(
            1,
            self.act1,
            state="closed",
            state_reason="completed",
            assignees=("rufus",),
            closed_at="2026-08-01T10:00:00Z",
        )
        plan = self.plan(self.pushed_ledger(), [closed, remote(2, self.act2)])
        ledger = sync.apply_remote_state(sync.Ledger(), plan)
        entry = ledger.actions["ACT-1"]
        self.assertEqual((entry.state, entry.state_reason), ("closed", "completed"))
        self.assertEqual(entry.assignees, ["rufus"])
        self.assertEqual(ledger.repo, "o/r")


def as_json(issue: sync.RemoteIssue) -> dict:
    return {
        "number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "state": issue.state,
        "stateReason": issue.state_reason,
        "url": issue.url,
        "assignees": [{"login": login} for login in issue.assignees],
        "labels": [{"name": name} for name in issue.labels],
        "updatedAt": issue.updated_at,
        "closedAt": issue.closed_at,
    }


class FakeGh:
    """Records gh invocations and answers them from a scripted issue list.

    `list_lag` hides the N most recently created issues from `issue list`,
    reproducing GitHub's label-filtered search index lagging behind a write.
    """

    def __init__(self, issues: list[sync.RemoteIssue] | None = None, list_lag: int = 0):
        self.issues = list(issues or [])
        self.list_lag = list_lag
        self.calls: list[list[str]] = []
        self.stdins: list[str | None] = []
        self._hidden: set[int] = set()
        self._next_number = max((issue.number for issue in self.issues), default=0) + 1

    def __call__(self, args, stdin=None):
        self.calls.append(list(args))
        self.stdins.append(stdin)
        if args[:2] == ["issue", "list"]:
            return json.dumps(
                [as_json(issue) for issue in self.issues if issue.number not in self._hidden]
            )
        if args[:2] == ["issue", "view"]:
            number = int(args[2])
            found = next(issue for issue in self.issues if issue.number == number)
            return json.dumps(as_json(found))
        if args[:2] == ["issue", "create"]:
            number = self._next_number
            self._next_number += 1
            title = args[args.index("--title") + 1]
            url = f"https://github.com/o/r/issues/{number}"
            self.issues.append(
                sync.RemoteIssue(number=number, title=title, body=stdin or "", state="open", url=url)
            )
            if self.list_lag > 0:
                self.list_lag -= 1
                self._hidden.add(number)
            return url + "\n"
        if args[:2] == ["issue", "edit"]:
            number = int(args[2])
            title = args[args.index("--title") + 1]
            self.issues = [
                sync.RemoteIssue(
                    number=issue.number,
                    title=title,
                    body=stdin or "",
                    state=issue.state,
                    url=issue.url,
                )
                if issue.number == number
                else issue
                for issue in self.issues
            ]
            return ""
        if args[:2] == ["label", "create"]:
            return ""
        raise AssertionError(f"unexpected gh call: {args}")


class CommandTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = write_project(Path(self.temp.name))
        self.ledger_path = self.project / "ltp" / "github-sync.yaml"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_command(self, argv: list[str], gh: FakeGh) -> int:
        args = sync.parse_args([*argv, "--project", str(self.project), "--repo", "o/r"])
        context = sync.build_context(args, runner=gh)
        return sync.COMMANDS[args.command](context, args)

    def test_push_without_apply_writes_nothing(self) -> None:
        gh = FakeGh()
        code = self.run_command(["push"], gh)
        self.assertEqual(code, 1)
        self.assertEqual([call[:2] for call in gh.calls], [["issue", "list"]])
        self.assertFalse(self.ledger_path.exists())

    def test_push_apply_creates_one_issue_per_action_and_records_them(self) -> None:
        gh = FakeGh()
        code = self.run_command(["push", "--apply"], gh)
        self.assertEqual(code, 0)
        created = [call for call in gh.calls if call[:2] == ["issue", "create"]]
        self.assertEqual(len(created), 2)
        ledger = sync.load_ledger(self.ledger_path)
        self.assertEqual(ledger.actions["ACT-1"].issue, 1)
        self.assertEqual(ledger.actions["ACT-2"].issue, 2)
        self.assertEqual(ledger.actions["ACT-1"].sync_status, sync.IN_SYNC)

    def test_push_is_idempotent(self) -> None:
        gh = FakeGh()
        self.run_command(["push", "--apply"], gh)
        gh.calls.clear()
        code = self.run_command(["push", "--apply"], gh)
        self.assertEqual(code, 0)
        self.assertEqual(
            [call for call in gh.calls if call[:2] in (["issue", "create"], ["issue", "edit"])],
            [],
        )

    def test_push_never_changes_issue_state(self) -> None:
        gh = FakeGh()
        self.run_command(["push", "--apply"], gh)
        gh.issues[0] = sync.RemoteIssue(
            number=1,
            title=gh.issues[0].title,
            body=gh.issues[0].body,
            state="closed",
            state_reason="completed",
            url=gh.issues[0].url,
        )
        (self.project / "ltp" / "ltp-model.yaml").write_text(
            MODEL.replace("Define a markdown format", "Define a markdown schema"), encoding="utf-8"
        )
        self.run_command(["push", "--apply"], gh)
        mutating = [call for call in gh.calls if call[:2] != ["issue", "list"]]
        state_changing = [
            call
            for call in mutating
            if any(flag in call for flag in ("--state", "close", "reopen", "--add-assignee"))
        ]
        self.assertEqual(state_changing, [])
        self.assertEqual(gh.issues[0].state, "closed")

    def test_push_refuses_to_clobber_a_github_edit_without_force(self) -> None:
        gh = FakeGh()
        self.run_command(["push", "--apply"], gh)
        edited_body = gh.issues[0].body + "\n\nRufus: I started this."
        gh.issues[0] = sync.RemoteIssue(
            number=1, title=gh.issues[0].title, body=edited_body, state="open", url=gh.issues[0].url
        )
        code = self.run_command(["push", "--apply"], gh)
        self.assertEqual(code, 1)
        self.assertEqual(gh.issues[0].body, edited_body)

        code = self.run_command(["push", "--apply", "--force"], gh)
        self.assertEqual(code, 0)
        self.assertNotIn("Rufus: I started this.", gh.issues[0].body)

    def test_only_restricts_the_push_to_named_actions(self) -> None:
        gh = FakeGh()
        code = self.run_command(["push", "--apply", "--only", "ACT-1"], gh)
        self.assertEqual(code, 0)  # holding ACT-2 back was deliberate, not a failure
        created = [call for call in gh.calls if call[:2] == ["issue", "create"]]
        self.assertEqual(len(created), 1)
        self.assertIn("ACT-1 — ", created[0][created[0].index("--title") + 1])
        ledger = sync.load_ledger(self.ledger_path)
        self.assertEqual(ledger.actions["ACT-1"].issue, 1)
        self.assertIsNone(ledger.actions["ACT-2"].issue)

    def test_a_lagging_issue_list_does_not_lose_a_created_issue(self) -> None:
        gh = FakeGh(list_lag=2)
        code = self.run_command(["push", "--apply"], gh)
        self.assertEqual(code, 0)
        self.assertEqual(
            [call[:3] for call in gh.calls if call[:2] == ["issue", "view"]],
            [["issue", "view", "1"], ["issue", "view", "2"]],
        )
        ledger = sync.load_ledger(self.ledger_path)
        self.assertEqual(ledger.actions["ACT-1"].issue, 1)
        self.assertEqual(ledger.actions["ACT-1"].sync_status, sync.IN_SYNC)

    def test_only_rejects_an_unknown_action_id(self) -> None:
        args = sync.parse_args(
            ["push", "--apply", "--only", "ACT-99", "--project", str(self.project), "--repo", "o/r"]
        )
        context = sync.build_context(args, runner=FakeGh())
        with self.assertRaises(sync.SyncError):
            sync.command_push(context, args)

    def test_pull_records_execution_state_without_touching_github(self) -> None:
        gh = FakeGh()
        self.run_command(["push", "--apply"], gh)
        gh.issues[0] = sync.RemoteIssue(
            number=1,
            title=gh.issues[0].title,
            body=gh.issues[0].body,
            state="closed",
            state_reason="completed",
            url=gh.issues[0].url,
            assignees=("rufus",),
            closed_at="2026-08-02T09:00:00Z",
        )
        gh.calls.clear()
        code = self.run_command(["pull"], gh)
        self.assertEqual(code, 0)
        self.assertEqual([call[:2] for call in gh.calls], [["issue", "list"]])
        ledger = sync.load_ledger(self.ledger_path)
        self.assertEqual(ledger.actions["ACT-1"].state, "closed")
        self.assertEqual(ledger.actions["ACT-1"].assignees, ["rufus"])

    def test_pull_rebuilds_a_deleted_ledger_from_the_markers(self) -> None:
        gh = FakeGh()
        self.run_command(["push", "--apply"], gh)
        self.ledger_path.unlink()
        code = self.run_command(["pull"], gh)
        self.assertEqual(code, 0)
        ledger = sync.load_ledger(self.ledger_path)
        self.assertEqual(ledger.actions["ACT-2"].issue, 2)

    def test_status_reports_drift_as_json(self) -> None:
        gh = FakeGh()
        args = sync.parse_args(
            ["status", "--json", "--project", str(self.project), "--repo", "o/r"]
        )
        context = sync.build_context(args, runner=gh)
        code = sync.command_status(context, args)
        self.assertEqual(code, 1)

    def test_pull_exits_zero_even_when_the_tree_is_untracked(self) -> None:
        gh = FakeGh()
        self.assertEqual(self.run_command(["pull"], gh), 0)
        self.assertTrue(self.ledger_path.exists())

    def test_a_published_snapshot_can_be_synced_without_the_source_repo(self) -> None:
        """The dashboard publishes a copy of a model that lives in another
        repository; --model/--ledger keep that copy's issue state fresh."""
        snapshot = Path(self.temp.name) / "site" / "projects" / "2r" / "model.yaml"
        snapshot.parent.mkdir(parents=True)
        snapshot.write_text(MODEL, encoding="utf-8")
        gh = FakeGh()
        args = sync.parse_args(
            ["pull", "--model", str(snapshot), "--repo", "o/r", "--project", str(self.project)]
        )
        context = sync.build_context(args, runner=gh)
        self.assertEqual(sync.command_pull(context, args), 0)
        # Default ledger location is beside the snapshot, not in the project.
        written = snapshot.with_name("github-sync.yaml")
        self.assertTrue(written.is_file())
        self.assertFalse(self.ledger_path.exists())
        self.assertEqual(sync.load_ledger(written).repo, "o/r")

    def test_a_snapshot_sync_refuses_to_guess_the_repo(self) -> None:
        snapshot = Path(self.temp.name) / "snapshot.yaml"
        snapshot.write_text(MODEL, encoding="utf-8")
        args = sync.parse_args(["pull", "--model", str(snapshot)])
        with self.assertRaises(sync.SyncError):
            sync.build_context(args, runner=FakeGh())

    def test_a_missing_model_is_a_clear_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            args = sync.parse_args(["status", "--project", temp, "--repo", "o/r"])
            with self.assertRaises(sync.SyncError):
                sync.build_context(args, runner=FakeGh())


if __name__ == "__main__":
    unittest.main()
