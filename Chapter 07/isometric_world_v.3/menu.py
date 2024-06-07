import pygame

class Menu:
    def __init__(self, x, y, tile_x, tile_y, tiles_sprites, tile_size=48):
        self.x = x
        self.y = y
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tiles = tiles_sprites
        self.tile_size = tile_size
        self.width = len(self.tiles) * tile_size
        self.height = tile_size
        self.active = False
        self.selected_tile = None

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (100, 100, 100),
                             (self.x, self.y, self.width, self.height))
            for idx, tile in enumerate(self.tiles):
                screen.blit(pygame.transform.scale(tile, 
                                                   (self.tile_size,
                                                    self.tile_size)),
                            (self.x + idx * self.tile_size, self.y))

    def is_mouse_over(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            return True
        return False

    def get_selected_tile(self, mouse_pos):
        if self.is_mouse_over(mouse_pos):
            idx = (mouse_pos[0] - self.x) // self.tile_size
            return self.tiles[idx]
        return None
    
    def get_selected_tile_index(self, mouse_pos):
        if self.is_mouse_over(mouse_pos):
            idx = (mouse_pos[0] - self.x) // self.tile_size
            return idx
        return None
