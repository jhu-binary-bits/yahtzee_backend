"""
import unittest

from src.app.engine.game_engine import GameEngine
from src.app.events.event import Event

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.game_engine = GameEngine()
        player_1_joined = '{"timestamp":1626828897580,"type":"player_joined","data":{"player_name":"Player 1"}}'
        player_2_joined = '{"timestamp":1626829156891,"type":"player_joined","data":{"player_name":"Player 2"}}'
        chat_message = '{"timestamp":1626828901443,"type":"chat_message","data":{"player_name":"Player 1","content":"Hello world."}}'
        player_1_joined_event = Event(message=player_1_joined, websocket="foo")
        player_2_joined_event = Event(message=player_2_joined, websocket="bar")
        chat_message_event = Event(message=chat_message, websocket="foo")

        self.game_engine.process_event(player_1_joined_event)
        self.game_engine.process_event(player_2_joined_event)
        self.game_engine.process_event(chat_message_event)

    def test_process_event_player_joined(self):
        self.assertEqual(2, len(self.game_engine.state_manager.players))
        self.assertEqual("Player 1", str(self.game_engine.state_manager.players[0]))
        self.assertEqual("Player 2", str(self.game_engine.state_manager.players[1]))

    def test_process_event_player_left(self):
        player_1_left = '{"timestamp":1626828897580,"type":"player_left","data":{}}'
        player_1_left_event = Event(message=player_1_left, websocket="foo")
        self.game_engine.process_event(player_1_left_event)

        self.assertEqual(1, len(self.game_engine.state_manager.players))
        self.assertEqual("Player 2", str(self.game_engine.state_manager.players[0]))

    def test_process_event_chat_received(self):
        self.assertEqual(1, len(self.game_engine.state_manager.chat_transcript.transcript_list))
        self.assertIn("Player 1: Hello world.", str(self.game_engine.state_manager.chat_transcript.transcript_list[0]))
        self.assertIn("Player 1: Hello world.", str(self.game_engine.state_manager.chat_transcript.get_transcript()))

    def test_get_game_state(self):
        game_state = self.game_engine.get_game_state_event()
        self.assertIn('"type": "game_state_update"', game_state)
        self.assertIn('"players": ', game_state)
        self.assertIn('"chat_transcript": ', game_state)
        self.assertIn('"game_transcript": ', game_state)
        self.assertIn("Player 1 joined the game.", game_state)
        self.assertIn("Player 2 joined the game.", game_state)
        self.assertIn("Player 1: Hello world.", game_state)


if __name__ == '__main__':
    unittest.main()
"""