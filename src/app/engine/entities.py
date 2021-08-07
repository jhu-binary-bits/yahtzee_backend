from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from itertools import groupby
from random import randint
from typing import List

from src.app.state.yahtzee.player import Player

@dataclass(init=False)
class Die():
    def __init__(self, die_id: int, face_value: int = None):
        self.die_id = die_id
        
        if face_value == None:
            face_value = Die._get_random_face_value()

        self.face_value = face_value

    @property
    def die_id(self) -> int:
        return self._die_id

    @die_id.setter
    def die_id(self, id: int):
        if 1 <= id <= 5:
            self._die_id = id

    @property
    def face_value(self) -> int:
        return self._face_value

    @face_value.setter
    def face_value(self, value: int):
        if 1 <= value <= 6:
            self._face_value = value
    
    def roll(self):
        rolled_face_value = Die._get_random_face_value()
        return Die(self.die_id, rolled_face_value)

    def __eq__(self, other):
        if not isinstance(other, Die):
            raise NotImplementedError

        return self._die_id == other._die_id

    @staticmethod
    def _get_random_face_value() -> int:
        return randint(1, 6)

    def to_json(self):
        return {
            "die_id": self.die_id,
            "face_value": self.face_value
        }

@dataclass(frozen=True, init=True)
class Roll():
    dice: List[Die] = field(default_factory=lambda: Roll._get_default_dice())

    @staticmethod
    def _get_default_dice() -> List[Die]:
        return [Die(1), Die(2), Die(3), Die(4), Die(5)]

    def roll_selected_dice(self, dice_to_roll: List[Die]):
        return [die.roll() if die in dice_to_roll else die for die in self.dice]

    def to_json(self):
        return [die.to_json() for die in self.dice]

class ScoreType(Enum):
    ONES = "ONES"
    TWOS = "TWOS"
    THREES = "THREES"
    FOURS = "FOURS"
    FIVES = "FIVES"
    SIXES = "SIXES"
    THREE_OF_A_KIND = "THREE_OF_A_KIND"
    FOUR_OF_A_KIND = "FOUR_OF_A_KIND"
    FULL_HOUSE = "FULL_HOUSE"
    SMALL_STRAIGHT = "SMALL_STRAIGHT"
    LARGE_STRAIGHT = "LARGE_STRAIGHT"
    YAHTZEE = "YAHTZEE"
    CHANCE = "CHANCE"

class SectionType(Enum):
    UPPER = "UPPER"
    LOWER = "LOWER"

@dataclass
class Score(ABC):
    _selected_roll: Roll = None

    @property
    def selected_roll(self) -> Roll:
        return self._selected_roll

    @property
    @abstractmethod
    def score_type(self) -> ScoreType:
        pass

    @property
    @abstractmethod
    def section_type(self) -> SectionType:
        pass

    @abstractmethod
    def is_valid_for_roll(self, roll: Roll) -> bool:
        pass

    def calculate_points(self) -> int:
        if self._selected_roll is None:
            return None
        
        if self.is_valid_for_roll(self._selected_roll):
            return self._calculate_points_internal()
        else:
            return 0

    @abstractmethod
    def _calculate_points_internal(self) -> int:
        pass

    @selected_roll.setter
    def selected_roll(self, roll: Roll):
        if self._selected_roll is None and roll is not None:
            self._selected_roll = roll

    def to_json(self):
        return {
            "score_type": self.score_type().value,
            "points": self.calculate_points()
        }

@dataclass
class UpperSectionScore(Score, ABC):
    def section_type(self) -> SectionType:
        return SectionType.UPPER 

    def is_valid_for_roll(self, roll: Roll) -> bool:
        return True

    def _calculate_points_internal(self) -> int:
        return sum([die.face_value for die in self._selected_roll.dice if die.face_value == self._die_value()])

    @abstractmethod
    def _die_value(self) -> int:
        pass 

@dataclass
class OnesScore(UpperSectionScore):
    def score_type(self) -> ScoreType:
        return ScoreType.ONES

    def _die_value(self) -> int:
        return 1

@dataclass
class TwosScore(UpperSectionScore):
    def score_type(self) -> ScoreType:
        return ScoreType.TWOS

    def _die_value(self) -> int:
        return 2

