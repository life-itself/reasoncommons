---
name: scrollable-explainer
description: Principles and patterns for writing and building long-form scroll-driven visual explainers (scrollytelling) — the ProPublica/NYT article form where prose and graphics interleave and scroll position drives the graphics. Use when drafting, structuring, critiquing or building any explainer in `explainers/`, or whenever asked for a "scrollable article", "scrollytelling piece", "visual explainer" or "NYT-style scrolling article".
---

# Scrollable explainers — principles & patterns

A reusable reference for building long-form scroll-driven explainers. Written from a
direct browser teardown of the best current example of the form, but the patterns below
are meant to be **adapted, not copied**. Section 6 is about how to depart from them.

**Worked case study:** [ProPublica — *Why Carbon Capture Can't Solve Climate Change*](case-study-propublica-ccs.md)
— full teardown with scroll map, verbatim text in order, implementation details and
screenshots (`reference/`). Every pattern below is evidenced there. Read that file when you
want the detail; read this one when you want the rules.

Add further teardowns as `case-study-<slug>.md` as we find pieces worth learning from.

---

## 1 · What the form is

Generically: **scrollytelling**. Publishers call individual pieces *projects* (ProPublica),
*visual stories* (NYT, Reuters), *visual essays* (The Pudding).

The useful definition is behavioural, not visual:

> **An illustrated world the reader scrolls through, with sentences placed inside it.**
> The drawing carries the explanation; the text labels, paces and lands the numbers.

Two things it is emphatically **not**:

- **Not a long article with pictures.** In an article, prose carries the argument and images decorate. Here it inverts.
- **Not an interactive infographic.** Nothing to click, drag, hover or toggle. Scroll is the only input.

**The diagnostic test:** delete the graphics. If the argument survives intact, you've
written an article, not an explainer. In this form the drawing carries steps the prose
deliberately never states.

---

## 1.5 · The three stages — do not collapse them

**Build in three separate, separately-committed stages.** The failure mode this prevents is
real and easy to fall into: if you write text and visual direction together, the script is
never judged as writing. Weak prose gets carried into production because it was never
looked at on its own.

Stage files live in `explainers/_process/<piece>/`, never beside the finished
article — only `index.md` (the article) and `scrolling.html` sit in the piece's
own folder. See AGENTS.md > Conventions for the layout.

| Stage | File | What it is | Gate |
|---|---|---|---|
| **1 · Script** | `_process/<piece>/01-script.md` → `03-script-v2.md` | Pure narrative. **No figure slots, no block numbers, no visual direction of any kind.** | Must survive a hard editorial critique before anything else starts |
| **2 · Visual script** | `_process/<piece>/04-visual-script.md` | The approved script, unchanged, with visuals annotated against it | Reviewed before a line of code |
| **3 · Build** | `<piece>/index.md` + `<piece>/scrolling.html` | Implementation | — |

Building the Markdown article: **never leave a blank line inside a `<figure>` or
`<svg>` block** — it silently turns the rest of the figure into a code block on
the published page. AGENTS.md > Conventions has the full explanation and the
check to run afterwards.

### Stage 1 is the one that matters

Write it as prose that stands alone. Read it aloud; if a sentence is hard to say, it is
wrong. Then — and this step is not optional — **critique it as a world-class non-fiction
editor would**, in a separate file (`_process/<piece>/02-critique.md`), and revise.

The critique must be adversarial or it is worthless. Ask specifically:

- **Where are the stakes?** Who is harmed, by how much, and does the reader meet them? An explanation with no one in it is a maths problem with a roof on.
- **Is there a person?** Named, specific, present.
- **Does the title match the spine**, or a section you liked?
- **Which paragraphs tell the reader what to conclude** instead of letting them conclude it?
- **Where does it enumerate rather than argue?** Three examples in a row is a list; lists kill momentum. Two read as a pattern.
- **Are the concepts named** — will the reader finish with a *word* they can use, or only a feeling?
- **How many signposts** ("Now the question is…", "Back to the…", "You may have noticed…")? Each costs a screen. Cut most; let the hard cut do the work.
- **Is the ending an ending**, or a trailer for the next piece?
- **What is working** — name it explicitly, so revision doesn't destroy it.

Finish the critique with a **ranked** fix list. Then write v2 against it.

### Stage 2 only begins once the script is approved

Do not adjust the prose to suit a drawing. If a visual won't fit the script, that is
information about the visual. The script's job is done.

---

## 2 · The patterns

Nine named patterns. Use them as a vocabulary — "this section needs a Comparison Ladder",
"give that a Pinned Stage."

### 2.1 · Cold Open

**What it is:** the piece opens with three to five short sentences — one per screen, over a
graphic that's already moving — and **the headline does not appear until after them.** In
the case study the H1 arrives 4,000px down the page. The reader has scrolled through four
sentences before the article has even told them its name.

**Why bother.** A normal article opens headline-first: *"Why Carbon Capture Can't Solve
Climate Change."* That tells you the conclusion in the first second, so the rest is just
supporting material for something you've already been handed. The Cold Open withholds the
conclusion and walks you into it instead:

> Global leaders are banking on tech advances to solve climate change.  ← *screen 1*
> One leading idea is to capture carbon pollution from the air and then bury it underground forever.  ← *screen 2*
> It may sound practical.  ← *screen 3*
> **There is no conceivable way it can work.**  ← *screen 4*

Forty words. The first three sentences describe the idea **attractively and in good faith** —
this is the crucial bit; it is not strawmanned, and by sentence three you're nodding along.
Then sentence four breaks it flatly.

**The mechanism is pacing, not cleverness.** You physically cannot see sentence four while
you're reading sentence three, because it's a screen away. The scroll does the withholding.

**Why this matters for us specifically:** it is prediction-and-violation — set up the
reader's expectation, then break it — achieved with **zero interaction**. No button, no
"guess before you scroll" prompt, no quiz. If you were planning to make the reader click to
commit to an answer before revealing it, this is the cheaper, more reliable way to get the
same effect.

**Doing it badly:** opening with three sentences of context that nobody would disagree with
and no reversal at the end. If sentence four isn't a genuine turn, you've just written a
slow headline.

### 2.2 · The Pinned Stage
The structural workhorse. A tall container holds a viewport-height child that sticks while
the container scrolls past. Text steps fade in and out over the pinned graphic.

**The container's height is the pacing dial** — it decides how long a graphic holds the
screen. In the case study these ranged **1,700px (~2 screens) to 4,240px (~4.7 screens)**.

### 2.3 · One Screen, One Sentence
In the body stretches, roughly **900px of scroll between text blocks** — a full screen of
drawing per sentence. If a sentence needs a second sentence to be understood, it is two
screens, not a paragraph.

### 2.4 · Scroll-as-Scale
**Make the scroll distance itself be the quantity.** The case study draws a pipeline that
snakes down through screen after screen while three lines land: *"more than double the
distance to fly around the earth" → "longer than the country's entire interstate highway
system" → "hundreds of thousands of miles."* You feel the length because you had to scroll
it. The graphic isn't illustrating the number — the scroll **is** the number.

This is the single most transferable technique in the form and the hardest to fake. Reach
for it whenever a quantity is meant to feel excessive.

### 2.5 · The Comparison Ladder
Never leave a large number as a number. Convert it, repeatedly, into something bodily,
each rung on its own screen:

> 6 billion tons → an area the size of Mexico → 68,000 miles of pipeline → *"a brand new geological waste site somewhere on the planet every four days for the next 25 years."*

The last rung converts a quantity into a **cadence** — a rate you can picture happening.

### 2.6 · The Bare Number Block
Numbers get their own text blocks, two or three words long, with a small caption beneath.
The case study's cost comparison is three such blocks — `$500 billion` / `$340 billion` /
`$50 billion`, each captioned. The juxtaposition argues; the prose doesn't have to.

### 2.7 · The Nut-Graph Island
Exactly one region of ordinary paragraph density — three or four paragraphs of 25–45 words,
early, right after the title card. It says what was found and why it matters. Then the
piece never returns to that density until the sources.

### 2.8 · The Frame Sequence
How the animation is actually done: **pre-rendered image frames swapped on scroll.** No
canvas, no video, no WebGL. An `<img>` whose `src` steps through a numbered sequence, over
a shared texture background reused across every stage. Cheap, robust, degrades gracefully,
works on any device.

### 2.9 · Abrupt Stop, Then Receipts
End the body on a short flat line — the case study's is six words, *"Carbon capture and
storage remains elusive."* No summary, no call to action, no flourish. Then hand off to
several hundred words of dense, plainly-set **Notes on Data Sources**. The transparency is
the ending; it does more for credibility than a peroration would.

---

## 3 · The measured baseline

Numbers to calibrate against — not targets to hit exactly. Measured from the case study;
[full figures there](case-studies/propublica-carbon-capture.md#1--the-vital-statistics).

| | |
|---|---|
| Body prose | **≈1,100 words** (+ ~700 of sources) |
| **Median words per text block** | **16** |
| Longest blocks | 39–45 words — nut graphs only |
| Page height | **~40 viewports** |
| Scroll between text blocks | **≈900px — one screen** |
| Pinned stages | **7** |
| `<canvas>` / `<video>` / interactions | **0 / 0 / 0** |

**The ratio that should reset your instincts:** ~1 word per 16px of scroll. A normal
article runs ~1 word per 1.5px. This form gives **ten times more visual space per word.**

---

## 4 · Build mechanics

### The DOM skeleton

```html
<div class="scroll-item">          <!-- tall; height = how long the graphic holds -->
  <div class="sticky-item">        <!-- position: sticky; top: 0; height: 100vh -->
    <div class="sticky-item-container">
      <div class="sticky-item-bg"><img src="paper-texture.jpg"></div>
      <img id="sequence">          <!-- frame swapped on scroll -->
      <svg><!-- charts drawn here --></svg>
      <div class="step-content" id="step-1"><p>…16 words…</p></div>
      <div class="step-content" id="step-2"><p>…16 words…</p></div>
    </div>
  </div>
</div>
```

```css
.scroll-item  { position: relative; height: 3000px; }  /* the pacing dial */
.sticky-item  { position: sticky; top: 0; height: 100vh; }
```

The stickiness is **pure CSS**. JavaScript does one job only: fire an event when a step
crosses a threshold, via `IntersectionObserver` — the [Scrollama](https://github.com/russellsamora/scrollama)
pattern. **Never scrolljack** (never hijack scroll physics with JS); it breaks
accessibility and readers hate it.

### Art direction observed

- **Ground:** a single flat paper texture (`rgb(230,228,229)` — pale grey-lavender), reused as the background image of every stage, so the whole piece reads as one continuous surface.
- **Palette:** near-black ink (`rgb(0,0,0)`, `rgb(49,48,45)`), a mid grey (`rgb(146,144,139)`), and two or three flat accent colours used sparingly. Text highlight blocks in dusty pink.
- **Style:** hand-drawn ink and cut-paper collage. Deliberately naive — childlike factories, scribbled smoke. Nothing slick, no gradients, no 3D. It reads as *honest* rather than *corporate*, and it is far cheaper to keep visually consistent than polished vector work.
- **Type:** two voices only — a heavy display serif at very large size (H1 measured at **144px**) for occasional section statements, and a smaller serif for the annotation sentences, set in a **narrow measure** (~30 characters) so blocks sit inside the illustration rather than spanning it.

---

## 5 · Checklist

1. **~1,100–1,400 words of body prose.** More argument means more *drawings*, not more sentences.
2. **Median ~16 words per block**; hard ceiling ~45, and only in the Nut-Graph Island.
3. **One screen of graphic per sentence** through the body.
4. **Zero interactions.** The reveal is the scroll.
5. **Cold Open of 3–5 sentences** ending on the thesis, before the title.
6. **Every significant number gets a Comparison Ladder.**
7. **One continuous illustrated world**, not a set of unrelated figures.
8. **Pre-rendered frame sequences**, not canvas or video.
9. **Abrupt stop, then full sources.**
10. **Mobile first**; honour `prefers-reduced-motion`; readable with JS off.

---

## 6 · Adapting this — don't follow it slavishly

The case study is *investigative journalism about physical infrastructure*. Much of what
makes it work is specific to that. Before copying a pattern, check it still earns its place.

**What transfers to almost any subject**

Cold Open · One Screen One Sentence · Comparison Ladder · Bare Number Block · Nut-Graph
Island · Abrupt Stop Then Receipts · zero interactions · the Pinned Stage.

**What is subject-specific and may not transfer**

- **Scroll-as-Scale** needs a genuinely large quantity. Don't stretch a page to five screens for a number that isn't excessive — it reads as padding.
- **The naive collage style** suits a piece attacking a corporate claim. A tender or technical subject may want a different register. What must survive is the *restriction*: one ground, one ink, two or three accents, two type voices.
- **~40 viewports of scroll** works for a linear physical process. An argument that branches — where the reader must hold two ideas side by side — may need a different structure entirely.

**Adapt the ratios to your material.** The 1:16 word-to-pixel ratio comes from a subject
where the physical scale *is* the argument. A conceptual subject may sit nearer 1:8 and
still be in the form. The invariant is not the ratio — it is that **the drawing carries
steps the prose never states.**

**When not to use this form at all**

- The argument depends on the reader comparing things freely → that's a tool, not an explainer.
- The content is mostly qualitative and quotation-driven → a well-set article is better.
- Nobody can commit to producing ~40 distinct drawings. **The art is most of the work** — a half-illustrated explainer is worse than a good plain article. Scope the drawing budget before committing to the form.

---

## Sources

- **Case study:** [ProPublica — *Why Carbon Capture Can't Solve Climate Change*](case-studies/propublica-carbon-capture.md) — full teardown; [live piece](https://projects.propublica.org/why-carbon-capture-cant-solve-climate-change/); frames in `reference/`
- [NYT — *Jeju Air Flight 2216*](https://www.nytimes.com/interactive/2026/05/01/world/asia/jeju-air-flight-2216-crash-south-korea.html) — same form, paywalled
- Archie Tse (NYT), *Why We Are Doing Fewer Interactives*, Malofiej 2016 — *"If you make the reader click or do anything other than scroll, something spectacular has to happen."* NYT click-through on interactive graphics: 10–15%; ~85% ignore tooltips and rollovers
- [The Pudding — *Easier scrollytelling with position sticky*](https://pudding.cool/process/scrollytelling-sticky/) · [Scrollama](https://github.com/russellsamora/scrollama)
- Chartbeat scroll-depth data (via [Slate](https://slate.com/technology/2013/06/how-people-read-online-why-you-wont-finish-this-article.html), [RebelMouse](https://www.rebelmouse.com/optimal-article-length)) — ~37s average time on an article; 800–1,500 words → 40–55% completion, 2,000+ → 20–30%
