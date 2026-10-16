# On-demand Discord reasoning prototype

David accepted `change-discord-bot-2026-10-16` revision 1 with the exact reply “i accept”. Its scope/path receipt is in the canonical collaboration YAML. This plan describes that accepted implementation, not a new authorization for live Discord operation, spending or deployment.

## Purpose and reasoning

Give the existing collaborators another surface for their saved reasoning: where are we, what should we examine next, what objections remain, and how does a selected channel contribution relate? This serves Future Reality injection `f-e-use-while-building` (accepted): “Rufus and David use the tool on their real work now while they keep building and redesigning it.” A Discord pilot may help that use; implementation alone does not establish the benefit.

No node or link changes are needed. The same accepted injection owns `verify_discord_adapter` and `evaluate_discord_pilot` backlog, linked to implementation bead `reasoncommons-oqf`. Existing collaboration priority `reasoncommons-5lo`, all reasoning standings and earlier approval receipts remain unchanged.

## Bounded implementation

Use one Python/discord.py gateway process with explicit slash commands and a selected-message context action. Claude Agent SDK loads the full canonical reason-commons package from the filesystem into an isolated project. No external MCP server, second provider integration, interactive viewer or hosted Activity is introduced.

The transport supplies authenticated Discord identity, invocation/source references and configured state. A transport-independent service stages edits, validates them with the canonical helper and enforces read-only/attribution/endorsement boundaries. SQLite persists conversation context, review versions and a before/after save journal. Per-state locking, single-runtime ownership, hash comparison and recovery protect sequential state updates. The operating assumption is a single writer/host; uncooperative external editors must be paused.

Questions and reviews do not alter YAML. Capture may add proposed reasoning or revise/challenge existing reasoning; it cannot endorse. Review expands a named fragment, retaining all endpoint conditions, full qualifications and an inspectable version. A typed acceptance command, tied to successful display and that exact version, applies endorsement deterministically with person/source evidence. Project implementation approval remains a separate protocol.

Tree attachments use the canonical one-standing Mermaid generator, a pinned local renderer and actual state. They preserve explicit tree/kind/standing metadata, IDs, context, AND conditions and qualifications; text is the labeled fallback. Beads is an explicit refreshed snapshot, not inferred current truth from YAML or task completion.

## Verification and delivery

Use the remote-work fixture adapted from `claim-tree-annotation.md` before real data. Local tests cover access, invocation-only transport, grounding references, attribution, capture restrictions, version-bound endorsement, pending review publication, restart continuity, duplicate/concurrent invocations, interrupted saves, external conflicts, permission callbacks and failed skill loading. Render and inspect the actual toy PNG separately. Existing reasoning helpers and PR scope/receipt checks must pass.

Deliver the source, dependency locks, tests and operating instructions on a reviewable branch/PR. Live model quality, actual Discord behavior, funded API use, persistent hosting and real collaboration usefulness remain unverified. The API budget estimate is not a hard billing cap. See [app operating instructions](../../../apps/discord/README.md) for configuration, recovery, privacy and the single-writer limitation.

Local evidence: 47 application tests and all 77 existing helper tests pass. A real Mermaid PNG of the remote-work fixture was rendered and visually inspected for qualifications, IDs, standing/context labels and the AND junction. The CLI check and explicit Beads snapshot refresh were exercised without credentials or model calls. The installed/locked versions are Claude Agent SDK 0.2.168, discord.py 2.7.1 and Mermaid CLI 11.17.0. Existing accepted-history revisions 1 and 2 were copied from the prior checkout only after comparing the latest accepted projection; validation still reports revision 2 with no accepted reasoning changes.
