---
title: Where we are, what's next
created: 2026-08-15
updated: 2026-08-16
status: checkpoint
---

# Next steps

Four explainers are written and built, all shipping as scrolling HTML only
(decided 2026-08-16 — the scroller is the better read, and maintaining each piece
twice cost a sync on every edit). The **Thinking in Systems** trilogy is finished
(#6). The Second Renaissance piece — the first to run the method on a real problem
rather than an invented clinic — has been rewritten from a blank page as
**Somewhere to Put It**, per the plan in
[#9](https://github.com/life-itself/reasoncommons/issues/9) /
[`docs/plans/2026-08-16-second-renaissance-narrative.md`](docs/plans/2026-08-16-second-renaissance-narrative.md).
Its stage files are `05-script.md` → `08-visual-script.md` in
`explainers/_process/second-renaissance/`; `01`–`04` are the superseded first pass,
kept for the record. What shipped is in [`changelog.md`](changelog.md).

## Open — Somewhere to Put It

1. **The ending promises a protocol that does not exist.** The piece is honest about
   this — it says so in as many words, and the merge rules are described as three
   sentences that have never been tested. That is a defensible tense for one piece.
   It stops being defensible if a year passes and the protocol still isn't built.
2. **Show it to the Second Renaissance core before an SR-wide link.** Not for
   clearance — nothing in it is quoted — but because it makes a public argument about
   how the group should change its mind, and springing that on people would be a poor
   opening move for a piece about not acting unilaterally.
3. **Robert and David have not seen *Whose Map Is It*, and it is now live.** The
   first pass at this material — the real June episode, the two rival definitions —
   is published at `explainers/whose-map-is-it/` as the deeper cut, linked from the
   series index and from *Somewhere to Put It*. It condenses quotes from their actual
   forum posts. **This is the most pressing open item on the page**, and it got more
   pressing when the piece acquired a URL: show it to them. If they object to being
   quoted, the fix is small — unpublish or paraphrase — but it should not wait for
   them to find it.

**The fate of `story/`.** #7 said shipping this piece supersedes `story/draft.md` —
same material, better form. The rewrite has moved further away from `story/draft.md`
still. Undecided.

## Worth knowing for any further work on these pages

They are checked by driving them in a real browser at 1280×800 and 390×844,
stepping through every trigger and looking at the result. Most of what has been
wrong — captions covering the thing they pointed at, boxes running off the edge of
their own drawing, a whole stage letterboxed into the middle third of the frame —
was invisible from the source. Do the same before calling any change finished.

A scripted pass helps and is cheap to rebuild: drive the page with `playwright-core`
against the installed Chrome, step each `.trigger`, and per step measure (a) the
union of visible SVG elements against the `<svg>` box, which catches drawings
running off their own canvas, and (b) each visible element against the active
caption's rect, which catches captions sitting on ink. That found five real defects
on this piece — a clipped map, text overflowing its card, a crack drawn through its
own label, an arrowhead landing on a name, portrait arrows pointing the wrong way —
but it does not replace looking: the fan of arrowheads converging into a smudge, and
5px labels in a thumbnail, only showed up in the screenshots.
