# Critique — A1, *Sixty people waiting*

Adversarial editorial review of [`draft.md`](draft.md), 2026-09-20. Checked against [`01-bottleneck-plain`](../../../01-bottleneck-plain/index.md) (the source it compresses), [`04-arc-v2.md`](../04-arc-v2.md), [`voice-guide.md`](../voice-guide.md), [`01-evaluation.md`](../01-evaluation.md), and [`where-does-the-thinking-go/01-same-conversation`](../../../where-does-the-thinking-go/01-same-conversation/index.md) as the sibling opener. Prose only; no figure notes, per brief.

**Body word count: 398** (from "A clinic opens at eight" to the end, excluding the header block and the key-claim line; the in-body bolded claim is 36 of those, so 362 of running prose). In range, but the bottom of it — B1 runs 478. There is room for the three or four sentences this chapter is missing, and it needs them.

## 1. Fact-check and arithmetic

**Verdict: every figure checks out against the source and against itself, with one false claim and one missing premise.**

Correct and faithful to the source:

| Claim in draft | Source | Verdict |
|---|---|---|
| Stations at 60 / 45 / 20 / 50 / 40 | line 30 | ✓ exact |
| Doctor sees twenty, so the clinic sees twenty | lines 26, 33 | ✓ `min(60,45,20,50,40) = 20` |
| Twenty a day for four years | line 26 | ✓ verbatim |
| Man in his sixties, second visit, cough since March, three hours Tuesday, left at four for his grandson, will try again next week | line 37 | ✓ every particular preserved |
| Forty a day, five days a week, "something like ten thousand a year" | line 39 | ✓ `40 × 5 × 50 = 10,000`; at 52 weeks, 10,400. "Something like" is an honest hedge and the right one |
| Maria: front desk, phone before the lights are on, queue open to close, complaints name her desk, "visibly and unarguably, the hardest-working person in the building", "irrelevant to how many people this clinic helps" | lines 20–24 | ✓ faithful compression |
| "Maria was never the problem. She was busy absorbing the anger that something else was generating." | line 57 | ✓ verbatim |
| "The station that sets the number — the one every other station is waiting on, whether it knows it or not — is the constraint. Every system has one." | line 61 | ✓ verbatim |
| Goldratt's Theory of Constraints as the lineage | line 172 | ✓ supported ("behind it Eliyahu Goldratt's Theory of Constraints") |

**Finding 1 (must fix). "Four of those numbers do not matter" is false, and the series contradicts it two chapters later.** The source says the opposite twice. Line 33: the clinic would manage "forty, which is what it would manage if the doctor's station matched the next tightest one" — the follow-up desk's 40 is the ceiling on every gain the next two chapters describe. Line 113: "Get her to fifty a day and follow-up booking, at forty, becomes the constraint." And the arc gives A2 the beat "expect it to move once you do" (04-arc-v2, A2). So the draft teaches the reader something A2 has to un-teach in its closing line. The three larger numbers determine where the constraint goes next; the 40 caps the first move. What is true today is narrower: only the smallest number is doing any work *right now*. Write that instead — "Today, only the smallest number is doing anything" — and the sentence is both true and a quiet setup for A2.

**Finding 2 (must fix). "The other forty go home" does not follow from what the draft has said.** The draft establishes sixty only as check-in's *capacity* ("check-in can process sixty people a day"). Capacity-to-process is not arrivals. To get forty turned away you need sixty people actually arriving, which the draft never states. The opening — "By noon, sixty people are waiting" — is a snapshot, not a daily count, and if sixty are already waiting at noon the honest reading is that demand runs well above sixty and the number sent home is more than forty. The source has the same latent gap but patches it later ("Sixty people checked in, against twenty the doctor can see. The other forty do not vanish", line 69) in a section the draft cut. Compression has made the gap load-bearing. One clause fixes it: sixty people a day come through the door.

**Finding 3 (overclaim, unsupported). "which is what being next to a constraint usually looks like from the outside."** Not in the source; the draft's own addition. Maria is not next to the constraint — she is two stations upstream of it (check-in → triage → doctor). And the generalisation is not true as stated: the station immediately before a constraint characteristically shows a *pile*, not anger; anger accrues wherever the public can reach a human being, which may be nowhere near the constraint. The chapter's own logic depends on Maria being visible, not adjacent. See §7.

