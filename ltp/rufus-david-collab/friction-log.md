# Friction log

Each place the tool, the format or the method falls short while Rufus and David use it on real work. Each entry is a candidate build item; it does not have to be fixed now. Started by Rufus on 2026-09-26 (action 3 in [scqh.md](scqh.md)). Newest first.

| date | friction | hit while | candidate fix |
| --- | --- | --- | --- |
| 2026-09-26 | No clear rule for when a new question is its own project and when it belongs inside an existing one. Rufus could not tell whether the funding decision should start a fresh analysis or grow out of this tree. | Planning the funding decision | Guidance in the method or the app: a dilemma under an existing obstacle is a new cloud in the same project; a new goal is a new project. |
| 2026-09-26 | Transition actions have no owner field, so owners are written into the statement ("David uses…"). Owners cannot be filtered, reassigned or shown on their own. | Recording the transition view | An `owner` (and perhaps `status`) field on transition actions. |
| 2026-09-26 | Links across views are refused: an action cannot point at the obstacle it removes, and evidence cannot point at the assumption it counts against. Those links live only in the report prose. | Recording the conflict resolution and the transition view | Allow a small set of cross-view kinds (for example `overcomes`, `challenges`) in the file format. |
| 2026-09-26 | The file cannot be validated from this repo: `check:import` needs a checkout of the app. Validation so far is a hand-rolled local script. | Every pass on this tree | Ship the validator as a standalone command, or run it in CI here. |
| 2026-09-26 | The `ltp-project` skill is not found by Claude Code in this repo unless the `.claude/skills` symlinks are wired by hand. | Starting the session | Track the symlinks, or document a one-line setup that is checked at session start. |
