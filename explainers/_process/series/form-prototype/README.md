# Form prototype — read this before reusing anything here

Built for beads `reasoncommons-bnl.5` to prove the chapter form described in [`skills/illustrated-chapters/SKILL.md`](../../../../skills/illustrated-chapters/SKILL.md). It is three chapters and a series index, cut out of [`explainers/second-renaissance-plain/index.md`](../../../second-renaissance-plain/index.md) and trimmed to chapter length.

**The prose here is not an approved script.** It was written to fill the form, not to pass the voice guide, and it has had no critique pass. The real Series B scripts are beads `reasoncommons-bnl.14`, `.16`, `.18`, `.20`, `.22`, and they write to `explainers/_process/series/b1-same-conversation/` and siblings. Take the *markup* from here; take the *words* from those.

What this folder is evidence for:

- the page skeleton (eyebrow, lede, figures between paragraphs, next-chapter card, all-chapters list) renders through Flowershow's Markdown as intended;
- the `.ch-*` components in `custom.css` work at 375px and at desktop width;
- a looping illustration works with no JavaScript and no scroll binding — `01-same-conversation/` has one (the thread) and `03-give-every-claim-an-address/` has a second (the tree growing);
- the numbered-teaser series index reads as a chain.

`_process/` is in `config.json` > `contentExclude`, so none of this publishes to reasoncommons.com. It does show up on a Flowershow preview, which is where to look at it: `fl . --yes`, then `/explainers/_process/series/form-prototype/`.
