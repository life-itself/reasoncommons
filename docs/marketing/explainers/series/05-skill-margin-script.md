# The skill in the margin — revised narrative

Proposal `explainer-margin-pacing-2026-10-20` revision 1, accepted by David Joseph with “yes” on 20 October 2026. The original story prose stays intact. This revised narrative supersedes the archived script below. Editorial review and visual mapping are in `06-skill-margin-pacing-critique.md` and `07-skill-margin-scroll-map.md`.

## The Wrong Queue — revised

Meet the people before asking them to solve anything. Maria handles check-in and follow-up booking. Tomasz works in triage. Dr Adeyemi sees patients. Leila runs the pharmacy. Sam manages the practice. At first the reader learns only what the story has established: who does which work, then what each station can handle. Nobody is chatting to the skill yet.

The clinic sees twenty people a day. The other forty go home. Sam brings in Reason Commons to help the team examine its explanation before choosing what to change.

Sam: “Everyone is busy, but forty people leave unseen. Help us work out what to change.” Reason Commons: “Separate what you observe from what you suspect. The shortfall is visible; ‘the front desk is the problem’ is a claim to check.”

Sam asks about the one hire. At check-in, the skill explains why output stays at twenty. Sam asks about the other stations. Only once the story has compared them does the skill identify the doctor’s room as the limiting station. It saves the receptionist-hire consequence as a suggestion, still proposed. Sam accepts the doctor constraint for now; that records only Sam’s position.

Dr Adeyemi describes six clinical hours, then two hours lost to repeated histories, missing notes and printing. The skill records the lost time as proposed. Only when the text reaches twenty-six does the skill suggest testing what happens if that time is returned.

Sam tells Maria that reception’s aim is to keep the doctor supplied, rather than clear check-in as fast as possible. Maria captures the concern the new policy creates: “Patients will think we are slower. The complaints will still come to the desk.” The skill keeps that side effect on record and asks who will explain the wait.

Sam asks if improving the doctor finishes the job. The skill explains the next constraint only as the story moves it to follow-up booking. Sam asks about pharmacy and the hospital; the skill records a backlog question to re-check the limiting station after each improvement. When the countersignature rule appears, Leila captures it. The skill asks what the rule was meant to protect before anyone replaces it.

## The Arrows Nobody Checks — revised

At first, each explanation still belongs to its owner. Do not show it as captured before the story says it leaves that person’s head. After the writing-down passage, Sam brings in Reason Commons to retain attributed explanations. Sam invites the team to write. Dr Adeyemi captures a short chain. The skill records it as proposed, not established.

As the seven questions arrive, the team learns how to examine the chain. The skill asks what Sam means by “funding.” Sam says the budget fell twelve percent since 2019 and suggests that this causes the wait. The skill asks what else must hold. Sam acknowledges that money may not be the missing capacity. The skill distinguishes a symptom from evidence of its cause, then asks what difference the budget hypothesis predicts in the waiting records. Sam keeps that comparison on the backlog instead of declaring the cause settled.

Once the text shows how a page can take criticism, Sam asks Maria to choose an arrow. Maria captures a challenge to the interruptions-to-overruns link. The skill marks that exact link disputed. Dr Adeyemi offers an observation about days without interruptions; the skill retains it as proposed evidence, without treating it as conclusive. Tomasz captures the 2018 waiting figures and the skill attaches that objection to the funding link. The ending shows a shared record with an open question, rather than manufacturing unanimous agreement.

## Five Shapes — revised

Sam brings the skill back to the task of deciding what to change. The skill asks what success would look like. Tomasz states the catchment goal; the skill records it as proposed. Sam accepts that displayed goal for now. The skill records Sam’s acceptance without speaking for everyone else.

Sam names the four symptoms. The skill suggests working backwards for shared causes, while reminding the team that the existing map is a hypothesis. Sam then asks Dr Adeyemi about access versus longer appointments. Dr Adeyemi explains the quality need. The skill asks which assumption makes longer slots necessary; Dr Adeyemi challenges it with the repeated-history problem. Only then does the skill record the disputed assumption.

