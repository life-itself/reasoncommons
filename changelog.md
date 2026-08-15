# Changelog

Notable changes to this project. Not strictly [Keep a Changelog](https://keepachangelog.com/)
format, but same spirit — human-readable, most recent first.

## 2026-08-16 — Repo gardening: Reason Commons branding, clean landing page, tidy explainers

A housekeeping session with no new content, but the site now looks like a project
rather than a workspace: the front door reads as an invitation, the finished
explainers stand on their own, and the scaffolding behind them is out of sight.

- **Rebranded to Reason Commons.** Site title and README header still said "Issue
  Trees & Logical Thinking Process"; both now match the naming decision recorded in
  `docs/brand-and-domain-naming.md`. Stale links to the old repo name were fixed
  across `config.json`, the dashboard manifest and the skill docs.
- **README is a landing page now.** It leads with a plain-language pitch instead of
  a pointer to another file, puts the demos near the top, and keeps the backstory to
  a short "About" at the bottom. The stale June "Next Steps" checklist is gone —
  planning lives in [GitHub issues](https://github.com/life-itself/reasoncommons/issues),
  which is also why `PLAN.md` was retired.
- **`explainers/` reorganised.** Each piece is now `<nn>-<slug>/index.md` (the
  article) plus `scrolling.html` (the scroll-driven version); scripts, critiques and
  superseded drafts moved into `explainers/_process/`, hidden from publishing. The
  series index became markdown, and `NEXT.md` moved to the repo root — there's now
  exactly one.
- **Root docs lowercased** (`motivation.md`, `changelog.md`) so Flowershow gives
  them clean URLs; `README.md` and `AGENTS.md` keep their uppercase names because
  tooling looks them up literally.
- **Two working conventions recorded in `AGENTS.md`**: this changelog convention,
  and a preview workflow — `main` is the live site, so render checks go to a
  separate Flowershow preview site (`fl . --name reasoncommons-preview --yes`)
  rather than to production.

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
