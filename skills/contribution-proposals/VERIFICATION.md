# Verification — contribution-proposals (v0.1)

**Date:** 2026-09-04 · **Runner:** Claude (agent, following `SKILL.md`)
**Inputs:** `examples/contributions.sample.txt` (7 synthetic contributions, written
to exercise every operation) + `../../ltp/ltp-model.yaml` (the real Second
Renaissance model, 63 entities / 61 links / 6 views)
**Outputs:** `examples/proposals.sample.yaml`, and the page built from it at
`../../talk/2r-research-group/demo-c/index.html`

## What this is, and isn't, evidence of

The renderer is verified. The *reading* is not: the seven contributions are
synthetic, written alongside the proposals rather than found in the wild, so
they say nothing about how well the skill reads text it did not anticipate.
That test is the live session this was built for, and the thing worth recording
afterwards is every proposal the room corrected or rejected and why — the same
`IO-5` AI-versus-steward comparison `../goal-alignment` is waiting on.

Following this repo's convention, the toy case came first. It uses the real
model rather than a toy tree, because the placement logic only has meaning
against a tree with real structure — a 6-node fixture would not have produced
the deep `current-reality` chain that exposed the child-ordering bug below.

## Mechanical checks

- `build-demo.py` validates and builds cleanly: 7 proposals across 2 views —
  2× `add_entity`, 1× `add_link`, 1× `challenge_entity`, 1× `challenge_link`,
  1× `support_entity`, 1× `unplaced`. All six operations covered.
- Every referenced id resolves: `NC-1`, `NC-2`, `NC-4`, `NC-5`, `UDE-2`, `CSF-2`
  as entities; `L-009` as a link; `goal-tree` and `current-reality` as views.
  Each is present in the view it is addressed to.
- The validator was run against seven deliberately broken copies of the sample
  and rejected each one with a named reason rather than producing a broken page:
  an unknown entity id, a link that exists but sits outside the named view, a
  missing `connects_to`, an `entity:` block smuggled onto a `challenge_entity`,
  a `review.status` of `accepted`, a misspelled view key (which lists the real
  ones), and a confidence outside high/medium/low.
- `ltp/ltp-model.yaml` is byte-identical after the run. The build script opens
  it read-only and records its SHA-256 prefix on the page.
- Confidence is not uniform: 4 high, 2 medium, and one contribution deliberately
  read as `unplaced` rather than forced under the nearest-sounding node.

## Interface checks — driven in a browser, not assumed

Every proposal was stepped through at 1440×860 and 1280×800:

- `add_entity` lands dashed under its parent and settles solid on accept;
  accepted nodes persist as the room advances.
- `support_entity`, `challenge_entity`, `challenge_link` and `add_link` each
  attach to the right node, in the right hue, with the verbatim quote intact.
- Switching from `goal-tree` to `current-reality` mid-run redraws the field.
- `unplaced` shows the no-address panel, relabels Accept to *Record as a gap*,
  disables Edit, and collects accepted gaps in the strip below the tree.
- Edit moved `PROP-001` from `NC-2` to `NC-3` and rewrote its claim; the tree
  redrew at the new address and stamped it *edited by the room*.
- The tally counts merged, declined, gaps, and still-open correctly, and states
  which model the session ran against.

Five defects were found this way and fixed: sections hidden with `[hidden]`
losing to `display:flex`; Cormorant rendering `1` as a small-cap `I` in the
tally; proposed children drawn *after* a target's existing children, which in
the long `current-reality` cause chain put the proposal a screen away from the
node it belonged to; the edit panel falling below the fold; and a relation
label repeated on all nine goal-tree nodes where it carried no information.

## Not yet tested

- A batch larger than about a dozen proposals. The header dots and the
  accumulating tree are both untested at, say, 30.
- Views other than `goal-tree` and `current-reality`. `evaporating-cloud` in
  particular is a conflict structure, not a hierarchy, and the upward outline
  may read poorly there.
- Any contribution the skill did not write itself.
