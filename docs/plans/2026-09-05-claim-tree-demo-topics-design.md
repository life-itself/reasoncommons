---
title: Claim-tree demo topics
created: 2026-09-05
status: approved for implementation
---

# Claim-tree demo topics

## Goal

Make the public "See it working" demo immediately compelling to the site audience by opening with climate, while preserving remote work and adding an AI-control version that demonstrate the same four-step cumulative-annotation interaction.

## Experience

`claim-tree-annotation-demo/index.html` opens on the climate question, "Can the world switch to clean energy in time?" The four beats remain unchanged: a seed question, a tree that exposes the material distinctions, a real source read against it, and mapped annotations that make the stable-scaffold idea concrete. The source card links directly to the source it represents.

The URL parameter selects the other examples without duplicating the page runtime: `?topic=ai` asks "Can humans stay in control of advanced AI?" and `?topic=remote-work` retains the current question and Ctrip example. The default source HTML is the climate version, so the published page remains meaningful without JavaScript.

## Trees

The climate tree asks what "in time" requires, whether clean supply can scale, whether fossil use outside electricity can fall, and whether a fair transition can be financed and governed. It surfaces solar, wind, grids and storage, nuclear and other firm low-carbon supply, electrification, and international coordination without prematurely endorsing one mix.

The AI tree asks what loss of control would mean, whether technical safeguards can work, whether institutions can prevent unsafe deployment, and whether capabilities may outpace safeguards. It uses Yudkowsky's maximal warning as an annotation rather than as the root claim, leaving room for evidence to support, qualify, or challenge it.

## Sources and annotation semantics

The climate card is a short, linked extract from IPCC AR6 WGIII Chapter 6, Energy Systems. Its three marked fragments respectively support systems integration, complicate a one-size-fits-all renewable answer, and broaden the supply branch to include nuclear or other low-carbon sources. The AI card links to the International AI Safety Report and to Yudkowsky's Time essay; its fragments distinguish a reported risk category from a strongly contested judgement about severity and governance.

## Implementation and checks

The existing self-contained component gets a small topic configuration layer that replaces the displayed question, tree labels, source card and annotation mapping before its animation initialises. A Node verification script asserts the default climate content, both URL-selectable alternatives, direct source links, and the expected annotation mappings. `node --check` covers syntax; the preview site is used for a visual and no-JavaScript check before any live-site integration.
