import pygame


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        # Explosion update logic
        pass

    def draw(self, screen):
        # Draw explosion (for simplicity, we use a circle)
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 30)
