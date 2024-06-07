def parse_command(self, command, player_name):
    player = self.world.players[player_name]
    if player is None:
        return "Player not in world"