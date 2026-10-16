---
title: Dashboard artifact and local previews
---

# Dashboard artifact and local previews

The read-only dashboard is a compiled standalone artifact at [`website/dashboard/index.html`](../../website/dashboard/index.html), with sample models and a manifest under `website/dashboard/projects/`. Its source build system is not present in this repository; older `skills/project-ltp/dashboard/` build/serve commands refer to retired files and are not a supported rebuild path.

## Preview an interchange file

From the repository root, run:

```sh
python3 skills/ltp-project/scripts/preview_dashboard.py path/to/project.ltp.yaml
```

The helper serves a temporary converted model on `127.0.0.1:8765`, opens a browser and leaves the source YAML unchanged. Use `--no-open` for a printed URL or `--port 9000` for a different port. To export a standalone HTML preview:

```sh
python3 skills/ltp-project/scripts/preview_dashboard.py path/to/project.ltp.yaml --export-html
```

See [preview limitations](../../skills/ltp-project/references/preview.md). This is an inspection surface, not an import validator or an editor.

## Published routes and model ownership

The public routes remain `/dashboard/index.html#/`, `/dashboard/index.html#/second-renaissance` and `/dashboard/index.html#/second-renaissance/current-reality`. The compiled artifact embeds its demo models; updating an adjacent model file alone does not rebuild that embedded data. Introducing a maintained dashboard source application is separate work; it would belong under `apps/`, with a deliberate publication step into `website/dashboard/`.

The canonical worked-example model remains [`ltp/ltp-model.yaml`](../../ltp/ltp-model.yaml), with an explicit generated public export at `/ltp/ltp-model.yaml`. The conversational collaboration model is a different format and stays outside the website root.
