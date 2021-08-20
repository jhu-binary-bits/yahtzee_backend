import unittest

from src.app.events.event import Event
from src.app.state.transcripts.message import Message
from src.app.state.transcripts.transcript import Transcript


class TestTranscript(unittest.TestCase):
    def setUp(self):
        self.chat_message_msg_1 = '{"timestamp":1626828901443,"type":"chat_message","data":{"player_name":"Player 1","content":"Hello world!", "destination":"all"}}'
        self.chat_message_msg_2 = '{"timestamp":1626830788218,"type":"chat_message","data":{"player_name":"Player 2","content":"Hello world again!","destination":"all"}}'
        self.chat_message_msg_3 = '{"timestamp":1626848134529,"type":"chat_message","data":{"player_name":"Player 3","content":"Hello...","destination":"all"}}'
        self.chat_event_1 = Event(self.chat_message_msg_1, websocket="foo")
        self.chat_event_2 = Event(self.chat_message_msg_2, websocket="bar")
        self.chat_event_3 = Event(self.chat_message_msg_3, websocket="foobar")
        self.chat_msg_1 = Message(self.chat_event_1)
        self.chat_msg_2 = Message(self.chat_event_2)
        self.chat_msg_3 = Message(self.chat_event_3)
        self.test_transcript = Transcript()
        self.test_transcript.add_message(self.chat_msg_1)
        self.test_transcript.add_message(self.chat_msg_2)
        self.test_transcript.add_message(self.chat_msg_3)

    def test_transcript_len(self):
        self.assertEqual(3, len(self.test_transcript.transcript_list))

    def test_transcript_list_contents(self):
        expected_text_1 = "Player 1: Hello world!"
        expected_text_2 = "Player 2: Hello world again!"
        expected_text_3 = "Player 3: Hello..."
        self.assertEqual(True, expected_text_1 in self.test_transcript.transcript_list[0])
        self.assertEqual(True, expected_text_2 in self.test_transcript.transcript_list[1])
        self.assertEqual(True, expected_text_3 in self.test_transcript.transcript_list[2])

    def test_transcript_contents(self):
        expected_text_1 = "Player 1: Hello world!"
        expected_text_2 = "Player 2: Hello world again!"
        expected_text_3 = "Player 3: Hello..."
        self.assertEqual(True, expected_text_1 in self.test_transcript.get_transcript())
        self.assertEqual(True, expected_text_2 in self.test_transcript.get_transcript())
        self.assertEqual(True, expected_text_3 in self.test_transcript.get_transcript())


if __name__ == '__main__':
    unittest.main()