Sam tries ready notes on paper. The skill walks the conditional effects forward as the text does: fewer repeated histories, consultations that fit, then notes ready the next day. At the side-effect question Sam asks Maria who would prepare them. Maria captures the forty minutes she cannot spare. The skill records that cost on the plan.

Sam names the three obstacles one at a time: before eight, the busiest person, one hire. The skill suggests an objective of preparing notes without overloading reception. After the story introduces the forced order, the skill asks who will draft the standard before training the hire. Sam names Tomasz and Dr Adeyemi, by Friday.

Maria later proposes that ready notes would fix the referral backlog. Sam disagrees. The skill saves their disputed link and suggests comparing ready-note days for two weeks. The story ends with something the team can investigate, not a claim that the intervention has worked.

## Archived first script — superseded

Change proposal `explainer-skill-margin-2026-10-20` revision 2. Implementation bead `reasoncommons-brw`. Built pages: [part one](../../../../website/explainers/01-bottleneck-in-practice/index.html), [part two](../../../../website/explainers/02-thinking-made-visible-in-practice/index.html), [part three](../../../../website/explainers/03-five-shapes-in-practice/index.html); shared [skill-margin.css](../../../../website/explainers/skill-margin.css) and [skill-margin.js](../../../../website/explainers/skill-margin.js).

The three trilogy pieces ([The Wrong Queue](../../../../website/explainers/01-bottleneck/index.html), [The Arrows Nobody Checks](../../../../website/explainers/02-thinking-made-visible/index.html), [Five Shapes](../../../../website/explainers/03-five-shapes/index.html)) explain the method. Nothing in them says that a reader could do this tomorrow, with the reason-commons skill. The "in practice" editions keep every word of the story and add a margin: the people of the Ashfield clinic, using the skill at the moment of the story where it makes the difference the story describes.

The story text is unchanged and already approved, so this file is the script for the margin only. Per `skills/scrollable-explainer/SKILL.md` §1.5 it was critiqued independently as writing before it was built; the critique and what changed are at the end. The scenes below are generated from the same data the pages use, so they match what a reader sees.

## Rules for the margin

- **The margin shows behaviour the skill actually has.** It records contributions as proposed and attributed, accepts only when a named person says so ("accepted for now"), keeps objections on the item as disputed, labels its replies (Capture result, Next step, Answer, Tree view), and recommends one next step with its reason. It never decides who is right. Its own suggestions are labelled "Suggested by the skill".
- **People send the notifications.** The skill never messages anyone on its own. Every lock-screen notification is a colleague's message in the channel.
- **The team chat is invoked, not overheard.** As in the prototype Discord bot in `apps/discord`, `/reason` answers by default (ask), records in capture mode, and `/reason-accept` endorses a displayed review. Every contribution the skill saves there carries `/reason · capture`. Plain replies are not captured. Dr Adeyemi dictates with the phone's keyboard; the prototype has no voice input of its own.
- **In a meeting, the person at the keyboard can record who accepts**, by name, as a facilitated session does with speaker labels. Anyone not named has not accepted.
- **One person, one device, one moment per scene.** Each scene names who, where, when and the device.
- **Every scene ends on what changes.** One plain sentence about the difference the record makes at that moment.
- **No product branding is drawn.** The desktop is "an AI assistant with the reason-commons skill"; the skill runs today in Claude Code, Codex and other agents that support skills. The closing card's install line installs the skill, not the prototype chat.
- **No pronouns for the cast in the margin.** The story's own text is unchanged.
- **The accent stays with the constraint.** Terracotta marks the thing at issue; the skill's own colour is the olive second accent.

## Cast

| Person | Role | Device | Why that device |
|---|---|---|---|
| Sam Whitfield | Practice manager | Desktop, back office | Plans, budgets and runs the sessions from a desk. |
| Maria Costa | Front desk | Phone, team-chat notifications | On the move all day; the notification is what tells Maria to shift focus. |
| Dr Funmi Adeyemi | GP | Phone, dictating | A minute between patients; dictating is faster than typing. |
| Tomasz Nowak | Triage nurse | Phone, team-chat notifications | Moves between rooms and acts on a notification. |
| Leila Haddad | Pharmacist | Phone, team chat | At the dispensary bench, not a desk. |
| The skill | reason-commons | In the assistant or the team chat | Drawn as a small tree, in olive. |

