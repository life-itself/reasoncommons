# Reason Commons Discord prototype

A single-host Python adapter gives the canonical [reason-commons skill](../../skills/reason-commons/SKILL.md) an explicit-invocation Discord surface. It uses Claude Agent SDK with API authentication, discord.py, SQLite and a local Mermaid renderer. The full skill package remains the source of reasoning instructions; it is not copied into this application.

This is a locally verified prototype. No live Discord connection, funded model invocation or deployment has been verified. See the [implementation scope and evidence](../../docs/product/plans/2026-10-16-discord-bot.md). The older [MCP access plan](../../docs/product/plans/2026-07-06-discord-mcp-agent-access.md) describes a different direction of integration.

## Commands

| Invocation | Behavior |
| --- | --- |
| `/reason question:… mode:ask` | Answer using the configured reasoning and supplied task snapshot; YAML remains byte-for-byte unchanged. This is the default mode. |
| `/reason question:… mode:capture` | Capture attributed contributions as proposed reasoning, or revise/challenge existing reasoning with its correct standing. No endorsement is inferred. |
| `/reason question:… mode:review` | Display an inspectable fragment with its full statements, standing and version-bound review token. YAML is unchanged. |
| `/reason-accept fragment:review-…` | Endorse the exact displayed fragment as the authenticated participant. The host performs this operation without asking the model to interpret acceptance. |
| `/reason-tree tree:current_reality standing:proposed` | Attach the canonical one-standing diagram as PNG, or a complete text view when rendering is unavailable. Omit standing for accepted, falling back to proposed when no nodes are accepted. |
| Message → Apps → Reason about message | Explain how that explicitly selected message relates to the saved reasoning. Its mapped author and actual message URL accompany the content; this action is read-only. |

Only configured guild/channel IDs and mapped human users are allowed. There is no ordinary-message listener, proactive interjection, automatic conversation ingestion or privileged Message Content Intent. The selected-message action uses the message delivered by Discord's context menu. Bring other context in the invocation itself. Unknown source authors require an explicit identity mapping first.

## Local installation and checks

Install Python 3.11+ (the local checks used 3.12), Git, uv and Node 22+. Work from a checkout containing the complete `skills/reason-commons/` package, not a standalone wheel alone.

```sh
cd apps/discord
uv sync --frozen
npm ci --no-audit --no-fund
uv run --frozen python -m unittest discover -s tests -v
```

The Python tests mock the provider and Discord boundaries and do not require credentials or paid model calls. They also run without the Node renderer. Installing the renderer downloads Puppeteer's browser; missing Chromium/system dependencies result in a labeled text attachment rather than a misleading old image.

Run the repository's existing helper tests from the repository root:

```sh
python3 -m unittest discover -s skills/reason-commons/tests
```

## Configuration

Use [.env.example](.env.example) as a variable reference. Export values from a private shell or secret manager; this app does not automatically load dotenv files. Do not commit credentials or paste them into chat. The live runner requires an explicit API key, model and positive per-invocation budget estimate, with no subscription-login fallback. The SDK budget is an estimate and can be exceeded by the final model request; it is not a hard billing limit. Configure account-side spending limits separately before a funded pilot.

`REASON_COMMONS_STATE` must identify a persistent conversational YAML file explicitly. The project's canonical file is `ltp/rufus-david-collab/reason-commons.yaml`; the app interchange `*.ltp.yaml` is a different format. Start on a private copy of `tests/fixtures/remote-work.yaml` with `alice`/`bob` mappings before selecting real collaboration data. Participant mapping uses Discord IDs, never editable display names. Example: `{"123456789012345678":"david"}`.

`REASON_COMMONS_RUNTIME` holds private persistent SQLite data, task snapshots and generated attachments. The state also uses the skill's sibling hidden history directory (for `reason-commons.yaml`, `.reason-commons/`). A state file binds to one runtime directory so two processes cannot accidentally maintain independent retry ledgers. All processes for that state must share the runtime and state volume on one host.

```sh
uv run --frozen reasoncommons-discord check
uv run --frozen reasoncommons-discord refresh-tasks
```

`check` validates state/configuration and reports the skill package hash without connecting to Discord or the model. `refresh-tasks` explicitly takes a read-only Beads snapshot. It does not edit tasks, update the YAML or silently initialize a database. A missing/invalid snapshot is labeled unavailable; after 24 hours it is labeled stale. Context longer than the supplied bound is explicitly marked truncated. The bot cannot infer current ownership/completion from stale data or YAML alone.

