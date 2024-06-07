# filename: asteroids_game.py

import pygame
import pymunk
import math

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

# Create the ship
ship_body = pymunk.Body(SHIP_MASS, pymunk.moment_for_circle(SHIP_MASS, 0, SHIP_RADIUS))
ship_body.position = WIDTH // 2, HEIGHT // 2
ship_shape = pymunk.Circle(ship_body, SHIP_RADIUS)
ship_shape.friction = SHIP_FRICTION
space.add(ship_body, ship_shape)

def draw_ship():
    pygame.draw.polygon(screen, (255, 255, 255), [
        ship_body.local_to_world((-SHIP_RADIUS, SHIP_RADIUS)),
        ship_body.local_to_world((SHIP_RADIUS, SHIP_RADIUS)),
        ship_body.local_to_world((0, -2*SHIP_RADIUS)),
        ship_body.local_to_world((-SHIP_RADIUS, SHIP_RADIUS))
    ])

def handle_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        force = (-SHIP_FORCE * math.sin(ship_body.angle), -SHIP_FORCE * math.cos(ship_body.angle))
        ship_body.apply_force_at_local_point(force, (0, 0))

def wrap_position(body):
    x, y = body.position
    if x < 0: x += WIDTH
    elif x > WIDTH: x -= WIDTH
    if y < 0: y += HEIGHT
    elif y > HEIGHT: y -= HEIGHT
    body.position = x, y

def game_loop():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input()
        space.step(1/60)
        wrap_position(ship_body)

        screen.fill((0, 0, 0))
        draw_ship()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()