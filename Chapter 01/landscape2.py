import pygame
import random

def generate_landscape(surface_width, landing_area_width):
    """
    Generates a landscape with a lowered flat landing area and random mountain peaks.

    Args:
        surface_width (int): Width of the planet's surface.
        landing_area_width (int): Width of the flat landing area.

    Returns:
        list: A list of y-coordinates representing the surface of the planet.
    """
    surface = []

    # Generate a random starting point for the landing area
    landing_area_start = random.randint(0, surface_width - landing_area_width)

    # Create the flat landing area
    for x in range(surface_width):
        if x >= landing_area_start and x < landing_area_start + landing_area_width:
            surface.append(100)  # Flat landing area
        else:
            surface.append(0)  # Initialize surface

    # Generate a random number of mountain peaks
    num_peaks = random.randint(3, 5)
    for _ in range(num_peaks):
        peak_base_width = random.randint(150, 350)  # Random base width between 50 and 250
        peak_center = random.randint(peak_base_width // 2, surface_width - peak_base_width // 2)
        peak_height = random.randint(200, 400)
        for x in range(peak_center - peak_base_width // 2, peak_center + peak_base_width // 2):
            surface[x] = max(surface[x], peak_height - abs(x - peak_center) * 10)

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
