import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Function to draw the snake
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Function to generate a new food position
def generate_food():
    while True:
        x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            return x, y

# Main function
def main():
    global screen, snake, direction, food

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = RIGHT

    food = generate_food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != DOWN:
            direction = UP
        elif keys[pygame.K_DOWN] and direction != UP:
            direction = DOWN
        elif keys[pygame.K_LEFT] and direction != RIGHT:
            direction = LEFT
        elif keys[pygame.K_RIGHT] and direction != LEFT:
            direction = RIGHT

        # Move the snake
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        if new_head == food:
            snake.insert(0, new_head)
            food = generate_food()
        else:
            snake.insert(0, new_head)
            snake.pop()

        # Check for collisions
        if new_head in snake[1:]:
            pygame.quit()
            sys.exit()

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        draw_snake(snake)
        pygame.display.update()

        # Adjust game speed
        clock.tick(FPS)

if __name__ == '__main__':
    main()
