import pygame


class Tile:
    def __init__(self, x, y, size, tile_type):
        self.x = x
        self.y = y
        self.size = size
        self.tile_type = tile_type  # 0 = Empty, 1 = Wall, 2 = Breakable

    def draw(self, screen):
        # Define colors
        COLORS = {
            0: (193, 245, 241),  # (193,245,241),(227,227,166)
            1: (193, 245, 241),
            2: (150, 75, 0),
        }

        # Draw tile
        pygame.draw.rect(
            screen, COLORS[self.tile_type], (self.x, self.y, self.size, self.size)
        )

        # Draw grid line (border)
        pygame.draw.rect(
            screen, (50, 50, 50), (self.x, self.y, self.size, self.size), 1
        )
