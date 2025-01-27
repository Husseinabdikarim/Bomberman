import pygame

from config import TILE_SIZE
from explosion import Explosion


class Bomb:
    bomb_surf = None

    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        if Bomb.bomb_surf is None:
            Bomb.bomb_surf = pygame.transform.scale(
                pygame.image.load("Bomb.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE),
            )

    def update(self):
        pass

    def explode(self):
        # Trigger explosion
        explosion = Explosion(self.x, self.y)
        self.game.explosions.append(explosion)
        self.game.bombs.remove(self)

    def draw(self, screen):
        bomb_rect = Bomb.bomb_surf.get_rect(
            center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
        )
        screen.blit(Bomb.bomb_surf, bomb_rect)