**Finding 4 (unused fact, and a gap).** The draft's own header block lists "Dr Adeyemi nine years in post" among the facts carried over, but the prose never names her or mentions her at all. She is "the doctor" — a box with the number 20 on it. This is not a factual error, but it breaks the arc: 04-arc-v2 makes Dr Adeyemi's two hours of admin *the open question that carries Series A*, asked in A2 and answered in A6. A2 cannot ask "but why is her admin there?" about a person the reader has never met. Either name her here in a clause, or delete her from the header block so the next drafter does not assume she is already on the page.

**Not errors, noted for whoever drafts A2.** The source's "a shade under eighteen minutes each" (line 86, repeated line 174) is loose: 6 hours ÷ 20 patients is 18 minutes exactly. The 26 that A2 depends on is sound — 480 minutes ÷ 18 = 26.7, rounded down. Nine years in post and four years of flat output are consistent. The clinic is never named "Ashfield" in this draft; if A2–A8 refer back to it by name, A1 should christen it.

**Disclosure.** B1 tells the reader in its fourth line that Maren is invented, and repeats it in a closing italic. The source piece discloses the clinic as a composite in its methodology. This draft discloses nothing. A series whose whole subject is checking claims cannot open with an invented clinic, five hard numbers and an unlabelled ten-thousand-a-year figure. A hostile reader finds this first, and is right to.

## 2. Can a cold reader say the key claim afterwards?

**Half of it.** The key claim has two clauses and the chapter proves one.

"How much any system achieves is set by one constraint" — yes. A reader will say "the slowest station decides how many you get through", probably in those words, because the arithmetic is airtight and the bolded sentence hands them the noun. That is a genuine success.

"And it is almost never where people are busiest" — no. They have been *told* this twice ("They are all wrong"; "She is also irrelevant") and shown one instance of it. They have not been given a reason, so they cannot regenerate it. The source earned the second clause in a whole section the compression dropped: "Everybody's busy" (lines 63–75), whose argument is that a non-constraint running flat out *manufactures work the constraint cannot absorb*, so full effort everywhere is evidence that nobody has found the constraint. That is the mechanism that converts "Maria happens to be irrelevant" into "busyness is systematically the wrong signal". Without it the reader has an anecdote, not a claim they can carry to their own organisation — which is the whole point of the reader profile in the arc ("someone who runs or cares about something complex … has felt that effort isn't adding up").

Two sentences would do it, and the budget is there. Something like: *A station that is not the constraint, running flat out, only manufactures work the constraint cannot absorb. When everyone is at full stretch, the honest reading is not that the place is well run — it is that nobody has found the constraint and everybody is compensating for it at once.* That is the second-best sentence in the source piece and its absence is the biggest single loss in the compression.

## 3. Does it earn "they are all wrong"?

**No. It asserts the reversal before the reader holds the opinion being reversed, then never lets them be wrong.**

The structural problem: "They are all wrong" arrives in sentence three, when the reader has read twenty-two words and has no view about the front desk whatsoever. Nothing is being overturned — there is nothing yet to overturn. What the line actually does is promise cleverness: *stay, I am about to surprise you*. That is a different and weaker effect than counterintuition, and a phone reader has seen that promise a thousand times.

Worse, the chapter never gives the reader a chance to be wrong. The staff's answer is reported, not shared. The best case for the front desk is never made: the draft says Maria is irrelevant before the reader has any reason to think she matters, so the demolition lands on a straw position that was handed to strangers rather than to them. The voice guide asks for the opposing view stated fairly (checklist box 6); the source at least concedes what the front-desk hire actually buys — "patients reach the waiting room sooner. You will have spent the entire budget to make people frustrated sitting down instead of standing up" (line 55). That joke works *because* the concession is real first.

The source earned the reversal with a decision the reader participates in: "Where do you put the one hire?" — front desk, still twenty; triage, still twenty; the doctor, twenty-six. The arc assigns that to A2 and I would not move it back. But A1 does not need the hire to make the reader complicit; it needs the reader to point at the desk *with* the staff for one beat before the floor goes. Two candidate moves, either cheap:

- Delay the verdict. Let the queue, the phone and the complaints stand as the obvious diagnosis for one paragraph, with the reader inside it, then turn. Presently the turn comes before the setup.
- Or make the reader answer. A single direct question — where would you put the money? — costs eight words and converts a told reversal into a felt one.

