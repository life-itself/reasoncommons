# Reading `check:import`, and repairing what it says

```bash
bun run check:import reports/ltp/<slug>/<slug>.ltp.yaml
```

Exit codes, and they mean different things:

| exit | meaning                                | what to do                                                  |
| ---- | -------------------------------------- | ----------------------------------------------------------- |
| 0    | the file would import                  | read any warnings, then hand over                           |
| 1    | the file would not import as it stands | repair, re-run                                              |
| 2    | the check could not run at all         | fix the path or the YAML syntax; do not touch the reasoning |

`--strict` also fails on the advisory findings (incoherent roles, judgment calls).
`--json` prints the whole analysis and nothing else.

## Repair rules

- At most **five** iterations. If the same code survives **three**, stop and put
  the specific ambiguity to the person. A sixth attempt on the same code is
  guessing.
- A repair may change an identifier, a role, a view assignment, or drop a
  relationship, an assumption or an assessment.
- **A repair may never invent a proposition.** If a reference dangles, either the
  document contains the missing proposition and you add it with its own
  provenance, or it does not and you drop the unit that referred to it and record
  the omission.
- **A repair may never delete real content to go green.** Dropping a claim the
  document makes, to make a count come out, is the one failure that cannot be
  seen in the output.

## Fatal: nothing could be planned

Reported as an `issue` rather than an exclusion. Nothing else in the output means
anything until it is fixed.

| what you see                                                                       | cause                                                                                                                                   | repair                                                                                                                                                                                               |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `UNREADABLE_DOCUMENT` at `ltp.schema_version` — "Expected string, received number" | `schema_version: 1.0` unquoted is a YAML float                                                                                          | `schema_version: "1.0"`                                                                                                                                                                              |
| `UNREADABLE_DOCUMENT` at `ltp` — "not the interchange format"                      | no top-level `ltp:` block                                                                                                               | wrap everything under `ltp:`                                                                                                                                                                         |
| `UNREADABLE_DOCUMENT` naming a field                                               | a value the schema refuses — a view name, a role, a kind                                                                                | check it against `references/vocabulary.md`; §19.2 of the spec is wrong about view names                                                                                                             |
| `UNSUPPORTED_SCHEMA`                                                               | `schema_version` is not a `1.x` string; the app reads `"1.0"` and `"1.1"` (`SUPPORTED_SCHEMA_VERSIONS` in `src/domain/ltp-document.ts`) | write `"1.0"`, as the example does; `"1.1"` is what an export emits and is only for a file that carries `coverage` or `history`. A later `1.x` minor is read with a notice; another major is refused |
| exit 2, "not valid YAML or JSON"                                                   | a syntax error; the message names the line                                                                                              | fix the syntax; a statement containing `: ` must be quoted                                                                                                                                           |

## Per-unit: refused, while the rest of the file imports

Each of these is an **exclusion**. The file is otherwise fine and the units named
are dropped, which is why a partly-refused file is more dangerous than a broken
one — it imports, quietly incomplete.

| code                       | cause                                                                                                                      | repair                                                                                                                                                               |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DUPLICATE_ID`             | one identifier used twice. The namespace is flat across entities, designations, relationships, assumptions and assessments | give the second use its own identifier; the `<view>-<kind>-<slug>` scheme prevents this                                                                              |
| `UNKNOWN_REFERENCE`        | a reference to an identifier the file never defines                                                                        | define the proposition the document actually contains, or drop the referring unit and record the omission                                                            |
| `UNSUPPORTED_CAUSAL_GROUP` | `from_entity_ids` holds more than one identifier, or `logic.mode` is `compound_and` / `alternative_or`                     | one source per relationship. A joint cause cannot be expressed — pick the dominant one or drop the link, and record the joint claim                                  |
| `CROSS_TREE_RELATIONSHIP`  | `from`, `to` and the relationship's own `tree` are not all the same view                                                   | there is no fix inside the file. Drop the relationship and record it as a cross-view link the importer refuses                                                       |
| `SELF_RELATIONSHIP`        | a proposition leads to itself                                                                                              | usually two extractions of the same sentence. Merge them, then re-point the link                                                                                     |
| `HARD_DEPENDENCY_CYCLE`    | units waiting on each other, typically a `parent_designation_id` loop                                                      | the message names the path. Break it: `goal` ← `critical_success_factor` ← `necessary_condition`, and `cloud_objective` ← `cloud_requirement` ← `cloud_prerequisite` |
| `PREREQUISITE_EXCLUDED`    | this unit only failed because something it names failed                                                                    | not a separate problem. Fix the cause above it and this goes away                                                                                                    |

## Advisory: it imports, and the reasoning does not read

**Incoherent role.** The role is not one the view holds. The file contract permits
this and everything downstream refuses it, so it is worth fixing even though it
does not block an import. Either move the proposition to the view whose role you
meant — the message names it — or use a role the current view holds. `observation`
is always available.

**Judgment calls.** Questions the importer refuses to answer for a team. On a
fresh conversion these are rare, because Create mode compares against nothing.
Copy each into the report's "Judgment calls" section verbatim.

## Nothing would import

`Nothing in this file would import.` The file is schema-valid and holds no
propositions — usually a document that turned out to be a price list, a form or a
narrative with no system in it. Do not pad it. Say what the document is and that
it does not carry reasoning.
