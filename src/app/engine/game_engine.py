import logging
from itertools import cycle
from typing import List

from src.app.engine.entities import Scorecard, Turn, ScoreType
from src.app.state.yahtzee.player import Player
from engine.entities import Die

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
        self.scorecards = [Scorecard(player=player.name) for player in players]
        self.scorecards_cycle = cycle(self.scorecards)
        self._update_current_turn()
        self.log.info(f"New game started with {len(players)} players.")
        return self

    def roll_selected_dice(self, dice_to_roll):
        #TODO: The "dice_to_roll" argument needs to be converted to a List[Die]
        #      prior to invoking the self.current_turn.roll_selected_dice function.
        newdice = []

        for d in dice_to_roll:
            #newd = Die(int(d[4]))
            newdice.append(int(d[4]))
            #self.log.info(d[4])
            #newdice.append(self.current_turn.last_roll.get_die_by_id(d[4]))
        #self.log.info(newdice[0].die_id)
        self.current_turn.roll_selected_dice(newdice)

    def select_score_for_roll(self, score_type_selected):
        # each score_type_selected from the front should match the name of the score in the enum
        self.current_scorecard.select_score_for_roll(ScoreType(score_type_selected.upper()))

        # Now that the current player has selected a score for their turn, update the current turn.
        self._update_current_turn()

    def _update_current_turn(self):
        if self._is_first_turn_of_game() or self.current_turn.is_turn_complete():
            self.current_scorecard = next(self.scorecards_cycle)
            self.current_turn = Turn()

    def _is_first_turn_of_game(self) -> bool:
        return self.current_turn is None
