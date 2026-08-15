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
  `_process/` is in `config.json` > `contentExclude` so Flowershow doesn't
  publish it. Drafts and critiques go there, never next to the article. Use
  `contentExclude`, not `contentHide` — `contentHide` only drops pages from the
  nav, and the URLs still resolve for anyone who guesses them.
- **No blank lines inside raw HTML in Markdown.** A blank line ends the raw HTML
  block as far as the Markdown parser is concerned. Anything after it that's
  indented four spaces or more — which inline SVG almost always is — then parses
  as an *indented code block*, and the figure renders on the page as literal
  markup. Keep `<figure>`…`</figure>` and `<svg>`…`</svg>` unbroken:
  ```html
  <figure>
  <svg viewBox="0 0 640 260" role="img" aria-label="…">
    <rect x="20" y="60" width="90" height="90"/>
    <rect x="140" y="60" width="90" height="90"/>   <!-- no blank line above -->
  </svg>
  <figcaption>Figure 1 · …</figcaption>
  </figure>
  ```
  Group the SVG with comments or `<g>` elements if you want visual separation.
  This bites silently: the page still returns 200, so it only shows up if you
  look at it. After changing any Markdown that embeds HTML, check the rendered
  output for escaped markup — `curl -s <url> | grep '&lt;rect\|&lt;svg'` should
  come back empty. Allow a moment after `fl` for the rebuild; a fetch made
  mid-rebuild can return a stale page and mislead you either way.
- There is exactly one `NEXT.md`, at the repo root. Don't create per-folder ones.
- **Preview before pushing to live.** `main` is the live site
  (`reasoncommons.com`, Flowershow site `ltp-issue-trees`) — never push to it
  just to see how something renders. Publish the working tree to a separate
  preview site instead:
  ```sh
  fl . --yes
  ```
  The target site name is committed in `.flowershow`, so this syncs only the
  changed files to https://reasoncommons-preview-rufuspollock.flowershow.me and
  the loop stays cheap: edit → `fl .` → look → repeat, landing on `main` only
  once it's right. `fl list` shows existing sites, `fl delete` removes one.
  Especially worth doing for anything that changes URLs or link structure.
  Two caveats. `fl` aborts on the tracked `.agents/skills/project-ltp` symlink,
  so move `.agents` aside for the publish and put it back after. And a preview
  is only reliable about content that *exists* — it ignores `contentExclude` and
  never deletes, so it shows pages production correctly omits. Check those
  against the live site, not the preview.
- Root docs are lowercase (`motivation.md`, `changelog.md`) so Flowershow gives them clean published URLs — except `README.md` and `AGENTS.md`, which keep their exact uppercase names because tooling (GitHub, Flowershow's homepage, Claude Code/Codex) looks them up by that literal filename.

## Changelog

This repo keeps a `changelog.md` (dated entries, newest first). At the end
of a work session, if something worth recording actually shipped — skip
trivial sessions (typo fixes, dead ends, no visible outcome) — draft a
dated entry. Match the entry's weight to what a reader would actually care
about: a real feature/fix/content gets a title, one or two sentences, and a
screenshot if something visual shipped; small stuff (cleanup, rename,
reorg, tidying) gets one plain sentence, no bullets, no screenshot — even
if several small things happened, that's still one combined sentence, not
a bullet per thing. Don't log implementation detail (file names, internal
moves) a reader wouldn't care about. First time writing an entry in this
repo, or if the format is unclear: fetch and follow
https://raw.githubusercontent.com/life-itself/changelog/main/CONVENTION.md
