---
created: 2026-06-06
status: in-progress
---

# Reason Commons

*Structure claims into trees. Map evidence to them. Grow shared understanding — together.*

Public argument is badly structured: claims are vague, debate doesn't accumulate, and evidence rarely maps to the specific point it bears on. What if a claim were instead a tree — broken into the sub-claims it actually depends on, with evidence for, against, or complicating each one attached directly to it? The tree becomes a shared, inspectable scaffold that outlives any one document, so a group reasoning about the same question can see where things stand and build on each other's work instead of talking past each other.

That's what we're exploring here: not one person's argument, but claims and evidence held in common — open to challenge, open to revision. This site is the case for that idea, worked through in examples and demos. There is no app to log into yet; there is a way of thinking, and enough built around it to judge whether it's worth adopting.

<div class="demo-cta">
  <a href="explainers/" class="btn-primary btn-primary-lg">
    Read the series
  </a>
</div>

The three-part series is the way in: why fixes don't stick, why reasoning has to be made visible, and the forty-year-old method that connects the two. Then watch the idea meet a real movement's strategy in [The Forum Doesn't Remember](explainers/second-renaissance/index.html).

**See it working:** [the annotation demo](claim-tree-annotation-demo/index.html) walks the four steps end to end · [the dashboard](dashboard/index.html) opens a live analysis of one organisation's constraints · [Goal Aligner](alignment/index.html) is an experiment in turning a room's scattered goals into one tree everyone signs off on.

**Read next:** [motivation.md](motivation.md) — why this matters, and the problem stated sharply · [AGENTS.md](AGENTS.md) — how the repo is organised, for contributors and AI agents. Planning happens in [GitHub issues](https://github.com/life-itself/reasoncommons/issues).

## About

Reason Commons is a collaboration between **Rufus Pollock** and **David Joseph**. Rufus's thread: issue trees and structured problem-framing — he wanted a tool like this for more than ten years. David's thread: "Abductio," a proposition-decomposition process inside his Promise Protocol framework.

Related: [Promise Foundation](https://www.promise.foundation/how-it-works) · [Provisio](https://praevisio.promise.foundation/) · [issuetrees.com](https://issuetrees.com)

## Working with this repo

The [dashboard](dashboard/index.html) is a read-only viewer for structured analyses of an organisation's goals and constraints — several live behind a project picker. To add an analysis, or to run the dashboard locally against a single project, see [docs/dashboard.md](docs/dashboard.md).

The repository also exposes the `skills/project-ltp/` workflow to Codex through `.agents/skills/project-ltp`. Open the repo in Codex and choose **Project LTP** from the Skills sidebar, or mention `$project-ltp` in a prompt; it may also be selected automatically for requests about analysis trees, project constraints, or reconciling a plan with the code. Restart Codex if the skill doesn't appear after checkout.
