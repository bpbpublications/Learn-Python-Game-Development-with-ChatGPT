# link.py
class Link:
    def __init__(self, source_room, target_room, action):
        self.source_room = source_room
        self.target_room = target_room
        self.action = action

    def use(self, player):
        # Define how the link is used to move between rooms.
        pass