# Reason Commons, the project — conversion report

This report is what makes the candidate beside it trustworthy: where every proposition came from, what was left out and why, and which calls a person still has to make. Nothing was dropped silently. It follows the shape the `ltp-project` skill asks for, with three additions the sources demanded: a section on the constraint the current-reality tree tests, a section placing every open issue, and the platform observations the file cites.

|                    |                                                              |
| ------------------ | ------------------------------------------------------------ |
| Sources            | this repository at `origin/main` 37aefee1d004 (`about.md`, `README.md`, `motivation.md`, `NEXT.md`, `talk/2r-research-group/notes.md`, `docs/plans/2026-09-01-site-positioning-and-landing-redesign.md`); `Promise-Foundation/reason-commons` at `05fe3d426aaa` (`docs/`, `features/`, `cucumber.mjs`, one source file); the 17 open issues here, at the revisions in the last section; the hosted platform, observed 2026-09-06 |
| Digest             | a commit sha per repository stands in for a file digest; issues carry their `updatedAt` |
| Read               | the documents named above in full; `docs/product-redesign/REDESIGN_PLAN.md`, `docs/CURRENT_STATE.md`, `docs/business_plan.md`, `docs/reason-commons-manifesto.md`, `docs/product-redesign/jobs_to_be_done.md`, `docs/product-redesign/why_redesign.md`, `docs/E1_DOGFOOD.md`, `docs/THROUGHPUT.md`, `docs/OPERATIONAL_PROJECTION_SPEC.md`, `docs/REASON_COMMONS_PROTOCOL.md`, `docs/LEVERAGE_PLAN.md`, `docs/reason-commons-strategy.ltp.yaml`, the `Feature:` and `Rule:` lines of all 43 feature files |
| Reading conditions | text throughout; no scans. The strategy file was mined for statements, not copied: it does not import and 158 of its 165 entities carry no provenance |
| Converted          | 2026-09-06 |
| Candidate          | `reason-commons.ltp.yaml` |
| `check:import`     | passes, exit 0 — 476 units in 20 waves, nothing excluded, nothing needing a decision; 301 would be safe to ratify unread; `--strict` also exit 0 |

## What the file claims

170 propositions, 170 roles, 132 relationships, 4 assumptions, 0 assessments.

goal 15  current_reality 18  conflict 24  future_reality 25  prerequisite 19  transition 69

All six views are present. The transition view is the largest because adequacy for this file means every open issue placed, with its need and expected effect where the author stated one.

## The goal, and why it is stated the way it is

The documents state the goal at four altitudes and none supersedes the others: the venture's ("We build infrastructure and applications for reality-corrected change. Our first customer is ourselves.", business_plan.md L5–L7), the institution's ("a persistent, governed, cumulative memory of reasons — owned by no single reasoner", manifesto L133), the product job's ("Make collective reasoning durable, inspectable, governable, and portable—without making humans carry the clerical burden", jobs_to_be_done.md L3) and the redesign's ("an epistemic performance environment, not a reasoning editor", REDESIGN_PLAN.md L11). This repository adds a fifth in plain words: "a better way for groups to think together and turn that thinking into action" (about.md L8).

The file takes the plain-words sentence as the goal, because it is the only one both authors have published jointly, it sits at the altitude of the outcome for a group rather than of the product or the company, and it obeys the project's own rule about vocabulary (about.md L12). The other four are not rivals; they answer different questions and each has a slot. Rufus's three strands (about.md L18–L20) are three critical success factors; David's "our first customer is ourselves" is the fourth. The institution's sentence and the product job are necessary conditions under the tooling factor. The redesign's sentence is a decision about the product's form and lives in the future-reality view as the four-destinations injection. The one sourced link across branches is business_plan.md L79: without the ability to improve our own change, "we have no basis for claiming they can improve anyone else's" — which is what makes David's diagnosis a condition of the goal rather than a preference.

**The throughput definition is not in this file**, because the interchange schema has no slot for it and the app's ratifiable record (`goal_unit`, `time_basis`, `system_boundary`, `counting_rule`, `baseline_rate`, `source`, `status`) hangs off the accepted goal node. Candidates are in the section of that name below.

## Items

Confidence: **high** — one sentence states it as fact, or it was observed directly. **medium** — assembled from two or more sentences, a subject was changed, or the view was a judgment call; the note says which.

