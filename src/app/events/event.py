import json
import logging

from datetime import datetime


class Event:
    def __init__(self, message: str):
        self.log = logging.getLogger(__name__)
        self.message = message
        self.event_dict = self.parse_message_to_dict()

        self.timestamp = self.get_timestamp()
        self.type = self.get_type()
        self.data = self.get_data()

        self.is_valid = self.validate_event()

    def parse_message_to_dict(self) -> dict:
        self.log.debug("Parsing message to dict")
        try:
            event_dict = json.loads(self.message)
            return event_dict
        except json.decoder.JSONDecodeError as e:
            self.log.error("Error when deserializing JSON, formatting is likely incorrect.")
            return {}

    def get_timestamp(self):
        self.log.debug("Parsing timestamp from message")
        try:
            return datetime.fromtimestamp(float(self.event_dict["timestamp"])/1000).strftime("%Y-%m-%d %H:%M:%S")
        except KeyError as e:
            self.log.error(f"Error parsing message, there was no 'timestamp' included in the message: {self.message}")
            return None

    def get_type(self):
        self.log.debug("Parsing type from message")
        try:
            return self.event_dict["type"]
        except KeyError as e:
            self.log.error(f"Error parsing message, there was no 'type' included in the message: {self.message}")
            return None

    def get_data(self):
        self.log.debug("Parsing data from message")
        try:
            return self.event_dict["data"]
        except KeyError:
            self.log.error(f"Error parsing message, there was no 'data' included in the message: {self.message}")
            return None

    def validate_event(self):
        """
        It is considered a valid event if the JSON was parsed and each of the expected fields is filled out
        """
        self.log.debug("Assessing event validity")
        if len(self.event_dict) > 0 and self.timestamp and self.type and self.data:
            return True
        return False
