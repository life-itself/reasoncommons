# Reason Commons in use

A read-only demonstration of Reason Commons through the collaboration's own reasoning, at [`/demos/reason-commons-in-use/index.html`](../../website/demos/reason-commons-in-use/index.html). It consolidates the supplied dashboard and six map perspectives into an overview, inspectable reading/diagram views and an account of the public record. The homepage and demos page link to it; adopting it as the homepage remains a separate decision.

## Build and check

From the public repository root:

```sh
python3 apps/reasoning-demo/build.py
python3 -m unittest discover -s apps/reasoning-demo -p 'test_*.py'
python3 apps/reasoning-demo/build.py --check
node --check apps/reasoning-demo/app.js
python3 scripts/export-website.py
python3 scripts/check-website.py
python3 -m http.server 8878 --bind 127.0.0.1 --directory website
```

Open `http://127.0.0.1:8878/demos/reason-commons-in-use/index.html`. The simple server renders the standalone demonstration; it does not render the site's Markdown pages as Flowershow does. The generated HTML includes the complete reading record and an escaped, non-executable public JSON payload. It needs no external fonts, libraries, runtime AI, fetch requests, account or browser storage. With JavaScript off, every selected statement and connection is readable and item fragments still resolve. Browser enhancement adds the view switches, filtering, native modal details, stable query routes and copyable skill briefs. Clipboard failure leaves a manually copyable brief.

## Source and publication boundary

The authoritative collaboration record is in the private product repository, following the 2026-10-21 source move. It is never copied into this repository. `publication.json` contains a deliberate allowlist of 50 statement IDs and 14 connection IDs, approved display names, release metadata and the reviewed public projection. The user accepted publishing this selected content under `accepted-reasoning-demo-2026-10-22` revision 1. Routine builds and public CI use that reviewed projection, so they do not need access to the private source.

For an authorized refresh, provide the current working YAML explicitly:

```sh
python3 apps/reasoning-demo/build.py --refresh /absolute/path/to/authorized/reason-commons.yaml
```

The refresh validates the working state with the existing Reason Commons validator, then exports only selected fields from explicitly selected accepted items. Every selected connection must retain all of its source statements and its target in the same tree; all must be accepted. A missing item, downgraded standing, unselected contributor/endorser, unsupported version or incomplete connection fails the refresh before output files are written. New accepted source items stay excluded until the allowlist is deliberately reviewed. Assumptions, challenges and backlog notes have no separate endorsement standing, so none is included in this first projection. Approval receipts, source paths, free-text contribution notes, feedback records and transport metadata are excluded too.

The projection retains full wording, node kind, relationship semantics, human endorsers, carefully mapped contribution attribution and the original acceptance context. Imported driver fallback means original authorship is unknown; it does not credit the driver as the author. Source status is kept separate from publication. Accepted reasoning is a working position, and the September/October statements are explicitly dated context, not a freshly verified report of the project's condition. Actions have no completion badges. There are no fictional metrics, outcome reports or public-history versions.

`snapshot_sha256` detects accidental changes to the pinned public payload. It is an integrity check, not a signature or evidence of human review. Builds validate the field allowlist and exact selected IDs independently. Review the whole diff and actual private-source comparison when refreshing. Do not infer that a successful build checked live source freshness: only an explicit refresh does that.

## Routes and graph meaning

Routes use the real static `index.html`, so direct links work without host rewrites:

- `?view=overview#overview`
- `?view=reasoning&tree=goal&mode=diagram#reasoning`
- `?view=reasoning&tree=current_reality&q=coherent#reasoning`
- `?view=reasoning&tree=goal&item=g-e-picturable-product#item-g-e-picturable-product`
- `?view=record#record`

All six perspectives expose only their selected accepted items. Four have no accepted connections; they show independent statements and explain the gap. Diagrams derive actual topology and explicitly join multiple source conditions at an AND junction. Disconnected statements stay separate. The layout does not infer a constraint, sequence, causal bridge or evidence rating. Diagrams have an independent scroll area and an equivalent reading view. Search preserves an entire connected component as context, highlights matching statements in reading mode, and uses the same selection in both modes. Graph order preserves source order within layout layers.

Copying a contribution brief prepares context for a later authorized skill conversation. It grants no shared-edit access and submits nothing. The brief includes the public release, exact item text and endorsers, and asks the skill to establish identity and check the current authorized record first. An outsider can retain a draft. There is no advertised automatic delivery channel.

## Release and rollback

Publish only `website/`. Run the build, drift, boundary and behavior checks, then use the existing separate Flowershow preview target when authenticated. Do not change production settings to test this page. A Git review/merge delivers the whole public projection and generated views together. Keep the release identifier stable for a rebuild without content changes. A later public content change needs a new identifier and renewed selection review; the current app does not claim to provide a historical release browser.

Rollback is a reviewed revert of the demo change on the publishing branch, removing the main-site entry links and its public files together. No private state or approval receipt should be reverted merely to roll back website delivery. If selected content needs withdrawal, remove it from the manifest, snapshot, generated HTML/JSON and search/graph output, publish the sanitized release and request host cache invalidation; do not promise that third-party copies can be recalled. The pilot only publishes the explicitly approved selected material.

## Review evidence

See [the review record](../../docs/product/reasoning-demo-review.md) for what was actually checked and the outstanding limits. Implementation bead: `reasoncommons-2uv`. The acceptance receipt and Goal backlog `demonstrate_accepted_reasoning` live in the private collaboration YAML. No reasoning nodes, links or standings changed. Human comprehension, coherence for a newcomer and willingness to test remain open questions.
