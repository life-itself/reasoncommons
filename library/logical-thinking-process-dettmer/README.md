# The Logical Thinking Process (Dettmer, 2007) — Markdown Edition

Source: `source/logical-thinking-process-dettmer.pdf` (H. William Dettmer, *The Logical Thinking Process: A Systems Approach to Complex Problem Solving*, ASQ Quality Press, 2007. 445 pages.)

This directory is a markdown conversion of the PDF, generated to make the book's content (and its ~250 logic-tree diagrams) usable/searchable/quotable from within this repo. Relevant background: `../../claim-tree-annotation.md`, `../../skills/tree-gen/`.

## How it was made

This is a real reflow, not a raw `pdftotext -layout` dump:

- **Text** was extracted per-page with plain `pdftotext` (no `-layout`), then reconstructed into markdown: hard-wrapped PDF lines were rejoined into paragraphs, running headers/footers/page-number furniture stripped, drop-cap first letters merged back into their word, bulleted and numbered lists reconstructed (as tight lists, no forced blank lines between items), epigraphs turned into blockquotes with their attribution, and `NOTE:`/`CAUTION:`/`TEST:`-style call-outs bolded. Section headings were detected from the book's own typographic conventions (ALL-CAPS = major section, "N. Title" / short Title Case = subsection) and chapter/part titles were injected directly from the book's own Table of Contents rather than reconstructed heuristically. Sentences that the source PDF splits mid-way — because body text visually wraps around a boxed sidebar figure, or a paragraph is cut by a page break and resumes after the next page's heading/figure — are detected (an unpunctuated paragraph followed, once short figure-caption-like fragments are skipped over, by a paragraph starting lowercase) and stitched back into one paragraph.
- **Diagrams** are vector drawings in the PDF, not embedded images, so they can't be extracted as text. Every page identified as containing a figure — the ~222 pages the book's own *List of Illustrations* lists, plus 29 more found by scanning for diagram-label text that had no matching caption (mostly the unlabeled decorative diagrams that open each chapter) — was rendered to a PNG (100dpi, `pngquant`-compressed, ~40KB avg, 251 images total, ~10MB) and embedded inline at the point where that page occurs.
- Each page's rendered image is `images/pNNN.png`, named by the book's own printed page number (e.g. `images/p152.png` = page 152, Figure 4.46, the Fordyce Corporation Current Reality Tree).

The book's **Index** (originally printed pages 405+) is dropped entirely — it's a page-number lookup aid for the print edition and a two-column layout that extracts as a jumbled mess, neither of which is useful in a searchable digital edition.

**Correctness over tidiness**: an earlier version of this pipeline aggressively dropped short/unpunctuated text on any page with a figure, on the theory that it was diagram-label debris duplicated by the embedded image. That turned out to also silently delete real sentences that happened to be short, or that trailed onto a figure-heavy page from the paragraph before it — genuine content loss, not just a style problem. Diagram debris (box labels, Yes/No decision-tree branches, "205 / p. 2" page-reference bubbles) is now only removed by two much narrower, safer passes that run *after* every other cleanup step: one drops a page's text entirely only when literally nothing on that page reads as real prose (≥10 words, ends in real punctuation) — i.e. the page is essentially 100% figure; the other drops individual leftover short/unpunctuated fragments only after confirming (via the sentence-stitching passes) that they have no reachable continuation anywhere nearby, on any page. Neither can delete a real sentence, because a real sentence either reads as substantial prose itself, or gets reunited with its continuation by the stitching passes first. `scripts/check.py` exists to keep this property from regressing silently — see "Checking" below.

**Known rough edges**, in decreasing order of how much they matter:
- Footnotes: the source PDF interleaves footnote text into the reading-order stream between the sentence that references it and the sentence's continuation, and the pipeline doesn't currently detect or re-order those — the words are all present, just not always in the right order around a footnote.
- Occasional run-on sentences where an epigraph or figure-reference immediately follows body text in the source PDF with no paragraph break — the reflow logic can't always tell where one ends and the next begins.
- The front-matter blurb/praise-quote pages and "Also available from ASQ Quality Press" book list (start of `00-front-matter.md`) went through the same generic reflow as body chapters and have a few misfired headings on book/author names — low-value content, left as is.
- Citation footnote markers (e.g. `1:236-260`) are preserved inline as plain text, not converted to real footnotes.

## Contents

| File | Book section | Printed pages |
|---|---|---|
| [00-front-matter.md](00-front-matter.md) | Reviews, title page, copyright, dedication, Table of Contents, List of Illustrations, Preface, Acknowledgments, Introduction | i–xxx |
| [01-chapter-1-introduction-to-toc.md](01-chapter-1-introduction-to-toc.md) | Ch 1 — Introduction to the Theory of Constraints | 3–30 |
| [02-chapter-2-categories-of-legitimate-reservation.md](02-chapter-2-categories-of-legitimate-reservation.md) | Ch 2 — Categories of Legitimate Reservation | 31–65 |
| [03-chapter-3-intermediate-objectives-map.md](03-chapter-3-intermediate-objectives-map.md) | Ch 3 — Intermediate Objectives Map | 67–88 |
| [04-chapter-4-current-reality-tree.md](04-chapter-4-current-reality-tree.md) | Ch 4 — Current Reality Tree | 91–157 |
| [05-chapter-5-evaporating-cloud.md](05-chapter-5-evaporating-cloud.md) | Ch 5 — Evaporating Cloud | 159–204 |
| [06-chapter-6-future-reality-tree.md](06-chapter-6-future-reality-tree.md) | Ch 6 — Future Reality Tree | 205–257 |
| [07-chapter-7-prerequisite-and-transition-trees.md](07-chapter-7-prerequisite-and-transition-trees.md) | Ch 7 — Prerequisite and Transition Trees | 261–309 |
| [08-chapter-8-changing-the-status-quo.md](08-chapter-8-changing-the-status-quo.md) | Ch 8 — Changing the Status Quo | 311–337 |
| [09-back-matter.md](09-back-matter.md) | Epilogue; Appendices A–J (incl. Executive Summary Trees, CRT/EC exercises, 3-UDE Cloud, legal application, Transformation Logic Tree software); Glossary; Bibliography | 339–404 |

## Regenerating

Run `python3 scripts/build.py` from this directory. It re-extracts text from `source/logical-thinking-process-dettmer.pdf` with `pdftotext`, renders the figure pages with `pdftoppm`/`pngquant` (skipping any `images/pNNN.png` that already exists), and rewrites all the `NN-*.md` files. Requires `pdftotext`, `pdftoppm`, and `pngquant` on `PATH` (all from Homebrew's `poppler` + `pngquant` packages).

## Checking

Run `python3 scripts/check.py` (add `--show-warnings` for detail) after any change to `build.py`, before trusting the output. It fails hard on things that should never happen — broken image links, leftover PDF furniture, a list that lost its tight (no-blank-line) formatting, 3+ consecutive blank lines — and separately reports two soft-warning counts for manual review: paragraphs that still look like they end mid-sentence, and suspiciously short headings. Both warning counts are compared against `scripts/check_baseline.txt`; a run that increases either number is very likely a regression from a `build.py` change and should be looked at before the baseline is updated. This exists because several early versions of the reflow logic silently dropped or garbled real text on figure-heavy pages — see `scripts/build.py`'s git history for the kind of thing this is meant to catch early.
