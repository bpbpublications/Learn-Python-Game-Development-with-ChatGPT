class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.items = []

    def add_exit(self, direction, room):
        self.exits[direction] = room

    def add_item(self, item):
        self.items.append(item)

    def display_items(self):
        if self.items:
            items_list = ", ".join(self.items)
            return f"You see: {items_list}"
        else:
            return "There are no items here."

class Player:
    def __init__(self, current_room):
        self.current_room = current_room
        self.inventory = []

    def move(self, direction):
        if direction in self.current_room.exits:
            self.current_room = self.current_room.exits[direction]
            return self.current_room.description
        else:
            return "You can't go that way."

    def take_item(self, item):
        if item in self.current_room.items:
            self.current_room.items.remove(item)
            self.inventory.append(item)
            return f"You have taken the {item}."
        else:
            return f"There's no {item} here."

def create_game():
    # Create rooms
    entrance = Room("Entrance", "You are at the entrance of a dark cave.")
    hallway = Room("Hallway", "You are in a dimly lit hallway.")
    treasure_room = Room("Treasure Room", "You are in a room filled with glittering treasures.")

    # Set up exits
    entrance.add_exit("north", hallway)
    hallway.add_exit("south", entrance)
    hallway.add_exit("east", treasure_room)
    treasure_room.add_exit("west", hallway)

    # Add items to rooms
    entrance.add_item("torch")
    treasure_room.add_item("diamond")
    
    player = Player(entrance)
    return player

def main():
    player = create_game()
    while True:
        print(player.current_room.description)
        print(player.current_room.display_items())
        command = input("What will you do? ").lower().split()
        if command[0] == "go":
            if len(command) > 1:
                direction = command[1]
                result = player.move(direction)
            else:
                result = "Go where?"
        elif command[0] == "take":
            if len(command) > 1:
                item = command[1]
                result = player.take_item(item)
            else:
                result = "Take what?"
        elif command[0] == "quit":
            print("Thanks for playing!")
            break
        else:
            result = "I don't understand that command."
        print(result)

if __name__ == "__main__":
    main()
