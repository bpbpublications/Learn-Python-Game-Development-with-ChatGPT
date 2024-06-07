# action.py
class Action:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self, player):
        # Define what happens when the player takes this action.
        pass