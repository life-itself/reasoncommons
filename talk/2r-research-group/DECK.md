---
title: The built deck — Where Does the Thinking Go?
status: built from slides-brief.md, ready to rehearse
built: 2026-09-03
---

# The deck

[`index.html`](./index.html) — one self-contained file. No build step, no
dependencies, no network at run time except Google Fonts (Cormorant Garamond

- DM Sans). Open it in a browser and press `F`.

Also published at <https://claude.ai/code/artifact/a679249a-36eb-49cd-8497-114d73f19021>
if the projector machine is easier to reach with a link than a file.

## Driving it

| Key                   |                                                      |
| --------------------- | ---------------------------------------------------- |
| `→` / `space` / click | next build step, then next slide                     |
| `←`                   | back one step                                        |
| `↑` `↓`               | whole slide, skipping its builds                     |
| `G`                   | overview grid — click any slide to jump              |
| `N`                   | presenter notes for the current slide                |
| `T`                   | start / pause the 4-minute write timer (Demo C only) |
| `F`                   | fullscreen                                           |
| `Home` `End`          | first / last slide                                   |

Click-anywhere advances, so a handheld remote that only sends a click works.

40 slides: 6 section dividers and 34 slides, in the exact order and with the
exact on-slide text of [`slides-brief.md`](./slides-brief.md). Nothing was
added to the argument and nothing reordered. Presenter notes carry the spoken
beats from [`script.md`](./script.md) plus staging and asset asks.

## What was filled in

Every `Visual:` and `Build:` line in the brief is now a real drawing. They are
drawn, not photographed, in the product's own visual grammar rather than a
deck style invented for the occasion. The normative sources all live in the
**`reason-commons` application repo**, not this one:
`src/features/essay/field/field.css` and `src/domain/graph.ts` define the
grammar, and `docs/product-redesign/DESIGN_RATIONALE.md` says why each rule
exists.

- **Four hues, one meaning each.** sage = held or observed · rust = going
  wrong or in the way · accent = only proposed, or newly connected ·
  structure = not reasoning at all (a forum, a model, a document). The brief
  asked for one accent reserved for one meaning; this is that, and it is the
  same one meaning it has in the app.
- **Four borders only**: a node, a dashed proposal, a commons boundary, a
  system boundary. Everything else separating is space and typography.
- **Six role families by glyph**, never by hue: ◎ outcome · ▲ trouble ·
  ↳ cause · ⇄ tension · ◆ move · ◉ evidence.
- **The legend is on every slide that uses the notation.** Not in a modal, not
  behind a `?`.
- **Arrivals condense** — blur to focus over five pixels. The two exceptions
  are the two the brief marks: the opening question evaporating, and the
  assumption breaking.
- **One field, 1200 × 600, that never changes shape.** The tree of change is
  drawn once and then transformed by each act — populated, glossed,
  challenged, read, counted — rather than as unrelated pictures.

## Demo B is built from the attached thread

Demo B is the pre-baked route: _Problems and Possible Responses Within Our
Influence_ (forum t/878, 20 posts, 26–31 Aug 2026), read against the tree.
Four placement cards, one of each type the brief asks for:

| Card               | Verbatim source                                                                                                                    | Target                                      |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| supports           | Asimong, post 7 — _"It's in the small tents that action is formulated, encouraged, and brought into reality."_                     | claim 4.2.1, under condition 4              |
| challenges a link  | Asimong, post 8 — _"what we need is mutual respect, with no expectation of coherence"_                                             | the link 6 → goal, and the assumption on it |
| challenges a claim | Robert Bunge, post 6 — _"there is no unified forum 'goal' that applies equally to each forum participant"_                         | the goal itself                             |
| nowhere to put it  | glennr86, post 19 — _"it's a long thread and admit I haven't read the whole thing (and not planning to), it's a bit overwhelming"_ | none — and that is the point                |

The assumption _shared action requires a shared worldview_ is introduced in
Demo A and **breaks on screen** when card 2 lands. It is the author's own
named assumption, from post 2 of the same thread.