Avatars are hand-drawn in the series' line style with one marker of role each: Sam's glasses and lanyard, Maria's headset, Dr Adeyemi's stethoscope, Tomasz's fob watch, Leila's pill bottle (worn with a headscarf).

## Layout

On screens 1100px and wider a fixed margin on the right holds one device at a time and plays the scene whose anchor the reader has most recently passed: a notification drops onto a lock screen and opens into the thread, or messages arrive one by one in a desktop window, the skill's after a moment of typing. Above the device: who, role, device, place and time; below it, *What changes*. Dots at the foot jump between scenes, and the margin can be hidden. Narrower screens show the same scenes as cards between the story's sections, which play when they scroll into view. A cast card comes first and a closing card with the install line last. With reduced motion every scene appears finished. Each scene plays once; going back shows it finished.

## Part one · The Wrong Queue

**Cover card.** In the margin: the same clinic, using the skill. As you read, the people of the Ashfield clinic use the reason-commons skill at the point in the story where it makes a difference. Each scene plays when you reach it, on the device that person would actually use.

**Scene 1.** *After “It has treated twenty patients a day for four years.”* Sam · desktop · Back office · Monday 07:50.
- Sam: By noon there are sixty people waiting, and everyone says it’s the front desk. Help me check that before I do anything about it.
- Skill · Capture result: Saved, from Sam: [Proposed] Undesirable effect · *About sixty people are waiting by noon.* [Proposed] Cause · *Check-in is too slow (what the staff say).*
- Skill · Next step: Ask each station how many people it can handle in a day. Why: a queue shows where people wait, not what limits how many are seen.
- What changes: “It’s the front desk” is on record as a claim to test, not a decision.

**Scene 2.** *After the five-stations drawing, before “The other forty go home.”* Tomasz’s phone · lock screen · Triage room · Monday 13:05.
- Notification · Sam: How many people can your station handle in a day? Add yours with /reason in capture mode.
- Maria: `/reason · capture` Check-in, 60. Follow-up booking’s mine too: 40.
- Tomasz: `/reason · capture` Triage, 45 if nobody’s off.
- Leila: `/reason · capture` Pharmacy, about 50.
- Dr Adeyemi: (dictated) `/reason · capture` Twenty. On a good day.
- Skill · Capture result: Five capacities saved as proposed, each in its author’s name. Suggested from them: [Proposed] Cause · *The doctor’s room, at twenty a day, limits how many patients the clinic sees.*
- What changes: The likely constraint has a name, worked out from numbers each person put in themselves.

**Scene 3.** *After the one-hire drawing.* Sam · desktop · Back office · Monday 16:30.
- Sam: Accept that for now: the doctor’s room limits how many we see. And what if we hire for the front desk anyway?
- Skill · Capture result: Accepted for now by Sam: [Accepted] Cause · *The doctor’s room, at twenty a day, limits how many patients the clinic sees.*
- Skill · Capture result: Suggested by the skill, saved as proposed: [Proposed] Injection · *Hire a second receptionist.* → [Proposed] Predicted effect · *Patients reach the waiting room sooner.* → [Proposed] Predicted effect · *The clinic still sees twenty a day.*
- Skill · Next step: Look at the doctor’s day before spending anything. Why: a hire changes the twenty only if it gives the doctor’s room more time.
- What changes: The hire is tried out on paper, where it costs nothing.

**Scene 4.** *After the doctor’s-day drawing.* Dr Adeyemi’s phone · team chat · Consulting room · Tuesday 11:52.
- Dr Adeyemi: (dictated) `/reason · capture` I lose about two hours a day. I re-take histories triage already took, because I can’t find them, and I print the forms myself.
- Skill · Capture result: Saved, from Dr Adeyemi, as proposed: [Proposed] Cause · *About two of the doctor’s eight hours go on work that doesn’t need a doctor.* [Proposed] Cause · *The doctor re-takes histories triage has already taken.*
- Skill · Next step: Ask triage whether the history could be recorded where the doctor reads it. Why: it would give back time inside the constraint without hiring anyone.
- What changes: Dr Adeyemi’s two lost hours are on record, said in the minute between two patients, with a question for triage.

