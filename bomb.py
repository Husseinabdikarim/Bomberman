import pygame
from config import TILE_SIZE
from explosion import Explosion


class Bomb:
    bomb_surf = None
    bomb_surf_2 = None

    def __init__(self, x, y, game, turn=0, bomb_type="player"):
        """
        Initialize the Bomb object.

        :param x: x-coordinate of the bomb.
        :param y: y-coordinate of the bomb.
        :param game: Reference to the Game object.
        :param turn: Number of turns before explosion (for initial bombs).
        :param bomb_type: Type of the bomb ('player' or 'initial').
        """
        self.x = x
        self.y = y
        self.game = game
        self.turn = turn
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

    def has_neighboring_bomb(self, x, y):
        """Check if there are any bombs in the neighboring tiles."""
        neighbors = [
            (x + TILE_SIZE, y),  # Right
            (x - TILE_SIZE, y),  # Left
            (x, y + TILE_SIZE),  # Down
            (x, y - TILE_SIZE),  # Up
        ]
        for nx, ny in neighbors:
            for bomb in self.game.bombs:
                if bomb.x == nx and bomb.y == ny:
                    return True  # Found a neighboring bomb
        return False  # No neighboring bombs

    def explode(self):
        """
        Trigger the explosion, remove the bomb, and check for chain reactions.
        """
        # Create explosion effect
        explosion = Explosion(self.x, self.y)
        self.game.explosions.append(explosion)

        # Queue to track bombs that need to explode
        to_explode = [(self.x, self.y)]
        # Set to track bombs that have already been added to the queue
        processed = set()

        # Remove current bomb
        if self in self.game.bombs:
            self.game.bombs.remove(self)

        while to_explode:
            x, y = to_explode.pop(0)  # Process next bomb
            processed.add((x, y))  # Mark this bomb as processed

            neighbors = [
                (x + TILE_SIZE, y),  # Right
                (x - TILE_SIZE, y),  # Left
                (x, y + TILE_SIZE),  # Down
                (x, y - TILE_SIZE),  # Up
            ]

            for nx, ny in neighbors:
                for bomb in self.game.bombs[:]:
                    if bomb.x == nx and bomb.y == ny and (bomb.x, bomb.y) not in processed:
                        if bomb.type == "player":
                            self.game.bombs.remove(bomb)
                            to_explode.append((bomb.x, bomb.y))
                            processed.add((bomb.x, bomb.y))
                        else:  # It's an "initial" bomb
                            if bomb.turn > 0:
                                bomb.turn -= 1
                                if bomb.has_neighboring_bomb(bomb.x, bomb.y):
                                    to_explode.append((bomb.x, bomb.y))
                                    processed.add((bomb.x, bomb.y))
                            else:
                                self.game.bombs.remove(bomb)
                                to_explode.append((bomb.x, bomb.y))
                                processed.add((bomb.x, bomb.y))

    def draw(self, screen):
        """
        Draw the bomb on the screen.

        :param screen: The Pygame screen object.
        """
        if self.type == "initial":
            bomb_rect = Bomb.bomb_surf_2.get_rect(
                center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
            )
            font = pygame.font.Font(None, 18)
            text_surf = font.render(str(self.turn), True, (0, 255, 0))
            text_rect = text_surf.get_rect(center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2))
            screen.blit(Bomb.bomb_surf_2, bomb_rect)
            screen.blit(text_surf, text_rect)
        elif self.type == "player":
            bomb_rect = Bomb.bomb_surf.get_rect(
                center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
            )
            screen.blit(Bomb.bomb_surf, bomb_rect)
