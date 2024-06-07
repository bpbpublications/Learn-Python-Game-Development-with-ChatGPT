import pygame

class Button:
    def __init__(self, x, y, 
                 radius, text,
                 action, 
                 color=(200, 200, 200),
                 text_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.text = text
        self.action = action
        self.color = color
        self.text_color = text_color

    def draw(self, screen, font):
        pygame.draw.circle(screen, self.color,
                           (self.x, self.y), self.radius)
        text_surface = font.render(self.text,
                                   True, self.text_color)
        screen.blit(text_surface, (self.x - text_surface.get_width() // 2,
                                   self.y - text_surface.get_height() // 2))

    def is_mouse_over(self, mouse_pos):
        distance = ((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)**0.5
        return distance <= self.radius
