import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
TILE_SIZE = 128
ISOMETRIC_WIDTH = TILE_SIZE * 2
ISOMETRIC_HEIGHT = TILE_SIZE
DEPTH = 24

# Colors
SAND = (255, 223, 186)
GRASS = (124, 252, 0)
WATER = (0, 191, 255)
ICE = (240, 255, 255)
BLACK = (0, 0, 0)

# Create screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isometric Tilemap Demo")
clock = pygame.time.Clock()

# Sample tilemap (16x16 array)
tilemap = [['grass', 'sand', 'water', 'ice'] * 4 for _ in range(16)]

# Camera position
camera = [0, 0]

def draw_tile(x, y, terrain):
    colors = {
        'sand': SAND,
        'grass': GRASS,
        'water': WATER,
        'ice': ICE
    }
    # Darker colors for depth
    darker_colors = {
        'sand': (205, 173, 136),
        'grass': (104, 232, 0),
        'water': (0, 141, 205),
        'ice': (200, 215, 215)
    }

    # Convert cartesian coordinates to isometric and apply camera translation
    iso_x = x - y + camera[0]
    iso_y = (x + y) / 2 + camera[1]

    # Adjusting for screen center and scaling tile size
    screen_x = WIDTH // 2 + iso_x * ISOMETRIC_WIDTH // 2
    screen_y = HEIGHT // 4 + iso_y * ISOMETRIC_HEIGHT

    # Draw depth sides
    pygame.draw.polygon(screen, darker_colors[terrain], [
        (screen_x, screen_y + DEPTH),
        (screen_x + ISOMETRIC_WIDTH // 2, screen_y + DEPTH + ISOMETRIC_HEIGHT // 2),
        (screen_x, screen_y + DEPTH + ISOMETRIC_HEIGHT),
        (screen_x - ISOMETRIC_WIDTH // 2, screen_y + DEPTH + ISOMETRIC_HEIGHT // 2),
        (screen_x - ISOMETRIC_WIDTH // 2, screen_y + ISOMETRIC_HEIGHT // 2)
    ])
    pygame.draw.polygon(screen, darker_colors[terrain], [
        (screen_x, screen_y + DEPTH + ISOMETRIC_HEIGHT),
        (screen_x + ISOMETRIC_WIDTH // 2, screen_y + DEPTH + ISOMETRIC_HEIGHT // 2),
        (screen_x + ISOMETRIC_WIDTH // 2, screen_y + ISOMETRIC_HEIGHT // 2)
    ])

    # Draw top tile
    pygame.draw.polygon(screen, colors[terrain], [
        (screen_x, screen_y),
        (screen_x + ISOMETRIC_WIDTH // 2, screen_y + ISOMETRIC_HEIGHT // 2),
        (screen_x, screen_y + ISOMETRIC_HEIGHT),
        (screen_x - ISOMETRIC_WIDTH // 2, screen_y + ISOMETRIC_HEIGHT // 2)
    ])

    # Draw grid overlay
    pygame.draw.lines(screen, BLACK, True, [
        (screen_x, screen_y),
        (screen_x + ISOMETRIC_WIDTH // 2, screen_y + ISOMETRIC_HEIGHT // 2),
        (screen_x, screen_y + ISOMETRIC_HEIGHT),
        (screen_x - ISOMETRIC_WIDTH // 2, screen_y + ISOMETRIC_HEIGHT // 2)
    ])

def handle_input():
    keys = pygame.key.get_pressed()
    speed = .25
    if keys[pygame.K_UP]:
        camera[1] -= speed
    if keys[pygame.K_DOWN]:
        camera[1] += speed
    if keys[pygame.K_LEFT]:
        camera[0] -= speed
    if keys[pygame.K_RIGHT]:
        camera[0] += speed

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_input()

        screen.fill((220, 220, 220))

        for row in range(len(tilemap)):
            for col in range(len(tilemap[row])):
                draw_tile(col, row, tilemap[row][col])

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
