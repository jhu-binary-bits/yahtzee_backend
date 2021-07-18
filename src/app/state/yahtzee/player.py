
class Player:
    def __init__(self, name, websocket, joined_at):
        self.name = name
        self.websocket = websocket
        self.joined_at_ts = joined_at

    def __str__(self):
        return self.name
