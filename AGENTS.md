# AGENTS.md

Guide for AI agents (Claude Code, Codex, etc.) working in this repo. `CLAUDE.md` is a symlink to this file.

## What this is

Logical Thinking Process (LTP) / Issue Tree app — a tool to decompose a top-level claim into a tree of sub-claims and accumulate evidence (annotations from source docs) against that stable tree scaffold. Collaboration of Rufus Pollock + David Joseph.

## Where to look

| Need | File |
|------|------|
| Project overview + references | `README.md` |
| Why this matters + problem framing (SCQH) | `motivation.md` |
| Planning — streams, next actions | [GitHub issues](https://github.com/life-itself/reasoncommons/issues) |
| Process spec + **gold-standard toy fixture** (tree, doc, annotations) | `claim-tree-annotation.md` |
| Static animated demo of the 4-step vision | `claim-tree-annotation-demo/` |
| AI skills (tree-gen, annotation-mapping, project-ltp) | `skills/` (see `skills/README.md`) |
| **Writing a scrolling visual explainer** — principles, patterns, worked teardown | `skills/scrollable-explainer/SKILL.md` — **read before drafting anything in `explainers/`** |
| The explainer series itself | `explainers/` — see its layout under Conventions below |

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
- Keep `motivation.md` (why + SCQH) current; it's referenced from `README.md`. Plan-of-work tracking (streams, next actions) lives in GitHub issues, not a repo file.
- **`explainers/` layout.** Only finished, readable pieces live at the top level;
  everything else is process material and stays out of the way:
  ```
  explainers/
    index.md                     series landing page
    <nn>-<slug>/
      index.md                   the article — the canonical published piece
      scrolling.html             scroll-driven version of the same piece
    _process/<nn>-<slug>/        scripts, critiques, superseded drafts, stills
    scroller.css, scroller.js    shared assets for the scrolling versions
  ```
  `_process/` is in `config.json` > `contentHide` so Flowershow doesn't publish
  it. Drafts and critiques go there, never next to the article.
- There is exactly one `NEXT.md`, at the repo root. Don't create per-folder ones.
- Root docs are lowercase (`motivation.md`, `changelog.md`) so Flowershow gives them clean published URLs — except `README.md` and `AGENTS.md`, which keep their exact uppercase names because tooling (GitHub, Flowershow's homepage, Claude Code/Codex) looks them up by that literal filename.

## Changelog

This repo keeps a `changelog.md` (dated entries, newest first). At the end
of a work session, if something worth recording actually shipped — skip
trivial sessions (typo fixes, dead ends, no visible outcome) — draft a
dated entry. Screenshots go in `changelog/images/`, embedded inline, if
something visual shipped. First time writing an entry in this repo, or if
the format is unclear: fetch and follow
https://raw.githubusercontent.com/life-itself/changelog/main/CONVENTION.md
