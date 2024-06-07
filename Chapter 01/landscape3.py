import pygame
import random

def generate_landscape(window_width, window_height):
    points = []
    x = 0
    y = random.randint(250, window_height - 50)
    points.append((x, y))

    while x <= window_width:
        x += random.randint(50, 100)
        y = random.randint(250, window_height - 50)
        points.append((x, y))

    # Create the landing area
    landing_area_start = random.randint(0, len(points) - 1)
    landing_area_end = min(landing_area_start + random.randint(3, 5), len(points) - 1)
    for i in range(landing_area_start, landing_area_end + 1):
        x, y = points[i]
        points[i] = (x, window_height - 50)

    return points

def render_landscape(window, points):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        pygame.draw.line(window, (255, 255, 255), (x1, y1), (x2, y2), 1)