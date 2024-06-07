import pygame


class AIController:
    def __init__(self, player):
        self.player = player

    def get_action(self, game_state):
        state_changes = {}
        
        # Extract relevant game state information
        fighter = game_state[f"fighter_{self.player}"]
        opponent = game_state[f"fighter_{3 - self.player}"]
        round_over = game_state["round_over"]
        
        # Implement your AI logic here
        if not round_over:
            if fighter["alive"]:
                # Example: Simple logic to move towards the opponent
                if fighter["position"].x < opponent["position"].x:
                    state_changes = {
                        "action": "movement",
                        "dx": 1
                    }
                elif fighter["position"].x > opponent["position"].x:
                    state_changes = {
                        "action": "movement",
                        "dx": -1
                    }
                # Add more logic for attacking, jumping, etc.
        
        return state_changes
    
    
class PlayerController:
    def __init__(self, player):
        self.player = player

    def get_action(self, game_state):
        state_changes = {}
        
        # Extract relevant game state information
        fighter = game_state[f"fighter_{self.player}"]
        opponent = game_state[f"fighter_{3 - self.player}"]
        round_over = game_state["round_over"]
        
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