**Scene 5.** *Inside the next section, after “…the cheapest place to find some was already inside it.”* Tomasz’s phone · lock screen · Corridor · Tuesday 12:10.
- Notification · Dr Adeyemi: Tomasz, could triage record the history where I read it?
- Tomasz: `/reason · capture` Yes, if the template’s on the triage tablet. Right now it’s paper only.
- Skill · Capture result: Saved, from Tomasz, as proposed: [Proposed] Obstacle · *The history template is only on paper.* → [Proposed] Intermediate objective · *The template is on the triage tablet.*
- What changes: Tomasz names what triage would need before being asked to take on the work.

**Scene 6.** *After “If you cannot tolerate that on a dashboard, none of this is available to you.”* Maria’s phone · lock screen · Front desk · Wednesday 08:02.
- Notification · Sam: Maria, from today keep about four patients ready for the doctor, rather than clearing the queue. The reasoning’s in the thread.
- Maria: `/reason · ask` So I’m not meant to clear the queue?
- Skill · Answer: That’s Sam’s change. The saved reasoning: checking people in faster than the doctor can see them only fills the waiting room.
- Maria: `/reason · capture` Patients will think we’re slower, and they’ll complain to the desk.
- Skill · Capture result: Saved, from Maria, as proposed: [Proposed] Undesirable effect · *Patients see the desk slow down and complain to it.* Next: who explains the wait at the door?
- What changes: Maria can see why the desk’s job has changed, and the worry about complaints is saved in Maria’s name instead of absorbed at the desk.

**Scene 7.** *After the constraint-moves drawing.* Sam · desktop · Back office · Wednesday 17:30.
- Sam: If Tomasz’s template works, the doctor sees more people. Then what?
- Skill · Answer: Output rises toward forty, where follow-up booking would set the number. The accepted cause holds for now.
- Skill · Capture result: Added to the backlog on the accepted cause: re-check every station’s capacity when output nears forty.
- What changes: The accepted answer carries a note saying when to check it again.

**Scene 8.** *After “…by good people whose own numbers depend on it.”* Leila’s phone · team chat · Dispensary · Monday 10:05.
- Leila: `/reason · capture` Why does every prescription need the doctor’s countersignature? I page Dr Adeyemi about eleven times a morning.
- Skill · Capture result: Saved, from Leila, as proposed: [Proposed] Cause · *Every prescription needs the doctor’s countersignature.* → [Proposed] Cause · *The pharmacist interrupts the doctor about eleven times a morning.*
- Skill · Next step: Find out who brought the rule in and what it was protecting. Why: its purpose tells you what any replacement has to keep.
- What changes: A rule that was “just how it’s done” is now a saved statement, with a question attached: what was it for?

**Closing card.** That was the reason-commons skill. It doesn’t decide who is right. What it adds is a record: who said what, what is accepted for now and by whom, what is disputed, and the one thing worth checking next. You can use it on your own work today, in Claude Code, Codex and other agents that support skills. Install line, then: How to install and start the skill; Part two, in practice: The Arrows Nobody Checks; Read this part without the margin.

## Part two · The Arrows Nobody Checks

**Cover card.** In the margin: five explanations, written down. The same clinic, the same five people. In this part the five use the reason-commons skill to get each explanation out of its author’s head, and to ask the story’s questions of each other’s reasoning, not of each other.

