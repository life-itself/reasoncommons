---
created: 2026-08-14
status: in-progress
owner: Rufus
---

# Plan — The LTP Explainer Trilogy

Three NYT-style scrolling visual explainers that make the case for thinking in
trees, built in sequence. This file is the working ledger: decisions at the top,
a checkbox pipeline below, and a position marker for resumable (loop-mode) work.

## Position

> **Currently on:** Stage 1 complete for Piece 1 — script v2 at `explainers/01-bottleneck/03-script-v2.md`, critique at `02-critique.md`. Next: stage 2, visual script. Prototype `index.html` predates the restructure and will be rebuilt from the stage-2 output.




Update this line at the end of every work unit.

## Why this exists

`story/draft.md` ("What Counts") was the first attempt. It is too anchored to
Second Renaissance's internal drama — it documents *our* work rather than
answering the universal question. Start fresh.

The target, per the 2026-07-30 outflow (`docs/plans/2026-07-30-outline-for-intro-narrative.md`):

> Whether you're running a business, a team, or any complex project, here's the
> problem you face, and here's a fundamentally different way of thinking about it.

## Decisions locked

| Decision | Choice | Rationale |
|---|---|---|
| **Packaging** | Three separate scrollers, sequential, standalone-but-linked. Ship #1 first. | Matches Goldratt's own sequencing across books — *The Goal* teaches TOC by story; the LTP comes later in *It's Not Luck*. Lets us learn from #1 before committing to #2–3. |
| **Reader** | Smart generalist, no ops background. | Widest reach; forces every idea to earn its jargon. |
| **Example structure** | One running case as spine + short lateral jumps. | A single case compounds (Goldratt's plant); jumps prove generality. |
| **Running case** | A community health clinic. | Carries a queue (#1), a funnel, genuine local-optimum conflict, enough texture for six trees (#3), and a true evaporating cloud (see more patients ↔ spend real time with each). No consulting smell. |
| **Lateral jumps (#1)** | Marketing funnel · a team's week · caring for a parent. | ~30s each. Third one deliberately non-commercial. |
| **Visual ambition** | ~~Scroll-driven SVG reveals + 2–3 interactive beats per piece.~~ **REVISED 2026-08-14:** scroll-driven reveal throughout; **at most ONE interaction per piece.** | Evidence overturned the original call. NYT click-through on interactive graphics is 10–15%; ~85% ignore tooltips/rollovers. Archie Tse: *"If you make the reader click or do anything other than scroll, something spectacular has to happen."* ProPublica's exemplar has **zero** interaction. See `skills/scrollable-explainer/SKILL.md`. |
| **Length + density** | **≈1,200 words of body prose, median 16 words per text block, ~50 drawings, one screen of graphic per sentence.** | Measured directly from the ProPublica reference in a browser: 1,834 editorial words (≈1,100 body + 700 methods), 79 blocks, median 16 words/block, 35,867px tall, 13 full-viewport pinned graphics, **zero interactions.** |
| **Reference piece** | Imitate the approach of ProPublica's *Why Carbon Capture Can't Solve Climate Change* — not its content. | Rufus's explicit direction, 2026-08-14. Anatomy measured in `skills/scrollable-explainer/SKILL.md`. |
| **Craft reference** | `skills/scrollable-explainer/SKILL.md` — form definition, exemplar shortlist, house rules. | Read before drafting any piece. Reusable across all three. |
| **Rhetorical engine** | Elicit the reader's prediction, *then* violate it. | The counterintuitiveness of TOC is the payload. In predictive-processing terms: generate a prediction, then break it. |
| **Draft medium** | Markdown with `[FIGURE n: spec]` slots. | Prose settles before any SVG is drawn. Markdown draft is the review artifact. |
| **Design system** | Reuse `story/_ds/organic-*` (cream/terracotta/sage, Caprasimo + Figtree, tokenised). | Already built, already on-site, already themed. |
| **Location** | New top-level `explainers/<nn>-<slug>/` — `draft.md`, `figures.md`, `index.html`. | Keeps the trilogy separate from the old story. |
| **`story/` (What Counts)** | Left in place, untouched. | Retire only once Piece 1 can replace it. Separate decision. |
| **Naming the method** | "Logical Thinking Process" is not named until late in #1 / in #2. | Concept before label. |

## The three pieces

### Piece 1 — *The Bottleneck* (working title)

**Answers:** why don't your fixes stick?
**Payload:** a system's output is set by one constraint; optimising every part is
not optimising the whole; local efficiency can actively harm global throughput.
**Hands off with:** "So — find the constraint. But *how do you find it?* That
turns out to be a thinking problem."

Source spine: Dettmer ch1; existing synthesis Parts 1–3.

### Piece 2 — *Thinking Made Visible* (working title)

**Answers:** why would you ever draw your reasoning as a tree?
**Payload:** reasoning is invisible, so it can't be checked, shared, or
accumulated; necessity vs. sufficiency; cause-effect vs. correlation; the
Categories of Legitimate Reservation as the etiquette that makes disagreement
productive instead of exhausting.
**Hands off with:** "One tree isn't enough — different questions need different
trees."

Source spine: Dettmer ch2 (CLR); existing synthesis Part 4. **This is the most
original piece relative to Goldratt** — it is where this project's own thesis
lives (claims get addresses; debate accumulates against a stable scaffold; see
`MOTIVATION.md`).

### Piece 3 — *The Six Trees* (working title)

**Answers:** what the Logical Thinking Process actually is.
**Payload:** IO map · Current Reality Tree · Evaporating Cloud · Future Reality
Tree · Prerequisite Tree · Transition Tree — each with the question it answers,
one beat of the clinic case, one diagram.
**Ends with:** the live demo (`claim-tree-annotation-demo/`, dashboard).

Source spine: Dettmer ch3–7; existing synthesis Part 5.

## Sourcing rules

- **`docs/The Theory of Constraints and the Logical Thinking Process - Learning to Think Better.md`** (449 lines) is pillaged and restructured, never merely extended. It is a good *essay*; a scroller is a different animal — beats, not paragraphs.
- **Dettmer** (`library/logical-thinking-process-dettmer/`) read just-in-time: ch1 + front matter for #1, ch2 for #2, ch3–7 per section of #3.
- ***The Goal*** — not required as a text. Its set pieces (Herbie on the hike, the dice game, the idle workers) are renderable without it. Revisit if a beat needs the actual prose.
- **Every claim in a beat sheet carries a source tag** (`[D ch1 p12]` or `[syn Part 2]`) so the drafting phase cannot invent.

## Pipeline

Each piece runs the same five stages. Each stage is one loop-resumable work unit.

```
beat sheet → markdown draft → figure specs → SVG/HTML build → publish
             with [FIGURE n]   incl. interactive
             slots             beats
```

### Piece 1 — The Bottleneck

- [x] **1.1** Read Dettmer ch1 + front matter; read existing synthesis in full
- [x] **1.2** Beat sheet — `explainers/01-bottleneck/beats.md`
- [x] **1.3** Draft v1 (essay form) → `draft-v1-prose.md`
- [x] **1.3c** Converted to shot list — `shotlist.md` (57 blocks, ~1,020 body words, 0 interactions)
- [ ] **1.4** Rufus review gate — redirect here, not later
- [ ] **1.5** Drawing production — 57 drawings, hand-drawn/ink register, one shared paper ground
- [ ] **1.6** Build `explainers/01-bottleneck/index.html` — pinned-stage pattern, CSS `position: sticky`, IntersectionObserver steps
- [ ] **1.7** Verify (see below) and publish

### Piece 2 — Thinking Made Visible

- [ ] **2.1** Read Dettmer ch2 in full
- [ ] **2.2** Beat sheet
- [ ] **2.3** Markdown draft
- [ ] **2.4** Rufus review gate
- [ ] **2.5** Figure specs
- [ ] **2.6** Build
- [ ] **2.7** Verify and publish

### Piece 3 — The Six Trees

- [ ] **3.1** Read Dettmer ch3–7
- [ ] **3.2** Beat sheet
- [ ] **3.3** Markdown draft
- [ ] **3.4** Rufus review gate
- [ ] **3.5** Figure specs
- [ ] **3.6** Build + wire the demo handoff
- [ ] **3.7** Verify and publish

### Cross-cutting (after #1 ships)

- [ ] Decide whether `story/` "What Counts" is retired, kept, or relinked
- [ ] Nav + `config.json` entries for the trilogy
- [ ] Cross-links between the three pieces

## Verification

A piece is done when all of these hold:

1. **No unearned jargon.** Every term is used only after the reader has felt the
   thing it names. Grep the draft for: throughput, constraint, system, local
   optimum, sufficiency, necessity, UDE — each first use must follow its felt example.
2. **Source-traceable.** Every factual/structural claim maps to a source tag in
   the beat sheet.
3. **The prediction beats actually withhold.** Each interactive beat must be
   unanswerable by scrolling past it — the reader commits first.
4. **Legible at 375px.** Every figure readable on a phone; no horizontal page scroll.
5. **Theme-correct.** All colour/type/spacing from Organic DS tokens; no hard-coded hex.
6. **Reduced-motion respected.** Every scroll animation has a `prefers-reduced-motion` path.
7. **Cold read.** A reader who knows nothing of TOC reaches the handoff line and
   wants the next piece.

## Open questions

- Running case: clinic is proposed, not battle-tested. If it strains at Piece 3's
  six trees, the fallback is a school or a small product team — but switching
  after Piece 1 ships is expensive, so stress-test it during 1.2.
- Whether Piece 1 replaces `/story/` on the site nav or sits alongside it.
