import pygame
import random

def generate_landscape(surface_width, flat_area_start, flat_area_end):
    """
    Generates a random hilly and mountainous landscape with a flat landing area.

    Args:
        surface_width (int): Width of the planet's surface.
        flat_area_start (int): Starting x-coordinate of the flat landing area.
        flat_area_end (int): Ending x-coordinate of the flat landing area.

    Returns:
        list: A list of y-coordinates representing the surface of the planet.
    """
    surface = []

    for x in range(surface_width):
        if x < flat_area_start or x > flat_area_end:
            surface.append(random.randint(100, 400))  # Random hills and mountains
        else:
            surface.append(500)  # Flat landing area

    return surface

def render_landscape(window, planet_surface):
    """
    Renders the planet's landscape on the given window.

    Args:
        window (pygame.Surface): The game window surface.
        planet_surface (list): List of y-coordinates representing the surface of the planet.
    """
    for x, y in enumerate(planet_surface):
        pygame.draw.line(window, (255, 255, 255), (x, window.get_height()), (x, window.get_height() - y))
