import pygame
import pymunk
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dropping Ball Demo")

# Create a Pygame clock object to control frame rate
clock = pygame.time.Clock()

# Create a Pymunk space
space = pymunk.Space()
space.gravity = (0, -900)  # Set gravity (positive y direction is down)

# Create a ground plane
ground = pymunk.Segment(space.static_body, (0, 0), (SCREEN_WIDTH, 0), 5)
ground.elasticity = 0.8
space.add(ground)

# Create a list to store balls
balls = []
pause = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Get the mouse position
            x, y = pygame.mouse.get_pos()

            # Create a Pymunk circle body and shape
            mass = 10
            radius = 20
            inertia = pymunk.moment_for_circle(mass, 0, radius)
            body = pymunk.Body(mass, inertia)
            body.position = x, SCREEN_HEIGHT - y  # Invert y-axis

            shape = pymunk.Circle(body, radius)
            shape.elasticity = 0.7  # Set elasticity
            space.add(body, shape)
            balls.append(shape)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pause = not pause
        
    if pause:
        continue

    # Clear the screen
    screen.fill(WHITE)

    # Update physics
    dt = 1.0 / 60.0  # 60 FPS
    for _ in range(10):
        space.step(dt)

    # Draw balls
    for ball in balls:
        pos_x, pos_y = ball.body.position
        pygame.draw.circle(screen, RED, (int(pos_x), SCREEN_HEIGHT - int(pos_y)), int(ball.radius))

    # Draw ground
    pygame.draw.line(screen, RED, (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 5)

    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
sys.exit()
