---
created: 2026-08-14
status: reference
type: case-study
---

# Case study — ProPublica, *Why Carbon Capture Can't Solve Climate Change*

**Read it:** <https://projects.propublica.org/why-carbon-capture-cant-solve-climate-change/>
(ungated, no login, no paywall)

**Credits:** ProPublica × Drilled, part of the *Carbon Captured* investigative series.

**Why this one.** It is the clearest available demonstration of the scrollable-explainer
form doing genuinely hard explanatory work — taking a technical, abstract, numbers-heavy
argument and making it land physically. It is also completely free to read, which makes it
a shareable common reference.

Patterns extracted from it live in [`../scrollable-explainers.md`](../scrollable-explainers.md).
This file is the underlying evidence: what the piece actually does, measured.

**Method.** Loaded in headless Chromium at 1280×900, 2026-08-14. DOM inspected for
structure, computed styles and asset strategy; all text blocks extracted in document order
with scroll positions; sixteen viewport screenshots taken at even intervals. Four
representative frames saved to [`../reference/`](../reference/).

---

## 1 · The vital statistics

| | |
|---|---|
| Editorial text blocks | **79** |
| Total editorial words | **1,834** |
| — body prose | **≈1,100** |
| — Notes on Data Sources | **≈700** |
| **Median words per text block** | **16** |
| Longest blocks | 39–45 words — nut graphs only |
| Shortest blocks | 2 words (`$500 billion`) |
| Page height | **35,867px** ≈ 40 viewports |
| Typical gap between text blocks | **≈900px — one full screen** |
| `<img>` / `<svg>` | 31 / 18 |
| Pinned stages (`.sticky-item`) | **7** |
| `<canvas>` / `<video>` | **0 / 0** |
| Buttons, sliders, toggles, tooltips | **0** |

**The defining ratio: ~1 word per 16px of scroll.** A conventional article runs about
1 word per 1.5px. This piece gives roughly **ten times more visual space per word**.

Note also how the words are distributed: **38% of all editorial text is the sources
appendix.** The actual argument is about 1,100 words — shorter than a newspaper feature —
spread across forty screens.

---

## 2 · The scroll map

Positions are measured pixel offsets on the live page.

| y | Section | Words | Function |
|---|---|---|---|
| 209–479 | **Cold Open** | 11 / 17 / 4 / 8 | Four sentences over an animating illustration, one per screen |
| 4,158 | **Title card** — "False Promises" | 2 | The H1, arriving 4,000px in |
| 4,725–5,225 | **Nut graphs** | 7 / 39 / 31 / 45 / 22 | The only paragraph-density in the piece |
| 5,988–9,111 | *The gap between promise and reality* | 7–39 | Projections vs. actual burial |
| 9,339–10,497 | *The four capture methods* | 5–15 | Display-serif section statement, then four labelled drawings |
| 11,797–15,520 | *Land footprint* | 12–23 | Scale ladder → "the size of Mexico" |
| 16,535–19,889 | *Pipelines* | 9–24 | **Scroll-as-Scale** — the signature sequence |
| 20,804–23,902 | *Storage sites and cost* | 14–41 | → "a new waste site every four days for 25 years" |
| 24,061–24,286 | **Bare Number Blocks** | 2 / 10 / 2 / 5 / 2 / 8 | $500bn vs $340bn vs $50bn, each captioned |
| 24,556–29,213 | *Why the test sites fail* | 11–42 | Six failure modes, one per screen |
| 30,228–32,183 | *Solar, the comparison* | 6–33 | The counter-example; ends on 6 words |
| 33,156–35,046 | **Notes on Data Sources** | ~700 | Dense, plain, unstyled |

---

## 3 · The Cold Open, verbatim

The first four text blocks, one per screen, over a hand-drawn earth ringed with factories
while smoke plumes animate upward and a vacuum hose descends:

> **Global leaders are banking on tech advances to solve climate change.** *(11 words)*
>
> **One leading idea is to capture carbon pollution from the air and then bury it underground forever.** *(17)*
>
> **It may sound practical.** *(4)*
>
> **There is no conceivable way it can work.** *(8)*

