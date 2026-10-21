# Retire outdated framing and app-era tooling

David accepted `change-retire-outdated-framing-2026-10-21` revision 1 with the reply “accept these changes”. The receipt, with its scope and approved paths, is in [the collaboration YAML](../../../ltp/rufus-david-collab/reason-commons.yaml). Work is tracked in Beads epic `reasoncommons-ffm`: `reasoncommons-ffm.1` for PR A and `reasoncommons-ffm.2` for PR B.

## Why

An audit on 2026-10-21 found the repository still presenting Reason Commons through framing the project no longer uses. Two decisions had landed without a sweep: the 2026-09-01 naming memo and Rufus's 2026-10-17 call that the app is retired and the offer is skills plus integrations. David then corrected the framing itself:

1. **Words are learned from use.** Settling on "tree of change / tree of action" puts the cart before the horse. The domain language should reflect what proves useful, and that is learned by using the tool.
2. **Lead with what it changes.** Issue trees are deprecated. The Logical Thinking Process is part of what makes Reason Commons work underneath, but it is how the sausage is made, not the sausage. "A tool to decompose a top-level claim" sells the mechanism, not the transformation or the expected benefit.
3. **Abductio and Promise Protocol are not part of Reason Commons.** Presenting them prominently is a mistake.

These are David's positions and remain proposed until Rufus responds. The accepted top goal `g-e-ltp-used-in-world` is deliberately unchanged.

## Reasoning served

- Current Reality · Undesirable effect · Accepted — `r-e-no-user-picture`: Rufus and David cannot yet show an average user a clear picture of how they would use the product. It feeds Goal · Critical success factor · Accepted — `g-e-picturable-product`.
- Current Reality · Observation · Proposed — `r-e-repo-feels-scattered`, for the tooling and clutter removal.
- Added, all proposed: Goal · Necessary condition `g-e-language-follows-use` (necessary for `g-e-picturable-product`), Current Reality · Cause `r-e-retired-framing-shown` (contributes to `r-e-no-user-picture`) and Future Reality · Injection `f-e-present-benefit-first`, which addresses it.

## How each file is treated

| Kind of file | Treatment |
|---|---|
| Describes the project now: agent docs, READMEs, current site pages, glossary, skill docs | Rewrite |
| Dated record: changelog, blog posts, talk material, landing-lab results, red-team critiques, dated plans, the friction log, the YAML's acceptance receipts | Leave the wording alone |
| Depends on something that is gone: the app's interchange format, its dashboard tooling, retired skills | Delete; Git history keeps it |

Kept deliberately: the `claim-tree-annotation.md` fixture (internal test data), `ltp/rufus-david-collab/rufus-david-collab.ltp.yaml` (the collaboration YAML's conversion baseline), the `/ltp` Guide and glossary (where the method is explained), Second Renaissance as the main example, the `/demos` mockups and the Flowershow site ID `ltp-issue-trees`.

## PR A — David's side

1. **Agent docs.** AGENTS.md describes what Reason Commons is for, with no tagline, and gains a "How we present Reason Commons" convention. The README intro and `motivation.md` follow suit.
2. **Retire app-era tooling.** Delete `ltp-project`, `ltp-visualize` and their `.agents` links, NEXT.md and the app-format model it was read from, and `docs/theory/` (moved to David's own repository). Update `skills/README.md`, the `reason-commons` skill description, the docs map and the checker's skill and NEXT.md rules. Close beads `vc0`, `db0` and `1ch`.
3. **Live site, small fixes.** The site title becomes "Reason Commons". Homepage, About, people pages and glossary drop the fixed tree vocabulary, the issue-tree, Abductio and Promise Protocol material, the LTP card and the demo and dashboard cards. The demo and dashboard stay published until PR B. The fixture stops being exported to the site.
4. **Guard.** `scripts/check-website.py` fails on the retired terms (issue tree, Abductio, Promise Protocol) outside dated folders.

## PR B — for Rufus's review

1. Reopen the naming memo's decision, and bring `brand.md`, `pages.md` and `ia.md` into line with the three corrections. Add a decision-log entry to the redesign plan.
2. Replace the dashboard and the claim-tree demo with short retired notices at their old URLs, so changelog and shared links still land somewhere. Remove their links from `/demos` and the explainers, and close bead `9zv`.

PR B changes Rufus's IA plan, which keeps both pages, so it merges only on his approval. His response is tracked on the backlog item for `f-e-present-benefit-first` and in bead `reasoncommons-ffm.2`.

## Open

- How this repository's `reason-commons` skill relates to the `reason-commons-contribute` plugin from `life-itself/reason-commons-tui`: a separate experiment for now, recorded as backlog on `g-e-form-follows-use`.
- Front-facing vocabulary stays provisional and is revised from what proves useful in use.
