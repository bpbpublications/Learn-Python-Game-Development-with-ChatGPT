# filename: asteroids_game.py

import pygame
import random
import math

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = 3
        self.bullets = pygame.sprite.Group()

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT))

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        self.bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = random.randrange(SCREEN_HEIGHT)
        self.speed = random.randint(1, 3)
        self.dir = math.radians(random.randint(0, 360))

    def update(self):
        self.rect.x += self.speed * math.cos(self.dir)
        self.rect.y += self.speed * math.sin(self.dir)

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH)
            self.rect.y = random.randrange(SCREEN_HEIGHT)

def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Asteroids")

    player = Player()
    asteroids = pygame.sprite.Group()

    for i in range(10):
        asteroid = Asteroid()
        asteroids.add(asteroid)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        keys = pygame.key.get_pressed()
        player.update(keys)

        for bullet in player.bullets:
            bullet.update()

        asteroids.update()

        for bullet in player.bullets:
            asteroids_hit = pygame.sprite.spritecollide(bullet, asteroids, True)
            for asteroid in asteroids_hit:
                player.bullets.remove(bullet)
                bullet.kill()

        if pygame.sprite.spritecollideany(player, asteroids):
            running = False

        screen.fill(BLACK)

        player.bullets.draw(screen)
        screen.blit(player.image, player.rect)
        asteroids.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()