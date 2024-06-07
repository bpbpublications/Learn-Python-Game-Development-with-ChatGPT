import pygame
import pymunk
from pymunk.pygame_util import DrawOptions
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SCREEN_COLOR = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Car Demo')
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, -900)

# Ground
ground = pymunk.Segment(space.static_body, (-1000, 100), (1000, 100), 5)
ground.friction = 1.0
space.add(ground)

# Car
car_body = pymunk.Body(100, pymunk.moment_for_box(100, (100, 40)))
car_body.position = (WIDTH / 2, HEIGHT / 2)
car_shape = pymunk.Poly.create_box(car_body, (100, 40))
car_shape.friction = 1.0
space.add(car_body, car_shape)

# Wheels
radii = 20
wheel1 = pymunk.Body(10, pymunk.moment_for_circle(10, 0, radii))
wheel1.position = (car_body.position.x - 40, car_body.position.y - 30)
wheel_shape1 = pymunk.Circle(wheel1, radii)
wheel_shape1.friction = 1.0
joint1 = pymunk.PinJoint(car_body, wheel1, (-40, -20))
space.add(wheel1, wheel_shape1, joint1)

wheel2 = pymunk.Body(10, pymunk.moment_for_circle(10, 0, radii))
wheel2.position = (car_body.position.x + 40, car_body.position.y - 30)
wheel_shape2 = pymunk.Circle(wheel2, radii)
wheel_shape2.friction = 1.0
joint2 = pymunk.PinJoint(car_body, wheel2, (40, -20))
space.add(wheel2, wheel_shape2, joint2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                car_body.apply_force_at_local_point((500, 0), (0, 0))
            elif event.key == pygame.K_d:
                car_body.apply_force_at_local_point((-500, 0), (0, 0))

    screen.fill(SCREEN_COLOR)
    
    # Draw
    options = DrawOptions(screen)
    space.debug_draw(options)
    
    # Drawing wheel spokes
    for wheel in [wheel1, wheel2]:
        for i in range(8):
            angle = i * 45
            x = wheel.position.x + radii * math.cos(angle)
            y = wheel.position.y + radii * math.sin(angle)
            pygame.draw.line(screen, (0, 0, 0), wheel.position, (x, y))
    
    pygame.display.flip()
    space.step(1/60.0)
    clock.tick(60)

pygame.quit()

