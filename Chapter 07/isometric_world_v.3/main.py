import pygame
import sys
import random
import os
from menu import Menu
from button import Button
import tkinter as tk
from tkinter import filedialog
import pickle


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

BUTTON_RADIUS = 30
BUTTON_SPACING = 10
buttons = [
    Button(SCREEN_WIDTH // 2 - 2 * (BUTTON_RADIUS + BUTTON_SPACING), SCREEN_HEIGHT - 50, BUTTON_RADIUS, "Load", "load"),
    Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, BUTTON_RADIUS, "Save", "save"),
    Button(SCREEN_WIDTH // 2 + 2 * (BUTTON_RADIUS + BUTTON_SPACING), SCREEN_HEIGHT - 50, BUTTON_RADIUS, "Switch", "switch")
]

def load_map():
    global tile_map
    root = tk.Tk()
    root.withdraw()  # This hides the main tkinter window

    filename = filedialog.askopenfilename(title="Select a map to load",
                                          filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")])

    if not filename:  # Check if user canceled the dialog
        return
    try:
        with open(filename, "rb") as file:
            tile_map = pickle.load(file)
            print("Map loaded successfully!")
    except Exception as e:
        print(f"An error occurred while loading the map: {e}")
        
def save_map():
    global tile_map
    root = tk.Tk()
    root.withdraw()  # This hides the main tkinter window

    filename = filedialog.asksaveasfilename(title="Save the map",
                                            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
                                            defaultextension=".pkl")

    if not filename:  # Check if user canceled the dialog
        return

    try:
        with open(filename, "wb") as file:
            pickle.dump(tile_map, file)
            print("Map saved successfully!")
    except Exception as e:
        print(f"An error occurred while saving the map: {e}")
        
def load_tiles_from_folder(folder_path):
    global tiles_sprites
    tiles_sprites = []
    
    for tile_image in os.listdir(folder_path):
        if tile_image.endswith(('.png', '.jpg', '.jpeg')):  # Checking if the file is an image
            sprite = pygame.image.load(os.path.join(folder_path, tile_image)).convert_alpha()
            tiles_sprites.append(sprite)
    print(f"Loaded {len(tiles_sprites)} tiles from {folder_path}")

def switch_tileset():
    global TILES_PATH
    
    root = tk.Tk()
    root.withdraw()  # This hides the main tkinter window

    folder_selected = filedialog.askdirectory(title="Select a tileset folder")

    if not folder_selected:  # Check if user canceled the dialog
        return

    TILES_PATH = folder_selected
    load_tiles_from_folder(folder_selected)


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
    
def draw_tile_sprite_index(x, y, tile_index, zoom, offset=68):
    """Draw a tile sprite at (x, y) with given zoom."""
    sprite = tiles_sprites[tile_index]   
    draw_tile_sprite(x, y, sprite, zoom, offset) 
   
def draw_tile_sprite(x, y, sprite, zoom, offset=68):    
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
    y = (y + BASE_TILE_HEIGHT + 5 ) / zoom + camera_offset[1]  # Flip the y-coordinate here
    return x, y

def world_to_tile(x, y):      
    tile_x = (x / (BASE_TILE_WIDTH // 2) + y / (BASE_TILE_HEIGHT // 2)) // 2
    tile_y = (y / (BASE_TILE_HEIGHT // 2) - x / (BASE_TILE_WIDTH // 2)) // 2
    return int(tile_x), int(tile_y)

def world_to_screen(x, y, camera_offset, zoom):     
    x = (x - camera_offset[0]) * zoom + SCREEN_WIDTH // 2
    y = (y - camera_offset[1]) * zoom  # Flip the y-coordinate back
    return x, y

def tile_to_world(tile_x, tile_y):
    x = (tile_x - tile_y) * (BASE_TILE_WIDTH // 2)
    y = (tile_x + tile_y) * (BASE_TILE_HEIGHT // 2)
    return x, y

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
            #tile_map[i][j] = random.choice(tiles_sprites)
            tile_map[i][j] = random.choice(range(len(tiles_sprites)))

    # Generate seed points
    seeds = [(random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)) for _ in range(NUM_CLUSTERS)]
    
    for seed in seeds:
        #seed_tile = random.choice(tiles_sprites)  # Assign a random tile type to this seed
        seed_tile_index = random.choice(range(len(tiles_sprites)))
        for x, y in get_tile_in_radius(seed[0], seed[1], MAX_RADIUS):
            distance = ((seed[0]-x)**2 + (seed[1]-y)**2)**0.5  # Calculate distance from seed
            probability = 1 - (distance / (MAX_RADIUS + 1))  # As you move away from the seed, this value decreases
            if random.random() < probability:  # Use this probability to determine if this tile should be of the same type as the seed
                #tile_map[x][y] = seed_tile
                tile_map[x][y] = seed_tile_index

def main():
    initialize_map()
    token_map_pos = [0, 0]
    camera_offset = [0, 0]
    zoom = 1.0
    
    menu = None

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
                    for button in buttons:
                        if button.is_mouse_over(event.pos):
                            if button.action == "load":
                                load_map()
                                continue
                            elif button.action == "save":
                                save_map()
                                continue
                            elif button.action == "switch":
                                switch_tileset()
                                continue

                    if menu and menu.active and menu.is_mouse_over(event.pos):
                        #selected_sprite = menu.get_selected_tile(event.pos)
                        selected_sprite_index = menu.get_selected_tile_index(event.pos)
                        if selected_sprite_index is not None:
                            tile_map[menu.tile_x][menu.tile_y] = selected_sprite_index
                            menu.active = False
                        continue

                    world_x, world_y = screen_to_world(event.pos[0], event.pos[1], camera_offset, zoom)
                    tile_x, tile_y = world_to_tile(world_x, world_y)
                    token_map_pos = [tile_x, tile_y]
                    menu = Menu(event.pos[0], event.pos[1], tile_x, tile_y, tiles_sprites)
                    menu.active = True  
                    
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
                
                draw_tile_sprite_index(x, y, tile_map[i][j], zoom)
                
        # Calculate the token's screen position and draw the token        
        w_x, w_y = tile_to_world(token_map_pos[0], token_map_pos[1])
        s_x, s_y = world_to_screen(w_x, w_y, camera_offset, zoom)        
        draw_tile_sprite(s_x, s_y, token_sprite, zoom, offset=20)
        
        if menu:
            menu.draw(screen)     
            
        for button in buttons:
            button.draw(screen, font)   

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