Robert's challenge to the goal is drawn **standing, not struck through**, and
returns on the "Loaded words" slide in the close. A challenge that simply
stands is the honest drawing.

Every quoted span is verbatim and continuous — shortened only by taking a
shorter run, never reworded, never stitched across two of a poster's
paragraphs. Checked against the source PDF and against
`fixtures/talk/forum-thread-878.md` in the `reason-commons` repo, whose
`tests/unit/talk.test.ts` enforces the same rule on its own deck.

## Demo C has a review page

The room writes, and then the room's contributions get read against the tree in
front of everyone: [`demo-c/index.html`](./demo-c/index.html). One proposal per
contribution, each landing dashed at a real address in the Second Renaissance
model, with Accept / Edit / Reject. Accepted proposals turn solid and stay,
so by the last one the tree on screen is the original plus everything the room
agreed to. Refresh throws it all away, and saying that out loud is part of the
point — nothing on disk changes.

**Presenting it without having built it?** [`docs/demo-c.md`](../../docs/demo-c.md) is the runbook — the URL, the fallbacks, and what to do when a reading is wrong on the night. It lives at <https://reasoncommons.com/talk/2r-research-group/demo-c/index.html>, and the trailing `/index.html` is not optional.

It is generated, not hand-authored. Download the contributions, then run the
`contribution-proposals` skill (`skills/contribution-proposals/SKILL.md`), which
reads them against the tree and builds the page. Work in the test route first —
it stamps the page, serves it, and opens it, and it cannot touch the live one:

```sh
python3 skills/contribution-proposals/scripts/build-demo.py --proposals <file>.yaml --test --serve
```

Then promote it onto `demo-c/`, which is the route that ships:

```sh
python3 skills/contribution-proposals/scripts/build-demo.py --promote
```

What ships in the repo today is a **rehearsal build from
[`2r_participant_contributions_test.docx`](../2r_participant_contributions_test.docx)** —
nine fictional participants, written independently of the tree, which is the
case worth rehearsing. Four of the nine challenge a claim, one challenges a
link, three add one, and one has nowhere to go. Replace it with the real batch
on the day.

Two things to settle before you drive it. It **opens on a challenge to the goal
itself** — Maya on `G-1` being too broad to rule anything out — and if the room
accepts that, a challenge sits on the goal for the rest of the session. Moving
her later is a one-line edit. And it **closes on the contribution with nowhere
to go**, Ana on art, celebration and grief ritual, which is the same beat Demo B
ends on.

Keys: `→` `←` move · `A` accept · `E` edit · `X` reject · `0` reset · `End`
jumps to the tally. `A` and `X` toggle, so a mis-press costs one keystroke.

## Before the talk

1. **Consent.** Asimong, Robert Bunge and glennr86 are quoted on slides.
   Public posts, but a slide is not a forum. Ask.
2. **The reverse-view counts** (`3 4 2 5 2 6 1 0`) are the deck's own figures
   and carry a date on the slide. Replace them with the real count. A number
   that arrives without its origin is the failure mode this whole thing exists
   to refuse.
3. **Demo C kit** — the shared form, its short link, and its QR. The QR on the
   slide is a labelled placeholder; drop the real code into the `.qr` block.
   And rebuild the review page from the real contributions once they are in;
   the committed one is a rehearsal.
4. **Optional swap-ins**, all working type-only today: a real dense
   white-paper page behind the ring on "No address"; the Life Itself logotype
   on the final slide; the public URL for the trees.
5. **Demo A can go live** — screen-share the tool and make the same two
   clicks. The drawing is the fallback and reads better from the back of a
   large room.

## One departure from the brief, named

The brief asks for the least-supported condition to pulse **in the accent
colour**. Accent means one thing in this grammar — _proposed, or newly
connected_ — and a condition nobody is holding is neither. So the reverse view
marks it two ways instead: by **absence** (the other seven fill with accent
ticks and it does not, which is Arnheim's point that disequilibrium is
expressed by equilibrium) and by **rust**, which already means _a thing going
wrong or in the way_. The alarm's boundary is drawn in words and with a count,
per the review checklist's question 17.
