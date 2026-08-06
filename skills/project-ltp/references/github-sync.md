# GitHub issue sync

Use this reference when a project wants its transition-tree actions tracked as
GitHub Issues, so committed work is visible without the tree and the tracker
becoming two rival accounts of what is being done.

## The rule that keeps one source of truth

| Question | Answered by |
|----------|-------------|
| What is this action, and what effect should it produce? | `ltp/ltp-model.yaml` |
| Which conditions does it advance, what verifies it, what is the risk? | `ltp/ltp-model.yaml` |
| Is it open, closed, or dropped? Who picked it up? When did it move? | the GitHub issue |

Nothing else crosses the line. `sync_github_issues.py` never opens, closes, or
reassigns an issue, and it never writes to the causal model. Anything that does
not fit the rule — an issue body edited on GitHub, an issue for a node that no
longer exists — is reported as drift for a person to settle.

## What links a node to an issue

The issue body opens with a marker comment:

```html
<!-- project-ltp:action=ACT-2 -->
```

That marker is the durable link. `ltp/github-sync.yaml` is a ledger of derived
state — issue number, state, assignees, and the digests of the last pushed
content — and can be deleted and rebuilt with `pull` at any time. Do not
hand-edit it, and do not treat it as a second model.

## Commands

Run from the skill's repository, pointing `--project` at the analyzed project:

```bash
python skills/project-ltp/scripts/sync_github_issues.py status --project /path/to/project
```

- `status` — read both sides and report. Writes nothing.
- `pull` — refresh `ltp/github-sync.yaml` with the state GitHub reports. This
  is what makes progress visible in the dashboard.
- `push` — create issues for untracked actions and update issues whose tree
  node has changed. **Dry run unless `--apply` is passed.**

Exit codes: `2` on error for all three. `status` returns 1 whenever anything
needs attention, so it is the one to gate CI on. `pull` returns 0 whenever it
recorded reality, however messy that reality is. `push` returns 1 only when
drift blocked a write, or when a dry run found work still to do — deliberately
held-back actions do not count as failure.

Useful flags: `--repo OWNER/NAME` (default: the project's `origin`), `--label`
(default `ltp-action`), `--view` (default `transition-tree`), and `--json`.
Push also takes `--only ACTION_ID` (repeatable, to open or update one node at a
time) and `--force` (overwrites issues edited on GitHub, losing those edits).

The script shells out to `gh`, so it uses whatever `gh auth status` reports.

## What `status` classifies

| Report | Meaning | Resolution |
|--------|---------|------------|
| needs an issue | an action with no issue | `push --apply` |
| issue is behind the tree | the node changed since the last push | `push --apply` |
| issue was edited on GitHub | someone edited the body directly | fold the edit into the tree, then push; or `push --apply --force` to discard it |
| conflict — both sides changed | the node and the body both moved | a person decides which is right |
| recorded issue not found | the ledger names an issue that no longer carries the marker | re-open, re-label, or clear the ledger entry and push |
| labelled issue with no tree node | work is being tracked that the tree does not explain | add a node for it, or drop the label |
| issue whose action is not in the tree | the node was removed or renamed | close the issue, or restore the node |

The last two matter most for the method: they are how work that does not trace
to the goal becomes visible instead of quietly accumulating.

## Suggested cadence

1. `pull` before reviewing progress, so the tree shows what GitHub knows.
2. `push --apply` after the transition tree changes.
3. `status` in CI or before a working session, to catch drift early.

Because the rendered body is deterministic, re-running `push` with an unchanged
model produces no GitHub writes at all.

## In the dashboard

Action nodes gain a ring badge — hollow for open, filled for closed as done,
grey for closed as not planned, amber for out of step — the overview gains a
tracked-work summary line, and the details panel shows the issue link,
assignees, and what any drift means. A project with no tracking renders
exactly as before.

Issue state reaches the page two ways, and the overview says which one it is:

1. **Live from GitHub.** The browser reads the repository's public issues API
   directly and rebuilds the action↔issue mapping from the body markers. This
   is what makes an issue closed a minute ago show as closed without anyone
   rebuilding or republishing the site. Declare the repository in the project
   manifest to enable it with no snapshot at all:

   ```json
   { "slug": "2r-research-circle",
     "github": { "repo": "Promise-Foundation/2R-Research", "label": "ltp-action" } }
   ```

2. **Snapshot.** `serve_dashboard.py` serves the ledger at `/api/github-sync`
   and the published dashboard reads `projects/<slug>/github-sync.yaml`. It
   paints immediately, works offline and for private repositories, and is the
   only source of *drift*, since deciding whether an issue body still matches
   its tree node needs the digests recorded at push time.

The snapshot renders first and the live read replaces it when it lands. Any
failure — offline, rate-limited, private, renamed — silently leaves the
snapshot on screen rather than emptying the page. Reads are unauthenticated, so
GitHub's 60-requests-per-hour-per-IP limit applies; the dashboard makes one
request per project opened.

Local serving needs `connect-src https://api.github.com` in the page's Content
Security Policy. `serve_dashboard.py` sets that; a host serving the published
build under a stricter policy would fall back to the snapshot.

## Publishing issue state for a project in another repository

The dashboard publishes a *snapshot* of each project's model under
`dashboard/public/projects/<slug>/`. When the analyzed project lives in a
different repository, `--model` and `--ledger` let the sync refresh that
snapshot's issue state directly, with no local clone of the source project:

```bash
python3 skills/project-ltp/scripts/sync_github_issues.py pull \
  --model skills/project-ltp/dashboard/public/projects/<slug>/model.yaml \
  --repo OWNER/NAME
```

The ledger defaults to `github-sync.yaml` beside the model, which is where the
dashboard looks. `--model` always requires an explicit `--repo`: guessing from
the working directory would find the repository holding the snapshot rather
than the one the work lives in.

`dashboard/package.json` wires this up as `npm run sync:github`, and
`publish_dashboard.sh` runs it before building. The refresh needs network and
an authenticated `gh`; when either is missing the publish continues with the
committed ledger and prints a warning, so an offline build never silently
publishes an empty tracker.
