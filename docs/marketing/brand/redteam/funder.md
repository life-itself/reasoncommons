---
title: Red team — funder / partner view
target: positioning-v1.md (with brand-narrative-v1.md)
created: 2026-10-17
---

# Red team: the funder and partner view

Point of view: a programme officer at a funder of collective epistemics / AI-for-good / civilisational resilience. I read dozens of "AI for better discourse" pitches a month. I fund theories of change I can believe, teams I think will deliver, and things that are not already done better by a grantee I fund.

Verdict in one line: an unusually honest internal document that, as positioning, would not get past my first screen, because it never states the one thing that is genuinely distinctive, it skips the most obvious competitor, and its only evidence of use is two founders running it on their own repo.

## 1. Distinctiveness: can I say "why this and not X" in one sentence?

No. After reading I can say what it does; I cannot say why it wins.

**Talk to the City is missing entirely.** The competitive frame (§4) lists forums, Google Docs, Kialo/Argdown, Polis/Loomio, consultants and ChatGPT. It does not list Talk to the City, the Habermas Machine, Polis's own LLM summarisation, Harmonica, or the dozen other "AI reads the discussion afterwards" tools I see every month. That omission is fatal because the draft's claimed differentiator is exactly their pitch:

> "unlike documents, threads, argument-mapping tools or consultants, it adds the structure *after* people talk, by AI, so the conversation stays a conversation"

Talk to the City already takes free-form input, has an LLM cluster it into claims, keeps verbatim attributed quotes, and leaves people talking normally. If "structure after, by AI" is the wedge, the wedge is taken. A programme officer who knows the field will stop reading here.

**The Polis/Loomio line is wrong in a way I'd notice.**

> "They do not keep the *reasoning* behind a position, so the group cannot build on why."

Polis reports clusters of statements; TttC keeps quoted reasons. The real difference is not "keeps reasoning" but *what shape* and *for how long*. Overclaiming a competitor's weakness signals you have not looked closely at them.

**What is actually distinctive is buried or absent.** Reading across both drafts and the changelog, the defensible differences are:

- **Causal and action structure, not clusters.** Polis and TttC answer "what do people think and where do they agree". This answers "what has to be true for our goal, what blocks it, what do we do, in what order". That is a goal-to-action chain, not opinion mapping. §4 gestures at it ("cover action as well as belief") in one clause on the Kialo line only.
- **Persistent, versioned state with an explicit human acceptance gate.** Most AI-sensemaking tools produce a report per round; the report is the end. Here the tree is the durable object, each change is proposed, accepted or disputed, snapshotted, and the next conversation is read against it. That is the "compound" claim, and it is the real moat if it works. It is listed as plumbing in §6 rather than argued as the category difference.
- **Git-native review.** "Pull requests for discourse" is the most distinctive idea in the whole document and it has been demoted to "use only where the audience is builders". For a funder, it is the clearest mental model on offer: proposals, review, merge, history.

The one sentence the draft should let me write, and currently does not: *"Polis and Talk to the City tell a group what it thinks at a moment; Reason Commons keeps a versioned map of what the group has agreed must be true and what it will do, and reads every new conversation against it as proposed changes that people accept or reject."* If that is not the claim, I do not know what is.

