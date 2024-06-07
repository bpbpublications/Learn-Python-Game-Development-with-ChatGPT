import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
BACKGROUND_COLOR = (50, 50, 50)
TILE_COLOR = (100, 100, 250)
GRID_COLOR = (70, 70, 70)
TOKEN_COLOR = (255, 0, 0)
BASE_TILE_WIDTH = 128
BASE_TILE_HEIGHT = 74
MAP_WIDTH = 40
MAP_HEIGHT = 40
TOKEN_SIZE = 20
SCROLL_SPEED = 5
ZOOM_SPEED = 0.1

# Create a screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TILES_PATH = "base_tiles/"
tiles_sprites = []

for tile_image in os.listdir(TILES_PATH):
    if tile_image.endswith(('.png', '.jpg', '.jpeg')):  # Checking if the file is an image
        sprite = pygame.image.load(os.path.join(TILES_PATH, tile_image)).convert_alpha()
        tiles_sprites.append(sprite)

tile_map = [[0 for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]

OVERLAYS_PATH = "overlays/"
token_image = "government_overlay.png"
token_sprite = pygame.image.load(os.path.join(OVERLAYS_PATH, token_image)).convert_alpha()


# Font setup for debugging
FONT_SIZE = 24
font = pygame.font.SysFont('arial', FONT_SIZE)

def draw_tile(x, y, width, height):
    """Draw an isometric tile at (x, y)"""
    points = [
        (x, y + height // 2),
        (x + width // 2, y),
        (x, y - height // 2),
        (x - width // 2, y)
    ]
    pygame.draw.polygon(screen, TILE_COLOR, points)
    pygame.draw.polygon(screen, GRID_COLOR, points, 1)
    
def draw_tile_sprite(x, y, sprite, zoom, offset=68):
    """Draw a tile sprite at (x, y) with given zoom."""
    width = sprite.get_width() * zoom
    h_off = (sprite.get_height() - offset) // 2  * zoom
    height = sprite.get_height() * zoom
    resized_sprite = pygame.transform.scale(sprite, (int(width), int(height)))
    screen.blit(resized_sprite, (x - width // 2, y - h_off - height // 2))

def render_text(text, x, y, color=(255, 255, 255)):
    """Utility function to render text on the screen."""
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))
    
def screen_to_world(x, y, camera_offset, zoom):  
    x = (x - SCREEN_WIDTH // 2) / zoom + camera_offset[0]
    y = (SCREEN_HEIGHT // 2 + y - SCREEN_HEIGHT // 2) / zoom + camera_offset[1]  # Flip the y-coordinate here
    return x, y

def world_to_tile(x, y):      
    tile_x = (x / (BASE_TILE_WIDTH // 2) + y / (BASE_TILE_HEIGHT // 2)) // 2
    tile_y = (y / (BASE_TILE_HEIGHT // 2) - x / (BASE_TILE_WIDTH // 2)) // 2
    return int(tile_x), int(tile_y)

def get_tile_in_radius(x, y, radius):
    """Generate tiles in a square radius around (x, y)."""
    for i in range(x - radius, x + radius + 1):
        for j in range(y - radius, y + radius + 1):
            if 0 <= i < MAP_WIDTH and 0 <= j < MAP_HEIGHT:  # Ensure the coordinates are within the map bounds
                yield i, j

def initialize_map():
    """Initialize the tile map with clusters of the same type."""
    NUM_CLUSTERS = 20  # Number of clusters you want
    MAX_RADIUS = 6     # The maximum radius around each seed in which tiles can be affected

    # Start by setting all tiles to a default type
    for i in range(MAP_WIDTH):
        for j in range(MAP_HEIGHT):
            tile_map[i][j] = random.choice(tiles_sprites)

    # Generate seed points
    seeds = [(random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)) for _ in range(NUM_CLUSTERS)]
    
    for seed in seeds:
        seed_tile = random.choice(tiles_sprites)  # Assign a random tile type to this seed
        for x, y in get_tile_in_radius(seed[0], seed[1], MAX_RADIUS):
            distance = ((seed[0]-x)**2 + (seed[1]-y)**2)**0.5  # Calculate distance from seed
            probability = 1 - (distance / (MAX_RADIUS + 1))  # As you move away from the seed, this value decreases
            if random.random() < probability:  # Use this probability to determine if this tile should be of the same type as the seed
                tile_map[x][y] = seed_tile



def main():
    initialize_map()
    token_map_pos = [0, 0]
    camera_offset = [0, 0]
    zoom = 1.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle zooming
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    zoom = min(2.0, zoom + ZOOM_SPEED)
                if event.button == 5:  # Mouse wheel down
                    zoom = max(0.5, zoom - ZOOM_SPEED)

                if event.button == 1:
                    world_x, world_y = screen_to_world(event.pos[0],
                                                       event.pos[1],
                                                       camera_offset,
                                                       zoom)
                    tile_x, tile_y = world_to_tile(world_x, world_y)
                    token_map_pos = [tile_x, tile_y]
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    camera_offset[0] -= SCROLL_SPEED
                if event.key == pygame.K_RIGHT:
                    camera_offset[0] += SCROLL_SPEED
                if event.key == pygame.K_UP:
                    camera_offset[1] -= SCROLL_SPEED
                if event.key == pygame.K_DOWN:
                    camera_offset[1] += SCROLL_SPEED

        # Handle scrolling based on mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < 40 and mouse_x > 0:
            camera_offset[0] -= SCROLL_SPEED
        if mouse_x > SCREEN_WIDTH - 40 and mouse_x < SCREEN_WIDTH - 1:
            camera_offset[0] += SCROLL_SPEED
        if mouse_y < 40 and mouse_y > 0:
            camera_offset[1] -= SCROLL_SPEED
        if mouse_y > SCREEN_HEIGHT - 40 and mouse_y < SCREEN_HEIGHT - 1:
            camera_offset[1] += SCROLL_SPEED

        screen.fill(BACKGROUND_COLOR)

        # Calculate the zoomed tile dimensions
        tile_width = BASE_TILE_WIDTH * zoom
        tile_height = BASE_TILE_HEIGHT * zoom

        # Draw the isometric grid
        for i in range(MAP_WIDTH):
            for j in range(MAP_HEIGHT):
                x = (i - j) * tile_width / 2 + SCREEN_WIDTH // 2
                y = (i + j) * tile_height / 2
                x -= camera_offset[0] * zoom
                y -= camera_offset[1] * zoom
                
                draw_tile_sprite(x, y, tile_map[i][j], zoom)               


        # Calculate the token's screen position and draw the token
        token_x = (token_map_pos[0] - token_map_pos[1]) * tile_width / 2 + SCREEN_WIDTH // 2
        token_y = (token_map_pos[0] + token_map_pos[1]) * tile_height / 2 + (BASE_TILE_HEIGHT // 2) * zoom
        token_x -= camera_offset[0] * zoom
        token_y -= camera_offset[1] * zoom
        draw_tile_sprite(int(token_x), int(token_y), token_sprite, zoom, offset=88)
        

        # Handle the debugging information rendering
        render_text(f'Token Tile Position: {token_map_pos[0]}, {token_map_pos[1]}', 10, 10)
        render_text(f'Mouse Screen Position: {mouse_x}, {mouse_y}', 10, 10 + FONT_SIZE)
        world_x, world_y = screen_to_world(mouse_x, mouse_y, camera_offset, zoom)
        render_text(f'Mouse World Position: {world_x:.2f}, {world_y:.2f}', 10, 10 + 2*FONT_SIZE)
        tile_x, tile_y = world_to_tile(world_x, world_y) 
        render_text(f'Mouse Tile Position: {tile_x}, {tile_y}', 10, 10 + 3*FONT_SIZE)
        render_text(f'Zoom & Offset: {zoom}, {camera_offset}', 10, 10 + 4*FONT_SIZE)
        pygame.display.flip()

main()
