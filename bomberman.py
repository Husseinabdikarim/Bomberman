import pygame
import random
from player import Player
from bomb import Bomb
from explosion import Explosion
from wall import Wall
from tile import Tile
from config import WIDTH, HEIGHT, TILE_SIZE, FPS
from collections import deque


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bomberman")
        self.running = True
        self.player = Player(self)
        self.bombs = []
        self.bomb_queue = deque()
        self.bomb_counter = 0
        self.explosions = []
        self.tiles = Game.create_map()

    @staticmethod
    def create_map():
        tiles = []
        for row in range(15):
            row_tiles = []
            for col in range(15):
                if random.random() < 0.2:  # 20% chance to be a wall
                    row_tiles.append(Wall(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE))
                else:
                    row_tiles.append(
                        Tile(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, 0)
                    )  # 0 = Empty tile
            tiles.append(row_tiles)
        return tiles
    
    @staticmethod
    def get_input_state():
        keys = pygame.key.get_pressed()
        return {
            "left": keys[pygame.K_LEFT],
            "right": keys[pygame.K_RIGHT],
            "up": keys[pygame.K_UP],
            "down": keys[pygame.K_DOWN],
            "bomb": keys[pygame.K_SPACE],
        }

    def run(self):
        while self.running:
            self.handle_events()
            self.update_game()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_game(self):
        walls = self.get_walls()
        
        input_state = Game.get_input_state()
        # Update player
        self.player.update(input_state, walls, self.bombs)

        # Handle bomb explosions
        if len(self.bomb_queue) > 0 and self.bomb_counter >= 3:
            first_bomb = self.bomb_queue.popleft()
            first_bomb.explode()
            self.bomb_counter -= 1

        # Update bombs and explosions
        for bomb in self.bombs[:]:
            bomb.update()
        for explosion in self.explosions:
            explosion.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)
        self.player.draw(self.screen)
        for bomb in self.bombs:
            bomb.draw(self.screen)
        pygame.display.flip()

    def get_walls(self):
        return [tile for row in self.tiles for tile in row if isinstance(tile, Wall)]


if __name__ == "__main__":
    game = Game()
    game.run()