## Live operation after setup is agreed

No registration, paid request or hosting is performed by installation/checks. Before a live pilot, select the guild/channel, map participant IDs, configure API funding and choose a persistent host. Use a dedicated service account and volume. Grant the bot View Channel, Send Messages and Attach Files in the chosen channel, with the applications.commands installation scope; no administrator or moderation permission is needed. Verify the installation against current [Discord documentation](https://docs.discord.com/developers/interactions/application-commands).

```sh
# Explicitly registers commands in the configured guild, then stays connected.
uv run --frozen reasoncommons-discord run --sync-commands

# Subsequent starts reuse the registered commands.
uv run --frozen reasoncommons-discord run
```

Stopping the process stops participation. An external supervisor may restart it with the same state/runtime volumes; none is provisioned here. Model calls occur only after explicit `reason` invocations; tree views and typed endorsement do not call the model. A failed delivery may leave a completed local save, so inspect the journal rather than blindly repeating a capture.

## Persistence, review and recovery

The host stages each model turn in an isolated Git project that links the complete canonical skill, ignores user-level settings and enables only that skill. Tools are restricted to reading that package/staged YAML and, for capture only, editing the staged YAML. Shell tools and other MCP servers are unavailable. The host requires discovery plus an observed read of SKILL.md, records a package hash and discards results if the package changes during the request. These checks demonstrate loading, not semantic obedience; a real model smoke test remains necessary.

Questions/reviews cannot mutate state. Independent guards prevent capture from adding endorsers, changing receipts or project metadata, deleting existing IDs or inventing another person's attribution. Captured contributions retain authenticated Discord references. The canonical helper validates every candidate before persistence.

Updates use a per-state advisory lock, a durable prepared SQLite journal, an immediate external-edit comparison, atomic file replacement, canonical history/view regeneration, then journal completion. A retry of the same interaction returns its saved response without running the model or reapplying contributions. Interrupted saves recover on the next authorized invocation when the file matches either the before/after hash. Bot processes must share the journal; the host supports one filesystem/host, not distributed writes.

**Use one writer for the canonical YAML while the bot runs.** The advisory lock serializes cooperating bot processes. The hash check detects ordinary external edits made while a model turn is running, but no compare-and-rename protocol can exclude an editor that ignores the lock and writes in the final instant. Pause the bot for desktop reasoning sessions or teach other writers to use the same lock.

Reviews are enabled for endorsement only after successful delivery in their configured channel. Tokens expire after 24 hours, are single-use and bind all selected items plus link endpoints. Changed fragment versions and unresolved disputes require fresh review/resolution. Unrelated backlog edits do not invalidate a fragment. Endorsement records the actual person, command options, interaction/user/channel IDs, fragment version and displayed review URL on the affected items. It does not represent unanimity, truth, task completion or project implementation approval.

Back up the YAML, its hidden accepted-history directory and the entire runtime together. SQLite stores request results, pending review versions and the last twelve invocations per channel used for conversational continuity; the full journal remains available locally. It is private operational data and is not automatically committed or sent elsewhere. The configured model receives invocation/source text, bounded history/task context and any reasoning it reads. Treat the runtime as sensitive.

If recovery reports an external conflict, stop the runner, preserve the current YAML and runtime, inspect `requests` in `store.sqlite` (before/after hashes and candidate text), and reconcile deliberately. Do not delete the ledger to force replay. After choosing the intended state, an operator must resolve the prepared entry and regenerate canonical views before restart. There is intentionally no automatic conflict-merging or history-reset command.

Generated attachments have complete statement qualifications and stable node IDs, explicit tree/kind/standing labels, context markers and AND junctions. Images are deterministic renderings of the saved YAML, not generated illustrations. Large/failed renders fall back to complete text. Attachments and journal records currently require operator-managed retention; preserve review/deduplication records when archiving.

## Sources

- [Claude Agent SDK filesystem skills and invocation](https://code.claude.com/docs/en/agent-sdk/skills)
- [SDK Python API and permission callbacks](https://code.claude.com/docs/en/agent-sdk/python)
- [API authentication for shared services](https://code.claude.com/docs/en/legal-and-compliance#authentication-and-credential-use)
- [Discord interactions and deferred responses](https://docs.discord.com/developers/interactions/receiving-and-responding)
- [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)
