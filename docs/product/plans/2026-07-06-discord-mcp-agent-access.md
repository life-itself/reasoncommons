# Discord MCP Agent Access Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Give Codex and/or Claude controlled access to Discord messages through the existing Discord bot, without building a custom Discord integration from scratch.

**Architecture:** Use an off-the-shelf Discord MCP server as the bridge between the coding agent and Discord. The existing bot token is supplied to the MCP server via environment variables, and the server exposes Discord tools such as guild discovery, channel listing, and message reading to MCP-compatible clients.

**Tech Stack:** Discord bot token, Discord Developer Portal permissions/intents, MCP, Claude Code MCP configuration, npm/npx, likely package `@pasympa/discord-mcp`.

---

## Recommendation

Use `@pasympa/discord-mcp` first.

Reasons:
- It is bot-token based, so it fits the existing Discord bot setup.
- It supports multi-guild Discord access.
- It exposes discovery and message tools, including `discord_read_messages`.
- It can be restricted with `DISCORD_MCP_TOOLSETS` and `DISCORD_ALLOWED_GUILDS`.

Avoid using Discord user tokens or scraping the Discord client. A separate skill found during research, `himself65/finance-skills@discord-reader`, reads Discord Desktop through Chrome DevTools/opencli. That is not the right first choice here because a proper bot already exists.

## Security Boundary

Start with read-focused access only:

```bash
DISCORD_MCP_TOOLSETS=discovery,messages
DISCORD_ALLOWED_GUILDS=YOUR_GUILD_ID
```

Important caveat: the `messages` toolset in `@pasympa/discord-mcp` may include write or destructive message tools, not only read tools. Before relying on it in an unattended workflow, inspect the exposed tools with `/mcp` and avoid granting broader Discord permissions than necessary.

The Discord bot should have only the needed permissions:
- View Channel
- Read Message History
- Send Messages only if agent posting is explicitly wanted later
- Manage Messages only if moderation/delete tools are intentionally needed later

Message body access may require enabling **Message Content Intent** in the Discord Developer Portal. Without it, Discord may return empty message content except for messages involving the bot.

## Task 1: Confirm Bot And Discord Permissions

**Files:**
- No repo files.

**Step 1: Open Discord Developer Portal**

Go to:

```text
https://discord.com/developers/applications
```

Select the existing bot application.

**Step 2: Confirm privileged intents**

In the Bot settings, confirm whether these are enabled:

- Message Content Intent
- Server Members Intent only if member tools are needed

Expected: Message Content Intent is enabled if the agent needs to read ordinary message text.

**Step 3: Confirm server permissions**

In the target Discord server, confirm the bot can see the target channel and read history.

Expected: the bot can access target channels without admin permissions.

## Task 2: Add Discord MCP To Claude Code

**Files:**
- Prefer user-level Claude Code MCP config managed by `claude mcp add`.
- Do not commit bot tokens.

**Step 1: Export the bot token in the shell**

Use the existing bot token:

```bash
export DISCORD_TOKEN="YOUR_BOT_TOKEN"
```

For persistent local use, add it to a private shell profile or secret manager, not to this repo.

**Step 2: Add the MCP server**

Run:

```bash
claude mcp add discord \
  -e DISCORD_TOKEN="$DISCORD_TOKEN" \
  -e DISCORD_MCP_TOOLSETS=discovery,messages \
  -e DISCORD_ALLOWED_GUILDS=YOUR_GUILD_ID \
  -- npx -y @pasympa/discord-mcp
```

Expected: Claude Code records an MCP server named `discord`.

**Step 3: Verify the MCP server is registered**

Run:

```bash
claude mcp list
```

Expected: `discord` appears in the list.

**Step 4: Inspect exposed tools**

Start Claude Code and run:

```text
/mcp
```

Expected: Discord tools are visible. Confirm the exposed surface is acceptable before using the agent on real channels.

## Task 3: Smoke Test Read Access

**Files:**
- No repo files unless logging notes manually.

**Step 1: List Discord guilds**

Ask Claude to list guilds available to the Discord MCP server.

Expected: only the allowed guild is available if `DISCORD_ALLOWED_GUILDS` was set.

**Step 2: List channels**

Ask Claude to list channels in the target guild.

Expected: target channels are visible.

**Step 3: Read recent messages**

Ask Claude to read a small number of recent messages from a known low-risk channel.

Example prompt:

```text
Using the Discord MCP server, read the last 5 messages from #general and summarize them.
```

Expected: message authors, timestamps, and content are available. If content is empty, check Message Content Intent and channel permissions.

## Task 4: Decide Codex Integration Path

**Files:**
- Depends on local Codex MCP configuration support.
- Potentially create or update local Codex config outside this repo.

**Step 1: Check whether this Codex environment can load MCP servers**

Look for local Codex MCP config conventions or available MCP tooling.

Expected: determine whether the same `npx -y @pasympa/discord-mcp` server can be registered directly for Codex.

**Step 2: If Codex MCP is available, mirror the Claude setup**

Use equivalent config:

```json
{
  "mcpServers": {
    "discord": {
      "command": "npx",
      "args": ["-y", "@pasympa/discord-mcp"],
      "env": {
        "DISCORD_TOKEN": "${DISCORD_TOKEN}",
        "DISCORD_MCP_TOOLSETS": "discovery,messages",
        "DISCORD_ALLOWED_GUILDS": "YOUR_GUILD_ID"
      }
    }
  }
}
```

Expected: Codex can call Discord MCP tools.

**Step 3: If Codex MCP is not available, use Claude Code for Discord access first**

Defer custom Codex bridging. Do not build a custom Discord integration unless the existing MCP route fails.

Expected: Claude Code becomes the first working Discord-connected agent path.

## Task 5: Evaluate Alternatives Only If Needed

**Files:**
- No repo files unless documenting findings.

Try these only if `@pasympa/discord-mcp` is unsuitable:

- `discord-ops`: better for project routing, multi-bot setups, notifications, and posting operational updates.
- `discord-mcp`: simpler bot-token MCP package, but research suggested it may be more write/action oriented and less clearly focused on reading history.
- `himself65/finance-skills@discord-reader`: read-only skill using Discord Desktop through CDP/opencli; avoid unless bot-token MCP access is blocked.

## Verification Checklist

- `claude mcp list` shows the Discord MCP server.
- `/mcp` shows Discord tools.
- Guild listing works.
- Channel listing works.
- Reading 5 recent messages from a test channel works.
- The bot cannot access guilds or channels outside the intended scope.
- No bot token has been committed to git.

## Open Questions

- Which Discord guild ID should be allowed?
- Which channels should be readable?
- Should the agent ever send messages, or should this remain read-only?
- Should Discord notes be summarized into repo docs, a database, or only used interactively?

