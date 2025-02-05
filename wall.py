import pygame
from tile import Tile


class Wall(Tile):
    def __init__(self, x, y, size):
        """
        Initialize the Wall object.

        :param x: x-coordinate of the wall.
        :param y: y-coordinate of the wall.
        :param size: Size of the wall tile.
        """
        super().__init__(x, y, size, 1)  # 1 = Wall tile
        self.color = (19, 17, 26)

    @staticmethod
    def get_walls(tiles):
        """
        Retrieve all wall tiles from the map.

        :return: A list of Wall objects.
        """
        return [tile for row in tiles for tile in row if isinstance(tile, Wall)]

    def draw(self, screen):
        """
        Draw the wall on the screen.

        :param screen: The Pygame screen object.
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(
            screen, (50, 50, 50), (self.x, self.y, self.size, self.size), 1
        )  # Border
