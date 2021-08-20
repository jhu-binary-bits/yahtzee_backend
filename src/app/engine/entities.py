from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from itertools import groupby
from random import randint
from typing import List
import logging
from state.yahtzee.player import Player

NO_BONUS_AMOUNT = 0
MINIMUM_UPPER_SECTION_SCORE_FOR_BONUS = 63
UPPER_SECTION_BONUS_POINTS = 35

@dataclass(init=False)
class Die():
    def __init__(self, die_id: int, face_value: int = None):
        self.die_id = die_id
        self.log = logging.getLogger(__name__)

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
        self.face_value = rolled_face_value
        return Die(self.die_id, rolled_face_value)

    def __eq__(self, other):
        if not isinstance(other, Die):
            raise NotImplementedError

        return self._die_id == other._die_id

    @staticmethod
    def _get_random_face_value() -> int:
        return randint(1, 6)


    def to_dict(self):
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

    def get_die_by_id(self, id: int):
        for d in self.dice:
            if d.die_id == id:
                return d
        return None

    def to_dict(self):
        return [die.to_dict() for die in self.dice]

    def to_full_house(self):
        self.dice[0].face_value = 1
        self.dice[1].face_value = 1
        self.dice[2].face_value = 1
        self.dice[3].face_value = 2
        self.dice[4].face_value = 2
        return None

    def to_straight(self):
        self.dice[0].face_value = 1
        self.dice[1].face_value = 2
        self.dice[2].face_value = 3
        self.dice[3].face_value = 4
        self.dice[4].face_value = 5
        return None

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
            return self._calculate_points_internal(self._selected_roll)
        else:
            return 0

    def calculate_potential_points(self, input_roll) -> int:
        if(self.is_valid_for_roll(input_roll)):
            return self._calculate_points_internal(input_roll)
        else:
            return 0
    def calculate_yahtzee_bonus_points(self, input_roll) -> int:
        return self._calculate_points_internal(input_roll)


    @abstractmethod
    def _calculate_points_internal(self, input_roll) -> int:
        pass

    @selected_roll.setter
    def selected_roll(self, roll: Roll):
        if self._selected_roll is None and roll is not None:
            self._selected_roll = roll

    def to_dict(self):
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

    def _calculate_points_internal(self, input_roll) -> int:
        return sum([die.face_value for die in input_roll.dice if die.face_value == self._die_value()])

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
        #sort dice by face value
        dicelist = sorted(roll.dice, key=lambda die: die.face_value, reverse=True)

        # Group dice by their face value
        grouped_dice = [list(iterator) for key, iterator in groupby(dicelist, lambda die: die.face_value)]

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

    def _calculate_points_internal(self, input_roll) -> int:
        return sum([die.face_value for die in input_roll.dice])

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

    def _calculate_points_internal(self, input_roll) -> int:
        return sum([die.face_value for die in input_roll.dice])

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

    def _calculate_points_internal(self, input_roll) -> int:
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

    def _calculate_points_internal(self, input_roll) -> int:
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

    def _calculate_points_internal(self, input_roll) -> int:
        return 40

@dataclass
class ChanceScore(Score):
    def section_type(self) -> SectionType:
        return SectionType.LOWER

    def score_type(self) -> ScoreType:
        return ScoreType.CHANCE

    def is_valid_for_roll(self, roll: Roll) -> bool:
        return True

    def _calculate_points_internal(self, input_roll) -> int:
        return sum([die.face_value for die in input_roll.dice])

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

    def _calculate_points_internal(self, input_roll) -> int:
        return 50

@dataclass(init=True)
class Scorecard():
    player: Player
    scores: List[Score] = field(default_factory=lambda: Scorecard._get_initial_scorecard())
    yahtzeebonus: int = 0

    def get_completed_turn_count(self):
        return len([score for score in self.scores if score.selected_roll is not None])

    def get_valid_scores_for_roll(self, roll: Roll) -> List[Score]:
        return [score for score in self.scores if score.is_valid_for_roll(roll)]

    def get_upper_section_score_sum(self):
        return self._get_section_total(SectionType.UPPER)

    def get_upper_section_bonus(self):
        return UPPER_SECTION_BONUS_POINTS if self.get_upper_section_score_sum() \
                                             >= MINIMUM_UPPER_SECTION_SCORE_FOR_BONUS else NO_BONUS_AMOUNT

    def get_upper_section_total(self):
        return self.get_upper_section_score_sum() + self.get_upper_section_bonus()

    # TODO: Yahtzee bonus logic

    def get_lower_section_total(self):
        return self._get_section_total(SectionType.LOWER)

    def get_grand_total(self):
        return self.get_upper_section_total() + self.get_lower_section_total()

    def select_score_for_roll(self, score_type: ScoreType, roll: Roll):

        score_for_roll = [score for score in self.scores if score.score_type() is score_type][0]

        #11 is the yahtzee score type
        if(self.scores[11].is_valid_for_roll(roll) and self.scores[11].selected_roll != None):
            print(self.scores[11])
            newroll = Roll()
            self.yahtzeebonus += 100
            if(score_type.name == "FULL_HOUSE"):
                newroll.to_full_house()
                score_for_roll.selected_roll = deepcopy(newroll)
            elif(score_type.name == "SMALL_STRAIGHT" or score_type.name == "LARGE_STRAIGHT"):
                newroll.to_straight()
                score_for_roll.selected_roll = deepcopy(newroll)
            else:
                score_for_roll.selected_roll = deepcopy(roll)
        else:
            score_for_roll.selected_roll = deepcopy(roll)

    @staticmethod
    def _is_not_null_score(x):
        return not(x is None)

    def _get_section_total(self, section_type: SectionType):
        # TODO: Not sure if we're using @property fields correctly, shouldn't we be able to access score.section_type?
        section_scores = [score.calculate_points() for score in self.scores if score.section_type() == section_type]
        non_null_scores = list(filter(self._is_not_null_score, section_scores))
        ret = sum(non_null_scores)
        if(section_type.name == "LOWER"):
            ret += self.yahtzeebonus
        return ret

    def __eq__(self, other):
        if not isinstance(other, Scorecard):
            raise NotImplementedError

        return self.player == other.player

    def to_dict(self):
        return {
            "scores": {score.score_type().value: score.calculate_points() for score in self.scores},
            "UPPER_BONUS": self.get_upper_section_bonus(),
            "UPPER_TOTAL": self.get_upper_section_total(),
            "LOWER_TOTAL": self.get_lower_section_total(),
            "GRAND_TOTAL": self.get_grand_total(),
            "yahtzee_bonus": self.yahtzeebonus,
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

    player: Player
    last_roll: Roll = Roll()
    roll_count: int = 0
    selected_score_type: ScoreType = None

    def roll_selected_dice(self, dice_to_roll: List[Die]):
        if self.roll_count == Turn.MAX_ROLL_COUNT:
            raise Exception(f"Dice have already been rolled {Turn.MAX_ROLL_COUNT} times this turn.")

        self.last_roll.roll_selected_dice(dice_to_roll)
        self.roll_count += 1

    def is_turn_complete(self) -> bool:
        return self.selected_score_type is not None

    def to_dict(self):
        return {
            "last_roll": self.last_roll.to_dict(),
            "roll_count": self.roll_count,
            "selected_score_type": self.selected_score_type.value if self.selected_score_type else None,
            "player": self.player.name
        }
