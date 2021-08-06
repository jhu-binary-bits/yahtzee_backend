import json
import logging
from datetime import datetime
from engine.game_engine import GameEngine
from events.event import Event
from state.transcripts.message import Message
from state.transcripts.transcript import Transcript
from state.yahtzee.player import Player


class StateManager:
    def __init__(self):
        """
        Instantiates the classes required classes to manage a game
        """
        self.log = logging.getLogger(__name__)
        self.players = list()
        self.game_engine = GameEngine()
        self.chat_transcript = Transcript()
        self.game_transcript = Transcript()

    def process_event(self, event):
        """
        The central method of this class which processes all valid events received by the EventBroker.
        Forwards events to the correct method for processing
        """
        if event.type == "player_joined":
            self.add_connected_player(event)
        elif event.type == "player_left":
            self.remove_connected_player(event)
        elif event.type == "chat_message":
            self.send_chat_message(event)
        elif event.type == "start_game":
            self.start_game()
        else:
            self.log.warning(f"Event type: {event.type} not recognized.")

    def add_connected_player(self, event: Event):
        self.log.info("Adding player to the game")
        new_player = Player(name=event.data["player_name"], websocket=event.websocket, joined_at=event.timestamp)
        self.players.append(new_player)
        self.transcribe_event(event)
        self.log.info("current player list: ")
        self.log.info(self.get_connected_players())
        return self

    def remove_connected_player(self, event: Event):
        self.log.info("Removing player to the game")
        for player in self.players:
            if player.websocket == event.websocket:
                event.data["player_name"] = player.name
                self.players.remove(player)
        self.transcribe_event(event)
        self.log.info("current player list: ")
        self.log.info(self.get_connected_players())
        return self

    def get_connected_players(self):
        return [str(player) for player in self.players]

    def send_chat_message(self, event: Event):
        message = Message(event)
        self.chat_transcript.add_message(message)
        return self

    def start_game(self):
        self.game_engine.start_game()
        return self

    def transcribe_event(self, event):
        message = Message(event)
        self.game_transcript.add_message(message)
        return self

    def publish_current_state(self):
        data = {
            "game_started": self.game_engine.game_started,
            "players": self.get_connected_players(),
            "chat_transcript": self.chat_transcript.get_transcript(),
            "game_transcript": self.game_transcript.get_transcript()
        }
        game_state_event = {
            "timestamp": datetime.now().timestamp(),
            "type": "game_state_update",
            "data": data
        }
        self.log.info("Publishing game state update:")
        self.log.info(game_state_event)
        return json.dumps(game_state_event)
