import logging

from events.event import Event
from state.state_manager import StateManager


class GameEngine:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.info("New game started")
        self.state_manager = StateManager()

    def process_event(self, event):
        if event.type == "player_joined":
            self.player_joined(event)
        elif event.type == "player_left":
            self.player_left(event)
        elif event.type == "chat_message":
            self.chat_received(event)
        else:
            self.log.warning(f"Event type: {event.type} not recognized.")

    def player_joined(self, event):
        self.state_manager.add_player(event)
        self.state_manager.transcribe_event(event)
        return self

    def player_left(self, event):
        event = self.state_manager.remove_player(event)
        self.state_manager.transcribe_event(event)
        return self

    def chat_received(self, event):
        self.state_manager.send_chat_message(event)
        return self

    # Right now these functions are pretty simple, but we can put more complicated
    # game logic in here to begin the game, track turns, calculate the winner, etc

    def get_game_state_event(self):
        return self.state_manager.get_current_state()
