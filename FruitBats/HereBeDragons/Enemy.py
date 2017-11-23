import pygame

from Characters import Character
from Helpers import *
from Collision import CollisionBox
from DynaSword import DynaSword
from Projectiles import Arrow


class Enemy(Character):
    """Base enemy class (Mango)"""
    detection_range = 5  # range, in tiles, before engaging with player
    attack_range = 2  # range, in tiles, before using an attack (in melee scenarios)
    acceleration = 20  # rate of acceleration, in tiles/sec/sec
    velocity = None  # current speed, as a Vector

    dynasword = None  # Pointer to dynasword

    def __init__(self, x, y, hitpoints, parent_map):

        """
        Constructor

        Args:
            x (int): x position to spawn.
            y (int): y position to spawn.
            hitpoints (int): Number of hitpoints for the enemy.
        """

        self.x = float(x)
        self.y = float(y)
        self.collision = CollisionBox((10, 1), (39, 72), True)
        self.sprite = pygame.image.load("graphics/enemy.png")
        self.velocity = Vector(0, 0)
        self.max_health = hitpoints
        self.health = self.max_health
        self.parent_map = parent_map

    def swipe(self, delta_time, player, object_list):
        """
        Default melee attack for enemy

        Args:
            delta_time (int): Update timing.
            player (Player): The player object.
            object_list (list): List of all objects currently in game.
        """

        if self.dynasword is None:
            self.dynasword = DynaSword(self.x, self.y, self)
            object_list.append(self.dynasword)

        # Basic attack
        self.dynasword.mouse_x = self.player_x
        self.dynasword.mouse_y = self.player_y
        self.dynasword.attack()

    def chase_player(self, delta_time, player, object_list, map):
        to_player = Vector(player.x - self.x, player.y - self.y)
        to_player.normalise(delta_time * self.acceleration * (1 - self.player_distance / self.detection_range))

        self.velocity += to_player

        # Move according to velocity
        if not self.move(self.velocity * delta_time, object_list):
            self.velocity = Vector(0, 0)


class ChaserEnemy(Enemy):
    """Enemy which chases after the player with a terrifying sword
        Vars:
            chasing (Boolean): Whether currently chasing the player
    """
    chasing = False

    def update(self, delta_time, player, object_list, map):

        """
        ChaseEnemy update

        Args:
            delta_time (float): Time since the last frame
            player (Player): The player object.
            object_list (list): List of all objects currently in game.
            map (Map): The map object.
        """

        # Get the player position and distance from enemy
        player_distance = distance((self.x, self.y), (self.player_x, self.player_y))

        # Check if the player is in range to chase
        if self.player_distance <= self.detection_range:
            # Chase them!
            self.chase_player(delta_time, player, object_list, map)

        # Check if in range to attack
        if self.player_distance <= self.attack_range:
            # Attack them!
            self.attack(delta_time, player, object_list)


class ArrowEnemy(Enemy):
    """Enemy which shoots the player with arrows
        Vars:
            arrow_timer (float): Time, in seconds, until next arrow is fired
            arrow_rate (float): Number of arrows per second shot by this enemy
    """
    arrow_timer = 0
    arrow_rate = 1

    def update(self, delta_time, player, object_list, map):
        # Shoot arrows if it's time
        self.arrow_timer -= delta_time
        if self.arrow_timer <= 0 and distance((player.x, player.y), (self.x, self.y)) < self.detection_range:
            object_list.append(Arrow((self.x, self.y), (player.x, player.y), 5, map))
            self.arrow_timer = 1 / float(self.arrow_rate)