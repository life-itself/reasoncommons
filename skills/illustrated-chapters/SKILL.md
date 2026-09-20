---
name: illustrated-chapters
description: The explainers-v2 chapter form — short Markdown pages on Flowershow with a static text column, SVG illustrations between the paragraphs, looping CSS animations where something changes over time, and a next-chapter card that chains the series. Use when building or editing any chapter or series index under `explainers/`, or whenever asked for an "illustrated chapter", a "Co-Star style" page, or the series index for one. For the retired scroll-driven form see `scrollable-explainer/`.
---

# Illustrated chapters — the form

The form the explainers were rebuilt into on 2026-09-20. It replaces the long scroll-driven pieces, which readers reported as not working: fragile on mobile, stale shared assets, pinned graphics fighting the prose, and five or six ideas per page. See [`docs/plans/2026-09-18-explainers-v2.md`](../../docs/plans/2026-09-18-explainers-v2.md) for the diagnosis and the decisions, and [`explainers/_process/series/costar-teardown.md`](../../explainers/_process/series/costar-teardown.md) for the reference model.

> **One idea, ~300–600 words, a static text column, drawings between the paragraphs, and a card at the foot that sells the next chapter.** No scroll-driven logic anywhere.

**Worked example:** [`explainers/_process/series/form-prototype/`](../../explainers/_process/series/form-prototype/) — three chapters and a series index, with both kinds of looping illustration. Its prose is scaffolding, not an approved script; take the markup from it, not the words.

---

## 1 · What a chapter is

One point, or at most two. If you cannot write the chapter's teaser — one sentence that *is* its key claim — the chapter is not focused enough to build. The teaser then appears in four places, identical every time: the page's `description` front matter, the `.ch-lede` under the title, the next-chapter card of the chapter before it, and the series index. That repetition is what makes the series read as a chain.

Order of work, and it is not negotiable: **script first, judged as writing, before any visual direction exists.** Stage discipline from [`scrollable-explainer/SKILL.md`](../scrollable-explainer/SKILL.md) §1.5 still applies — draft, an independent adversarial critique, then revise against [`voice-guide.md`](../../explainers/_process/series/voice-guide.md). The script files live in `explainers/_process/series/<nn>-<slug>/` and contain no figure specs. Illustration notes belong to the build.

## 2 · Layout on disk

Each chapter is a folder with an `index.md`, so relative links can be plain folder URLs — the pattern that is known to resolve on Flowershow:

```
explainers/<series-slug>/
  index.md                          the series index
  01-<slug>/index.md                chapter 1
  02-<slug>/index.md
```

Links: `../02-nowhere-to-put-it/` between chapters, `../` up to the index. Do **not** link a bare folder and hope; and do not use `<nn>-<slug>/index.html`, which is the old scrolling form's URL shape.

Everything is Markdown so it stays editable in a browser. `custom.css` at the repo root carries every `.ch-*` component, so a chapter's own markup is small.

## 3 · The page skeleton

```markdown
---
title: Nowhere to put it
description: <the teaser — one sentence, the chapter's key claim>
date: 2026-09-20
---

<p class="ch-eyebrow"><a href="../">Series title</a> · Chapter 2 of 5</p>

<p class="ch-lede">The teaser again, verbatim.</p>

Two or three short paragraphs.

<figure class="ch-fig">
<svg viewBox="0 0 440 260" role="img" aria-label="…what a person who cannot see it would need told…">
  …
</svg>
<figcaption>A SMALL-CAPS LABEL, NOT A SENTENCE</figcaption>
</figure>

More paragraphs. **One bolded key claim per chapter, no more.**

<a class="ch-next" href="../03-give-every-claim-an-address/">
<span class="ch-next-label">Next chapter</span>
<span class="ch-next-title" data-n="3">Give every claim an address</span>
<span class="ch-next-teaser">That chapter's teaser, verbatim.</span>
</a>

### All chapters

<ol class="ch-toc">
<li><a href="../01-same-conversation/"><span class="ch-toc-title">…</span><span class="ch-toc-teaser">…</span></a></li>
<li class="is-current"><span class="ch-toc-body"><span class="ch-toc-title">…</span><span class="ch-toc-teaser">…</span></span></li>
<li class="is-todo"><span class="ch-toc-body"><span class="ch-toc-title">…</span><span class="ch-toc-teaser">Not built yet.</span></span></li>
</ol>
```

Rules the markup depends on:

- **Never put a blank line inside a raw HTML block.** A blank line ends the block for the Markdown parser, and the indented SVG that follows parses as a code block and renders as literal markup — on a page that still returns 200, so it is only visible if you look. This is the single most common way to break one of these pages (AGENTS.md > Conventions).
- The `<li>` content must be exactly one flex child. A linked row wraps in `<a>`; an un-linked row (the current chapter, or one not built yet) wraps in `<span class="ch-toc-body">`. Forget it and the title and teaser sit side by side.
- The numbers in `.ch-toc` come from a CSS counter — never write them in the markup, or they will drift when a chapter is inserted.
- `data-n` on `.ch-next-title` prints the next chapter's number; the arrow is added by CSS.
- **SVG `id`s are page-global.** Two figures on one page that both define `<marker id="ch-arrow">` silently share the first one. Prefix every `id` with the figure — `tree-arrow`, `thread-window` — and check before adding a second figure that uses `defs`.

