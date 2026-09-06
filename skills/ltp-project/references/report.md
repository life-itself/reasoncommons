# The conversion report

The report is where everything the YAML cannot hold goes, and it is what makes the
YAML trustworthy. A candidate file on its own asserts a set of claims with no
account of where they came from or what was left behind; a reviewer has no way to
tell a faithful extraction from a confident one. **Nothing is ever dropped
silently.**

Write it to `<slug>.report.md` beside the candidate. Fill every section. "None" is
a real answer and a useful one; an absent section is not.

---

```markdown
# <Title> — conversion report

|                    |                                                              |
| ------------------ | ------------------------------------------------------------ |
| Source             | `warehouse-study.pdf`                                        |
| Digest             | `shasum -a 256` of the source file, one line per file        |
| Pages              | 34                                                           |
| Pages read         | 1–34                                                         |
| Reading conditions | text layer throughout / pages 12–18 are scans read as images |
| Converted          | 2026-08-10                                                   |
| Candidate          | `warehouse-throughput.ltp.yaml`                              |
| `check:import`     | passes, exit 0 — 16 units in 2 waves, nothing excluded       |

## What the file claims

11 propositions, 11 roles, 4 relationships, 1 assumption, 0 assessments.

current_reality 4 future_reality 2 goal 3 prerequisite 2
No conflict view, no transition view. See **Not in this file**.

## Items

| id                  | view            | role               | page | confidence | from the document                       | note                                             |
| ------------------- | --------------- | ------------------ | ---- | ---------- | --------------------------------------- | ------------------------------------------------ |
| r-e-orders-wait     | current_reality | undesirable_effect | 12   | high       | "Orders wait an average of three days"  |                                                  |
| r-e-reported-weekly | current_reality | observation        | 15   | high       | "reported weekly rather than per shift" | role: the document never says what this is for   |
| f-e-release-to-line | future_reality  | injection          | 18   | medium     | "we recommend releasing each order"     | a recommendation read as a change, not as a task |

Confidence: **high** — one sentence states it as fact. **medium** — assembled from
two or more sentences, or the view was a judgment call. **low** — paraphrased
across a section, or read from a scanned page.

## Relationships asserted

| id                          | kind           | from → to                             | page | the sentence that asserts the link                                      |
| --------------------------- | -------------- | ------------------------------------- | ---- | ----------------------------------------------------------------------- |
| r-rel-batch-causes-wait     | causes         | r-e-batch-of-200 → r-e-orders-wait    | 12   | "This is because picking starts only once 200 orders have accumulated." |
| r-rel-reporting-contributes | contributes_to | r-e-reported-weekly → r-e-orders-wait | 15   | "Weekly reporting partly explains why the delay has gone unremarked."   |

If the last column cannot be filled, the relationship should not exist.

## Deliberately omitted

| what                                                  | where | why                                    |
| ----------------------------------------------------- | ----- | -------------------------------------- |
| "Automation may also contribute."                     | p.12  | hedged claim too weak to assert        |
| Releasing orders would fix the three-day wait         | p.18  | cross-view link the importer refuses   |
| "Capacity and shift length together drive batch size" | p.14  | joint causation the format cannot hold |
| "This report is organised as follows…"                | p.1   | boilerplate                            |

Categories, and use these words: hedged claim too weak to assert; cross-view link
the importer refuses; joint causation the format cannot hold; no identifiable
subject; outside the system boundary; duplicate of an earlier claim; boilerplate.

## Judgment calls for the reviewer

1. **Is "throughput is reported weekly" a cause of the delay, or an observation
   about it?** The document states it and calls it a partial explanation. Read as
   an `observation` with a `contributes_to` link. Alternative: `intermediate_cause`
   with a `causes` link, which claims more than page 15 says.
2. **Is the recommendation a solution or a task?** Read as a `future_reality`
   injection, because the document says what should be true and not who does it.
   Alternative: a `transition` action, which would need an actor the document never
   names.

## Validator output

<the tail of `bun run check:import`, verbatim>

## Not in this file

- **No conflict view.** The document never states a dilemma; it treats the delay
  as a straightforward capacity problem.
- **No transition view.** No actions with actors, dates or sequence.
- **No assessments.** The document recommends; it never claims to have established
  a critical root cause.

These are gaps in the source, not in the conversion.
```

---

Two notes on why the sections are shaped this way.

**Judgment calls are questions with options**, deliberately mirroring
`ImportDecision`'s own `question` and `choices` fields. The reviewer answers in the
same form the importer would have asked in, and the answer is directly actionable.

**"Not in this file" exists to stop a reviewer blaming the conversion for a gap in
the document.** Without it, a four-view candidate reads as a failed extraction
rather than an accurate one.
