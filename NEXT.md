---
title: What's next
updated: 2026-09-06
generated_from: ltp/reason-commons/reason-commons.ltp.yaml @ 5bb59fa89bab
---

# Next

Open work, read off the transition tree of [the Reason Commons model](ltp/reason-commons/reason-commons.ltp.yaml) ([report](ltp/reason-commons/reason-commons.report.md)). Detail lives in the linked issues; history lives in [`changelog.md`](changelog.md). Regenerated with `bun scripts/next-from-ltp.ts` from a Reason Commons app checkout, so edit the model rather than this file: an action's place here is a consequence of what the model says it waits for, and the report says why.

## Now

Actions no other action precedes.

- **[#4](https://github.com/life-itself/reasoncommons/issues/4) — Improve the annotation demo to say that this was always wanted but painful, and that AI has changed that.** — expected effect not yet stated
- **[#12](https://github.com/life-itself/reasoncommons/issues/12) — Pick a provider and put the newsletter signup embed in place of the landing page's placeholder.** — expected effect not yet stated
- **[#13](https://github.com/life-itself/reasoncommons/issues/13) — Add a short screen recording of the four steps, of the real tooling as it comes online, to join or replace the scripted animation.** — expected effect not yet stated
- **[#14](https://github.com/life-itself/reasoncommons/issues/14) — Give the dashboard a short intro page saying what the analysis is, whose constraints it holds, and how to read the trees.** — expected: The dashboard works as a demonstration of the method rather than as an unexplained tool
- **[#15](https://github.com/life-itself/reasoncommons/issues/15) — Decide the clean split between Introduction and Guide and whether 'The Forum Doesn't Remember' stays inside Introduction.** — expected effect not yet stated
- **[#17](https://github.com/life-itself/reasoncommons/issues/17) — Edit the original SVGs to fix the three named figure defects in the plain explainer versions.** — expected effect not yet stated
- **[#19](https://github.com/life-itself/reasoncommons/issues/19) — Find the Flowershow option that hides the file-tree sidebar on the homepage or globally.** — expected effect not yet stated
- **[#20](https://github.com/life-itself/reasoncommons/issues/20) — Check the mobile right-edge clipping on a real device.** — expected: The clipping is confirmed or ruled out on a real device
- **[#23](https://github.com/life-itself/reasoncommons/issues/23) — Put the Second Renaissance tree into a machine-readable git repository, synced with GitHub issues.** — expected: The connected repository holds the tree as the platform's export, with its version history, refreshed on every sync
- **[#24](https://github.com/life-itself/reasoncommons/issues/24) — Split the viewer and the editor into separate components.** — expected effect not yet stated
- **[#32](https://github.com/life-itself/reasoncommons/issues/32) — Establish the three commons with their purpose, membership, decision authority and throughput status, and connect the app-development commons to life-itself/reasoncommons.** — expected: David and Rufus can identify which commons owns a contribution, a decision and a result without reconstructing the distinction from chat
- **[#34](https://github.com/life-itself/reasoncommons/issues/34) — Make starting a commons lead from existing material to a useful first decision.** — expected: A participant reaches a useful first judgment with less facilitator explanation and correction work
- **[part of #37](https://github.com/life-itself/reasoncommons/issues/37) — Check the existing focus addresses and public reading against the need for shareable tree links.** — expected effect not yet stated

## Then

In the order the model's `precedes` links give; "after" names what each waits for.

- [#20](https://github.com/life-itself/reasoncommons/issues/20) — Fix the theme's content container padding and overflow-wrap so text no longer clips. (after #20) — expected effect not yet stated
- [#23](https://github.com/life-itself/reasoncommons/issues/23) — Put the David-and-Rufus tree into the same machine-readable, version-controlled form. (after #32) — expected effect not yet stated
- [#36](https://github.com/life-itself/reasoncommons/issues/36) — Define and exercise the handoff from the Research Group into the Second Renaissance model on one real case. (after #32) — expected: The group can show what intellectual progress reached the movement's model, why it was accepted and what remains uncertain
- [#33](https://github.com/life-itself/reasoncommons/issues/33) — Establish a reproducible app baseline: an isolated test database, recorded versions, reachable attribution and one verified run summary. (after “Decide which surface names the proposer and the ratifier of a change that has just landed.”, “Deploy the agent-turn and realize-narrative functions and record their versions.”) — expected: David and Rufus can attribute dogfood friction to the product rather than to an unknown deployment or test outage
- [#35](https://github.com/life-itself/reasoncommons/issues/35) — Bring a small set of selected existing issues into the commons as reviewable proposals, adopting the original issue on acceptance. (after #32, #33) — expected: David and Rufus can explain why selected work matters and what it should change while continuing to work from GitHub
- [#37](https://github.com/life-itself/reasoncommons/issues/37) — Run a measured dogfood cycle and select the next app work from its findings. (after #32, #33, #34, #35, #36) — expected: David and Rufus can explain why the next development task is more valuable than alternatives using recorded experience

## Placed, not as an action

Issues the model holds as something other than an action to take.

- [#18](https://github.com/life-itself/reasoncommons/issues/18) — `t-e-18-need` (transition need): The explainer's closing stops being defensible if a year passes and the protocol is still not built.

## Not from an issue

Actions the model carries from the app repository's own work order and open decisions.

- Decide which surface names the proposer and the ratifier of a change that has just landed. — expected: Current-change attribution is reachable — https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L632
- Admit R3 by adding @phase-r3 and @phase-e9a to the profile in the same change as the code, with the green profile figure recorded. (after “Decide which surface names the proposer and the ratifier of a change that has just landed.”) — expected: AI cannot cross the authority boundary, and every consequential reliance links to a decision and a packet manifest — https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L743
- Deploy the agent-turn and realize-narrative functions and record their versions. — expected: Both functions are deployed and their versions are recorded with the tested commit — https://github.com/life-itself/reasoncommons/issues/33#work
- Use the closed evidence loop on active Reason Commons work, registering the prediction prospectively in a deployed build. (after “Deploy the agent-turn and realize-narrative functions and record their versions.”) — expected: Teams record check-ins on their transition steps — https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/E1_DOGFOOD.md#L15
- Carry out the Model row as specified in MODEL_ROW_RETARGET.md. (after “Admit R3 by adding @phase-r3 and @phase-e9a to the profile in the same change as the code, with the green profile figure recorded.”) — expected effect not yet stated — https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L745
- Continue R4 to R5 in the redesign plan's dependency ladder. — expected effect not yet stated — https://github.com/Promise-Foundation/reason-commons/blob/05fe3d426aaa/docs/CURRENT_STATE.md#L746
