# Verification — annotation-mapping (Stream 1b)

**Date:** 2026-07-11 · **Runner:** Claude (agent, following `SKILL.md`)
**Inputs:** tree `../tree-gen/gold/remote-work.tree.json` + doc `gold/remote-work.source.md` (Bloom 2015 Ctrip)
**Output:** `verification/2026-07-11-run.annotations.json` · **Gold:** `gold/remote-work.annotations.json`

## Diff vs gold

The 3 gold annotations from `../../claim-tree-annotation.md` (expanded to 5 (passage, node) pairs in the gold fixture):

| Gold annotation | Node | Relation | Result |
|---|---|---|---|
| an-1 "13% improvement in performance" | `q-root` | supports | **match** (same quote, node, relation) |
| an-2 calls-per-minute in quieter environment | `tasks-solo` | supports | **match** (slightly longer quote span; same node + relation) |
| an-3 gains narrowed on return to office | `time` | complicates | **match** |
| an-4 call-centre setting | `whom` | limits | **match** |
| an-5 call-centre setting | `tasks` | limits | **match** (same passage, second node — per-pair emission works) |

Extra beyond gold: an-6 (satisfaction/attrition → `q-root`, supports) — borderline (satisfaction is not productivity); flagged as weak in its note. Acceptable per gold-fixture criterion ("extra annotations are fine"), but a candidate for tightening the precision guidance.

Mechanical checks (python): every `nodeId` exists in the tree, every `relation` in {supports, complicates, limits}, every `quote` is a verbatim substring of the source doc.

## Verdict

**Pass** — each of the 3 gold fragments lands on the correct node with the gold relation (5/5 (passage, node) pairs matched).

Still to do per SKILL.md: try one *new* doc against the same tree to check generalisation.
