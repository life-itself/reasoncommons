# Verification — tree-gen (Stream 1a)

**Date:** 2026-07-11 · **Runner:** Claude (agent, following `SKILL.md`)
**Input:** `"Does remote work increase productivity?"`
**Output:** `verification/2026-07-11-run.tree.json` · **Gold:** `gold/remote-work.tree.json` (from `../../claim-tree-annotation.md`)

## Diff vs gold

| Gold branch | Generated? | Notes |
|---|---|---|
| `whom` — for whom / which roles | yes (`whom`, children `whom-role`/`whom-work`) | same distinctions, slightly different slugs & phrasing |
| `tasks` — for what tasks (solo vs collaborative) | yes, matching ids `tasks-solo`/`tasks-collab` | near-identical |
| `time` — time horizon (short vs long) | yes, matching ids | near-identical |
| `conditions` — setup / management | yes, matching ids | near-identical |
| — | extra: `measure` (how is productivity measured?) | not in gold; a defensible extra distinction, not counted against |

Mechanical checks (python): valid JSON, unique kebab-case ids, root id `q-root`, `kind` consistent (`question` throughout), depth ≤ 3, leaves have `children: []`.

## Verdict

**Pass** — the generated tree covers all four gold major sub-questions (for whom / what tasks / what horizon / what conditions) with equivalent leaf distinctions. One extra branch (`measure`) beyond gold; acceptable per SKILL.md ("rephrasing is fine — coverage of the major distinctions is what matters").

Still to do per SKILL.md: try one *new* claim to check generalisation.
