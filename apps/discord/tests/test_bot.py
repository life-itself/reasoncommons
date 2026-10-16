from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, Mock

from reasoncommons_discord.bot import deliver, invocation, make_client


def interaction():
    return SimpleNamespace(
        id=123, guild_id=10, channel_id=20, user=SimpleNamespace(id=100, bot=False),
        response=SimpleNamespace(defer=AsyncMock(), send_message=AsyncMock()),
        edit_original_response=AsyncMock(return_value=SimpleNamespace(jump_url="https://discord.com/channels/10/20/123")),
    )


class BotTests(unittest.IsolatedAsyncioTestCase):
    async def test_denied_invocation_does_not_defer_or_run_agent(self):
        current = interaction()
        service = SimpleNamespace(authorize=Mock(side_effect=ValueError("unmapped")), handle=AsyncMock())
        await deliver(current, service, invocation(current, "question"))
        current.response.send_message.assert_awaited_once()
        current.response.defer.assert_not_awaited()
        service.handle.assert_not_awaited()

    async def test_one_response_edit_and_mentions_disabled(self):
        current = interaction()
        service = SimpleNamespace(authorize=Mock(), handle=AsyncMock(return_value={"text": "@everyone test", "attachments": []}))
        await deliver(current, service, invocation(current, "question"))
        current.response.defer.assert_awaited_once()
        args = current.edit_original_response.call_args.kwargs
        self.assertFalse(args["allowed_mentions"].everyone)
        self.assertFalse(args["allowed_mentions"].users)
        current.edit_original_response.assert_awaited_once()

    async def test_review_not_marked_published_until_successful_delivery(self):
        current = interaction()
        store = SimpleNamespace(publish=Mock())
        service = SimpleNamespace(authorize=Mock(), handle=AsyncMock(return_value={
            "text": "Inspectable fragment", "review_token": "review-123", "attachments": []}), store=store)
        current.edit_original_response.side_effect = [RuntimeError("delivery failure"), None]
        await deliver(current, service, invocation(current, "question", "review"))
        store.publish.assert_not_called()

    async def test_long_review_is_attached_in_full_before_acceptance_enabled(self):
        with tempfile.TemporaryDirectory() as root:
            current = interaction()
            text = "Full qualification. " * 300
            store = SimpleNamespace(publish=Mock())
            service = SimpleNamespace(authorize=Mock(), handle=AsyncMock(return_value={
                "text": text, "review_token": "review-123", "attachments": []}),
                store=store, config=SimpleNamespace(runtime=Path(root)))
            await deliver(current, service, invocation(current, "question", "review"))
            self.assertEqual(next((Path(root) / "artifacts").glob("*.txt")).read_text(), text)
            self.assertLessEqual(len(current.edit_original_response.call_args.kwargs["content"]), 2000)
            store.publish.assert_called_once()

    async def test_only_explicit_commands_and_no_message_content_intent(self):
        service = SimpleNamespace(config=SimpleNamespace(guild_id=10))
        client = make_client(service)
        self.assertFalse(client.intents.message_content)
        self.assertFalse(hasattr(client, "on_message"))
        commands = client.tree.get_commands(guild=SimpleNamespace(id=10))
        self.assertEqual({c.name for c in commands}, {"reason", "reason-accept", "reason-tree", "Reason about message"})
        await client.close()

    def test_bot_identity_is_rejected(self):
        current = interaction()
        current.user.bot = True
        with self.assertRaisesRegex(ValueError, "Bots"):
            invocation(current, "accept", "accept")
