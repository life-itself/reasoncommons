---
title: Where we are, what's next
created: 2026-08-15
updated: 2026-08-16
status: checkpoint
---

# Next steps

Checkpoint after shipping the explainer trilogy and tidying the repo around it.

- **What shipped:** see [`changelog.md`](changelog.md).
- **Open questions + follow-up work:** tracked in
  [issue #6](https://github.com/life-itself/reasoncommons/issues/6).

## The one decision waiting on you

**Keep both formats, or pick one?** Each explainer exists twice — a markdown
article (`<piece>/index.md`) and a scroll-driven version
(`<piece>/scrolling.html`). Same words, same figures, two files to keep in sync
on every edit. That cost is real and recurring, so it's worth settling before
the next piece of writing rather than after.

To judge it: read piece 1 and piece 3 end to end in both forms on the live site,
then say which earns its keep.

## Ready to pick up

- **Extend the 2026-08-16 changelog entry.** It was written before the explainers
  restructure, the SVG rendering fix, and the preview workflow landed. Per the
  changelog convention these are all small stuff, so one added sentence, not
  bullets.
- **Anything from [issue #6](https://github.com/life-itself/reasoncommons/issues/6).**

## Known friction (not blocking)

- **`fl` can't publish from the repo root unaided** — it aborts on the tracked
  `.agents/skills/project-ltp` symlink. Workaround is moving `.agents` aside for
  the publish and restoring it after.
  ([flowershow#1361](https://github.com/flowershow/flowershow/issues/1361))
- **`fl` previews ignore `contentExclude`**, so `_process/` is visible on the
  preview site. Production, built from GitHub, correctly 404s it — the live site
  is right, the preview is not.
  ([flowershow#1362](https://github.com/flowershow/flowershow/issues/1362))
- **`fl` never deletes.** A preview keeps files removed from the repo, so it can
  disagree with production about anything deleted or excluded. `fl delete` then
  republish if in doubt.

Conventions worth knowing before editing anything here — the `explainers/`
layout, the no-blank-lines-inside-raw-HTML rule, and the preview workflow — are
in [`AGENTS.md`](AGENTS.md) under Conventions.
