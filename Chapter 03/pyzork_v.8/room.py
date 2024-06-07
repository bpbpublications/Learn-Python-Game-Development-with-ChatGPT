class Room:
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image
        self.items = []
        self.npcs = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def add_npc(self, npc):
        self.npcs.append(npc)