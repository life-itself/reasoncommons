# Reason Commons landing page: implementation handoff

Prepared 21 October 2026 from the designer prompt and the landing-page copy. Nothing has been committed to `life-itself/reasoncommons` or published to reasoncommons.com. The repository's `AGENTS.md` requires a typed change proposal and recorded acceptance before this lands, so committing it is a separate step.

## What is here

| File | Purpose |
| --- | --- |
| `index.html` | The complete page: one self-contained file (HTML, CSS, inline SVG, a small script). Suggested home: `website/landing-lab/shared-working-table/index.html`, beside the existing candidates. |
| `hero-illustration.svg` | The hero illustration as a standalone asset (people around a shared table, one place left open). |
| `reason-commons-social.png` | 1200×630 social preview image. |
| `previews/` | Desktop (1440px) and phone (375px) full-page captures, each session view, and the no-JavaScript phone rendering of the session. |

Page title, description, canonical URL, Open Graph and Twitter metadata, image alt text, a skip link and a reduced-motion state are all in `index.html`.

## Form integration

The integration point is the `data-endpoint` attribute on `<form id="join-form">`. It is empty, so the page currently shows a preview notice above the form, and a send attempt shows "Your message was not sent. Please try again." with every field kept. No success is ever simulated.

When an endpoint is set, the script sends `POST` with a `FormData` body and `Accept: application/json`, and shows "Thank you. Your message has been sent." only on a 2xx response. Any other status or network error shows the failure message and keeps the entered text.

| Field | Values |
| --- | --- |
| `name` | required |
| `email` | required |
| `interest` | `beta` (default), `pilot-or-research`, `funding-or-support` |
| `bring` | free text, optional |
| `agent` | sent only when `interest` is `beta`: `claude-code`, `codex`, `another-compatible-agent`, `none-yet` |

A hidden `website` field is a spam trap; the script drops it and does not send if it is filled. The endpoint must accept cross-origin posts from the page's origin. For submission without JavaScript, also set the form's `action` to the endpoint; the endpoint's own confirmation page then applies.

The beta buttons scroll to `#join`, select "Trying the beta" and focus the name field. "Discuss research or support" clears that choice and focuses "Hosting a pilot or research partnership", with the submit label switching to "Start a conversation".

## Destinations used

All links are the verified destinations from the copy document: `#session`, `#idea`, `#support`, `#join`, `https://reasoncommons.com/skills`, `https://github.com/life-itself/reasoncommons/tree/main/skills/reason-commons` and `https://reasoncommons.com/about`. No email address, calendar link or `/beta` route was added.

## Remaining publication dependencies

1. A form endpoint and a decision on who receives and stores submissions. The copy makes no privacy statement and none was added; decide whether one is needed next to the form.
2. Upload `reason-commons-social.png` to `https://reasoncommons.com/assets/reason-commons-social.png`, or change the `og:image` and `twitter:image` URLs to wherever it lives.
3. `canonical` and `og:url` point to `https://reasoncommons.com/`. Change them if the page is published at a landing-lab path first.
4. Fonts are Alegreya and Alegreya Sans (SIL Open Font License), loaded from Google Fonts. Self-host them if the site prefers no third-party font requests.
5. Analytics: the Flowershow config uses Google Analytics, but this standalone page includes none. Add the site's snippet if it should be measured.
6. Making it the homepage means replacing the route served by `website/README.md`; follow `docs/product/repository-boundaries.md` and preview with `fl` before production.

## Interface wording added beyond the supplied copy

All supplied copy appears verbatim. The interactive example needed some short labels, listed here for editorial review:

- Hero: an "Early" stamp beside the current-product line.
- Session tabs and buttons: "Understand", "Try", "Return", "Next: Try", "Next: Return". Each view's caption reuses sentences from the How it works copy.
- Card kinds: Observation, Possible explanation, Concern, Proposal, Report, Open question, and the legend describing each line style.
- Attribution and status: "Brought by the group", "Illustrative" on every card, "Attached to: a more explicit invitation, not yet proposed", "Attached to: this trial", "Not yet chosen", the standing track "Proposed / Chosen / Tried" ("Tried once" in Return), "From a newcomer", "Kept visible", "Unresolved".
- Try slots: "What we hope it will improve", "What concerns us", "Who could report", and "Newcomers: how the invitation felt, and whether they took it up."
- Return: "Recorded before the trial", "Reported after", "Recorded before · hope / concern / the problem", "Report · still uncertain", and the relation labels "might explain", "reported", "not yet known".
- Support ledger labels: "Today", "What support could enable", "The question", "What would count as evidence", plus "Read the source" and "Try the skill" proof links reusing the footer labels.
- Idea section: the catalogue-card header "Common sense / a practice".
- Form: "(optional)" on the agent question, and the preview notice that disappears once an endpoint is set.

## What was checked

- No horizontal overflow at 375px, 820px and 1440px; no console errors.
- Session tabs work with click, arrow keys, Home and End; with JavaScript off, the three views read in sequence with the fictional label at the top.
- With reduced motion, no animations run.
- The fictional label stays pinned at the top of the example while it scrolls, and every card carries "Illustrative".
- Contrast on paper: ink 10.5:1, secondary text 6.7:1, clay text 6.1:1, white on the clay button 5.5:1.

Not yet checked: real screen readers, Safari and physical phones, and a live form endpoint.
