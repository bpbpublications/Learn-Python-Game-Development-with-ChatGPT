if action.context == "link":
    # Check if the room has a link in the specified direction
    direction = obj_name
    target_room_name = self.world.links.get(
        (self.current_room.name, direction), None)

    if target_room_name:
        self.current_room = self.world.rooms[target_room_name]
        return f"You move to the {direction}"
        
    else:
        return "You can't go that way."      