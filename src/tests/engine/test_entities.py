from dataclasses import dataclass
from unittest import main, TestCase

from src.app.engine.entities import Die, FullHouseScore, OnesScore, Roll, SmallStraightScore, ThreeOfAKindScore

@dataclass
class OneFaceValueDie(Die):
    def __init__(self, die_id: int):
        super().__init__(die_id, 1)

@dataclass
class TwoFaceValueDie(Die):
    def __init__(self, die_id: int):
        super().__init__(die_id, 2)

@dataclass
class ThreeFaceValueDie(Die):
    def __init__(self, die_id: int):
        super().__init__(die_id, 3)

@dataclass
class FourFaceValueDie(Die):
    def __init__(self, die_id: int):
        super().__init__(die_id, 4)

@dataclass
class FiveFaceValueDie(Die):
    def __init__(self, die_id: int):
        super().__init__(die_id, 5)

@dataclass
class SixFaceValueDie(Die):
    def __init__(self, die_id: int):
        super().__init__(die_id, 6)

class TestEntities(TestCase):
    def test_ones_score_calculate_points_with_no_roll(self):
        ones_score = OnesScore()

        points = ones_score.calculate_points()

        self.assertEqual(points, None)
    
    def test_ones_score_calculate_points_with_roll_with_one_one(self):
        roll = Roll([OneFaceValueDie(1), TwoFaceValueDie(2), TwoFaceValueDie(3), TwoFaceValueDie(4), TwoFaceValueDie(5)])

        ones_score = OnesScore()
        ones_score.selected_roll = roll

        points = ones_score.calculate_points()

        self.assertEqual(points, 1)

    def test_ones_score_calculate_points_with_roll_with_four_ones(self):
        roll = Roll([OneFaceValueDie(1), OneFaceValueDie(2), OneFaceValueDie(3), OneFaceValueDie(4), TwoFaceValueDie(5)])

        ones_score = OnesScore()
        ones_score.selected_roll = roll

        points = ones_score.calculate_points()

        self.assertEqual(points, 4)

    def test_three_of_a_kind_score_is_valid_for_roll_with_three_dice_with_same_face_value(self):
        roll = Roll([FiveFaceValueDie(1), FiveFaceValueDie(2), FiveFaceValueDie(3), TwoFaceValueDie(4), SixFaceValueDie(5)])

        three_of_kind_score = ThreeOfAKindScore()
        is_valid_for_roll = three_of_kind_score.is_valid_for_roll(roll)

        self.assertEqual(is_valid_for_roll, True)

    def test_three_of_a_kind_score_is_valid_for_roll_without_three_dice_with_same_face_value(self):
        roll = Roll([FourFaceValueDie(1), FiveFaceValueDie(2), FiveFaceValueDie(3), TwoFaceValueDie(4), SixFaceValueDie(5)])

        three_of_kind_score = ThreeOfAKindScore()
        is_valid_for_roll = three_of_kind_score.is_valid_for_roll(roll)

        self.assertEqual(is_valid_for_roll, False)

    def test_three_of_a_kind_score_calculate_points_for_roll_with_three_dice_with_same_face_value(self):
        roll = Roll([FiveFaceValueDie(1), FiveFaceValueDie(2), FiveFaceValueDie(3), TwoFaceValueDie(4), SixFaceValueDie(5)])

        three_of_kind_score = ThreeOfAKindScore()
        three_of_kind_score.selected_roll = roll
        points = three_of_kind_score.calculate_points()

        self.assertEqual(points, 23)

    def test_three_of_a_kind_score_calculate_points_for_roll_with_three_dice_with_same_face_value(self):
        roll = Roll([FiveFaceValueDie(1), FiveFaceValueDie(2), FiveFaceValueDie(3), FiveFaceValueDie(4), SixFaceValueDie(5)])

        three_of_kind_score = ThreeOfAKindScore()
        three_of_kind_score.selected_roll = roll
        points = three_of_kind_score.calculate_points()

        self.assertEqual(points, 26)

    def test_full_house_score_is_valid_for_roll_with_three_ones_and_two_twos(self):
        roll = Roll([OneFaceValueDie(1), OneFaceValueDie(2), OneFaceValueDie(3), TwoFaceValueDie(4), TwoFaceValueDie(5)])

        full_house_score = FullHouseScore()
        is_valid_for_roll = full_house_score.is_valid_for_roll(roll)

        self.assertEqual(is_valid_for_roll, True)

    def test_full_house_score_is_valid_for_roll_with_four_ones_and_one_two(self):
        roll = Roll([OneFaceValueDie(1), OneFaceValueDie(2), OneFaceValueDie(3), OneFaceValueDie(4), TwoFaceValueDie(5)])

        full_house_score = FullHouseScore()
        is_valid_for_roll = full_house_score.is_valid_for_roll(roll)

        self.assertEqual(is_valid_for_roll, False)

    def test_small_straight_score_is_valid_for_roll_with_four_sequential_dice(self):
        roll = Roll([TwoFaceValueDie(1), ThreeFaceValueDie(2), FourFaceValueDie(3), FiveFaceValueDie(4), ThreeFaceValueDie(5)])

        small_straight_score = SmallStraightScore()
        is_valid_for_roll = small_straight_score.is_valid_for_roll(roll)

        self.assertEqual(is_valid_for_roll, True)

    def test_small_straight_score_is_valid_for_roll_without_four_sequential_dice(self):
        roll = Roll([TwoFaceValueDie(1), FourFaceValueDie(2), FiveFaceValueDie(3), TwoFaceValueDie(4), SixFaceValueDie(5)])

        small_straight_score = SmallStraightScore()
        is_valid_for_roll = small_straight_score.is_valid_for_roll(roll)

        self.assertEqual(is_valid_for_roll, False)

if __name__ == '__main__':
    main()