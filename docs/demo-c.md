---
title: Running Demo C — the contribution review
updated: 2026-09-04
---

# Running Demo C

Demo C is the participatory part of [the talk](../talk/2r-research-group/DECK.md). The room writes for four minutes, their contributions are read against the Second Renaissance tree, and the group works through them one at a time on screen — accept, edit, or reject — watching the tree change as it goes.

This page is the runbook. It assumes you are not the person who built it.

## The URL

> **https://reasoncommons.com/talk/2r-research-group/demo-c/index.html**

**Type `/index.html` on the end.** The folder form — `.../demo-c/` — returns 404. Bare folder URLs only resolve for markdown pages on this site, and this is a hand-built HTML page. If someone reports a blank page or a 404, this is almost always why.

Two other addresses that are *not* it:

| Address | |
|---|---|
| `.../demo-c-test/index.html` | **404 on purpose.** The test route is local-only — gitignored and in `contentExclude`. See [Step 3](#3-review-it-on-the-test-route). |
| `.../demo-c/` | 404 — missing `index.html`. |

The page is one self-contained file. Once it has loaded you can pull the network cable and it will still work; the only outbound request is Google Fonts, and it falls back to Georgia and the system sans without them.

### The build tells you as well

You do not have to remember any of this. Every build ends by printing where the page can be opened — the local file, the published address, and, when serving, the localhost one:

```
  wrote talk/2r-research-group/demo-c/index.html (71 KB, self-contained)

  open it now    file:///…/talk/2r-research-group/demo-c/index.html
  published at   https://reasoncommons.com/talk/2r-research-group/demo-c/index.html
                 once this is committed and merged to main (a minute or two).
                 Keep the /index.html — the bare folder URL 404s.
```

A test build prints the same thing the other way round, so there is no way to mistake one route for the other:

```
  TEST BUILD — stamped on the page, gitignored, not published

  open it now    file:///…/talk/2r-research-group/demo-c-test/index.html
  will NOT publish — https://reasoncommons.com/talk/2r-research-group/demo-c-test/index.html
                   returns 404 by design: the test route is gitignored
                   and excluded from the site. Use --promote when it is right.
```

## If nothing has changed, you are done

The URL above already carries a full nine-contribution rehearsal batch. **Open it, press `→`, and it works.** You do not need Python, this repo, or Claude Code to run the demo.

Everything below is only for the case where new contributions arrive and you want *those* on screen instead.

## Putting a new batch on screen

### 0. Once per machine

You need Python 3 with PyYAML, a clone of the repo, and — for the reading step — Claude Code with the skill wired in.

```sh
pip3 install pyyaml
git clone git@github.com:life-itself/reasoncommons.git
cd reasoncommons
```

`.claude/` is gitignored, so the skill symlink does not come with the clone. Add it:

```sh
mkdir -p .claude/skills
ln -s ../../skills/contribution-proposals .claude/skills/contribution-proposals
```

Restart Claude Code if the skill does not appear. Run everything below from the repository root.

### 1. Get the contributions into a file

Download whatever the room wrote. A Google Doc downloaded from the browser is a `.docx`; a Google Form's responses are a `.csv`. Both work, as do `.txt`, `.md` and `.tsv`. A `.pdf`, `.rtf` or `.odt` needs re-exporting first, or paste the text into a `.txt`.

Put it anywhere. `talk/` is a reasonable place.

### 2. Run the skill

In Claude Code:

```
/contribution-proposals talk/<your-file>.docx
```

It reads each contribution against `ltp/ltp-model.yaml` and proposes one address in the tree for each — a claim to add, a claim or a link to challenge, or an honest *nowhere to put this*. It writes `talk/2r-research-group/demo-c-test/proposals.yaml` and builds a page from it.

**It never edits the tree.** `ltp/ltp-model.yaml` is read-only to the whole pipeline. Accepting a proposal on the night changes the page's memory and nothing else.

### 3. Review it on the test route

The skill builds to a **test route** first, which is deliberately unpublishable: gitignored, listed in `config.json` > `contentExclude`, and stamped with a rust *test build* chip in its header, a `TEST · ` prefix on the browser tab, and a rust hairline along the top edge. You cannot project it by accident.

```sh
python3 skills/contribution-proposals/scripts/build-demo.py --test --serve
```

That serves the repo and opens the page. Click through every proposal and ask:

- Does each one land on the node it should?
- Would the contributor recognise the reading as what they meant?
- Does the accepted state persist as you advance?
- Does anything overflow at the projector's resolution? Test at the real one.

To fix a reading, edit `talk/2r-research-group/demo-c-test/proposals.yaml` and rebuild with `--test`, then reload the tab. Leave the server running between rebuilds.

You can also fix placements live during the demo with `E` — see below. That is often the better answer, because correcting the machine in front of the room is a stronger demonstration than a machine that was right every time.

### 4. Promote it

```sh
python3 skills/contribution-proposals/scripts/build-demo.py --promote
```

Copies the batch onto `talk/2r-research-group/demo-c/` and rebuilds it there without the stamp. That route is the one that publishes.

Check the title in `talk/2r-research-group/demo-c/proposals.yaml` before you ship. It says *rehearsal · test contributions* today, which is honest for fictional data and a lie for real contributions. Change it to something like `Demo C — the room's contributions` and rebuild.

### 5. Publish

```sh
python3 skills/contribution-proposals/scripts/build-demo.py --promote --publish
```

That does steps 4 and 5 together: promotes the batch, commits it, pushes straight to `main`, and then waits until the URL is actually serving *this* build before telling you it is live. It checks the served page against this build's own stamp, so a cached copy of the previous version cannot fool it.

```
  committed  Demo C: the room's contributions
  pushed     main (1 commit(s))
  waiting for the deploy…
  live after 47s (74,512 bytes)

  LIVE  https://reasoncommons.com/talk/2r-research-group/demo-c/index.html
```

`--message` sets the commit subject. `--dry-run` prints the plan and does nothing.

**This publishes with no review step.** It only stages `talk/2r-research-group/demo-c/`, so nothing else in your working tree goes out, and it refuses rather than guessing when the situation is not simple — on a branch rather than `main`, or when `main` has moved on the remote. If you would rather have review, commit and open a pull request in the ordinary way.

Publishing to the preview site instead is `fl . --yes`. Note the preview **ignores `contentExclude`**, so the test route shows up there even though it 404s in production. Do not send anyone a preview link and call it the demo.

## Driving it in the room

| Key | |
|-----|--|
| `→` / `space` | next proposal |
| `←` | previous |
| `A` | accept — or, on a *nowhere to put it*, record it as a gap |
| `E` | edit the claim, where it attaches, or the relation |
| `X` | reject — the proposal stays visible, struck through, not deleted |
| `0` | reset everything to pending |
| `End` | jump to the tally |

`A` and `X` toggle, so a mis-press costs one keystroke. The dots in the header are clickable and jump to any proposal.

Accepting turns a dashed node solid and it stays as you advance, so by the last proposal the room is looking at the original tree plus everything it agreed to.

**Refreshing throws all of it away.** That is deliberate, and worth saying out loud: the decisions live in the room, and merging them into the tree is a separate, deliberate act afterwards. It also means a stray refresh mid-demo costs you the session's accepts, so try not to.

## Reading the page

Left is the contribution, verbatim, with the contributor's name. Under it, clearly labelled as the machine's words, is the reading, the proposed address, why, and a confidence.

Right is the tree. The grammar is the deck's:

- **Solid** — reasoning the group already relies on.
- **Dashed, amber** — proposed, not yet relied upon. The whole grammar in one mark.
- **Rust** — a challenge, or something in the way.
- **Quiet grey** — the tree, not under discussion.

The path from whatever is under discussion up to the goal stays at full strength, so you can always see what a claim traces to. Everything else fades back.

## When it goes wrong

| | |
|---|---|
| Blank page or 404 | You dropped `/index.html`. See [The URL](#the-url). |
| `demo-c-test` is 404 | Correct. It is local-only and never publishes. |
| Merged but the URL is stale | Give it a minute, then hard-reload. Flowershow rebuilds on push. `--publish` waits for this and tells you when it has landed. |
| `--publish` says main has moved | Someone else pushed. `git pull --rebase origin main`, rebuild, publish again. It refuses instead of reconciling production for you. |
| `--publish` says you are not on main | You are on a branch, or in a git worktree, where main cannot be checked out. Publish from the primary checkout. |
| No internet in the room | Open the HTML file directly from a clone — `talk/2r-research-group/demo-c/index.html`. It is self-contained. **Download a copy before you travel.** |
| `PyYAML is required` | `pip3 install pyyaml` |
| Build refuses with a named error | It found a dangling reference — an id not in the model, a link not in the named view, a missing placement field. Fix `proposals.yaml`. Never fix the model to suit a proposal. |
| The skill is not offered in Claude Code | The symlink in [Step 0](#0-once-per-machine) is missing. It is gitignored, so a fresh clone never has it. |
| A reading is wrong on the night | Press `E` and correct it live, or `X` and move on. Both are fine, and both are better television than pretending. |

## Rules that must hold

1. **The tree is never edited by this.** No step here writes to `ltp/ltp-model.yaml`, and there is no code that could.
2. **Contributions are quoted verbatim.** Not tidied, not corrected, not stitched together. Shortened only by taking a shorter continuous run.
3. **The machine's reading is labelled as the machine's.** The page does this; do not describe it as the contributor's view.
4. **Nothing is merged.** Accepting on the night is the room's decision, not a change to the model. Recording those decisions afterwards is a separate, deliberate act by a person.
5. **Do not publish a batch nobody has reviewed.** The test route exists so this cannot happen by accident. Do not work around it.

## Deeper

- [`skills/contribution-proposals/SKILL.md`](../skills/contribution-proposals/SKILL.md) — how the reading is done, the six operations, and what makes a defensible placement.
- [`references/html-demo-spec.md`](../skills/contribution-proposals/references/html-demo-spec.md) — what the page draws and why, for anyone changing it.
- [`talk/2r-research-group/DECK.md`](../talk/2r-research-group/DECK.md) — the deck this sits inside.
