import logging

from datetime import datetime


class Message:
    def __init__(self, event):
        self.log = logging.getLogger(__name__)
        self.event = event
        self.timestamp = self.format_timestamp()
        self.player = self.event.data["player_name"]
        self.event_type = self.event.type
        self.event_data = self.event.data

        self.text = self.set_message()

    def format_timestamp(self):
        return datetime.strptime(self.event.timestamp_est, "%Y-%m-%d %H:%M:%S").strftime("%I:%M%p").lstrip("0")

    def set_message(self):
        message = f"{self.timestamp}  {self.player}"

        if self.event_type == "chat_message":
            txt = self.event.data['content'].strip(" \t\n\r")
            message += f": {txt}"
        elif self.event_type == "player_joined":
            message += " joined the game."
        elif self.event_type == "player_left":
            message += " left the game."
        elif self.event_type == "rolled_dice":
            pass
        # TODO: Add in other types of game transcript messages
        else:
            self.log.warning("Game event type not recognized, could not produce an entry for the transcript.")
            self.log.warning(f"\tMessage from client was: {self.event.message}")
            return ""

        return message