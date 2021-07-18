import logging

from events.event import Event
from state.chat.chat_message import ChatMessage
from state.chat.chat_history import ChatHistory
from state.transcript.game_event import GameEvent
from state.transcript.game_transcript import GameTranscript
from state.yahtzee.player import Player


class GameEngine:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.info("New game started")
        self.players = list()
        self.chat_history = ChatHistory()
        self.game_transcript = GameTranscript()

    def get_players_strings(self):
        return [str(player) for player in self.players]

    def add_player(self, event: Event):
        self.log.info("Adding player to the game")
        new_player = Player(name=event.data["player_name"], joined_at=event.timestamp)
        self.players.append(new_player)
        self.log.info("current player list: ")
        self.log.info(self.get_players_strings())
        return self

    def remove_player(self, websocket):
        self.log.info("Removing player from the game")
        # TODO: Going to need to figure out how to associate websockets with specific players.
        # TODO:    For now, we can't remove players from the game, and we can't refresh the page.
        return self

    def send_chat_message(self, event: Event):
        message = ChatMessage(event)
        self.chat_history.add_message(message)

    def process_event(self, event):
        if event.type == "player_joined":
            self.add_player(event)
            self.game_transcript.add_game_event(GameEvent(event))
        elif event.type == "chat_message":
            self.send_chat_message(event)
        else:
            self.log.warning(f"Event type: {event.type} not recognized.")

    def get_state(self):
        state = {
            "players": self.get_players_strings(),
            "chat_history": self.chat_history.history
        }
        return state
