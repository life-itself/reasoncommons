---
title: Running the dashboard
updated: 2026-09-04
---

# Running the dashboard

The site publishes a read-only dashboard for structured analyses of an organisation's goals and constraints. Each analysis opens on the current constraint, the next action, its expected effect, and any defined throughput signals; the six underlying trees, evidence, assumptions, and filters are available on demand. This page covers adding a project and running the dashboard locally; for what the analysis *is*, start with [the explainer series](../explainers/).

## Published multi-project dashboard

The site publishes the dashboard at [`/dashboard/`](../dashboard/index.html) with a project picker, so several analyses live in one place. Each project is a static model under `skills/project-ltp/dashboard/public/projects/<slug>/model.yaml`, listed in `public/projects/manifest.json`. To add a project, drop its `ltp-model.yaml` (and optional `throughput.yaml`) under a new slug, add a manifest entry, then build and publish:

```bash
sh skills/project-ltp/scripts/publish_dashboard.sh
```

This builds the dashboard and copies it to the repo-root `dashboard/` directory that the site serves. The build first runs the configured throughput generators in `skills/project-ltp/dashboard/throughput.config.json`.

For the bundled Second Renaissance projects, committed semantic changes to the canonical model at `ltp/ltp-model.yaml` are automatically attributed to the 2R Research Circle. Stable entity IDs created, updated, or deleted count once per mainline revision; formatting-only changes do not count. The generated weekly totals, operation breakdown, revision hashes, and affected IDs are written to `public/projects/2r-research-circle/throughput.yaml`. The initial model commit is a zero baseline rather than throughput.

## Linking to a project or a tree

The open project and view are held in the URL, so any screen can be linked to directly — in an issue, a talk, or a message that says "look at this branch of the reality tree". The published site serves the dashboard as a single file, so the address is a hash on `/dashboard/index.html`:

| Link | Opens |
|------|-------|
| `/dashboard/index.html#/` | the project picker |
| `/dashboard/index.html#/second-renaissance` | that project's overview |
| `/dashboard/index.html#/second-renaissance/current-reality` | its Current Reality Tree |

The first segment is the project's `slug` in `projects/manifest.json`; the second is the view id used in `model.yaml` — `goal-tree`, `current-reality`, `evaporating-cloud`, `future-reality`, `prerequisite-tree`, or `transition-tree`. A link to a tree the project has not modelled opens its overview instead, and an unknown project slug lands on the picker, so an out-of-date link degrades rather than breaking. The address bar updates as you move around, so a link can just be copied from it, and Back and Forward walk the views visited.

## Local single-project dashboard

For any project containing `ltp/ltp-model.yaml`, run the local read-only server (it live-reloads as you edit the model):

```bash
python skills/project-ltp/scripts/serve_dashboard.py --project /path/to/project --open
```

The server prefers port `8765`. If that port is occupied and `--port` was not specified, it automatically tries the next available port and prints the URL it selected. Pass `--port 9000` when an exact port is required.

To explore the bundled remote-work toy fixture:

```bash
python skills/project-ltp/scripts/serve_dashboard.py \
  --project skills/project-ltp/evals/fixtures/dashboard --open
```

The server binds to `127.0.0.1`, exposes only the known model files and bundled interface, and does not write to the analysed project.

## How to use the graphical interface

1. Start on **Overview** to follow the current constraint → next move → expected shift. Select any card to inspect its evidence and reasoning.
2. Use the top navigation to switch between the Goal, Current Reality, Evaporating Cloud, Future Reality, Prerequisite, and Transition views. A disabled view has not yet been modelled in `ltp/ltp-model.yaml`.
3. Pan or zoom the canvas, use the minimap for orientation, and drag nodes into a temporary arrangement. Layout changes are view-only and are not saved.
4. Select a node to open its status, confidence, reasoning, source evidence, assumptions, causal connections, and membership in other views.
5. Open **Refine** to filter nodes by evidence status and confidence. Open **How to read this** for the status legend.
6. When a real `ltp/throughput.yaml` exists, use the Overview metrics and trend disclosure to inspect goal throughput and supporting flow signals. Git-derived node throughput also shows created, updated, and deleted totals plus the revisions and entity IDs that produced them. The dashboard intentionally shows no made-up metrics when that file is absent.

The dashboard polls the YAML files and refreshes after changes. To revise the analysis, ask Codex to update the canonical files under `ltp/` (or edit them in an editor); the browser itself remains read-only. Stop the server with `Ctrl+C` in the terminal that launched it.