**Scene 1.** *After “Nothing has changed except that it is now outside you, where it can be looked at.”* Tomasz’s phone · lock screen · Triage room · Thursday 13:30.
- Notification · Sam: Everyone: put your explanation of the waits in here with /reason, one link at a time. Nobody argues yet.
- Dr Adeyemi: (dictated) `/reason · capture` Countersignature, so interruptions, so overruns, so notes after seven, so tomorrow’s notes aren’t ready.
- Tomasz: `/reason · capture` The ten-minute appointment rule.
- Skill · Capture result: Saved as proposed, each in its author’s name. Sam’s, Maria’s and Leila’s came in this morning. Nothing is accepted yet. [Proposed] Cause · Dr Adeyemi · *Every prescription needs the doctor’s countersignature (first of five links).* [Proposed] Cause · Tomasz · *The ten-minute appointment rule.* [Proposed] Cause · Sam · *Funding.* [Proposed] Cause · Maria · *The referral backlog.* [Proposed] Cause · Leila · *Nobody asks us.*
- What changes: All five explanations are written down, each in its author’s name, before anyone argues for one.

**Scene 2.** *After the seven-questions drawing.* Sam · desktop · Back office · Thursday 15:00.
- Sam: Help me make my funding point something people can check.
- Skill · Next step: “Funding” can’t be true or false yet. What about funding causes the wait?
- Sam: Our budget fell 12% in real terms since 2019.
- Skill · Capture result: Revised, from Sam, as proposed: [Proposed] Cause · *The budget fell 12% in real terms since 2019.* Next: is that enough on its own to cause the wait, or does something else have to hold too?
- Sam: It only matters if money is what the doctor’s room is short of.
- Skill · Capture result: Saved on the link to the wait, as an assumption from Sam: *only if money is what the doctor’s room is short of.*
- What changes: “Funding” becomes a claim that can be checked, with the condition it depends on written on the link.

**Scene 3.** *After “…because they attacked it and it held.”* Maria’s phone · team chat · Front desk · Friday 09:40.
- Maria: `/reason · capture` I don’t see how the countersignature makes the notes late. What am I missing?
- Skill · Capture result: Challenge saved, from Maria, on Dr Adeyemi’s link: [Disputed] Link · causes · *Consultations overrun → notes are written after seven.* Next: Dr Adeyemi, if this link holds, what else would be true?
- Dr Adeyemi: (dictated) `/reason · capture` On days the pharmacy’s closed, I’m done by six.
- Skill · Capture result: Saved on the link, from Dr Adeyemi, as proposed: [Proposed] Observation · *On days without pharmacy interruptions, the doctor’s notes are finished by six.*
- What changes: Maria’s question sits on one link of Dr Adeyemi’s chain, and Dr Adeyemi answers it with an observation anyone can check.

**Scene 4.** *After “Each of them puts their chain on the wall, and then everybody gets the questions.”* Tomasz’s phone · team chat · Triage room · Monday 08:20.
- Tomasz: `/reason · capture` Could something else have done it? Waits were just as long in 2018, before the budget fell.
- Skill · Capture result: Saved, from Tomasz, as proposed, with an objection on Sam’s link: [Proposed] Observation · *Waits were as long in 2018, before the budget fell.* [Disputed] Link · causes · *The budget fell 12% since 2019 → patients wait.*
- Skill · Next step: Sam, do the 2018 waiting figures match your records?
- What changes: Sam’s explanation meets one specific objection, from the triage room, and it is the link that is in question, not Sam.

**Scene 5.** *After “…which is a different kind of object entirely.”* Sam · desktop · Staff room, all five present · Monday 17:00.
- Sam: Show the chain we tested this afternoon.
- Skill · Tree view: Current reality, proposed: [Proposed] Cause · *The ten-minute appointment rule.* → [Proposed] Cause · *Histories get re-taken and notes go unwritten.* → [Proposed] Undesirable effect · *A third of patients come back with the same complaint.*
- Sam: Maria, Tomasz, Dr Adeyemi and I accept that for now. Leila doesn’t, yet.
- Skill · Capture result: Accepted for now by Sam, Maria, Tomasz and Dr Adeyemi. Leila has not endorsed it. Tomasz’s objection to the funding link stays open.
- What changes: Everyone can see which links are agreed and by whom, which one is still in question, and who has not agreed yet.

