---
name: tree-gen
description: Generate a claim tree (structured decomposition of a top-level claim or question into sub-claims/sub-questions) as canonical JSON. Use when the user gives a claim or question and wants it decomposed into an issue tree / LTP tree.
---

# tree-gen — claim tree generation

Decompose a top-level **claim or question** into a hierarchical tree of sub-claims / sub-questions and emit it as canonical JSON (schema below). This is Stream 1a of the LTP / Issue Tree app.

**Structure only.** The tree carries no scoring, no evidence, no attribution — those are added later by annotation-mapping (Stream 1b). Keep nodes to the decomposition itself.

## Input

A single top-level claim or question, e.g. `"Does remote work increase productivity?"`. Optionally a source document to seed the decomposition from.

## What makes a good tree

- **Each level answers one decomposition question.** The children of a node are the distinctions that evidence will eventually have to land on ("for whom?", "for what tasks?", "over what horizon?").
- **Sibling sets aim to be MECE** — mutually exclusive, collectively exhaustive — but readability beats forcing it.
- **Depth 2–3** for a toy tree. Stop when a node is concrete enough that a document fragment could clearly support/complicate it.
- **Questions stay questions, claims stay claims** — match the `kind` of the root. A question root ("Does X?") yields sub-*questions*; a claim root ("X is true") yields sub-*claims*.
- Node text is short (a phrase, not a paragraph).

## Output — canonical tree JSON

```json
{
  "version": "0.1",
  "root": {
    "id": "q-root",
    "text": "Does remote work increase productivity?",
    "kind": "question",
    "children": [
      {
        "id": "whom",
        "text": "For whom? (which workers / roles?)",
        "kind": "question",
        "children": [
          { "id": "whom-ic",   "text": "Individual contributors vs managers?", "kind": "question", "children": [] },
          { "id": "whom-deep", "text": "Deep-work roles vs collaborative roles?", "kind": "question", "children": [] }
        ]
      }
    ]
  }
}
```

**Node fields**
- `id` — stable, unique, kebab-case slug. Root is always `q-root`. Children use a short semantic slug, optionally prefixed by the parent slug for readability (`whom`, `whom-ic`). Must be unique across the whole tree; downstream annotations reference nodes by `id`.
- `text` — the sub-claim / sub-question, a short phrase.
- `kind` — `"question"` or `"claim"`; matches the root.
- `children` — array of child nodes; `[]` at leaves.

Emit **only** the JSON object, nothing else, so it is machine-consumable.

## Validation

Run against the gold fixture `gold/remote-work.tree.json` (extracted from `../../claim-tree-annotation.md`). Generate a tree for `"Does remote work increase productivity?"` and compare by eye: does it cover the same major branches (for whom / what tasks / what horizon / what conditions)? Rephrasing is fine — coverage of the major distinctions is what matters. Then try one *new* claim to check it generalises.

## Notes & future improvements

- **Validation is eyeball vs a gold fixture, by choice.** At this stage tree quality is a judgment call (coverage of major sub-questions), so an automated node-match scorer would reward string overlap and punish good rephrasings — false signal. Chosen the fixture approach: it gives a reusable canonical artifact that also seeds annotation-mapping (1b) and the UI (1c).
- **Later:** add a semantic auto-scorer (embedding/LLM-judge node matching, not string match) once we've seen enough real outputs to know what "good" looks like. Also consider: node-id slug-collision handling, and a `notes`/`rationale` field per node if it proves useful.
