import pygame


class Explosion:
    def __init__(self, x, y):
        """
        Initialize the Explosion object.

        :param x: x-coordinate of the explosion.
        :param y: y-coordinate of the explosion.
        """
        self.x = x
        self.y = y

    def update(self):
        """
        Update the explosion state.
        """
        pass

    def draw(self, screen):
        """
        Draw the explosion on the screen.

        :param screen: The Pygame screen object.
        """
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 30)