The series index is the same list one size up — `<ol class="ch-toc ch-toc-lg">` — under the series title, a `.ch-lede`, and ~150 words on who it is for and what they will be able to say afterwards.

## 4 · Illustrations

**Draw them for the page, as standalone inline SVG.** Do not capture stills from a scrolling version: they carry that form's layout — wide empty panels, captions far from the marks they name — and read as leftovers. `explainers/second-renaissance-plain/img/the-stack-v2.svg` showed redrawing is cheap.

The prose names what to look at; the drawing does the explaining. Put labels on the marks, not in a key.

**Palette.** Paper ground (never white), near-black ink, one mid grey, and terracotta reserved for *the thing at issue* — the constraint, the contested claim, the new node. Spend the accent on nothing else; it is what lets the eye find the point before reading a word. The tokens are on `:root` in `custom.css`: `--ch-paper #efe9dd`, `--ch-ink #31302d`, `--ch-grey #92908b`, `--ch-rule #d8d0bf`, `--ch-mark #c25c34`. `.ch-fig` always draws on paper, in light mode and dark, because a drawing in fixed ink has to read the same in both.

**Size the type off the phone, not the desktop.** In a `viewBox` 440 units wide, the figure is about 343 CSS px on a 375 px phone, so a user unit is 0.78 px. Anything below 14 units is unreadable there. Use **≥14 for labels that are read as words, ≥12 for tracked small-caps labels**, and if the text no longer fits, show fewer things — two conditions and "AND SIX MORE, NOT SHOWN" beats eight boxes nobody can read. Keep the whole drawing inside the viewBox: a label running past the right edge is the defect this form produces most often.

**Animate only what changes over time** — a thread greying, work flowing through a system, a tree growing. Structures stay still. About three or four animations across a whole series, not one per chapter.

## 5 · How the looping illustrations work

CSS animations declared in `custom.css`, never SMIL and never JavaScript, and never bound to scroll.

```css
@media (prefers-reduced-motion: no-preference) {
  .ch-anim-tree .g-root   { animation: ch-g-root   12s ease-in-out infinite; }
  .ch-anim-tree .g-level1 { animation: ch-g-level1 12s ease-in-out infinite; }
}
```

Four rules make them behave:

1. **CSS, so `prefers-reduced-motion` is honoured.** SMIL cannot be switched off by a media query; CSS can. With motion reduced, no rule applies at all.
2. **Author the SVG in the state worth seeing when nothing animates** — the complete figure, or the frame that carries the point. Elements that must start hidden get `opacity="0"` as an attribute and are revealed by the loop; everything else is authored in its final state.
3. **Every animation in one figure shares a duration and uses no delay.** Stagger by moving the keyframe percentages, not by `animation-delay`: on an infinite animation a delay phase-shifts the whole loop, so the beats drift apart instead of playing in sequence.
4. **Animate only `opacity`, `transform`, `fill` and `stroke`.** They are cheap, and they work on an SVG `<g>` without `transform-box` fuss — a CSS `translateY(74px)` on a `<g>` moves it 74 *user units*.

Leave a third of the loop holding the finished frame, so a reader who looks up sees the point rather than a fragment.

## 6 · Checking it

There is no preview site in a cloud session (`fl` is not available). Two scripts stand in:

```sh
NODE_PATH=<scratch>/node_modules node scripts/render-preview.mjs <page.md> out.html   # page → standalone HTML
node scripts/phone-check.mjs file://…/out.html shot.png 375                            # 375px, lists overflow
node scripts/phone-check.mjs file://…/out.html wide.png 1280
```

`render-preview.mjs` is an approximation of the theme, not the theme (it needs `marked` on `NODE_PATH`). It is enough for the things that actually break: escaped markup, overflow, and a component that doesn't look like it was meant to. **Look at the screenshot** — the overflow list catches labels leaving the viewport but not a caption sitting on top of the thing it names.

Then check the escaped-markup trap explicitly; it should come back empty:

```sh
grep -c '&lt;svg\|&lt;rect\|&lt;span' out.html
```

**Headless screenshots do not capture CSS animation state** — every frame comes back byte-identical, which looks like a broken animation and isn't. To verify a loop, sample the computed style instead: on a fresh page load set `animationPlayState: 'paused'` and `animationDelay: -duration × fraction` on each animated element, wait two `requestAnimationFrame`s, then read back `opacity`, `transform` and `stroke`. Four fractions across the loop show whether the beats land where the keyframes say.

Rufus reviews on a real preview (`fl . --yes`) before anything merges to `main`.

## 7 · Checklist before closing a build

- [ ] Teaser identical in the front matter, the `.ch-lede`, the previous chapter's next-card, and the series index.
- [ ] One bolded key claim in the chapter, at most.
- [ ] 300–600 words.
- [ ] No blank line inside any raw HTML block; the rendered page has no escaped markup.
- [ ] No overflow at 375 px and at 1280 px, and the screenshots looked right at both.
- [ ] Every label inside its viewBox, and no smaller than 14 units (12 for small caps).
- [ ] Terracotta used only for the thing at issue.
- [ ] Every `<svg>` has a `role="img"` and an `aria-label` that says what it shows.
- [ ] Animations loop without JavaScript, honour reduced motion, and hold the finished frame.
- [ ] Next-chapter card and all-chapters list present, with the current row marked `is-current`.
