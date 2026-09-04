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
| Contributions | Whatever the room's tooling produced — a Google Docs or Word `.docx`, a form export, a pasted text file. Unstructured is expected. |
| Target model | `ltp/ltp-model.yaml`, or another model produced by `../project-ltp`. |
| Presentation details | Title, event, date, and how contributors should be credited. Ask if not given. |

## Workflow

### 1. Read the contributions and segment them

If the file is a `.docx` — which a Google Doc downloaded from the browser will
be — get the text out of it first:

```sh
python3 skills/contribution-proposals/scripts/read-contributions.py <file>.docx
```

It handles `.docx`, `.txt`, `.md`, `.csv` and `.tsv`, prints to stdout, and
takes `--out` to write a file. It extracts text and nothing else; everything
below is yours. A `.doc`, `.pdf` or `.odt` needs re-exporting as `.docx` first.

Then work out where one contribution ends and the next begins.
Common shapes: blank-line-separated blocks, `---` rules, `Name: text` lines, a
form export with a timestamp column, one bullet per person. Say how many you
found before going further — a segmentation that silently merges two people is
worse than one that asks.

**Attribution.** Use the name each person gave, spelled the way they spelled it.
A contribution read back to a room without its author stops feeling like
anyone's, and the argument this whole thing serves is that a merged proposal
keeps its author. Fall back to `Participant 1`, `Participant 2`, … only where
the batch genuinely arrived without names, or where someone asked not to be
named — and say which you did.

Consent is still a real question when contributions come from somewhere the
person did not expect to be quoted on a slide, a public forum thread being the
obvious case. A form the room filled in during the session, knowing it would be
read back, is not that case. Ask when it is unclear; do not silently anonymise a
room that wanted to be credited.

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

#### Contributions that do not look like they fit

Most of them will not, at first. People answer the question they heard, not the
one on the slide, and they answer it in their own vocabulary — a permaculture
cooperative, a mutual credit network, a carpentry apprenticeship, nine hundred
characters of hard-won experience that never once uses the word *condition*.
This is the normal case, not the awkward one, and reading it well is most of
what the skill is for.

Work in this order:

1. **Find the operative claim.** A long contribution is usually one claim plus
   the experience that earned it. Marta's cooperative is not the claim; *views
   follow changed lives rather than preceding them* is the claim, and the
   cooperative is her evidence for it. Say so in `interpretation.note` when you
   have had to separate the two.
2. **Ask what it says must be true, or is going wrong.** That question moves
   almost any contribution into the model's register without distorting it.
   "The currency people use decides what they can do with each other" becomes
   *taking part depends on unpaid time, so it is rationed to people whose hours
   are not already sold* — which is a cause, and the current-reality tree holds
   causes.
3. **Then look for the address.** The trees are broad: a goal about civilizational
   transformation, success factors about embodiment, learning, and
   transmissibility. Most claims about how people actually change have a
   defensible home under one of them.
4. **Check you have not smuggled in your own claim.** The test is whether the
   contributor would recognise `interpretation.statement` as what they meant.
   If it needs a premise they did not offer, you have written your own proposal
   and attributed it to them.

Two contributions can circle the same subject and belong in different places.
Ana Beatriz on participants' hours is a cause of an existing undesirable effect;
Sam on who funds the group has no address at all. Resolving that difference in
the `rationale` is worth more to the room than either placement on its own.

**Reserve `unplaced` for genuine absence, not for surprise.** A contribution
about soil, or money, or a trade you have never modelled is not thereby
unplaceable. It is unplaced only when you have done the three steps above and
the honest answer is that attaching it anywhere would hide what it revealed.

#### Building on a claim the room just accepted

For `add_entity`, `placement.connects_to` may name an **earlier `add_entity`
proposal** instead of an entity — `connects_to: PROP-003` — when a contribution
extends one already on the table rather than anything in the model. Kwame's
apprenticeship claim is a condition on Marta's, not on `CSF-1` directly, and
drawing it that way is more truthful than flattening both under the same parent.

Two rules. The reference must point **backwards**, to a proposal the room has
already seen, and to one in the same view. And put the pair adjacent in the
running order, so they are decided together — a child left hanging under a
rejected parent is legible but not a good moment on stage. Record the fallback
address under `alternatives` for exactly that case.

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

See `examples/proposals.sample.yaml` for a worked batch of nine covering all six
operations, read against the real Second Renaissance model — including two long
contributions that never use the model's vocabulary, one proposal that hangs off
another, and one honest `unplaced`.

### 5. Build it to the test route and look at it

**Always build to the test route first.** Whether the reading is any good is not
a thing you can tell from the YAML, and the live route is what gets published.

```sh
python3 skills/contribution-proposals/scripts/build-demo.py \
  --proposals <wherever you wrote it>.yaml --test --serve
```

That validates, writes `talk/2r-research-group/demo-c-test/`, keeps a copy of
the proposals there for the next round, serves the repo, and opens the page.
The test route is gitignored and in `config.json` > `contentExclude`, so a
half-read batch cannot reach a commit or the published site by accident, and the
page carries a rust **test build** stamp in its header, its browser tab, and a
hairline along its top edge — no one is going to project it thinking it is the
real one.

Add `--no-open` to skip the browser, `--port` to move off 8731. Leave the server
running and it picks up each rebuild on reload:

```sh
python3 skills/contribution-proposals/scripts/build-demo.py --test   # rebuild, then reload the tab
```

Then click through every proposal. Does each one land on the node you meant? Is
the interpretation something the contributor would recognise? Does the accepted
state persist as you advance? Does anything overflow at the projector's
resolution? Fix `talk/2r-research-group/demo-c-test/proposals.yaml` and rebuild.

`--check` validates and writes nothing. The script refuses to build on a
dangling reference — an entity id that is not in the model, a link that is not
in the named view, a missing placement field for the chosen operation, a chain
to a proposal that has not appeared yet. Fix `proposals.yaml`; never fix the
model.

### 6. Promote it when it is right

```sh
python3 skills/contribution-proposals/scripts/build-demo.py --promote
```

That copies the test batch onto `talk/2r-research-group/demo-c/` and rebuilds it
there without the stamp. That route is the one that ships.

The result is one self-contained HTML file with the model and the proposals
embedded. No server, no build step, no network at run time except Google Fonts.

To publish, follow the repo's preview-first rule in `AGENTS.md`: `fl . --yes`
to the preview site, look, then land on `main`. Note that Flowershow previews
ignore `contentExclude`, so the test route *will* show up on a preview site and
will not show up in production — which is usually what you want, but is worth
knowing before you send anyone a preview link.

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