What must *not* happen in revision: do not soften "They are all wrong." The sentence is right; its position is wrong.

## 4. Is the goal stated plainly enough to carry seven chapters?

**The words are right. The placement contradicts the sentence's own claim about itself.**

"Say what the clinic is for, plainly, because everything else depends on it" sits in paragraph eight, *after* everything that depended on it: after the arithmetic, after "four of those numbers do not matter", after the ten thousand. A reader who has already been told which number matters does not need to be told what the clinic is for; they experience the paragraph as a recap, skim it, and the one sentence the next seven chapters rest on is the one sentence they skipped.

The arc requires throughput said plainly here, and the draft does have it: "how many patients come out the far end". That is exactly right — plain, visual, no jargon, and it will survive being quoted back. But it is buried mid-paragraph in a fifty-word sentence carrying three other jobs. It needs to be a short sentence on its own line.

Also, "Say what the clinic is for, plainly" is a stage direction: an imperative addressed to nobody, the narrator telling himself what to do next in front of the reader. Voice guide item 2 wants us speaking as the people doing the work, not narrating the construction of the essay. Make it a statement of fact about the clinic.

Recommended position: immediately after "She is also irrelevant to how many people this clinic helps." That line raises the question "irrelevant to *what*?" and the goal is the answer. Then the capacities arrive as the answer to a question the reader is already holding, and "it is arithmetic" lands on a goal the reader has agreed to. At present the arithmetic is true of a number the reader has not yet been told to care about.

## 5. Does it open a series, or is it a compressed long piece?

**Compressed long piece, with visible seams.** Set beside B1 the difference is not subtle.

B1 does opening-a-series work that A1 does not: it names the series and the chapter position, opens on a named person with her own quoted sentence, discloses the invention immediately, introduces the movement *after* the person in two plain sentences, and closes on a turn that opens a question rather than summarising ("The record is complete, and the movement still cannot tell you what it concluded the first two times"). It also leaves the reader with a *character*, not just a claim, so chapters 2–5 have someone to come back to.

A1's seams, quoting them:

- **"Here is why."** This is the scar left where a section heading was cut. The source had "### Five stations, one number" there. In a chapter you do not announce that an explanation is coming; you explain.
- **The capacity sentence** — 61 words, five clauses, five numbers — is five short sentences from the source (line 30) fused into one. On a phone this is the paragraph people bounce off. The source's staccato version is better, not worse, and costs no extra words.
- **Paragraph eight** reads as a summary paragraph from a longer argument, because that is its shape: it restates the goal, restates the throughput claim, and restates that one station governs it. Three restatements of things the chapter has been doing.
- **No character carried forward.** Maria is introduced, used as the counterexample, and closed out ("Maria was never the problem"). The doctor — the one the series is actually about — is a capacity number. The chapter ends with nobody to follow into A2. B1 ends with Maren still unanswered.
- **No disclosure line, no chapter furniture** (eyebrow, lede). The lede may come from the key-claim line at build time, in which case fine; the disclosure will not appear by itself.

The good news is that the underlying material is series material. What is missing is connective tissue at both ends — the reader's own wrong answer at the front, an open question at the back — not more argument in the middle.

## 6. The last line

**"This is not our idea. It is the heart of Eliyahu Goldratt's Theory of Constraints, and the seven chapters after this one are what you can do with it once you believe it."**

Four separate problems in thirty-three words.

1. **It duplicates furniture the page already renders.** B1 ships a next-chapter card and a full chapter list (its lines 93–107). A printed trailer is a second, worse copy of both, immediately above them.
2. **"the seven chapters after this one"** is inventory management, not writing. It tells the reader about the product rather than the world, and it breaks the moment the chapter count changes — which, per the arc's own history, it already has once (16 → 8+5).
3. **"once you believe it"** concedes that the reader may not, at the exact point where the chapter should have finished convincing them, and makes the remaining series contingent on belief rather than on an open question. It is a hedge in the wrong direction: not honest calibration, just a loss of nerve.
4. **It ends on attribution.** A bibliography is the weakest available last beat. The chapter's last image should be the clinic.

Cut the whole sentence. End on the world: the doctor who is the constraint and who is not idle, or the man with the cough coming back next week. Either leaves A2's question hanging without printing a trailer, and the card underneath does the rest.

## 7. Is the Goldratt lineage placed well?

