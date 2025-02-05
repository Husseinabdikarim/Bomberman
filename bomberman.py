import pygame
import random
from player import Player
from bomb import Bomb
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
        self.players = [Player(self, 1), Player(self, 2)]  # Two players
        self.bombs = []
        self.bomb_queue = deque()  # Queue for handling bomb explosions
        self.bomb_counter = 0  # Tracks the number of bombs on the map
        self.explosions = []
        self.tiles = Game.create_map()

        # Add initial bombs to the map
        self.setup_initial_bombs()

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
        """Handle inputs for both players"""
        keys = pygame.key.get_pressed()
        return {
            # Player 1 (Arrow keys + Space)
            "p1_left": keys[pygame.K_LEFT],
            "p1_right": keys[pygame.K_RIGHT],
            "p1_up": keys[pygame.K_UP],
            "p1_down": keys[pygame.K_DOWN],
            "p1_bomb": keys[pygame.K_SPACE],

            # Player 2 (WASD + LShift)
            "p2_left": keys[pygame.K_a],
            "p2_right": keys[pygame.K_d],
            "p2_up": keys[pygame.K_w],
            "p2_down": keys[pygame.K_s],
            "p2_bomb": keys[pygame.K_LSHIFT]
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
        walls = Wall.get_walls(self.tiles)
        # walls = self.get_walls()

        # Update the player based on input
        input_state = self.get_input_state()
        for player in self.players:
            player.update(input_state, walls, self.bombs)

        # Handle bomb explosions (process the bomb queue)
        if len(self.bomb_queue) >= 3:
            first_bomb = self.bomb_queue.popleft()
            first_bomb.explode()

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
        for player in self.players:
            player.draw(self.screen)
        for bomb in self.bombs:
            bomb.draw(self.screen)

        pygame.display.flip()

    def setup_initial_bombs(self):
        """Ask the player if they want to manually place bombs."""
        prompt = self.user_prompt()
        if prompt:  # if prompt is 'y'
            placed_bombs = Bomb.show_bomb_placement_screen(self)  # manually place bombs
            bomb_turns = Bomb.get_bomb_turns(self, placed_bombs)  # Get turns for each bomb

            for (row, col), turn in bomb_turns.items():
                bomb_x, bomb_y = col * TILE_SIZE, row * TILE_SIZE
                self.bombs.append(Bomb(bomb_x, bomb_y, self, turn=turn, bomb_type="initial"))
        else:  # if prompt is 'n'
            Bomb.add_initial_bombs(self, 5)  # Automatic setup

    def user_prompt(self):
        """Show a simple Yes/No menu for bomb placement."""
        font = pygame.font.Font(None, 36)
        selecting = True
        choice = False

        while selecting:
            self.screen.fill((30, 30, 30))
            bg_image = pygame.image.load("assets/background_image.png")
            bg_image = pygame.transform.scale(bg_image, (600, 600))
            self.screen.blit(bg_image, (0, 0))
            text = font.render("Do you want to manually place bombs? (Y/N)",
                               True, (255, 200, 100))  # (255, 200, 100)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        choice = True
                        selecting = False
                    elif event.key == pygame.K_n:
                        selecting = False

        return choice


if __name__ == "__main__":
    game = Game()
    game.run()
