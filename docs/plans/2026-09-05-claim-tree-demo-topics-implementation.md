# Claim-tree demo topic variants Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a climate-first claim-tree annotation demo with rigorous source mappings and visible AI and remote-work appendix examples.

**Architecture:** Keep the standalone HTML component and its current animation runtime for the climate walkthrough. Replace the generic climate card with several source-specific cards and a fixed flights array, remove URL-selected topic state, and append static tree-and-evidence examples for AI and remote work below the closing.

**Tech Stack:** Self-contained HTML, inline JavaScript, Node.js `assert` verification.

## Global Constraints

The default URL is climate and remains readable without JavaScript.
All three topic variants use the existing four-beat narrative and hover/flight interaction.
Every source card has a direct, external source link; source excerpts are short and clearly attributed.
The public walkthrough is climate; AI and remote work are anchored appendix sections in the same document.
Markdown remains unwrapped outside code blocks.

## Review revision

Tasks 1–4 below record the committed first pass. User review supersedes its URL variants and generic IPCC mapping. The remaining work is to replace that implementation with the evidence-rich, single-page design in Tasks 5–7.

---

### Task 1: Create a static regression check

**Files:**
- Create: `claim-tree-annotation-demo/verify.mjs`
- Test: `claim-tree-annotation-demo/verify.mjs`

**Interfaces:**
- Consumes: the UTF-8 contents of `claim-tree-annotation-demo/index.html`.
- Produces: exit status 0 only when climate is the default and both alternate topic configurations, source URLs, and annotations exist.

- [ ] **Step 1: Write the failing test**

