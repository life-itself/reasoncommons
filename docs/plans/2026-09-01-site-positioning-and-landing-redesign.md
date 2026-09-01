---
title: Site positioning, landing page, and navigation redesign
created: 2026-09-01
status: in progress — shipping in this session
---

# Site positioning, landing page, and navigation redesign

Brainstorm + design for the reasoncommons.com rework. Produced with `/superpowers:brainstorming`. This document is the reference for *what the site is* and *how it should be structured*; it stays off the published site (`docs/plans/` is in `contentExclude`).

## Problem

The site sprawls. Flowershow publishes every top-level folder that is not explicitly excluded, so the real site is roughly a dozen destinations while the nav advertises four. The landing page opens on the *problem statement* rather than on what the visitor is looking at, ends on contributor/Codex instructions, and gives a rough experiment (Goal Aligner) the same nav billing as the strongest asset (the explainer series). Nothing says "start here". The framing the project actually uses in conversation and in the funding pitch — *trees of thought / trees of change and trees of action*, with AI tooling as the bet — appears nowhere on the site.

## What Reason Commons is (the reference statement)

Reason Commons is a project exploring a better way for groups to **think together and turn that thinking into action**. You hold your reasoning as living trees — a **tree of change** (what is the goal, what is blocking it, why) and a **tree of action** (what to do about it) — and you map evidence and discussion onto them, so a group builds one shared, inspectable structure instead of talking past each other in threads that never accumulate.

We are building **AI tooling** to make this cheap enough to actually use. AI drafts the trees from existing material, and — the distinctive bet — folds ongoing forum discussion back into them as structured annotations, so the analysis keeps improving instead of scrolling away. Enriching the discussion and improving the tree at the same time.

The approach is **grounded in the Logical Thinking Process (LTP)**, a forty-year-old method from the Theory of Constraints — the most thorough realization of this idea. The site keeps its rigour without requiring its vocabulary. LTP lives in a dedicated **Guide** section for the people who go looking for it (and as an SEO surface).

**Status:** there is no app to log into yet. There is a way of thinking, a demo of the four steps, an explainer series, and a live application of the method to one movement's strategy (Second Renaissance). Enough to judge whether it is worth adopting, joining, or funding.

**Audience:** smart, mission-aligned people in communities that already reason hard in public — AI governance, effective altruism, climate, social movements — with little or no LTP background. They are evaluating whether to engage, not debating formal logic. (Unchanged from `docs/brand-and-domain-naming.md`.)

**What a visitor should come away understanding:** structuring claims into trees, then annotating and updating the leaves and branches from ongoing discussion, is a much better way to collectively reason and to build collective plans — and AI now makes it practical.

### The three strands (from the funding pitch, `drafts/funding-proposal.md`)

1. **Tooling** — AI-assisted software for creating, maintaining, and evolving LTP artefacts (goal trees, issue trees, problem trees), with the annotation layer that connects ongoing discussion to the structure.
2. **Community adoption** — work with communities already engaged in complex reasoning (AI governance, EA, climate) to demonstrate the approach and build the workflows that sustain it.
3. **Living laboratory** — apply the system within Second Renaissance itself, coordinating strategic thinking across an active Discourse community.

## Primary visitor and calls to action

Two co-equal primary CTAs on the landing page:

- **Read the series** → `/explainers` — the accessible way in; the introduction to the ideas.
- **See it working** → `/claim-tree-annotation-demo/index.html` — the four steps end to end. Later joined or replaced by a short **video demo** (see backlog).

Secondary, mid-page: browse the demos; read the Guide.

Background, at the foot of the page only: **email capture** (updates / occasional newsletter), plus links to GitHub (issues) and Discord for getting involved. "Get in touch" is deliberately not a hero action — there is nothing to onboard onto yet.

## Information architecture and navigation

Current nav: `Goal Aligner · The Series · Dashboard · Blog`

New nav: **`Introduction · Demos · Guide · Blog · About`** plus GitHub and Discord as social icons.

| Nav item | What it is | Path | Change |
|---|---|---|---|
| **Introduction** | the explainer series — the accessible narrative way in | `/explainers` | renamed from "The Series"; the Second Renaissance piece stays inside it, framed as "the method on a real problem", not as part of the core trilogy |
| **Demos** | index of rough, unfinished, and demonstration pieces | `/demos` | new index page; Goal Aligner and the talk deck move physically under `/demos/`; the annotation demo and the dashboard stay at their current paths and are linked from the index |
| **Guide** | the Logical Thinking Process — a plain-language intro page in front of the nine reference docs, plus the reading list | `/ltp` | new `ltp/index.md` intro page; the `/ltp/` path is kept |
| **Blog** | the two essays | `/blog` | new `blog/index.md` so the bare path resolves |
| **About** | who is behind it, the three strands, status, related projects, how to get involved | `/about` | new page; absorbs the "About", "Related", and "Working with this repo" content currently on the landing |

Dropped from nav: Goal Aligner and Dashboard (both now reached via Demos).

