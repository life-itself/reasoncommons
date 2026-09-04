---
title: Claim-tree demo topics
created: 2026-09-05
status: approved for implementation
---

# Claim-tree demo topics

## Goal

Make the public "See it working" demo immediately compelling to the site audience by opening with climate, using rigorous source-to-claim mappings, while preserving remote work and adding AI control as shorter examples on the same page.

## Experience

`claim-tree-annotation-demo/index.html` opens on the climate question, "Can the world switch to clean energy in time?" The four beats remain unchanged: a seed question, a tree that exposes the material distinctions, real sources read against it, and mapped annotations that make the stable-scaffold idea concrete. Each source card links directly to the report it represents, distinguishes quoted findings from editorial explanation, and lands short passages on the most specific relevant claim.

The closing links down to a visible appendix, "Two more questions, same method." AI control and remote-work productivity appear there as compact tree-and-evidence examples rather than alternate page states. This keeps the climate walkthrough continuous, makes every example discoverable by scrolling, and leaves the page meaningful without JavaScript.

## Trees

The climate tree asks what "in time" requires, whether clean supply can scale, whether fossil use outside electricity can fall, and whether a fair transition can be financed and governed. It surfaces solar, wind, grids and storage, nuclear and other firm low-carbon supply, electrification, and international coordination without prematurely endorsing one mix.

The AI tree asks what loss of control would require: dangerous capabilities, a propensity to use them, access and autonomy, and inadequate safeguards. Yudkowsky's maximal warning remains an attributed forecast rather than the root claim, leaving empirical capability evidence and explicit scientific uncertainty visible beside it.

## Sources and annotation semantics

The climate walkthrough uses three IEA reports whose findings match individual branches. The 2023 Net Zero Roadmap supplies scenario-specific figures for available technologies, renewable capacity, electrification and the emissions timetable. Electricity Grids and Secure Energy Transitions quantifies the grid build-out, connection queue and investment bottleneck. Nuclear Power and Secure Energy Transitions supplies a scenario comparison and construction-cost qualification for the firm low-carbon branch. Mappings use `supports`, `complicates`, or `limits` semantics and retain the condition or scenario around every number.

The AI appendix uses METR's 2026 Frontier Risk Report for measured agent capabilities and its overall rogue-deployment assessment, the International AI Safety Report for the present/future distinction and disagreement among experts, and Yudkowsky's Time essay for the strongest catastrophic forecast. These sources are shown as different kinds of evidence rather than blended into a synthetic consensus. The remote-work appendix retains the randomized Ctrip experiment and makes its unusually measurable call-centre setting part of the mapping.

## Implementation and checks

The existing self-contained component keeps one animated climate tree and a static, semantic appendix below the closing. The dynamic topic configuration and fragment routing are removed. A Node verification script asserts the stronger source URLs and figures, appendix anchors, all three examples, and the absence of alternate page-state machinery. `node --check` covers syntax; the preview site is used for visual, mobile and no-JavaScript checks before any live-site integration.
