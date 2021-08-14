import unittest

from src.app.events.event import Event
from src.app.state.transcripts.message import Message


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.player_joined_msg = '{"timestamp":1626828897580,"type":"player_joined","data":{"player_name":"Player 1"}}'
        self.chat_message_msg = '{"timestamp":1626828901443,"type":"chat_message","data":{"player_name":"Player 1","content":"Hello world!"}}'
        self.player_joined_event = Event(self.player_joined_msg, websocket="foo")
        self.chat_event = Event(self.chat_message_msg, websocket="bar")
        self.test_player_joined_msg = Message(self.player_joined_event, None)
        self.test_chat_msg = Message(self.chat_event, None)

    def test_player_joined_message(self):
        expected_text = "Player 1 joined the game."
        self.assertEqual(True, expected_text in self.test_player_joined_msg.text)

    def test_chat_message(self):
        expected_text = "Hello world!"
        self.assertEqual(True, expected_text in self.test_chat_msg.text)


if __name__ == '__main__':
    unittest.main()
