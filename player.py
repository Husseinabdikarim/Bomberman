import pygame
from bomb import Bomb
from config import WIDTH, HEIGHT, TILE_SIZE, PLAYER_SIZE


class Player:
    player_surf = None
    
    def __init__(self, game):
        """
        Initialize the Player object.

        :param game: Reference to the Game object.
        """
        self.game = game
        self.x, self.y = 0, 0
        self.target_x, self.target_y = 0, 0  # Target position on the grid
        if Player.player_surf is None:
            Player.player_surf = pygame.transform.scale(
                pygame.image.load("bomberman.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE),
            )

    def update(self, input_state, walls, bombs):
        """
        Update the player's position and actions.

        :param input_state: Dictionary of input states (e.g., movement and bomb drop).
        :param walls: List of wall objects to check for collisions.
        :param bombs: List of active bombs.
        """
        # If the player is not at their target position, don't accept new input
        if self.x != self.target_x or self.y != self.target_y:
            self.move_towards_target()
            return

        # Set new target position based on input
        new_target_x, new_target_y = self.target_x, self.target_y
        new_target_x, new_target_y = self.player_movement(input_state, new_target_x, new_target_y)

        # Prevent diagonal movement
        if (input_state["left"] or input_state["right"]) and (input_state["up"] or input_state["down"]):
            return 

        # Check for collisions with walls
        player_rect = pygame.Rect(new_target_x, new_target_y, PLAYER_SIZE, PLAYER_SIZE)
        for wall in walls:
            wall_rect = pygame.Rect(wall.x, wall.y, TILE_SIZE, TILE_SIZE)
            if player_rect.colliderect(wall_rect):
                return 

        # Update target position
        self.target_x, self.target_y = new_target_x, new_target_y

        self.drop_bomb(bombs, input_state)

    def player_movement(self, input_state, new_target_x, new_target_y):
        """
        Calculate the player's new target position based on input.

        :param input_state: Dictionary of input states.
        :param new_target_x: Current target x-coordinate.
        :param new_target_y: Current target y-coordinate.
        :return: Updated target x and y coordinates.
        """
        # Only allow horizontal or vertical movement, but not both at the same time
        if input_state["left"] and self.target_x > 0:
            new_target_x -= TILE_SIZE
        elif input_state["right"] and self.target_x < (WIDTH - TILE_SIZE):
            new_target_x += TILE_SIZE
        if input_state["up"] and self.target_y > 0:
            new_target_y -= TILE_SIZE
        elif input_state["down"] and self.target_y < (HEIGHT - TILE_SIZE):
            new_target_y += TILE_SIZE
        return new_target_x, new_target_y

    def drop_bomb(self, bombs, input_state):
        """
        Drop a bomb at the player's current position.

        :param bombs: List of active bombs.
        :param input_state: Dictionary of input states.
        """
        if input_state["bomb"]:
            bomb_x = round(self.target_x / TILE_SIZE) * TILE_SIZE
            bomb_y = round(self.target_y / TILE_SIZE) * TILE_SIZE
            if not any(b.x == bomb_x and b.y == bomb_y for b in bombs):
                new_bomb = Bomb(bomb_x, bomb_y, self.game)
                bombs.append(new_bomb)
                self.game.bomb_queue.append(new_bomb)
                self.game.bomb_counter += 1

    def move_towards_target(self):
        """
        Smoothly move the player towards their target position.
        """
        if self.x < self.target_x:
            self.x += 5
        if self.x > self.target_x:
            self.x -= 5
        if self.y < self.target_y:
            self.y += 5
        if self.y > self.target_y:
            self.y -= 5

    def draw(self, screen):
        """
        Draw the player on the screen.

        :param screen: The Pygame screen object.
        """ 
        player_rect = Player.player_surf.get_rect(
                center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
            )
        screen.blit(Player.player_surf, player_rect)
