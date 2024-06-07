# main.py
from player import Player
from world import World
from action import Action
from room import Room
from npc import NPC
from item import Item

def create_world():
    world = World()

    # Create rooms
    room1 = Room("Forest Clearing", "You are in a tranquil forest clearing.")
    room2 = Room("Cave Entrance", "A dark cave entrance looms ahead.")
    room3 = Room("Cave Interior", "The cave is dimly lit with mysterious symbols on the walls.")
    room4 = Room("Riddle Chamber", "You stand in a chamber filled with riddles.")
    room5 = Room("Treasure Room", "You have found a room filled with glittering treasures!")

    # Add rooms to the world
    world.add_room(room1)
    world.add_room(room2)
    world.add_room(room3)
    world.add_room(room4)
    world.add_room(room5)

    # Create links between rooms
    world.add_link(room1, room2, "north")
    world.add_link(room2, room3, "east")
    world.add_link(room3, room4, "south")
    world.add_link(room4, room5, "west")
    
     # Create NPCs
    wizard = NPC("Wizard", "A wise and friendly wizard greets you.")

    # Add NPCs to rooms
    room3.add_npc(wizard)  # Add the wizard to the cave interior
    
    # Create items
    axe = Item("Axe", "A sharp and sturdy axe for chopping wood.")

    # Add items to rooms
    room1.add_item(axe)  # Add the axe to the forest clearing

    return world

def create_actions():
    actions = [
        Action("Move",
               "Move to another room",
               ["move"],
               context="link"),
        Action("Throw",
               "Remove an object from inventory",
               ["throw", "drop", "remove", "place"]
               context="inventory"),
        Action("Talk",
               "Talk to an NPC",
               ["talk"],
               context="npc"),
        Action("Attack",
               "Attack an NPC",
               ["attack"],
               context="npc"),
        Action("Pickup",
               "Pick up an item",
               ["pickup"],
               context="room")
    ]
    return actions

def main():
    # Initialize the game world, create rooms, items, NPCs, and links.

    player = Player()
    world = create_world()

    actions = create_actions()
    
    current_room = world.rooms["Forest Clearing"]  # Start in the forest clearing

    # Game loop
    while True:
        # Display current room description, inventory, and available actions.
        print(current_room.description)
        print("Items: ", ", ".join([item.name for item in current_room.items]))
        print("NPCs: ", ", ".join([npc.description for npc in current_room.npcs]))
        print("Inventory: ", ", ".join([item.name for item in player.inventory]))
        print("Available Actions: ", ", ".join([action.name for action in actions]))
        
        # Get player input.
        command = input("Enter your command: ")
        parts = command.split()
        
        if len(parts) >= 2:
            verb = parts[0].lower()
            obj_name = " ".join(parts[1:]).lower()

            # Find matching action based on verb
            matching_actions = [action for action in actions if verb in action.verbs]
            
            if matching_actions:
                action = matching_actions[0]
                obj = None

                if action.context == "link":
                    # Check if the room has a link in the specified direction
                    direction = obj_name
                    target_room = world.links.get((current_room, direction), None)

                    if target_room:
                        current_room = target_room
                        print("You move to the", direction)
                        continue
                    else:
                        print("You can't go that way.")
                        continue
                    
                if action.context == "inventory":
                        # Check if the player has the object in inventory
                    item = next((item for item in player.inventory if obj_name == item.name.lower()), None)

                    if item:
                        if action.name == "Throw":
                            # item.use(player)  # remove line
                            player.remove_item(item)
                            current_room.add_item(item)
                        else:
                            print(f"You can't do that with the {item.name}.")
                    else:
                        print("Item not found.")

                elif action.context == "room":
                    # Check if the object is in the same room
                    item = next((item for item in current_room.items if obj_name == item.name.lower()), None)

                    if item:
                        if action.name == "Pickup":
                            player.add_item(item)  # Add the item to player's inventory
                            current_room.remove_item(item)  # Remove the item from the room
                            print(f"You picked up the {item.name}.")
                        else:
                            print("You can't do that with the", item.name)
                    else:
                        print("Item not found.")
                
                if action.context == "npc":
                    # Check if the NPC is in the same room
                    npc = next((npc for npc in current_room.npcs if obj_name == npc.name.lower()), None)

                    if npc:
                        if action.name == "Talk":
                            npc.talk(player)  # Call the talk method of the NPC
                            continue
                        else:
                            print("You can't do that with the", npc.name)
                            continue
                    else:
                        print("NPC not found.")
                        continue  
                if obj:
                    if action.can_execute(player, obj):
                        action.execute(player, obj)
                    else:
                        print("You can't do that.")
                else:
                    print("Object not found.")
            else:
                print("Invalid action.")

        # Update game state and respond to player actions.
        # Check for game over conditions or win conditions.

if __name__ == "__main__":
    main()
