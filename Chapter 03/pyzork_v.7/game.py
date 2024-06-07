# main.py
from player import Player
from world import World
from action import Action
from room import Room
from npc import NPC
from item import Item

def create_world():
    world = World()

    # # Create rooms
    #room1 = Room("Forest Clearing", "You are in a tranquil forest clearing.")
    # room2 = Room("Cave Entrance", "A dark cave entrance looms ahead.")
    # room3 = Room("Cave Interior", "The cave is dimly lit with mysterious symbols on the walls.")
    # room4 = Room("Riddle Chamber", "You stand in a chamber filled with riddles.")
    # room5 = Room("Treasure Room", "You have found a room filled with glittering treasures!")
    
    # bridge = Room("Bridge", "A sturdy stone bridge spans a deep chasm.")
    # world.add_room(bridge)

    # # Add rooms to the world
    # world.add_room(room1)
    # world.add_room(room2)
    # world.add_room(room3)
    # world.add_room(room4)
    # world.add_room(room5)

    # # Create links between rooms
    # world.add_link(room1, room2, "north")
    # world.add_link(room2, room3, "east")
    # world.add_link(room3, room4, "south")
    # world.add_link(room4, room5, "west")
    # world.add_link(bridge, room2, "north")
    # world.add_link(bridge, room3, "south")
    
    #  # Create NPCs
    # wizard = NPC("Wizard", "A wise and friendly wizard greets you.")    
    # troll = NPC("Troll", "A large and menacing troll guards the bridge.")    

    # # Add NPCs to rooms
    # room3.add_npc(wizard)  # Add the wizard to the cave interior
    # bridge.add_npc(troll)
    
    # # Create items
    # axe = Item("Axe", "A sharp and sturdy axe for chopping wood.")

    # # Add items to rooms
    # room1.add_item(axe)  # Add the axe to the forest clearing

    return world

def create_actions():
    actions = [
        Action("Move",
               "Move to another room",
               ["move"],
               context="link"),
        Action("Throw",
               "Remove an object from inventory",
               ["throw", "drop", "remove", "place"],
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

class GameEngine:
    def __init__(self) -> None:
        self.player = Player()
        self.world = create_world()
        self.actions = create_actions()
    
        self.current_room = None 
        
    def observe(self):
        if self.current_room:
            items = ", ".join([item.name for item in self.current_room.items])
            npcs = ", ".join([npc.description for npc in self.current_room.npcs])
            inventory = ", ".join([item.name for item in self.player.inventory])
            actions = ", ".join([action.name for action in self.actions])
            return dict(description=self.current_room.description,
                        image=self.current_room.image,
                        items=items,
                        npcs=npcs,
                        inventory=inventory,
                        actions=actions,
                        )
        else:
            return dict(description="You are in a void.",
                        image=None,
                        items=None,
                        npcs=None,
                        inventory=None,
                        actions=None,
                        )    
    
    def add_object(self,
                   object_type,
                   object_name,
                   object_description,
                   object_image,
                   object_rooms,
                   object_special
                   ):
        if object_type == "ROOM":
            new_room = Room(object_name, object_description, object_image)
            self.world.add_room(new_room)
            if self.current_room is None:
                self.current_room = new_room
            if object_rooms and object_special:
                rooms = zip(object_rooms, object_special)
                #add links to room
                for room, dir in rooms:
                    link_room = self.world.rooms.get(room, None)
                    if link_room:
                        self.world.add_link(new_room,
                                            link_room,
                                            dir.lower())                    
                
        elif object_type == "ITEM":
            pass
        elif object_type == "NPC":
            pass
                     
    def parse_command(self, command):
        # parse player input.        
        parts = command.split()
        
        if len(parts) >= 2:
            verb = parts[0].lower()
            obj_name = " ".join(parts[1:]).lower()

            # Find matching action based on verb
            matching_actions = [action for action in self.actions if verb in action.verbs]
            
            if matching_actions:
                action = matching_actions[0]
                obj = None

                if action.context == "link":
                    # Check if the room has a link in the specified direction
                    direction = obj_name
                    target_room = self.world.links.get((self.current_room, direction), None)

                    if target_room:
                        self.current_room = target_room
                        return f"You move to the {direction}"
                       
                    else:
                        return "You can't go that way."                       
                    
                if action.context == "inventory":
                        # Check if the player has the object in inventory
                    item = next((item for item in self.player.inventory if obj_name == item.name.lower()), None)

                    if item:
                        if action.name == "Throw":
                            # item.use(player)  # remove line
                            self.player.remove_item(item)
                            self.current_room.add_item(item)
                        else:
                            return f"You can't do that with the {item.name}."
                    else:
                        return "Item not found."

                elif action.context == "room":
                    # Check if the object is in the same room
                    item = next((item for item in self.current_room.items if obj_name == item.name.lower()), None)

                    if item:
                        if action.name == "Pickup":
                            self.player.add_item(item)  # Add the item to player's inventory
                            self.current_room.remove_item(item)  # Remove the item from the room
                            return f"You picked up the {item.name}."
                        else:
                            return f"You can't do that with the {item.name}"
                    else:
                        return "Item not found."
                
                if action.context == "npc":
                    # Check if the NPC is in the same room
                    npc = next((npc for npc in self.current_room.npcs if obj_name == npc.name.lower()), None)

                    if npc:
                        if action.name == "Talk":                            
                            return npc.talk(self.player)
                        else:
                            return f"You can't do that with the {npc.name}"                            
                    else:
                        return "NPC not found."
                        
                if obj:
                    if action.can_execute(self.player, obj):
                        action.execute(self.player, obj)
                    else:
                        return "You can't do that."
                else:
                    return "Object not found."
            else:
                return "Invalid action."
        
    