**Plain ChatGPT.** The answer given ("forget it, not know who said what") is right but weak: Claude Projects, ChatGPT memory and a shared Google Doc of a tree get you 60% of the way. The honest moat is the acceptance protocol and the method (LTP's Categories of Legitimate Reservation as a challenge discipline), not memory.

## 2. Credibility: aspirational dressed as current

The draft's §6 is commendably candid about what is aspirational. The problem is that §1 and §2, which are the parts that would become copy, contradict §6.

**The positioning statement describes the aspiration in the present tense.**

> "turns ordinary discussion into a shared, addressable tree of what the group thinks is true and what it will do"

> "People talk the way they already do. AI reads the conversation into a tree"

> "Over time a group gets a map of its own thinking and its own plan that gets better every time it talks, instead of starting again."

Today, per §6 and the changelog, people talk *to an AI agent in a terminal* and the agent builds the tree with them. Reading a group's forum or Discord thread is "Demoed with rehearsal material only; the `contribution-proposals` skill that did it is retired." "Ordinary discussion" and "the way they already do" are not true today. "Over time ... gets better every time it talks" has been observed for exactly one group of two people for about three weeks (skill shipped 2026-09-28).

**The headline itself fails the draft's own test.** The scoring table gives "Conversations that compound" a 2 on "true today" and notes: "True in a skill session; not yet true for a forum." Then it is recommended as the winner. A funder will take the headline as the claim. If the thing that compounds is "a session with Claude Code", say so, or pick a headline that is true.

**"Forty-year-old method that works" is borrowed credibility.** The evidence that TOC/LTP works is in manufacturing and operations. There is no cited evidence it works for movements, research circles or public discourse, which is the entire bet. "Works" needs a scope or a source.

**"We make the same rigour cost a conversation"** (§4, consultants). Unproven equivalence. Has an LTP practitioner compared a skill-built tree with a facilitated one? The practitioner row in §3 asks them to ("tell us where it is wrong"), which tells me it has not been done.

**The $2k/day and "six trees in your head" figures** are flagged in §6 as unsourced but are load-bearing in the narrative's loop. If the loop is the "why now", its premises need a source.

**The proof points are mostly about process plumbing in the founders' own repo.** PR templates, a tree check in CI, typed change-acceptance receipts. To a funder this reads as: the only user is the team, and the most-developed feature is governance of the team's own commits. It also risks the opposite of the intended impression: a protocol where "fix it" requires a typed proposal and a recorded acceptance receipt sounds heavy, not like "the conversation stays a conversation".

**Traction absent entirely.** Nowhere: number of installs, number of groups that have tried it, number of trees with more than two contributors, any testimonial, any user outside Rufus and David. The funder row in §3 admits it: "Evidence that it changes outcomes for a group other than us: none yet." Honest, but then the positioning should be built around getting that evidence, not around a transformation claim.

**The "no app" claim is a diligence trap, and it hides your best traction.** §6 "Watch" flags a separate Reason Commons app. The changelog (2026-09-06) is more specific: there is an app that imports and exports `.ltp.yaml`, and "the live Reason Commons space connected to the 2R-Research repository" superseded the dashboard model. So:

- A funder who looks at GitHub will find `Promise-Foundation/reason-commons`, an app, and a live space, and then read "There is no app to sign up for." That looks either inaccurate or like a team with two products and no shared story.
- A live space used by the 2R Research Circle is the closest thing in the whole project to *a group other than us*. The positioning does not mention it. Either it is real traction and should lead the funder case, or it is not being used and the 2R tree claims should be scoped down accordingly.

**The 2R tree is described as proof of the method, not of adoption.** "A tree of change for Second Renaissance exists, drawn from the movement's written corpus." Drawn by whom, accepted by whom? If 2R did not review and accept it, it is an analyst's model of a movement, which is what consultants already produce.

**Access contradicts the equity claim.** The funder promise is "a cheap, open route to structured collective reasoning for the civic and movement groups that could never afford it". The product is a skill for Claude Code / Codex, installed with `npx`, which needs a paid AI subscription and command-line fluency. The civic groups in the promise mostly have neither. That is not "cheap" for them; it is cheap for AI-native builders. Either the first audience is builders and stewards who act on a group's behalf (say so, and make the steward the theory of change), or the route to civic groups needs a step that does not exist yet.

## 3. Scale of ambition: is "transforms collaboration" earned?

It is too big and too small at the same time.

**Too big for the evidence.** "Transforms collaboration" (the frame the narrative is aiming for) on the basis of a CLI skill used by its two authors is the classic shape of the pitches I decline: a civilisational claim attached to a prototype with no users. The tone section says "Concrete, not visionary" and "Honest, not hyped"; the frame breaks both rules.

**Too small for my portfolio.** Funders of collective epistemics are not buying "groups stop losing what they work out in conversation". That is a productivity benefit for small teams; a SaaS company can serve it. What would interest me is the commons claim the draft deliberately shelves in §7: public, addressable, versioned trees of what a movement or field believes and plans, that anyone can propose changes to and that accumulate over years, as public infrastructure in the way Wikipedia or open data are. That is a civilisational-resilience story with a clear "why open, why grant-funded, why not a startup". The draft makes the infrastructure argument nowhere. Ironically the founder's track record (open data, open knowledge infrastructure) is exactly the credibility that argument would need, and it is not mentioned.

**No theory of change from skill to commons.** The narrative's "Today / Being built / The aim" jumps from "install a skill" to "a commons ... built on over years" with nothing between. I need the middle: who adopts first, what they do with it weekly, what makes a second group join, what we would measure, how it is sustained after the grant. A loop diagram for why the method never spread is given; a loop for why it will spread now is not.

**Team and delivery are invisible.** Neither draft says who Rufus Pollock and David Joseph are, what they have built before, what Life Itself and the Promise Foundation are, how much time they have, or who maintains this. For a funder, "can the team deliver" is half the decision. The about page has a paragraph; the positioning has nothing.

## 4. The ask: what I'd want to see next

"Talk to us about a pilot with one community" is the right shape and far too vague. Before I would take a second call I want:

1. **A named pilot partner and a named steward.** Most plausibly the 2R Research Circle, given there is already a live space. Who in that group runs it, how often, on which conversations.
2. **A pre-stated outcome measure.** Something a sceptic would accept: rate of re-litigated arguments, share of decisions traceable to an accepted node, number of distinct contributors whose points were accepted into the tree, time-to-acceptance, retention of contributors across months. Baseline before, measure after.
3. **A head-to-head.** Run the same corpus through Talk to the City (or Polis + LLM report) and through Reason Commons, and show what the group can do with each six weeks later. If the answer is "the same", I want to know before funding.
4. **The forum-to-tree step, working on real material.** It is the leap the whole brand opens on, and it is currently retired. Even a crude working version with real threads beats any copy.
5. **Budget, timeline, team time, and what success at month 6 and month 18 looks like**, including how a non-terminal user gets in.
6. **Resolution of the app question.** One product story, or a clear "skill now, app later, here's why".

## The three most important changes, ranked

1. **State the real differentiator and confront the nearest competitor.** Add Talk to the City (and AI-summarised Polis) to the competitive frame and replace "structure after people talk, by AI" (which they already do) with the actual wedge: a persistent, versioned goal-to-action tree with a human acceptance gate that each new conversation is read against as proposed changes ("pull requests for discourse"). Fix the overclaim about Polis.
2. **Make the headline and positioning statement true today, or tense them honestly.** "Conversations that compound", "ordinary discussion" and "the way they already do" describe the retired forum-reading step. Either rewrite to what ships (a group reasons with an AI steward and keeps an accepted, attributed tree) or mark the leap as "next" in the same sentence. Resolve the "no app" versus live-2R-space contradiction, and if 2R is using it, lead the funder case with that.
3. **Give funders a theory of change, a team, and a concrete pilot.** Add the missing middle from skill to commons (first adopters, steward role, how it spreads, why open infrastructure), say who the team is and why they can deliver, and replace "talk to us about a pilot" with a named partner, an outcome measure and a comparison against an existing tool.