@dataclass
class ThreesScore(UpperSectionScore):
    def score_type(self) -> ScoreType:
        return ScoreType.THREES

    def _die_value(self) -> int:
        return 3

@dataclass
class FoursScore(UpperSectionScore):
    def score_type(self) -> ScoreType:
        return ScoreType.FOURS

    def _die_value(self) -> int:
        return 4

@dataclass
class FivesScore(UpperSectionScore):
    def score_type(self) -> ScoreType:
        return ScoreType.FIVES

    def _die_value(self) -> int:
        return 5

@dataclass
class SixesScore(UpperSectionScore):
    def score_type(self) -> ScoreType:
        return ScoreType.SIXES

    def _die_value(self) -> int:
        return 6

@dataclass
class GroupedScore(Score, ABC):
    def _get_length_of_groups_of_dice(self, roll: Roll) -> List[int]:
        # Group dice by their face value
        grouped_dice = [list(iterator) for key, iterator in groupby(roll.dice, lambda die: die.face_value)]
        
        # Get the length of each group of dice
        return [len(group_of_dice) for group_of_dice in grouped_dice]

@dataclass
class ThreeOfAKindScore(GroupedScore):
    def section_type(self) -> SectionType:
        return SectionType.LOWER 

    def score_type(self) -> ScoreType:
        return ScoreType.THREE_OF_A_KIND

    def is_valid_for_roll(self, roll: Roll) -> bool:
        length_of_groups_of_dice = self._get_length_of_groups_of_dice(roll)

        return len([length_of_group_of_dice for length_of_group_of_dice in length_of_groups_of_dice if length_of_group_of_dice >= 3]) == 1

    def _calculate_points_internal(self) -> int:
        return sum([die.face_value for die in self._selected_roll.dice])

@dataclass
class FourOfAKindScore(GroupedScore):
    def section_type(self) -> SectionType:
        return SectionType.LOWER 

    def score_type(self) -> ScoreType:
        return ScoreType.FOUR_OF_A_KIND

    def is_valid_for_roll(self, roll: Roll) -> bool:
        length_of_groups_of_dice = self._get_length_of_groups_of_dice(roll)

        # One group of 4 or more dice
        return len([length_of_group_of_dice for length_of_group_of_dice in length_of_groups_of_dice if length_of_group_of_dice >= 4]) == 1

    def _calculate_points_internal(self) -> int:
        return sum([die.face_value for die in self._selected_roll.dice])

@dataclass
class FullHouseScore(GroupedScore):
    def section_type(self) -> SectionType:
        return SectionType.LOWER 

    def score_type(self) -> ScoreType:
        return ScoreType.FULL_HOUSE

    def is_valid_for_roll(self, roll: Roll) -> bool:
        length_of_groups_of_dice = self._get_length_of_groups_of_dice(roll)

        # Two groups of dice: one with 3 dice and one with 2 dice
        return len([length_of_group_of_dice for length_of_group_of_dice in length_of_groups_of_dice if length_of_group_of_dice == 3]) == 1 and \
               len([length_of_group_of_dice for length_of_group_of_dice in length_of_groups_of_dice if length_of_group_of_dice == 2]) == 1

    def _calculate_points_internal(self) -> int:
        return 25

@dataclass
class SmallStraightScore(Score):
    def section_type(self) -> SectionType:
        return SectionType.LOWER 

    def score_type(self) -> ScoreType:
        return ScoreType.SMALL_STRAIGHT

    def is_valid_for_roll(self, roll: Roll) -> bool:
        small_straight_variation_one_die_face_values = set([1, 2, 3, 4])
        small_straight_variation_two_die_face_values = set([2, 3, 4, 5])
        small_straight_variation_three_die_face_values = set([3, 4, 5, 6])

        roll_face_values = set([die.face_value for die in roll.dice])

        return (small_straight_variation_one_die_face_values <= roll_face_values) or \
               (small_straight_variation_two_die_face_values <= roll_face_values) or \
               (small_straight_variation_three_die_face_values <= roll_face_values)

    def _calculate_points_internal(self) -> int:
        return 30

