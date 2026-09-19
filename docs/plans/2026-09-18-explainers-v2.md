---
created: 2026-09-18
status: active
owner: Rufus
---

# Plan — Explainers v2: short illustrated chapters

The current explainers are five long (2,000+ word) scroll-driven pieces. Several readers have said they don't really work. This plan replaces them with short chapters in the manner of [Co-Star's astrology 101](https://www.costarastrology.com/how-does-astrology-work): static text, illustrations (still or looping) between paragraphs, one or two points per chapter, chapters linked into a series.

State lives in **beads** (`bd list --label explainers-v2`), not in this file. This file says what the work is and why it is in this order. Scheduled sessions execute it (see [Runner](#runner)).

## Diagnosis

- **Form.** Scroll-driven drawings are fragile (mobile collisions, stale assets, pinned graphics fighting the text) and ask a lot of the reader. Readers report them as not functional.
- **Length.** Each piece carries five or six ideas. Co-Star chapters carry one, at ~300 words, and the series carries the rest.
- **Scripts.** The prose is in a literary, aphoristic register ("people leave rooms", "run without any of its vocabulary"). When Rufus rewrote the 2R talk script by hand on 2026-09-04 he consistently pulled the other way: plainer, "we", explicit, lineage named, AI named as the enabler. See [`voice-guide.md`](../../explainers/_process/series/voice-guide.md).
- **Story.** It is not yet settled what arc the illustrated introduction should follow — how closely to follow the book (Dettmer, *The Logical Thinking Process*, in `library/`), and how the Second Renaissance case relates to the LTP basics. This is the decision the whole series rests on, so it is the one human gate.

## Decisions

| Decision | Choice |
|---|---|
| Form | Short chapters, Markdown pages on Flowershow (editable in the browser), static text column, SVG illustrations inline or as `<img>`; some illustrations loop (SMIL/CSS animated SVG). **No scroll-driven logic.** Each chapter ends with a next-chapter card and an all-chapters list; the series index is a numbered list of one-line teasers. |
| Chapter size | One or two points; roughly 300–600 words. |
| Voice | [`voice-guide.md`](../../explainers/_process/series/voice-guide.md), derived from Rufus's talk rewrite. Every script is checked against it. |
| Focus | Two things: the LTP basics (following the book more closely) and the Second Renaissance story. The other trilogy pieces are source material, not targets. |
| Order | Finish the simple 2R piece → evaluate → settle the arc → scripts → form → build chapters → retire the long pieces. Don't do everything at once. |
| Old pieces | Retire: move to `explainers/_archive/`, exclude from the site, redirect their URLs if Flowershow supports it. Not many readers yet, so URL stability doesn't matter. |
| Autonomy | Sessions work directly on `main` in this checkout (nobody else is working here), check on the preview site (`fl . --yes`) before pushing. One gate: Rufus approves the arc. Everything else proceeds and is reviewed after. |
| Scheduler | Local launchd job every 5.5h running `claude -p --model opus`. Each session works through ready beads until none are left, then exits. |

## Phases

The beads issues carry the detail and acceptance criteria. In order:

1. **Finish the simple 2R piece** (`explainers/second-renaissance-plain/`) — voice pass, fold in what the talk (`talk/2r-research-group/script.md`) worked out since, fix the figure defects (#17), make it the lead 2R piece on the index.
2. **Evaluate** — a short note on what the finished piece teaches about length, form and voice, and what should carry into the series.
3. **Chapter form** — template, next/all-chapters nav, series index, one animated illustration as proof. Prototyped on a section of the 2R piece. Runs in parallel with the arc.
4. **Arc** — the overall story of the illustrated introduction: reader, takeaways, chapter list with the one or two points each makes, mapping to the book, what is kept or dropped from the current pieces, how 2R relates. Independent critique, revision, then **Rufus approves (gate)**.
5. **Decompose** — once the arc is approved, one script bead and one build bead per chapter.
6. **Scripts** — per chapter: draft → independent critique → revise, against the voice guide. Stage discipline from `skills/scrollable-explainer/SKILL.md` §1.5 still applies: script judged as writing before any visual work.
7. **Build chapters** — per chapter: illustrations and page, checked on the preview at desktop and phone width.
8. **Retire the long pieces and close out** — archive, redirects, index and nav, changelog entry.

## Runner

`scripts/explainer-loop/run.sh`, fired by `~/Library/LaunchAgents/com.lifeitself.reasoncommons-explainers.plist` (source copy in `scripts/explainer-loop/`) every 19,800 s.

- Exits at once, without starting Claude, if nothing is ready (`bd ready --label explainers-v2 --exclude-label human`) — so it idles cheaply while the arc waits on Rufus.
- Refuses to run if the working tree is dirty or another session holds the lock.
- Runs `claude -p --model opus --dangerously-skip-permissions` with [`session-prompt.md`](../../scripts/explainer-loop/session-prompt.md).
- Unloads itself when the epic is closed.
- Authenticates with a long-lived token from `claude setup-token`, read from `~/.config/reasoncommons-explainers/oauth-token` (mode 600, outside the repo). The interactive login can't be refreshed from launchd: on 2026-09-19 the first three runs all failed with "OAuth session expired and could not be refreshed". Auth failures and other non-zero exits raise a macOS notification.
- Log: `~/Library/Logs/reasoncommons-explainers.log`. Only runs while the Mac is awake; a missed interval fires once on wake.

Controls:

```sh
launchctl kickstart gui/$(id -u)/com.lifeitself.reasoncommons-explainers   # run now
launchctl bootout gui/$(id -u)/com.lifeitself.reasoncommons-explainers     # stop
bd ready --label explainers-v2                                              # what's next
bd list --label human --status open                                         # waiting on Rufus
```
