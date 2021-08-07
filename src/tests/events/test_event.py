"""
import unittest
from src.app.events.event import Event


class TestEvent(unittest.TestCase):
    def setUp(self) -> None:
        player_joined = '{"timestamp":1626828897580,"type":"player_joined","data":{"player_name":"Player 1"}}'
        player_left = '{"timestamp":1626829899580,"type":"player_left","data":{"player_name":"Player 1"}}'
        chat_message = '{"timestamp":1626828901443,"type":"chat_message","data":{"player_name":"Player 1","content":"Hello"}}'
        invalid_event_1 = '{"type":"chat_message","data":{"player_name":"Player 1","content":"Hello"}}'
        invalid_event_2 = '{"timestamp":1626829899580,"type":"player_left","typo":{}}'
        self.test_event_player_joined = Event(message=player_joined, websocket="foo")
        self.test_event_player_left = Event(message=player_left, websocket="bar")
        self.test_event_chat_message = Event(message=chat_message, websocket="foobar")
        self.test_invalid_event_1 = Event(message=invalid_event_1, websocket="foobar2")
        self.test_invalid_event_2 = Event(message=invalid_event_2, websocket="foobar3")

    def test_is_valid(self):
        self.assertTrue(self.test_event_player_joined.is_valid)
        self.assertTrue(self.test_event_player_left.is_valid)
        self.assertTrue(self.test_event_chat_message.is_valid)
        self.assertFalse(self.test_invalid_event_1.is_valid)
        self.assertFalse(self.test_invalid_event_2.is_valid)

    def test_timestamp(self):
        self.assertEqual("2021-07-20 20:54:57", self.test_event_player_joined.timestamp_est)
        self.assertEqual("2021-07-20 21:11:39", self.test_event_player_left.timestamp_est)
        self.assertEqual("2021-07-20 20:55:01", self.test_event_chat_message.timestamp_est)

    def test_type(self):
        self.assertEqual("player_joined", self.test_event_player_joined.type)
        self.assertEqual("player_left", self.test_event_player_left.type)
        self.assertEqual("chat_message", self.test_event_chat_message.type)

    def test_data(self):
        self.assertEqual({"player_name": "Player 1"}, self.test_event_player_joined.data)
        self.assertEqual({"player_name": "Player 1"}, self.test_event_player_left.data)
        self.assertEqual({"player_name": "Player 1", "content": "Hello"}, self.test_event_chat_message.data)

    def test_websocket(self):
        self.assertEqual("foo", self.test_event_player_joined.websocket)
        self.assertEqual("bar", self.test_event_player_left.websocket)
        self.assertEqual("foobar", self.test_event_chat_message.websocket)


if __name__ == '__main__':
    unittest.main()
"""