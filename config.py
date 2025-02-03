# Game Constants
WIDTH = 600
HEIGHT = 600
TILE_SIZE = 40
FPS = 60
PLAYER_SIZE = 40
EXCLUDED_ROWS = {0, 1, 13, 14}
EXCLUDED_COLS = {0, 1, 2, 12, 13, 14}
PROTECTED_TILES = {
    (0, 0),  # Player 1 start
    (WIDTH//TILE_SIZE-1, HEIGHT//TILE_SIZE-1)  # Player 2 start
}
