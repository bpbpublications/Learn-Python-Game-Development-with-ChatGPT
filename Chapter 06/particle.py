import pygame
import pymunk
import random
import math

class SmokeParticle:
    def __init__(self, x, y, velocity, lifespan):
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 5))
        self.body.position = x, y
        self.body.velocity = velocity   
        self.body.velocity_func = self.no_gravity     
        self.lifespan = lifespan
        self.life_elapsed = 0
        self.shape = pymunk.Circle(self.body, 5)
        self.shape.collision_type = 99  # A unique collision type for smoke particles
        self.shape.sensor = True  # Ensure that they don't interfere with other bodies
        self.radius = 5
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)  # Create a transparent surface
        pygame.draw.circle(self.image, (150, 150, 150), (5, 5), self.radius) 
        
    def update(self, dt):
        self.life_elapsed += dt
        self.radius += .1
        if self.life_elapsed >= self.lifespan:
            return False
        return True
    
    def no_gravity(self, body, gravity, damping, dt):
        body.velocity *= 0.99  # A slight damping to make smoke slow down over time

    def draw(self, screen, offset_x):
        alpha = int(255 * (1 - self.life_elapsed / self.lifespan))
        temp_image = self.image.copy()  # Copy the image to not modify the original
        temp_image.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)  # Apply the alpha
        screen.blit(temp_image, (int(self.body.position.x + offset_x) - 5, int(self.body.position.y) - 5))


class ParticleSystem:
    def __init__(self, space):
        self.space = space
        self.particles = []
        
    def emit(self, x, y, velocity, lifespan):
        particle = SmokeParticle(x, y, velocity, lifespan)
        self.particles.append(particle)
        self.space.add(particle.body, particle.shape)
        
    def emit_many(self, x, y, count, variance=(0, 0), speed=100, particle_lifetime=1.0):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            velocity = (math.cos(angle) * speed + random.uniform(-variance[0], variance[0]),
                        math.sin(angle) * speed + random.uniform(-variance[1], variance[1]))
            self.emit(x, y, velocity, particle_lifetime)
        
    def update(self, dt):
        for particle in self.particles[:]:
            alive = particle.update(dt)
            if not alive:
                self.space.remove(particle.body, particle.shape)
                self.particles.remove(particle)
                
    def draw(self, screen, offset_x):
        for particle in self.particles:
            particle.draw(screen, offset_x)
