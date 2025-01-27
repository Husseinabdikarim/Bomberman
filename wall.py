import pygame
from tile import Tile


class Wall(Tile):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, 1)  # 1 = Wall tile
        self.color = (19, 17, 26)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(
            screen, (50, 50, 50), (self.x, self.y, self.size, self.size), 1
        )  # Border
