import pygame
import random
import json

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (173, 216, 230)  # Light Blue
OBSTACLE_COLOR = (64, 64, 64)       # Dark Grey
REWARD_COLOR = (255, 255, 0)        # Yellow
PLAYER_COLOR = (255, 0, 0)          # Red

GRAVITY_ACCELERATION = 0.2  # Adjust the gravity acceleration value
MAX_GRAVITY = .6
JUMP_STRENGTH = -10  # Adjust the jump strength (negative value for upward motion)
MAX_VELOCITY = -10

LEVEL_FILE_NAME = "level_v.4.json"

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

        
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, cols, rows):
        super().__init__()        
        self.velocity = 0
        self.gravity = 0
        self.frames = []
        sprite_width = sprite_sheet.get_width() // cols
        sprite_height = sprite_sheet.get_height() // rows
        
        for i in range(rows):
            for j in range(cols):
                frame = sprite_sheet.subsurface(pygame.Rect(
                    j * sprite_width,
                    i * sprite_height,
                    sprite_width,
                    sprite_height,
                    ))
                self.frames.append(frame)
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image = self.frames[self.current_frame]
        self.move()
        self.apply_gravity()
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -self.rect.width
            
    def flap(self):        
        self.velocity = max(MAX_VELOCITY, self.velocity+JUMP_STRENGTH)
        self.gravity = 0
        
    def apply_gravity(self):
        self.gravity = min(MAX_GRAVITY, self.gravity + GRAVITY_ACCELERATION)
        
    def debug_draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)

    def move(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        
    @property
    def x(self):
        return self.rect.x
    
    @x.setter
    def x(self, value):
        self.rect.x = value
    
    @property
    def y(self):
        return self.rect.y
    
    @y.setter
    def y(self, value):
        self.rect.y = value
        

class Obstacle:
    def __init__(self, x, h):
        self.x = x
        self.height = h

    def move(self):
        self.x -= 5  # Adjust the speed of obstacles here

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, 0, 50, self.height))
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.height + 150, 50, SCREEN_HEIGHT - self.height - 150))

class Reward:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x -= 5  # Adjust the speed of rewards here

    def draw(self):
        pygame.draw.rect(screen, REWARD_COLOR, (self.x, self.y, 20, 20))
        
sprite_sheet = pygame.image.load("./images/bird_sprite_sheet_fixed.png")

# Game initialization
all_sprites = pygame.sprite.Group()
player = Bird(100, SCREEN_HEIGHT // 2, sprite_sheet, 2, 2)
all_sprites.add(player)
obstacles = []
rewards = []
score = 0
font = pygame.font.Font(None, 36)

#load level
def load_level():
    with open(LEVEL_FILE_NAME, "r") as f:
        data = json.load(f)
        obstacles = [Obstacle(x, h) for x, h in data["obstacles"]]
        rewards = [Reward(x, y) for x, y in data["rewards"]]
    return obstacles, rewards
        
obstacles, rewards = load_level()

# Create a Clock object to control the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    player.flap()
            elif event.key == pygame.K_g and game_over:
                # Reset the game                
                player.y = SCREEN_HEIGHT // 2
                obstacles, rewards = load_level()             
                score = 0
                game_over = False

    if not game_over:
        # # Generate obstacles and rewards
        # if len(obstacles) == 0 or SCREEN_WIDTH - obstacles[-1].x >= 200:
        #     obstacles.append(Obstacle(SCREEN_WIDTH))

        # if len(rewards) == 0 or SCREEN_WIDTH - rewards[-1].x >= 300:
        #     rewards.append(Reward(SCREEN_WIDTH))

        # Move player, obstacles, and rewards
        all_sprites.update()
        for obstacle in obstacles:
            obstacle.move()
        for reward in rewards:
            reward.move()

        # Check for collisions
        for obstacle in obstacles:
            if player.x + 40 > obstacle.x and player.x < obstacle.x + 50:
                if player.y < obstacle.height or player.y + 40 > obstacle.height + 150:
                    game_over = True

        for reward in rewards:
            if player.x + 40 > reward.x and player.x < reward.x + 20:
                if player.y < reward.y + 20 and player.y + 40 > reward.y:
                    rewards.remove(reward)
                    score += 5

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw player, obstacles, rewards, and score  
    #player.debug_draw()
    all_sprites.draw(screen) 
    for obstacle in obstacles:
        obstacle.draw()
    for reward in rewards:
        reward.draw()
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    debug_text = font.render(f"velocity={round(player.velocity, 2)}, gravity={round(player.gravity, 2)}", True, (0, 1, 0))
    screen.blit(debug_text, (10, 30))

    if game_over:
        game_over_text = font.render("Game Over! Press 'G' to play again.", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 20))

    pygame.display.update()
    clock.tick(30)
# Quit Pygame
pygame.quit()
