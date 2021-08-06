import logging


class GameEngine:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.game_started = False

    def start_game(self):
        self.game_started = True
        self.log.info("New game started")
        return self
