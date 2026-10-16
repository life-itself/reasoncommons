# Reason Commons Email Signup Design

## Goal

Let a Reason Commons visitor record interest in occasional future project updates from the landing page, using the shared Life Itself open-interest service while presenting Reason Commons as the subscriber-facing project.

## Scope

The CRM repository's shared `POST /interest/v1` route records open interest in Twenty. It has no per-project registration, brand, sender, Resend configuration, target packet, or double opt-in. Its operator enables the route once with the shared Twenty credential and object mapping; Reason Commons then uses the stable lower-case target slug `reason-commons`. `reasoncommons@lifeitself.org` remains the intended sender for a later newsletter, but this form sends no email.

The Reason Commons landing page will replace its email-capture placeholder with a JSX-compatible native HTML form (camel-case React attributes and self-closing `<input />` elements). The form posts to `https://mailer.lifeitself.org/interest/v1` and sends only the visitor's email, `target=reason-commons`, `project=Reason Commons`, the visible consent promise `Get future updates from Reason Commons.`, consent-copy version `2026-09-09`, and the landing's canonical URL as `source`. It will sit in the existing “Stay in touch” section, retain the low-volume promise, use the site's existing button styling, and use a normal browser form post with no JavaScript, CORS, or redirect. The Worker will show its own confirmation page after a successful submission.

The CRM client guide is the complete agent and human handoff for this form. The form's target, project, consent copy, and consent-copy version are recorded as consent evidence in Twenty; it does not create a Resend audience or an email-delivery entitlement.

## Data flow

1. A visitor enters an email address on reasoncommons.com and submits the form.
2. The browser posts the documented interest fields to `/interest/v1`.
3. The Worker writes a Reason Commons interest and consent event to Twenty, with the visible consent copy, version, and source evidence.
4. The Worker displays its confirmation page. No email is sent and no Resend state is created.

## Error handling and safety

The external form will send no extra tracking or profile fields and must treat an error page or network failure as a recoverable failure without exposing provider or CRM details. Before public release, the CRM operator must confirm that the globally enabled route is deployed; a malformed-input request must return `400`, not create an interest record, and a designated seed mailbox must prove the Twenty record. Tests must cover malformed input, successful interest recording, and unavailable-Twenty retry behaviour.

## Non-goals

This work does not create a newsletter, broadcast authoring/sending workflow, Resend audience, brand configuration, double opt-in flow, account/login functionality, or browser-side tracking.