Forty words. Three sentences build the reader's assumption in good faith — note that the
idea is stated *attractively*, not strawmanned — and the fourth demolishes it flatly, with
no hedging and no cleverness.

**What to take from this:** it is prediction-and-violation executed with **zero
interaction**. No button, no "guess first" prompt. The withholding is done purely by
pacing — you cannot see sentence four while reading sentence three, because it is a screen
away. Scroll *is* the reveal mechanism.

The headline does not appear until 4,000px later. The piece earns your attention before it
introduces itself.

![Cold open](../reference/ccs-01-cold-open.png)

---

## 4 · The features that work

### 4.1 · Scroll-as-Scale — the signature move

The pipelines sequence (y=16,535–19,889) draws a pipe that snakes down through screen after
screen. Three sentences land as you descend:

> In the U.S. alone, this could require building more than 68,000 miles of new pipelines in a little more than two decades.
>
> That's more than double the distance to fly around the earth.
>
> And longer than the country's entire interstate highway system.
>
> Globally, pipelines could tally in the hundreds of thousands of miles.

You *feel* the length because your thumb had to travel it. The drawing is not illustrating
the number — **the scroll is the number.**

This is the most transferable technique in the piece and the hardest to fake. It only works
when the quantity is genuinely excessive; stretching a page for an unremarkable number
reads as padding.

![Scroll as scale](../reference/ccs-04-scroll-as-scale.png)

### 4.2 · The Comparison Ladder

No large number is ever left as a number. Each is converted, rung by rung, into something
bodily — and each rung gets its own screen:

> 6 billion tons of CO₂ a year
> → 768,000 square miles of land for carbon-absorbing plants
> → *"roughly the size of Mexico — and compete for valuable land used to grow food"*
> → 2,000 storage reservoirs
> → **"a brand new geological waste site somewhere on the planet every four days for the next 25 years."**

The final rung is the best sentence in the piece. It converts a quantity into a **cadence** —
a rate you can picture actually happening, repeatedly, for a span you can imagine living
through. Quantity → rhythm is the highest rung on any comparison ladder.

### 4.3 · Bare Number Blocks

The cost argument is made almost entirely without prose. Six text blocks, alternating
number and caption:

> **$500 billion** — *annual global expenditure on carbon capture and storage by 2050*
> **$340 billion** — *China's military budget in 2025*
> **$50 billion** — *U.N.'s humanitarian and development aid budget in 2024*

Two words, then a caption. The juxtaposition does the arguing; no sentence says "this is a
lot." Trusting the reader here is what makes it land.

### 4.4 · The Nut-Graph Island

Exactly one region of ordinary paragraph density (y=4,793–5,225): four paragraphs of 39,
31, 45 and 22 words stating what the investigation found. Then the piece never returns to
that density until the sources. Density is rationed to the one place it's needed.

### 4.5 · The display-serif section statement

Occasionally a full-width statement in very large display serif (H1 measured at **144px**)
acts as a chapter marker — *"To make CCS work, we would need to capture CO2 pollution in
four ways:"* — followed by four small labelled drawings, each with a five-to-fifteen word
caption. Big type does the structural work that subheadings would do in an article.

![Explainer diagram](../reference/ccs-03-explainer-diagram.png)

### 4.6 · Abrupt stop, then receipts

The body's last line is six words:

> **Carbon capture and storage remains elusive.**

No summary, no call to action, no rhetorical lift. Then straight into ~700 words of
*Notes on Data Sources* — every figure traced to a named report, plus the IEA's emailed
response quoted at length against itself. The transparency **is** the ending, and it does
more for credibility than a peroration could.

### 4.7 · Art direction as argument

Hand-drawn ink and cut-paper collage on a single flat paper texture. Deliberately naive —
childlike factories, scribbled smoke plumes, wobbly pipes. Nothing slick, no gradients, no
3D renders.

This is a rhetorical choice, not just an aesthetic one. The piece is attacking a
corporate-technocratic claim; the hand-made style positions it as *honest* against
*polished*. It is also far cheaper to keep visually consistent across forty screens than
polished vector work would be.

![Sticky illustration](../reference/ccs-02-sticky-illustration.png)

