---
name: contribution-proposals
description: >
  Turn a batch of raw participant contributions — a Google Doc export, a form
  dump, a pasted text file of what a room wrote — into reviewable proposals for
  how each one might change an existing LTP model, and render them as a
  self-contained review page the group clicks through live, accepting,
  editing, or rejecting each proposal and watching the tree change on screen.
  Use this skill whenever contributions, comments, survey answers, workshop
  notes, or forum posts need to be read against an `ltp-model.yaml` and put in
  front of people for a decision. The target model is never modified: the skill
  produces a separate `proposals.yaml` and an HTML page, and only a human
  merges anything.
---

# Contribution proposals

A room writes. Each person offers something the model might be missing,
underestimating, or getting wrong. This skill reads those contributions against
an existing LTP model and, for each one, proposes a single address in the tree —
then renders the set as a page the group works through together.

The output is a **review package**, not an edit. `ltp-model.yaml` is read-only
here. Nothing in `proposals.yaml` has standing over the tree; accepting a
proposal changes the page's memory and nothing else. This is the same governance
rule as `../goal-alignment` and it exists for the same reason: the project's own
model names AI mappings that misrepresent a contribution (`NBR-2`) as a real
risk, and puts confirmation authority with contributors and reviewers
(`INJ-5`).

## Required operating principles

1. **The contribution is quoted verbatim.** Never tidy, correct spelling,
   expand contractions, reword, or stitch two separate passages together.
   Shorten only by taking a shorter *continuous run*. Their words are the one
   thing here that cannot be reconstructed if you lose them.
2. **Separate their claim from your reading of it.** `source.text` is theirs;
   `interpretation.statement` is yours, and the page labels it as the machine's
   words. If the reading had to assume something, say so in
   `interpretation.note`.
3. **One proposal per contribution.** Even when you can see six implications.
   The room needs *Participant 4 said this → the reader proposes that → decide*,
   not a menu of seven ontological readings. Record the runners-up under
   `alternatives`, which the page shows as a quiet line, never as a choice.
4. **`unplaced` is a successful result, not a failure.** If nothing in the model
   can hold a contribution without misfiling it, say so. A contribution that
   exposes a genuine gap may be the most valuable thing in the batch — and
   forcing it under the nearest-sounding node hides exactly what it revealed.
5. **Propose the address you can defend from the tree.** The `rationale` has to
   be checkable against the entities on screen by someone who has never seen
   this skill. "Both mention practice" is not a rationale.
6. **Confidence is calibrated, not polite.** `medium` and `low` are normal. A
   batch where everything is `high` has not been read carefully.
7. **Never modify the target model.** No edits, no "while I was in there". The
   build script re-reads the model on every run and records its hash.

## Inputs

| What | Where it usually comes from |
|------|------------------------------|
| Contributions | A text file the user downloaded — Google Doc export, form responses, pasted notes. Unstructured is expected. |
| Target model | `ltp/ltp-model.yaml`, or another model produced by `../project-ltp`. |
| Presentation details | Title, event, date, and how contributors should be credited. Ask if not given. |

## Workflow

### 1. Read the contributions and segment them

Open the file and work out where one contribution ends and the next begins.
Common shapes: blank-line-separated blocks, `---` rules, `Name: text` lines, a
form export with a timestamp column, one bullet per person. Say how many you
found before going further — a segmentation that silently merges two people is
worse than one that asks.

**Attribution.** Default to `Participant 1`, `Participant 2`, … numbered in
document order. Use real names only if the user confirms the room agreed to be
named on a slide. A public post is still not a slide; the deck's own pre-talk
checklist asks for consent first.

### 2. Read the target model

Load `ltp/ltp-model.yaml`. You need the `entities` (id, type, statement), the
`links` (id, from, to, relation), and the `views` map — a proposal is addressed
to a view, because the view is what the room will be looking at.

Note which relation dominates each view. In `goal-tree` every link is
`necessary_for`; in `current-reality` they vary.

### 3. For each contribution, choose one operation

