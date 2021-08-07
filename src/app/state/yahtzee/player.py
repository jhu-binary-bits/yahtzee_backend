from dataclasses import dataclass


@dataclass(init=True)
class Player:
    name: str
    websocket: object
    joined_at: object

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "name": self.name,
            "websocket": self.websocket
        }
