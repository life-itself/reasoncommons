---
created: 2026-06-06
status: in-progress
---

# Reason Commons

*Logical Thinking Process (LTP) / Issue Tree tooling — see [docs/brand-and-domain-naming.md](docs/brand-and-domain-naming.md) for the naming decision.*

Collaboration of Rufus Pollock with David Joseph to build tooling for structured thinking — specifically a Logical Thinking Process (LTP) / Issue Tree app. Both David and Rufus share a long-standing desire to improve public discourse and improve collaboration: aligning efforts to goals, making claims or hypotheses and their logical structure clearer (claim-trees), allowing debate to accumulate, mapping evidence clearly to specific sub-claims.

**Core shared vision:** Patterns and tooling where you take a top-level claim, recursively decompose it into sub-claims, and build a directed graph (DAG) of claims + evidence. Enables "cathedral building" where discourse actually accumulates rather than being scattered across forum posts.

<div class="demo-cta">
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

**Key docs:** [MOTIVATION.md](MOTIVATION.md) — why this matters + problem framing (SCQH) · [AGENTS.md](AGENTS.md) — guide for AI agents. Planning (streams, next actions) now happens in [GitHub issues](https://github.com/life-itself/reasoncommons/issues).

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

David's angle: his "Abductio" process for proposition decomposition — takes any claim, breaks into subclaims until confidence threshold is met. Built into his Promise Protocol framework.

Rufus's angle: issue trees / SCQH / Minto pyramids — wanted an app for this for 10+ years. Previously almost built one 3–4 years ago.

**First shared experiment:** Create a LTP for Second Renaissance (theory of constraints / prerequisite tree).

**Communication channel:** Second Renaissance Discord sub-channel.

## References

- Meeting notes (Jun 6, 2026): https://docs.google.com/document/d/1UEEZSlEMlOlsDxiQOR5WIfxbiQ7Mlw7nw060j_1jqcM/edit
- David's LTP project: https://stitch.withgoogle.com/projects/3568286358932959093
- David's "Signs of Change": https://drive.google.com/file/d/1hAKIH8aCyS_xk5mFlFWNZ_cvF4yteF30/view
- Promise Foundation: https://www.promise.foundation/how-it-works
- Provisio (David's AI risk/promise app): https://praevisio.promise.foundation/
- issuetrees.com (Rufus's site): https://issuetrees.com

## Next Steps

- [x] Create Discord channel for LTP collaboration **✅2026-06-06 - new channel in 2R server**
- [x] Begin with AI skill development for claim tree generation
- [x] Build a minimal local Project LTP tree and throughput viewer on the toy fixture
- [ ] Test with Life Itself research group as initial use case

### 1. Write up background post on Rufus's interest in structured thinking
- [ ] Get transcript / recording from Jun 6 conversation with David
- [ ] Locate written material shared with David in that session
- [ ] Find old issue tree diagrams
- [ ] Draft post synthesising background + personal story

### 2. Create diagram of four steps for the app
- [ ] Sketch the four-step process Rufus has in mind for the app
- [ ] Produce clean diagram (Mermaid or similar) to share with David

### 3. Create shared repo for ideas collaboration
- [ ] Set up GitHub repo for LTP / issue tree app ideas
- [ ] Invite David as collaborator

### 4. Setup Discord bot for Second Renaissance channel
- [x] Set up bot to monitor the LTP collaboration Discord sub-channel **✅2026-06-23 - setup done, not doing anything yet**
- [ ] Configure summaries / updates to feed into workplan

### 5. Sketch simple website demo (4 steps)
- [x] Rufus to produce sketch of demo site showing the four-step flow: **[claim tree annotation demo](claim-tree-annotation-demo/index.html)**
  1. Material (input) → 2. Tree (claim decomposition) → 3. Related doc → 4. Annotation
