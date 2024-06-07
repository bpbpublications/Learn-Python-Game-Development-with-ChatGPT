import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
FPS = 30

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animated Bird Demo")

# Load the sprite sheet
sprite_sheet = pygame.image.load("./images/bird_sprite_sheet.png")

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, cols, rows):
        super().__init__()
        self.frames = []
        sprite_width = sprite_sheet.get_width() // cols
        sprite_height = sprite_sheet.get_height() // rows
        
        for i in range(rows):
            for j in range(cols):
                frame = sprite_sheet.subsurface(pygame.Rect(
                    j * sprite_width, i * sprite_height, sprite_width, sprite_height))
                self.frames.append(frame)
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image = self.frames[self.current_frame]
        self.rect.x += 5
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -self.rect.width

# Create a sprite group and add the bird to it
all_sprites = pygame.sprite.Group()
# bird = Bird(0, SCREEN_HEIGHT // 2, sprite_sheet, 3, 3)
# all_sprites.add(bird)
birds_cnt = 0
frame = 0

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    if birds_cnt < 9 and frame>9:        
        bird = Bird(0, 100 * birds_cnt, sprite_sheet, 3, 3)
        all_sprites.add(bird)
        birds_cnt += 1
        frame = 0

    # Update
    all_sprites.update()
    
    frame += 1

    # Draw
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
