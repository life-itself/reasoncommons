# Second Renaissance explainer — process files

Two passes at this piece. The second replaced the first on 2026-08-16.

## Pass 2 — *Somewhere to Put It* (current, shipped)

Written from a blank page against
[`docs/plans/2026-08-16-second-renaissance-narrative.md`](../../../docs/plans/2026-08-16-second-renaissance-narrative.md)
([#9](https://github.com/life-itself/reasoncommons/issues/9)).

| | |
|---|---|
| `05-script.md` | stage 1, v1 |
| `06-critique.md` | the adversarial read of it |
| `07-script-v2.md` | stage 1, final |
| `08-visual-script.md` | stage 2 |
| built | [`../../second-renaissance/index.html`](../../second-renaissance/index.html) — live |

## Pass 1 — *Whose Map Is It* (superseded, kept)

A retelling of the June "define throughput" episode. Dropped because it assumed a
reader already inside the trees: it opens on an argument about a word, and a cold
Second Renaissance reader needs the case for the trees before they need a dispute
inside them. Nothing is wrong with it as writing — it is a different, more advanced
piece, and its material may yet become one (see `NEXT.md`).

| | |
|---|---|
| `01-script.md` | stage 1, v1 |
| `02-critique.md` | the adversarial read of it |
| `03-script-v2.md` | stage 1, final |
| `04-visual-script.md` | stage 2 |
| built | `whose-map-is-it.html` — the page exactly as it shipped, restored from `e45a2bb^` |

`whose-map-is-it.html` is the real thing and still works: open it from the
filesystem and it renders and scrolls. Its asset paths were repointed one level up
(`../../scroller.css`) to survive the move into `_process/`; nothing else changed.
It is **not published** — `_process/` is in `config.json` > `contentExclude` — so it
has no URL on reasoncommons.com. To give it one, copy it back out to
`explainers/<slug>/index.html` and restore the original single-`../` paths.

It contains condensed quotes from real forum posts by Robert and David, who have
**not** seen it. That is the reason to think before giving it a public URL.
