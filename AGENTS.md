# AGENTS.md

Guide for AI agents (Claude Code, Codex, etc.) working in this repo. `CLAUDE.md` is a symlink to this file.

## What this is

Logical Thinking Process (LTP) / Issue Tree app — a tool to decompose a top-level claim into a tree of sub-claims and accumulate evidence (annotations from source docs) against that stable tree scaffold. Collaboration of Rufus Pollock + David Joseph.

## Where to look

| Need | File |
|------|------|
| Project overview + references | `README.md` |
| Why this matters + problem framing (SCQH) | `MOTIVATION.md` |
| Plan of work — streams, next actions, verification | `PLAN.md` |
| Process spec + **gold-standard toy fixture** (tree, doc, annotations) | `claim-tree-annotation.md` |
| Static animated demo of the 4-step vision | `claim-tree-annotation-demo/` |
| AI skills (tree-gen, annotation-mapping, project-ltp) | `skills/` (see `skills/README.md`) |
| **Writing a scrolling visual explainer** — principles, patterns, worked teardown | `skills/scrollable-explainer/SKILL.md` — **read before drafting anything in `explainers/`** |
| The explainer series itself (drafts, beat sheets) | `explainers/` · plan in `docs/plans/2026-08-14-ltp-explainer-trilogy.md` |

## Conventions

- **Skills** live in top-level `skills/<name>/` so they're usable outside Claude Code (e.g. Codex). `.claude/` is gitignored (local-only, see `.gitignore`), so to let Claude Code discover them, wire the symlinks locally:
  ```sh
  mkdir -p .claude/skills
  ln -s ../../skills/tree-gen .claude/skills/tree-gen
  ln -s ../../skills/annotation-mapping .claude/skills/annotation-mapping
  ln -s ../../skills/project-ltp .claude/skills/project-ltp
  ```
- **Codex skills** are discovered under `.agents/skills/`. The repository tracks
  `.agents/skills/project-ltp` as a symlink to the same canonical
  `skills/project-ltp/` directory, so edits stay shared between Claude Code and
  Codex. In the Codex app, invoke it explicitly with `$project-ltp` or let its
  description trigger it automatically. Restart Codex if a newly added skill
  does not appear in the Skills sidebar.
- **Toy example first.** Validate any AI skill against the gold data in `claim-tree-annotation.md` before touching real applications (e.g. Second Renaissance).
- Keep `MOTIVATION.md` (why + SCQH) and `PLAN.md` (plan of work) current; both are referenced from `README.md`.
