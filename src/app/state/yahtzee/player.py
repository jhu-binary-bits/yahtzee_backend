
class Player:
    def __init__(self, name, joined_at):
        self.name = name
        self.joined_at_ts = joined_at

    def __str__(self):
        return self.name
