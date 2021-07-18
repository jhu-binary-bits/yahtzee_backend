import logging
from state.chat.chat_message import ChatMessage


class ChatHistory:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.history = list()

    def add_message(self, message: ChatMessage):
        self.history.append(message.message)
