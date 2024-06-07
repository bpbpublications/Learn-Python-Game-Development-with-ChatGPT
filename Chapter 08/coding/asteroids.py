# filename: asteroids.py

import pygame
import pymunk
import math
import random

# Pygame initialization
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Pymunk initialization
space = pymunk.Space()
space.gravity = (0.0, 0.0)

# Ship parameters
SHIP_RADIUS = 10
SHIP_MASS = 1
SHIP_FRICTION = 0.7
SHIP_FORCE = 100
SHIP_ROTATION_SPEED = 0.05

# Create the ship
ship_body = pymunk.Body(SHIP_MASS, pymunk.moment_for_circle(SHIP_MASS, 0, SHIP_RADIUS))
ship_body.position = WIDTH // 2, HEIGHT // 2
ship_shape = pymunk.Circle(ship_body, SHIP_RADIUS)
ship_shape.friction = SHIP_FRICTION
space.add(ship_body, ship_shape)

# Asteroids parameters
ASTEROID_COUNT = 10

# Create the asteroids
for _ in range(ASTEROID_COUNT):
    size = random.randint(20, 100)
    asteroid_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, size))
    asteroid_body.position = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    asteroid_shape = pymunk.Circle(asteroid_body, size)
    space.add(asteroid_body, asteroid_shape)

# Game loop
running = True
thrust = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                thrust = True
                angle = ship_body.angle
                force = -SHIP_FORCE * math.sin(angle), SHIP_FORCE * math.cos(angle)
                ship_body.apply_force_at_local_point(force, (0, 0))
            elif event.key == pygame.K_a:
                ship_body.angle += SHIP_ROTATION_SPEED
            elif event.key == pygame.K_d:
                ship_body.angle -= SHIP_ROTATION_SPEED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                thrust = False

    # Update physics
    dt = 1/60.0
    space.step(dt)

    # Wrap ship around screen
    x, y = ship_body.position
    if x > WIDTH: x = 0
    if x < 0: x = WIDTH
    if y > HEIGHT: y = 0
    if y < 0: y = HEIGHT
    ship_body.position = x, y

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.polygon(screen, (255, 255, 255), [
        (ship_body.position.x - SHIP_RADIUS, HEIGHT - (ship_body.position.y - SHIP_RADIUS)),
        (ship_body.position.x, HEIGHT - (ship_body.position.y + SHIP_RADIUS)),
        (ship_body.position.x + SHIP_RADIUS, HEIGHT - (ship_body.position.y - SHIP_RADIUS))
    ])
    if thrust:
        pygame.draw.polygon(screen, (255, 0, 0), [
            (ship_body.position.x - SHIP_RADIUS, HEIGHT - (ship_body.position.y + SHIP_RADIUS)),
            (ship_body.position.x, HEIGHT - (ship_body.position.y + SHIP_RADIUS + 10)),
            (ship_body.position.x + SHIP_RADIUS, HEIGHT - (ship_body.position.y + SHIP_RADIUS))
        ])
    for body in space.bodies:
        if isinstance(list(body.shapes)[0], pymunk.Circle) and body != ship_body:
            pygame.draw.circle(screen, (255, 255, 255), (int(body.position.x), HEIGHT - int(body.position.y)), list(body.shapes)[0].radius)
    pygame.display.flip()

pygame.quit()