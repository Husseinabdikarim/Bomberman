import pygame


class Tile:
    def __init__(self, x, y, size, tile_type):
        """
        Initialize the Tile object.

        :param x: x-coordinate of the tile.
        :param y: y-coordinate of the tile.
        :param size: Size of the tile.
        :param tile_type: Type of the tile (0 = Empty, 1 = Wall, 2 = Breakable).
        """
        self.x = x
        self.y = y
        self.size = size
        self.tile_type = tile_type  # 0 = Empty, 1 = Wall, 2 = Breakable

    def draw(self, screen):
        """
        Draw the tile on the screen.

        :param screen: The Pygame screen object.
        """
        # Define colors
        COLORS = {
            0: (193, 245, 241),  # Empty tile color
            1: (193, 245, 241),  # Wall tile color
            2: (150, 75, 0),     # Breakable tile color
        }

        # Draw tile
        pygame.draw.rect(
            screen, COLORS[self.tile_type], (self.x, self.y, self.size, self.size)
        )

        # Draw grid line (border)
        pygame.draw.rect(
            screen, (50, 50, 50), (self.x, self.y, self.size, self.size), 1
        )