| id | view | role | locator | confidence | statement | note |
| --- | --- | --- | --- | --- | --- | --- |
| `g-e-groups-think-and-act` | goal | goal | `about.md#L8` | high | Groups have a better way to think together and to turn that thinking into action. |  |
| `g-e-tooling-cheap-enough` | goal | critical success factor | `about.md#L10` | high | AI tooling makes holding a group's reasoning as living trees cheap enough to actually use. |  |
| `g-e-communities-adopt` | goal | critical success factor | `about.md#L19` | high | Communities already engaged in complex reasoning adopt the approach and develop the practices that make it stick. |  |
| `g-e-2r-living-laboratory` | goal | critical success factor | `about.md#L20` | high | The system is applied within Second Renaissance, coordinating strategic thinking across an active community whose contributions currently stay fragmented. |  |
| `g-e-first-customer-ourselves` | goal | critical success factor | [docs/business_plan.md#L7](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/business_plan.md#L7) | medium | The group building Reason Commons is its own first customer. | the source says 'our first customer is ourselves' of the company; read as the group that builds the app |
| `g-e-improves-own-change` | goal | necessary condition | [docs/business_plan.md#L79](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/business_plan.md#L79) | medium | Reason Commons improves the developing group's ability to change itself. | a conditional sentence read as the condition it names |
| `g-e-protocol-governs-dev` | goal | necessary condition | [docs/business_plan.md#L75](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/business_plan.md#L75) | high | The common protocol governs product development and resource allocation. |  |
| `g-e-cheaper-to-know` | goal | necessary condition | [docs/product-redesign/jobs_to_be_done.md#L5](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/jobs_to_be_done.md#L5) | medium | It is cheaper for the group to know what it believes, why, and who stands behind it than not to know. | 'for the group' added to the project's master criterion |
| `g-e-no-clerical-burden` | goal | necessary condition | [docs/product-redesign/jobs_to_be_done.md#L3](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/jobs_to_be_done.md#L3) | high | Humans do not carry the clerical burden of producing the structure of collective reasoning. |  |
| `g-e-rigour-without-vocabulary` | goal | necessary condition | `about.md#L12` | high | Reason Commons keeps the Logical Thinking Process's rigour without requiring its vocabulary. |  |
| `g-e-memory-owned-by-none` | goal | necessary condition | [docs/reason-commons-manifesto.md#L133](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/reason-commons-manifesto.md#L133) | high | The memory of reasons is persistent, governed, cumulative, and owned by no single reasoner. |  |
| `g-e-work-is-not-change` | goal | necessary condition | [docs/product-redesign/REDESIGN_PLAN.md#L119](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L119) | high | Completing an action records execution, and observation determines what happened. |  |
| `g-e-ai-no-silent-authority` | goal | necessary condition | [docs/product-redesign/REDESIGN_PLAN.md#L125](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L125) | high | AI drafts and analyzes but does not silently acquire authority. |  |
| `g-e-judgeable-from-site` | goal | necessary condition | `about.md#L14` | high | Outsiders can judge from what is published whether Reason Commons is worth adopting, joining, or funding. |  |
| `g-e-2r-contributions-improve` | goal | necessary condition | `talk/2r-research-group/notes.md#L82` | high | Today's contributions improve Second Renaissance's reasoning and cause useful things to happen. |  |
| `r-e-no-dogfood-result` | current_reality | undesirable effect | [docs/E1_DOGFOOD.md#L3](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/E1_DOGFOOD.md#L3) | high | No completed real dogfood result is recorded in the app repository. |  |
| `r-e-2r-space-no-contributions` | current_reality | undesirable effect | `reason-commons.report.md#platform-observations-2026-09-06` | high | The 2R space named Reason Commons Focus holds 67 accepted nodes and zero contributions. |  |
| `r-e-issues-why-not-stated` | current_reality | undesirable effect | `reason-commons.report.md#platform-observations-2026-09-06` | high | The issues projected from the 2R space read 'Why this matters: Not yet stated.' |  |
| `r-e-group-reasons-in-chat` | current_reality | undesirable effect | `reason-commons.report.md#platform-observations-2026-09-06` | high | The developing group's decisions are recorded in prose by assistants and discussed in Discord and Docs, and the app repository has no space of its own. |  |
| `r-e-issue-sets-unrelated` | current_reality | undesirable effect | `reason-commons.report.md#platform-observations-2026-09-06` | high | Issues #32 to #37 state no relationship to issues #4 to #24 beyond three cross-references. |  |
| `r-e-site-says-no-app` | current_reality | undesirable effect | `README.md#L12` | high | The site says there is no app to log into yet, while the hosted app has three redesign phases admitted. |  |
| `r-e-r3-not-admitted` | current_reality | undesirable effect | [docs/CURRENT_STATE.md#L13](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L13) | high | Redesign phase R3 is not admitted, and the single red scenario 04:43 waits on a decision that is David's. |  |
| `r-e-newest-ratifier-unreachable` | current_reality | undesirable effect | [docs/CURRENT_STATE.md#L630](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L630) | high | The ratifier of the newest accepted change is the one ratifier no reader can reach. |  |
| `r-e-agent-turn-not-deployed` | current_reality | undesirable effect | [docs/CURRENT_STATE.md#L232](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L232) | high | The agent-turn function has not run against a live provider since its rewrite, and deploying it is David's. |  |
| `r-e-narrative-not-deployed` | current_reality | undesirable effect | [docs/CURRENT_STATE.md#L235](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L235) | high | The realize-narrative function is written and bundle-checked and not deployed. |  |
| `r-e-evidence-expensive` | current_reality | undesirable effect | [docs/CURRENT_STATE.md#L505](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L505) | high | The hosted project has a daily sign-up ceiling, so whole-profile acceptance runs must be budgeted. |  |
| `r-e-sequencing-premises-differ` | current_reality | observation | `motivation.md#L28` | high | Rufus's motivation defers the Second Renaissance application until a toy example works end to end, while issues #32 and #36 make it immediate. |  |
| `r-e-everything-open-is-davids` | current_reality | intermediate cause | [docs/CURRENT_STATE.md#L748](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L748) | high | Every open decision, deployment and admission step routes through David. |  |
| `r-e-assistants-outpace-ratifiers` | current_reality | intermediate cause | `reason-commons.report.md#platform-observations-2026-09-06` | medium | Assistants produce plans, handoffs and issues faster than the two humans ratify them. | assembled from the six issues' creation stamps and the length of the status document |
| `r-e-suite-shares-prod-db` | current_reality | intermediate cause | [docs/CURRENT_STATE.md#L311](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L311) | high | The acceptance suite shares the production database with the running application. |  |
| `r-e-work-order-no-dogfood-step` | current_reality | root cause | [docs/CURRENT_STATE.md#L739](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L739) | high | The immediate work order runs admit R3, then the Model row, then R4 to R5, and contains no dogfood step. |  |
| `r-e-validation-scarce` | current_reality | root cause | [docs/product-redesign/why_redesign.md#L53](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/why_redesign.md#L53) | high | Once generating plausible reasoning is cheap, generation is no longer the scarce resource; validation is. |  |
| `r-e-group-not-using-product` | current_reality | root cause | `reason-commons.report.md#platform-observations-2026-09-06` | medium | The group developing Reason Commons does not hold its own reasoning in Reason Commons. | observed on the platform, not stated in any document; David's own diagnosis in other words |
| `c1-e-objective` | conflict | cloud objective | `talk/2r-research-group/notes.md#L76` | high | A group's thinking accumulates and increasingly results in action. |  |
| `c1-e-req-a` | conflict | cloud requirement | `talk/2r-research-group/notes.md#L78` | high | Conversation stays natural and open. |  |
| `c1-e-req-b` | conflict | cloud requirement | `talk/2r-research-group/notes.md#L78` | high | Reasoning is structured enough to build on. |  |
| `c1-e-pre-a` | conflict | cloud prerequisite | `talk/2r-research-group/notes.md#L79` | high | People contribute normally, in threads and rooms, without filing their thought. |  |
| `c1-e-pre-b` | conflict | cloud prerequisite | `talk/2r-research-group/notes.md#L79` | high | People think in trees and file their thought into the method. |  |
| `c1-e-injection` | conflict | injection | `talk/2r-research-group/notes.md#L79` | high | People contribute normally and the system reveals the structure underneath. |  |
| `c2-e-objective` | conflict | cloud objective | [docs/reason-commons-strategy.ltp.yaml#L10](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/reason-commons-strategy.ltp.yaml#L10) | high | Reason Commons is known to create trustworthy institutional learning worth its full cost. |  |
| `c2-e-req-a` | conflict | cloud requirement | [docs/business_plan.md#L119](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/business_plan.md#L119) | high | The team discovers quickly which parts of the approach work, transfer, or should die. |  |
| `c2-e-req-b` | conflict | cloud requirement | [docs/reason-commons-strategy.ltp.yaml#L301](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/reason-commons-strategy.ltp.yaml#L301) | high | Claims of value rest on evidence that counts as customer value. |  |
| `c2-e-pre-a` | conflict | cloud prerequisite | [docs/business_plan.md#L7](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/business_plan.md#L7) | high | The group uses the product on its own development first. |  |
| `c2-e-pre-b` | conflict | cloud prerequisite | [docs/reason-commons-strategy.ltp.yaml#L302](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/reason-commons-strategy.ltp.yaml#L302) | high | Value is proven with independent teams against a strong conventional baseline. |  |
| `c2-e-injection` | conflict | injection | [docs/business_plan.md#L83](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/business_plan.md#L83) | high | Customer Zero is the first falsification attempt, ahead of an external design partner, a paying customer and repeatable transfer. |  |
| `c3-e-objective` | conflict | cloud objective | [docs/product-redesign/REDESIGN_PLAN.md#L552](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L552) | high | The redesign's claims are true of production behaviour. |  |
| `c3-e-req-a` | conflict | cloud requirement | [docs/product-redesign/REDESIGN_PLAN.md#L804](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L804) | high | Admitted phases are green against production behaviour. |  |
| `c3-e-req-b` | conflict | cloud requirement | [#33#bounded-gate](https://github.com/life-itself/reasoncommons/issues/33#bounded-gate) | high | The dogfood begins without every future redesign phase being complete. |  |
| `c3-e-pre-a` | conflict | cloud prerequisite | [docs/CURRENT_STATE.md#L739](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L739) | medium | R3 is admitted and then the Model row lands before any use of the product on our own work. | the work order's sequence read as a prerequisite of the admit-first requirement |
| `c3-e-pre-b` | conflict | cloud prerequisite | [#37#work](https://github.com/life-itself/reasoncommons/issues/37#work) | medium | The dogfood runs on the deployed build now. | read from #37's 'run a measured dogfood cycle' as the opposing prerequisite |
| `c3-e-injection` | conflict | injection | [#33#acceptance-criteria](https://github.com/life-itself/reasoncommons/issues/33#acceptance-criteria) | high | A dogfood needs a reproducible deployed build with attribution reachable, not another phase tag in the profile. |  |
| `c4-e-objective` | conflict | cloud objective | [docs/product-redesign/REDESIGN_PLAN.md#L268](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L268) | high | A ratifier judges with the whole case available and scarce attention protected. |  |
| `c4-e-req-a` | conflict | cloud requirement | [features/38_decide_workspace.feature#L68](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/features/38_decide_workspace.feature#L68) | high | The decision leads with what could change it. |  |
| `c4-e-req-b` | conflict | cloud requirement | [features/38_decide_workspace.feature#L36](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/features/38_decide_workspace.feature#L36) | high | Nothing consequential is hidden from the case. |  |
| `c4-e-pre-a` | conflict | cloud prerequisite | `reason-commons.report.md#platform-observations-2026-09-06` | medium | The group is shown a short ranked list of what to do next. | the shape in which #32–#37 were delivered, read as the prerequisite of leading with a minimum |
| `c4-e-pre-b` | conflict | cloud prerequisite | `NEXT.md#L8` | medium | The group is shown every open issue flat, with no order. | NEXT.md's flat list read as the prerequisite of hiding nothing |
| `c4-e-injection` | conflict | injection | [docs/product-redesign/REDESIGN_PLAN.md#L250](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L250) | high | Lead with the decision-relative minimum and keep the complete case on dig. |  |
| `f-e-four-destinations` | future_reality | injection | [docs/product-redesign/REDESIGN_PLAN.md#L131](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L131) | high | A reasoning space has exactly four destinations, with conversation as a persistent rail rather than a fifth. |  |
| `f-e-standing-deterministic` | future_reality | injection | [docs/product-redesign/REDESIGN_PLAN.md#L184](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L184) | high | Standing is a deterministic projection whose material spans carry exact source identities and versions. |  |
| `f-e-consequence-ranked-crux` | future_reality | injection | [docs/product-redesign/REDESIGN_PLAN.md#L73](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L73) | high | Standing shows one consequence-ranked crux that explains what, why, why now, and what relies on it. |  |
| `f-e-meaning-checkpoint` | future_reality | injection | [docs/product-redesign/REDESIGN_PLAN.md#L116](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L116) | high | The record never attributes a material normalization to a contributor without confirmation. |  |
| `f-e-standing-reservations` | future_reality | injection | [docs/product-redesign/REDESIGN_PLAN.md#L83](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L83) | high | Dissent is a structured reservation with a stable target, lifecycle events and explicit proceed-with-dissent links. |  |
| `f-e-decision-packet-manifest` | future_reality | injection | [docs/product-redesign/REDESIGN_PLAN.md#L250](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L250) | high | A Decide packet leads with the decision-relative minimum and stores a content-addressed manifest of what was presented. |  |
| `f-e-acceptance-vs-reliance` | future_reality | injection | [docs/product-redesign/REDESIGN_PLAN.md#L117](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L117) | high | Accepting reasoning changes model membership, and authorizing reliance records a bounded operational judgment. |  |
| `f-e-work-items-are-projections` | future_reality | injection | [docs/OPERATIONAL_PROJECTION_SPEC.md#L65](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/OPERATIONAL_PROJECTION_SPEC.md#L65) | high | External work items are projections of transition actions and never define their necessity or expected effect. |  |
| `f-e-provider-neutral-export` | future_reality | injection | [docs/product-redesign/REDESIGN_PLAN.md#L91](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L91) | high | A space's reasoning is exported provider-neutrally with integrity and provenance. |  |
| `f-e-e1-closed-loop-on-own-work` | future_reality | injection | [docs/E1_DOGFOOD.md#L15](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/E1_DOGFOOD.md#L15) | high | The team uses the closed evidence loop on active Reason Commons work. |  |
| `f-e-three-commons` | future_reality | injection | [#32#work](https://github.com/life-itself/reasoncommons/issues/32#work) | high | Three distinct commons exist with recorded purpose, throughput status and authority, and the app-development commons is connected to life-itself/reasoncommons. |  |
| `f-e-start-from-material` | future_reality | injection | [#34#acceptance-criteria](https://github.com/life-itself/reasoncommons/issues/34#acceptance-criteria) | high | Starting a commons leads from existing material to a useful first decision without Logical Thinking Process vocabulary. |  |
| `f-e-adopt-issues-as-proposals` | future_reality | injection | [#35#acceptance-criteria](https://github.com/life-itself/reasoncommons/issues/35#acceptance-criteria) | high | Selected existing GitHub issues enter the commons as bounded proposals, and on acceptance the original issue is adopted rather than duplicated. |  |
| `f-e-progress-not-conflated` | future_reality | desired effect | [#32#establishing-these-boundaries](https://github.com/life-itself/reasoncommons/issues/32#establishing-these-boundaries) | high | Subsequent development has a goal, and the three kinds of progress are not conflated. |  |
| `f-e-prose-not-second-model` | future_reality | desired effect | [docs/product-redesign/REDESIGN_PLAN.md#L197](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L197) | high | Readable prose does not become a second, ungoverned model. |  |
| `f-e-action-without-false-consensus` | future_reality | desired effect | [docs/product-redesign/REDESIGN_PLAN.md#L243](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L243) | high | A decision proceeds with dissent open, and nobody carries the political burden of keeping it alive by hand. |  |
| `f-e-teams-record-checkins` | future_reality | desired effect | [docs/E1_DOGFOOD.md#L16](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/E1_DOGFOOD.md#L16) | high | Teams record check-ins on their transition steps. |  |
| `f-e-trackers-not-competing-plan` | future_reality | desired effect | [docs/OPERATIONAL_PROJECTION_SPEC.md#L19](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/OPERATIONAL_PROJECTION_SPEC.md#L19) | high | An external issue tracker does not become a second, competing model of the plan. |  |
| `f-e-inheritor-five-answers` | future_reality | desired effect | [docs/product-redesign/REDESIGN_PLAN.md#L829](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L829) | high | From Standing alone a newcomer can say what the team thinks is happening, what is disputed, what it does because of it, who authorized reliance, and what would cause another look. |  |
| `f-e-cheaper-than-two-places` | future_reality | desired effect | [#35#expected-benefit-and-check](https://github.com/life-itself/reasoncommons/issues/35#expected-benefit-and-check) | high | Maintaining the commons costs David and Rufus less effort than maintaining both places by hand. |  |
| `f-e-nb-review-backlog` | future_reality | undesirable effect | [docs/product-redesign/REDESIGN_PLAN.md#L927](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L927) | high | The commons becomes an AI reasoning factory that produces a human review backlog. |  |
| `f-e-nb-notification-stream` | future_reality | undesirable effect | [docs/product-redesign/REDESIGN_PLAN.md#L933](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L933) | high | The product becomes a generic notification stream. |  |
| `f-e-nb-tutorial-product` | future_reality | undesirable effect | [docs/product-redesign/REDESIGN_PLAN.md#L934](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L934) | high | The product becomes a tutorial-heavy methodology product. |  |
| `f-e-nb-archive-disconnected` | future_reality | undesirable effect | [docs/product-redesign/REDESIGN_PLAN.md#L936](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L936) | high | The commons becomes a historical archive disconnected from current decisions and due observations. |  |
| `f-e-nb-proxy-counts` | future_reality | undesirable effect | [docs/product-redesign/REDESIGN_PLAN.md#L895](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L895) | medium | Success is read from messages sent, claims created, AI drafts generated or reviews completed. | four excluded proxies gathered into one sentence |
| `p-e-next-work-chosen-from-dogfood` | prerequisite | implementation objective | [#37#acceptance-criteria](https://github.com/life-itself/reasoncommons/issues/37#acceptance-criteria) | high | The next proposed app work has an explicit connection to the agreed goal, an expected effect, and a date or condition for checking it, selected from a recorded dogfood review. |  |
| `p-e-obs-tests-are-not-dogfood` | prerequisite | observation | [docs/E1_DOGFOOD.md#L77](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/E1_DOGFOOD.md#L77) | high | Code fixtures and local or hosted acceptance tests are verification, not dogfood evidence. |  |
| `p-e-obs-migration-not-behaviour` | prerequisite | observation | [docs/product-redesign/REDESIGN_PLAN.md#L571](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L571) | high | Migration application is not evidence that the behaviour above it is complete. |  |
| `p-e-obs-backfill-fabricates` | prerequisite | observation | [docs/product-redesign/REDESIGN_PLAN.md#L918](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L918) | high | Historical backfill can fabricate epistemic standing unless legacy records carry honest labels. |  |
| `p-e-obst-attribution` | prerequisite | obstacle | [docs/CURRENT_STATE.md#L630](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L630) | high | The ratifier of the newest accepted change is reachable from no surface. |  |
| `p-e-io-attribution` | prerequisite | intermediate objective | [docs/CURRENT_STATE.md#L632](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L632) | high | David has decided which surface names the proposer and the ratifier of a change that has just landed. |  |
| `p-e-obst-deployments` | prerequisite | obstacle | [docs/CURRENT_STATE.md#L232](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L232) | high | The agent-turn and realize-narrative functions are not deployed since their rewrite. |  |
| `p-e-io-deployments` | prerequisite | intermediate objective | [#33#work](https://github.com/life-itself/reasoncommons/issues/33#work) | high | Both functions are deployed and their versions are recorded with the tested commit. |  |
| `p-e-obst-test-database` | prerequisite | obstacle | [docs/CURRENT_STATE.md#L311](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L311) | high | The acceptance suite shares the production database, cannot delete the spaces it leaves behind, and is budgeted by the sign-up ceiling. |  |
| `p-e-io-test-database` | prerequisite | intermediate objective | [#33#work](https://github.com/life-itself/reasoncommons/issues/33#work) | high | Browser acceptance tests run against an isolated, reproducible database. |  |
| `p-e-obst-import-coverage` | prerequisite | obstacle | [cucumber.mjs#L25](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/cucumber.mjs#L25) | high | No acceptance step has ever driven a file upload, and the import surface belongs to a phase that is not admitted. |  |
| `p-e-io-import-coverage` | prerequisite | intermediate objective | [#34#work](https://github.com/life-itself/reasoncommons/issues/34#work) | high | Import identity-conflict choices and browser upload coverage are finished before repeated import is relied on. |  |
| `p-e-obst-versions-recorded` | prerequisite | obstacle | [#33#interpretation](https://github.com/life-itself/reasoncommons/issues/33#interpretation) | high | Deployed behaviour can differ from the checkout, so a dogfood result is hard to interpret. |  |
| `p-e-io-versions-recorded` | prerequisite | intermediate objective | [#33#work](https://github.com/life-itself/reasoncommons/issues/33#work) | high | The tested application commit, migrations and deployed function versions are recorded. |  |
| `p-e-obst-commons-3` | prerequisite | obstacle | `reason-commons.report.md#platform-observations-2026-09-06` | high | The group has no space of its own, no agreed goal and no throughput status. |  |
| `p-e-io-commons-3` | prerequisite | intermediate objective | [#32#acceptance-criteria](https://github.com/life-itself/reasoncommons/issues/32#acceptance-criteria) | high | The app-development commons has a stable URL, a distinct purpose, an explicit throughput status, and recorded membership and authority. |  |
| `p-e-obst-adoption-honesty` | prerequisite | obstacle | [docs/product-redesign/REDESIGN_PLAN.md#L918](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L918) | high | Adopting existing issues into the commons could fabricate epistemic standing they never had. |  |
| `p-e-io-adoption-honesty` | prerequisite | intermediate objective | [#35#work](https://github.com/life-itself/reasoncommons/issues/35#work) | high | Adopted issues enter as proposals with their source identity, revision and excerpts preserved and human-written content untouched. |  |
| `p-e-obst-premises-differ` | prerequisite | obstacle | `motivation.md#L28` | high | The two collaborators hold different sequencing premises about the Second Renaissance application. |  |
| `t-e-4-reality` | transition | transition existing reality | [#4#reality](https://github.com/life-itself/reasoncommons/issues/4#reality) | high | The annotation demo does not explain why AI has changed the game. |  |
| `t-e-4-need` | transition | transition need | [docs/reason-commons-manifesto.md#L115](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/reason-commons-manifesto.md#L115) | high | AI removes the translation cost of encoding one's own reasoning into a formal system. |  |
| `t-e-4-action` | transition | transition action | [#4](https://github.com/life-itself/reasoncommons/issues/4) | high | Improve the annotation demo to say that this was always wanted but painful, and that AI has changed that. |  |
| `t-e-12-reality` | transition | transition existing reality | [#12#reality](https://github.com/life-itself/reasoncommons/issues/12#reality) | high | The landing page ships a placeholder where a newsletter signup should be. |  |
| `t-e-12-need` | transition | transition need | `about.md#L30` | high | A low-volume update list is coming for people who want to follow along. |  |
| `t-e-12-action` | transition | transition action | [#12](https://github.com/life-itself/reasoncommons/issues/12) | high | Pick a provider and put the newsletter signup embed in place of the landing page's placeholder. |  |
| `t-e-13-reality` | transition | transition existing reality | [#13#reality](https://github.com/life-itself/reasoncommons/issues/13#reality) | high | The 'See it working' call to action points at the scripted animation. |  |
| `t-e-13-action` | transition | transition action | [#13](https://github.com/life-itself/reasoncommons/issues/13) | high | Add a short screen recording of the four steps, of the real tooling as it comes online, to join or replace the scripted animation. |  |
| `t-e-14-reality` | transition | transition existing reality | [#14#reality](https://github.com/life-itself/reasoncommons/issues/14#reality) | high | The constraints dashboard is linked as a bare 'Prototype' and reads as opaque. |  |
| `t-e-14-action` | transition | transition action | [#14](https://github.com/life-itself/reasoncommons/issues/14) | high | Give the dashboard a short intro page saying what the analysis is, whose constraints it holds, and how to read the trees. |  |
| `t-e-14-effect` | transition | transition expected effect | [#14#so-that](https://github.com/life-itself/reasoncommons/issues/14#so-that) | high | The dashboard works as a demonstration of the method rather than as an unexplained tool. |  |
| `t-e-15-reality` | transition | transition existing reality | [#15#reality](https://github.com/life-itself/reasoncommons/issues/15#reality) | high | The navigation labels 'Introduction' and 'Guide' overlap in what they introduce. |  |
| `t-e-15-action` | transition | transition action | [#15](https://github.com/life-itself/reasoncommons/issues/15) | high | Decide the clean split between Introduction and Guide and whether 'The Forum Doesn't Remember' stays inside Introduction. |  |
| `t-e-17-reality` | transition | transition existing reality | [#17#reality](https://github.com/life-itself/reasoncommons/issues/17#reality) | high | The plain explainer versions carry rough edges inherited from the source drawings. |  |
| `t-e-17-action` | transition | transition action | [#17](https://github.com/life-itself/reasoncommons/issues/17) | high | Edit the original SVGs to fix the three named figure defects in the plain explainer versions. |  |
| `t-e-19-reality` | transition | transition existing reality | [#19#reality](https://github.com/life-itself/reasoncommons/issues/19#reality) | high | The landing page shows Flowershow's file-tree navigation listing internal folders. |  |
| `t-e-19-action` | transition | transition action | [#19](https://github.com/life-itself/reasoncommons/issues/19) | high | Find the Flowershow option that hides the file-tree sidebar on the homepage or globally. |  |
| `t-e-18-reality` | transition | transition existing reality | [#18#reality](https://github.com/life-itself/reasoncommons/issues/18#reality) | high | The Second Renaissance explainer closes on a proposed protocol that has not been built. |  |
| `t-e-18-need` | transition | transition need | [#18](https://github.com/life-itself/reasoncommons/issues/18) | high | The explainer's closing stops being defensible if a year passes and the protocol is still not built. |  |
| `t-e-18-effect` | transition | transition expected effect | [#18#a-year](https://github.com/life-itself/reasoncommons/issues/18#a-year) | medium | By September 2027 the forum-to-model protocol exists or the explainer's closing is revised. | 'a year' from the issue's 2026-09 date, read as a check date |
| `t-e-20-reality` | transition | transition existing reality | [#20#reality](https://github.com/life-itself/reasoncommons/issues/20#reality) | high | Running text clips at the right edge on narrow mobile widths, which is pre-existing theme behaviour. |  |
| `t-e-20-action` | transition | transition action | [#20](https://github.com/life-itself/reasoncommons/issues/20) | high | Check the mobile right-edge clipping on a real device. |  |
| `t-e-20-effect` | transition | transition expected effect | [#20#if-real](https://github.com/life-itself/reasoncommons/issues/20#if-real) | high | The clipping is confirmed or ruled out on a real device. |  |
| `t-e-20-fix-action` | transition | transition action | [#20#theme-level-fix](https://github.com/life-itself/reasoncommons/issues/20#theme-level-fix) | high | Fix the theme's content container padding and overflow-wrap so text no longer clips. |  |
| `t-e-23-reality` | transition | transition existing reality | [#23#reality](https://github.com/life-itself/reasoncommons/issues/23#reality) | medium | The trees are not yet in a machine-readable, version-controlled repository synced with GitHub issues. | the issue's title and one line, restated as the present state |
| `t-e-23-action` | transition | transition action | [#23](https://github.com/life-itself/reasoncommons/issues/23) | high | Put the Second Renaissance tree into a machine-readable git repository, synced with GitHub issues. |  |
| `t-e-23-effect` | transition | transition expected effect | [docs/CURRENT_STATE.md#L266](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L266) | high | The connected repository holds the tree as the platform's export, with its version history, refreshed on every sync. |  |
| `t-e-23-dr-action` | transition | transition action | [#23#d-r-tree](https://github.com/life-itself/reasoncommons/issues/23#d-r-tree) | high | Put the David-and-Rufus tree into the same machine-readable, version-controlled form. |  |
| `t-e-24-reality` | transition | transition existing reality | [#24#deep-link](https://github.com/life-itself/reasoncommons/issues/24#deep-link) | high | There is no deep link to an individual tree, so trees cannot be shared directly. |  |
| `t-e-24-viewer-need` | transition | transition need | [#24#viewer](https://github.com/life-itself/reasoncommons/issues/24#viewer) | high | The viewer is standalone, embeddable and usable from the command line. |  |
| `t-e-24-action` | transition | transition action | [#24](https://github.com/life-itself/reasoncommons/issues/24) | high | Split the viewer and the editor into separate components. |  |
| `t-e-24-links-need` | transition | transition need | [#24#hard-links](https://github.com/life-itself/reasoncommons/issues/24#hard-links) | high | Hard links exist so that trees can be shared directly. |  |
| `t-e-24-links-action` | transition | transition action | [#37#work](https://github.com/life-itself/reasoncommons/issues/37#work) | high | Check the existing focus addresses and public reading against the need for shareable tree links. |  |
| `t-e-32-reality` | transition | transition existing reality | [#32#reality](https://github.com/life-itself/reasoncommons/issues/32#reality) | medium | Three separate commons have been proposed, and today the group's work is not held apart by commons. | assembled from #32's opening sentence and the platform observation that the app repository has no space |
| `t-e-32-need` | transition | transition need | [#32#need](https://github.com/life-itself/reasoncommons/issues/32#need) | high | Subsequent development has a goal, and the three kinds of progress are kept apart. |  |
| `t-e-32-action` | transition | transition action | [#32](https://github.com/life-itself/reasoncommons/issues/32) | high | Establish the three commons with their purpose, membership, decision authority and throughput status, and connect the app-development commons to life-itself/reasoncommons. |  |
| `t-e-32-effect` | transition | transition expected effect | [#32#expected-benefit-and-check](https://github.com/life-itself/reasoncommons/issues/32#expected-benefit-and-check) | high | David and Rufus can identify which commons owns a contribution, a decision and a result without reconstructing the distinction from chat. |  |
| `t-e-33-reality` | transition | transition existing reality | [#33#reality](https://github.com/life-itself/reasoncommons/issues/33#reality) | high | Deployed behaviour differs from the checkout and browser tests interfere with the live application. |  |
| `t-e-33-need` | transition | transition need | [#33#need](https://github.com/life-itself/reasoncommons/issues/33#need) | medium | Dogfood results are interpretable rather than confounded by deployment differences or test interference. | assembled from #33's opening sentence |
| `t-e-33-action` | transition | transition action | [#33](https://github.com/life-itself/reasoncommons/issues/33) | high | Establish a reproducible app baseline: an isolated test database, recorded versions, reachable attribution and one verified run summary. |  |
| `t-e-33-effect` | transition | transition expected effect | [#33#expected-benefit-and-check](https://github.com/life-itself/reasoncommons/issues/33#expected-benefit-and-check) | high | David and Rufus can attribute dogfood friction to the product rather than to an unknown deployment or test outage. |  |
| `t-e-34-reality` | transition | transition existing reality | [#34#reality](https://github.com/life-itself/reasoncommons/issues/34#reality) | high | A new commons gives too little guidance about what to bring and what useful result to expect. |  |
| `t-e-34-need` | transition | transition need | [#34#acceptance-criteria](https://github.com/life-itself/reasoncommons/issues/34#acceptance-criteria) | high | A participant can start from real material and reach a useful first judgment without the method's vocabulary. |  |
| `t-e-34-action` | transition | transition action | [#34](https://github.com/life-itself/reasoncommons/issues/34) | high | Make starting a commons lead from existing material to a useful first decision. |  |
| `t-e-34-effect` | transition | transition expected effect | [#34#expected-benefit-and-check](https://github.com/life-itself/reasoncommons/issues/34#expected-benefit-and-check) | high | A participant reaches a useful first judgment with less facilitator explanation and correction work. |  |
| `t-e-35-reality` | transition | transition existing reality | [#35#reality](https://github.com/life-itself/reasoncommons/issues/35#reality) | high | The sync projects accepted actions and reconciles existing mappings, and creating an issue does not import it into the app. |  |
| `t-e-35-need` | transition | transition need | [#35#need](https://github.com/life-itself/reasoncommons/issues/35#need) | high | The repository stays the familiar collaboration surface while its work is connected to the commons' goal and reasoning. |  |
| `t-e-35-action` | transition | transition action | [#35](https://github.com/life-itself/reasoncommons/issues/35) | high | Bring a small set of selected existing issues into the commons as reviewable proposals, adopting the original issue on acceptance. |  |
| `t-e-35-effect` | transition | transition expected effect | [#35#expected-benefit-and-check](https://github.com/life-itself/reasoncommons/issues/35#expected-benefit-and-check) | high | David and Rufus can explain why selected work matters and what it should change while continuing to work from GitHub. |  |
| `t-e-36-reality` | transition | transition existing reality | [#36#reality](https://github.com/life-itself/reasoncommons/issues/36#reality) | high | Research activity and a proposed change are not yet an accepted update in the receiving model. |  |
| `t-e-36-need` | transition | transition need | [#36#need](https://github.com/life-itself/reasoncommons/issues/36#need) | high | The Research Group's throughput is a controlled, deliberated update accepted into the Second Renaissance model. |  |
| `t-e-36-action` | transition | transition action | [#36](https://github.com/life-itself/reasoncommons/issues/36) | high | Define and exercise the handoff from the Research Group into the Second Renaissance model on one real case. |  |
| `t-e-36-effect` | transition | transition expected effect | [#36#expected-benefit-and-check](https://github.com/life-itself/reasoncommons/issues/36#expected-benefit-and-check) | high | The group can show what intellectual progress reached the movement's model, why it was accepted and what remains uncertain. |  |
| `t-e-37-reality` | transition | transition existing reality | [#37#reality](https://github.com/life-itself/reasoncommons/issues/37#reality) | high | A completed feature or a larger reasoning graph is not evidence that the software is helping. |  |
| `t-e-37-need` | transition | transition need | [#37#need](https://github.com/life-itself/reasoncommons/issues/37#need) | high | The next app priorities follow observed constraints on the three commons' work. |  |
| `t-e-37-action` | transition | transition action | [#37](https://github.com/life-itself/reasoncommons/issues/37) | high | Run a measured dogfood cycle and select the next app work from its findings. |  |
| `t-e-37-effect` | transition | transition expected effect | [#37#expected-benefit-and-check](https://github.com/life-itself/reasoncommons/issues/37#expected-benefit-and-check) | high | David and Rufus can explain why the next development task is more valuable than alternatives using recorded experience. |  |
| `t-e-0443-reality` | transition | transition existing reality | [docs/CURRENT_STATE.md#L752](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L752) | high | Which surface names the proposer and the ratifier of a change that has just landed is an open question, and David's. |  |
| `t-e-0443-action` | transition | transition action | [docs/CURRENT_STATE.md#L632](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L632) | high | Decide which surface names the proposer and the ratifier of a change that has just landed. |  |
| `t-e-0443-effect` | transition | transition expected effect | [#33#acceptance-criteria](https://github.com/life-itself/reasoncommons/issues/33#acceptance-criteria) | high | Current-change attribution is reachable. |  |
| `t-e-deploy-reality` | transition | transition existing reality | [docs/CURRENT_STATE.md#L232](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L232) | high | The agent-turn function has not run against a live provider since its rewrite, and the realize-narrative function is not deployed. |  |
| `t-e-deploy-action` | transition | transition action | [#33#work](https://github.com/life-itself/reasoncommons/issues/33#work) | high | Deploy the agent-turn and realize-narrative functions and record their versions. |  |
| `t-e-deploy-effect` | transition | transition expected effect | [#33#work](https://github.com/life-itself/reasoncommons/issues/33#work) | high | Both functions are deployed and their versions are recorded with the tested commit. |  |
| `t-e-admit-r3-action` | transition | transition action | [docs/CURRENT_STATE.md#L743](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L743) | high | Admit R3 by adding @phase-r3 and @phase-e9a to the profile in the same change as the code, with the green profile figure recorded. |  |
| `t-e-admit-r3-effect` | transition | transition expected effect | [docs/product-redesign/REDESIGN_PLAN.md#L703](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/product-redesign/REDESIGN_PLAN.md#L703) | high | AI cannot cross the authority boundary, and every consequential reliance links to a decision and a packet manifest. |  |
| `t-e-model-row-action` | transition | transition action | [docs/CURRENT_STATE.md#L745](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L745) | high | Carry out the Model row as specified in MODEL_ROW_RETARGET.md. |  |
| `t-e-r4-r5-action` | transition | transition action | [docs/CURRENT_STATE.md#L746](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L746) | high | Continue R4 to R5 in the redesign plan's dependency ladder. |  |
| `t-e-e1-action` | transition | transition action | [docs/E1_DOGFOOD.md#L15](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/E1_DOGFOOD.md#L15) | high | Use the closed evidence loop on active Reason Commons work, registering the prediction prospectively in a deployed build. |  |
| `t-e-e1-effect` | transition | transition expected effect | [docs/E1_DOGFOOD.md#L16](https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/E1_DOGFOOD.md#L16) | high | Teams record check-ins on their transition steps. |  |

## Relationships asserted

If the last column could not be filled, the relationship does not exist in the file.

| id | kind | from → to | the sentence or structure that carries the link |
| --- | --- | --- | --- |
| `t-rel-4-reality-enables-action` | enables | `t-e-4-reality` → `t-e-4-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-4-need-enables-action` | enables | `t-e-4-need` → `t-e-4-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-12-reality-enables-action` | enables | `t-e-12-reality` → `t-e-12-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-12-need-enables-action` | enables | `t-e-12-need` → `t-e-12-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-13-reality-enables-action` | enables | `t-e-13-reality` → `t-e-13-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-14-reality-enables-action` | enables | `t-e-14-reality` → `t-e-14-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-14-action-produces-effect` | produces | `t-e-14-action` → `t-e-14-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-15-reality-enables-action` | enables | `t-e-15-reality` → `t-e-15-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-17-reality-enables-action` | enables | `t-e-17-reality` → `t-e-17-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-19-reality-enables-action` | enables | `t-e-19-reality` → `t-e-19-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-18-reality-enables-need` | enables | `t-e-18-reality` → `t-e-18-need` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-20-reality-enables-action` | enables | `t-e-20-reality` → `t-e-20-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-20-action-produces-effect` | produces | `t-e-20-action` → `t-e-20-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-20-check-precedes-fix` | precedes | `t-e-20-effect` → `t-e-20-fix-action` | "Needs a real-device check … and, if real, a theme-level fix" — #20 |
| `t-rel-23-reality-enables-action` | enables | `t-e-23-reality` → `t-e-23-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-23-reality-enables-dr-action` | enables | `t-e-23-reality` → `t-e-23-dr-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-23-action-produces-effect` | produces | `t-e-23-action` → `t-e-23-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-24-viewer-need-enables-action` | enables | `t-e-24-viewer-need` → `t-e-24-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-24-reality-enables-links-action` | enables | `t-e-24-reality` → `t-e-24-links-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-24-links-need-enables-action` | enables | `t-e-24-links-need` → `t-e-24-links-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-32-reality-enables-action` | enables | `t-e-32-reality` → `t-e-32-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-32-need-enables-action` | enables | `t-e-32-need` → `t-e-32-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-32-action-produces-effect` | produces | `t-e-32-action` → `t-e-32-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-33-reality-enables-action` | enables | `t-e-33-reality` → `t-e-33-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-33-need-enables-action` | enables | `t-e-33-need` → `t-e-33-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-33-action-produces-effect` | produces | `t-e-33-action` → `t-e-33-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-34-reality-enables-action` | enables | `t-e-34-reality` → `t-e-34-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-34-need-enables-action` | enables | `t-e-34-need` → `t-e-34-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-34-action-produces-effect` | produces | `t-e-34-action` → `t-e-34-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-35-reality-enables-action` | enables | `t-e-35-reality` → `t-e-35-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-35-need-enables-action` | enables | `t-e-35-need` → `t-e-35-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-35-action-produces-effect` | produces | `t-e-35-action` → `t-e-35-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-36-reality-enables-action` | enables | `t-e-36-reality` → `t-e-36-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-36-need-enables-action` | enables | `t-e-36-need` → `t-e-36-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-36-action-produces-effect` | produces | `t-e-36-action` → `t-e-36-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-37-reality-enables-action` | enables | `t-e-37-reality` → `t-e-37-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-37-need-enables-action` | enables | `t-e-37-need` → `t-e-37-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-37-action-produces-effect` | produces | `t-e-37-action` → `t-e-37-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-18-need-enables-36` | enables | `t-e-18-need` → `t-e-36-action` | "Related: #18, the broader unfinished forum-to-model protocol. This is a bounded working case of that ambition" — #36 |
| `t-rel-36-produces-18-effect` | produces | `t-e-36-action` → `t-e-18-effect` | the same sentence in #36: the bounded case is what would make the explainer's closing true |
| `t-rel-24-links-check-part-of-37` | implements | `t-e-24-links-action` → `t-e-37-action` | "Check actual viewer compatibility and source/deep links against #23 and #24" — #37, work |
| `t-rel-32-precedes-35` | precedes | `t-e-32-effect` → `t-e-35-action` | "Depends on the app-development commons being established" — #35 |
| `t-rel-32-precedes-36` | precedes | `t-e-32-effect` → `t-e-36-action` | "Agree who may propose, review and accept changes in the receiving commons" (#36) needs the authority #32 records |
| `t-rel-32-precedes-37` | precedes | `t-e-32-effect` → `t-e-37-action` | "After the Reason Commons goal and provisional throughput are agreed" — #37 |
| `t-rel-32-precedes-23-dr` | precedes | `t-e-32-effect` → `t-e-23-dr-action` | a space has to exist before its tree can be exported; #32 creates it |
| `t-rel-33-precedes-35` | precedes | `t-e-33-effect` → `t-e-35-action` | "Depends on … the relevant import/review path being reliable" — #35 |
| `t-rel-33-precedes-37` | precedes | `t-e-33-effect` → `t-e-37-action` | "Demonstrate the journey before relying on the dogfood measurements." — #33 |
| `t-rel-34-precedes-37` | precedes | `t-e-34-effect` → `t-e-37-action` | "The first dogfood case is establishing the Reason Commons project's own goal and throughput" (#34) and "After the … goal and provisional throughput are agreed" (#37) — two sentences, medium |
| `t-rel-35-precedes-37` | precedes | `t-e-35-effect` → `t-e-37-action` | "Include one app-development decision using selected GitHub issues" — #37 |
| `t-rel-36-precedes-37` | precedes | `t-e-36-effect` → `t-e-37-action` | "… and one Research Group handoff to the movement model" — #37 |
| `t-rel-0443-reality-enables-action` | enables | `t-e-0443-reality` → `t-e-0443-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-0443-action-produces-effect` | produces | `t-e-0443-action` → `t-e-0443-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-0443-precedes-33` | precedes | `t-e-0443-effect` → `t-e-33-action` | "Current-change attribution is reachable." is #33's acceptance criterion; the decision is what makes it reachable |
| `t-rel-deploy-reality-enables-action` | enables | `t-e-deploy-reality` → `t-e-deploy-action` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-deploy-action-produces-effect` | produces | `t-e-deploy-action` → `t-e-deploy-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-deploy-precedes-33` | precedes | `t-e-deploy-effect` → `t-e-33-action` | "verify the live agent's meaning-confirmation path" and "Record … deployed function versions" — #33, work |
| `t-rel-admit-r3-produces-effect` | produces | `t-e-admit-r3-action` → `t-e-admit-r3-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-0443-precedes-admit-r3` | precedes | `t-e-0443-effect` → `t-e-admit-r3-action` | "what this step still needs is 04:43 decided and features 34 and 38 re-run" — CURRENT_STATE.md L743 |
| `t-rel-admit-r3-precedes-model-row` | precedes | `t-e-admit-r3-effect` → `t-e-model-row-action` | "It is gated behind step 3 entirely, not partly" — CURRENT_STATE.md L745 |
| `t-rel-e1-action-produces-effect` | produces | `t-e-e1-action` → `t-e-e1-effect` | the step's own shape: its existing reality and its need enable the action, the action produces its expected effect |
| `t-rel-deploy-precedes-e1` | precedes | `t-e-deploy-effect` → `t-e-e1-action` | "Only a deployed build and a prospectively registered, non-fixture run can start this evaluation" — E1_DOGFOOD.md L6 |
| `p-rel-io-attribution-overcomes` | overcomes | `p-e-io-attribution` → `p-e-obst-attribution` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-attribution-for-objective` | necessary_for | `p-e-io-attribution` → `p-e-next-work-chosen-from-dogfood` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-deployments-overcomes` | overcomes | `p-e-io-deployments` → `p-e-obst-deployments` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-deployments-for-objective` | necessary_for | `p-e-io-deployments` → `p-e-next-work-chosen-from-dogfood` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-test-database-overcomes` | overcomes | `p-e-io-test-database` → `p-e-obst-test-database` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-test-database-for-objective` | necessary_for | `p-e-io-test-database` → `p-e-next-work-chosen-from-dogfood` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-import-coverage-overcomes` | overcomes | `p-e-io-import-coverage` → `p-e-obst-import-coverage` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-import-coverage-for-objective` | necessary_for | `p-e-io-import-coverage` → `p-e-next-work-chosen-from-dogfood` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-versions-recorded-overcomes` | overcomes | `p-e-io-versions-recorded` → `p-e-obst-versions-recorded` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-versions-recorded-for-objective` | necessary_for | `p-e-io-versions-recorded` → `p-e-next-work-chosen-from-dogfood` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-commons-3-overcomes` | overcomes | `p-e-io-commons-3` → `p-e-obst-commons-3` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-commons-3-for-objective` | necessary_for | `p-e-io-commons-3` → `p-e-next-work-chosen-from-dogfood` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-adoption-honesty-overcomes` | overcomes | `p-e-io-adoption-honesty` → `p-e-obst-adoption-honesty` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `p-rel-io-adoption-honesty-for-objective` | necessary_for | `p-e-io-adoption-honesty` → `p-e-next-work-chosen-from-dogfood` | prerequisite-tree structure: the intermediate objective overcomes its obstacle and is necessary for the implementation objective |
| `f-rel-three-commons-cause-focus` | causes | `f-e-three-commons` → `f-e-progress-not-conflated` | "Establishing these boundaries inside the application gives subsequent development a goal and prevents the three kinds of progress being conflated." — #32 |
| `f-rel-deterministic-standing-no-second-model` | causes | `f-e-standing-deterministic` → `f-e-prose-not-second-model` | "Deterministic traceability prevents readable prose from becoming a second, ungoverned model." — REDESIGN_PLAN.md L197 |
| `f-rel-reservations-allow-action` | causes | `f-e-standing-reservations` → `f-e-action-without-false-consensus` | "A durable reservation allows action without false consensus and removes the political burden…" — REDESIGN_PLAN.md L243 |
| `f-rel-e1-loop-produces-checkins` | causes | `f-e-e1-closed-loop-on-own-work` → `f-e-teams-record-checkins` | the registered prediction: action → expected effect — E1_DOGFOOD.md L15–L16 |
| `f-rel-projections-no-second-plan` | causes | `f-e-work-items-are-projections` → `f-e-trackers-not-competing-plan` | "one authoritative account of required attention and one projection discipline" — OPERATIONAL_PROJECTION_SPEC.md L19; stated as purpose, so medium |
| `c1-rel-pre-a-for-req-a` | necessary_for | `c1-e-pre-a` → `c1-e-req-a` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c1-rel-pre-b-for-req-b` | necessary_for | `c1-e-pre-b` → `c1-e-req-b` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c1-rel-req-a-for-objective` | necessary_for | `c1-e-req-a` → `c1-e-objective` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c1-rel-req-b-for-objective` | necessary_for | `c1-e-req-b` → `c1-e-objective` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c1-rel-conflict` | conflicts_with | `c1-e-pre-a` → `c1-e-pre-b` | "The conflict as two columns: what people want … vs what accumulation needs" — talk notes L78 |
| `c1-rel-injection-satisfies-a` | satisfies | `c1-e-injection` → `c1-e-req-a` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c1-rel-injection-satisfies-b` | satisfies | `c1-e-injection` → `c1-e-req-b` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c2-rel-pre-a-for-req-a` | necessary_for | `c2-e-pre-a` → `c2-e-req-a` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c2-rel-pre-b-for-req-b` | necessary_for | `c2-e-pre-b` → `c2-e-req-b` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c2-rel-req-a-for-objective` | necessary_for | `c2-e-req-a` → `c2-e-objective` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c2-rel-req-b-for-objective` | necessary_for | `c2-e-req-b` → `c2-e-objective` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c2-rel-conflict` | conflicts_with | `c2-e-pre-a` → `c2-e-pre-b` | "Founder dogfooding, check-in frequency and product usage do not establish incremental customer value" — strategy file L301, against "Our first customer is ourselves" — business_plan.md L7 |
| `c2-rel-injection-satisfies-a` | satisfies | `c2-e-injection` → `c2-e-req-a` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c2-rel-injection-satisfies-b` | satisfies | `c2-e-injection` → `c2-e-req-b` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c3-rel-pre-a-for-req-a` | necessary_for | `c3-e-pre-a` → `c3-e-req-a` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c3-rel-pre-b-for-req-b` | necessary_for | `c3-e-pre-b` → `c3-e-req-b` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c3-rel-req-a-for-objective` | necessary_for | `c3-e-req-a` → `c3-e-objective` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c3-rel-req-b-for-objective` | necessary_for | `c3-e-req-b` → `c3-e-objective` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c3-rel-conflict` | conflicts_with | `c3-e-pre-a` → `c3-e-pre-b` | the work order (CURRENT_STATE.md L739) against #33's "not a request to complete every future redesign phase"; the opposition is the documents' own framing |
| `c3-rel-injection-satisfies-a` | satisfies | `c3-e-injection` → `c3-e-req-a` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c3-rel-injection-satisfies-b` | satisfies | `c3-e-injection` → `c3-e-req-b` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c4-rel-pre-a-for-req-a` | necessary_for | `c4-e-pre-a` → `c4-e-req-a` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c4-rel-pre-b-for-req-b` | necessary_for | `c4-e-pre-b` → `c4-e-req-b` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c4-rel-req-a-for-objective` | necessary_for | `c4-e-req-a` → `c4-e-objective` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c4-rel-req-b-for-objective` | necessary_for | `c4-e-req-b` → `c4-e-objective` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c4-rel-conflict` | conflicts_with | `c4-e-pre-a` → `c4-e-pre-b` | feature 38's two rules, L36 and L68, hold both wants; the opposition is the documents' own framing |
| `c4-rel-injection-satisfies-a` | satisfies | `c4-e-injection` → `c4-e-req-a` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `c4-rel-injection-satisfies-b` | satisfies | `c4-e-injection` → `c4-e-req-b` | cloud structure: prerequisites hold up requirements, requirements hold up the objective, the injection satisfies both requirements |
| `r-rel-0443-blocks-admission` | causes | `r-e-newest-ratifier-unreachable` → `r-e-r3-not-admitted` | "the reason is now one thing rather than three: … 04:43, waits on a decision that is David's" — CURRENT_STATE.md L13 |
| `r-rel-shared-db-costly-evidence` | causes | `r-e-suite-shares-prod-db` → `r-e-evidence-expensive` | "the BDD suite sharing the production database with the running application is the condition that makes the question unanswerable" — CURRENT_STATE.md L311 |
| `r-rel-davids-gate-r3` | causes | `r-e-everything-open-is-davids` → `r-e-r3-not-admitted` | "waits on a decision that is David's" — CURRENT_STATE.md L13 |
| `r-rel-davids-gate-deploy` | causes | `r-e-everything-open-is-davids` → `r-e-agent-turn-not-deployed` | "deploying is David's" — CURRENT_STATE.md L232 |
| `r-rel-davids-gate-no-result` | contributes_to | `r-e-everything-open-is-davids` → `r-e-no-dogfood-result` | "Only a deployed build and a prospectively registered, non-fixture run can start this evaluation" (E1_DOGFOOD.md L6) with "deploying is David's" (CURRENT_STATE.md L232) — two sentences, so `contributes_to` |
| `r-rel-validation-scarce-outpace` | contributes_to | `r-e-validation-scarce` → `r-e-assistants-outpace-ratifiers` | "generation is no longer the scarce resource. Validation is." — why_redesign.md L53, a general claim applied to this group, so `contributes_to` |
| `r-rel-not-using-reasons-in-chat` | causes | `r-e-group-not-using-product` → `r-e-group-reasons-in-chat` | "reasoning buried in a transcript is not operationally available — nobody can query it, challenge it, or build on it" — manifesto L17, the mechanism applied to ourselves; see judgment call 6 |
| `r-rel-not-using-why-not-stated` | contributes_to | `r-e-group-not-using-product` → `r-e-issues-why-not-stated` | the managed section prints 'Not yet stated.' for any action without a linked reality or need (operational-projection.ts L204); the 2R space is commons 2, so `contributes_to` |
| `r-rel-no-step-no-result` | contributes_to | `r-e-work-order-no-dogfood-step` → `r-e-no-dogfood-result` | the work order (CURRENT_STATE.md L739–L746) lists no dogfood step; absence, so `contributes_to` |
| `g-rel-tooling-cheap-enough-for-goal` | necessary_for | `g-e-tooling-cheap-enough` → `g-e-groups-think-and-act` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-communities-adopt-for-goal` | necessary_for | `g-e-communities-adopt` → `g-e-groups-think-and-act` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-2r-living-laboratory-for-goal` | necessary_for | `g-e-2r-living-laboratory` → `g-e-groups-think-and-act` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-first-customer-ourselves-for-goal` | necessary_for | `g-e-first-customer-ourselves` → `g-e-groups-think-and-act` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-improves-own-change-for-first-customer-ourselves` | necessary_for | `g-e-improves-own-change` → `g-e-first-customer-ourselves` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-protocol-governs-dev-for-first-customer-ourselves` | necessary_for | `g-e-protocol-governs-dev` → `g-e-first-customer-ourselves` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-cheaper-to-know-for-first-customer-ourselves` | necessary_for | `g-e-cheaper-to-know` → `g-e-first-customer-ourselves` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-no-clerical-burden-for-tooling-cheap-enough` | necessary_for | `g-e-no-clerical-burden` → `g-e-tooling-cheap-enough` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-rigour-without-vocabulary-for-tooling-cheap-enough` | necessary_for | `g-e-rigour-without-vocabulary` → `g-e-tooling-cheap-enough` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-memory-owned-by-none-for-tooling-cheap-enough` | necessary_for | `g-e-memory-owned-by-none` → `g-e-tooling-cheap-enough` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-work-is-not-change-for-tooling-cheap-enough` | necessary_for | `g-e-work-is-not-change` → `g-e-tooling-cheap-enough` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-ai-no-silent-authority-for-tooling-cheap-enough` | necessary_for | `g-e-ai-no-silent-authority` → `g-e-tooling-cheap-enough` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-judgeable-from-site-for-communities-adopt` | necessary_for | `g-e-judgeable-from-site` → `g-e-communities-adopt` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-2r-contributions-improve-for-2r-living-laboratory` | necessary_for | `g-e-2r-contributions-improve` → `g-e-2r-living-laboratory` | goal-tree structure: the condition below holds up the one above (judgment call 4) |
| `g-rel-self-improvement-basis-for-adoption` | necessary_for | `g-e-improves-own-change` → `g-e-communities-adopt` | "If our systems cannot improve the organization's ability to change itself, we have no basis for claiming they can improve anyone else's." — business_plan.md L79 |

## Assumptions

| id | on | statement | source |
| --- | --- | --- | --- |
| `r-asm-transcript-not-available` | `r-rel-not-using-reasons-in-chat` | Reasoning buried in a transcript is not operationally available: nobody can query it, challenge it, or build on it. | manifesto L17 |
| `c1-asm-structure-needs-tree-thinkers` | `c1-rel-conflict` | Structure only arrives if the people contributing think in trees themselves. | the belief the talk's 'what if people didn't have to think in trees?' (notes L79) is written against |
| `c2-asm-founder-use-is-not-value` | `c2-rel-conflict` | Founder dogfooding, check-in frequency and product usage do not establish incremental customer value. | strategy file L301 |
| `f-asm-e1-necessary-conditions` | `f-rel-e1-loop-produces-checkins` | At least one active space has an accepted transition action and a person responsible for checking its outcome. | E1_DOGFOOD.md L20–L21 |

## Deliberately omitted

| what | where | why |
| --- | --- | --- |
| every "issue X serves goal node Y" link | the placement section below | cross-view link the importer refuses; carried in the transition need's wording and in the table |
| "#33 overcomes the shared-database obstacle" | #33 work, CURRENT_STATE.md L311 | cross-view link the importer refuses (transition ↔ prerequisite) |
| "the four destinations address graph archaeology" | REDESIGN_PLAN.md L131, why_redesign.md L173 | cross-view link the importer refuses (future ↔ current reality) |
| "adopting seventeen issues at once causes a review backlog" | REDESIGN_PLAN.md L927 | hedged claim too weak to assert; the negative branch is carried, the causal edge is not |
| "the group not using the product caused #32–#37 to state no relationship to #4–#24" | the issues | no sentence asserts it; recorded as judgment call 7 instead of forced |
| E1's two necessary conditions as joint causes of the check-in effect | E1_DOGFOOD.md L20–L21 | joint causation the format cannot hold; written as one assumption on the link |
| the toy-first vs 2R-first disagreement as a cloud | motivation.md L28 vs #32, #36 | the later talk and its live contributions appear to supersede L28; held as an observation and question R1 |
| the remaining seven constitution rules, the seven scarce acts, the definition of complete, the eighteen jobs | REDESIGN_PLAN.md L116–L127, L15–L21, L967–L981; jobs_to_be_done.md | a second tranche; nothing the seventeen issues hang from |
| the pre-redesign product's undesirable effects | why_redesign.md L7, L173, L177, L396, L572 | historical; largely addressed by R0–R2, and not what the issues turn on |
| the strategy file's four clouds (authority vs scale, accountability vs candor, open commons vs confidentiality, general protocol vs wedge) | reason-commons-strategy.ltp.yaml L202–L235 | a second tranche; they need re-sourcing to the documents they summarise |
| an intermediate objective for the sequencing-premises obstacle | motivation.md L28 | no source sentence names the resolving condition; question R1 does |
| the Lovable private registry blocking a clean install | observed while reinstalling dependencies | no locator in any document; question D5 |
| the five-card onboarding generated from `src/domain/fields.ts` | the 2026-09-06 dialogue | dialogue only; partly #34's work, not a proposition in a source |
| an explained-prioritisation notification | the 2026-09-06 dialogue | dialogue only, and it risks REDESIGN_PLAN.md L933 |
| update the site's "There's no app to log into yet" once commons 3 exists | README.md L12, about.md L14 | an untraced task: no issue, no goal sentence; proposed as a new issue for Rufus |
| the Discord invite link | NEXT.md L24 on the previous main | untraced; no goal sentence |
| "#13 supersedes #4" | #13 "Related: #4" | the issue says join or replace; no `supersedes` written; question R4 |

## Judgment calls for the reviewer

1. **Which sentence is the goal?** about.md L8, "a better way for groups to think together and turn that thinking into action" — the only jointly published statement, at the group's altitude, in the project's own register. *Alternative:* jobs_to_be_done.md L3 as the goal with about.md L8 as a critical success factor; that puts the product where the group should be.
2. **Whose first customer?** business_plan.md L7 says "our" of the company; `g-e-first-customer-ourselves` reads it as the group that builds the app, which is commons 3's system. *Alternative:* keep the company as subject and treat the group's self-use as a necessary condition under it; that imports the venture into a two-person commons.
3. **"For the group" in the master criterion** `g-e-cheaper-to-know` scopes jobs_to_be_done.md L5 to the group, because the condition is asserted of commons 3. *Alternative:* keep the sentence general; then it is a tooling condition rather than a self-use one.
4. **Are the goal-tree edges asserted?** critical success factor → goal and necessary condition → factor are the tree's structure; only `g-rel-self-improvement-basis-for-adoption` is carried by a sentence (business_plan.md L79). *Alternative:* ratify the fourteen structural edges as convention, or ask for a sentence for each; the example file writes them without one.
5. **Is `r-e-group-not-using-product` the critical root cause?** the file designates it `root_cause` and withholds `critical_root_cause`, because no document draws that conclusion. It reaches the seven project-level undesirable effects; the three engineering effects trace to David as sole gate and to the shared database. David's own phrase — "my ability to dogfood it" — is the junction of the two. *Alternative:* ratify it as critical in commons 3 (the report proposes this as the first ratification), or reject it if refutation condition 1 or 2 below already holds.
6. **The manifesto's mechanism applied to ourselves** `r-rel-not-using-reasons-in-chat` is `causes`, resting on the assumption from manifesto L17. *Alternative:* `contributes_to`, if the reviewer thinks Discord and Docs are not the transcript the manifesto has in mind.
7. **Why do the six new issues ignore the eleven?** not written as a relationship: no sentence asserts the cause. The undesirable effect stands alone. *Alternative:* add `causes` from `r-e-group-not-using-product`; the grounds would be this report's argument, not a source.
8. **"Not yet stated" as an undesirable effect** two sources: the observed issue bodies and the template line that prints them (operational-projection.ts L204). *Alternative:* treat it as an observation rather than an effect; the file uses `undesirable_effect` because it is what a reader of the issues sees.
9. **#4 and #13: join or replace?** no `supersedes`; both actions stand. *Alternative:* if the video replaces the demo, #4's action folds into #13's.
10. **#23 split in two** the 2R half is reported complete by the platform's export; the David-and-Rufus half remains and waits for #32. *Alternative:* keep one action and mark it done when both trees are exported.
11. **#24 split in two** the viewer/editor split and the deep-link check are different acts with different waits. *Alternative:* one action; then the check inherits the split's wait.
12. **#18 as a need with a dated expectation** the issue names no action; #36 is its bounded case; the effect is dated by the issue's own "a year". *Alternative:* an action of its own — "build the forum-to-model protocol" — which no document states.
13. **#15 as an action** deciding is something someone does, and it is the smallest real decision available for commons 3's first packet. *Alternative:* hold it as an observation until Rufus decides; then it never reaches Decide.
14. **Priority is about the constraint resource** the current-reality tree's engineering branch names David's attention as the resource everything routes through; issues that consume none of it proceed, whatever their size. *Alternative:* priority by contribution to the goal; that demotes all site work, which is what the six issues did implicitly.
15. **Two prerequisites written without a sentence** `c3-e-pre-a`/`c3-e-pre-b` and `c4-e-pre-a`/`c4-e-pre-b` are read from the work order, #37, the shape of #32–#37 and NEXT.md. *Alternative:* drop clouds 3 and 4 to a second tranche.
16. **Provenance in two repositories** relative paths resolve in this repository; app-repo locators are blob URLs pinned to `05fe3d426aaa`; issue URLs with a fragment name the part of the issue. *Alternative:* pin this repository's locators to a sha as well, at the cost of every link changing on each edit.

## The constraint, and what would refute the diagnosis

David's diagnosis is that the bottleneck is his ability to dogfood the product. The current-reality tree tests it rather than declares it. `r-e-group-not-using-product` reaches: no dogfood result, the group's reasons living in chat and assistants' prose, the six issues unrelated to the eleven, the site still saying there is no app, and (partly) the projected issues that say "not yet stated". It does not reach R3's admission, the undeployed functions or the cost of evidence; those trace to `r-e-everything-open-is-davids` and `r-e-suite-shares-prod-db`. So the diagnosis holds for the project and not for the engineering, and the two meet exactly in David's sentence: self-use starved by the one person's queue.

Three things would refute it, and the file records them here so the ratification is falsifiable:

1. Commons 3 exists with the goal accepted and the seventeen issues placed, and within thirty days David and Rufus still decide in Discord and Docs — no Decide packet signed by either. Then the constraint is usability or David's engineering capacity, not self-use.
2. The dogfood journey is blocked by a defect only R3's admission run would have caught. Then the work order's admit-first sequence was right and cloud 3 resolves the other way.
3. #35's own check — the effort of the small workflow against maintaining two places — comes out against the commons. Then `g-e-cheaper-to-know` is false for a two-person group, and changing the measure is a normative act (THROUGHPUT.md L64), not a quiet edit.

## Where each issue landed

One heading per issue, in the fixed form `### Issue #N`, so a comment on the issue can link to it. "Constraint" says whether the model gives the work priority: **yes** means it starts or extends the group's own use of the product, or frees David's time on that path; **no** means it does not need to and proceeds. Where the model says wait, it says why and what would reverse it.

### Issue #4

**Improve claim tree annotation demo to mention challenge today and solution with AI** — opened by rufuspollock, revision `2026-07-30T13:43:02Z`, [https://github.com/life-itself/reasoncommons/issues/4](https://github.com/life-itself/reasoncommons/issues/4)

| entity | role | statement |
| --- | --- | --- |
| `t-e-4-reality` | transition existing reality | The annotation demo does not explain why AI has changed the game. |
| `t-e-4-action` | transition action | Improve the annotation demo to say that this was always wanted but painful, and that AI has changed that. |

- **Serves:** g-e-judgeable-from-site (community adoption).
- **Expected effect:** not stated by the author; the issue quotes the beat it wants, not the change in the world.
- **Ordering:** none. Why AI changed the game is a first-principles argument the manifesto already makes (L115), so this does not wait on the tooling being demonstrable.
- **Constraint:** No — proceeds. It consumes none of David's time, which the current-reality tree names as the constraint resource.
- **What would change this:** If the demo is later asked to show *our* tooling doing the work rather than the argument, it inherits #13's real-tooling dependency.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #12

**Landing: wire up email-capture embed** — opened by rufuspollock, revision `2026-09-04T22:27:23Z`, [https://github.com/life-itself/reasoncommons/issues/12](https://github.com/life-itself/reasoncommons/issues/12)

| entity | role | statement |
| --- | --- | --- |
| `t-e-12-reality` | transition existing reality | The landing page ships a placeholder where a newsletter signup should be. |
| `t-e-12-action` | transition action | Pick a provider and put the newsletter signup embed in place of the landing page's placeholder. |

- **Serves:** g-e-judgeable-from-site.
- **Expected effect:** not stated; about.md L30 supplies the need ("A low-volume update list is coming").
- **Ordering:** none (a Unit A leftover in the positioning plan, L104).
- **Constraint:** No — proceeds.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #13

**Video demo of the four-step flow** — opened by rufuspollock, revision `2026-09-01T14:30:39Z`, [https://github.com/life-itself/reasoncommons/issues/13](https://github.com/life-itself/reasoncommons/issues/13)

| entity | role | statement |
| --- | --- | --- |
| `t-e-13-reality` | transition existing reality | The 'See it working' call to action points at the scripted animation. |
| `t-e-13-action` | transition action | Add a short screen recording of the four steps, of the real tooling as it comes online, to join or replace the scripted animation. |

- **Serves:** g-e-judgeable-from-site and g-e-tooling-cheap-enough.
- **Expected effect:** not stated.
- **Ordering:** none written. The issue says "ideally of the real tooling as it comes online": in that form it waits for #33 and #34, but 'ideally' is a hedge, so no `precedes` edge is asserted; recording the existing animation waits for nothing.
- **Constraint:** No in its animation form; waits in its real-tooling form.
- **What would change this:** record the animation now; redo the recording when commons 3 has its first decision on screen.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #14

**Reframe the Dashboard as a curated example** — opened by rufuspollock, revision `2026-09-01T14:30:40Z`, [https://github.com/life-itself/reasoncommons/issues/14](https://github.com/life-itself/reasoncommons/issues/14)

| entity | role | statement |
| --- | --- | --- |
| `t-e-14-reality` | transition existing reality | The constraints dashboard is linked as a bare 'Prototype' and reads as opaque. |
| `t-e-14-action` | transition action | Give the dashboard a short intro page saying what the analysis is, whose constraints it holds, and how to read the trees. |
| `t-e-14-effect` | transition expected effect | The dashboard works as a demonstration of the method rather than as an unexplained tool. |

- **Serves:** g-e-judgeable-from-site.
- **Expected effect:** stated by the author: the dashboard "works as a demonstration of the method rather than an unexplained tool" — the one site issue with a worked criterion.
- **Ordering:** none. Note that the 2R Research Circle project left the dashboard on 2026-09-06 (changelog), so the intro describes the Second Renaissance analysis.
- **Constraint:** No — proceeds.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #15

**Reconcile "Introduction" vs "Guide", and the Second Renaissance piece's placement** — opened by rufuspollock, revision `2026-09-01T14:30:42Z`, [https://github.com/life-itself/reasoncommons/issues/15](https://github.com/life-itself/reasoncommons/issues/15)

| entity | role | statement |
| --- | --- | --- |
| `t-e-15-reality` | transition existing reality | The navigation labels 'Introduction' and 'Guide' overlap in what they introduce. |
| `t-e-15-action` | transition action | Decide the clean split between Introduction and Guide and whether 'The Forum Doesn't Remember' stays inside Introduction. |

- **Serves:** g-e-judgeable-from-site.
- **Expected effect:** not stated.
- **Ordering:** none.
- **Constraint:** No. Held as an action because deciding is something someone does; it is also the smallest real decision available for commons 3's first Decide packet (#34's first case).
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #17

**Plain explainer versions: fix rough figures inherited from source drawings** — opened by rufuspollock, revision `2026-09-03T20:44:09Z`, [https://github.com/life-itself/reasoncommons/issues/17](https://github.com/life-itself/reasoncommons/issues/17)

| entity | role | statement |
| --- | --- | --- |
| `t-e-17-reality` | transition existing reality | The plain explainer versions carry rough edges inherited from the source drawings. |
| `t-e-17-action` | transition action | Edit the original SVGs to fix the three named figure defects in the plain explainer versions. |

- **Serves:** g-e-judgeable-from-site.
- **Expected effect:** not stated (a bug with three named defects).
- **Ordering:** none.
- **Constraint:** No — proceeds.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #18

**"The Forum Doesn't Remember" ends on a protocol that does not exist yet** — opened by rufuspollock, revision `2026-09-03T20:44:10Z`, [https://github.com/life-itself/reasoncommons/issues/18](https://github.com/life-itself/reasoncommons/issues/18)

| entity | role | statement |
| --- | --- | --- |
| `t-e-18-reality` | transition existing reality | The Second Renaissance explainer closes on a proposed protocol that has not been built. |
| `t-e-18-need` | transition need | The explainer's closing stops being defensible if a year passes and the protocol is still not built. |
| `t-e-18-effect` | transition expected effect | By September 2027 the forum-to-model protocol exists or the explainer's closing is revised. |

- **Serves:** g-e-2r-contributions-improve and g-e-2r-living-laboratory.
- **Expected effect:** dated and sealable: by September 2027 the protocol exists or the closing is revised (the issue's own 'a year').
- **Ordering:** held as a need, not an action. #36 is "a bounded working case of that ambition" (its own words), so #18's need enables #36's action and #36 produces #18's dated effect.
- **Constraint:** Yes, through #36.
- **What would change this:** if #36 is dropped, #18 needs an action of its own or a revised closing.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #19

**Homepage: suppress the file-tree sidebar on the landing** — opened by rufuspollock, revision `2026-09-03T20:44:18Z`, [https://github.com/life-itself/reasoncommons/issues/19](https://github.com/life-itself/reasoncommons/issues/19)

| entity | role | statement |
| --- | --- | --- |
| `t-e-19-reality` | transition existing reality | The landing page shows Flowershow's file-tree navigation listing internal folders. |
| `t-e-19-action` | transition action | Find the Flowershow option that hides the file-tree sidebar on the homepage or globally. |

- **Serves:** g-e-judgeable-from-site.
- **Expected effect:** not stated (a bug).
- **Ordering:** none.
- **Constraint:** No — proceeds.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #20

**Mobile: right-edge text clipping on narrow screens** — opened by rufuspollock, revision `2026-09-03T20:44:19Z`, [https://github.com/life-itself/reasoncommons/issues/20](https://github.com/life-itself/reasoncommons/issues/20)

| entity | role | statement |
| --- | --- | --- |
| `t-e-20-reality` | transition existing reality | Running text clips at the right edge on narrow mobile widths, which is pre-existing theme behaviour. |
| `t-e-20-action` | transition action | Check the mobile right-edge clipping on a real device. |
| `t-e-20-effect` | transition expected effect | The clipping is confirmed or ruled out on a real device. |
| `t-e-20-fix-action` | transition action | Fix the theme's content container padding and overflow-wrap so text no longer clips. |

- **Serves:** g-e-judgeable-from-site.
- **Expected effect:** the check has one: confirmed or ruled out on a real device.
- **Ordering:** the issue's own "if real": the check precedes the fix.
- **Constraint:** No — proceeds.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #23

**Get trees (2R tree and maybe D+R tree) into a machine-readable git repo** — opened by rufuspollock, revision `2026-09-04T10:39:51Z`, [https://github.com/life-itself/reasoncommons/issues/23](https://github.com/life-itself/reasoncommons/issues/23)

| entity | role | statement |
| --- | --- | --- |
| `t-e-23-reality` | transition existing reality | The trees are not yet in a machine-readable, version-controlled repository synced with GitHub issues. |
| `t-e-23-action` | transition action | Put the Second Renaissance tree into a machine-readable git repository, synced with GitHub issues. |
| `t-e-23-dr-action` | transition action | Put the David-and-Rufus tree into the same machine-readable, version-controlled form. |

- **Serves:** g-e-memory-owned-by-none.
- **Expected effect:** for the 2R tree: the platform already exports it to the connected repository on every sync (CURRENT_STATE.md L266), so this half is reported complete and its worked check is whether Rufus can read it; for the David-and-Rufus tree: not stated.
- **Ordering:** the second half waits for #32: a space has to exist before it can be exported.
- **Constraint:** the first half no (done); the second half yes.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #24

**[inbox] UX ideas about the Reason Commons app(s)** — opened by rufuspollock, revision `2026-09-04T10:41:53Z`, [https://github.com/life-itself/reasoncommons/issues/24](https://github.com/life-itself/reasoncommons/issues/24)

| entity | role | statement |
| --- | --- | --- |
| `t-e-24-reality` | transition existing reality | There is no deep link to an individual tree, so trees cannot be shared directly. |
| `t-e-24-viewer-need` | transition need | The viewer is standalone, embeddable and usable from the command line. |
| `t-e-24-action` | transition action | Split the viewer and the editor into separate components. |
| `t-e-24-links-need` | transition need | Hard links exist so that trees can be shared directly. |

- **Serves:** g-e-memory-owned-by-none and g-e-judgeable-from-site.
- **Expected effect:** not stated.
- **Ordering:** two proposals. Deep links: a check, part of #37's work ("Check actual viewer compatibility and source/deep links against #23 and #24"), against the focus addresses the app already keeps. Viewer/editor split: waits for what #37 observes.
- **Constraint:** the check no (cheap); the split waits.
- **What would change this:** if the dogfood shows sharing a tree is a top friction, the split moves up.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #32

**Establish three distinct commons and record their goals, throughput and authority** — opened by dvdgdn, revision `2026-09-06T17:20:23Z`, [https://github.com/life-itself/reasoncommons/issues/32](https://github.com/life-itself/reasoncommons/issues/32)

| entity | role | statement |
| --- | --- | --- |
| `t-e-32-reality` | transition existing reality | Three separate commons have been proposed, and today the group's work is not held apart by commons. |
| `t-e-32-need` | transition need | Subsequent development has a goal, and the three kinds of progress are kept apart. |
| `t-e-32-action` | transition action | Establish the three commons with their purpose, membership, decision authority and throughput status, and connect the app-development commons to life-itself/reasoncommons. |
| `t-e-32-effect` | transition expected effect | David and Rufus can identify which commons owns a contribution, a decision and a result without reconstructing the distinction from chat. |
| `p-e-io-commons-3` | intermediate objective | The app-development commons has a stable URL, a distinct purpose, an explicit throughput status, and recorded membership and authority. |
| `f-e-three-commons` | injection | Three distinct commons exist with recorded purpose, throughput status and authority, and the app-development commons is connected to life-itself/reasoncommons. |
| `f-e-progress-not-conflated` | desired effect | Subsequent development has a goal, and the three kinds of progress are not conflated. |

- **Serves:** g-e-first-customer-ourselves and g-e-protocol-governs-dev.
- **Expected effect:** its own: the two can say which commons owns a contribution, decision and result without reconstructing it from chat.
- **Ordering:** precedes #35, #36, #37 and #23's second half, by those issues' own sentences.
- **Constraint:** Yes — it is the first act of removing the constraint.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #33

**Establish a reproducible app baseline for the three-commons dogfood** — opened by dvdgdn, revision `2026-09-06T17:20:24Z`, [https://github.com/life-itself/reasoncommons/issues/33](https://github.com/life-itself/reasoncommons/issues/33)

| entity | role | statement |
| --- | --- | --- |
| `t-e-33-reality` | transition existing reality | Deployed behaviour differs from the checkout and browser tests interfere with the live application. |
| `t-e-33-need` | transition need | Dogfood results are interpretable rather than confounded by deployment differences or test interference. |
| `t-e-33-action` | transition action | Establish a reproducible app baseline: an isolated test database, recorded versions, reachable attribution and one verified run summary. |
| `t-e-33-effect` | transition expected effect | David and Rufus can attribute dogfood friction to the product rather than to an unknown deployment or test outage. |
| `t-e-0443-effect` | transition expected effect | Current-change attribution is reachable. |
| `t-e-deploy-action` | transition action | Deploy the agent-turn and realize-narrative functions and record their versions. |
| `t-e-deploy-effect` | transition expected effect | Both functions are deployed and their versions are recorded with the tested commit. |
| `p-e-io-deployments` | intermediate objective | Both functions are deployed and their versions are recorded with the tested commit. |
| `p-e-io-test-database` | intermediate objective | Browser acceptance tests run against an isolated, reproducible database. |
| `p-e-obst-versions-recorded` | obstacle | Deployed behaviour can differ from the checkout, so a dogfood result is hard to interpret. |
| `p-e-io-versions-recorded` | intermediate objective | The tested application commit, migrations and deployed function versions are recorded. |
| `c3-e-req-b` | cloud requirement | The dogfood begins without every future redesign phase being complete. |
| `c3-e-injection` | injection | A dogfood needs a reproducible deployed build with attribution reachable, not another phase tag in the profile. |

- **Serves:** g-e-work-is-not-change and g-e-improves-own-change.
- **Expected effect:** its own: dogfood friction is attributable to the product rather than to deployment or test outage.
- **Ordering:** requires the 04:43 decision and the two deployments (its acceptance criteria and work); precedes #35 and #37.
- **Constraint:** Yes — it is David's time on the dogfood path.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #34

**Make starting a commons lead from existing material to a useful first decision** — opened by dvdgdn, revision `2026-09-06T17:20:25Z`, [https://github.com/life-itself/reasoncommons/issues/34](https://github.com/life-itself/reasoncommons/issues/34)

| entity | role | statement |
| --- | --- | --- |
| `t-e-34-reality` | transition existing reality | A new commons gives too little guidance about what to bring and what useful result to expect. |
| `t-e-34-need` | transition need | A participant can start from real material and reach a useful first judgment without the method's vocabulary. |
| `t-e-34-action` | transition action | Make starting a commons lead from existing material to a useful first decision. |
| `t-e-34-effect` | transition expected effect | A participant reaches a useful first judgment with less facilitator explanation and correction work. |
| `p-e-io-import-coverage` | intermediate objective | Import identity-conflict choices and browser upload coverage are finished before repeated import is relied on. |
| `f-e-start-from-material` | injection | Starting a commons leads from existing material to a useful first decision without Logical Thinking Process vocabulary. |

- **Serves:** g-e-rigour-without-vocabulary and g-e-no-clerical-burden.
- **Expected effect:** its own: a useful first judgment with less facilitation.
- **Ordering:** precedes #37 (the goal is #34's first case and #37's precondition).
- **Constraint:** Yes for the first case. The five-card onboarding discussed on 2026-09-06 is not in any document and is not in the file.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #35

**Bring selected existing GitHub issues into the Reason Commons commons without duplicates** — opened by dvdgdn, revision `2026-09-06T17:20:26Z`, [https://github.com/life-itself/reasoncommons/issues/35](https://github.com/life-itself/reasoncommons/issues/35)

| entity | role | statement |
| --- | --- | --- |
| `t-e-35-reality` | transition existing reality | The sync projects accepted actions and reconciles existing mappings, and creating an issue does not import it into the app. |
| `t-e-35-need` | transition need | The repository stays the familiar collaboration surface while its work is connected to the commons' goal and reasoning. |
| `t-e-35-action` | transition action | Bring a small set of selected existing issues into the commons as reviewable proposals, adopting the original issue on acceptance. |
| `t-e-35-effect` | transition expected effect | David and Rufus can explain why selected work matters and what it should change while continuing to work from GitHub. |
| `p-e-io-adoption-honesty` | intermediate objective | Adopted issues enter as proposals with their source identity, revision and excerpts preserved and human-written content untouched. |
| `f-e-adopt-issues-as-proposals` | injection | Selected existing GitHub issues enter the commons as bounded proposals, and on acceptance the original issue is adopted rather than duplicated. |
| `f-e-cheaper-than-two-places` | desired effect | Maintaining the commons costs David and Rufus less effort than maintaining both places by hand. |

- **Serves:** g-e-cheaper-to-know and g-e-ai-no-silent-authority.
- **Expected effect:** its own: the two can explain why selected work matters while working from GitHub; its check compares effort against maintaining two places.
- **Ordering:** requires #32 and #33 (its own text); precedes #37.
- **Constraint:** Yes — and it is the mechanism by which this model's placements become ratifiable in the app.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #36

**Define and exercise the Research Group handoff into the Second Renaissance model** — opened by dvdgdn, revision `2026-09-06T17:20:27Z`, [https://github.com/life-itself/reasoncommons/issues/36](https://github.com/life-itself/reasoncommons/issues/36)

| entity | role | statement |
| --- | --- | --- |
| `t-e-36-reality` | transition existing reality | Research activity and a proposed change are not yet an accepted update in the receiving model. |
| `t-e-36-need` | transition need | The Research Group's throughput is a controlled, deliberated update accepted into the Second Renaissance model. |
| `t-e-36-action` | transition action | Define and exercise the handoff from the Research Group into the Second Renaissance model on one real case. |
| `t-e-36-effect` | transition expected effect | The group can show what intellectual progress reached the movement's model, why it was accepted and what remains uncertain. |

- **Serves:** g-e-2r-contributions-improve and g-e-2r-living-laboratory.
- **Expected effect:** its own: the group can show what intellectual progress reached the movement's model.
- **Ordering:** requires #32 (authority in the receiving commons); precedes #37; carries #18.
- **Constraint:** Yes for the living-laboratory condition, conditional on question R1 (motivation.md L28).
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### Issue #37

**Run a measured dogfood cycle and use its findings to select the next app work** — opened by dvdgdn, revision `2026-09-06T17:20:28Z`, [https://github.com/life-itself/reasoncommons/issues/37](https://github.com/life-itself/reasoncommons/issues/37)

| entity | role | statement |
| --- | --- | --- |
| `t-e-24-links-action` | transition action | Check the existing focus addresses and public reading against the need for shareable tree links. |
| `t-e-37-reality` | transition existing reality | A completed feature or a larger reasoning graph is not evidence that the software is helping. |
| `t-e-37-need` | transition need | The next app priorities follow observed constraints on the three commons' work. |
| `t-e-37-action` | transition action | Run a measured dogfood cycle and select the next app work from its findings. |
| `t-e-37-effect` | transition expected effect | David and Rufus can explain why the next development task is more valuable than alternatives using recorded experience. |
| `p-e-next-work-chosen-from-dogfood` | implementation objective | The next proposed app work has an explicit connection to the agreed goal, an expected effect, and a date or condition for checking it, selected from a recorded dogfood review. |
| `c3-e-pre-b` | cloud prerequisite | The dogfood runs on the deployed build now. |

- **Serves:** g-e-improves-own-change and g-e-cheaper-to-know.
- **Expected effect:** its own: the two can explain why the next task is more valuable than alternatives using recorded experience.
- **Ordering:** requires #32–#36 (its own work list); produces the prerequisite tree's implementation objective.
- **Constraint:** Yes — it is the constraint review itself.
- **What the model does not claim:** that the issue's completion criteria are an effect in the world. Closing the issue records that the work was reported done (OPERATIONAL_PROJECTION_SPEC.md §7.4); whether it had its effect is answered by observation in the commons.

### How the two sets relate without one demoting the other

Rufus's site issues serve the *community adoption* factor through `g-e-judgeable-from-site`; the six proposed on 2026-09-06 serve *Customer Zero*. business_plan.md L79 says the second is necessary for the *claim* the first makes — and that ordering is the documents', binding only claim-bearing content (#4's tooling reading, #13's real-tooling recording), not the site work as such. Priority in this model is about the constraint resource, David's attention, not about worth: eight of the eleven consume none of it and are marked *proceeds*. Only #13 in one form, #23's second half, #24's split and #36 depend on David's path, each with grounds and a stated reversal. The chain #32 → #33 → {#34, #35, #36} → #37 is carried only as far as the issues' own sentences carry it. And the six are proposals: their author is recorded, nothing is pre-ratified, and #35 is how they and the eleven enter commons 3 on equal footing, each acceptable, reservable or rejectable.

## Throughput candidates for commons 3

None of these is a proposition in the file; the definition is the app's own record, proposed against the accepted goal and ratified there. THROUGHPUT.md L14–L16 warns that calling the apparatus's rates throughput invites optimising the apparatus; for a group whose goal is its own thinking-to-action the object and the apparatus partly coincide, which is the question to put to both authors (R8, D4).

| candidate | goal unit | time basis | system boundary | counting rule | baseline | source | supported by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **A (recommended)** | one consequential development decision made in commons 3 through a Decide packet, with reliance recorded, whose action has an execution record | per week | from a contribution in commons 3 to the execution record of the decided action | once, when the execution record exists | 0 on 2026-09-06 | decision records joined to execution records | the goal's own words, "thinking into action"; REDESIGN_PLAN.md L117; #32: "Neither issue closure nor code volume is presumed to be throughput" |
| B | active `use` reliance records per active space, entered by the decision-maker | per 30 days | commons 3 | at the reliance event | 0 | reliance events | E9A_DOGFOOD.md |
| C | real check-ins on transition steps per active space | per week | commons 3 | one observation per attempted action | 0 | observation records | E1_DOGFOOD.md L13–L22 |
| D (later) | "Externally initiated consequential workflows in which later action or decision quality measurably improves, net of fully loaded capture and review cost" | — | external teams | — | — | — | strategy file L47; the unit for the community-adoption factor, not for now |

## Validator output

```
Reading /Users/davidjoseph/github/reasoncommons/ltp/reason-commons/reason-commons.ltp.yaml

✓ schema 1.0 — “Groups think together and act on it, proven on ourselves first” (reason-commons)
✓ every role is coherent in the view it was placed in
✓ 476 units would be offered for ratification, in 20 waves
✓ nothing excluded
✓ nothing needing a decision

  goal 45   current_reality 46   conflict 78   future_reality 56   prerequisite 52   transition 199
  301 of 476 would be safe to ratify unread
```

## Not in this file

- **No assessments.** No source draws a `critical_root_cause`, `breaks_conflict` or `negative_branch_mitigated` conclusion; the first is proposed above as commons 3's first ratification.
- **No throughput definition.** Not a slot in the format; see the candidates.
- **Cloud 5, AI does the labour vs AI holds no authority**, waits for a second tranche; it is expressed meanwhile through the handling of #32–#37 as proposals.
- **The strategy file's four clouds**, the pre-redesign undesirable effects and the rest of the constitution: a second tranche, listed under *Deliberately omitted*.
- **No edges from the pivot's cloud into the transition tree** saying "admit R3 after #33" or "Model row after #37": the model's recommendations, not sourced sentences. They are in the placement section with their grounds and reversals, and the only sourced ordering among the app's own actions is written (04:43 before admitting R3; R3 before the Model row; deployments before the E1 clock).

These are gaps the sources leave or tranches deferred, not failures of the conversion.

## Platform observations, 2026-09-06

Facts the file cites that no document states, observed through the hosted project's public read path and GitHub on 2026-09-06:

- The space **Reason Commons Focus** (`365f2925-1a97-4367-8df2-e76a7757540e`, created 2026-08-13) is connected to `Promise-Foundation/2R-Research` with a healthy sync last run 2026-09-04. It holds 67 accepted nodes (32 goal, 18 current reality, 17 transition), 68 edges, 4 proposals, 426 events and **0 contributions**, 0 reliance records, 0 decision records, 0 throughput definitions.
- Its projected issues in that repository (#6–#12, labelled `rc:ready`) read "Why this matters: Not yet stated." and "What needs to change: Not yet stated." — the managed section's fallback when an action has no linked reality or need.
- `Promise-Foundation/reason-commons` has no reasoning space of its own and no GitHub issues; its work order and open decisions live in `docs/CURRENT_STATE.md`.
- Issues #32–#37 in this repository were created between 17:20:23Z and 17:20:28Z on 2026-09-06 under one account, from an assistant's session; they cross-reference only #23, #18 and #24.
- The two collaborators' conversation about the project happens in Discord and Google Docs; this repository's `about.md` says "There is no app to log into yet."

## Questions

**To Rufus**

R1. Is motivation.md L28 — "Stream 3 — Second Renaissance LTP — deferred; too complex until a toy example works end-to-end" — superseded by the 2026-09-04 talk and its live contributions? #32 and #36 assume it is.
R2. about.md L8 as the goal, with jobs_to_be_done.md L3 as its tooling condition — agreed, or is the product job the goal?
R3. #23's 2R half: can you read `.reason-commons/365f2925-1a97-4367-8df2-e76a7757540e.ltp.json` in `2R-Research`, and does the platform's issue projection there close the "synced with GitHub issues" part?
R4. Does #13's recording replace #4, or does #4 stand as the animation's own argument?
R5. Is #36 an acceptable bounded case of #18, and is September 2027 the check date the issue's "a year" implies?
R6. Should the site's status line ("There's no app to log into yet") change when commons 3 exists? The model lists it as an untraced task.
R7. #24: is the viewer/editor split a proposal for the app, or for this site's dashboard?
R8. Which throughput candidate reads to you as "our thinking increasingly results in action" — A, B or C?

**To David**

D1. Which surface names the proposer and the ratifier of a change that has just landed (04:43)? The model makes this the first prerequisite of #33.
D2. Dates for deploying `agent-turn` and `realize-narrative`, and for entering the E1 prediction prospectively.
D3. Do you ratify "the group developing Reason Commons does not hold its own reasoning in Reason Commons" as the critical root cause, knowing the three engineering effects trace elsewhere?
D4. Which throughput candidate, and does the object/apparatus coincidence for commons 3 concern you?
D5. Is the Lovable private registry a real install blocker for anyone but you, and where should it be recorded?
D6. Does the Model row wait behind #37, or does R3's admission pull it forward regardless?
D7. Is "Reason Commons Focus" commons 1 or commons 2? Its content is the research group's adoption plan under a commons-1-sounding name.

## Source revisions

| source | revision |
| --- | --- |
| life-itself/reasoncommons | `origin/main` 37aefee1d004 |
| Promise-Foundation/reason-commons | `05fe3d426aaa` (branch `claude/repo-work-prioritization-eb792b`) |
| issue #4 | `2026-07-30T13:43:02Z` |
| issue #12 | `2026-09-04T22:27:23Z` |
| issue #13 | `2026-09-01T14:30:39Z` |
| issue #14 | `2026-09-01T14:30:40Z` |
| issue #15 | `2026-09-01T14:30:42Z` |
| issue #17 | `2026-09-03T20:44:09Z` |
| issue #18 | `2026-09-03T20:44:10Z` |
| issue #19 | `2026-09-03T20:44:18Z` |
| issue #20 | `2026-09-03T20:44:19Z` |
| issue #23 | `2026-09-04T10:39:51Z` |
| issue #24 | `2026-09-04T10:41:53Z` |
| issue #32 | `2026-09-06T17:20:23Z` |
| issue #33 | `2026-09-06T17:20:24Z` |
| issue #34 | `2026-09-06T17:20:25Z` |
| issue #35 | `2026-09-06T17:20:26Z` |
| issue #36 | `2026-09-06T17:20:27Z` |
| issue #37 | `2026-09-06T17:20:28Z` |

