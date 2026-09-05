# Reason Commons Email Signup Design

## Goal

Let a Reason Commons visitor subscribe to occasional project updates from the landing page, using the shared Life Itself Mailer while presenting Reason Commons as the subscriber-facing publication.

## Scope

The CRM repository will configure a reusable `life-itself` brand in the existing mailer Worker and a `reasoncommons-updates` list under that brand. The list will use double opt-in, record its own Twenty source, and send from `Reason Commons <updates@lifeitself.org>`, which must already be authorised in Resend. The existing deployed Worker, D1 database, secret names, and endpoint remain unchanged.

The Reason Commons landing page will replace its email-capture placeholder with a native HTML form that posts to the Worker `subscribe` endpoint. It will send the visitor's email, the `reasoncommons-updates` subscription ID, and a redirect back to the Reason Commons site. The form will sit in the existing “Stay in touch” section, retain the low-volume promise, and use the site's existing button styling. The Worker will display its branded success/confirmation state if the redirect is not accepted.

The CRM documentation will add a concise site-signup onboarding route for both humans and agents. It will state that a shared Life Itself brand is infrastructure, while each site list supplies the public title, sender, welcome copy, consent setting, and Twenty source; it will link directly to the configuration files, verification commands, and form shape.

## Data flow

1. A visitor enters an email address on reasoncommons.com and submits the form.
2. The browser posts `email`, `subscription=reasoncommons-updates`, and an allowed Reason Commons `redirect` URL to the existing Worker.
3. The Worker records the pending subscription, emails a confirmation link, and applies the configured Twenty source after confirmation.
4. After confirmation, the visitor is an active subscriber of Reason Commons updates and can unsubscribe through the Worker’s signed link.

## Error handling and safety

The existing Worker continues to validate malformed email input and reject redirects whose origins have not been allow-listed. The new list is double opt-in, so entering an address alone does not subscribe someone. Before release, tests must cover the new configuration and subscription path; deployment must use the documented malformed-input smoke check and a designated seed mailbox for confirmation and unsubscribe verification.

## Non-goals

This work does not create a broadcast authoring/sending workflow, alter the Worker’s infrastructure, replace its database schema, or add account/login functionality to Reason Commons.
