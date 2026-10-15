---
date: 2026-08-15
title: "Explainer trilogy: drafted, built, and shipped in two formats"
authors: ["rufus-pollock"]
promote: false
---

Three-part LTP explainer series in `explainers/`, replacing the earlier single `story/`
piece as the project's introductory narrative. Each piece went through a script pass
(draft → self-critique → independent fresh-agent critique with no authorship context →
revision), then a visual build.

- Added `skills/scrollable-explainer/` — general-purpose write-up of the scroll-driven
  ("scrollytelling") explainer form, with a full measured teardown of a ProPublica piece
  as the worked case study.
- Wrote and built three pieces: **The Wrong Queue** (`01-bottleneck`), **The Arrows
  Nobody Checks** (`02-thinking-made-visible`), **Five Shapes** (`03-five-shapes`).
- Each part now ships in two forms from the same finalized prose:
  - `article.md` — static markdown with inline SVG figures, no `<script>` (matches the
    `story/draft.md` convention)
  - `index.html` — scroll-driven animated version, via shared `explainers/scroller.js` /
    `scroller.css`
- `explainers/index.html` lists both formats per part.
- Mobile portrait layout for piece 1's five-station diagram (pieces 2–3 still pending).
- `explainers/NEXT.md` — checkpoint with open questions and a prioritized follow-up list.
  Tracked in [issue #6](https://github.com/life-itself/reasoncommons/issues/6).

Known gaps: pieces 2–3 need the same mobile pass as piece 1; piece 3's HTML page
renders empty with JavaScript disabled; the scroller uses an ad hoc palette rather than
the real Organic design tokens; `story/`'s fate is undecided.
