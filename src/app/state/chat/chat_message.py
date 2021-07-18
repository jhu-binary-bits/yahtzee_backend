import logging
from datetime import datetime


class ChatMessage:
    def __init__(self, event):
        self.log = logging.getLogger(__name__)
        self.event = event
        self.timestamp = self.event.timestamp
        self.player = self.event.data["player_name"]
        self.content = self.event.data["content"]

        self.text = self.set_message()

    # def format_timestamp(self): # TODO: Add a timestamp (hour: minute)?, if we want
    #     datetime.(self.event.timestamp)

    def set_message(self):
        # TODO: We could add a timestamp as well if we want
        return f"{self.player}: {self.content}"
