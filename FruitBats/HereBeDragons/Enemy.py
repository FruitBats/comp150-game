import pygame

from Characters import Character
from Helpers import *
from Collision import CollisionParams
from DynaSword import DynaSword


class ChaserEnemy(Character):
    detection_range = 5  # range, in tiles, before engaging with player
    acceleration = 20  # rate of acceleration, in tiles/sec/sec
    velocity = None  # current speed, as a Vector
    chasing = False  # whether currently chasing the player or not

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.collision = CollisionParams((10, 1), (39, 72), True)
        self.sprite = pygame.image.load("graphics/enemy.png")
        self.velocity = Vector(0, 0)

    def update(self, delta_time, player, object_list, map):
        # Check if the player is in range
        player_distance = distance((self.x, self.y), (player.x, player.y))
        if player_distance <= self.detection_range:
            self.chasing = True
        else:
            self.chasing = False

        # Chase the player if close
        if self.chasing:
            to_player = Vector(player.x - self.x, player.y - self.y)

            self.velocity += to_player.normalise(
                delta_time * self.acceleration
                * (1 - player_distance / self.detection_range))

        # Move according to velocity
        if not self.move(self.velocity * delta_time, object_list):
            self.velocity = Vector(0, 0)

class Enemy(Character):

    """Testing new enemies - Mango"""

    detection_range = 5  # range, in tiles, before engaging with player
    attack_range = 2 # range, in tiles, before using an attack
    acceleration = 20  # rate of acceleration, in tiles/sec/sec
    velocity = None  # current speed, as a Vector
    chasing = False  # whether currently chasing the player or not

    dynasword2 = None  # Pointer to dynasword

    # The current position of the player
    player_x = 0
    player_y = 0
    player_distance = 0

    def __init__(self, x, y, hitpoints):

        """
        Constructor

        Args:
            x (int): x position to spawn.
            y (int): y position to spawn.
            hitpoints (int): Number of hitpoints for the enemy.
        """

        self.x = float(x)
        self.y = float(y)
        self.hitpoints = hitpoints
        self.collision = CollisionParams((10, 1), (39, 72), True)
        self.sprite = pygame.image.load("graphics/enemy.png")
        self.velocity = Vector(0, 0)

    def update(self, delta_time, player, object_list, map):

        """
        Called in main game loop to update the enemy

        Args:
            delta_time (int): Update timing.
            player (Player): The player object.
            object_list (list): List of all objects currently in game.
            map (Map): The map object.
        """

        # Get the player position and distance from enemy
        self.player_x = player.x
        self.player_y = player.y
        self.player_distance = distance((self.x, self.y), (self.player_x, self.player_y))

        # Call chase function if chaser enemy
        self.chase_player(delta_time, player, object_list, map)

        # Check health
        if self.hitpoints <= 0:
            self.die()

        # Check if in range to attack
        if self.player_distance <= self.attack_range:
            self.attack(delta_time, player, object_list)

    def attack(self, delta_time, player, object_list):
        """
        Default melee attack for enemy.

        Args:
            delta_time (int): Update timing.
            player (Player): The player object.
            object_list (list): List of all objects currently in game.
        """

        # TODO: Talk to Louis about the DynaSword. Currently, the attack time dictates the angle of the swing.
        # TODO: Attack time should instead dictate how long the swing takes to complete, regardless of angle.
        # TODO: Fix rendering. Currently enemy sword is rendering on the player?

        if self.dynasword2 is None:
            self.dynasword2 = DynaSword(self.x, self.y)
            object_list.append(self.dynasword2)

        # Basic attack
        self.dynasword2.mouse_x = self.player_x
        self.dynasword2.mouse_y = self.player_y
        self.dynasword2.attack()

    def die(self):
        pass # Enemy should "die"

    def chase_player(self, delta_time, player, object_list, map):
        # Check if the player is in range

        if self.player_distance <= self.detection_range:
            self.chasing = True

        else:
            self.chasing = False

        # Chase the player if close
        if self.chasing:
            to_player = Vector(player.x - self.x, player.y - self.y)

            self.velocity += to_player.normalise(delta_time * self.acceleration * (1 - self.player_distance / self.detection_range))

        # Move according to velocity
        if not self.move(self.velocity * delta_time, object_list):
            self.velocity = Vector(0, 0)