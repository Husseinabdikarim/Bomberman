import pygame
import random
from player import Player
from bomb import Bomb
from explosion import Explosion
from wall import Wall
from tile import Tile
from config import WIDTH, HEIGHT, TILE_SIZE, FPS, EXCLUDED_ROWS, EXCLUDED_COLS
from collections import deque


class Game:
    def __init__(self):
        """
        Initialize the Game object.
        
        - Set up the screen, clock, and game state.
        - Initialize player, bombs, bomb queue, and explosions.
        - Generate the game map and add initial bombs.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bomberman")
        self.running = True
        self.player = Player(self)
        self.bombs = []
        self.bomb_queue = deque()  # Queue for handling bomb explosions
        self.bomb_counter = 0  # Tracks the number of bombs on the map
        self.explosions = []
        self.tiles = Game.create_map()

        # Add initial bombs to the map
        # TODO 2: make sure to add turns in them before explosion.
        self.add_initial_bombs(5)

    @staticmethod
    def create_map():
        """
        Generate the game map with a mix of walls and empty tiles.
        
        :return: A 2D list representing the map tiles.
        """
        tiles = []
        for row in range(15):
            row_tiles = []
            for col in range(15):
                if row in EXCLUDED_ROWS and col in EXCLUDED_COLS:
                    row_tiles.append(Tile(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, 0))  # 0 = Empty tile
                else:
                    if random.random() < 0.2:  # 20% chance to be a wall
                        row_tiles.append(Wall(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE))
                    else:
                        row_tiles.append(Tile(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, 0))
            tiles.append(row_tiles)
        return tiles

    @staticmethod
    def get_input_state():
        """
        Retrieve the current state of player input.

        :return: A dictionary with input states for movement and bomb placement.
        """
        # TODO 3: Consider 2 player modes.
        keys = pygame.key.get_pressed()
        return {
            "left": keys[pygame.K_LEFT],
            "right": keys[pygame.K_RIGHT],
            "up": keys[pygame.K_UP],
            "down": keys[pygame.K_DOWN],
            "bomb": keys[pygame.K_SPACE],
        }

    def run(self):
        """
        Main game loop.

        - Handles events, updates game state, and renders the screen.
        - Runs at a constant frame rate defined by FPS.
        """
        while self.running:
            self.handle_events()
            self.update_game()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self):
        """
        Handle events such as quitting the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_game(self):
        """
        Update the game state, including player, bombs, and explosions.
        """
        # Get all wall tiles for collision detection
        walls = self.get_walls()

        # Update the player based on input
        input_state = Game.get_input_state()
        self.player.update(input_state, walls, self.bombs)

        # Handle bomb explosions (process the bomb queue)
        if len(self.bomb_queue) > 0 and self.bomb_counter >= 3:
            first_bomb = self.bomb_queue.popleft()
            first_bomb.explode()
            self.bomb_counter -= 1

        # Update all bombs and explosions
        for bomb in self.bombs[:]:
            bomb.update()
        for explosion in self.explosions:
            explosion.update()

    def render(self):
        """
        Render all game elements onto the screen.
        """
        self.screen.fill((0, 0, 0))

        # Draw all tiles
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)

        # Draw the player, bombs, and explosions
        self.player.draw(self.screen)
        for bomb in self.bombs:
            bomb.draw(self.screen)

        # for explode in self.explosions:
        #     explode.draw(self.screen)    

        pygame.display.flip()

    def get_walls(self):
        """
        Retrieve all wall tiles from the map.

        :return: A list of Wall objects.
        """
        return [tile for row in self.tiles for tile in row if isinstance(tile, Wall)]

    def add_initial_bombs(self, num_bombs):
        """
        Add a specified number of random bombs to empty locations on the map.

        :param num_bombs: Number of bombs to add.
        """
        for _ in range(num_bombs):
            # Find all empty tiles
            empty_tiles = []
            for row in range(15):
                for col in range(15):
                    # Add the tile to empty_tiles if it is a Tile and not a Wall
                    if (isinstance(self.tiles[row][col], Tile)
                            and not isinstance(self.tiles[row][col], Wall)):
                        empty_tiles.append((row, col))

            if not empty_tiles:
                break  # No empty tiles found

            # Randomly select a position for the bomb
            row, col = random.choice(empty_tiles)
            bomb_x = col * TILE_SIZE
            bomb_y = row * TILE_SIZE

            # Create a Bomb
            new_bomb = Bomb(bomb_x, bomb_y, self, bomb_type="initial")
            self.bombs.append(new_bomb)


if __name__ == "__main__":
    game = Game()
    game.run()
