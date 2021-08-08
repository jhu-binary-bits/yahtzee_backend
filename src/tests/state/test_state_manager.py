import unittest

from src.app.events.event import Event
from src.app.state.state_manager import StateManager


class TestStateManager(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()
        player_joined_1 = '{"timestamp":1626828897580,"type":"player_joined","data":{"player_name":"Player 1"}}'
        player_joined_2 = '{"timestamp":1626829899580,"type":"player_joined","data":{"player_name":"Player 2"}}'
        test_event_player_joined_1 = Event(message=player_joined_1, websocket="foo")
        test_event_player_joined_2 = Event(message=player_joined_2, websocket="bar")
        self.state_manager.add_connected_player(test_event_player_joined_1)
        self.state_manager.add_connected_player(test_event_player_joined_2)

    def test_start_game_and_get_current_state(self):
        start_game_message = '{"timestamp":1626828897580,"type":"game_started","data":{"player_name":"Player 2"}}'
        start_game_event = Event(message=start_game_message, websocket="foo")
        self.state_manager.start_game(start_game_event)

        current_state = self.state_manager.publish_current_state()
        self.assertIsNotNone(current_state)

"""
import unittest

from events.event import Event
from state.state_manager import StateManager


class TestStateManager(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()
        player_joined_1 = '{"timestamp":1626828897580,"type":"player_joined","data":{"player_name":"Player 1"}}'
        player_joined_2 = '{"timestamp":1626829899580,"type":"player_joined","data":{"player_name":"Player 2"}}'
        test_event_player_joined_1 = Event(message=player_joined_1, websocket="foo")
        test_event_player_joined_2 = Event(message=player_joined_2, websocket="bar")
        self.state_manager.add_player(test_event_player_joined_1)
        self.state_manager.add_player(test_event_player_joined_2)

    def test_add_player(self):
        self.assertEqual(2, len(self.state_manager.players))

    def test_remove_player(self):
        player_1_left = '{"timestamp":1626828897580,"type":"player_left","data":{}}'
        player_2_left = '{"timestamp":1626828897580,"type":"player_left","data":{}}'
        test_event_player_1_left = Event(message=player_1_left, websocket="foo")
        test_event_player_2_left = Event(message=player_2_left, websocket="bar")
        self.state_manager.remove_player(test_event_player_1_left)
        self.state_manager.remove_player(test_event_player_2_left)

        self.assertEqual(0, len(self.state_manager.players))

    def test_get_current_players(self):
        self.assertEqual(2, len(self.state_manager.get_current_players()))
        self.assertEqual("Player 1", self.state_manager.get_current_players()[0])
        self.assertEqual("Player 2", self.state_manager.get_current_players()[1])

    def test_send_chat_message(self):
        chat_message = '{"timestamp":1626828901443,"type":"chat_message","data":{"player_name":"Player 1","content":"Hello world."}}'
        test_event_chat_message = Event(message=chat_message, websocket="foobar")
        self.state_manager.send_chat_message(test_event_chat_message)

        self.assertIn("Player 1: Hello world.", self.state_manager.chat_transcript.transcript_list[0])
        self.assertIn("Player 1: Hello world.", self.state_manager.chat_transcript.get_transcript())

    def test_transcribe_event(self):
        self.assertIn('Player 1 joined the game.', self.state_manager.game_transcript.get_transcript())
        self.assertIn('Player 2 joined the game.', self.state_manager.game_transcript.get_transcript())

    def test_get_current_state(self):
        player_left = '{"timestamp":1626829899580,"type":"player_left","data":{}}'
        test_event_player_left = Event(message=player_left, websocket="foo")
        self.state_manager.remove_player(test_event_player_left)

        game_state = self.state_manager.get_current_state()
        self.assertIn('"type": "game_state_update"', game_state)
        self.assertIn('"players": ["Player 2"]', game_state)
        self.assertIn('"game_transcript":', game_state)
        self.assertIn('Player 1 joined the game.', game_state)
        self.assertIn('Player 1 left the game.', game_state)


if __name__ == '__main__':
    unittest.main()
"""
