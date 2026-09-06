# The vocabulary, and nothing else

Every value a candidate file may use for `tree`, `role`, `kind` and an assessment
`kind`. Nothing here is a suggestion or an abbreviation. A value not in these
tables is either refused by the file contract or accepted by it and then refused
by everything downstream, and the second is worse than the first.

**Do not take these names from `LTP_RATIFICATION_AND_IMPORT_SPEC.md`.** §19.2 of
that document lists the views as `goal | problem | conflict | solution |
implementation | transition`. Those are the names the _interface_ uses
(`FieldKey` in `src/domain/fields.ts`). The names a _file_ uses are the ones
below, and `problem`, `solution` and `implementation` are not among them.

> **This file is checked against the code.** `tests/unit/skill-vocabulary.test.ts`
> reads the tables here and asserts they equal `TreeTypeSchema`, `NODE_ROLES`,
> `treesForRole`, `RELATIONS` and `LtpAssessmentSchema`. It parses the first
> column of every table row, and the second column of the roles table as a
> comma-separated list. Keep that shape. If the test fails, the code moved and
> this file is now wrong — fix this file, not the test.

## The six views

The `tree` of every entity, relationship and assessment.

| view            | the app calls it | what it argues                                                 |
| --------------- | ---------------- | -------------------------------------------------------------- |
| goal            | goal             | what worthwhile success requires                               |
| current_reality | problem          | the unwanted reality that exists now, and what causes it       |
| conflict        | conflict         | needs that appear to pull in opposite directions               |
| future_reality  | solution         | a change, and the future it produces                           |
| prerequisite    | implement        | what stands in the way, and the conditions for getting past it |
| transition      | task             | what someone actually does, in sequence                        |

## The roles

The `role` of every designation. A designation has no `tree` of its own — it
inherits the view of the proposition it names, so a role has to belong to _that_
view. The file contract does not check this. `roleBelongsInTree` does, later, and
`bun run check:import` reports it as advice.

`observation` and `evidence` belong to all six views. `observation` is the honest
answer when a sentence states something about the system and the document never
says what the statement is for; reach for it rather than guessing at a role that
claims more.

| role                        | views                                                                     | what the sentence has to be doing                                         |
| --------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| goal                        | goal                                                                      | naming the outcome the whole argument is for                              |
| critical_success_factor     | goal                                                                      | naming something without which the goal cannot hold                       |
| necessary_condition         | goal                                                                      | naming something a success factor itself requires                         |
| undesirable_effect          | current_reality, future_reality                                           | naming something happening that nobody wants                              |
| intermediate_cause          | current_reality                                                           | naming a cause that is itself caused by something else                    |
| root_cause                  | current_reality                                                           | naming a cause the document does not explain further                      |
| critical_root_cause         | current_reality                                                           | naming the one root cause the document argues explains the rest           |
| cloud_objective             | conflict                                                                  | naming what both sides of the dilemma are for                             |
| cloud_requirement           | conflict                                                                  | naming a need the objective depends on                                    |
| cloud_prerequisite          | conflict                                                                  | naming the action a requirement is thought to demand                      |
| injection                   | conflict, future_reality                                                  | naming a change that breaks the dilemma or produces the future            |
| desired_effect              | future_reality                                                            | naming what becomes true once the change is made                          |
| implementation_objective    | prerequisite                                                              | naming what has to be achieved for the change to be real                  |
| obstacle                    | prerequisite                                                              | naming what currently stops that objective                                |
| intermediate_objective      | prerequisite                                                              | naming what gets past a specific obstacle                                 |
| transition_existing_reality | transition                                                                | naming the situation a step starts from                                   |
| transition_need             | transition                                                                | naming why that situation has to change                                   |
| transition_action           | transition                                                                | naming what someone does                                                  |
| transition_expected_effect  | transition                                                                | naming what the action is expected to produce                             |
| observation                 | goal, current_reality, conflict, future_reality, prerequisite, transition | stating something about the system whose purpose the document never gives |
| evidence                    | goal, current_reality, conflict, future_reality, prerequisite, transition | reporting a measurement or a source that bears on another claim           |

**Two roles the file contract accepts and no view holds: `vision` and
`higher_level_objective`.** They pass `LtpDocumentSchema`, and nothing downstream
takes them. Never write them. If a sentence reaches past the goal, it is a `goal`
in its own right or it is outside the document's system and belongs in the
report's omissions.

The eight names in `LEGACY_DESIGNATION_ROLES` (`src/domain/graph.ts`) —
`intermediate_effect`, `objective`, `requirement`, `prerequisite`,
`desirable_effect`, `action`, `expected_effect`, `assumption` — exist for rows
written by an earlier version. The import uses the strict enum and refuses them.

## Relationship kinds

The `kind` of every relationship. **Both ends and the relationship's own `tree`
must be the same view**, so no kind here can be used across two views, including
the ones `CROSS_TREE_RELATIONS` documents as legitimately cross-tree.

| kind                   | when the source supports it                                               |
| ---------------------- | ------------------------------------------------------------------------- |
| necessary_for          | the source says the target cannot hold without the source                 |
| causes                 | the source asserts the link plainly: "because", "therefore", "driven by"  |
| contributes_to         | the source says the link is partial: "one factor", "partly explains"      |
| conflicts_with         | the source says the two cannot both be satisfied                          |
| requires               | the source says one thing demands another to proceed                      |
| satisfies              | the source says one thing meets a need another stated                     |
| overcomes              | the source says one thing removes an obstacle                             |
| precedes               | the source puts one action before another in sequence                     |
| produces               | the source says an action yields a specific result                        |
| invalidates_assumption | the source says a change breaks a belief the reasoning rested on          |
| implements             | the source says one thing carries out another                             |
| supersedes             | the source says one claim replaces another                                |
| supports               | the source offers something as backing for a claim                        |
| challenges             | the source offers something as counting against a claim                   |
| refines                | the source restates a claim more precisely                                |
| enables                | the source says one thing makes another possible without making it happen |

`so_that`, `blocks`, `contradicts` and `evidences` are `LEGACY_RELATIONS`. The
import refuses them.

## Assessment kinds

The `kind` of every assessment. Write one only where the document _itself_ draws
the conclusion. A conversion that assesses on the author's behalf is inventing
the part of the reasoning a team is supposed to do.

| kind                      | what it concludes                                                    |
| ------------------------- | -------------------------------------------------------------------- |
| critical_root_cause       | that one root cause explains the effects the argument cares about    |
| breaks_conflict           | that an injection resolves the dilemma without giving up either need |
| validated_solution_branch | that a branch of the future reality holds up                         |
| solution_sufficient       | that the change is enough to reach the goal                          |
| negative_branch_mitigated | that an unwanted effect of the change has been dealt with            |
| implementation_ready      | that the obstacles have objectives against them                      |
| transition_complete       | that the steps cover the change                                      |
| transition_executable     | that the steps can actually be carried out                           |

## Logic modes

`logic.mode` on a relationship may be `necessary` or `sufficient`, or absent.
`compound_and` and `alternative_or` parse and are then refused with
`UNSUPPORTED_CAUSAL_GROUP`. Absent is the normal case.
