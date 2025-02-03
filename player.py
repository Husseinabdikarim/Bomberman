import pygame
from bomb import Bomb
from config import WIDTH, HEIGHT, TILE_SIZE, PLAYER_SIZE


class Player:
    player_1_surf = None
    player_2_surf = None
    
    def __init__(self, game, player_num=1):
        """
        Initialize the Player object.

        :param game: Reference to the Game object.
        """
        self.game = game
        self.player_num = player_num
        self.x, self.y = self.set_initial_position()
        self.target_x, self.target_y = self.x, self.y

        # Load bomb images if not already loaded
        if Player.player_1_surf is None:
            Player.player_1_surf = pygame.transform.scale(
                pygame.image.load("bomberman_p1.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE),
            )
        if Player.player_2_surf is None:
            Player.player_2_surf = pygame.transform.scale(
                pygame.image.load("bomberman_p2.png").convert_alpha(),
                (TILE_SIZE, TILE_SIZE),
            )

    def set_initial_position(self):
        """Set different starting positions for players"""
        if self.player_num == 1:
            return 0, 0
        return (WIDTH - TILE_SIZE), (HEIGHT - TILE_SIZE)

    def get_player_input(self, input_state):
        """Get movement direction for this specific player"""
        if self.player_num == 1:
            return {
                "left": input_state["p1_left"],
                "right": input_state["p1_right"],
                "up": input_state["p1_up"],
                "down": input_state["p1_down"],
                "bomb": input_state["p1_bomb"]
            }
        else:
            return {
                "left": input_state["p2_left"],
                "right": input_state["p2_right"],
                "up": input_state["p2_up"],
                "down": input_state["p2_down"],
                "bomb": input_state["p2_bomb"]
            }

    def update(self, input_state, walls, bombs):
        """
        Update the player's position and actions.

        :param input_state: Dictionary of input states (e.g., movement and bomb drop).
        :param walls: List of wall objects to check for collisions.
        :param bombs: List of active bombs.
        """
        player_input = self.get_player_input(input_state)
        # If the player is not at their target position, don't accept new input
        if self.x != self.target_x or self.y != self.target_y:
            self.move_towards_target()
            return

        # Set new target position based on input
        new_target_x, new_target_y = self.target_x, self.target_y
        new_target_x, new_target_y = self.player_movement(player_input, new_target_x, new_target_y)

        # Prevent diagonal movement
        if (player_input["left"] or player_input["right"]) and (player_input["up"] or player_input["down"]):
            return 

        # Check for collisions with walls
        player_rect = pygame.Rect(new_target_x, new_target_y, PLAYER_SIZE, PLAYER_SIZE)
        for wall in walls:
            wall_rect = pygame.Rect(wall.x, wall.y, TILE_SIZE, TILE_SIZE)
            if player_rect.colliderect(wall_rect):
                return

        # In Player.update():
        for other_player in self.game.players:
            if other_player != self:
                # Check both CURRENT and TARGET positions
                other_current_rect = pygame.Rect(other_player.x, other_player.y, PLAYER_SIZE, PLAYER_SIZE)
                other_target_rect = pygame.Rect(other_player.target_x, other_player.target_y, PLAYER_SIZE, PLAYER_SIZE)

                if player_rect.colliderect(other_current_rect) or player_rect.colliderect(other_target_rect):
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
        player_input = self.get_player_input(input_state)
        if player_input["bomb"]:
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
        if self.player_num == 1:
            player_1_rect = Player.player_1_surf.get_rect(
                center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
            )
            screen.blit(Player.player_1_surf, player_1_rect)

        else:
            player_2_rect = Player.player_2_surf.get_rect(
                center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2)
            )
            screen.blit(Player.player_2_surf, player_2_rect)
