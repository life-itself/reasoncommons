---
name: ltp-project
description: >
  Produce or repair a Reason Commons LTP project file — `*.ltp.yaml`, the same
  interchange document the app imports and exports (as canonical JSON or as the
  YAML dialect, history included) — from a PDF, a Markdown or text document, a
  repository's plans and issues, a roadmap, or meeting notes, plus a report
  naming every judgment call. Use when asked to turn a document, a repo, a
  plan, an issue export or notes into an ltp.yaml, an LTP project, a six-tree
  model or import-ready reasoning; to extract goals, undesirable effects, root
  causes, conflicts, prerequisites or actions from source material; or when a
  candidate ltp.yaml fails validation and needs repairing. Supersedes the
  `project-ltp` and `pdf-to-ltp` skills.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Source material → candidate `ltp.yaml`

## One skill, two homes

The canonical copy of this skill lives in the Reason Commons app repository
(`Promise-Foundation/reason-commons`, at `.claude/skills/ltp-project/`).
`life-itself/reasoncommons` carries a byte-identical mirror at
`skills/ltp-project/`. Edit the canonical copy, then copy the whole directory
over the mirror; `diff -r` the two before editing either, and if they differ the
mirror is the stale one.

The format is the app's own. What this skill writes is what the app imports
through its attach control, and what the app exports from a space (Integrations →
Export reasoning) as canonical JSON or as the YAML dialect, with the version
series and event history under `history`. A space's export committed to a
connected repository — `.reason-commons/<space-id>.ltp.json` — is therefore a
live, complete example of the format. Do not hand-write anything that format
already carries for you.

## What you produce

Two files and one green command. Never one file.

```
reports/ltp/<slug>/<slug>.ltp.yaml     the candidate
reports/ltp/<slug>/<slug>.report.md    everything the YAML cannot hold
bun run check:import <path>            must exit 0 before you hand anything over
```

In the app repository `reports/` is gitignored, which is correct: a machine wrote
this and a person has to read it before any of it is ratified. In another
repository, write to a path a person will review before it is committed, and say
which one. Use a different path only if asked.

## Read these first

- `references/example-project.ltp.yaml` — the format in full, correct, across all
  six views. Copy its style. It is the same file the app ships as
  `public/example-project.ltp.yaml`, and a unit test holds the two identical.
- `references/vocabulary.md` — the only valid view names, roles, relationship
  kinds and assessment kinds. **Never write one of these from memory.**

