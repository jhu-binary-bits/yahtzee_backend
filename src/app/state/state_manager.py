import json
import logging
from datetime import datetime
from engine.game_engine import GameEngine
from events.event import Event
from pprint import pformat
from state.transcripts.message import Message
from state.transcripts.transcript import Transcript
from state.yahtzee.player import Player
import itertools


class StateManager:
    def __init__(self):
        """
        Instantiates the classes required classes to manage a game
        """
        self.log = logging.getLogger(__name__)
        self.players = list()
        self.game_engine = GameEngine()
        self.chat_transcript = Transcript()
        self.game_transcript = Transcript()
        self.private_transcripts = {}

    def process_event(self, event):
        """
        The central method of this class which processes all valid events received by the EventBroker.
        Forwards events to the correct method for processing
        """
        if event.type == "player_joined":
            self.add_connected_player(event)
        elif event.type == "player_left":
            self.remove_connected_player(event)
        elif event.type == "chat_message":
            self.send_chat_message(event)
        elif event.type == "game_started":
            self.start_game(event)
        elif event.type == "rolled_dice":
            self.roll_selected_dice(event)
        elif event.type == "score_selected":
            self.score_selected(event)
        else:
            self.log.warning(f"Event type: {event.type} not recognized.")

    def add_connected_player(self, event: Event):
        self.log.info("Adding player to the game")
        new_player = Player(name=event.data["player_name"], websocket=event.websocket, joined_at=event.timestamp)
        self.players.append(new_player)
        self.transcribe_event(event)
        self.log.info("current player list: ")
        self.log.info(self.get_connected_players())

        # Temporary hack to reset game each time a new player joins (makes debugging much easier).
        self.game_engine = GameEngine()

        return self

    def remove_connected_player(self, event: Event):
        self.log.info("Removing player from the game")
        for player in self.players:
            if player.websocket == event.websocket:
                event.data["player_name"] = player.name
                self.players.remove(player)
        self.transcribe_event(event)
        self.log.info("current player list: ")
        self.log.info(self.get_connected_players())
        return self

    def get_connected_players(self):
        return [str(player) for player in self.players]

    def send_chat_message(self, event: Event):
        message = Message(event)
        if(event.data['destination'] == "all"):
            self.chat_transcript.add_message(message)
        else:
            key = event.data['player_name'] + "/" + event.data['destination']
            self.private_transcripts[key].add_message(message)
        return self

    def start_game(self, event: Event):
        for pair in itertools.combinations(self.players, 2):
            privateTranscript = Transcript()
            key = pair[0].name + "/" + pair[1].name
            key2 = pair[1].name + "/" + pair[0].name
            self.private_transcripts[key] = privateTranscript
            self.private_transcripts[key2] = privateTranscript
        self.game_engine.start_game(self.players)
        self.transcribe_event(event, len(self.players))
        return self

    def roll_selected_dice(self, event: Event):
        self.game_engine.roll_selected_dice(event.get_data()["dice_to_roll"])
        valuelist = [dice.face_value for dice in self.game_engine.current_turn.last_roll.dice]
        self.log.info(valuelist)
        self.transcribe_event(event, valuelist)

    def score_selected(self, event: Event):
        self.game_engine.select_score_for_roll(event.get_data()["selected_score_type"])
        self.transcribe_event(event, event.get_data()["selected_score_type"].lower().replace("_", " "))
        event.type = "update_turn"
        self.transcribe_event(event, self.game_engine.current_turn.player.name)

    def transcribe_event(self, event, info=None):
        message = Message(event, info)
        self.game_transcript.add_message(message)
        return self

    def publish_current_state(self):
        if not self.game_engine.game_started:
            data = {
                "game_started": self.game_engine.game_started,
                "players": self.get_connected_players(),
                "chat_transcript": self.chat_transcript.get_transcript(),
                "game_transcript": self.game_transcript.get_transcript(),
                "scorecards": [],
                "current_turn": ""
            }
            game_state_event = {
                "timestamp": datetime.now().timestamp(),
                "type": "game_state_update",
                "data": data
            }
        else:
            # current_turn_valid_scores = self.game_engine.current_scorecard.get_valid_scores_for_roll(
            #     roll=self.game_engine.current_turn.last_roll
            # )

            valid_scores = {}
            #if the roll is yahtzee and there is already a score selected, deal with yahtzee bonus
            #index 11 is the yahtzee score
            if(self.game_engine.current_scorecard.scores[11].is_valid_for_roll(self.game_engine.current_turn.last_roll) and self.game_engine.current_scorecard.scores[11].selected_roll != None):
                valid_scores = {score.score_type().value: score.calculate_yahtzee_bonus_points(self.game_engine.current_turn.last_roll) for score in self.game_engine.current_scorecard.scores}
            #otherwise proceed normally
            else:
                valid_scores = {score.score_type().value: score.calculate_potential_points(self.game_engine.current_turn.last_roll) for score in self.game_engine.current_scorecard.scores}

            #{score.score_type().value: score.calculate_potential_points(self.game_engine.current_turn.last_roll) for score in self.game_engine.current_scorecard.scores}

            data = {
                "game_started": self.game_engine.game_started,
                "players": self.get_connected_players(),
                "chat_transcript": self.chat_transcript.get_transcript(),
                "game_transcript": self.game_transcript.get_transcript(),
                "private_transcripts": {key: self.private_transcripts[key].get_transcript() for key in self.private_transcripts},
                "scorecards": {scorecard.player.name: scorecard.to_dict() for scorecard in self.game_engine.scorecards},
                "current_turn": {
                    **self.game_engine.current_turn.to_dict(),
                    "valid_scores": valid_scores
                },
                "game_winner": self.game_engine.game_winner
            }
            game_state_event = {
                "timestamp": datetime.now().timestamp(),
                "type": "game_state_update",
                "data": data
            }

        self.log.info("Publishing game state update:")
        self.log.info(pformat(game_state_event))
        return json.dumps(game_state_event)
