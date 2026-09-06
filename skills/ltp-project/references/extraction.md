# Reading the document, and what to take from it

## Reading it

Size it first. `ls -l` for bytes, and on macOS:

```bash
mdls -name kMDItemNumberOfPages -raw "$PDF"
```

`(null)` means the metadata is absent, not that the file is broken — read the
first window and find out.

Read in windows of **at most 20 pages** with the `Read` tool's `pages` parameter
(`"1-20"`, `"21-40"`, …). Over about ten pages the parameter is required anyway.

After each window, append to an **extraction ledger** — one line per candidate
claim:

```
locator | verbatim fragment | first-guess view
```

The locator is whatever a person can follow back: a page for a PDF, `path#L<n>`
for a text file, the URL for an issue or a comment.

For anything over roughly 60 pages, write the ledger to a scratch file as you go.
The failure mode on a long document is not misreading it; it is losing pages 1–20
to context pressure and producing, in good faith, a confident file about the
second half only.

### When the pages are scans

Extracted text that is empty, or that arrives with mangled ligatures, run-together
words or hyphens mid-word, means the page is an image being read as one. That is
workable — vision reads a scan — but it is not the same evidence.

Say so. Record the reading conditions in the report header, mark every item from
those pages `low` confidence, and tell the person that the `anthropic-skills:pdf`
skill can OCR a text layer first if they want higher fidelity. Never proceed as
though the text had been clean.

### When the source is not a PDF

A Markdown or text document is read whole. A repository is read selectively:
plans, READMEs, decision records, issues and notes state intent and are the
material; code states behaviour and is evidence for the report's coverage note,
not a source of propositions. An issue export is a backlog — read it in the
reverse mode SKILL.md describes, one candidate `transition` action per item, and
keep the issue URL as the locator so a refusal can point at the exact item.

## What counts as a claim

Keep a sentence only if it **asserts something about the system the document is
about**. Drop:

- headings, running heads, page furniture
- figure and table captions that only label ("Figure 4: Order flow")
- "this report is organised as follows", scope notes, acknowledgements, method
  boilerplate