**Closing card.** That was the reason-commons skill. It asks the questions in this piece of whatever is said, keeps each objection on the link it is about, and records who has accepted what, for now. You can use it on your own work today, in Claude Code, Codex and other agents that support skills. Install line, then: How to install and start the skill; Part three, in practice: Five Shapes; Read this part without the margin.

## Part three · Five Shapes

**Cover card.** In the margin: five questions, five shapes. The clinic has its map. In this part the skill picks the right kind of tree for each question without anyone needing its name, and the people who would carry the change find its costs while they are still on paper.

**Scene 1.** *After “…it isn’t even the first one.”* Sam · desktop · Back office · Tuesday 07:45.
- Sam: We’ve got the map. Where do we start?
- Skill · Next step: With what should be happening: one sentence saying what success looks like for the clinic. Why: every fix on the map can then be checked against it.
- What changes: The first step is one sentence about what the clinic is for, which every fix can be checked against.

**Scene 2.** *After the goal drawing.* Tomasz’s phone · lock screen · Triage room · Tuesday 12:20.
- Notification · Sam: `/reason · capture` Draft goal: see more patients, faster.
- Tomasz: `/reason · capture` Faster isn’t the point if a third come back. Everyone in the catchment who needs to be seen is seen, and doesn’t need to come back for the same thing.
- Skill · Capture result: Saved, from Tomasz, as proposed, revising Sam’s draft: [Proposed] Goal · *Everyone in the catchment who needs to be seen is seen, and does not need to come back for the same thing.*
- Sam: `/reason-accept`
- Skill: Accepted for now by Sam.
- What changes: Where the clinic is trying to get to is written down and accepted for now, so the ten-minute rule can be checked against it.

**Scene 3.** *After “…It stops existing.”* Dr Adeyemi’s phone · lock screen · Consulting room · Wednesday 14:00.
- Notification · Sam: `/reason · capture` Dr Adeyemi wants longer appointments again. We can’t afford fewer slots.
- Skill · Capture result: Saved as a conflict, all proposed: [Proposed] Objective · *Serve the catchment.* [Proposed] Need · *See enough people.* [Proposed] Prerequisite · *Ten-minute slots.* [Proposed] Need · *Consultations that hold up.* [Proposed] Prerequisite · *Longer slots.* Next: what has to be true for ten minutes to rule out a good consultation?
- Dr Adeyemi: (dictated) `/reason · capture` Only if the time goes on the patient. Most of my overrun is the history being taken twice.
- Skill · Capture result: Assumption challenged, from Dr Adeyemi: [Disputed] Assumption on the link · *Consultation length is the only lever on quality.*
- What changes: Both positions are on the page as needs, and the argument moves to one assumption that can be checked: where the overrun time goes.

**Scene 4.** *After “…the obvious somebody is Maria, who has no forty minutes.”* Maria’s phone · lock screen · Front desk · Wednesday 16:40.
- Notification · Sam: Maria, the plan needs the notes ready by eight. Who would prepare them?
- Maria: `/reason · capture` It’d be me, and there aren’t forty minutes before eight.
- Skill · Capture result: Saved on the notes plan, from Maria, as proposed: [Proposed] Undesirable effect · *Preparing the notes takes forty minutes the front desk doesn’t have before eight.*
- What changes: The plan’s cost is on record from the person who would carry it, before the plan is agreed.

**Scene 5.** *After the obstacles drawing.* Sam · desktop · Back office · Thursday 09:00.
- Sam: What’s in the way: the summarising has to happen before eight, the only person who could do it is the busiest, and there’s money for exactly one hire.
- Skill · Capture result: Saved Sam’s three obstacles. Suggested by the skill, what gets past them, in order, all proposed: [Proposed] Intermediate objective · *A written summarising standard.* → [Proposed] Intermediate objective · *Time freed, or another person found.* → [Proposed] Intermediate objective · *The one hire spent on notes, not the desk.*
- Skill · Next step: Decide who writes the summarising standard. Why: the hire can’t be trained on a standard that doesn’t exist yet.
- Sam: Tomasz and Dr Adeyemi, by Friday.
- What changes: The one hire goes to the notes, not the desk, and the order is set by what depends on what.

