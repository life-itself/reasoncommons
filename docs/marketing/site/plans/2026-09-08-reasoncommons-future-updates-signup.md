# Reason Commons Future Updates Signup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a safe, low-friction Reason Commons future-updates signup once the CRM operator has released its target packet.

**Architecture:** Reason Commons provides a semantic native HTML form and a same-origin thank-you page. The CRM service is the consent, delivery-eligibility, and suppression authority; its released target packet supplies the exact endpoint, target key, consent copy, privacy-policy reference, acknowledgement policy, and support route. The form cannot be deployed before that packet exists.

**Tech Stack:** Flowershow Markdown and raw HTML; `config.json`; Life Itself Mailer external signup form contract.

## Global Constraints

- Exclude `docs/superpowers` from Flowershow publication through `config.json`.
- The public collection class is `future-notifications`; opt-in is single opt-in.
- The configured sender is `reasoncommons@lifeitself.org` and the subscriber-facing project name is Reason Commons.
- Use a standard browser form post; do not add JavaScript, `fetch`, CORS, Resend, Twenty, D1 access, browser-supplied consent metadata, or tracking fields.
- Submit only `email`, the operator-issued `target`, and the optional same-origin `redirect` defined by the released packet.
- Do not publish, advertise, or submit the form until the CRM operator has released a packet with `releaseState: released`.

---

### Task 1: Keep agent process material out of the published site

**Files:** Modify `config.json`.

**Interfaces:** Consumes Flowershow's `contentExclude` array. Produces a site that excludes `docs/superpowers`.

- [ ] **Step 1: Add the process-document exclusion**

Add `"/docs/superpowers"` as a distinct `contentExclude` entry directly after `"/docs/plans"`.

- [ ] **Step 2: Validate the configuration syntax**

Run `node -e "JSON.parse(require('fs').readFileSync('config.json', 'utf8'))"`. Expected: exit status 0.

- [ ] **Step 3: Preview the exclusion**

Run `fl . --yes`. Expected: production must exclude `/docs/superpowers/`; the repository notes that preview ignores `contentExclude`, so do not treat preview visibility as a failure.

- [ ] **Step 4: Commit**

Commit `config.json` with message `chore: exclude agent process docs from site`.

### Task 2: Obtain and verify the CRM release packet

**Files:** Read `../crm/ref/external-signup-form-contract.md`.

**Interfaces:** Consumes the CRM operator's released Reason Commons target packet. Produces exact, non-secret form values: `endpoint`, `target`, `siteOrigin`, `consentCopy`, `consentCopyVersion`, `privacyPolicy`, `acknowledgementPolicy`, and `supportOwner`.

- [ ] **Step 1: Register the target with the CRM operator**

Provide the fixed decisions: project name `Reason Commons`; sender `reasoncommons@lifeitself.org`; `formClass: future-notifications`; `optInMode: single-opt-in`; and `siteOrigin: https://reasoncommons.com`. The operator must provide the approved consent copy, consent-copy version, privacy-policy reference, acknowledgement policy, support owner, endpoint, and target key.

- [ ] **Step 2: Check the release gate**

Confirm that `releaseState` equals `released`, `permittedFields` contains `email` and optionally `redirect`, and `siteOrigin` equals `https://reasoncommons.com` exactly.

- [ ] **Step 3: Check operator test evidence**

Require evidence for the approved target, default acknowledgement page, valid same-origin redirect, invalid redirect, retry with the same idempotency key, later re-consent with a new key, suppression, and acknowledgement UI.

### Task 3: Add the landing-page form and success destination

**Files:** Modify `README.md`; create `thanks/index.md`; create a focused verification script.

**Interfaces:** Consumes the released packet values from Task 2. Produces a native form that submits the exact allowed fields and a thank-you page eligible for the packet's same-origin redirect.

- [ ] **Step 1: Write the failing static form assertion**

Require the Stay in touch form to have a labelled `email` field with `autocomplete="email"` and `required`, one hidden `target` field containing the issued target key, and one hidden `redirect` field pointing to `https://reasoncommons.com/thanks/`.

- [ ] **Step 2: Run the assertion to verify it fails**

Expected: failure because the current landing has only the email-capture placeholder.

- [ ] **Step 3: Replace the landing placeholder with the released form**

Add a `method="post"` form whose action, target key, and nearby consent copy exactly match the released packet. Retain GitHub and Issues & discussion below it. Do not add fields, client code, or an unapproved privacy claim.

- [ ] **Step 4: Add the same-origin thank-you page**

Create `thanks/index.md` with an acknowledgement matching the issued acknowledgement policy. It may say that the visitor has signed up for Reason Commons updates, but must not claim confirmation, CRM completion, provider eligibility, or delivery.

- [ ] **Step 5: Run the assertion to verify it passes**

Expected: pass.

- [ ] **Step 6: Preview and test the real target**

Publish to the separate Flowershow preview with `fl . --yes`. Check label, keyboard use, layout, consent copy, and successful same-origin redirect. Submit only an approved seed mailbox, then confirm the acknowledgement and the operator's recorded consent/suppression behavior.

- [ ] **Step 7: Commit**

Commit the landing page, thank-you page, and verification script with message `feat: add reasoncommons updates signup`.

### Task 4: Record the shipped public change

**Files:** Modify `changelog.md`.

- [ ] **Step 1: Add the changelog entry**

Add a newest-first dated entry describing the low-volume Reason Commons signup, without documenting internal provider, database, or CRM implementation details.

- [ ] **Step 2: Commit**

Commit `changelog.md` with message `docs: record reasoncommons updates signup`.
