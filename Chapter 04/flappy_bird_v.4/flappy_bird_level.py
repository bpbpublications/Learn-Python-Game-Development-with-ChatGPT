import pygame
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
LEVEL_FILE_NAME = "level_v.4.json"

# Classes reused from the main game
class Player:
    def __init__(self, x=100, y=300):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, 40, 40))

class Obstacle:
    def __init__(self, x, height):
        self.x = x
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, 0, 50, self.height))
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.height + 150, 50, SCREEN_HEIGHT - self.height - 150))

class Reward:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, REWARD_COLOR, (self.x, self.y, 20, 20))


# Initialize
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Level Editor")
font = pygame.font.Font(None, 36)

# Variables
player = Player()
obstacles = []
rewards = []
scroll_x = 0
mode = None  # Either 'O' for Obstacle or 'R' for Reward

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                mode = 'O'
            elif event.key == pygame.K_r:
                mode = 'R'
            elif event.key == pygame.K_s:  # Save
                with open(LEVEL_FILE_NAME, "w") as f:
                    json.dump({"obstacles": [(o.x, o.height) for o in obstacles], "rewards": [(r.x, r.y) for r in rewards]}, f)
            elif event.key == pygame.K_l:  # Load
                with open(LEVEL_FILE_NAME, "r") as f:
                    data = json.load(f)
                    obstacles = [Obstacle(x, h) for x, h in data["obstacles"]]
                    rewards = [Reward(x, y) for x, y in data["rewards"]]
            elif event.key == pygame.K_RIGHT:
                scroll_x -= 20
            elif event.key == pygame.K_LEFT:
                scroll_x += 20
        elif event.type == pygame.MOUSEBUTTONDOWN and mode:
            x, y = event.pos
            x -= scroll_x
            if mode == 'O':
                obstacles.append(Obstacle(x, y))
            elif mode == 'R':
                rewards.append(Reward(x, y))

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    player.draw()

    for obstacle in obstacles:
        obstacle.draw()

    for reward in rewards:
        reward.draw()

    # Scrolling
    for obstacle in obstacles:
        obstacle.x += scroll_x
    for reward in rewards:
        reward.x += scroll_x
    scroll_x = 0

    pygame.display.update()

# Quit
pygame.quit()
