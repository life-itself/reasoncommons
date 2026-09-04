# The review page

What `templates/demo.html` draws, and why it draws it that way. Read this before
changing the template; the grammar is borrowed, not invented, and breaking it
breaks the talk it sits inside.

## Where the grammar comes from

`talk/2r-research-group/index.html` — the deck this page is presented alongside.
Its header comment is the normative statement; the short version:

- **Four hues, one meaning each.** sage = held or observed · rust = going wrong
  or in the way · accent = only proposed, or newly connected · structure = not
  reasoning at all.
- **Four borders are entitled to exist**: a node, a dashed proposal, a commons
  boundary, a system boundary. Everything else separating is space and
  typography.
- **Six role families by glyph, never by hue**: ◎ outcome · ▲ trouble · ↳ cause
  · ⇄ tension · ◆ move · ◉ evidence.
- **The legend is on the page**, always, not behind a `?`.
- **Arrival is condensation** — blur to focus over five pixels. Nothing slides,
  scales, bounces, or snaps.

**One deliberate departure.** In the deck a `move` or `tension` node is drawn in
accent. Here accent has to mean *proposed* and nothing else, so every existing
node is drawn quiet whatever its family, and only the node under discussion
takes its family hue. Dash, not hue, carries the proposal. If you reintroduce
accent for existing injections, the page starts lying about what is proposed.

## Layout

Two columns under a thin bar, with the legend along the bottom.

**Left — the contribution.** Their words at display size, verbatim, with the
contributor's name set large enough to read as a person rather than a footnote.
Then, under a label that says whose words they are, the reader's interpretation,
the operation, the address, the rationale, and the confidence. Controls sit at
the foot of the column and are sticky, so they are never below the fold on a
projector.

Length varies more than anything else about real contributions — one line to a
thousand characters — so the quote steps down through three sizes at 340 and 700
characters, and the longest tier scrolls within 38vh rather than pushing the
proposal off the screen.

**Right — the field.** The view named in the proposal's placement, drawn as an
indented outline rather than a node-and-edge graph. This follows the deck's own
drawing of the tree of change: *one rank, in a column; indentation is the parent
relation.* It costs no edge routing, never overlaps, survives any number of
nodes, and reads from the back of a room.

The outline runs **upward**: a view's links point child → parent
(`NC-2 necessary_for CSF-1`), so the roots are the entities with no outgoing
link — the goal in a goal tree, the terminal effects in a current-reality tree —
and each indented child is *`relation`* its parent. When every link in the view
carries the same relation, the label is suppressed on every node and stated once
in the header instead; when relations vary, each one is labelled. An entity
reachable by two paths is drawn where it is first reached and shown at half
strength on the repeat.

## The four states of a proposal

| State | Drawn as |
|-------|----------|
| pending | dashed, accent, amber wash, arriving by blur |
| accepted | solid, sage, settled — the dashed border becomes what the community holds |
| rejected | dashed, faint, struck through — kept, never deleted |
| edited | the amended wording and address, stamped *edited by the room* |

Decided proposals stay on screen as the room advances, so the tree accumulates:
by the last proposal the field is the original tree plus everything the room
agreed to, with the declines still legible beside it.

Three strengths, not two. The proposal and its target are the figure. **Every
ancestor of the target, up to the root of the view, stays at full strength** and
carries a faint band so the path reads as a path — a claim you cannot trace to
a goal is not a claim anyone can review, and a greyed-out goal makes the review
impossible. Everything else drops to 50%. Decided proposals are never dimmed;
they are the record of what the room did. The field also scrolls to show the
whole path from the root down to the node in play when it fits, and centres the
node when it does not.

## How each operation is drawn

- **`add_entity`** — a dashed card indented under `connects_to`, drawn *before*
  that node's existing children so it sits against its address rather than at
  the end of a long list. Its footer names the relation and the contributor.
  `connects_to` may be an earlier proposal rather than an entity, in which case
  the card nests under that proposal's card — so a contribution can extend a
  claim the room accepted a minute ago, and the nesting is drawn rather than
  asserted. The Edit dropdown offers those proposed claims as addresses too.
- **`support_entity` / `challenge_entity`** — a chip attached to the target card
  carrying the verbatim quote (clipped at 180 characters; the full text is on
  the left at size), the contributor, and the reader's one-line reading.
  Challenges are rust; supports are accent.
- **`challenge_link`** — the same chip, attached to the *child* end of the link,
  directly under the relation label it disputes. Both ends of the link stay
  intact, which is the whole point of the distinction.
- **`add_link`** — a chip on the `from` card naming the relation and the target.
- **`unplaced`** — no overlay at all. A bordered panel above the tree says *No
  confident address* and gives the reasoning; the whole view drops to context
  strength; the Accept button becomes **Record as a gap**, and accepted gaps
  collect in a strip under the tree.

## Test builds

`--test` writes the same page to `talk/2r-research-group/demo-c-test/` with
`meta.mode: "test"`, and the page then says so three ways: a rust **test build**
chip in the header bar, a `TEST · ` prefix on the browser tab, and a rust
hairline along the top edge of the app. Rust is the right hue for it — in this
grammar rust means *something going wrong or in the way*, and a test build on a
projector during the real session is exactly that.

The route is gitignored and listed in `config.json` > `contentExclude`, so a
half-read batch reaches neither a commit nor the published site. Flowershow
previews ignore `contentExclude`, so it does appear on a preview site; that is
usually wanted, but worth knowing before sending someone a preview link.

## State

All of it lives in one JavaScript object: the current index, a decision per
proposal, and an edit per proposal. There is no storage, no fetch, no
persistence. Refresh is the reset, and that is a design decision rather than a
missing feature — a page that quietly remembered the room's verdicts would be
claiming an authority it does not have.

## Constraints to keep

- Self-contained. The model and the proposals are embedded as JSON at build
  time. The only network request is Google Fonts, and the stack degrades to
  Georgia and system sans.
- No dependencies, no build step at run time, no server.
- Readable at 1280×800. Test there, not only on a laptop display.
- `prefers-reduced-motion` turns off the arrival animation.
