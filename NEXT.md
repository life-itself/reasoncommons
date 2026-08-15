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

**[#6 — Finalise the trilogy](https://github.com/life-itself/reasoncommons/issues/6).**
Polish on the three existing pieces: a browser bug pass, portrait mobile layouts
for pieces 2–3, and wiring the real Organic design tokens into the scroller.

The browser bug pass is the main item and genuinely needs a browser — reading
source and checking HTTP responses is how the raw-markup figure bug survived in
piece 1 until someone looked at the page.

## Sequencing

Start both at once. Two constraints:

1. **Rufus decides the diagram register** (current clean style vs a paper-collage
   art-direction pass) *before* the Organic token wiring in #6 — changing the
   register changes the styling that work depends on.
2. **#7 stage 3 comes after #6's token work lands**, so the new piece inherits
   the final look rather than being restyled twice. Stages 1–2 of #7 have no
   such dependency and should start immediately.
