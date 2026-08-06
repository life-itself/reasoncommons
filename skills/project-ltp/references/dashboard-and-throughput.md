# Local dashboard and throughput

Use this reference when preparing a model for graphical exploration or serving
the bundled local dashboard.

## Dashboard-ready model

Keep `ltp/ltp-model.yaml` authoritative. In addition to the shared-model fields,
include:

```yaml
analysis:
  current_constraint: RC-1
  recommended_next_action: ACT-1
  expected_effect: DE-1
  updated_at: 2026-07-12T14:32:00Z

links:
  - id: L-1
    from: RC-1
    to: UDE-1
    relation: causes
    confidence: high

views:
  current-reality:
    title: Why delivery is unpredictable
    purpose: The causes behind the observed effects.
    entities: [RC-1, UDE-1]
    links: [L-1]
```

Use stable link IDs. Define only views supported by the analysis. Reuse entity
and link IDs rather than copying entities into view-specific structures.

Supported view keys are:

- `goal-tree`
- `current-reality`
- `evaporating-cloud`
- `future-reality`
- `prerequisite-tree`
- `transition-tree`

Validate the contract against `references/ltp-model.schema.json` when a JSON
Schema validator is available.

## Tracked actions

If the project syncs its transition-tree actions to GitHub Issues, the ledger
at `ltp/github-sync.yaml` is served alongside the model and adds issue badges to
action nodes. See `references/github-sync.md`; validate against
`references/github-sync.schema.json`. The file is generated — never hand-edit it.

## Throughput versus flow indicators

Do not equate completed tasks with Theory of Constraints throughput unless the
project explicitly defines completed tasks as its goal unit.

Create `ltp/throughput.yaml` only when a defensible definition and real periods
are available:

```yaml
definition:
  name: Validated decisions adopted by participating groups
  unit: adopted decisions
  period: week
  goal_entity: G-1
  constraint_entity: RC-1
  source: manual activity log

periods:
  - date: 2026-07-06
    throughput: 3
    completed: 8
    work_in_progress: 14
    blocked: 5
    median_cycle_time_days: 6.2
    constraint_queue: 9
```

Treat `completed`, `work_in_progress`, `blocked`, `median_cycle_time_days`, and
`constraint_queue` as supporting flow indicators. Never fabricate missing
periods or silently mix different units.

Validate against `references/throughput.schema.json` when possible.

## Automatic Git-derived node throughput

Use Git-derived node throughput only when the recipient project explicitly
defines adopted changes to another project's LTP model as its goal unit. A
committed change is treated as adoption into the canonical model; proposed,
uncommitted, formatting-only, and generated Markdown changes do not count.

The bundled dashboard configures this relationship for the 2R projects:

- source project: `second-renaissance`
- canonical source: repository-root `ltp/ltp-model.yaml`
- recipient project: `2r-research-circle`
- baseline: the initial committed Second Renaissance model
- unit: one stable entity ID created, semantically updated, or deleted in one
  first-parent revision

The semantic projection for an entity contains the entity fields, its incident
causal links, and its tree-view memberships. YAML mapping order and set-like
list order are normalized away. A stable ID counts at most once per revision,
even when several of its fields change:

```text
throughput = created IDs + updated IDs + deleted IDs
```

`dashboard/throughput.config.json` declares the relationship. Both `npm run
build` and `npm run dev` generate the recipient's `throughput.yaml` before
starting. Run it directly with:

```bash
cd skills/project-ltp/dashboard
npm run generate:throughput
```

The generated file contains consecutive weekly aggregates—including observed
zero-change weeks through the built revision—and a revision ledger with the
affected IDs. The generator also synchronizes the static source-project model
from the same Git revision, so the displayed tree and measured tree cannot
silently diverge. Because the calculation uses repository history, builds must
have the configured baseline revision available rather than a history truncated
after that revision.

## Serve locally

From the skill's repository, run:

```bash
python skills/project-ltp/scripts/serve_dashboard.py --project /path/to/project --open
```

The server binds to loopback, prefers `127.0.0.1:8765`, serves only the bundled
frontend and the three known YAML files, and is read-only. If the preferred port
is occupied and `--port` was not supplied, it tries subsequent ports and prints
the selected URL. An explicit `--port` remains strict. The dashboard polls file
metadata so model changes appear without restarting the server.

Use `--host` with `--allow-network` only after the user explicitly requests
network exposure.