- any sentence whose subject is the document rather than the world ("we surveyed
  twelve sites", "Section 3 examines picking") — though what such a sentence
  _reports_ often is a claim
- recommendations addressed to the reader rather than statements about the system,
  unless the document also says what they would change

A table row counts only when the row states a claim, not when it is a value in a
series.

## Turning a sentence into a proposition

A proposition is a complete statement someone could agree or disagree with,
readable by a person who has never seen the PDF.

- present tense
- one subject, and it is named — never `it`, `this`, `the above`, `they`
- one claim; a sentence joining two with "and" becomes two propositions
- the source's quantity, direction and hedging preserved ("three days", not "a
  long time")
- aim for under 200 characters; the contract's limit is 2000

Never supply a subject the source does not have. If you cannot say _who or what_,
the sentence is not a proposition — log it under omissions as "no identifiable
subject". Inventing the subject is the single most damaging thing a conversion can
do, because the result reads exactly like reasoning the document did.

| in the document                                             | as a proposition                                                                                                 |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| "Delays are a significant issue."                           | _(omit — no subject, no claim)_                                                                                  |
| "It takes far too long."                                    | _(resolve from context, or omit)_                                                                                |
| "Orders wait ~3 days pre-pick."                             | Orders wait an average of three days before picking begins.                                                      |
| "Batching is driven by forklift capacity and shift length." | Batch size is set by the forklift runs a shift can absorb. **and** Batch size is set by the length of the shift. |

## Identifiers

```
<view>-<kind>-<slug>[-N]

view   g | r | c | f | p | t        goal, current_reality, conflict,
                                   future_reality, prerequisite, transition
kind   e | d | rel | asm | as      entity, designation, relationship,
                                   assumption, assessment
slug   two to four kebab words taken from the statement
-N     only on an actual collision
```

`g-e-ship-same-day`, `g-d-ship-same-day`, `r-rel-batch-causes-wait`,
`r-asm-nothing-else-delays`.

The importer holds **one flat namespace across all five collections**, so a
proposition and the designation naming it would collide if both used the same
slug alone. The `kind` segment is what keeps them apart. Do not check this with a
grep — `id:` also matches `entity_id:`, `relationship_id:` and
`parent_designation_id:`. `bun run check:import` reports the clash with both
paths, which is what you want anyway.

## Provenance

Every entity gets one:

```yaml
provenance:
  path: "warehouse-study.pdf#page=12"
```

Add `author` only when the document names a person or organisation as its author.

This is not decoration. `analyseImport` uses `provenance.path` as the entity's
reported path, so it becomes the locator in the import plan **and in every
refusal message about that proposition**. Write a locator a person can act on,
never a sentence.

## A worked example

Source, page 12 of `warehouse-study.pdf`:

> Orders wait an average of three days before picking begins. This is because
> picking starts only once 200 orders have accumulated, and batch size is in turn
> driven by the number of forklift runs a shift can absorb. Weekly rather than
> per-shift reporting partly explains why the delay has gone unremarked.
> Automation may also contribute. We recommend releasing each order to the pick
> line as it arrives, which would bring picking to within four hours of release.

Six sentences. Four propositions in `current_reality`, two in `future_reality`,
two `causes` links, one `contributes_to`, and two things deliberately left out.

```yaml
ltp:
  schema_version: "1.0"
  project_id: warehouse-throughput
  title: Improve warehouse throughput

  entities:
    - id: r-e-orders-wait
      tree: current_reality
      statement: Orders wait an average of three days before picking begins.
      provenance: { path: "warehouse-study.pdf#page=12" }
    - id: r-e-batch-of-200
      tree: current_reality
      statement: Picking starts only once 200 orders have accumulated.
      provenance: { path: "warehouse-study.pdf#page=12" }
    - id: r-e-batch-set-by-forklifts
      tree: current_reality
      statement: Batch size is set by the number of forklift runs a shift can absorb.
      provenance: { path: "warehouse-study.pdf#page=12" }
    - id: r-e-reported-weekly
      tree: current_reality
      statement: Throughput is reported weekly rather than once per shift.
      provenance: { path: "warehouse-study.pdf#page=12" }
    - id: f-e-release-to-line
      tree: future_reality
      statement: Each order is released to the pick line as it arrives.
      provenance: { path: "warehouse-study.pdf#page=12" }
    - id: f-e-picking-within-four-hours
      tree: future_reality
      statement: Picking begins within four hours of order release.
      provenance: { path: "warehouse-study.pdf#page=12" }

  designations:
    - { id: r-d-orders-wait, entity_id: r-e-orders-wait, role: undesirable_effect }
    - { id: r-d-batch-of-200, entity_id: r-e-batch-of-200, role: intermediate_cause }
    - { id: r-d-batch-set-by-forklifts, entity_id: r-e-batch-set-by-forklifts, role: root_cause }
    - { id: r-d-reported-weekly, entity_id: r-e-reported-weekly, role: observation }
    - { id: f-d-release-to-line, entity_id: f-e-release-to-line, role: injection }
    - {
        id: f-d-picking-within-four-hours,
        entity_id: f-e-picking-within-four-hours,
        role: desired_effect,
      }

  relationships:
    - id: r-rel-batch-causes-wait
      tree: current_reality
      kind: causes
      from_entity_ids: [r-e-batch-of-200]
      to_entity_id: r-e-orders-wait
    - id: r-rel-forklifts-cause-batch
      tree: current_reality
      kind: causes
      from_entity_ids: [r-e-batch-set-by-forklifts]
      to_entity_id: r-e-batch-of-200
    - id: r-rel-reporting-contributes
      tree: current_reality
      kind: contributes_to
      from_entity_ids: [r-e-reported-weekly]
      to_entity_id: r-e-orders-wait
    - id: f-rel-release-causes-four-hours
      tree: future_reality
      kind: causes
      from_entity_ids: [f-e-release-to-line]
      to_entity_id: f-e-picking-within-four-hours

  assumptions: []
  assessments: []
  changes: []
```

The judgment calls, each of which belongs in the report:

- **"Weekly reporting partly explains…"** → `contributes_to`, not `causes`.
  "Partly explains" is a weaker claim and the file has a weaker word for it.
- **"Throughput is reported weekly"** → role `observation`. The document states it
  as fact and never says whether it is a cause; `intermediate_cause` would be a
  claim the author did not make.
- **"Automation may also contribute."** → omitted entirely. No subject, and "may"
  is not an assertion. Two propositions and a link would all be invented.
- **The recommendation → a `future_reality` injection**, not a `transition`
  action. The document says what should be true, not who does what on Monday.
- **No relationship from the change to the problem.** "Releasing each order would
  fix the three-day wait" spans `future_reality` and `current_reality`, and the
  importer refuses relationships across two views. The link is real reasoning the
  format cannot hold; record it, do not force it.
- **No assessment.** The document recommends; it never claims to have established
  a critical root cause.
