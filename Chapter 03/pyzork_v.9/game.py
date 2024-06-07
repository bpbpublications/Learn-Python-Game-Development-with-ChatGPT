# main.py
from player import Player
from world import World
from action import Action
from room import Room
from npc import NPC
from item import Item

def create_world():
    world = World("game.db")
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
        self.world = create_world()
        self.actions = create_actions()
    
        self.world.load_world()
        if len(self.world.rooms) > 0:
            # set current room to the first room
            room_name = next(iter(self.world.rooms))
            self.current_room = self.world.rooms[room_name]
        else:
            self.current_room = None
        
    def observe(self, player_name):
        self.world.load_world()   # update the world view of any changes
        player = self.world.players.get(player_name, None)
        if player is None:
            # player needs to be added to the game
            starting_room_name = next(iter(self.world.rooms))
            player = Player(player_name, starting_room_name, True)
            self.world.add_player(player)
        
        if player.current_room:
            room = self.world.rooms[player.current_room]
            players = []
            for name, p in self.world.players.items():
                if p.current_room == player.current_room:
                    players.append(name)                
            players = players
            items = ", ".join([item.name for item in room.items])
            npcs = ", ".join([npc.description for npc in room.npcs])
            inventory = ", ".join([item.name for item in player.inventory])
            actions = ", ".join([action.name for action in self.actions])
            return dict(description=room.description,
                        image=room.image,
                        players=players,
                        items=items,
                        npcs=npcs,
                        inventory=inventory,
                        actions=actions,
                        )
        else:            
            players = []
            for name, p in self.world.players.items():
                if p.current_room is None or p.current_room == '':
                    players.append(name)   
                    
            return dict(description="You are in a void.",
                        image=None,
                        players=players,
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
        
        self.world.load_world()
                     
    def parse_command(self, command, player_name):
        player = self.world.players[player_name]
        if player is None:
            return "Player not in world"
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
                    target_room_name = self.world.links.get((player.current_room, direction), None)

                    if target_room_name:
                        player.current_room = target_room_name
                        self.world.update_player(player)
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
        
    



