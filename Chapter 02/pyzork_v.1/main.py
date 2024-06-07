# main.py
from player import Player
from world import World
from action import Action

def main():
    # Initialize the game world, create rooms, items, NPCs, and links.

    player = Player()
    world = World()

    # Define actions
    actions = [
        Action("Move", "Move to another room", ["move"], context="link"),
        Action("Throw", "Throw an object", ["throw"], context="inventory"),
        Action("Talk", "Talk to an NPC", ["talk"], context="npc"),
        Action("Attack", "Attack an NPC", ["attack"], context="npc"),
        Action("Pickup", "Pick up an item", ["pickup"], context="room")
    ]

    # Game loop
    while True:
        # Display current room description, inventory, and available actions.
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
                    pass
                elif action.context == "inventory":
                    # Check if the player has the object in inventory
                    pass
                elif action.context == "npc":
                    # Check if the NPC is in the same room
                    pass
                elif action.context == "room":
                    # Check if the object is in the same room
                    pass

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