## Landing page structure (`README.md`)

`README.md` is the Flowershow homepage source and also the GitHub README, so the top is plain Markdown (renders well in both) and the card sections are hand-written HTML using classes defined in `custom.css` (degrade to readable plain blocks on GitHub). Card styling uses the `lessflowery` theme's CSS custom properties (`--color-background-surface`, `--color-foreground`, `--color-accent`, `--width-content`) so it follows light/dark automatically. No Tailwind utility classes — they are not reliably compiled from Markdown content in this Flowershow setup; the explainers use the same scoped-CSS approach.

**Above the fold**

- **Hero** — headline, one-sentence subhead, two buttons (*Read the series* / *See it working*).
  - Headline: *A better way to think together — and to act on it.*
  - Subhead: hold your reasoning as living trees of change and action, map evidence and discussion onto them, and build shared understanding that actually accumulates — with AI doing the heavy lifting.
- **What you have here** — a card row:
  1. **The idea** — trees of change and trees of action; every claim and every step has an address.
  2. **The AI tooling we're building** — drafting trees from source material, and folding forum discussion back into them as annotations.
  3. **See it working** — the four-step demo (and, soon, a video).
  4. **Grounded in the Logical Thinking Process** — → Guide.

**Mid page**

- **The three-part series** — brief; "start here"; links to each part and to the Second Renaissance application.
- **Demos and experiments** — card grid: annotation demo, Goal Aligner, Dashboard, the talk — explicitly labelled rough / unfinished.
- **The method underneath** — a short paragraph on LTP → Guide and reading list.

**Below the fold**

- **About** — teaser: who (Rufus Pollock + David Joseph), the three strands, "no app yet", related projects (Promise Foundation, Provisio, issuetrees.com) → full `/about`.
- **Stay in touch** — email capture embed (provider TBD — placeholder in place), Discord, GitHub issues.

**Removed from the landing entirely:** "Working with this repo" (Codex / `$project-ltp` / dashboard build-and-serve) — moves to `/about` and `docs/dashboard.md`.

## Content reorganisation

`contentExclude` additions: `/docs/plans`, `/docs/prompts`, `/docs/notes`, `/examples`, `/talk/2r-research-group`, and the raw 82 KB book summary at `/docs/The Theory of Constraints and the Logical Thinking Process - Learning to Think Better`.

Kept published: `/docs/theory`, `/docs/dashboard.md`, `/docs/brand-and-domain-naming.md`, `/library`, `/ltp`.

`/examples/individual-swe-notes/` is fixture data for the annotation/goal-alignment skills (a persona's notes), not site content — excluded rather than deleted so it stays available to the skills.

## The Goal Aligner move

`alignment/` → `demos/goal-aligner/` (`git mv`). A meta-refresh stub is left at `alignment/index.html` pointing to `/demos/goal-aligner/` because this Flowershow setup has no redirect config; the old path is ~1 month old and only linked internally, so this is low-risk. `contentExclude` paths for the app's `export/`, `extracted/`, `uploads/` subfolders are repointed.

## Staging

- **Unit A** — landing page, nav, `contentExclude` sweep, email-capture placeholder. Shippable alone.
- **Unit B** — `/demos/` index and Goal Aligner move, `/ltp/` intro page, `/about`, `/blog/` index, `docs/` curation.
- **Unit C (backlog)** — video demo, Dashboard reframed as a curated example, reconciling "Introduction" vs "Guide" naming and the Second Renaissance piece's placement.

This session ships A and most of B. C is tracked in issues and `NEXT.md`.

## Backlog → GitHub issues

Shipped 2026-09-01 (closed #5 with a summary comment): new landing page, nav restructure, `contentExclude` sweep, `/demos/` index + Goal Aligner move, `/ltp/` intro page, `/about`, `/blog` index.

Open follow-ups:

- [#12](https://github.com/life-itself/reasoncommons/issues/12) — wire up the email-capture embed (placeholder in place).
- [#13](https://github.com/life-itself/reasoncommons/issues/13) — video demo of the four-step flow.
- [#14](https://github.com/life-itself/reasoncommons/issues/14) — reframe the Dashboard as a curated example.
- [#15](https://github.com/life-itself/reasoncommons/issues/15) — reconcile "Introduction" vs "Guide" naming and the Second Renaissance piece's placement.
- Discord invite URL — not in the repo; landing/about link to GitHub only for now.

## Open questions / risks

- **Tailwind in Markdown** — unverified; using scoped CSS in `custom.css` instead. Verify nothing regresses on preview.
- **Redirects** — no mechanism in this Flowershow setup; the Goal Aligner move relies on a meta-refresh stub.
- **Email provider** — not chosen; landing ships with a styled placeholder and an HTML comment marking where the embed goes.
- **Discord invite URL** — not in the repo; landing/about link to GitHub for now with a TODO for the Discord link.
- **Second Renaissance piece** — kept inside Introduction as "the method on a real problem"; revisit in Unit C.
