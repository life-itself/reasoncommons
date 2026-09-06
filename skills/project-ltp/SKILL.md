---
name: project-ltp
description: >
  DEPRECATED on 2026-09-06 — do not use this skill to produce or revise an LTP
  model. Use `ltp-project` instead: it writes the Reason Commons `*.ltp.yaml`
  interchange file, the same document the app imports and exports as JSON or
  YAML with history. What remains here is the read-only dashboard over legacy
  `ltp-model.yaml` files and its build scripts.
---

> **Deprecated 2026-09-06.** This skill's `ltp-model.yaml` format was a second, incompatible way of writing an LTP model, and a model written this way cannot be imported into Reason Commons or carry the version and event history the app keeps. Use [`../ltp-project/SKILL.md`](../ltp-project/SKILL.md) for any new or revised model; a space's export from the app (`.reason-commons/<space-id>.ltp.json` in a connected repository) is the canonical representation of a model with history. GitHub issue tracking for transition-tree actions is done by the Reason Commons GitHub projection, which writes and reconciles managed issues itself, so `scripts/sync_github_issues.py` is retired with it. The dashboard under `dashboard/` and `scripts/serve_dashboard.py` remain as a viewer for the legacy `ltp-model.yaml` files still bundled on the site until the dashboard can read the interchange format.


# Project LTP

Reconstruct the logic implicit in a project and maintain one evidence-backed
causal model. Render the Goal Tree, Current Reality Tree, Evaporating Clouds,
Future Reality Tree, Prerequisite Tree, and Transition Tree as views of that
shared model rather than as unrelated documents.

## Required operating principles

1. Classify every material statement as `observed`, `inferred`, `provisional`,
   `confirmed`, or `disputed`.
2. Attach evidence, source paths, line ranges when available, reasoning, and
   confidence to observed and inferred entities.
3. Never present inferred business intent as fact.
4. Express important causal links as:
   `If [cause], then [effect], because [assumption].`
5. Reuse stable entity and link identifiers across all trees.
6. Record tree membership under the model's `views` map.
7. Maintain the machine-readable model in `ltp-model.yaml`.
8. Continue with a clearly marked provisional goal when evidence is incomplete.
9. Never claim repository coverage that was not actually achieved.

Read `references/principles-and-model.md` before building or revising the
causal model.

## Choose the analysis mode

### Forward mode

Use when the primary input is a codebase, system, or collection of project
artifacts.

Build in this order:

1. Evidence map
2. Goal Tree
3. Current Reality Tree
4. Evaporating Clouds
5. Future Reality Tree
6. Prerequisite Tree
7. Transition Tree
8. Next-action recommendation

### Reverse mode

Use when the primary input is a TODO list, roadmap, implementation plan, or
task set. Treat each task as a candidate Transition Tree action, infer the
logic it is supposed to serve, and reject or flag tasks that do not trace to
the goal.

### Reconciliation mode

Use when both implementation evidence and a plan are available. Compare what
the code does, what the plan assumes, what the goal requires, and what work is
missing or irrelevant.

Read `references/analysis-workflow.md` for the full examination and
reconciliation procedure.

## Repository workflow

### 1. Inventory

Enumerate files and classify them as source, tests, configuration,
infrastructure, documentation, schemas, UI text, CI/CD, monitoring, plans,
generated files, vendor dependencies, binaries, or unknown.

### 2. Examine behavior

Identify actors, inputs, outputs, workflows, state changes, integrations,
failure paths, and acceptance criteria. Prefer evidence in this order:

1. Executable behavior and tests
2. Configuration and schemas
3. Public interfaces and contracts
4. Architecture decisions
5. Operational documentation
6. Issues and plans
7. README claims
8. Comments and TODOs
9. Names and directory structure

### 3. Find intent and pain signals

Look for product claims, architectural intent, incomplete work, repeated
failures, workarounds, contradictions, reliability risks, security risks,
deprecations, and missing implementations.

### 4. Synthesize one causal model

Create entities, evidence items, assumptions, links, open questions,
contradictions, coverage gaps, view membership, and the current constraint in
`ltp-model.yaml`.

### 5. Render the trees

Read `references/tree-construction.md` and apply the construction rules for
each tree. Reuse entity IDs whenever the same condition appears in multiple
views.

### 6. Determine what to work on next

Identify the current constraint, locate the earliest blocked objective, prefer
high-leverage actions over visible activity, and choose one primary action.
State its expected immediate effect and the uncertainty most likely to change
the recommendation.

## Required files

When the user asks for a full analysis, create an `ltp/` directory with the
canonical deliverables below:

- `00-coverage-and-evidence.md`
- `01-project-model.md`
- `02-goal-tree.md`
- `03-current-reality-tree.md`
- `04-evaporating-clouds.md`
- `05-future-reality-tree.md`, including negative-branch analysis
- `06-prerequisite-tree.md`
- `07-transition-tree.md`
- `08-next-action.md`
- `09-assumptions-and-questions.md`
- `ltp-model.yaml`

Create `throughput.yaml` only when a defensible goal unit and real observations
are available. Never invent throughput history to fill the dashboard.

Use Mermaid diagrams when useful, but ensure every diagram also has a readable
text representation.

Read `references/validation-and-deliverables.md` for validation checks,
incremental-update behavior, output requirements, and the final response
format.

## Track actions as GitHub Issues

When the user wants transition-tree actions tracked, assigned, or closed as
GitHub Issues, read `references/github-sync.md` and use:

```bash
python skills/project-ltp/scripts/sync_github_issues.py status --project /path/to/project
```

`status` and `pull` are safe to run unprompted. `push` writes to GitHub, so run
it as a dry run first and only pass `--apply` once the user has seen the plan.

Hold the boundary the sync depends on: the model owns what an action is, and
the issue owns whether it is open, assigned, or done. Never record execution
state in `ltp-model.yaml`, and never resolve reported drift by inventing an
answer — say which side changed and let the user decide.

## Local dashboard

When the user asks for a visual or local interface, read
`references/dashboard-and-throughput.md`, make the shared model dashboard-ready,
then run:

```bash
python skills/project-ltp/scripts/serve_dashboard.py --project /path/to/project --open
```

Treat the dashboard as a read-only view of the YAML files, not as a second
source of truth. Bind to loopback unless the user explicitly requests network
access.

## Completion rules

Before finalizing:

1. Validate causal sufficiency and expose assumptions.
2. Check cross-tree identifier consistency.
3. Distinguish observations from interpretations.
4. List contradictions and unresolved questions.
5. Report excluded, unreadable, generated, binary, or oversized files.
6. Give one primary next action, not an unranked task list.
7. State what evidence could overturn the recommendation.
8. Validate stable link IDs and all entity/link references in `views`.
