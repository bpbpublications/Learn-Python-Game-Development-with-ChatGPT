import pygame
import pymunk
import random
import math

# Initialize Pygame and Pymunk
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Physics with Pygame and Pymunk")
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0.0, 900.0)

# Create ground
ground = pymunk.Segment(space.static_body, (0, height), (width, height), 1)
ground.elasticity = 0.95
space.add(ground)

# Function to create a ball
def create_ball(space, x, y):
    mass = 1
    radius = 20
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.95
    space.add(body, shape)
    return shape

# Function to create a box
def create_box(space, x, y):
    mass = 1
    size = 40
    moment = pymunk.moment_for_box(mass, (size, size))
    body = pymunk.Body(mass, moment)
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (size, size))
    shape.elasticity = 0.95
    space.add(body, shape)
    return shape

# Create 10 balls and 10 boxes at random positions
for i in range(10):
    x = random.randint(100, 700)
    y = random.randint(100, 400)
    create_ball(space, x, y)

    x = random.randint(100, 700)
    y = random.randint(100, 400)
    create_box(space, x, y)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((255, 255, 255))

    # Update physics
    space.step(1/50.0)

    # Draw objects
    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            x, y = shape.body.position
            pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), int(shape.radius), 0)
        elif isinstance(shape, pymunk.Poly):
            body = shape.body
            vertices = [p.rotated(body.angle) + body.position for p in shape.get_vertices()]
            vertices = [(int(x), int(y)) for x, y in vertices]
            #vertices = [p + body.position for p in shape.get_vertices()]  # uncomment to see boxes not rotate
            pygame.draw.polygon(screen, (255, 0, 0), vertices)

    pygame.draw.line(screen, (0, 0, 0), (0, height), (width, height), 2)

    # Flip screen
    pygame.display.flip()

    # Tick
    clock.tick(50)

pygame.quit()
