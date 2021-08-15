import logging
from itertools import cycle
from typing import List

from engine.entities import Scorecard, Turn, ScoreType
from state.yahtzee.player import Player

COMPLETED_GAME_TURN_COUNT = 13

class GameEngine:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.game_started = False
        self.scorecards = List[Scorecard]
        self.scorecards_cycle = None
        self.current_scorecard = None
        self.current_turn = None
        self.game_winner = None

    def start_game(self, players: List[Player]):
        self.game_started = True
        self.scorecards = [Scorecard(player=player) for player in players]
        self.scorecards_cycle = cycle(self.scorecards)
        self._update_current_turn()
        self.game_winner = {"player_name": None, "grand_total": None}
        self.log.info(f"New game started with {len(players)} players.")
        return self

    def roll_selected_dice(self, dice_to_roll):
        dice = [self.current_turn.last_roll.get_die_by_id(int(die_id)) for die_id in dice_to_roll]
        self.current_turn.roll_selected_dice(dice)

    def select_score_for_roll(self, score_type_selected):
        # each score_type_selected from the front should match the name of the score in the enum
        score_type_selected = ScoreType(score_type_selected.upper())
        self.current_scorecard.select_score_for_roll(score_type_selected, self.current_turn.last_roll)
        self.current_turn.selected_score_type = score_type_selected

        # Now that the current player has selected a score for their turn, update the current turn.
        self._update_current_turn()

    def _update_current_turn(self):
        if self._is_first_turn_of_game() or self.current_turn.is_turn_complete():
            if self._is_game_complete():
                self.log.info("The game is complete")
                self._calculate_winner()
            else:
                self.current_scorecard = next(self.scorecards_cycle)
                self.current_turn = Turn(player=self.current_scorecard.player)

    def _is_first_turn_of_game(self) -> bool:
        return self.current_turn is None

    def _is_game_complete(self) -> bool:
        for scorecard in self.scorecards:
            if scorecard.get_completed_turn_count() < COMPLETED_GAME_TURN_COUNT:
                return False
        return True

    def _calculate_winner(self):
        top_scorecard = max(self.scorecards, key=lambda scorecard: scorecard.get_grand_total())

        self.game_winner["player_name"] = top_scorecard.player.name
        self.game_winner["grand_total"] = top_scorecard.get_grand_total()
