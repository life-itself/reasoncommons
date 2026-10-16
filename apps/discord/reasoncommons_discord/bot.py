"""Only explicit application commands and a selected-message action."""
import logging

import discord
from discord import app_commands

from .service import Invocation
from .store import atomic_write, digest

LOG = logging.getLogger(__name__)


def invocation(interaction, text, mode="ask", source=None, standing=None):
    if interaction.user.bot:
        raise ValueError("Bots cannot contribute or endorse reasoning.")
    return Invocation(str(interaction.id), interaction.guild_id or 0,
                      interaction.channel_id or 0, str(interaction.user.id),
                      text, mode, source, standing)


async def deliver(interaction, service, request):
    try:
        service.authorize(request)
    except ValueError as exc:
        await interaction.response.send_message(str(exc), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())
        return
    await interaction.response.defer(thinking=True)
    try:
        response = await service.handle(request)
        content = response["text"]
        paths = list(response.get("attachments", []))
        if len(content) > 1900:
            path = service.config.runtime / "artifacts" / ("response-" + digest(request.id)[:20] + ".txt")
            atomic_write(path, content)
            paths.append(str(path))
            content = content[:1100] + "\n\nComplete answer/inspectable fragment attached."
            if response.get("review_token"):
                content += "\nEndorse that exact fragment with /reason-accept fragment:" + response["review_token"]
        files = [discord.File(path) for path in paths]
        try:
            message = await interaction.edit_original_response(
                content=content, attachments=files, allowed_mentions=discord.AllowedMentions.none())
        finally:
            for file in files:
                file.close()
        if response.get("review_token"):
            service.store.publish(response["review_token"], message.jump_url)
    except ValueError as exc:
        await interaction.edit_original_response(content=str(exc)[:1900],
                                                  allowed_mentions=discord.AllowedMentions.none())
    except Exception as exc:
        # Avoid reflecting provider errors or credentials into a channel/log.
        LOG.error("Invocation %s failed (%s)", request.id, type(exc).__name__)
        await interaction.edit_original_response(
            content="This invocation could not finish delivery. The local journal may contain a completed save; inspect it before repeating.",
            allowed_mentions=discord.AllowedMentions.none())


def make_client(service, *, sync_commands=False):
    class Client(discord.Client):
        def __init__(self):
            intents = discord.Intents.none()
            intents.guilds = True
            super().__init__(intents=intents, allowed_mentions=discord.AllowedMentions.none())
            self.tree = app_commands.CommandTree(self)

        async def setup_hook(self):
            if sync_commands:
                await self.tree.sync(guild=discord.Object(id=service.config.guild_id))

    client = Client()
    guild = discord.Object(id=service.config.guild_id)

    @client.tree.command(name="reason", description="Ask, capture a contribution, or review a reasoning fragment", guild=guild)
    @app_commands.choices(mode=[
        app_commands.Choice(name="Ask (read only)", value="ask"),
        app_commands.Choice(name="Capture proposed reasoning", value="capture"),
        app_commands.Choice(name="Review for possible endorsement", value="review"),
    ])
    async def reason(interaction: discord.Interaction, question: str, mode: str = "ask"):
        await deliver(interaction, service, invocation(interaction, question, mode))

    @client.tree.command(name="reason-accept", description="Endorse the exact version of a displayed fragment", guild=guild)
    async def accept(interaction: discord.Interaction, fragment: str):
        await deliver(interaction, service, invocation(interaction, fragment, "accept"))

    @client.tree.command(name="reason-tree", description="View one tree and one reasoning standing as a PNG", guild=guild)
    @app_commands.choices(standing=[
        app_commands.Choice(name="Accepted for now", value="accepted"),
        app_commands.Choice(name="Proposed", value="proposed"),
        app_commands.Choice(name="Disputed", value="disputed"),
    ])
    async def tree(interaction: discord.Interaction, tree: str, standing: str | None = None):
        await deliver(interaction, service, invocation(interaction, tree, "tree", standing=standing))

    @app_commands.context_menu(name="Reason about message")
    async def selected_message(interaction: discord.Interaction, message: discord.Message):
        author = service.config.participants.get(str(message.author.id))
        if message.author.bot or not author or not message.content:
            await interaction.response.send_message(
                "Select a text message from a mapped human participant.", ephemeral=True)
            return
        if message.guild is None or message.guild.id != interaction.guild_id or message.channel.id != interaction.channel_id:
            await interaction.response.send_message("Select a message in this configured channel.", ephemeral=True)
            return
        source = {"by": author, "discord_user_id": str(message.author.id),
                  "message_id": str(message.id), "url": message.jump_url,
                  "text": message.content[:12000]}
        await deliver(interaction, service, invocation(
            interaction, "How does this selected message relate to the saved reasoning?", source=source))

    client.tree.add_command(selected_message, guild=guild)
    return client
