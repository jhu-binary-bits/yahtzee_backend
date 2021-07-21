import json
import logging
from datetime import datetime
from events.event import Event
from state.transcripts.message import Message
from state.transcripts.transcript import Transcript
from state.yahtzee.player import Player


class StateManager:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.players = list()
        self.chat_transcript = Transcript()
        self.game_transcript = Transcript()

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

    def transcribe_event(self, event):
        message = Message(event)
        self.game_transcript.add_message(message)
        return self

    def get_current_state(self):
        data = {
            "players": self.get_current_players(),
            "chat_transcript": self.chat_transcript.get_transcript(),
            "game_transcript": self.game_transcript.get_transcript()
        }
        game_state_event = {
            "timestamp": datetime.now().timestamp(),
            "type": "game_state_update",
            "data": data
        }
        return json.dumps(game_state_event)
