import json
import logging
from datetime import datetime
from events.event import Event
from state.chat.chat_message import ChatMessage
from state.chat.chat_history import ChatHistory
from state.transcript.game_event import GameEvent
from state.transcript.game_transcript import GameTranscript
from state.yahtzee.player import Player


class StateManager:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.players = list()
        self.chat_history = ChatHistory()
        self.game_transcript = GameTranscript()

    def add_player(self, event: Event):
        self.log.info("Adding player to the game")
        new_player = Player(name=event.data["player_name"], websocket=event.websocket, joined_at=event.timestamp)
        self.players.append(new_player)
        self.log.info("current player list: ")
        self.log.info(self.get_current_players())
        return self

    def remove_player(self, event: Event):
        self.log.info("Removing player to the game")
        for player in self.players:
            if player.websocket == event.websocket:
                event.data["player_name"] = player.name
                self.players.remove(player)
        self.log.info("current player list: ")
        self.log.info(self.get_current_players())
        return event

    def get_current_players(self):
        return [str(player) for player in self.players]

    def send_chat_message(self, event: Event):
        message = ChatMessage(event)
        self.chat_history.add_message(message)
        return self

    def transcribe_event(self, event):
        self.game_transcript.add_game_event(GameEvent(event))
        return self

    def get_current_state(self):
        data = {
            "players": self.get_current_players(),
            "chat_transcript": self.chat_history.get_transcript(),
            "game_transcript": self.game_transcript.get_transcript()
        }
        game_state_event = {
            "timestamp": datetime.now().timestamp(),
            "type": "game_state_update",
            "data": data
        }
        return json.dumps(game_state_event)