**Scene 6.** *After the Maria section, before “For the first time, they can find out.”* Maria’s phone · team chat · Front desk · Monday 08:30.
- Maria: `/reason · capture` My referral backlog and the countersignature are the same jam. Notes ready by eight fixes both.
- Sam: `/reason · capture` I don’t think so. The backlog is the hospital’s, not ours.
- Skill · Capture result: Saved Maria’s link as proposed, with Sam’s objection: [Disputed] Link · causes · *Notes ready by eight → the referral backlog shrinks.* Next: if Maria is right, the backlog shrinks on days the notes are ready by eight. Check for two weeks?
- Maria: Deal.
- Sam: Deal.
- What changes: Two people disagree, and for once there is something specific to check.

**Closing card.** That was the reason-commons skill. It chooses the shape that fits the question, so nobody has to learn the method’s vocabulary first, and it keeps every claim at an address: who made it, who accepted it, and what would settle it. You can use it on your own work today, in Claude Code, Codex and other agents that support skills. Install line, then: How to install and start the skill; Start again, in practice: The Wrong Queue; Read this part without the margin; See it working: the claim-tree annotation demo.

## Critique and response

An independent reviewer critiqued the first draft against `SKILL.md`, the schema, the Discord README and the voice guide (2026-10-20). Its main findings, and what changed:

1. **The skill messaged people unprompted** in four notifications, contradicting the margin's own rule and the bot's "no proactive interjection". *Changed:* every notification is now from a person (Sam or Dr Adeyemi).
2. **Replies were captured that nobody invoked the skill on**, and the prototype has no voice input. *Changed:* every saved contribution carries `/reason · capture`; Maria's question in part one uses ask mode and changes nothing; Dr Adeyemi dictates.
3. **Acceptance from a "Yes"** to a structural question, merging two different meanings into one node (part two, scene 4), and acceptances nobody saw. *Changed:* that scene is replaced by Tomasz challenging Sam's funding link, which keeps part three's "It is Maria who spots it" new; the part-two map is accepted on screen by four named people with Leila explicitly not yet; Sam's acceptance in part one is shown.
4. **Wrong arithmetic.** At thirty-eight a day the doctor's room still limits, and the draft read the queue as the constraint against its own scene 1. *Changed:* part one, scene 7 now asks what happens past forty and adds a backlog note to re-check the stations then, without a time jump.
5. **The skill authored claims credited to people** (Sam's sixty, the goal sentence, the obstacles) and presented its own traces unmarked. *Changed:* Sam says sixty, Tomasz writes the goal, Sam names the obstacles, and the skill's traces and objectives are labelled "Suggested by the skill".
6. **Anchors.** Part two's first scene sat before the line saying no chain had left anyone's head, and Maria's question before "It's a legal move". *Changed:* both moved after; Sam's hire money no longer appears before the story mentions it.
7. **Aphoristic "What changes" lines** (ten of them). *Changed:* replaced with plain statements of what is now on record, mostly in the reviewer's suggested wording.
8. **Pronouns, length and schema.** *Changed:* pronouns for the cast removed; scenes trimmed, with summaries drawn as small tree fragments; evidence is an `Observation`; conflict positions are `Prerequisite`; the skill no longer speaks in the first person.

Not adopted or adopted differently:

- **Part three, scene 1 "restates the story".** Kept and cut to two bubbles: it is the one place the skill chooses a tree from a plain question, which is the point of part three.
- **Merge part three's walk-forward scene into the side-effect scene.** Done by cutting the walk-forward scene, since the story already draws that chain.
- **Replace Leila's headscarf with a dispensing tray.** The headscarf stays as part of how Leila looks; a pill bottle is added as the role marker.
- **Review tokens.** `/reason-accept` endorses a displayed review; the goal scene shows the saved fragment and Sam's `/reason-accept` without a separate `/reason · review` step, to keep the scene short.
- **Layout and avatar notes are Stage 2 material.** Kept here briefly as the build brief, because the margin has no separate visual script.
