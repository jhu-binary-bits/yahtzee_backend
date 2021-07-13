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

    def parse_message_to_dict(self) -> dict:
        self.log.debug("Parsing message to dict")
        try:
            event_dict = json.loads(self.message)
            return event_dict
        except json.decoder.JSONDecodeError as e:
            self.log.info("Encountered exception when deserializing json.")
            self.log.info(f"Exception: {e}")
            return {}

    def get_timestamp(self):
        try:
            return datetime.fromtimestamp(float(self.event_dict["timestamp"])/1000).strftime("%Y-%m-%d %H:%M:%S")
        except KeyError:
            self.log.error("There was no 'timestamp' key included in the message.")

    def get_type(self):
        try:
            return self.event_dict["type"]
        except KeyError:
            self.log.error("There was no 'type' key included in the message.")

    def get_data(self):
        try:
            return self.event_dict["data"]
        except KeyError:
            self.log.error("There was no 'data' key included in the message.")
