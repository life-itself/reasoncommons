---
date: 2026-09-06
title: "One skill for LTP project files, and the 2R Research Circle leaves the dashboard"
authors: ["david-joseph"]
promote: false
---

There is now one way to write an LTP model with an AI: [`skills/ltp-project`](../skills/ltp-project/SKILL.md), which produces the Reason Commons `*.ltp.yaml` project file — the same interchange document the app imports and exports as JSON or YAML, version and event history included — from a PDF, a Markdown document, a repository's plans and issues, a roadmap or meeting notes, with a report of every judgment call. It is a byte-identical mirror of the canonical skill in [Promise-Foundation/reason-commons](https://github.com/Promise-Foundation/reason-commons); edit it there and copy it here. The older [`project-ltp`](../skills/project-ltp/SKILL.md) skill is deprecated: its `ltp-model.yaml` was a second, incompatible format that the app cannot import and that carries no history, and its GitHub issue sync is now done by the Reason Commons projection, which writes and reconciles managed issues itself. The skill's read-only dashboard stays as a viewer for the legacy models still bundled here.

The **2R Research Circle** project is gone from [the dashboard](../dashboard/index.html): its model was the July 2026 analysis, superseded by the live Reason Commons space connected to the [2R-Research repository](https://github.com/Promise-Foundation/2R-Research), which exports the current model to that repository as `.reason-commons/<space-id>.ltp.json`. The throughput track that fed it — counted from this repository's Git history — went with it, so `throughput.config.json` now holds no tracks and the generator tolerates that. The dashboard was rebuilt and republished; the Second Renaissance and the software-engineer example remain.
