import logging
from state.chat.chat_message import ChatMessage


class ChatHistory:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.history = list()

    def add_message(self, message: ChatMessage):
        self.history.append(message.text)

    def get_transcript(self):
        messages = ""
        for i, msg in enumerate(self.history):
            if i == 0:
                messages += msg
            else:
                messages += f"\n{msg}"
        return messages
