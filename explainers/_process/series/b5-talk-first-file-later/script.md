# Script — B5, *Talk first, file later*

Series B, chapter 5 of 5. Bead `reasoncommons-bnl.22`. Revised against [`critique.md`](critique.md); the draft is in [`draft.md`](draft.md). Prose only, no visual direction. 600 words.

**Read the source note before editing a word of this.** The chapter is an evidence claim, and the draft got two things wrong about what the evidence shows.

---

**Key claim:** AI reads the conversation afterwards and proposes where each point belongs; people decide what goes in.

---

What follows is a real run of the reader we built, on invented input: nine contributions written by a colleague as test material — fictional people, not a transcript of any session. The tree is the movement's real one; the readings are what came back.

They were asked what they would add, change, question or challenge in the movement's reasoning, so they were already aimed at the tree. That makes this the easier half of the problem: the reader has not been tried on a conversation that was not about the tree, which is the case this series argues for. What it does test is whether ordinary prose becomes a proposal at a specific address — none of the nine used the notation or named a node.

Take Maya's. She is sympathetic to the big civilizational goal but not sure it helps the group choose: "transform civilization", as she puts it, justifies almost anything, and she wants a nearer-term statement of success.

The reading came back as a challenge to the root claim: *the goal is too broad to discriminate between courses of action, so it cannot do the work a goal is supposed to do.* Not that the goal is wrong — that it cannot rule anything out. If that placement is accepted, the objection has an address and the next person can argue with it there.

A second reading came back at lower confidence: she might instead be proposing an intermediate goal under the root. The reader judged she offers it to show what is missing rather than as a proposal, and recorded the alternative rather than choosing silently between them.

Across the nine: four challenge a claim, one a link, two propose a missing condition, one names a cause the tree had no room for. Seven landed in the goal tree, two in the current-reality tree — "what should be true" and "why isn't it" are different questions with different addresses.

And one came back unplaced. Ana asked where art, celebration, grief ritual, shared meals and beauty fit — not practice exactly, not outreach exactly, but often what makes a culture worth belonging to. She named three possible answers herself; the third was that this points at something the tree does not represent, and the reader took that one. Its reason: the nearest address was the condition about durably embodying practices, and filing celebration and grief there would make them instrumental — close to the reading Ana was wary of. It recorded that placement as a live alternative anyway.

A contribution the tree cannot hold is not noise. It is the tree showing where it is thin.

**Nothing in that run went into the tree. The reader proposes; people decide what goes in.** (For a technical reader: a pull request, with the same right to say no.)

None of this is finished. The trees are provisional and wrong in places, the reader is a prototype, the rules for accepting anything are a draft, and nobody with standing over the tree has checked whether these nine readings are *right* — three of the nine the reader was only half sure of, by its own estimate of itself.

What has changed is the price of speaking. Maren writes her sentence the way she always would; the reading gets done without her; what is left is deciding, which lands on whoever keeps the tree — real work, and much less of it than before.

The trees are public and waiting. And if you want to watch a group work out what is actually in the way — the constraint, and why fixes don't stick — that is the other series.

---

## Source note for the build

**Two things the first draft got wrong. Do not reintroduce either.**

1. **The contributors are invented.** `talk/2r_participant_contributions_test.docx` is titled "Demo C test input · fictional participant data", and `proposals.yaml` says in its first lines that the nine are fictional and this is "rehearsal material, not the room's words". The draft opened with "Nine people contributed to a session", attached to a real event name and date in the YAML metadata. The label now leads the chapter, and says *invented*, not "rehearsal". Arc decision 3.
2. **They were prompted at the tree.** The docx prints the prompt: *"After looking at the current Second Renaissance reasoning, what would you add, change, question, or challenge? What feels missing or incorrectly assumed?"* They had seen the reasoning. This is a structured review round, not untargeted conversation, so it does not by itself demonstrate the series' own thesis — that the value is in catching what people say when they are *not* thinking about the tree. The script says so plainly in its second paragraph. **`DECK.md` line 121 calls these contributions "written independently of the tree", which the docx does not support; do not propagate that phrasing.** See the note on the open decision below.

Verified against `proposals.yaml` and `ltp/ltp-model.yaml`: Maya's paraphrase and her "transform civilization" quote (hers, not the tree's wording — G-1 reads "Co-initiate a conscious transformation toward a wiser, weller, regenerative civilization"); the italicised reading, near-verbatim from `interpretation.statement`; the alternative and why it ranked lower; 6 high / 3 medium; 4 challenge_entity, 1 challenge_link, 2 condition additions, 1 root cause (Marcus, under UDE-3 in the current-reality view), 1 unplaced; 7 goal-tree / 2 current-reality placements; Ana's three self-named options, the instrumentalising objection, and the recorded CSF-1 alternative; all nine `review.status: pending`.

Say "the reader" for the AI and "the tree" for the LTP model, never "the model" for both — the draft collided them and ended up saying the AI lacked the category, which is the opposite of the point.

`skills/contribution-proposals/VERIFICATION.md` states that nobody with standing over the tree has reviewed whether the readings are right. The honesty paragraph carries that; keep it.

**B4's constraint still binds:** do not turn "proposes a placement" into "files it", and do not drop the sentence about the deciding landing on whoever keeps the tree.

**Open decision for Rufus** (bead created): whether to run the reader on genuinely untargeted conversation — a real forum thread — before this series goes live, since B1–B4 argue for exactly the case Demo C does not cover. The script is honest about the gap either way.
