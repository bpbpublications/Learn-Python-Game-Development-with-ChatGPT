# GENERATE USING PROMPTS
# [SYSTEM] You are a Python game developer. As a developer, you prefer to break down code into smaller modules that can be unit tested and imported as needed. When you get a new request, it is up to you to break down requirements into self-contained modules that can be run and tested. If you are unsure of which modules to develop first please ask the user.

# [USER] Please write me a lunar lander game in Python. When the lander crashes display an explosion and deduct 100 from the player's score. When the lander lands successfully display fireworks and add 1000 to the player's score. Display the player's score in the top right corner of the window. 
# Make the lander white in color and the background black with stars. The surface of the planet is represented with a line. The surface should be hilly and mountainous but there should be a flat area large enough for the lander to land on. 

import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Lunar Lander Game")

# Font for displaying the score
font = pygame.font.Font(None, 36)

# Initialize player score
player_score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    window.fill(BLACK)
    
    # Display player's score in the top right corner
    score_text = font.render(f"Score: {player_score}", True, WHITE)
    score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
    window.blit(score_text, score_rect)
    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
