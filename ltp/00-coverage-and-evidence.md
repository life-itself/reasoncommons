# Coverage and evidence

## Scope

Primary analysis scope: the five supplied files under `docs/ltp_trees/`, treated as one provisional Second Renaissance causal model.

Supporting implementation scope: the Project LTP skill contract, model schema, local-dashboard source, server, tests, fixture, `README.md`, and `MOTIVATION.md`. These files determine how the supplied trees are normalized and rendered; they are not evidence that the Second Renaissance group behaves as described.

Analysis mode: reconciliation. The documents already contain a Goal Tree, Current Reality Tree, conflict diagrams, Future Reality Tree, and Prerequisite Tree. This run reconciles them into one stable-ID model and infers the missing Transition Tree.

## Inventory and coverage

| Area | Discovered | Examined | Treatment |
|---|---:|---:|---|
| `docs/ltp_trees/*.md` | 5 files / 2,561 lines | 5 | Read in full and normalized |
| Project LTP instructions/references/schema | 7 | 7 | Read in full |
| Dashboard behavior and server/test contract | 10 key files | 10 | Read directly |
| Project intent and plan | 4 key files | 4 | Read directly |
| Primary repository inventory | 106 files before these deliverables | Classified | Not claimed as full-project behavioral analysis |

The repository inventory excluded `.git`, the secondary `.claude` worktree, and installed `node_modules`. Generated dashboard bundles, package locks, browser-demo exports, `.DS_Store`, thumbnails, screenshots, build metadata, bytecode, and backup `*.md~` files were classified rather than read as primary evidence. Large theory documents outside `docs/ltp_trees` were not treated as source evidence for this model. The cited but absent Second Renaissance whitepapers and “How” paper were not examined.

## Evidence map

| ID | Source lines | Observation | Evidential use |
|---|---|---|---|
| EVD-1 | Goal Tree 1–24 | Explicit goal and eight CSFs | Provisional destination |
| EVD-2 | CRT 5–13 | System boundary and candidate throughput | Boundary and goal unit |
| EVD-3 | CRT 17–51 | Fifteen named UDEs | Candidate present effects |
| EVD-4 | CRT 55–81 | Six candidate root causes | Candidate causal structure |
| EVD-5 | CRT 291–317 | Conversion architecture named likely constraint | Constraint hypothesis |
| EVD-6 | CRT 321–346 | Lived validation explicitly required | Earliest validation gap |
| EVD-7 | Conflict 496–524 | Movement/depth cloud and core injection | Central conflict |
| EVD-8 | FRT 17–39 | Tree stewardship protocol | Governance injection |
| EVD-9 | FRT 41–68 | Throughput, conversion, layered participation | Principal injections |
| EVD-10 | FRT 72–113 | Learning, stewardship, pockets, replication, review | Operating-system injections |
| EVD-11 | FRT 522–629 | Five negative branches and trims | Risk controls |
| EVD-12 | PRT 80–112 | Consent-based entry prerequisites | Entry objective |
| EVD-13 | PRT 126–160 | Recurring practice and safety | Practice objective |
| EVD-14 | PRT 173–215 | Contribution and stewardship safeguards | Leadership objective |
| EVD-15 | PRT 219–275 | Dense containers, sangha, outward service | Pocket objective |
| EVD-16 | PRT 278–322 | Maturity-rated replication | Replication objective |
| EVD-17 | PRT 329–372 | Movement tied to pocket learning | Scaling sequence |
| EVD-18 | PRT 452–482 | Governance-first dependency chain; TT missing | Transition ordering |
| EVD-19 | PLAN 29–58 | Dashboard only verified on toy fixture | Rendering context |

## Evidence limits

The primary documents are authored analysis, not operational observations. The CRT calls itself provisional and asks the group to validate its UDEs and arrows. Accordingly:

- Explicit document content is observed as artifact evidence.
- Claims about actual group behavior remain provisional.
- Proposed causal links and future effects remain inferred or provisional.
- No entity is marked confirmed because no group decision or user confirmation of the substantive model was supplied.
- No `throughput.yaml` was created because no real period observations exist.

