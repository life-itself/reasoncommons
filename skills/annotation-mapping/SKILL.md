---
name: annotation-mapping
description: Map fragments of a source document onto the nodes of an existing claim tree, with a relation label (supports / complicates / limits) and a link back to origin. Use when you have a claim tree (from tree-gen) and a source document and want to attach the document's relevant passages to the right nodes.
---

# annotation-mapping — map a source doc onto a claim tree

Given a **claim tree** (canonical JSON from `tree-gen`) and a **source document**, extract the passages of the document that bear on specific nodes, and emit them as annotations: each a verbatim quote, the node it lands on, a relation label, and a note. This is Stream 1b of the LTP / Issue Tree app.

The tree is the **stable scaffold**; the document is incoming world. AI proposes the mapping; a human confirms/corrects.

## Inputs

1. A claim tree in canonical schema (see `../tree-gen/SKILL.md`). Nodes have stable `id`s — annotations reference them.
2. A source document (text/markdown).

## What to produce

For each passage of the document that clearly bears on a node, one annotation:

- **`quote`** — verbatim span from the source (don't paraphrase; this is the link back to origin).
- **`nodeId`** — the tree node it lands on. **A passage may map to more than one node** — emit one annotation per (passage, node) pair.
- **`relation`** — one of:
  - `supports` — the passage is evidence *for* the claim / a positive answer to the question.
  - `complicates` — it qualifies, tensions, or conditions the claim (e.g. "but only short-term").
  - `limits` — it bounds the scope / generalisability (e.g. "only for this population / task").
- **`note`** — one line on *why* this passage lands on this node with this relation.

**Guidance**
- Land a passage on the **most specific** node it clearly speaks to (prefer `tasks-solo` over `tasks` when the passage is about solo tasks). Also attach to a broader node when the passage genuinely limits/complicates the whole branch.
- Only map passages with a **clear** bearing — skip generic framing. Precision over recall.
- Don't invent nodes. If a strong passage fits no node, note it separately (it may signal the tree is incomplete) but do not fabricate a `nodeId`.

## Output — canonical annotations JSON

```json
{
  "version": "0.1",
  "source": { "id": "bloom-2015", "title": "…", "cite": "…" },
  "tree": "path or id of the tree these annotations attach to",
  "annotations": [
    { "id": "an-1", "nodeId": "q-root", "quote": "Home working led to a 13% improvement in performance", "relation": "supports", "note": "Headline positive result answers the root question." }
  ]
}
```

Emit **only** the JSON object. `id` is a stable per-annotation slug (`an-1`, `an-2`, …).

## Validation

Gold fixture: run against `gold/remote-work.source.md` + the tree `../tree-gen/gold/remote-work.tree.json`; compare output to `gold/remote-work.annotations.json`. "Good enough" = each of the ~5 gold passages lands on the correct node with a sensible relation (exact wording/extra annotations are fine). Then try one *new* doc against the same tree to check it generalises.

## Notes & future improvements

- **Validation is eyeball vs a gold fixture, by choice** — same rationale as `tree-gen`: mapping quality is a judgment call, so an automated scorer would give false signal until we've seen more real output. Later: an LLM-judge / semantic scorer on (passage→node, relation) pairs.
- The relation set (`supports` / `complicates` / `limits`) mirrors the demo's `s` / `c` / `l` keys. Revisit if real docs need finer relations (e.g. `refutes`, `defines`).
- Passages that fit no node are a signal to grow the tree — a future loop could feed these back into `tree-gen`.
