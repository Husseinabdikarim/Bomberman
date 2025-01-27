import pygame

from config import TILE_SIZE
from explosion import Explosion


class Bomb:
    bomb_surf = None
    bomb_surf_2 = None

    def __init__(self, x, y, game, bomb_type="player"):
        """
        Initialize the Bomb object.

        :param x: x-coordinate of the bomb.
        :param y: y-coordinate of the bomb.
        :param game: Reference to the Game object.
        :param bomb_type: Type of the bomb ('player' or 'initial').
        """
        self.x = x
        self.y = y
        self.game = game
        self.type = bomb_type  # 'player' for player bombs, 'initial' for random bombs

        # Load bomb images if not already loaded
        if Bomb.bomb_surf is None:
            Bomb.bomb_surf = pygame.transform.scale(
                pygame.image.load("Bomb.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE),
            )
        if Bomb.bomb_surf_2 is None:
            Bomb.bomb_surf_2 = pygame.transform.scale(
                pygame.image.load("initial_bomb.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE),
            )

    def update(self):
        """
        Update the bomb state.
        """
        pass

    def explode(self):
        """
        Trigger the explosion, remove the bomb, and check for chain reactions.
        """
        # Trigger explosion
        explosion = Explosion(self.x, self.y)
        self.game.explosions.append(explosion)

        # Remove the current bomb from the list
        if self in self.game.bombs:
            self.game.bombs.remove(self)

        # Check for neighboring bombs
        neighbors = [
            (self.x + TILE_SIZE, self.y),  # Right
            (self.x - TILE_SIZE, self.y),  # Left
            (self.x, self.y + TILE_SIZE),  # Down
            (self.x, self.y - TILE_SIZE),  # Up
        ]

        for nx, ny in neighbors:
            for bomb in self.game.bombs[:]:  # Check remaining bombs
                if bomb.x == nx and bomb.y == ny:
                    bomb.explode()  # Chain explosion

    def draw(self, screen):
        """
        Draw the bomb on the screen.

        :param screen: The Pygame screen object.
        """
        # Draw the appropriate bomb sprite based on its type
        if self.type == "initial":
            bomb_rect = Bomb.bomb_surf_2.get_rect(
                center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
            )
            screen.blit(Bomb.bomb_surf_2, bomb_rect)
        elif self.type == "player":
            bomb_rect = Bomb.bomb_surf.get_rect(
                center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
            )
            screen.blit(Bomb.bomb_surf, bomb_rect)
