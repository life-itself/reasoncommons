# Teardown — Co-Star, *How does astrology work?*

Reference model for the explainers-v2 form. Index: https://www.costarastrology.com/how-does-astrology-work · first chapter: https://www.costarastrology.com/how-does-astrology-work/what-is-astrology. The site is client-rendered, so plain fetches return an empty shell; render it with headless Chrome (`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --virtual-time-budget=10000 --dump-dom <url>`). Read 2026-09-18.

## Series shape

- **Index page** (~240 words): title, subtitle ("The Astronomy of Astrology: A 101 from your friends at Co–Star"), then a numbered list of 8 chapters. Each entry is number + title + arrow + a one-sentence teaser that is itself the chapter's key point ("The natal chart (a.k.a. birth chart) is a map of the universe at the exact place and time that someone was born.").
- **8 chapters**, each building on the last: what is astrology → natal chart → sun signs → rising sign → houses → house systems → aspects → transits & orbs.

## Chapter shape (*What is astrology?*, ~350 words including captions)

- One point: astrology views the sky from Earth's perspective; the zodiac is the band the planets move through.
- A short opening claim in large type ("Astrology & astronomy were a single discipline for thousands of years."), one paragraph of context, then "We begin with astronomy."
- Then alternating one-or-two-sentence paragraphs and illustrations. Illustrations: 3 looping GIFs (heliocentric, geocentric, helio-vs-geo side by side), several static PNG/SVG drawings (zodiac ring, constellations on the horizon). Captions are small caps labels ("GEOCENTRIC MODEL OF THE UNIVERSE (EARTH IN THE CENTER)").
- A comparison panel: Heliocentric vs Geocentric, each with a one-line gloss.
- **End:** a "NEXT SECTION" card — number, title, arrow, the next chapter's teaser — then "ALL SECTIONS" listing every chapter.
- No scroll-driven behaviour. The text column is fixed; motion lives only in looping illustrations.

## What to take

- One idea per chapter, stated as its teaser. If you can't write the teaser, the chapter isn't focused.
- Short paragraphs; the illustration does the explaining, the text names what to look at.
- Looping animation for things that *move* (flow through a system, a queue growing, a tree growing), static drawings for structures.
- The next-chapter card sells the next chapter with its key point, so the series reads as a chain.
- Friendly, plain, "your friends at" register — consistent with the [voice guide](voice-guide.md).
