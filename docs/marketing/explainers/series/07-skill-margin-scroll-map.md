# Margin scroll map and visual brief

Reviewed against the revised narrative and critique before implementation. Scope: `explainer-margin-pacing-2026-10-20` revision 1. The original prose is unchanged; flow markers are attributes on existing elements. Existing drawing triggers remain the clock.

The cast begins as a list, then becomes a persistent avatar strip during conversations. An olive ring and written name identify the current person; terracotta stays with the constraint. Each conversation has a short heading. A phone notification occupies one complete beat before opening. The device contains at most the latest message and its predecessor. At narrow widths it becomes a compact lower margin and the drawing occupies the unobscured area. The same beat state controls every width. No timer may unlock information and there is no nested scrolling transcript.

## Part one

| Story beat | Margin state |
|---|---|
| Opening and Maria introduction | Cast; highlight Maria. No conversation. |
| s1–s5 | Highlight each introduced station; reveal only its established capacity. |
| s6–s8 | Hold the established comparison. |
| The other forty go home | Highlight Reason Commons; explain why Sam brings it in. |
| Man with cough; 10,000 | Sam asks for help; skill separates observation from hypothesis. |
| h1–h5 | One message each: hire question, check-in consequence, other stations question, doctor constraint, proposed consequence. |
| Maria was never the problem; constraint named | Sam accepts; skill records Sam's working position. |
| d1–d4 | Clinical hours, admin hours, saved cause, conditional improvement. |
| Reception slows; only then spend; tidy example | Sam's notification, Maria's concern, skill saves side effect. |
| m1–m4 | Finished?, next constraint, pharmacy/hospital?, review backlog. |
| r1–r2 | Leila captures rule; skill asks its purpose. |
| Sources | Concrete starting prompt and install route. |

## Part two

| Story beat | Margin state |
|---|---|
| Opening through private explanations | Cast and established perspectives. Nothing captured. |
| Nothing changed except outside you | Explicit skill introduction. |
| Intuition; funding feeling; rank | Sam invites writing, doctor captures, skill records proposed chain. |
| w1–w3 | Hold: drawn does not mean checked. |
| q1–q7 | Clarify, state claim, missing condition, uncertainty, sign versus cause, predicted evidence, test backlog. |
| Page takes criticism; legal move; it doesn't always work | Notification, Maria's challenge, disputed link. |
| Back to clinic; chains on wall | Doctor's observation, saved as proposed evidence. |
| Some chains won't survive; what's left | Tomasz's older figures, funding objection saved. |
| One map; next question | Sam asks for the record; skill shows the open link. |
| Sources | Closing invitation. |

## Part three

| Story beat | Margin state |
|---|---|
| Hero; good, now what? | Cast; explicit introduction for planning a change. |
| g1–g3 | Ask success, Tomasz's goal, saved proposed goal. |
| Until sentence exists; cannot argue about gap | Sam accepts; skill records Sam's acceptance. |
| u1–u3 | Symptoms, shared-cause inquiry, hypothesis reminder. |
| v1–v4; cloud breaks | Notification, doctor's need, assumption question, doctor's challenge, disputed assumption. |
| f1–f3 | Proposed fix and its conditional effects. |
| f4; forty minutes; find that now | Notification, Maria's cost, saved side effect. |
| p1–p4 | Three obstacles then proposed objective. |
| Forced order; five questions | Draft standard before training; named owners and Friday. |
| Maria sees connection; manager disagrees; first time | Hypothesis, objection, disputed link and two-week comparison. |
| Sources | Closing invitation. |

## Verification

Check every trigger at 1440×900, 1280×720, 375×800 and 390×844, plus tablet and short landscape. Check fast/reverse scroll, resize, reduced motion, latest-message visibility and document overflow. On a fresh visit to check-in, later capacities and all skill messages must be absent. Waiting must not advance messages. Check notification holds and wheel scrolling over the device. Compare original story text and files for preservation. Comprehension remains an open reader test.

## Implementation evidence — 20 October 2026

All 100 assigned beats were checked at 1440×900, 1280×720, 390×844, 375×800, 900×900 and 844×390. Final checks found no caption/beat mismatch, mounted transcript longer than two messages, message clipping, companion-panel overflow or document overflow. Twenty-four settled screenshots at desktop and phone widths were inspected in contact sheets. The repository's Chrome phone checker independently reported 375px viewport and 375px document width with no overflow for The Wrong Queue. The 713-link/asset website check, current exports, JavaScript syntax checks and diff whitespace check pass.

The checks exposed and corrected four issues: closely spaced prose markers could skip an arrival; long node replies could clip at phone and short landscape heights; the original tall station stack became too small beside a lower margin; and crossing the phone breakpoint needed fresh drawing geometry. Marked prose now has reading space, replies are concise, phone drawings use compact geometry and larger labels, and a width change rebuilds from the original SVG template while keeping the reading beat. The doctor is marked as the constraint only after all five capacities have been introduced.

A settled notification remained at message one after a 2.5-second hold, and opened only at its next assigned beat. Reverse navigation to check-in removed all chat and later capacity values. Wheel scrolling over the device moved the main story. Hide/show, reload with the hidden preference, and a 375→1440→900 resize were checked. Original story paragraphs match all three originals after excluding edition notices, and the original editions and shared scroller files are unchanged.

Temporary accessibility fixtures used the current source: the reduced-motion fixture simulated the preference for JavaScript and applied the actual reduced-motion CSS rules; it had no arrival animation or step transition and kept the same message state. The script-free fixture removed all scripts and exposed the actual noscript fallback; every story step remained readable without overflow. This checks the fallback branches without changing operating-system preferences; it is not a native preference-toggle test.

The scripts, editorial critique, mapping and implementation are local working files on `claude/explainers-skill-connections-48f05d`. The previous private Claude artifact has not been replaced. David's editorial review and the existing test with new readers remain open; these technical checks do not establish comprehension.