**Bolted on.** It is currently the last sentence of the chapter, fused to the trailer, which makes the lineage feel like a disclaimer rather than a credit. The voice guide (item 5) wants the lineage *named*, and the evaluation (01-evaluation §"Voice") wants it kept but placed where it is the subject rather than dropped into a story. The arc allots "one line of lineage" and does not fix its position.

The right place is directly under the bolded key claim. The claim is the thing being credited; put the credit against the thing. One sentence — *This is Eliyahu Goldratt's, from the Theory of Constraints* — stamps the claim, discharges the debt, and frees the ending. A1 need not name Dettmer; the arc gives him to A4, where the Logical Thinking Process is the subject, and that split is right.

## 8. Sentences doing no work

- **"She was busy absorbing the anger that something else was generating, which is what being next to a constraint usually looks like from the outside."** The brief names this as a prime suspect; it is half right. The first clause is the source's, and it is earned — it is concrete, it explains why every finger points at Maria, and it is the best image in the chapter. The *appended* clause is the flourish: an abstraction dropped on top of a picture, factually loose (§1, finding 3), and it introduces "from the outside" when the chapter has never established an inside. Cut from "which" and the sentence improves.
- **"Say what the clinic is for, plainly, because everything else depends on it"** — stage direction, and false about its own position. §4.
- **"and the seven chapters after this one are what you can do with it once you believe it"** — cut entirely. §6.
- **"whether it knows it or not"** — borrowed verbatim from the source, where it sits mid-piece and reads fine. As part of *the* bolded key claim of the opening chapter it wants to be maximally plain; stations do not know things, and the aside makes the reader parse a personification inside the one sentence they are meant to carry away. Weakest element of an otherwise excellent claim sentence. Consider "the one every other station ends up waiting on".
- **"Almost none knows where its own is."** The source's "Almost no system knows where its own is" is clearer; the compressed version reads clipped and momentarily ambiguous after "Every system has one".
- **"Here is why."** Removable with no loss. §5.

Not guilty, despite looking like flourishes: "visibly and unarguably" (pre-empts the obvious objection — it is doing work); "It is not an average or a target; it is arithmetic" (the only line that stops a reader thinking "yes, but on a good day"); "Multiply him" (two words, does more than a paragraph could).

## 9. Voice-guide checklist, box by box

- [~] **Could a reader who has never heard of LTP say, after this chapter, the one or two things it set out to say?** Half. They get "the slowest station sets the output". They do not get "busyness is the wrong signal", because the mechanism was cut with the "Everybody's busy" section. §2.
- [✗] **Is each concept stated plainly before (or as) it is illustrated?** No, inverted twice. The goal — the thing everything else depends on — arrives after the arithmetic that depended on it. "Four of those numbers do not matter" is asserted before the reader has any criterion for mattering. §4.
- [✗] **Any sentence whose job is to sound good rather than to say something?** Three: the "next to a constraint" coda, the "Say what the clinic is for" stage direction, and the chapter-count trailer. §8.
- [~] **"We" voice; lineage credited where a method is used; AI named where it is the enabler.** "We" appears exactly once, in "This is not our idea" — acceptable for a story chapter (B1 is also largely impersonal and uses "we" only in its disclosure), but it means the one "we" in the chapter is doing double duty as the lineage credit and then gets cut with the ending; make sure a "we" survives, in the disclosure line if nowhere else. Lineage credited but misplaced (§7). AI correctly absent — the arc gives that to Series B.
- [✓] **One bolded key claim at most per section.** Exactly one, and it is the right sentence, well positioned as the chapter's hinge. Do not touch this in revision beyond the "whether it knows it or not" question.
- [✗] **Every hedge honest, no overclaim, the opposing view stated fairly.** Two overclaims ("four of those numbers do not matter"; "which is what being next to a constraint usually looks like"). One honest and well-judged hedge ("something like ten thousand"). The opposing view — the genuine case for fixing the front desk — is never stated at all, which is also why the reversal does not land (§3). One hedge in the wrong direction ("once you believe it").
- [✓] **300–600 words.** 398. In range with about 150 words of headroom, which is roughly what the fixes below need.

## 10. What is working — protect this

Name it explicitly, because a revision that fixes §3 and §4 could easily flatten all of it.

