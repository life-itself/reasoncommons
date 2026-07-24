---
name: goal-alignment
description: >
  Given an individual's (or smaller group's) LTP model, e.g. produced by
  project-ltp, and a target collective-goal LTP model, suggest specific,
  reviewable cross-tree links between entities — which of the individual's
  goals, injections, or actions could advance, support, or risk conflicting
  with which parts of the collective goal tree. Use this skill whenever the
  user wants "smart suggestions" for how their own project or effort could
  help move a group's stated goals forward. Every suggestion requires human
  confirmation before it counts as an accepted alignment — never merge,
  auto-adopt, or treat a suggestion as ground truth.
---

# Goal Alignment

Propose specific, checkable links between one causal model (an individual's
or a smaller group's) and another (a larger collective's), so a person can
see where their own goals, injections, and actions could genuinely advance
someone else's stated goals — and where a claimed connection is weak and
shouldn't be trusted.

## Why suggestions, not scores

An earlier prototype tried fully automated matching between individual
content and a single authoritative group tree (see
`docs/prompts/LTP_BACKGROUND_PROMPT.md:115-121`) and was shelved: the trees
weren't developed enough and the matching wasn't reliable enough to create
real synergy. The project's own reconciliation of this exact problem,
`skills/project-ltp/dashboard/public/projects/2r-research-circle/model.yaml`,
encodes the lesson directly:

- `UDE-5` — automated alignment suggestions are not yet poignant or reliable
  enough to create synergy.
- `NBR-2` — AI mappings can misrepresent a contribution or manufacture
  significance where there isn't any.
- `INJ-5` — let AI suggest mappings and deltas while contributors and
  reviewers retain confirmation authority.
- `IO-5` — AI and steward mappings should be compared on real contributions,
  with errors and corrections recorded, before matching is trusted further.

This skill implements `INJ-5` directly: it produces suggestions, never
merges, and every suggestion carries a rationale a human can check against
the source model's own evidence. Running it once on a real pair of trees is
itself the `IO-5` pilot the project already called for — see
`VERIFICATION.md`.

## Required operating principles

1. Never invent an alignment that isn't traceable to the source entity's own
   statement, evidence, or reasoning. If the honest answer is "weak" or
   "unclear," say so — do not round a weak connection up to a strong one.
2. Every suggestion needs a `relation`, a plain-language `rationale`, and a
   `confidence`, and starts with `status: suggested`. Only a human reviewer
   changes status to `confirmed`, `rejected`, or `edited`.
3. Prefer fewer, well-evidenced suggestions over exhaustive coverage. Most
   entities in the source model won't have a genuine target — that's
   expected, not a gap to fill.
4. Keep the two source models untouched. Alignment output is a separate
   artifact that references entity IDs in both, never a merge of the two.
5. Include at least one deliberately weak or "unclear" suggestion when one
   genuinely exists, rather than silently dropping it — it demonstrates the
   matching is calibrated, not just optimistic.

## Workflow

### 1. Load both models

Read the source (individual/smaller-group) `ltp-model.yaml` and the target
(collective) `ltp-model.yaml`. Note each one's `provisional_goal` and
`views.goal-tree` — that is usually where the highest-leverage matches live.

### 2. Find genuine candidates

For each source entity that represents something actionable (`action`,
`injection`, and `critical_success_factor` are the usual candidates — a raw
`root_cause` or `undesirable_effect` rarely is on its own), ask: does *doing
this* plausibly move any target entity, based on what the source entity's
own evidence says it actually is? Reject candidates that only match at the
level of shared vocabulary ("both mention 'teams'") without a real
mechanism.

### 3. Write the rationale before the relation

Draft the one- or two-sentence mechanism first — e.g. "this decision-log
habit is a small working instance of the versioned, challengeable knowledge
commons the target treats as a necessary condition." If no real mechanism
comes to mind, don't force a `relation`: either mark it `unclear` with low
confidence, or drop it.

### 4. Choose a relation and confidence

Use `advances`, `supports`, `provides_evidence_for`,
`at_risk_of_conflicting_with`, or `unclear` — see
`references/alignment-suggestions.schema.json` for the full contract.
Confidence reflects how directly the mechanism holds, not how much you want
it to be true.

### 5. Emit `alignment-suggestions.yaml`

Validate against `references/alignment-suggestions.schema.json`. Every
`source_entity` / `target_entity` must exist in its respective model.

### 6. Hand off for review

Suggestions are `status: suggested` until a human reviewer — ideally
including someone with standing over the target tree — confirms, rejects,
or edits each one. Do not report the pilot as "aligned" until that review
happens.

## Local dashboard

Register the pair in the multi-project dashboard's `projects/manifest.json`
under `alignments` (see the entry for the `individual-swe-example` →
`second-renaissance` pilot). Suggestions are not a separate screen — they
surface inside the source project's own tree interface, the same one used
for any project:

- A source entity with a suggestion gets a small ◆ badge on its node, in
  both the graph and list views.
- Selecting that node opens the same DetailsPanel used for Evidence,
  Assumptions, and Causal connections, with an added "Alignment
  suggestions" section: the target entity, relation, rationale, confidence,
  and Confirm / Reject / Reset controls plus a reviewer-note field.
- The project's Overview tab gets one summary line (suggestion count,
  confirmed/rejected/open) with a jump-to-node link and an export of the
  reviewed decisions.

There is no dedicated alignment screen — an individual's tree looks and
behaves exactly like the collective's, with alignment as a layer on top of
it, not a different interface next to it.
