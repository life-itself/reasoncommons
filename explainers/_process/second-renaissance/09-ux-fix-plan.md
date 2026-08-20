# Landing, pacing and stacked steps — UX fix plan (2026-08-20)

Reported after watching people arrive on `second-renaissance/index.html` cold.

## What was wrong

1. **No landing.** The piece opened straight into a pinned stage — a drawing, one sentence, no title, no orientation, no sign that scrolling was the interaction. The Cold Open pattern (SKILL.md §2.1) assumes a reader who arrived from a headline and already knows they are in a story; a cold link gives them none of that.
2. **The opening did not respond.** `.sticky-item` occupied a full viewport of document flow *before* the first `.trigger`, and the observer fires a step only when a trigger crosses the middle 10% band of the screen. So beat two arrived at roughly **1.45 screens** of scrolling. The first screen and a half of the piece was dead.
3. **The step blocks overwrote each other.** Each beat replaced the previous one in place, so at any moment the reader saw one sentence with no trace of what came before — no sense of a sequence unfolding.
4. **The framing came too late.** Maren's story ran before the title and before any statement of what the Second Renaissance is.

## Decisions taken

- Statement (*"A shortage of somewhere to put them."*) stays **before** Maren, as the payoff of the paragraph that builds to it. Maren then illustrates a shortage the reader has already been named.
- Pacing and stacking land in the **shared** assets; hero and nav markup go on `second-renaissance` only this pass, so one piece can be judged before the other four follow.
- Stacking is **wide-screen only**; portrait keeps one block at a time.
- Top bar **fades in after the hero** rather than sitting over it.

This gives up the Cold Open reversal, which was real — the old opening earned its turn on *"A year later, not one sentence of it has changed."* An unrecognised page beats a well-paced one nobody stays on, and the dek carries a compressed version of the same turn.

## The work

1. **Pacing** — `.sticky-item{margin-bottom:-100svh}` so the sticky stops consuming a screen ahead of its own triggers; first step change moves from ~1.45 screens to ~0.45. `.scroll-item{padding-bottom:55svh}` extends the sticky's travel so the last beat is not unpinning as it appears. Net: the dead screen moves from the head of each section, where it reads as broken, to the tail, where it reads as a hold on a finished drawing.
2. **Stacked steps** — opt-in `<div class="steps stack">`. Steps leave absolute positioning and become a left column; `scroller.js` marks every step up to and including the active one `.on`, the active one `.cur`, and dims the ones behind. Groups that do not opt in are untouched. Under 640px only `.cur` shows.
3. **Hero** — `.hero`, full viewport, kicker / title / dek, a line saying it is a scrolling piece, and a scroll cue that bobs (off under `prefers-reduced-motion`). Replaces the title card rather than adding to it.
4. **Top bar** — `.topnav`, fixed, ~44px, home link left and piece name right, faded in by an observer on the hero.
5. **Reorder** — hero → framing prose → statement → Maren (stacked) → everything downstream unchanged. No prose rewritten.

## Risks to check in preview

- Stage 1 retimes pieces nobody is looking at: read all five, watching for a last beat that now clips.
- The stacked column could collide with artwork at intermediate widths: check 1100px and 1440px.
