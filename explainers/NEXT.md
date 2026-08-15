---
title: Explainer series — where we are, what's next
created: 2026-08-15
status: checkpoint
---

# Thinking in Systems — status and next steps

Checkpoint for review. Written after shipping markdown articles alongside the scrolling
HTML for all three parts. Read this, then decide what happens next — the two lists below
split work into what needs your judgment and what I can just go and do.

## What exists right now

Every part ships in **two forms**, same words:

| | Article (markdown, static) | Scrolling (HTML, animated) |
|---|---|---|
| 1 · The Wrong Queue | `01-bottleneck/article.md` | `01-bottleneck/index.html` |
| 2 · The Arrows Nobody Checks | `02-thinking-made-visible/article.md` | `02-thinking-made-visible/index.html` |
| 3 · Five Shapes | `03-five-shapes/article.md` | `03-five-shapes/index.html` |

`explainers/index.html` lists both for each part. Both formats read from the same
finalised prose (each script went through: draft → self-critique → **independent
fresh-agent critique with no authorship context** → revision — piece 1 twice, after the
independent critic caught an arithmetic error that didn't check out).

The markdown follows the pattern already proven live on this site by `story/draft.md`:
inline `<svg>` figures with `<figure>`/`<figcaption>`, no `<script>`. The HTML pages use
the same drawing logic but generated at runtime via JS and `IntersectionObserver` for the
scroll-driven reveal (`explainers/scroller.js`, `scroller.css`).

Reference material, in case useful again: `skills/scrollable-explainer/` — a general
write-up of the scroll-driven-explainer form, with a full measured teardown of a ProPublica
piece as the worked case study. Not specific to this project.

## Open questions — need your judgment

1. **Format.** Do we keep publishing both forms long-term, or is the markdown article
   actually the better default and the HTML scrollers become a "for fun" secondary link?
   My instinct after building both: the markdown reads *fine* — the argument doesn't
   depend on the animation — but I built it, so take that with a grain of salt.
2. **Read it as a reader, not as review-of-critiques.** I've read these pieces so many
   times editing them that I can no longer tell if they're actually good or just
   internally consistent. Worth reading `01-bottleneck/article.md` cold, ideally on a
   day you haven't been staring at this project.
3. **`story/` ("What Counts").** Still live, still linked in nav, still the old
   Second-Renaissance-flavoured piece this whole effort was meant to replace. Retire it,
   keep it alongside, or fold its "reconstructed forum thread" device into something
   else? Untouched pending this decision.
4. **How much more to invest in the drawings.** They're clean SVG diagrams — boxes,
   arrows, a counter — not the ProPublica reference's naive paper-collage illustrated
   world. That was a deliberate corner cut to get all three shipped. Worth a second pass
   with real art direction, or is diagram-clean actually the right register for this
   subject matter (more textbook, less magazine)?
5. **Does Flowershow actually render these as intended?** I've only checked in a
   standalone browser. I can't run your Flowershow build from here — the front matter,
   the `article.md` vs `index.html` routing at the same path, and whether inline SVG
   survives Flowershow's markdown pipeline the same way it does in `story/draft.md` all
   need a real look at the deployed site, not just my local judgement.

## What I can take on next, if you want it

Roughly in priority order:

1. **Portrait mobile layout for pieces 2 and 3.** Piece 1's five-station diagram got a
   proper stacked portrait layout after I found the desktop version collapsed to an
   unreadable ribbon on a phone. Pieces 2 and 3 still use their landscape diagrams on
   mobile — legible, but small, same fix needed (roughly 8 more diagrams' worth of work).
2. **No-JS fallback for the scrolling HTML pages.** With JavaScript disabled, part 3's
   page currently renders **completely empty** — every drawing is built at runtime. Part
   1 keeps only its one hand-coded (non-generated) drawing. This mattered more before we
   had the markdown fallback; now that the article versions cover the no-JS case, it's
   lower priority, but the HTML pages are still broken on their own terms if that's ever
   meant to be a real bar.
3. **Wire the Organic design system.** The scroller currently uses its own ad hoc palette
   (close to, but not actually, the tokens in `story/_ds/`). Swapping to the real
   cream/terracotta/sage/Caprasimo tokens would make this feel like one site rather than
   two aesthetics.
4. **Update the stale ledger.** `docs/plans/2026-08-14-ltp-explainer-trilogy.md`'s
   position marker still describes an earlier stage of the process (pre-restructure into
   script → critique → visual → build). Worth a pass to make it match reality, or retiring
   it in favour of this file.
5. **A fourth teardown for the skill**, if another scroll-driven explainer piece worth
   studying turns up — the reference doc is built to take more case studies.

## What I'd suggest doing at this checkpoint

Read the two markdown articles for pieces 1 and 3 end to end (2 is probably fine if 1 is),
look at the live site if you can get a build running, and tell me: keep both formats or
pick one, and what's next from the list above. Everything else waits on that.
