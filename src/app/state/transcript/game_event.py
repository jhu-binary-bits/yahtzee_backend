import logging


class GameEvent:
    def __init__(self, event):
        self.log = logging.getLogger(__name__)
        self.event = event
        self.timestamp = self.event.timestamp
        self.player = self.event.data["player_name"]
        self.event_type = self.event.type
        self.event_data = self.event.data

        self.message = self.set_message()

        # def format_timestamp(self): # TODO: Add a timestamp (hour: minute: seconds)?, if we want
        #     datetime.(self.event.timestamp)

    def set_message(self):
        message = f"{self.timestamp} - {self.player} "

        if self.event_type == "player_joined":
            message += "joined the game."

        # TODO: Add in other types of game transcript messages

        elif self.event_type == "rolled_dice":
            pass

        else:
            self.log.warning("Game event type not recognized, could not produce an entry for the transcript.")
            return ""

        return message