---

## 5 · How it's built

### Structure

```html
<div class="scroll-item">              <!-- relative; height 1,700–4,240px -->
  <div class="sticky-item">            <!-- sticky; top:0; height:100vh -->
    <div class="sticky-item-container">
      <div class="sticky-item-bg"><img src="2026-ccs-page-bg.jpg"></div>
      <img id="footprint-sequence">    <!-- src swapped per scroll step -->
      <svg><!-- charts --></svg>
      <div class="opener-step-content-desktop"><p>…16 words…</p></div>
    </div>
  </div>
</div>
```

```css
.scroll-item { position: relative; height: 3000px; }   /* the pacing dial */
.sticky-item { position: sticky; top: 0; height: 100vh; }
```

**Measured `.scroll-item` heights: 1,700px · 3,330px · 4,230px · 4,240px** — roughly 2 to
4.7 screens each. This container height is how pacing is controlled; there is no timing
code.

### Notable implementation choices

- **Stickiness is pure CSS.** No scroll listeners for positioning. JS only fires step events.
- **Animation is a pre-rendered frame sequence** — an `<img>` whose `src` steps through numbered frames. No `<canvas>`, no `<video>`, no WebGL anywhere in the page. Robust, cheap, degrades gracefully.
- **One shared background texture** (`2026-ccs-page-bg.jpg`) is reused as the backdrop of every stage, which is what makes forty screens read as a single continuous surface rather than a slideshow.
- **Charts are inline SVG**, drawn once, revealed by step.
- **Zero interactive controls** in the entire editorial body.

### Palette measured

| Role | Value |
|---|---|
| Ground (paper) | `rgb(230, 228, 229)` — pale grey-lavender |
| Ink | `rgb(0, 0, 0)` / `rgb(49, 48, 45)` |
| Mid grey | `rgb(146, 144, 139)` |
| Text highlight | dusty pink blocks behind Cold Open sentences |

Two type voices: a display serif (*Feature Headline*) at very large sizes for statements,
and a smaller serif for annotation sentences, set in a narrow measure (~30 characters) so
blocks sit *inside* the illustration rather than spanning the page.

---

## 6 · What we'd do differently

Honest notes, so this doesn't get treated as scripture.

- **The sources appendix is 38% of the text.** Right for investigative journalism where the numbers are contested; probably disproportionate for an explainer of an established idea.
- **Forty viewports is a lot.** It works because the subject is a linear physical process — capture, transport, store — that genuinely has stages. An argument that branches, or that asks the reader to hold two ideas side by side, would strain this structure.
- **No navigation or progress indicator.** On a 35,000px page the reader has no sense of how much remains. A slim progress rule would cost nothing.
- **The naive collage style is subject-specific.** What must survive porting is not the style but the *restriction*: one ground, one ink, two or three accents, two type voices.

---

## 7 · Full text, in scroll order

Preserved because the rhythm is the lesson — read down the word counts and you can see the
form. `[n]` is the word count of each block.

**Cold open**
`[11]` Global leaders are banking on tech advances to solve climate change.
`[17]` One leading idea is to capture carbon pollution from the air and then bury it underground forever.
`[4]` It may sound practical.
`[8]` There is no conceivable way it can work.

**Title** · `[2]` False Promises

**Nut graphs**
`[39]` For more than 40 years, oil companies have been funding research at prestigious universities into climate change "solutions" that would not require the public to stop using oil and gas…
`[31]` An investigation by ProPublica and Drilled has found that boosters of CCS have ignored evidence of the technology's limitations, or overstated its potential…
`[45]` They've promoted this idea despite the fact that for CCS to work at the scale now envisioned, the world would need to devote almost unimaginable resources…
`[22]` Optimism has reigned, however, because small tests have worked and because slow global response to climate change has left few other options.

