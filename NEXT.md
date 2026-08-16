---
title: Where we are, what's next
created: 2026-08-15
updated: 2026-08-16
status: checkpoint
---

# Next steps

The **Thinking in Systems** trilogy is written and built, and ships as scrolling
HTML only (decided 2026-08-16 — the scroller is the better read, and maintaining
each piece twice cost a sync on every edit). What shipped is in
[`changelog.md`](changelog.md).

Two streams. **They can run in parallel** — they touch different files — with one
ordering constraint noted at the bottom.

## Opus work

**[#7 — Second Renaissance explainer](https://github.com/life-itself/reasoncommons/issues/7).**
A sibling to the trilogy, applying the LTP to SR itself, readable cold, that we
can hand to someone in the SR initiative to motivate them. Built on the real SR
trees in `docs/ltp_trees/` and the `story/draft.md` forum reconstruction.

Start here, at stage 1: write the script, critique it adversarially, revise.
Read the issue and `skills/scrollable-explainer/SKILL.md` first, and show the
script before going further. This is the bigger and more valuable of the two
streams.

Stages 1 and 2 (script, then visual script) are Opus. Stage 3 (build) is Sonnet
work against the approved visual script.

## Sonnet work

**[#6 — Finalise the trilogy](https://github.com/life-itself/reasoncommons/issues/6)
— done 2026-08-16.** All four remaining items are in: the browser bug pass,
portrait layouts for pieces 2–3, the Organic design tokens, and the stale
position marker in the plan doc. See [`changelog.md`](changelog.md).

Worth knowing for future work on these pages: they were checked by driving them
in a real browser at 1280×800 and 390×844, stepping through every trigger and
looking at the result. Most of what was wrong — captions covering the thing they
pointed at, boxes running off the edge of their own drawing — was invisible from
the source. Do the same before calling any change to them finished.

## Carried over from #6

Two things that were never build work and outlived the issue:

- **Read part one cold**, as a reader rather than an author, to check the prose
  still lands. `explainers/_process/01-bottleneck/article.md` is the final
  prose. This one is Rufus's, not an agent's.
- **The fate of `story/`.** Left in place. #7 supersedes `story/draft.md`, so
  decide it there rather than here.

## Sequencing

**#7 stage 3 is now unblocked** — the token work has landed, so a new piece
built against `explainers/scroller.css` inherits the final look. Stages 1–2 of
#7 are the remaining work.
