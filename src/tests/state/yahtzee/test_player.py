import unittest

from src.app.state.yahtzee.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.test_player_1 = Player(name="player 1", websocket="foo", joined_at="2021-07-01 01:01:01")
        self.test_player_2 = Player(name="player 2", websocket="bar", joined_at="2021-07-02 02:02:02")

    def test_str(self):
        # Not really how __str__ is supposed to be used, but can test it like this I guess
        # Intended effect: print(player) will automatically use the __str__ function to print the name
        self.assertEqual("player 1", self.test_player_1.__str__())
        self.assertEqual("player 2", self.test_player_2.__str__())


if __name__ == '__main__':
    unittest.main()