Then, as you need them: `references/extraction.md` (reading, segmenting,
propositions, identifiers, a worked example), `references/validation.md` (each
code, its cause, its repair), `references/report.md` (the report's shape).

## Do not take view names from the spec

`LTP_RATIFICATION_AND_IMPORT_SPEC.md` §19.2 lists the views as
`goal | problem | conflict | solution | implementation | transition`. Those are
the _interface's_ names. A file using them is refused. The six values a file uses:

```
goal   current_reality   conflict   future_reality   prerequisite   transition
```

## Procedure

1. **Size the source.** For a PDF: `ls -l`, and
   `mdls -name kMDItemNumberOfPages -raw <pdf>` for a page count. For a
   repository or a folder: list it and decide which files state something about
   the system — plans, READMEs, decision records, issues, notes. Code is evidence
   of behaviour, not of intent; it belongs in the report's coverage note, not in
   propositions.
2. **Read it.** A PDF in windows of at most 20 pages with `Read`'s `pages`
   parameter; a text source whole. Keep an extraction ledger as you go —
   `locator | verbatim fragment | first-guess view` — and write it to a scratch
   file for anything over about 60 pages or a dozen documents.
3. **Note the reading conditions.** Empty or mangled text from a PDF means the
   page is a scan being read as an image. Record it, mark those items low
   confidence, and say that `anthropic-skills:pdf` can OCR a text layer first.
   Never proceed silently.
4. **Segment.** Keep only sentences that assert something about the system. Drop
   headings, page furniture, bare captions, scope notes, and any sentence whose
   subject is the document rather than the world.
5. **Rewrite each as a complete proposition.** Present tense, one named subject,
   one claim, the source's quantity and hedging preserved, no `it` or `this`.
   Never supply a subject the source lacks — that sentence is not a proposition.
6. **Put each in exactly one view.** Wants something true, or a condition for it →
   `goal`. Happening now and unwanted, or a cause of it → `current_reality`. Two
   things pulling against each other → `conflict`. A change to make, or an effect
   expected once made → `future_reality`. Something blocking a change, or a step
   past the block → `prerequisite`. The before and after of a change, or an action
   in sequence → `transition`. Still ambiguous → the view the section is about,
   **and record the call in the report**.
7. **Assign a role that view holds.** From `references/vocabulary.md` only. When
   unsure use `observation` — it is valid in all six views and is how you keep a
   file honest instead of precise-sounding.
8. **Relationships, conservatively.** Default is _no relationship_. See below.
9. **Assumptions.** One per relationship, only where the source names the belief
   the link rests on. Zero is a fine answer.
10. **Assessments.** Only where the source itself draws the conclusion. Default
    is none.
11. **Provenance on every entity** — `provenance: { path: "<locator>" }`, where
    the locator is `<pdf>#page=<n>` for a PDF, `<path>#L<line>` for a text file,
    and the issue or comment URL for a tracker item. This becomes the locator in
    the import plan and in every refusal message about that proposition, so make
    it one a person can act on.
12. **Write both files, then validate and repair.** `bun run check:import <path>`
    from a Reason Commons app checkout — `~/github/reason-commons` unless
    `REASON_COMMONS_DIR` says otherwise — at most five iterations. If the same
    code survives three, stop and put the ambiguity to the person. With no
    checkout at hand, attach the file in the app: the import packet runs the same
    analysis and refuses for the same reasons.

Nothing has to be listed in dependency order. The importer resolves references in
two passes and plans in its own order, so a child may name a parent defined later.

## A plan, a backlog or an issue export

Each task is a candidate `transition` action, and only a candidate. Its "why"
section is the `transition_need`; a "current state" or "context" section is the
`transition_existing_reality`; acceptance criteria that describe something
observable in the world once the work is done are the `transition_expected_effect`.
Criteria that only say when the work is complete are not an effect and go in the
report. A task that traces to no goal or need in the material is recorded in the
report as untraced, never given a reason it does not have. Ordering words ("after",
"blocked by", "first") are `precedes`.

## Relationships: the burden of proof

Emit a relationship only when **a single sentence in the source asserts the
link, unhedged, between two propositions already extracted into the same view.**
Everything weaker goes in the report.

| in the source                                                | what you may write                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------------------- |
| "X because Y", "Y therefore X", "X is driven by Y"           | `causes`                                                                  |
| "one factor is", "partly explains", "among the drivers"      | `contributes_to`, never `causes`                                          |
| "may cause", "might lead to", "could result in"              | nothing; a judgment call                                                  |
| "is associated with", "correlates with"                      | nothing; correlation is not a causal claim                                |
| "we believe", "it appears", "suggests", "is consistent with" | nothing; the belief may become an `assumption` on a link you _did_ assert |
| "A and B together cause C"                                   | pick the dominant cause or omit; record the joint claim                   |

Default kinds per view: `goal` → `necessary_for`; `current_reality` → `causes` or
`contributes_to`; `conflict` → `conflicts_with`; `future_reality` → `causes`;
`prerequisite` → `overcomes`, `necessary_for`; `transition` → `precedes`,
`produces`.

## Three rules never traded away

1. **One flat identifier namespace** across entities, designations, relationships,
   assumptions and assessments. Use `<view>-<kind>-<slug>`:
   `g-e-ship-same-day`, `g-d-ship-same-day`, `r-rel-batch-causes-wait`.
2. **Exactly one identifier in `from_entity_ids`**, and never `logic.mode` of
   `compound_and` or `alternative_or`. Joint causes are refused outright.
3. **A relationship joins two propositions in the same view.** `from`, `to` and
   the relationship's own `tree` must all match. No exceptions, including for the
   kinds documented elsewhere as cross-tree. Such a link is real reasoning the
   format cannot carry — record it, do not force it.

## Stop and ask when

- a PDF has no text layer _and_ the page images are illegible
- the source is not about a system anyone acts on — a novel, a price list, a form,
  or code with no plan, README or issue that says what it is for
- the same validator code survives three repair attempts
- the material is about several unrelated systems, and it is not clear which one
  the project is meant to be

## Never

- invent a proposition to satisfy a dangling reference
- delete real content to make the validator green
- write `vision` or `higher_level_objective` — the file contract accepts them and
  no view holds them
- assess on the author's behalf, when the source only recommends
- hand over the YAML without the report
