---
created: 2026-09-18
status: active
owner: Rufus
---

# Plan — Explainers v2: short illustrated chapters

The current explainers are five long (2,000+ word) scroll-driven pieces. Several readers have said they don't really work. This plan replaces them with short chapters in the manner of [Co-Star's astrology 101](https://www.costarastrology.com/how-does-astrology-work): static text, illustrations (still or looping) between paragraphs, one or two points per chapter, chapters linked into a series.

State lives in **beads** (`bd list --label explainers-v2`), not in this file. This file says what the work is and why it is in this order. Scheduled sessions execute it (see [Runner](#runner)).

## Diagnosis

- **Form.** Scroll-driven drawings are fragile (mobile collisions, stale assets, pinned graphics fighting the text) and ask a lot of the reader. Readers report them as not functional.
- **Length.** Each piece carries five or six ideas. Co-Star chapters carry one, at ~300 words, and the series carries the rest.
- **Scripts.** The prose is in a literary, aphoristic register ("people leave rooms", "run without any of its vocabulary"). When Rufus rewrote the 2R talk script by hand on 2026-09-04 he consistently pulled the other way: plainer, "we", explicit, lineage named, AI named as the enabler. See [`voice-guide.md`](../../explainers/_process/series/voice-guide.md).
- **Story.** It is not yet settled what arc the illustrated introduction should follow — how closely to follow the book (Dettmer, *The Logical Thinking Process*, in `library/`), and how the Second Renaissance case relates to the LTP basics. This is the decision the whole series rests on, so it is the one human gate.

## Decisions

| Decision | Choice |
|---|---|
| Form | Short chapters, Markdown pages on Flowershow (editable in the browser), static text column, SVG illustrations inline or as `<img>`; some illustrations loop (SMIL/CSS animated SVG). **No scroll-driven logic.** Each chapter ends with a next-chapter card and an all-chapters list; the series index is a numbered list of one-line teasers. |
| Chapter size | One or two points; roughly 300–600 words. |
| Voice | [`voice-guide.md`](../../explainers/_process/series/voice-guide.md), derived from Rufus's talk rewrite. Every script is checked against it. |
| Focus | Two things: the LTP basics (following the book more closely) and the Second Renaissance story. The other trilogy pieces are source material, not targets. |
| Order | Finish the simple 2R piece → evaluate → settle the arc → scripts → form → build chapters → retire the long pieces. Don't do everything at once. |
| Old pieces | Retire: move to `explainers/_archive/`, exclude from the site, redirect their URLs if Flowershow supports it. Not many readers yet, so URL stability doesn't matter. |
| Autonomy | Cloud sessions work on the `claude/explainers-v2` branch and open a draft PR; Rufus merges to `main` (the live site). One gate: Rufus approves the arc (closed 2026-09-19). Everything else proceeds and is reviewed after. |
| Scheduler | Scheduled cloud routines (one-shot, created with the `schedule` skill) running Opus. Each session works through ready beads until none are left, then exits. The original local launchd runner was dropped on 2026-09-19: it could not authenticate unattended. |

## Phases

The beads issues carry the detail and acceptance criteria. In order:

1. **Finish the simple 2R piece** (`explainers/second-renaissance-plain/`) — voice pass, fold in what the talk (`talk/2r-research-group/script.md`) worked out since, fix the figure defects (#17), make it the lead 2R piece on the index.
2. **Evaluate** — a short note on what the finished piece teaches about length, form and voice, and what should carry into the series.
3. **Chapter form** — template, next/all-chapters nav, series index, one animated illustration as proof. Prototyped on a section of the 2R piece. Runs in parallel with the arc.
4. **Arc** — the overall story of the illustrated introduction: reader, takeaways, chapter list with the one or two points each makes, mapping to the book, what is kept or dropped from the current pieces, how 2R relates. Independent critique, revision, then **Rufus approves (gate)**.
5. **Decompose** — once the arc is approved, one script bead and one build bead per chapter.
6. **Scripts** — per chapter: draft → independent critique → revise, against the voice guide. Stage discipline from `skills/scrollable-explainer/SKILL.md` §1.5 still applies: script judged as writing before any visual work.
7. **Build chapters** — per chapter: illustrations and page, checked on the preview at desktop and phone width.
8. **Retire the long pieces and close out** — archive, redirects, index and nav, changelog entry.

## Runner

Scheduled cloud routines, named "Explainers v2 — continue (n of m)". Each one clones `origin/main`, installs `bd` (or reads `.beads/issues.jsonl` directly), and works through ready beads with [`session-prompt.md`](../../scripts/explainer-loop/session-prompt.md) plus the cloud differences in the routine's own prompt.

- Work goes on the `claude/explainers-v2` branch with a draft PR to `main`; sessions never push to `main` and have no preview site.
- A session stops at once if the only work left is behind a `human` gate.
- List routines and check runs with the `RemoteTrigger` tool (`list`, `list_runs`, `get_run_log`), or on claude.ai; add more with the `schedule` skill.

Useful checks:

```sh
bd ready --label explainers-v2                                              # what's next
bd list --label human --status open                                         # waiting on Rufus
```
