# npc.py
class NPC:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def talk(self, player):
        # Define how the player can interact with the NPC.
        pass

    def trade(self, player):
        # Define trading logic with the NPC.
        pass

    def attack(self, player):
        # Define combat logic with the NPC.
        pass