# Skills

AI skills for the LTP / Issue Tree app. Kept here (top-level, not inside a
runtime-specific directory) so the canonical skill can be shared by Claude
Code and Codex.

- Claude Code: symlink a skill into the gitignored `.claude/skills/<name>`.
- Codex: symlink a skill into `.agents/skills/<name>`. This repository tracks
  `.agents/skills/project-ltp` so Project LTP appears in the Codex Skills
  sidebar and can be invoked with `$project-ltp`.

## Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| `tree-gen/` | Input claim/question → claim tree (Stream 1a) | v0.1 — verified vs gold on the toy claim, see `tree-gen/VERIFICATION.md` |
| `annotation-mapping/` | Source doc + tree → fragments mapped to nodes with relation labels (Stream 1b) | v0.1 — verified vs gold annotations (5/5), see `annotation-mapping/VERIFICATION.md` |
| `project-ltp/` | Codebase / roadmap / plan → evidence-backed causal model rendered as the six Theory-of-Constraints LTP trees (Goal, Current Reality, Evaporating Cloud, Future Reality, Prerequisite, Transition) + a single next-action recommendation + optional local read-only dashboard + GitHub Issue sync for transition-tree actions | v0.3 — dashboard, schemas, server + sync tests, toy fixture, and skill references |
| `goal-alignment/` | Two LTP models (an individual/smaller-group one + a collective one) → reviewable, human-confirmed suggestions for where the first could advance the second — never auto-merged | pilot #1 — toy example only, see `goal-alignment/VERIFICATION.md`; the `IO-5` AI-vs-steward comparison it enables has not yet run |

The canonical **tree JSON schema** is defined in `tree-gen/SKILL.md`; `tree-gen/gold/remote-work.tree.json` is the gold fixture (extracted from `../claim-tree-annotation.md`) that also seeds 1b and 1c.

Each is validated against the gold-standard toy case in `../claim-tree-annotation.md` (remote-work productivity). See `../PLAN.md` for verification criteria.
