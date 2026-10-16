# Reason Commons

Reason Commons develops ways to use the Logical Thinking Process with AI so that people can think and act better together. It is a collaboration between Rufus Pollock and David Joseph.

Read the public introduction at [reasoncommons.com](https://reasoncommons.com). This repository holds the shared reasoning, project work, installable skills and website; the [Reason Commons application](https://github.com/Promise-Foundation/reason-commons) has its own repository.

## Project map

| Area | Purpose | Start here |
| --- | --- | --- |
| Shared reasoning | Goals, claims, proposed changes, acceptance and reasoning backlog across the project | [Collaboration model](ltp/rufus-david-collab/reason-commons.yaml), Bead `reasoncommons-a4l`, [workflow](docs/beads-reasoning.md) |
| Project working material | Research, experiments, positioning, plans and references | [Docs map](docs/README.md) |
| Installable skills | Skills with their own helpers, fixtures and tests | [Installation and usage](skills/README.md) |
| Runnable applications | Application code, configuration, tests and operating instructions | [Applications](apps/README.md) |
| Public website | Deliberately published pages, static demos and assets | [Public homepage](website/README.md), [publishing and cutover](docs/product/repository-boundaries.md) |
| Shared utilities | Tools crossing area boundaries | [Website exports](scripts/export-website.py), [website checks](scripts/check-website.py), [phone checks](scripts/phone-check.mjs) |

[Motivation](motivation.md) explains the project's purpose and framing. [AGENTS.md](AGENTS.md) defines the contribution rules. [NEXT.md](NEXT.md) remains the single generated work view; its model/source declaration is independent of the conversational collaboration model. GitHub issues hold project-level planning and Beads holds agent-executable work, ownership and handoffs.

## Working here

Resume the collaboration from `bd --sandbox show reasoncommons-a4l`, then read the working YAML and [Beads/reasoning workflow](docs/beads-reasoning.md). Keep one canonical source for each artifact. Project working documents belong in `docs/`; app- and skill-specific helpers, tests and operating instructions stay with their owner. New shared packages or workspace tooling need an actual shared dependency.

Install skills from this repository; `.agents/skills/` and local `.claude/skills/` links still resolve to the canonical top-level `skills/` packages. Use the [gold toy fixture](claim-tree-annotation.md) before real applications.

The website publishes from `website/`. Run `python3 scripts/export-website.py` after changing an explicitly exported source, then `python3 scripts/check-website.py`. Preview with `fl website --yes` against the separate preview site. The production site's Flowershow root must be switched to `/website` in coordination with merging this migration; see the [cutover instructions](docs/product/repository-boundaries.md).
