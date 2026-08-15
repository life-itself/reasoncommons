---
created: 2026-06-06
status: in-progress
---

# Reason Commons

*Structure claims into trees. Map evidence to them. Grow shared understanding — together.*

Public argument is badly structured: claims are vague, debate doesn't accumulate, and evidence rarely maps to the specific point it bears on. What if a claim were instead a tree — broken into the sub-claims it actually depends on, with evidence for, against, or complicating each one attached directly to it? The tree becomes a shared, inspectable scaffold that outlives any one document, so a group reasoning about the same question can see where things stand and build on each other's work instead of talking past each other.

That's what we're exploring here: not one person's argument, but claims and evidence held in common — open to challenge, open to revision.

<div class="demo-cta">
  <a href="explainers/index.html" class="btn-primary btn-primary-lg">
    Read the series
  </a>
  <a href="dashboard/index.html" class="btn-primary btn-primary-lg">
    Open the Project LTP dashboard
  </a>
  <a href="alignment/index.html" class="btn-primary btn-primary-lg">
    Try Goal Aligner
  </a>
  <a href="story/index.html" class="btn-primary btn-primary-lg">
    Read “What Counts”
  </a>
  <a href="claim-tree-annotation-demo/index.html" class="btn-primary btn-primary-lg">
    Explore the claim tree annotation demo
  </a>
</div>

**Key docs:** [motivation.md](motivation.md) — why this matters + problem framing (SCQH) · [AGENTS.md](AGENTS.md) — guide for AI agents. Planning (streams, next actions) happens in [GitHub issues](https://github.com/life-itself/reasoncommons/issues).

## Use Project LTP with Codex

This repository exposes the canonical `skills/project-ltp/` workflow to Codex
through `.agents/skills/project-ltp`. Open the repository in Codex, then either:

- open **Skills** in the sidebar and choose **Project LTP**; or
- mention it in a prompt, for example:

  ```text
  Use $project-ltp to reconcile this repository with its open GitHub issues,
  recommend the single highest-leverage next action, and open the local
  dashboard.
  ```

Codex may also select the skill automatically for requests about LTP trees,
project constraints, causal analysis, or plan/code reconciliation. If the skill
does not appear immediately after checkout, restart Codex.

## Project LTP dashboard

Project LTP analyses are explored in a read-only dashboard that opens with the
current constraint, next action, expected effect, and any defined throughput
signals; the six LTP trees, evidence, assumptions, and filters are available on
demand.

### Published multi-project dashboard

The site publishes the dashboard at [`/dashboard/`](dashboard/index.html) with a
project picker, so several analyses live in one place. Each project is a static
model under `skills/project-ltp/dashboard/public/projects/<slug>/model.yaml`,
listed in `public/projects/manifest.json`. To add a project, drop its
`ltp-model.yaml` (and optional `throughput.yaml`) under a new slug, add a
manifest entry, then build and publish:

```bash
sh skills/project-ltp/scripts/publish_dashboard.sh
```

This builds the dashboard and copies it to the repo-root `dashboard/` directory
that the site serves. The build first runs the configured throughput generators
in `skills/project-ltp/dashboard/throughput.config.json`.

For the bundled 2R projects, committed semantic changes to the canonical
Second Renaissance model at `ltp/ltp-model.yaml` are automatically attributed
to the 2R Research Circle. Stable entity IDs created, updated, or deleted count
once per mainline revision; formatting-only changes do not count. The generated
weekly totals, operation breakdown, revision hashes, and affected IDs are
written to
`public/projects/2r-research-circle/throughput.yaml`. The initial Second
Renaissance model commit is a zero baseline rather than throughput.

### Local single-project dashboard

For any project containing `ltp/ltp-model.yaml`, run the local read-only server
(it live-reloads as you edit the model):

```bash
python skills/project-ltp/scripts/serve_dashboard.py --project /path/to/project --open
```

The server prefers port `8765`. If that port is occupied and `--port` was not
specified, it automatically tries the next available port and prints the URL it
selected. Pass `--port 9000` when an exact port is required.

To explore the bundled remote-work toy fixture:

```bash
python skills/project-ltp/scripts/serve_dashboard.py \
  --project skills/project-ltp/evals/fixtures/dashboard --open
```

The server binds to `127.0.0.1`, exposes only the known model files and bundled
interface, and does not write to the analyzed project.

### How to use the graphical interface

1. Start on **Overview** to follow the current constraint → next move → expected
   shift. Select any card to inspect its evidence and reasoning.
2. Use the top navigation to switch between the Goal, Current Reality,
   Evaporating Cloud, Future Reality, Prerequisite, and Transition views. A
   disabled view has not yet been modelled in `ltp/ltp-model.yaml`.
3. Pan or zoom the canvas, use the minimap for orientation, and drag nodes into
   a temporary arrangement. Layout changes are view-only and are not saved.
4. Select a node to open its status, confidence, reasoning, source evidence,
   assumptions, causal connections, and membership in other views.
5. Open **Refine** to filter nodes by evidence status and confidence. Open
   **How to read this** for the status legend.
6. When a real `ltp/throughput.yaml` exists, use the Overview metrics and trend
   disclosure to inspect goal throughput and supporting flow signals.
   Git-derived node throughput also shows created, updated, and deleted totals
   plus the revisions and entity IDs that produced them. The dashboard
   intentionally shows no made-up metrics when that file is absent.

The dashboard polls the YAML files and refreshes after changes. To revise the
analysis, ask Codex to update the canonical files under `ltp/` (or edit them in
an editor); the browser itself remains read-only. Stop the server with
`Ctrl+C` in the terminal that launched it.

## About

Reason Commons is a collaboration between **Rufus Pollock** and **David Joseph**. Rufus's thread: issue trees, SCQH, Minto pyramids — wanted a tool like this for 10+ years. David's thread: "Abductio," a proposition-decomposition process inside his Promise Protocol framework.

Related: [Promise Foundation](https://www.promise.foundation/how-it-works) · [Provisio](https://praevisio.promise.foundation/) · [issuetrees.com](https://issuetrees.com)
