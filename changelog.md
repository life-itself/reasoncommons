# Changelog

Notable changes to this project. Not strictly [Keep a Changelog](https://keepachangelog.com/)
format, but same spirit — human-readable, most recent first.

## 2026-08-16 — Whose Map Is It

![Two rival definitions of throughput, drawn side by side at equal weight, with an empty dashed box above them where a way of choosing between them would be](changelog/images/2026-08-16-whose-map-is-it.png)

A fourth scrolling explainer, and the first that applies the method to a real
problem rather than an invented clinic: the Second Renaissance sat down to define
what counts as progress, could not, and discovered that its binding constraint was
not its strategy but its inability to change its own mind. It is a sibling to the
trilogy, not a part four — someone handed only this link, with no series behind
them, still gets a complete read. Every diagram comes from the group's actual five
trees.

## 2026-08-16 — The explainer trilogy, finished

![Five Shapes read on a phone: the obstacles and what gets past each one, stacked and legible](changelog/images/2026-08-16-trilogy-polish.png)

Drove all three explainers in a real browser and fixed what only shows up there —
captions sitting on top of the very thing they were pointing at, boxes falling off
the edge of their own drawing, a chain of arrows that read as a tangle. Parts two and
three now have portrait layouts to match part one, so the diagrams are readable on a
phone instead of shrinking to a ribbon, and the series finally uses the real Organic
colours and Figtree rather than a palette that was merely close.

## 2026-08-16 — Repo gardening

Rebranded to Reason Commons, turned the README into a real landing page, and tidied
the explainers folder and docs — no new content, but the site now reads as a
finished project rather than a workspace. Also fixed the diagrams in *The Wrong
Queue*, which had been rendering as raw markup instead of pictures.

## 2026-08-15 — Explainer trilogy: drafted, built, and shipped in two formats

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
