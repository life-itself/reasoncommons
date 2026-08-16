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
(#6) and **Whose Map Is It** (#7) — the Second Renaissance piece, the first to run
the method on a real problem rather than an invented clinic — is built, with its
three stage files in `explainers/_process/second-renaissance/`. What shipped is in
[`changelog.md`](changelog.md).

## Open — Whose Map Is It

**Read it end to end and decide whether to hand it to anyone.** It was written to
be given to someone inside the Second Renaissance, and it quotes Robert and David
at length from the forum. Nobody outside this repo has seen it. Two things first:

1. **The quotes.** Condensed from real posts. Robert and David should see it
   before an SR-wide link does — the piece is *about* not changing a shared map
   unilaterally, so publishing it unilaterally would be a poor opening move.
2. **The ending.** It closes on a protocol that does not exist yet: how a proposal
   enters the map, who hears the objections, who merges. If that is not going to
   be built, the ending is a promise the initiative cannot keep.

**The fate of `story/`.** #7 said shipping this piece supersedes
`story/draft.md` — same material, better form. Now live, still undecided.

## Carried over

- **Read part one cold**, as a reader rather than an author, to check the prose
  still lands. `explainers/_process/01-bottleneck/article.md` is the final prose.
  This one is Rufus's, not an agent's.

## Worth knowing for any further work on these pages

They are checked by driving them in a real browser at 1280×800 and 390×844,
stepping through every trigger and looking at the result. Most of what has been
wrong — captions covering the thing they pointed at, boxes running off the edge of
their own drawing, a whole stage letterboxed into the middle third of the frame —
was invisible from the source. Do the same before calling any change finished.

## Not started

- The update protocol itself — the thing the explainer ends by asking for.
- Applying `skills/tree-gen` and `skills/annotation-mapping` to the real SR trees,
  which the toy fixture in `claim-tree-annotation.md` was validating for.
