# Email-only Stay in Touch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the landing page’s “Stay in touch” card contain only the future-updates email signup.

**Architecture:** Remove the existing repository-links paragraph from the footer card in `README.md`. Preserve the signup form, consent promise, and surrounding layout unchanged.

**Tech Stack:** Flowershow MDX-compatible Markdown; shell assertions; Flowershow preview deployment.

## Global Constraints

- Do not change the email form, its hidden consent fields, or its Mailer endpoint.
- Remove both the `GitHub` and `Issues & discussion` calls to action together by removing their shared paragraph.
- Do not line-wrap Markdown prose; keep raw HTML blocks free of blank lines.
- Verify the deployed preview before committing or pushing.

---

### Task 1: Remove the repository-links CTA row

**Files:**
- Modify: `README.md:60`
- Test: landing-page source and preview response

**Interfaces:**
- Consumes: the `.rc-cta-row` paragraph below the signup form.
- Produces: an email-only “Stay in touch” card.

- [x] **Step 1: Write the failing test**

Run an assertion that the finished landing page must not contain either CTA label:

```sh
! rg -n 'GitHub|Issues &amp; discussion' README.md
```

- [x] **Step 2: Run the test to verify it fails**

Run: `! rg -n 'GitHub|Issues &amp; discussion' README.md`

Expected: FAIL because the CTA row is still present.

- [x] **Step 3: Write the minimal implementation**

Delete this complete line from `README.md`:

```html
<p class="rc-cta-row"><a class="btn-secondary" href="https://github.com/life-itself/reasoncommons">GitHub</a> <a class="btn-secondary" href="https://github.com/life-itself/reasoncommons/issues">Issues &amp; discussion</a></p>
```

- [x] **Step 4: Run the source and preview checks**

Run:

```sh
! rg -n 'GitHub|Issues &amp; discussion' README.md
rg -n '<form class="rc-signup"|mailer.lifeitself.org/interest/v1|reason-commons' README.md
```

Publish with `fl . --yes` while temporarily moving the tracked `.agents` symlink outside the repository, then assert the preview response contains the form and neither CTA label.

- [ ] **Step 5: Commit and push**

```sh
git add README.md docs/superpowers/plans/2026-09-09-email-only-stay-in-touch.md
git commit -m "fix: keep stay in touch focused on email"
git push origin main
```
