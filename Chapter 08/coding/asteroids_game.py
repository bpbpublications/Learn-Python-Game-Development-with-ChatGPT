# filename: asteroids_game.py

# ... other code ...

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('actual_path_to_your_image_file')  # Load the asteroid image
        self.image = pygame.transform.scale(self.image, (20, 20))  # Scale the image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH)
        self.rect.y = random.randrange(SCREEN_HEIGHT)
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randrange(SCREEN_WIDTH)

# ... other code ...