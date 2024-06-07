# player.py
class Player:
    def __init__(self, name, current_room, online):
        self.name = name
        self.current_room = current_room
        self.online = online
        self.inventory = []

    def add_item(self, item):
        # Add an item to the player's inventory.
        self.inventory.append(item)

    def remove_item(self, item):
        self.inventory.remove(item)

    def use_item(self, item):
        item.use(self)

    def take_action(self, action):
        # Handle player actions.
        pass