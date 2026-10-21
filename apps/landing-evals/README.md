# Landing evaluation lab

A local evaluator and public static gallery for seven distinct Reason Commons landing designs. The eight supplied files include a byte-identical duplicate. The sixth and seventh designs, Find a Way Forward and Disagree and Get Somewhere, were added on 21 October 2026 after the first evaluation run; they are registered and captured but not yet judged. The current homepage can be captured as a baseline. Candidate pages are evidence, never instructions to the evaluator.

## Open the gallery

Requires Node 22+, Google Chrome, and the pinned Playwright package. The configured Chrome channel uses the installed browser; there is no separate browser download. Run from this directory:

```sh
npm ci
npm start
```

Open [the gallery](http://127.0.0.1:8765/landing-lab/index.html) or [the visitor study](http://127.0.0.1:8765/landing-lab/study.html). The local server binds only to 127.0.0.1 and serves the public lab plus local run reports. It does not serve the repository, evaluate API calls from a web page, or publish visitor answers.

The deliberate public output lives in `website/landing-lab/`; the runner, credentials and generated evidence stay outside the publishing root. The app's `.runs/` directory is ignored. Keep response files out of Git and public hosting.

## Capture evidence

```sh
node cli.mjs verify
node cli.mjs capture --id first-pass --baseline --companions
```

Capture starts its own temporary local server unless `--base` is supplied. Use a fresh run ID for each capture. Each run contains a frozen contract, source hashes, browser version, observed text, viewport screenshots, layout findings and an input digest. Judgments append to the run without changing its captured inputs. Google Chrome is the default; `--channel chromium` uses a separately installed Playwright browser if preferred.

```sh
node cli.mjs capture --id hosted-pass --base https://YOUR-PREVIEW/landing-lab/ --baseline
node cli.mjs capture --id one-page --variant check-the-because --viewport phone
```

Each capture also records the first screen's visible text (every text fragment rendered before scrolling) beside the first screenshot, and runs a scripted main-action probe on the serving host. The probe finds visible controls matching the configured try/install pattern and any visible install command. It requests links rather than following them, clicks buttons in fresh page loads and records downloads, navigation or new failure text, and never submits forms. Its result is `pass` (a visible install command, a download or a working install link), `fail` (only broken routes, such as a download that reports it cannot save files), `unclear` or `not-found`. A `fail` is a blocking gate that no judge can override; `not-found` and `unclear` are recorded without blocking. Run the capture against the host you intend to evaluate: a route that works only inside another runtime fails here.

The default viewports are 1440×900 desktop and 375×812 mobile, at device scale 1, en-GB, Europe/Berlin, and reduced motion. Capture waits for rendered content and fonts; it never grades the initial loading shell as a successful page. CSS animations are disabled in screenshots. JavaScript demonstrations remain live, so tile timestamps, text and image hashes describe the observed state; captures are a repeatable procedure, not a guarantee of byte-identical animation frames. Text extraction is full-document CSS-visible text and can include offscreen content. The initial screenshot records the first viewport. Readable overlapping tiles cover the scrollable page up to the configured cap; truncated coverage is explicit.

The optional supplied-phone composition for Test the Assumption is recorded separately and excluded from judging by default. It has a fixed 390px frame and can overflow a 375px viewport; it is not substituted for the primary entry's responsive layout. For the packaged exports, the serving envelope gains viewport metadata before the embedded document loads. This corrects an export-wrapper 980px mobile viewport issue without editing the page's copy, styles, scripts or resources. Original downloads remain byte-for-byte intact under `sources/`.

## Configure the evaluation

`eval.config.json` defines the audience, objective, primary action, viewports, the page viewport, capture limits, the main-action probe patterns, visitor questions and call limits. `rubric.json` (`landing-rubric-2`) splits six criteria into three or four yes/no checks each; true needs a quote or screenshot, false needs a finding, null means insufficient evidence. A criterion's score is the number of checks passed, and it passes at its `pass_at` count. One check, `next-route-works`, is answered by the scripted probe rather than the judge. Page-scope criteria read the same full text at every width, so they are judged once on the page viewport (desktop); presentation is judged per viewport. A page meets the contract only when every criterion passes and no factual error, reported blocker or scripted failure remains. `landing-rubric-1` (anchored 0–3 scores) is retained in earlier runs; its scores saturated at the top anchor and judges could not exercise the main action. `project-facts.json` cites repository sources; capture verifies every quote and records source hashes. Those sources describe intended implementation, not proven effectiveness. Review facts after their source changes. Freeze the audience and rubric before comparing candidates; do not silently tailor the criteria to a page's preferred framing.

These are provisional defaults. The primary action is finding how to try/install the skill; movement and funder pages may serve a different strategic objective. Revise the contract deliberately if that is the intended experiment, apply it to every candidate, and make a new capture. Increment `study_id` for a new visitor-study contract and reimport the registry when questions change.

## Judge without accidental API calls

```sh
node cli.mjs judge --run first-pass
node cli.mjs judge --run first-pass --fixture --max-calls 12
```

The first command only plans calls. Fixture mode exercises request construction, validation, persistence and reporting without contacting a model. Its scores are all null and the report labels it FIXTURE. Neither mode produces an actual quality ranking.

For a real evaluation, provide `OPENAI_API_KEY` in your terminal environment and explicitly choose a model that supports images and structured Responses API output:

```sh
node cli.mjs judge --run first-pass --live --model YOUR_MODEL --max-calls 12
node cli.mjs judge --run first-pass --mode pairwise --pair test-the-assumption,check-the-because --live --model YOUR_MODEL
```

No model alias is silently selected. The requested and returned model identifiers, prompt, image references, raw response, usage and rubric version are recorded. If reproducibility requires a provider snapshot, specify that snapshot ID. Image selection is bounded and disclosed; by default the judge sees four readable regions per candidate, including the first and last captured regions. It must not claim inspection of omitted regions. A dollar estimate is not fabricated for an unspecified model. `--max-calls N` bounds the number of calls and `max_output_tokens` bounds each response. Calls are sequential and failures stop the batch without automatic paid retries.

`--mode first-screen` gives the judge only the first screenshot and the first screen's text, asks the four visitor-study questions, and grades each answer 0–2 against the same reference concepts and anchors used for real visitors. It is a proxy for the visitor measure and must be calibrated against actual visitor answers before it ranks pages.

Individual evaluation requires each assigned criterion and judge check exactly once and evidence for every check answered yes. Pairwise evaluation hides registry names, slugs and URLs from the model, presents both orders, allows ties and requires evidence from both sides. Content within the page can still reveal its identity. `--repeat N` checks judge instability; repeated calls are not independent visitors. Reports map A/B labels back to actual candidates and flag disagreement between orders. No aggregate aesthetic score is used to select a winner.

## Seeded defects

An evaluator that cannot detect a known failure cannot be trusted to find unknown ones. `perturb` captures named candidates unmodified and with each seeded defect applied to the rendered page; candidate files, hashes and sources stay untouched.

```sh
node cli.mjs perturb --id seeded-pass --variant make-work-add-up
node cli.mjs perturb --id seeded-pass-2 --variant make-work-add-up --defects remove-install
```

`remove-install` deletes every try/install control and install command, so the scripted probe must stop reporting `pass`. `false-claim` inserts a capability and outcome claim that the facts contradict after the headline; a judge should report a factual error. `bury-headline` moves the headline to the end of the page; the first-screen text no longer contains it, and a first-screen judge should explain the page less well. Seeded captures are excluded from judging and Codex packets unless `--seeded` is passed. Tests check that each defect takes effect and that the probe catches `remove-install`; whether judges catch the other two needs a judged run.

## Visitor responses and human calibration

Invite a visitor to the study URL before showing them the gallery. Assignment is uniform using browser cryptographic randomness. Where the host permits session storage, it persists within that browser tab; restricted hosts record `session_persistence: false`. The gallery and study embed the registry and its hash so they also work without cross-file fetch access. The visitor starts the 20-second exposure after the page is ready. The page is hidden while they answer four comprehension questions; they then explore freely and describe their next action and uncertainties. Consent, timing, interruptions, viewport, assigned revision and whether the page failed to load are included in the downloaded JSON. Refreshing can repeat exposure, so resumed responses are labelled and must be reviewed separately. This is an exploratory study, not a conversion experiment.

The visitor downloads their file or copies the displayed JSON, then shares it with the organiser through an agreed channel. Anonymous Flowershow hosting blocks downloads and browser storage, so the copyable export is the supported route there. There is no submission backend. The visible consent explains possible AI and human analysis and asks visitors to omit identifying or confidential information. The organiser should review files and retain only what is needed before using an external model.

```sh
node cli.mjs judge --run first-pass --visitors /absolute/path/to/response-files
node cli.mjs judge --run first-pass --visitors /absolute/path/to/response-files --live --model YOUR_MODEL
```

Visitor grading checks the study and page hashes and rejects duplicate participant IDs within an import batch. It grades actual answers against reference concepts, with 0–2 anchors, equivalent wording accepted and evidence quoted from the answer. It receives no page text or screenshots with which to manufacture a visitor's understanding. Inspect load failures, exposure interruptions and resumed sessions before interpreting results. Browser-generated metadata and self-reports cannot authenticate a participant or prevent deliberate tampering.

Human labels are a JSON array. IDs are shown in `run.json`; pairwise labels use the A/B presentation order recorded for that judgment. Multiple annotators can label the same item; duplicate entries by the same annotator are rejected.

```json
[
  { "judgment_id": "UUID-FROM-RUN", "criterion_id": "clarity", "label": 2, "annotator": "reviewer-1" }
]
```

```sh
node cli.mjs report --run first-pass --labels /absolute/path/to/human-labels.json
```

Calibration rejects fixture and failed judgments, records exact agreement and preserves disagreements for inspection. Keep human-labelled examples for rubric development separate from a held-out set. A small exact-agreement percentage does not establish population reliability. Real conversion testing additionally needs a defined outcome, randomised traffic allocation, sample-size planning and a stopping rule; those are not supplied by this exploratory lab.

## Reports and publication

```sh
node cli.mjs report --run first-pass
```

Open `.runs/first-pass/report.html` directly, or use `http://127.0.0.1:8765/runs/first-pass/report.html` while the local server runs. Reports show technical findings, source and image hashes, individual criteria, gates, order disagreement and visitor/calibration evidence. Candidate links open the current local files, whether the report is served by the lab or opened directly. The machine-readable run retains the exact captured URLs, which can refer to a temporary server that has since closed. Report screenshots preserve the captured revision independently of current candidate files.

Before publishing, run the repository's website checks. The existing `website/.flowershow` points to `reasoncommons-preview`. Use authenticated Flowershow CLI publication from the repository root:

```sh
python3 scripts/export-website.py
python3 scripts/check-website.py
fl website --yes
```

Only `website/` is published; `.runs/`, visitor answers, facts, prompts and API credentials are outside it. Do not change the live homepage or production root to test the lab. Confirm the returned preview target and compare served page/registry bytes before calling publication verified. Authenticated publication to the existing preview requires CLI login. For a preview without an account, the Flowershow CLI also supports `--anon`; publish a separate staging copy containing only the public lab. Anonymous previews expire after seven days, inject a publication banner and impose `sandbox allow-scripts allow-popups`. The self-contained gallery and copyable study export support those restrictions. Do not point anonymous publication at the existing linked production/preview folder.

## Validation and reasoning

```sh
npm test
```

Tests cover preservation/extraction, export-envelope normalization, grounded judgment evidence, schema and scale rejection, blocking gates, comparison order, source-version-bound visitor import, fixture exclusion from calibration, blind prompt construction, evidence tampering, escaping and the local-server boundary. They also cover checklist grounding and scope, the scripted main-action gate, first-screen evidence limits and checklist calibration. One test launches Google Chrome against fixture pages to check that the probe fails a Claude-only download, passes a visible install command and that each seeded defect takes effect; it is skipped when Chrome is unavailable. Browser verification additionally exercises the gallery, phone layout and visitor download flow.

Approved by David Joseph under `landing-eval-lab-2026-10-19` revision 1, exact reply `accept`, recorded at `2026-10-19T07:23:27Z` in `ltp/rufus-david-collab/reason-commons.yaml`. Implementation bead: `reasoncommons-3si`. The checklist rubric, main-action probe, first-screen task, seeded defects and the results correction were approved under `landing-eval-rubric-2-2026-10-20` revision 1, exact reply `yes i accept these changes`, recorded at `2026-10-20T05:21:50Z`; implementation bead `reasoncommons-zu9`. The lab serves accepted Goal critical success factors `g-e-picturable-product` and `g-e-real-users`; their new comprehension and visitor-validation backlog remains open. No claim or link was endorsed by approving implementation.

## Current preview and verified run

The separate anonymous preview is [the public gallery](https://bp4y64zd-anon.flowershow.me/landing-lab/index.html) and [visitor study](https://bp4y64zd-anon.flowershow.me/landing-lab/study.html), published on 2026-10-19 for seven days (until approximately 2026-10-26). It requires no hosting login. On that host, visitors copy the response JSON and send it to the organiser. The existing `website/.flowershow` target and production site are unchanged. Ownership-claim details are retained locally in `/private/tmp/reasoncommons-fl-anon-result.txt`; treat that file as private.

The initial local evidence is `.runs/landing-baseline/report.html`: 13 captures, 207 readable screenshots, 12 individual fixture judgments and four reversed-order fixture judgments. All fixture scores are null. Fifteen evaluator tests pass, the website checker passes 559 links/assets, and the timed visitor flow was exercised with marked automation answers rather than actual participant evidence. Live OpenAI calls and human calibration remain unverified.

## Fresh native Codex judges

Native Codex contexts can judge the same frozen evidence without an API key. Export a separate packet per fresh context; each packet randomizes individual case order and uses neutral case/image filenames. The original mapping stays in a sibling private file. Give each judge only its packet and output path, with no prior conversation, source identities or other judges’ findings. Require direct inspection of every supplied PNG and strict schema output.

```sh
node cli.mjs codex-export --run landing-baseline --packet scorer-one --batch scoring
node cli.mjs codex-import --run landing-baseline --packet scorer-one --output /absolute/output.json --agent scorer-one
node cli.mjs codex-export --run landing-baseline --packet pair-forward --pair FIRST,SECOND --batch comparison
node cli.mjs codex-export --run landing-baseline --packet pair-reverse --pair FIRST,SECOND --reverse --batch comparison
```

Start a fresh context for each comparison order. Imports check packet/case/image hashes, frozen input identity, case completeness, declared image inspection, exact text grounding, permitted images and schema/gates before appending any judgment. A declared image list does not itself prove visual inspection; the orchestration must retain actual image-tool observations. Failed output can be corrected for validation errors without supplying a desired score; retain the original output for audit. Duplicate agent imports are rejected. Native judgments use `mode: codex`, distinct from API calls and null-score fixtures. They record the agent, packet, raw-output and adapter hashes. Exact serving model snapshots are not exposed by native tooling and must not be invented. Fresh contexts sharing a model can share systematic bias.

For the accepted 24-individual/four-pairwise `landing-rubric-1` study, `publish-results --run landing-baseline --decision /absolute/decision.json` writes the public report and JSON to `website/landing-lab/results/`. The decision file supplies `shortlist`, `shortlist_rule` and `recommendation`, and optionally `recommendation_status` (`provisional` or `withdrawn`) and a `correction` (`date`, `heading`, `text`, scripted `evidence`) shown above the recommendation. On 20 October 2026 its recommendation was withdrawn: Untangle the Problem's only install route, a Download the skill button, calls Claude's artifact runtime and reports that the view cannot save files on any ordinary web host, which the judges could not see because they read text without exercising controls. This command does not yet publish `landing-rubric-2` runs. The public export excludes fixture judgments, private visitor answers and private runtime files. It embeds selected screenshot bytes so inspection works on restrictive static hosts, and shows both individual scores, exact quotations, factual flags and mapped comparison disagreement. It refuses an incomplete study. Opposite orders assigned to different contexts reveal combined order/session instability; they cannot isolate a causal position effect.

Publish this deliberate output through the repository’s normal `website/` → GitHub `main` → Flowershow flow after preview and repository checks. Adding files locally makes them eligible for publishing; the deployment sees the committed revision. The separate anonymous CLI preview is temporary and does not replace the normal deployment path.
