import pygame
import random
import landscape3 as ls

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

# Landscape parameters
SURFACE_WIDTH = 800
LANDING_AREA_WIDTH = 75

# Generate the planet's landscape
landscape = ls.generate_landscape(WINDOW_WIDTH, WINDOW_HEIGHT)

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
    
    # Render the planet's landscape
    ls.render_landscape(window, landscape)
    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
