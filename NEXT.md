---
title: What's next
updated: 2026-09-03
---

# Next

## Site positioning & landing redesign

Shipped and live on 2026-09-03 (PR #16): new landing page in Rufus's voice, nav `Introduction · Demos · Guide · Blog · About`, new `/demos` + `/about` + `/ltp` + `/blog` index pages, Goal Aligner moved `/alignment/` → `/demos/goal-aligner/` (meta-refresh stub at the old path), narrow `contentExclude` (only `/docs/plans`, `/examples`, `/talk/2r-research-group`, the raw book file, the `CLAUDE.md` symlink — the rest of `docs/` stays a linkable knowledge base). Design/reference doc: [`docs/plans/2026-09-01-site-positioning-and-landing-redesign.md`](docs/plans/2026-09-01-site-positioning-and-landing-redesign.md).

Remaining, tracked in GitHub issues:

- **Email-capture embed** ([#12](https://github.com/life-itself/reasoncommons/issues/12)) — landing ships with a placeholder in the `.rc-foot` block of `README.md`; pick a provider and wire it.
- **Video demo** of the four-step flow ([#13](https://github.com/life-itself/reasoncommons/issues/13)) — join or replace the annotation demo with a short screen recording.
- **Reframe the Dashboard** ([#14](https://github.com/life-itself/reasoncommons/issues/14)) as a curated example with a proper intro, not a bare prototype link.
- **Reconcile "Introduction" vs "Guide"** ([#15](https://github.com/life-itself/reasoncommons/issues/15)) naming and settle where the Second Renaissance piece belongs.
- **Discord invite link** — not in the repo; landing/about link to GitHub only for now.

Not yet tracked in issues:

- **Left file-tree sidebar on the homepage** still lists internal folders (`Skills`, `Talk`, `Library`, `Ltp`, `Docs`, `Alignment`). That's Flowershow's file nav, separate from the top nav — suppressing it on the landing is its own small task.
- **Mobile right-edge text clipping** on narrow screens — pre-existing `lessflowery` theme behaviour (visible on `/motivation` and the pre-redesign homepage too), not caused by the redesign. Wants a real-device check and possibly a theme-level fix.

## Explainers

- *The Forum Doesn't Remember, and Doesn't Cumulate* ends on a protocol that does not exist yet. It says so plainly, which is defensible for now and stops being defensible if a year passes and it still isn't built.
- **The two plain explainer versions** (`explainers/01-bottleneck-plain/`, `explainers/second-renaissance-plain/`) are live, linked from the series index, and built for a usability A/B against the scroll-driven originals. Known rough edges, all inherited from the source drawings and left as faithful stills: a few figures (the doctor's-day bars, the constraint-migration rows) carry a lot of empty paper; in *the stack* the staircase doesn't visually meet the map thumbnail; in *it moves* the dashed hospital box clips the follow-up box. Fixing those means editing the original SVGs, not the stills.
