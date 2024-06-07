import pygame
import time
import random

pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
game_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# Snake characteristics
snake_block = 10
snake_speed = 15

# Font settings
font_style = pygame.font.SysFont(None, 50)

def message(msg, color):
    rendered_message = font_style.render(msg, True, color)
    game_display.blit(rendered_message, [screen_width / 6, screen_height / 3])

def game_loop():
    game_over = False
    game_paused = False

    # Initial position of the snake
    snake_x = screen_width / 2
    snake_y = screen_height / 2

    # Initial velocity of the snake
    snake_x_change = 0
    snake_y_change = 0

    # Snake body list
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_y_change = -snake_block
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_y_change = snake_block
                    snake_x_change = 0
                elif event.key == pygame.K_SPACE:
                    game_paused = not game_paused

        if not game_paused:
            snake_x += snake_x_change
            snake_y += snake_y_change

            if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
                game_over = True

            game_display.fill(black)
            pygame.draw.rect(game_display, green, [food_x, food_y, snake_block, snake_block])
            snake_head = [snake_x, snake_y]
            snake_list.append(snake_head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            for block in snake_list[:-1]:
                if block == snake_head:
                    game_over = True

            for segment in snake_list:
                pygame.draw.rect(game_display, white, [segment[0], segment[1], snake_block, snake_block])

            pygame.display.update()

            # Check if the snake ate the food
            if snake_x == food_x and snake_y == food_y:
                food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
                food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
                snake_length += 1

            clock.tick(snake_speed)

        else:
            game_display.fill(black)
            message("Paused", red)
            pygame.display.update()
            clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
