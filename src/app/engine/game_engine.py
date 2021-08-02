import logging


class GameEngine:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.info("New game started")
