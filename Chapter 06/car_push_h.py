import pygame
import pymunk
import random
import math
from particle import ParticleSystem

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 900)
space.damping = 0.9

particle_system = ParticleSystem(space)

car_body = pymunk.Body(1000, pymunk.moment_for_box(1000, (80, 30)))
car_body.position = 400, 500
car_poly = pymunk.Poly.create_box(car_body, (80, 30))
car_poly.friction = 0.7
space.add(car_body, car_poly)

wheels = []
for offset in [-30, 30]:
    wheel_body = pymunk.Body(50, pymunk.moment_for_circle(50, 0, 15))
    wheel_body.position = car_body.position.x + offset, car_body.position.y + 15
    wheel_shape = pymunk.Circle(wheel_body, 15)
    wheel_shape.friction = 1.0
    space.add(wheel_body, wheel_shape)
    wheels.append(wheel_body)
    slide_joint = pymunk.SlideJoint(car_body, wheel_body, (offset, 15), (0, 0), 0, 25)
    space.add(slide_joint)
    pin_joint = pymunk.PivotJoint(car_body, wheel_body, (car_body.position.x + offset, car_body.position.y + 15))
    pin_joint.collide_bodies = False
    space.add(pin_joint)

ground = pymunk.Segment(space.static_body, (-10000, 580), (10000, 580), 1)
ground.friction = 1.0
space.add(ground)

clouds = [(random.randint(0, 10000), random.randint(100, 500)) for _ in range(100)]

obstacles = []
for i in range(20):
    x = random.randint(0, 10000)
    width = random.randint(450, 450)
    triangle = pymunk.Body(body_type=pymunk.Body.STATIC)
    triangle_shape = pymunk.Poly(triangle, [(x, 580), (x + width // 2, 580 - random.randint(20, 150)), (x + width, 580)])
    triangle_shape.friction = 1.0
    space.add(triangle, triangle_shape)
    obstacles.append(triangle_shape)

FONT_HEIGHT = 24
font = pygame.font.SysFont(None, FONT_HEIGHT)
car_force = 20000
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        car_body.apply_force_at_local_point((car_force, 0), (0, 0))
        particle_system.emit(car_body.position.x - 40,
                             car_body.position.y,
                             (car_body.velocity.x * 0.1,
                              -100 + random.uniform(-100, 20)),
                             2)
    if keys[pygame.K_d]:
        car_body.apply_force_at_local_point((-car_force, 0), (0, 0))
        particle_system.emit(car_body.position.x - 40,
                             car_body.position.y,
                             (car_body.velocity.x * 0.1,
                              -100 + random.uniform(-120, 20)),
                             2)
    if keys[pygame.K_f]:
        car_force += 1000

    space.step(1/60.0)
    screen.fill((135, 206, 235))

    offset_x = WIDTH // 2 - int(car_body.position.x)
    
    for cloud_x, cloud_y in clouds:
        pygame.draw.ellipse(screen, (255, 255, 255), (cloud_x + offset_x - 50, cloud_y - 25, 100, 50))

    for obstacle in obstacles:
        pygame.draw.polygon(screen, (50, 50, 50), [(v[0] + offset_x, v[1]) for v in obstacle.get_vertices()])

    pygame.draw.polygon(screen, (0, 0, 255), [v.rotated(car_body.angle) + car_body.position + (offset_x, 0) for v in car_poly.get_vertices()])
    
    for wheel in wheels:
        pygame.draw.circle(screen, (64, 128, 255), (int(wheel.position.x + offset_x), int(wheel.position.y)), 15)
        angle = wheel.position.x * -0.1  # Assuming wheel radius as 15, this gives a rotation for the wheel
        pygame.draw.arc(screen, (0, 0, 0), (int(wheel.position.x + offset_x) - 15, int(wheel.position.y) - 15, 30, 30), angle, angle + .1, 15)
        angle = angle + math.pi / 2
        pygame.draw.arc(screen, (0, 0, 0), (int(wheel.position.x + offset_x) - 15, int(wheel.position.y) - 15, 30, 30), angle, angle + .1, 15)
        angle = angle + math.pi / 2
        pygame.draw.arc(screen, (0, 0, 0), (int(wheel.position.x + offset_x) - 15, int(wheel.position.y) - 15, 30, 30), angle, angle + .1, 15)
        angle = angle + math.pi / 2
        pygame.draw.arc(screen, (0, 0, 0), (int(wheel.position.x + offset_x) - 15, int(wheel.position.y) - 15, 30, 30), angle, angle + .1, 15)

    pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 3)
    
    particle_system.update(1/60.0)
    particle_system.draw(screen, offset_x)

    
    speed_text = font.render(f"Speed: {int(car_body.velocity.x)}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 10))
    friction_text = font.render(f"Force: {car_force:.2f}", True, (0, 0, 0))
    screen.blit(friction_text, (10, 10 + FONT_HEIGHT))  

    pygame.display.flip()
    clock.tick(60)
