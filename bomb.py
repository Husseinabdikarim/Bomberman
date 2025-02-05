import pygame
import random
from explosion import Explosion
from wall import Wall
from tile import Tile
from config import WIDTH, HEIGHT, TILE_SIZE, PROTECTED_TILES


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
                pygame.image.load("assets/Bomb.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE),
            )
        if Bomb.bomb_surf_2 is None:
            Bomb.bomb_surf_2 = pygame.transform.scale(
                pygame.image.load("assets/initial_bomb.png").convert_alpha(),
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
    @staticmethod
    def add_initial_bombs(game, num_bombs):
        """
        Add a specified number of random bombs to empty locations on the map.

        :param game:
        :param num_bombs: Number of bombs to add.
        """
        for _ in range(num_bombs):
            # Find all empty tiles
            empty_tiles = []
            for row in range(15):
                for col in range(15):
                    if (col, row) in PROTECTED_TILES:
                        continue
                    # Add the tile to empty_tiles if it is a Tile and not a Wall
                    if (isinstance(game.tiles[row][col], Tile)
                            and not isinstance(game.tiles[row][col], Wall)):
                        empty_tiles.append((row, col))

            if not empty_tiles:
                break  # No empty tiles found

            # Randomly select a position for the bomb
            row, col = random.choice(empty_tiles)
            bomb_x = col * TILE_SIZE
            bomb_y = row * TILE_SIZE

            # Create a Bomb
            turns = random.randint(1, 3)
            new_bomb = Bomb(bomb_x, bomb_y, game, turns, bomb_type="initial")
            game.bombs.append(new_bomb)

    @staticmethod
    def show_bomb_placement_screen(game):
        """Display an interactive screen to manually place bombs."""
        screen = game.screen
        tiles = game.tiles
        selecting = True
        bg_overlay = pygame.Surface((WIDTH, HEIGHT))
        bg_overlay.set_alpha(180)  # Semi-transparent background
        bg_overlay.fill((193, 245, 241))  # Black overlay

        empty_tiles = []
        for row in range(15):
            for col in range(15):
                if ((row, col) not in PROTECTED_TILES and isinstance(tiles[row][col], Tile)
                        and not isinstance(tiles[row][col], Wall)):
                    empty_tiles.append((row, col))

        placed_bombs = []

        while selecting:
            screen.blit(bg_overlay, (0, 0))

            for row in range(15):
                for col in range(15):
                    x, y = col * TILE_SIZE, row * TILE_SIZE

                    if isinstance(tiles[row][col], Wall):
                        pygame.draw.rect(screen, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE))
                    elif (row, col) in empty_tiles:
                        pygame.draw.rect(screen, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE), 2)

                    # If already selected, fill it in
                    if (row, col) in placed_bombs:
                        pygame.draw.rect(screen, (200, 50, 50), (x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    col, row = mx // TILE_SIZE, my // TILE_SIZE
                    if (row, col) in empty_tiles:
                        if (row, col) in placed_bombs:
                            placed_bombs.remove((row, col))  # Remove if clicked again
                        else:
                            placed_bombs.append((row, col))  # Add bomb location
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and placed_bombs:  # Finish selection
                        selecting = False

            pygame.display.flip()

        return placed_bombs

    @staticmethod
    def get_bomb_turns(game, placed_bombs):
        """
        Ask the user for turns for each manually placed bomb.
        :param game:
        :param placed_bombs: List of (row, col) tuples where bombs were placed.
        :return: Dictionary mapping bomb positions to turn values.
        """
        screen = game.screen
        bomb_turns = {}  # Store turns for each bomb position

        font = pygame.font.Font(None, 28)
        selecting_turns = True

        while selecting_turns:
            screen.fill((30, 30, 30))
            instruction_text = font.render("Enter turns for each bomb (1-3). Press Enter when done.",
                                           True, (255, 255, 255))
            screen.blit(instruction_text, (20, 20))

            # Display the bombs
            for i, (row, col) in enumerate(placed_bombs):
                x, y = col * TILE_SIZE, row * TILE_SIZE

                turn_text = font.render(f"Bomb {i + 1}: ({row},{col}) - Turns: {bomb_turns.get((row, col), '?')}",
                                        True, (255, 255, 255))
                screen.blit(turn_text, (20, 50 + i * 30))

            pygame.display.flip()

            # Handle turn input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(bomb_turns) == len(placed_bombs):
                        selecting_turns = False
                    elif pygame.K_1 <= event.key <= pygame.K_3:
                        turn = event.key - pygame.K_0  # Convert key to integer
                        if len(bomb_turns) < len(placed_bombs):
                            bomb_turns[placed_bombs[len(bomb_turns)]] = turn  # Assign turn

        return bomb_turns

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
