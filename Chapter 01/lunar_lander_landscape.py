import pygame
import random
import landscape

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
FLAT_AREA_START = 200
FLAT_AREA_END = 600

# Generate the planet's landscape
planet_surface = landscape.generate_landscape(SURFACE_WIDTH, FLAT_AREA_START, FLAT_AREA_END)

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
    landscape.render_landscape(window, planet_surface)
    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
