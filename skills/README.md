# Skills

AI skills for the LTP / Issue Tree app. Kept here (top-level, not inside a
runtime-specific directory) so the canonical skill can be shared by Claude
Code and Codex.

- Claude Code: symlink a skill into the gitignored `.claude/skills/<name>`.
- Codex: symlink a skill into `.agents/skills/<name>`. This repository tracks
  `.agents/skills/ltp-project` (and the deprecated `.agents/skills/project-ltp`)
  so they appear in the Codex Skills sidebar and can be invoked with
  `$ltp-project`.

## Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| `tree-gen/` | Input claim/question → claim tree (Stream 1a) | v0.1 — verified vs gold on the toy claim, see `tree-gen/VERIFICATION.md` |
| `annotation-mapping/` | Source doc + tree → fragments mapped to nodes with relation labels (Stream 1b) | v0.1 — verified vs gold annotations (5/5), see `annotation-mapping/VERIFICATION.md` |
| `ltp-project/` | Document, repository, plan, issue export or notes → a Reason Commons `*.ltp.yaml` project file (the interchange document the app imports, and exports as JSON or YAML with history), plus a report of every judgment call | unified 2026-09-06 — **mirror**; the canonical copy is `Promise-Foundation/reason-commons` `.claude/skills/ltp-project/`, keep the two byte-identical (`diff -r`) |
| `project-ltp/` | **Deprecated 2026-09-06** — its `ltp-model.yaml` format cannot be imported into Reason Commons. Kept only for the read-only dashboard over the legacy models still bundled on the site, and its build scripts | superseded by `ltp-project/`; GitHub issue sync is now the Reason Commons projection's job |
| `scrollable-explainer/` | Principles + patterns for writing and building long-form scroll-driven visual explainers, with a measured teardown of the ProPublica CCS piece as the worked case study | v0.1 — reference only (no code); read before drafting in `../explainers/` |
| `contribution-proposals/` | A batch of raw participant contributions (Google Doc export, form dump, pasted notes) + a target `ltp-model.yaml` → one reviewable proposal per contribution for how it might extend, support, challenge, or fail to fit the model, rendered as a self-contained page a room clicks through live — accept, edit, reject — watching the tree change. Never merges | v0.1 — renderer verified end to end in a browser against the real 2R model; the *reading* is untested on contributions it did not write, see `contribution-proposals/VERIFICATION.md` |
| `goal-alignment/` | Two LTP models (an individual/smaller-group one + a collective one) → reviewable, human-confirmed suggestions for where the first could advance the second — never auto-merged | pilot #1 — toy example only, see `goal-alignment/VERIFICATION.md`; the `IO-5` AI-vs-steward comparison it enables has not yet run |

The canonical **tree JSON schema** is defined in `tree-gen/SKILL.md`; `tree-gen/gold/remote-work.tree.json` is the gold fixture (extracted from `../claim-tree-annotation.md`) that also seeds 1b and 1c.

Each is validated against the gold-standard toy case in `../claim-tree-annotation.md` (remote-work productivity). See each skill's own `VERIFICATION.md` for its pass criteria.
