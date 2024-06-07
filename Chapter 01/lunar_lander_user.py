import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (150, 150, 150)
LANDER_COLOR = (255, 255, 255)
SCORE_COLOR = (255, 255, 255)
# GENERATED WITH PROMPT
# Please write me a lunar lander game in Python. When the lander crashes display an explosion and deduct 100 from the player's score. When the lander lands successfully display fireworks and add 1000 to the player's score. Display the player's score in the top right corner of the window. 

# Make the lander white in color and the background black with stars. The surface of the planet is represented with a line. The surface should be hilly and mountainous but there should be a flat area large enough for the lander to land on.



FONT_SIZE = 24

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lunar Lander Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load sounds
explosion_sound = pygame.mixer.Sound("explosion.wav")
fireworks_sound = pygame.mixer.Sound("fireworks.wav")

# Initialize game variables
player_score = 0
lander_x = WIDTH // 2
lander_y = 50
lander_velocity = 0
gravity = 0.5
thrust = -1
surface_y = HEIGHT - 50

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        lander_velocity += thrust

    # Update lander position and velocity
    lander_y += lander_velocity
    lander_velocity += gravity

    # Check for collision with surface
    if lander_y >= surface_y:
        if abs(lander_velocity) > 5:
            explosion_sound.play()
            player_score -= 100
        else:
            fireworks_sound.play()
            player_score += 1000
        lander_y = surface_y

    # Clear the screen
    screen.fill(BLACK)

    # Draw surface
    pygame.draw.line(screen, LINE_COLOR, (0, surface_y), (WIDTH, surface_y), 2)

    # Draw lander
    pygame.draw.rect(screen, LANDER_COLOR, (lander_x, lander_y, 20, 20))

    # Draw player score
    font = pygame.font.Font(None, FONT_SIZE)
    score_text = font.render(f"Score: {player_score}", True, SCORE_COLOR)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()