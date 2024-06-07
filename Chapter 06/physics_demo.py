import sys
import pygame
from pygame.locals import QUIT
import pymunk

# Initialization
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics Demo with Pymunk and Pygame")
clock = pygame.time.Clock()

# Create a Pymunk space
space = pymunk.Space()
space.gravity = (0, -900)

# Display Functions
def to_pygame(p):
    """Convert pymunk to pygame coordinates"""
    return int(p[0]), int(-p[1] + height)


def draw_objects():
    screen.fill((255, 255, 255))

    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            pos = to_pygame(shape.body.position)
            pygame.draw.circle(screen, (0, 0, 255), pos, int(shape.radius), 0)

        elif isinstance(shape, pymunk.Segment):  # static bodies
            body = shape.body
            pv1 = body.position + shape.a.rotated(body.angle)
            pv2 = body.position + shape.b.rotated(body.angle)
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            pygame.draw.lines(screen, (0, 255, 0), False, [p1, p2])

    pygame.display.flip()


# Add a static body (ground)
ground = pymunk.Segment(space.static_body, (0, 50), (width, 50), 5)
ground.friction = 1.0
space.add(ground)

# Add a circle (dynamic rigid body with mass, volume, and elasticity)
mass = 1
radius = 30
moment = pymunk.moment_for_circle(mass, 0, radius)
circle_body = pymunk.Body(mass, moment)
circle_body.position = (width / 2, height / 2)
circle_shape = pymunk.Circle(circle_body, radius)
circle_shape.elasticity = 0.8
circle_shape.friction = 0.5
space.add(circle_body, circle_shape)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw_objects()
    space.step(1/60.0)
    clock.tick(60)

pygame.quit()
sys.exit()
