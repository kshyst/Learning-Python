import unittest
from unittest.mock import Mock, patch, AsyncMock

from telegram.ext import ConversationHandler

from bot import (
    start_command_handler,
    GENDER,
    bio_message_handler,
    cancel_command_handler,
)
from telegram import Update
import asyncio


class TestInformationBotSampleTestCase(unittest.TestCase):

    def setUp(self):
        self.update = Mock(spec=Update)
        self.context = AsyncMock()

    def test_sample_start_command_handler(self):
        self.update.effective_chat.id = "987654321"
        self.update.effective_message.id = "111222333"

        with patch.object(self.context.bot, "send_message") as mock_send_message:
            state = asyncio.run(start_command_handler(self.update, self.context))
            mock_send_message.assert_called_once_with(
                chat_id=self.update.effective_chat.id,
                text="Hi, I'm here to find out more information about you."
                "You can /cancel me at any time you want.\n\n"
                "Are you a Boy or a Girl?",
                reply_to_message_id=self.update.effective_message.id,
            )
            self.assertEqual(state, GENDER)

    def test_sample_bio_message_handler(self):
        self.update.effective_chat.id = "987654321"
        self.update.effective_message.id = "111222333"

        with patch.object(self.context.bot, "send_message") as mock_send_message:
            state = asyncio.run(bio_message_handler(self.update, self.context))
            mock_send_message.assert_called_once_with(
                chat_id=self.update.effective_chat.id,
                text="Thank you! I hope we can talk again some day.",
                reply_to_message_id=self.update.effective_message.id,
            )
            self.assertEqual(state, ConversationHandler.END)

    def test_sample_cancel_command_handler(self):
        self.update.effective_chat.id = "987654321"
        self.update.effective_message.id = "111222333"

        with patch.object(self.context.bot, "send_message") as mock_send_message:
            state = asyncio.run(cancel_command_handler(self.update, self.context))
            mock_send_message.assert_called_once_with(
                chat_id=self.update.effective_chat.id,
                text="Bye! I hope we can talk again some day.",
                reply_to_message_id=self.update.effective_message.id,
            )
            self.assertEqual(state, ConversationHandler.END)