```js
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const page = readFileSync(new URL('./index.html', import.meta.url), 'utf8');
assert.match(page, /Can the world switch to clean energy in time\?/);
assert.match(page, /ai:/);
assert.match(page, /remote-work:/);
assert.match(page, /https:\/\/www\.ipcc\.ch\/report\/ar6\/wg3\/chapter\/chapter-6\//);
assert.match(page, /https:\/\/internationalaisafetyreport\.org\/publication\/international-ai-safety-report-2025/);
assert.match(page, /https:\/\/time\.com\/6266923\/ai-eliezer-yudkowsky-open-letter-not-enough\//);
assert.match(page, /topic === 'ai'/);
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `node claim-tree-annotation-demo/verify.mjs`

Expected: `AssertionError` because the climate topic configuration is absent.

- [ ] **Step 3: Keep the test focused on externally meaningful content**

Add assertions that the page contains `?topic=remote-work`, a `sourceUrl` field, and one support (`key: 's'`) and one complication (`key: 'c'`) annotation in the climate topic. Do not assert CSS or exact line positions.

- [ ] **Step 4: Commit the red test**

```bash
git add claim-tree-annotation-demo/verify.mjs
git commit -m "test: define claim-tree demo topic variants"
```

### Task 2: Make climate the no-JavaScript default

**Files:**
- Modify: `claim-tree-annotation-demo/index.html:116-355`

**Interfaces:**
- Consumes: the climate question, tree labels, source link and short IPCC fragments specified in `2026-09-05-claim-tree-demo-topics-design.md`.
- Produces: climate content in the seed question, both rendered trees and source card before the component script runs.

- [ ] **Step 1: Replace the visible remote-work seed and both tree copies**

Set the root text to `Can the world switch to clean energy in time?`. Use the parent labels `What does “in time” require?`, `Can clean supply scale?`, `Can fossil use fall beyond electricity?`, and `Can the transition be fair and governable?`; use concrete leaves for emissions pace, remaining warming risk, solar/wind plus grids/storage, nuclear and other firm low-carbon supply, electrification, alternative fuels, finance/materials, and coordination/energy access.

- [ ] **Step 2: Replace the default source card with a linked IPCC extract**

Use the IPCC AR6 WGIII Chapter 6 Energy Systems URL. Mark three short fragments: systems integration can facilitate variable renewable energy; debates continue about wind and solar shares; and nuclear can contribute to low-carbon systems. Map them to supply, supply, and firm low-carbon nodes, respectively.

- [ ] **Step 3: Add a small non-JavaScript variant note below the source card**

Include links to `?topic=ai` and `?topic=remote-work`, with climate named as the default. Do not add a new navigation surface.

- [ ] **Step 4: Run the red test**

Run: `node claim-tree-annotation-demo/verify.mjs`

Expected: it continues to fail because the alternate topic configuration and configuration-driven flights do not exist.

### Task 3: Add URL-selected content and annotation mappings

**Files:**
- Modify: `claim-tree-annotation-demo/index.html:390-560`

**Interfaces:**
- Consumes: `URLSearchParams`, `topicData[topic]`, and rendered elements `[data-topic-question]`, `[data-node]`, and `[data-tree-doc]`.
- Produces: the selected topic’s content and `flights` array before reveal, animation and hover listeners initialise.

- [ ] **Step 1: Define the topic data contract**

Create a `topicData` object whose `climate`, `ai`, and `remote-work` entries each contain `question`, `nodes`, `sourceHtml`, `sourceUrl`, and `flights`. Let missing or unknown query values select `climate`.

- [ ] **Step 2: Configure the climate topic**

Use the default climate labels and IPCC source card. Its flights attach a support fragment to `supply-grid`, a complication fragment to `supply-renewables`, and a limit/broadening fragment to `supply-firm`.

- [ ] **Step 3: Configure the AI topic**

Set the question to `Can humans stay in control of advanced AI?`. Provide nodes for failure modes, technical safeguards, institutions and competition, and the pace of capability progress. The source card links to the International AI Safety Report 2025 and Yudkowsky’s Time essay; it maps the report’s current-capability qualification as a complication and Yudkowsky’s warning as a clearly attributed limiting/warning annotation.

- [ ] **Step 4: Configure the preserved remote-work topic**

Restore the existing question, tree labels, Ctrip source card and five flights exactly enough to retain the existing illustrated argument.

- [ ] **Step 5: Apply data before runtime lookup**

At the start of `componentDidMount`, select the topic, update the document title, seed question and both label copies, replace `data-tree-doc` content, then assign `const flights = selected.flights`. The existing reveal, flight and hover code must continue to consume `flights` unchanged.

- [ ] **Step 6: Run checks and commit**

Run: `node claim-tree-annotation-demo/verify.mjs && node --check claim-tree-annotation-demo/support.js`

Expected: both commands exit 0.

```bash
git add claim-tree-annotation-demo/index.html claim-tree-annotation-demo/verify.mjs
git commit -m "feat: add climate and AI claim-tree demos"
```

### Task 4: Inspect the published preview and record the shipped change

**Files:**
- Modify: `changelog.md`

**Interfaces:**
- Consumes: preview URLs for the default, `?topic=ai`, and `?topic=remote-work` routes.
- Produces: a reader-facing changelog entry only after the preview contains the expected HTML and the asset is current.

- [ ] **Step 1: Publish the worktree to the existing Flowershow preview**

Move the tracked `.agents` symlink outside the worktree temporarily, run `fl . --yes`, then restore it. Do not push `main` merely to inspect the page.

- [ ] **Step 2: Check the default and alternate routes**

Fetch `claim-tree-annotation-demo/index.html`, `claim-tree-annotation-demo/index.html?topic=ai`, and `claim-tree-annotation-demo/index.html?topic=remote-work`. Confirm the response does not escape HTML markup and the page contains the default climate wording and alternate route links.

- [ ] **Step 3: Add and verify the changelog entry**

Add a dated entry explaining that the live demo now opens on a climate transition question and offers AI-control and remote-work examples. Run `node claim-tree-annotation-demo/verify.mjs`, `git diff --check`, and `git status --short` before committing.

- [ ] **Step 4: Commit the changelog**

```bash
git add changelog.md
git commit -m "docs: record claim-tree demo update"
```

### Task 5: Define the reviewed evidence contract

**Files:**
- Modify: `claim-tree-annotation-demo/verify.mjs`

- [ ] Assert direct links to the IEA Net Zero Roadmap, electricity-grids report and nuclear report, plus their distinctive quantitative findings.
- [ ] Assert a `#more-examples` link and appendix containing METR 2026, the International AI Safety Report, Yudkowsky's essay and the Ctrip experiment.
- [ ] Assert that `topicData`, `URLSearchParams` and `#topic=` routing are absent.
- [ ] Run the test and confirm it fails before changing the page.

### Task 6: Implement the evidence-rich single page

**Files:**
- Modify: `claim-tree-annotation-demo/index.html`

- [ ] Replace the generic IPCC source card with three compact IEA source cards. Preserve the scenario and conditional context around short highlighted findings and map every passage to a specific climate leaf.
- [ ] Replace topic configuration with a fixed climate flights array and keep the existing animation and hover tracing intact.
- [ ] Link the closing to `#more-examples` and append compact AI and remote-work examples with visible mini trees, source passages, relation labels and direct source links.
- [ ] Check responsive layout and no-JavaScript readability.

### Task 7: Verify, preview and record the revision

**Files:**
- Modify: `changelog.md`

- [ ] Run the focused verification, component syntax compilation, project tests and `git diff --check`.
- [ ] Publish to the Flowershow preview using the repository's `.agents` workaround, then inspect desktop and phone-sized captures plus fetched markup.
- [ ] Update the changelog to describe the evidence-rich climate walkthrough and on-page appendix accurately, then commit the reviewed revision.
