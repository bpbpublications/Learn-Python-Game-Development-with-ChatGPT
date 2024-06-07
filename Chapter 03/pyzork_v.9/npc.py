# npc.py
class NPC:
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image

    def talk(self, player):
        if self.name == "Wizard":
            print("Wizard:", "Greetings, young adventurer! I can offer you advice on your journey.")
            print("Wizard:", "If you're stuck, try asking for hints or suggestions.")
        else:
            print(f"{self.name}:", "There's nothing much I have to say right now.")

    def trade(self, player):
        # Define trading logic with the NPC.
        pass

    def attack(self, player):
        # Define combat logic with the NPC.
        pass