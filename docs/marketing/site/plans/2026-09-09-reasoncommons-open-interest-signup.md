# Reason Commons Open Interest Signup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let Reason Commons visitors register interest in future updates through the shared CRM route, without starting a newsletter or sending email.

**Architecture:** The landing uses a normal HTML form post to the globally enabled `/interest/v1` Worker route. The Worker records the submission and consent evidence in Twenty; the Worker, not Reason Commons, renders the success page. This supersedes the target-packet plan at `2026-09-08-reasoncommons-future-updates-signup.md` for the current pre-newsletter scope.

**Tech Stack:** Flowershow MDX-compatible Markdown; `config.json`; Life Itself Mailer open-interest client guide.

## Global Constraints

- Exclude `docs/superpowers` from Flowershow publication through `config.json`.
- Use `target=reason-commons` and `project=Reason Commons` consistently.
- Use the visible promise `Get future updates from Reason Commons.` and consent-copy version `2026-09-09`.
- Post only `email`, `target`, `project`, `consent_copy`, `consent_copy_version`, and `source` to `https://mailer.lifeitself.org/interest/v1`.
- Do not add a sender, brand configuration, Resend data, newsletter language, double opt-in, JavaScript, CORS, a redirect, or any tracking/profile fields.
- Do not publish the form until the CRM operator confirms `INTEREST_SIGNUPS_ENABLED=true` is deployed and a malformed-input request returns `400`.

---

### Task 1: Exclude private process material

**Files:** Modify `config.json`.

- [ ] **Step 1: Add the exclusion**

Add `"/docs/superpowers"` directly after `"/docs/plans"` in `contentExclude`.

- [ ] **Step 2: Validate configuration**

Run `node -e "JSON.parse(require('fs').readFileSync('config.json', 'utf8'))"`. Expected: exit status 0.

### Task 2: Confirm the shared endpoint is ready

**Files:** Read `../crm/guides/open-interest-signup.md`.

- [ ] **Step 1: Check the safe malformed-input response**

Post `email=not-an-email`, `target=reason-commons`, `project=Reason Commons`, `consent_copy=Get future updates from Reason Commons.`, and `consent_copy_version=2026-09-09` to `https://mailer.lifeitself.org/interest/v1`.

Expected: `400`; `404` means the CRM operator must enable and deploy the shared route, and no interest record or email is created by this check.

- [ ] **Step 2: Verify one controlled successful submission**

Use an approved seed mailbox and the exact form fields from Task 3. Expected: Worker confirmation page and a Twenty interest record with target `reason-commons`, the given consent copy/version, and canonical landing URL as source; no Resend state or email.

### Task 3: Add the landing form

**Files:** Modify `README.md`; modify `custom.css`.


- [ ] **Step 1: Replace the placeholder with the native form**

Use the exact endpoint and hidden values from Step 1, render the same consent promise as visible text adjacent to the submit button, and retain the existing GitHub and Issues & discussion links beneath the form.

- [ ] **Step 2: Preview the page**

Run `fl . --yes`, then check the label, keyboard interaction, low-volume promise, and form layout. Remember that preview ignores `contentExclude`; verify the exclusion after production deployment.

### Task 4: Record the public change

**Files:** Modify `changelog.md`.

- [ ] **Step 1: Add the release entry after the controlled signup succeeds**

Add a newest-first dated entry saying visitors can register interest in occasional future Reason Commons updates. Do not claim that a newsletter exists or describe CRM implementation details.
