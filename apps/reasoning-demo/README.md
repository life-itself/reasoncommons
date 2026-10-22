# Reason Commons in use: a site of commons

A static, read-only site at [`/demos/reason-commons-in-use/index.html`](../../website/demos/reason-commons-in-use/index.html) showing what a platform of commons could look like. A commons is a goal and the reasoning a group builds around it with the Reason Commons skill. The site lists accepted reasoning from Rufus and David's collaboration; Gandhi 2.0, a proposed source reconstruction from analyses of a Second Renaissance discussion; and a clearly labelled fictional example, Willow Lane Primary. Nothing on the site edits a commons; contributions start from a copyable brief taken to the reader's own AI.

## Pages

| Page | What it answers |
| --- | --- |
| `index.html` | What is a commons, and which ones can I read? |
| `how-it-works.html` | How is a commons built, what are the six questions, and what do the standings mean? This is the one page that names the Logical Thinking Process. |
| `<commons>/index.html` | The overview: the goal, what stands in the way, the conflict and the change chosen, actions, and who contributed and accepted. |
| `<commons>/map.html` | The six questions, each drawn small in its real shape. |
| `<commons>/goal.html`, `in-the-way.html`, `conflict.html`, `change.html`, `prerequisites.html`, `actions.html` | One question each: a diagram read in that tree's direction, an outline view, and the statements no connection reaches yet. |
| `<commons>/items.html` | Every statement and connection. `items.html#<id>` shows one item on its own (CSS `:target`), with a diagram of its neighbours, its contributors and endorsers, assumptions, challenges, open work, history and a brief for the skill. |
| `<commons>/questions.html`, `learning.html` | Open questions, and expected-versus-reported outcomes. Generated only when the commons publishes them, which today means only the example. |
| `<commons>/changes.html`, `about.html` | Releases with earlier wording kept, and what the record is and isn't. |

Diagrams are static SVG laid out at build time in `diagrams.py`: layered for the trees, the classic five-box arrangement for a conflict, and role groups for statements without connections. Every arrow comes from a published link; a link with several sources meets at one "and" junction before its single arrow. Text is wrapped with measured Alegreya Sans advance widths, so it cannot overflow its box. The font files are the unchanged Latin subsets from the reference pages, under the SIL Open Font License (`fonts/OFL.txt`).

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

Open `http://127.0.0.1:8878/demos/reason-commons-in-use/index.html`. Every page is complete without JavaScript; `app.js` adds the diagram/outline switch, statement search, path highlighting and clipboard copying, and redirects the earlier `?view=…&tree=…&item=…` links to the new pages. `--check` compares all 49 generated files and fails on unexpected files in the published folder. With PyYAML installed it also re-projects the fictional example and source reconstruction from their public working files and fails if either pinned snapshot has drifted.

## Three records, three publication boundaries

**Ours.** The authoritative collaboration record is in the private product repository and is never copied here. `publication.json` holds the reviewed allowlist of 50 statement IDs and 14 connection IDs, approved display names and the pinned accepted-only projection (projection version 1), unchanged from `accepted-reasoning-demo-2026-10-22` revision 1; the redesign was accepted as `commons-site-redesign-2026-10-22` revision 1. Routine builds and CI use the pinned projection, so they need no private access. For an authorized refresh:

```sh
python3 apps/reasoning-demo/build.py --refresh /absolute/path/to/authorized/reason-commons.yaml
```

The refresh validates the working state with the skill's validator, then exports only the selected fields of the selected items, all of which must still be accepted. Proposed and disputed reasoning, assumptions, challenges, backlog, outcome reports, receipts, paths and notes stay private. Publishing any of them needs its own selection approval.

**The fictional example.** `examples/willow-lane/reason-commons.yaml` is an invented working file in the skill's conversational format, checked by the skill's own validator, with feedback snapshots that match its statements exactly. `examples/willow-lane/publication.json` selects its items and adds display names, roles and an authored release history. Its projection (version 2) keeps standings, prior endorsement of disputed items, assumptions, challenges, open work, cross-tree traces and reports, and is accepted by the build only when `is_example` is true. Every example page carries a "Fictional example" banner, its URL and data say `example-`, and its briefs say there is no shared record behind it. To change it, edit the working file and run:

```sh
python3 apps/reasoning-demo/build.py --refresh-example
```

**Gandhi 2.0.** `ltp/gandhi-2-0/reason-commons.yaml` is a compact AI reconstruction from two supplied analyses, with 22 proposed statements, 15 proposed connections and source locators on every item. The original thread and source documents have not been independently checked. The registry at `commons/gandhi-2-0/publication.json` pins an explicit selection, reviewed source descriptions and the initial release. Projection version 3 permits only proposed AI reconstruction with no endorsers or feedback commitments/reports. It reuses the qualification checks without changing version 1's accepted-only boundary or version 2's fictional-example requirement. Every page has a source-reconstruction banner; inspect an item for its source locator and inference label. Original documents, local paths, approval receipts and unselected fields are not exported. Refresh after an authorised edit:

```sh
python3 apps/reasoning-demo/build.py --refresh-reconstruction
```

The opening view starts with candidate common ground, the AI-dependence conflict, a proposed comparison with its possible harm, and an unassigned first task. Other source branches remain open review work. There is no trial result, assigned host or participant endorsement. See [the source and review record](../../docs/product/gandhi-2-0-source-review.md).

## Meaning the site preserves

- Standing is spelled out and shown by border style as well as colour: accepted for now (solid), proposed (dashed), disputed (dotted). Earlier acceptance of a disputed item is shown as history, never as current acceptance.
- Contribution and acceptance are separate. AI-originated ideas are attributed to the AI; imported statements with no known author say so.
- Our accepted-only record groups statements without accepted connections by role, with no arrows. Qualified public records draw proposed connections as proposed, including joint conditions. No constraint, root cause, sequence or evidence rating is inferred from layout.
- Outcome verdicts keep their meaning: observed, not observed, unclear, not assessed and awaiting a report stay distinct, and no trial is called a success.
- The example's people, places and reports are invented. Nothing in it is evidence about a real project.

## Release and rollback

Publish only `website/`. Run the build, tests, drift and website checks, then use the existing separate Flowershow preview target when authenticated; do not change production settings to test this page. Rollback is a reviewed revert of the demo change on the publishing branch. If selected content of ours needs withdrawal, remove it from the allowlist and snapshot, rebuild, publish and request host cache invalidation; third-party copies cannot be recalled.

## Review evidence

See [the review record](../../docs/product/reasoning-demo-review.md) for what was checked and what remains open. Human comprehension, coherence for a newcomer and willingness to test are still untested.