**Body**
`[34]` In 2008, the International Energy Agency projected that to stave off dangerous levels of warming, we would have to be burying around 1.6 billion tons… of CO2 per year…
`[7]` Since then, its optimistic projections have continued.
`[12]` But deployment of the technology has never come close to those ambitions.
`[19]` Right now, globally, we're permanently burying less CO2 than a single large power plant can emit in a year.
`[39]` Some experts point to the CO2 that gets pumped into the ground to help extract oil as proof CCS works. But that process… isn't designed to function that way.
`[12]` Global leaders are betting on carbon capture working now more than ever.
`[13]` The models used in the latest United Nations assessment presume the technology succeeds.
`[23]` IEA representatives and U.N. modelers say their projections reflect what the world has to do to achieve its goals of averting extreme warming.
`[14]` **To make CCS work, we would need to capture CO2 pollution in four ways:**
`[5]` Trap it from smoke stacks.
`[10]` Absorb it from the air with fast-growing grasses or trees,
`[12]` then capture it from those plants when they are burned for fuel.
`[9]` Scrub it from the air, often using giant fans.
`[15]` Then we would pump all of it into porous rock deep beneath the earth's surface.
`[23]` The U.N. analysis now suggests that countries must inject 6 billion tons of CO2 underground each year by the middle of the century.
`[17]` Getting 6 billion tons of CO2 a year out of the atmosphere, though, is a daunting task.
`[12]` Imagine the neighborhoods and parks near oil, gas or coal-fired industrial plants.
`[20]` We would need to add equipment to capture the CO2 from each facility, in some cases doubling its land footprint.
`[18]` And we would need to devote about 768,000 square miles of land worldwide to growing those carbon-absorbing plants.
`[23]` That would cover an area roughly the size of Mexico — and compete for valuable land used to grow food or sustain forests.
`[24]` If all of this works, and the CO2 is successfully captured, it must then be moved to a place where it can be buried.
`[22]` In the U.S. alone, this could require building more than 68,000 miles of new pipelines in a little more than two decades.
`[11]` That's more than double the distance to fly around the earth.
`[9]` And longer than the country's entire interstate highway system.
`[11]` Globally, pipelines could tally in the hundreds of thousands of miles.
`[33]` To cross the oceans, we would need at least 85 specially built tankers… As of April, there were only three ships in the world equipped to do that.
`[18]` Then, there is the challenge of finding a place to put 6 billion tons of CO2 a year.
`[41]` Today, just 12 large-scale geologic reservoirs have attempted to permanently store CO2 pollution — but we would need more than 2,000 reservoirs of that size…
`[25]` That means we would need to open a brand new geological waste site somewhere on the planet every four days for the next 25 years.
`[14]` Every site would need constant monitoring for decades to ensure the CO2 doesn't leak.
`[14]` Even if this could be done, it would cost tens of trillions of dollars.
`[18]` Right now, U.S. taxpayers are paying oil and gas companies $85 for every metric ton they put underground.
`[35]` At that rate, by 2050, the world could be spending half a trillion dollars — more than China's military budget, and 10 times more than the U.N.'s… aid budget.
`[2]` **$500 billion** · `[10]` annual global expenditure on carbon capture and storage by 2050
`[2]` **$340 billion** · `[5]` China's military budget in 2025
`[2]` **$50 billion** · `[8]` U.N.'s humanitarian and development aid budget in 2024
`[16]` The few test sites that exist suggest that keeping carbon underground may not work at scale.
`[42]` Since 1996, while the 12 large-scale geological storage projects have opened, plans for another 12 have been scrapped…
`[12]` Some rock layers can hold far less CO2 than experts have estimated.
`[11]` Finicky pipes and injection systems can get clogged or break down.
`[24]` The rock that seals CO2 in place can crack, risking a leak. In one instance, injected CO2 caused the ground above it to bulge.
`[12]` In another instance, CO2 escaped from an old oil industry well nearby.
`[14]` Thorough, long-term monitoring can be expensive, but without it, such leaks could be missed.
`[14]` Climate experts know about the costs, technical troubles and failures of CCS test projects.
`[19]` Yet many of them have continued to boost the technology, even as they have downplayed solutions showing greater progress.
`[33]` For example, the same modelers who overestimated the potential of geological carbon storage repeatedly underestimated solar power…
`[13]` Over the last several decades, solar power is the technology that has thrived.
`[6]` **Carbon capture and storage remains elusive.**

**Notes on Data Sources** · ~700 words across 14 blocks.