@dataclass
class LargeStraightScore(Score):
    def section_type(self) -> SectionType:
        return SectionType.LOWER 

    def score_type(self) -> ScoreType:
        return ScoreType.LARGE_STRAIGHT

    def is_valid_for_roll(self, roll: Roll) -> bool:
        large_straight_variation_one_die_face_values = set([1, 2, 3, 4, 5])
        large_straight_variation_two_die_face_values = set([2, 3, 4, 5, 6])

        roll_face_values = set([die.face_value for die in roll.dice])

        return (large_straight_variation_one_die_face_values <= roll_face_values) or \
               (large_straight_variation_two_die_face_values <= roll_face_values)

    def _calculate_points_internal(self) -> int:
        return 40

@dataclass
class ChanceScore(Score):
    def section_type(self) -> SectionType:
        return SectionType.LOWER 

    def score_type(self) -> ScoreType:
        return ScoreType.CHANCE

    def is_valid_for_roll(self, roll: Roll) -> bool:
        return True

    def _calculate_points_internal(self) -> int:
        return sum([die.face_value for die in self._selected_roll.dice])

@dataclass
class YahtzeeScore(GroupedScore):
    def section_type(self) -> SectionType:
        return SectionType.LOWER 

    def score_type(self) -> ScoreType:
        return ScoreType.YAHTZEE

    def is_valid_for_roll(self, roll: Roll) -> bool:
        length_of_groups_of_dice = self._get_length_of_groups_of_dice(roll)

        # One group of 5 dice
        return len([length_of_group_of_dice for length_of_group_of_dice in length_of_groups_of_dice if length_of_group_of_dice == 5]) == 1

    def _calculate_points_internal(self) -> int:
        return 50

@dataclass(init=True)
class Scorecard():
    player: Player
    scores: List[Score] = field(default_factory=lambda: Scorecard._get_initial_scorecard())

    def get_valid_scores_for_roll(self, roll: Roll) -> List[Score]:
        return [score for score in self.scores if score.is_valid_for_roll(roll)]

    def get_upper_section_total(self):
        return self._get_section_total(SectionType.UPPER)

    def get_lower_section_total(self):
        return self._get_section_total(SectionType.LOWER)

    def get_grand_total(self):
        return self.get_upper_section_total() + self.get_lower_section_total()

    def select_score_for_roll(self, score_type: ScoreType, roll: Roll):
        score_for_roll = [score for score in self.scores if score.score_type == score_type][0]

        score_for_roll.selected_roll = roll

    def _get_section_total(self, section_type: SectionType):
         return sum(filter(None, [score.calculate_points() for score in self.scores if score.section_type == section_type]))

    def __eq__(self, other):
        if not isinstance(other, Scorecard):
            raise NotImplementedError

        return self.player.websocket == other.player.websocket

    def to_json(self):
        return {
            "player": self.player.to_json(),
            "scores": [score.to_json() for score in self.scores]
        }

    @staticmethod
    def _get_initial_scorecard() -> List[Score]:
        return [OnesScore(),
                TwosScore(),
                ThreesScore(),
                FoursScore(),
                FivesScore(),
                SixesScore(),
                ThreeOfAKindScore(),
                FourOfAKindScore(),
                FullHouseScore(),
                SmallStraightScore(),
                LargeStraightScore(),
                YahtzeeScore(),
                ChanceScore()]

@dataclass(init=True)
class Turn:
    MAX_ROLL_COUNT = 3

    last_roll: Roll = Roll()
    roll_count: int = 1
    selected_score_type: ScoreType = None

    def roll_selected_dice(self, dice_to_roll: List[Die]):
        if self.roll_count == Turn.MAX_ROLL_COUNT:
            raise Exception(f"Dice have already been rolled {Turn.MAX_ROLL_COUNT} times this turn.")

        self.last_roll.roll_selected_dice(dice_to_roll)
        self.roll_count += 1

    def is_turn_complete(self) -> bool:
        return self.selected_score_type is not None

    def to_json(self):
        return {
            "last_roll": self.last_roll.to_json(),
            "roll_count": self.roll_count,
            "selected_score_type": self.selected_score_type.value if self.selected_score_type else None
        }
