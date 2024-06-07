class World:
    def __init__(self):
        self.rooms = {}
        self.items = {}
        self.links = {}
        self.npcs = {}

    def add_room(self, room):
        self.rooms[room.name] = room

    def add_link(self, source_room, target_room, direction):
        self.links[(source_room, direction)] = target_room
        self.links[(target_room, opposite_direction(direction))] = source_room      
    
        
def opposite_direction(direction):
    if direction == "north":
        return "south"
    elif direction == "south":
        return "north"
    elif direction == "east":
        return "west"
    elif direction == "west":
        return "east"