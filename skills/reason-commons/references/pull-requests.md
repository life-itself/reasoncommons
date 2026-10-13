# Pull requests that name their reasoning

For a project whose reasoning YAML lives in its own repository. Each pull request says which part of the tree it serves and lists the tree updates it makes, and a check confirms that list against the YAML. The result is that work reaching the repository stays connected to the goal, and anyone reading a pull request can see why it exists.

## The template

Save as `.github/pull_request_template.md`, replacing the state-file path:

```markdown
## What this changes

<!-- One or two sentences. -->

## Reasoning this serves

<!-- Existing node or link IDs from path/to/reason-commons.yaml that this change puts into practice or supports, one per line, e.g. "- `f-e-some-injection` — what it says". Leave empty only if Tree updates lists new reasoning. -->

## Tree updates

<!-- Every node and link this pull request adds, changes or removes in the YAML, one per line, e.g. "- added `r-e-some-effect` — what it says". Write "None" if it changes no reasoning. Generate the list with:
python3 skills/reason-commons/scripts/check_pr_trees.py path/to/reason-commons.yaml --base origin/main --suggest -->
```

GitHub fills a new pull request's description with this template in the browser. `gh pr create --body` and agents that write their own description do not, so tell agents working in the repository (in `AGENTS.md` or equivalent) to use these sections.

## The check

`scripts/check_pr_trees.py` compares the working tree with the merge base of `--base` and `HEAD`, across one or more state files. In each section, a list item's first backticked ID is its claim; any later IDs, such as a link's endpoints, are description. HTML comments are ignored, so the template's examples never count. The check fails when:

- a listed tree update has no matching YAML change, or its verb (`added`, `changed`, `removed`) disagrees with the YAML;
- the YAML adds, changes or removes a node or link that is not listed;
- a served ID is not a node or link in the YAML;
- the description has no Tree updates section, or names no reasoning at all.

Any difference in a node or link counts as a change, including status, wording, contributions and assumptions. Backlog edits and coordination fields do not.

To run it on every pull request, save as `.github/workflows/tree-check.yml`:

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
      - name: Check the stated tree updates against the YAML
        env:
          PR_BODY: ${{ github.event.pull_request.body }}
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
        run: |
          printf '%s\n' "$PR_BODY" > "$RUNNER_TEMP/pr-body.md"
          python3 skills/reason-commons/scripts/check_pr_trees.py path/to/reason-commons.yaml --base "$BASE_SHA" --body-file "$RUNNER_TEMP/pr-body.md"
```

The description passes through an environment variable rather than being interpolated into the script, so nothing in it can run as a command. The `edited` trigger re-runs the check when someone fixes the description.

## Small changes

A typo fix still names what it serves, usually the nearest existing node, with Tree updates set to "None". If citing reasoning for small changes becomes a ritual, record that as a challenge in the tree rather than loosening the check silently.
