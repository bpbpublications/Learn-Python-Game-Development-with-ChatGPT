# item.py
class Item:
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image

    def use(self, player):
        # Define how the item is used.
        pass