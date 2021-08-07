import logging
from itertools import cycle
from typing import List

from src.app.engine.entities import Scorecard, Turn
from src.app.state.yahtzee.player import Player


class GameEngine:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.game_started = False
        self.scorecards = List[Scorecard]
        self.scorecards_cycle = None
        self.current_scorecard = None
        self.current_turn = None

    def start_game(self, players: List[Player]):
        self.game_started = True
        self.scorecards = [Scorecard(player=player) for player in players]
        self.scorecards_cycle = cycle(self.scorecards)
        self._update_current_turn()
        self.log.info(f"New game started with {len(players)} players.")
        return self

    def roll_selected_dice(self, dice_to_roll):
        #TODO: The "dice_to_roll" argument needs to be converted to a List[Die]
        #      prior to invoking the self.current_turn.roll_selected_dice function.
        self.current_turn.roll_selected_dice(dice_to_roll)

    def select_score_for_roll(self, score_type_selected):
        #TODO: The "score_type_selected" argument needs to be converted to a ScoreType enumeration value
        #      prior to invoking the self.current_turn.roll_selected_dice function.
        self.current_scorecard.select_score_for_roll(score_type_selected)

        # Now that the current player has selected a score for their turn, update the current turn.
        self._update_current_turn()

    def _update_current_turn(self):
        if self._is_first_turn_of_game() or self.current_turn.is_turn_complete():
            self.current_scorecard = next(self.scorecards_cycle)
            self.current_turn = Turn()

    def _is_first_turn_of_game(self) -> bool:
        return self.current_turn is None