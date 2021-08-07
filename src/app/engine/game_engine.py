import logging
from typing import List

from src.app.engine.entities import Scorecard
from src.app.state.yahtzee.player import Player


class GameEngine:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.game_started = False
        self.scorecards = List[Scorecard]

    def start_game(self, players: List[Player]):
        self.game_started = True
        self.scorecards = [Scorecard(player=player) for player in players]
        self.log.info("New game started")
        return self
