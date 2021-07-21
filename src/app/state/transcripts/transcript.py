import logging
from state.transcripts.message import Message


class Transcript:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.transcript_list = list()

    def add_message(self, message: Message):
        self.transcript_list.append(message.text)

    def get_transcript(self):
        transcript_str = ""
        for i, txt in enumerate(self.transcript_list):
            if i == 0:
                transcript_str += txt
            else:
                transcript_str += f"\n{txt}"
        return transcript_str
