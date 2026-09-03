---
title: What's next
updated: 2026-09-01
---

# Next

## Site positioning & landing redesign

Design doc: [`docs/plans/2026-09-01-site-positioning-and-landing-redesign.md`](docs/plans/2026-09-01-site-positioning-and-landing-redesign.md). Units A + most of B shipped 2026-09-01 (new landing, nav `Introduction · Demos · Guide · Blog · About`, `/demos/` + `/about/` + `/ltp/` + `/blog/` index pages, Goal Aligner moved to `/demos/goal-aligner/`, `contentExclude` sweep). Remaining, tracked in GitHub issues:

- **Email-capture embed** ([#12](https://github.com/life-itself/reasoncommons/issues/12)) — landing ships with a placeholder; pick a provider and wire it.
- **Video demo** of the four-step flow ([#13](https://github.com/life-itself/reasoncommons/issues/13)) — join or replace the annotation demo with a short screen recording.
- **Reframe the Dashboard** ([#14](https://github.com/life-itself/reasoncommons/issues/14)) as a curated example with a proper intro, not a bare prototype link.
- **Reconcile "Introduction" vs "Guide"** ([#15](https://github.com/life-itself/reasoncommons/issues/15)) naming and settle where the Second Renaissance piece belongs.
- **Discord invite link** — not in the repo; landing/about link to GitHub only for now.

## Explainers

- *The Forum Doesn't Remember, and Doesn't Cumulate* ends on a protocol that does not exist yet. It says so plainly, which is defensible for now and stops being defensible if a year passes and it still isn't built.
- **Review the two plain explainer versions** on the preview (`explainers/01-bottleneck-plain/`, `explainers/second-renaissance-plain/`) — 5 unpushed commits on `main`. Built for a usability A/B against the scrolling originals. Known rough edges, all inherited from the source drawings and left as faithful stills: a few figures (the doctor's-day bars, the constraint-migration rows) carry a lot of empty paper; in *the stack* the staircase doesn't visually meet the map thumbnail; in *it moves* the dashed hospital box clips the follow-up box. Fixing those means editing the original SVGs, not the stills.
