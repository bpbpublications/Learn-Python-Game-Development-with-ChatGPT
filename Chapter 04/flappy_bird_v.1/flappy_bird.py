import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (173, 216, 230)  # Light Blue
OBSTACLE_COLOR = (64, 64, 64)       # Dark Grey
REWARD_COLOR = (255, 255, 0)        # Yellow
PLAYER_COLOR = (255, 0, 0)          # Red

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Classes
class Player:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5

    def jump(self):
        self.velocity = -10  # Negative value to move upwards

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, 40, 40))

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)

    def move(self):
        self.x -= 5  # Adjust the speed of obstacles here

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, 0, 50, self.height))
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.height + 150, 50, SCREEN_HEIGHT - self.height - 150))

class Reward:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(100, 400)

    def move(self):
        self.x -= 5  # Adjust the speed of rewards here

    def draw(self):
        pygame.draw.rect(screen, REWARD_COLOR, (self.x, self.y, 20, 20))

# Game initialization
player = Player()
obstacles = []
rewards = []
score = 0
font = pygame.font.Font(None, 36)

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
                    player.jump()
            elif event.key == pygame.K_g and game_over:
                # Reset the game
                player = Player()
                obstacles = []
                rewards = []
                score = 0
                game_over = False

    if not game_over:
        # Generate obstacles and rewards
        if len(obstacles) == 0 or SCREEN_WIDTH - obstacles[-1].x >= 200:
            obstacles.append(Obstacle(SCREEN_WIDTH))

        if len(rewards) == 0 or SCREEN_WIDTH - rewards[-1].x >= 300:
            rewards.append(Reward(SCREEN_WIDTH))

        # Move player, obstacles, and rewards
        player.move()
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
    player.draw()
    for obstacle in obstacles:
        obstacle.draw()
    for reward in rewards:
        reward.draw()
    
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game Over! Press 'G' to play again.", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 20))

    pygame.display.update()
    clock.tick(30)
# Quit Pygame
pygame.quit()