| Operation | Use it when | Placement fields |
|-----------|-------------|------------------|
| `add_entity` | The contribution names something the model does not contain, which belongs under an existing node | `view`, `connects_to`, `relation` |
| `support_entity` | It backs an entity the model already has — testimony, an example, a case | `view`, `connects_to` |
| `challenge_entity` | It disputes a claim the model makes | `view`, `connects_to` |
| `challenge_link` | Both ends are fine; the arrow between them is what fails | `view`, `link` |
| `add_link` | Both entities exist; the model is missing a relation between them | `view`, `from`, `to`, `relation` |
| `unplaced` | No address exists that would not misfile it | `view` (for context only) |

**Direction matters for `add_entity`.** The new node always links *into* the
existing one: the created link is `new_entity --relation--> connects_to`. In a
goal tree that means the new node is a necessary condition *for* `connects_to`;
in a current-reality tree it means the new node *causes* `connects_to`. If the
contribution names a new *effect* rather than a new cause, it is usually a
`challenge_entity` on the effect the model already claims, or an `add_entity`
hung off something further down. Do not invert the link to make it fit.

Distinguishing `challenge_entity` from `challenge_link` is worth the extra
thought, and the page draws them differently. Ask: can the node be true and the
arrow still fail? If yes, it is the link.

### 4. Write `proposals.yaml`

Validate against `references/proposals.schema.json`. Ids are `PROP-001`
upward, in the order the room should see them. Every `review.status` is
`pending` — the file never records a decision.

Ordering is a presentation decision, not an alphabetical one. A good batch opens
with one the machine clearly got right, puts a genuinely contestable one in the
middle, and does not bury an `unplaced` at the end as an afterthought.

Use `>-` for the verbatim text and keep it on one unwrapped line, matching the
repo's no-line-wrap convention. If a contribution has real internal line breaks,
use `|-` instead so they survive.

See `examples/proposals.sample.yaml` for a worked batch of seven covering all
six operations, read against the real Second Renaissance model.

### 5. Build the page

```sh
python3 skills/contribution-proposals/scripts/build-demo.py \
  --model ltp/ltp-model.yaml \
  --proposals talk/2r-research-group/demo-c/proposals.yaml \
  --out talk/2r-research-group/demo-c/index.html
```

Those are the defaults, so a bare `python3
skills/contribution-proposals/scripts/build-demo.py` does the same thing. Add
`--check` to validate without writing.

The script refuses to build on a dangling reference — an entity id that is not
in the model, a link that is not in the named view, a missing placement field
for the chosen operation. Fix `proposals.yaml`; never fix the model.

The result is one self-contained HTML file with the model and the proposals
embedded. No server, no build step, no network at run time except Google Fonts.

### 6. Look at it before the room does

```sh
python3 -m http.server 8731
```

then open `http://localhost:8731/talk/2r-research-group/demo-c/index.html` and
click through every proposal. Opening the file directly with `file://` works
too. Check that each one lands on the node you meant, that the accepted state
persists as you advance, and that nothing overflows at the projector's
resolution.

To publish, follow the repo's preview-first rule in `AGENTS.md`: `fl . --yes`
to the preview site, look, then land on `main`.

## Driving it in the room

| Key | |
|-----|--|
| `→` / `space` | next proposal |
| `←` | previous |
| `A` | accept — or, on an `unplaced`, record it as a gap |
| `E` | edit the claim, its placement, or the relation |
| `X` | reject — the proposal stays visible, struck through, not deleted |
| `0` | reset everything to pending |
| `End` | jump to the tally |

`A` and `X` toggle, so a mis-press is one keystroke to undo. The header dots are
clickable and jump to any proposal.

Accepting turns a dashed node solid and it stays in the tree as you advance, so
by the last proposal the room is looking at the original tree plus everything it
agreed to. Refreshing the page throws all of that away, which is the honest
behaviour and worth saying out loud: the decisions live in the room, and merging
them into `ltp-model.yaml` is a separate, deliberate act afterwards.

`Edit` is deliberately narrow — the claim's wording, what it attaches to, and
the relation. Nothing else. Its best use is the case where the reader got the
idea right and the address wrong: correcting that in front of everyone is a
better demonstration than a machine that was right every time.

## What this skill does not do

- It does not merge anything into `ltp-model.yaml`, and it has no code that
  could.
- It is not a general LTP editor. No node dragging, no arbitrary graph editing,
  no property inspector.
- It does not persist decisions. There is no storage, no export of the room's
  verdicts. If you want them recorded, write them down.

`references/html-demo-spec.md` describes what the page draws and why, for
anyone changing the template.
