# Pull requests that carry reasoning and approval

For a project whose conversational reasoning YAML lives in its own repository. A PR carries the reviewed implementation, the actual tree updates and the recorded typed acceptance of the displayed proposal versions it implements. It names the reasoning served so reviewers can follow the work toward the goal.

## From proposal to PR

1. Show the Change proposal with its ID, revision, reasoning, tree updates, exact covered file paths and validation plan.
2. Wait for typed human acceptance; record the reply, participant, scope, proposal version, recording time and `approved_paths` in `change_acceptances`. Save the intended tree updates and validate before implementation.
3. Implement and test the approved scope. A material expansion needs a revised proposal and fresh acceptance before the extra edits.
4. Include the implementation, reasoning changes and receipt together in the PR. Cite the existing receipt rather than requesting acceptance again for the same approved version and scope.
5. Review the final diff against the accepted scope before merging. Implementation approval, PR review and reasoning endorsement are separate decisions. Creating or merging a PR does not set node/link status to accepted or complete unresolved backlog work.

## The template

Save as `.github/pull_request_template.md`, replacing the state-file path:

```markdown
## What this changes

<!-- One or two sentences. -->

## Reasoning this serves

<!-- Existing node or link IDs from path/to/reason-commons.yaml, one per line. Leave empty only if Tree updates lists new reasoning. -->

## Tree updates

<!-- Every added, changed or removed node/link, one per line, e.g. - added `n3` — what it says. Write None for no node/link edits, and describe any backlog work separately. Generate with:
python3 skills/reason-commons/scripts/check_pr_trees.py path/to/reason-commons.yaml --base origin/main --suggest -->

## Accepted change proposals

<!-- One saved acceptance reference per line, using this exact format:
- `proposal-id` revision 1 by `participant-id`
The receipt must cover the changed files and tree IDs. -->

## Validation

<!-- Checks completed, remaining uncertainty, and review of implementation against the accepted scope. -->
```

GitHub fills a new PR's description with the template in the browser. Agents or `gh pr create --body-file` must fill these sections themselves. An acceptance reference is not a fresh proposal or a request to endorse the reasoning. Several proposals may be delivered in one PR; list the relevant receipt versions individually.

## What the check establishes

`scripts/check_pr_trees.py` compares the working tree with the merge base of `--base` and `HEAD`, across one or more state files. In the reasoning sections, a list item's first backticked ID is its claim; later IDs, such as link endpoints, are description. Template comments are ignored. The checker validates current conversational state using the sibling `update_views.py` helper without writing snapshots or views. Keep both scripts together when using them in another repository.

The check fails when:

- a stated tree update has no matching node/link change, a verb disagrees, an actual node/link change is unstated, a served ID does not exist, or required reasoning sections are missing;
- the current YAML or acceptance metadata is invalid, or an earlier acceptance receipt has been changed or removed;
- the Accepted change proposals section is missing, empty or malformed, or names an unrecorded proposal version and participant;
- a cited receipt lacks `approved_paths`, a changed file is outside the cited paths, or a changed node/link ID is outside the cited tree-item IDs.

Use exact repository-relative paths, including the state file and coordination files covered by the proposal. Paths are literal names, not globs; renames require both the old and new names. Coverage may come from several cited receipts. Uncited receipts cannot supply coverage. Receipt additions and backlog/coordination edits are covered through their file paths and textual scope; the Tree updates list still describes node/link changes. Historical node/link IDs remain valid receipt references after removal.

The working-tree check includes tracked and staged changes, including staged new files. Untracked drafts are outside the PR until explicitly staged. Run after staging the intended files, then repeat against the committed branch if its diff changes. CI checks the committed PR head. Old conversational receipts without `approved_paths` remain valid records, but need a new scoped approval to supply PR file coverage; do not retrofit an earlier reply to an expanded approval.

These checks establish declared coverage, not that code inside an approved file fulfills the intended change, that a stored reply came from the human, or that approval preceded editing. Review the implementation and original conversation for those questions. The checker never changes reasoning standing.

## Run locally and in CI

```sh
python3 skills/reason-commons/scripts/check_pr_trees.py path/to/reason-commons.yaml --base origin/main --body-file /tmp/pr-body.md
```

Save as `.github/workflows/tree-check.yml`, adjusting the state-file path:

```yaml
name: Tree check
on:
  pull_request:
    types: [opened, edited, synchronize, reopened]
permissions:
  contents: read
jobs:
  tree-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pyyaml
      - name: Test reasoning and approval helpers
        run: python3 -m unittest discover -s skills/reason-commons/tests
      - name: Check tree updates and recorded acceptance coverage
        env:
          PR_BODY: ${{ github.event.pull_request.body }}
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
        run: |
          printf '%s\n' "$PR_BODY" > "$RUNNER_TEMP/pr-body.md"
          python3 skills/reason-commons/scripts/check_pr_trees.py path/to/reason-commons.yaml --base "$BASE_SHA" --body-file "$RUNNER_TEMP/pr-body.md"
```

The description passes through an environment variable rather than being interpolated into executable shell code. The `edited` trigger rechecks corrected descriptions; `synchronize` checks updated commits.

## Small changes

A small fix still follows the proposal and typed acceptance rule, names the reasoning served, and makes the meaningful annotation or backlog update described by the proposal. Write None only for no node/link edits, and report backlog work in the proposal, scope and result. Reuse existing reasoning rather than inventing claims to fill a template. If the connection to the goal is missing or the requirement encourages loose citations, record that gap or challenge and resolve it before implementation.
