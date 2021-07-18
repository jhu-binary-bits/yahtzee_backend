import logging
from state.transcript.game_event import GameEvent


class GameTranscript:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.transcript_list = list()

    def add_game_event(self, game_event: GameEvent):
        self.transcript_list.append(game_event.text)

    def get_transcript(self):
        transcript = ""
        for i, txt in enumerate(self.transcript_list):
            if i == 0:
                transcript += txt
            else:
                transcript += f"\n{txt}"
        return transcript
