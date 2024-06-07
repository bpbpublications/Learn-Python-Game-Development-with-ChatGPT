import pygame
    
    
class PlayerController:
    def __init__(self, player):
        self.player = player
        self.difficulty = 1

    def get_action(self, game_state):
        state_changes = {}    
        
        # # Get Key-presses
        key = pygame.key.get_pressed()

        # Check Warrior player controls the game
        if self.player == 1:
            # Player movement coordinates
            if key[pygame.K_a]:
                state_changes = {
                    "action": "movement",
                    "dx": -1
                }
            if key[pygame.K_d]:
                state_changes = {
                    "action": "movement",
                    "dx": 1
                }
            # Player Jumping
            if key[pygame.K_w]:
                state_changes = {
                    "action": "jumping"                        
                }

            # Player Attacking
            if key[pygame.K_z] or key[pygame.K_x]: 
                # Determine which attack type was used
                if key[pygame.K_z]:
                    state_changes = {
                        "action": "attacking",
                        "attack_type": 1
                        }
                if key[pygame.K_x]:
                    state_changes = {
                        "action": "attacking",
                        "attack_type": 2
                        }
        # code for the Wizard is very similar
        # Check Wizard player controls the game
        if self.player == 2:
            # Player movement coordinates
            if key[pygame.K_h]:
                state_changes = {
                    "action": "movement",
                    "dx": -1
                }
            if key[pygame.K_k]:
                state_changes = {
                    "action": "movement",
                    "dx": 1
                }
            # Player Jumping
            if key[pygame.K_u]:
                state_changes = {
                    "action": "jumping"                        
                }
            # Player Attacking
            if key[pygame.K_n] or key[pygame.K_m]:                    
                # Determine which attack type was used
                if key[pygame.K_n]:
                    state_changes = {
                        "action": "attacking",
                        "attack_type": 2
                        }
                if key[pygame.K_m]:
                    state_changes = {
                        "action": "attacking",
                        "attack_type": 2
                        }
        
        return state_changes