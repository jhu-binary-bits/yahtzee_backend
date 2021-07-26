import json
import logging
from datetime import datetime
from events.event import Event
from state.transcripts.message import Message
from state.transcripts.transcript import Transcript
from state.yahtzee.player import Player
import random


class StateManager:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.players = list()
        self.chat_transcript = Transcript()
        self.game_transcript = Transcript()
        self.dice_vals = [1, 1, 1, 1, 1]

    def add_player(self, event: Event):
        self.log.info("Adding player to the game")
        new_player = Player(name=event.data["player_name"], websocket=event.websocket, joined_at=event.timestamp)
        self.players.append(new_player)
        self.transcribe_event(event)
        self.log.info("current player list: ")
        self.log.info(self.get_current_players())
        return self

    def remove_player(self, event: Event):
        self.log.info("Removing player to the game")
        for player in self.players:
            if player.websocket == event.websocket:
                event.data["player_name"] = player.name
                self.players.remove(player)
        self.transcribe_event(event)
        self.log.info("current player list: ")
        self.log.info(self.get_current_players())
        return self

    def get_current_players(self):
        return [str(player) for player in self.players]

    def send_chat_message(self, event: Event):
        message = Message(event)
        self.chat_transcript.add_message(message)
        return self

    def roll_dice(self, event: Event):
        data = event.get_data()["dice_selected"]
        nums = []
        for c in range(len(data)):
            nums.append(int(data[c][4]))
        ret = []
        for c in range(5):
            if c in nums:
                ret.append(random.randint(1,6))
            else:
                ret.append(self.dice_vals[c])

        self.dice_vals = ret
        message = Message(event)
        message.dice_message(self.dice_vals)
        self.game_transcript.add_message(message)
        return self

    def transcribe_event(self, event):
        message = Message(event)
        self.game_transcript.add_message(message)
        return self

    def get_current_state(self):
        data = {
            "players": self.get_current_players(),
            "chat_transcript": self.chat_transcript.get_transcript(),
            "game_transcript": self.game_transcript.get_transcript(),
            "dice_vals": self.dice_vals
        }
        game_state_event = {
            "timestamp": datetime.now().timestamp(),
            "type": "game_state_update",
            "data": data
        }
        return json.dumps(game_state_event)
