import logging
from state.transcript.game_event import GameEvent


class GameTranscript:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.transcript = list()

    def add_game_event(self, game_event: GameEvent):
        self.transcript.append(game_event.message)
