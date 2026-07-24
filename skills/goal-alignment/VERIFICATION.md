# Verification — goal-alignment (pilot #1)

**Date:** 2026-07-24 · **Runner:** Claude (agent, following `SKILL.md`)
**Inputs:** source `../project-ltp/dashboard/public/projects/individual-swe-example/model.yaml`
(synthetic toy example — one engineer's TODO/journal/project notes) + target
`../project-ltp/dashboard/public/projects/second-renaissance/model.yaml`
**Output:**
`../project-ltp/dashboard/public/projects/alignments/individual-swe-example__second-renaissance.yaml`

## What this is, and isn't, evidence of

This is the AI-suggested half of the `IO-5` comparison the project's own
`2r-research-circle` model already prescribes ("AI and steward mappings are
compared on real contributions with errors and corrections recorded") —
before matching is trusted further. It is **not** yet that comparison: no
human with standing over the Second Renaissance tree has reviewed these
6 suggestions. Until that happens, treat every one as `status: suggested`,
not as an accepted alignment.

It also runs on a synthetic toy tree, not a real person's actual notes
repo — per this project's own convention of validating a new skill against
a toy example before pointing it at real data (`PLAN.md`, "Decisions
locked"). The individual model was hand-authored to include one
deliberately unrelated action (`ACT-5`, a routine CRDT-library PR) as a
control case.

## Mechanical checks

- Every `source_entity` id (`ACT-1`, `INJ-1`, `ACT-2`, `ACT-4`, `ACT-5`)
  exists in `individual-swe-example/model.yaml`.
- Every `target_entity` id (`INJ-0`, `CSF-2`, `NC-6`, `RC-0`, `INJ-5`, `G-1`)
  exists in `second-renaissance/model.yaml`.
- Every suggestion has `relation`, `rationale`, `confidence`, and
  `status: suggested`, matching `references/alignment-suggestions.schema.json`.
- Confidence is not uniform: 1 high (`AL-001`), 4 medium, 1 low (`AL-006`,
  the deliberate control case) — the calibration principle in `SKILL.md`
  §1/§5 held rather than defaulting every match to "high."

## Judgment check

The strongest suggestion, `AL-001` (ship the decision-log tool → Second
Renaissance's own `INJ-0`, "a lightweight stewardship and revision protocol
for the trees"), is a same-shape-artifact match: both are a versioned,
stable-ID, rationale-carrying record, one already built at small scale. The
weakest, `AL-006`, is included specifically to show the skill will say
"unclear" rather than manufacture a connection between an unrelated
open-source PR and the collective goal (the `NBR-2` risk named in
`2r-research-circle/model.yaml`).

## Verdict

**Pass** on the mechanical contract (schema-valid, all IDs resolve,
confidence calibrated, no manufactured-significance suggestion left
unflagged).

**Not yet run:** the actual `IO-5` step — an independent human/steward
mapping on the same pair of models, compared against this AI-suggested one,
with errors and corrections recorded. That comparison, not this file alone,
is what should decide whether goal-alignment is trusted on a real
individual's notes repo.
