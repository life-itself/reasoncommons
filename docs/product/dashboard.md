---
title: Dashboard artifact and local previews
---

# Dashboard artifact and local previews

The read-only dashboard is a compiled standalone artifact at [`website/dashboard/index.html`](../../website/dashboard/index.html), with sample models and a manifest under `website/dashboard/projects/`. Its source build system is not present in this repository; older `skills/project-ltp/dashboard/` build/serve commands refer to retired files and are not a supported rebuild path.

## Retirement

The `ltp-project` preview helper that rendered interchange files through this dashboard was retired on 2026-10-21, together with the Reason Commons app whose format it served. Retiring the dashboard itself is proposed in bead `reasoncommons-ffm.2` and awaits Rufus's review; until then it stays published as a static artifact.

## Published routes and model ownership

The public routes remain `/dashboard/index.html#/`, `/dashboard/index.html#/second-renaissance` and `/dashboard/index.html#/second-renaissance/current-reality`. The compiled artifact embeds its demo models; updating an adjacent model file alone does not rebuild that embedded data. Introducing a maintained dashboard source application is separate work; it would belong under `apps/`, with a deliberate publication step into `website/dashboard/`.

The canonical worked-example model remains [`ltp/ltp-model.yaml`](../../ltp/ltp-model.yaml), with an explicit generated public export at `/ltp/ltp-model.yaml`. The conversational collaboration model is a different format and stays outside the website root.