1. **The opening two beats.** "A clinic opens at eight. By noon, sixty people are waiting." Eleven words, a place, a time, a problem, no manifesto. The 01-evaluation's first complaint about the 2R piece was that it opened on manifesto instead of story; A1 does not make that mistake for a second.
2. **"She is also irrelevant to how many people this clinic helps."** Standing alone as its own paragraph, this does the entire reversal on Maria in eleven words. It is the best-placed line in the draft.
3. **The cough paragraph.** One man, fully particular — sixties, March, three hours, four o'clock, a grandson — then "Multiply him", then ten thousand. Moving from one person to a policy-scale number in two sentences without losing the person is the hardest thing in this kind of writing, and it is done here. Change nothing in it.
4. **The absence of jargon.** The reader meets exactly one technical word, "constraint", and it is defined in the sentence that introduces it. No throughput, no bottleneck, no subordination, no five focusing steps. This is a real discipline and the whole series depends on it holding.
5. **"It is not an average or a target; it is arithmetic."** Closes the escape hatch before the reader finds it.
6. **The bolded claim itself**, and the decision to have exactly one.
7. **Fidelity.** Every fact that came from the source came across intact, including the small particulars that are easiest to lose in compression. The problems below are all *added* or *omitted* material, not corrupted material.

## Ranked fixes

1. **Kill "Four of those numbers do not matter."** It is false (the 40 caps A2's whole gain; the others determine where the constraint moves next) and A2's closing beat has to contradict it. Replace with a true and narrower version — that today only the smallest number is doing any work — which also seeds A2 instead of fighting it.
2. **State demand, or "the other forty" does not follow.** Add the clause that sixty people a day come through the door. Without it the draft derives forty turned-away from a processing *capacity*, and the ten-thousand figure inherits the gap.
3. **Move the goal up and make it a statement, not a stage direction.** Put it immediately after "She is also irrelevant to how many people this clinic helps", where it answers the question that line raises. Cut "Say what the clinic is for, plainly, because everything else depends on it". Give throughput its own short sentence — "The number that matters is how many patients come out the far end" — rather than burying it in a fifty-word clause-chain.
4. **Earn "they are all wrong."** Two moves, either or both: let the obvious diagnosis stand for one beat with the reader inside it before the verdict lands, and state the best case for the front desk fairly (what the hire there actually buys) before demolishing it. Keep the sentence "They are all wrong" — fix where it sits, not what it says.
5. **Rewrite the ending.** Cut "and the seven chapters after this one are what you can do with it once you believe it" — the page already renders a next-chapter card and a chapter list, and the count will change again. End on the clinic: the doctor who sets the number and is not idle, or the man with the cough coming back next week. Leave A2's question open rather than printing a trailer for it.
6. **Move Goldratt to sit directly under the bolded claim**, as one sentence crediting the claim. This is what frees the ending in fix 5. Leave Dettmer to A4.
7. **Restore the "busyness is the wrong signal" mechanism, in two sentences.** A non-constraint at full stretch manufactures work the constraint cannot absorb; universal busyness means nobody has found the constraint. Without this the second half of the key claim is an assertion the reader cannot regenerate, and the chapter's transferable idea does not transfer. Budget is available.
8. **Name Dr Adeyemi, in a clause, when the doctor's twenty first appears.** The arc makes her admin the question that carries all of Series A; A2 cannot ask it about a stranger. Alternatively drop her from the header's carried-facts block — but naming her is the better fix, and it removes the chapter's odd asymmetry where the non-constraint has a name, a phone and a window and the constraint is a box with a number on it.
9. **Cut "which is what being next to a constraint usually looks like from the outside."** Unsupported, geographically wrong (Maria is two stations upstream), and it smothers the chapter's best image under an abstraction.
10. **Add a composite disclosure**, one italic line in B1's style: the clinic is a composite and its numbers are illustrative, chosen so the arithmetic can be checked. A series about checking claims cannot open with unlabelled invented numbers.
11. **Break the capacity sentence into short sentences**, as the source has it. Sixty-one words and five numbers in one sentence is the paragraph a phone reader abandons.
12. **Small repairs.** "Almost none knows" → "Almost no system knows". Consider dropping "whether it knows it or not" from the bolded claim so the one sentence the reader carries is wholly plain. Name the clinic Ashfield if A2–A8 will refer back to it by name. Confirm the published form supplies the eyebrow and lede that B1 has.

Net effect on length: roughly 30 words cut, 90 added, landing near 460 — still inside the band and still shorter than B1.
