---
title: Demo C experiment
---

# Demo C experiment

Demo C is the participatory part of [the research-group talk](../../website/talk/2r-research-group/slides.html). Its current [standalone rehearsal page](../../website/talk/2r-research-group/demo-c/index.html) and [proposal data](../../website/talk/2r-research-group/demo-c/proposals.yaml) are public artifacts under `website/talk/2r-research-group/demo-c/`. The public URL remains https://reasoncommons.com/talk/2r-research-group/demo-c/index.html.

The page presents nine fictional contributions against the Second Renaissance tree. It quotes each contribution and offers a proposed placement or objection for review. Its on-screen accept/edit/reject controls affect the page's local memory; they do not edit the canonical model at `ltp/ltp-model.yaml` or ratify the fictional contributions. Refreshing the page resets that review state.

## Inspect the existing experiment

Serve `website/` locally and open `/talk/2r-research-group/demo-c/index.html`, or open the standalone HTML directly from a clone. Keep the rehearsal label visible; do not present fictional data as a real room's contributions.

The original document/form fixture now lives at [`docs/product/demo-c/2r_participant_contributions_test.docx`](demo-c/2r_participant_contributions_test.docx). Talk scripts, notes and the slides brief are in `docs/marketing/talk/2r-research-group/`.

## Historical workflow

The original runbook depended on the retired `contribution-proposals` skill and its build/publish helpers. Those commands are not available in the current checkout. Consult the [original runbook at the pre-migration revision](https://github.com/life-itself/reasoncommons/blob/f001dbcfd0a41e82b9c1510bfbd1193f0527ae24/docs/demo-c.md) as historical context, rather than as operating instructions for the migrated repository.

Reintroducing a maintained ingestion/build workflow is separate product work. Its code and tests need an explicit owner; the current static artifact stays in the website root. Preview publication uses `fl website --yes` against the separate preview target after the normal [website checks and cutover review](repository-boundaries.md).
