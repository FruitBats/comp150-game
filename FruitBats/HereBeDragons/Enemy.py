import random

import pygame

from Characters import Character
from Helpers import *
from Collision import CollisionBox
from DynaSword import DynaSword
import Projectiles


class Enemy(Character):
    """Base enemy class (Mango)

    Attributes:
        detection_range (float): Range from the player, in tile units, before engaging with the player
        attack_range (float): Range from the player, in tile units, before using a melee attack (if applicable)
        acceleration (float): Rate of movement acceleration, in tiles/sec/sec
        velocity (Vector): Speed of the enemy, in tiles/sec
        dynasword (DynaSword): The DynaSword owned by this enemy, if applicable
        being_majestic (Boolean): Whether or not the enemy is currently majestically dying
        majestic_timer (float): Time, in seconds, before majestic death becomes regular death
    """
    detection_range = 5
    attack_range = 2
    acceleration = 20
    velocity = None
    dynasword = None

    being_majestic = False
    majestic_timer = 1

    def __init__(self, (x, y), hitpoints, parent_map):
        """Spawns an enemy with a certain amount of hit points

        Args:
            (x, y) (float): Position to spawn, in tile unuits
            hitpoints (int): Number of hitpoints to spawn with
            parent_map (MapClass): Map wherein this enemy lives
        """

        self.x = float(x)
        self.y = float(y)
        self.collision = CollisionBox((10, 7), (37, 62), True)
        self.sprite_origin = Vector(28, 44)
        self.sprite = pygame.image.load("graphics/enemy.png")
        self.velocity = Vector(0, 0)
        self.max_health = hitpoints
        self.health = self.max_health
        self.parent_map = parent_map

    def default_update(self, delta_time, player, object_list):
        """Does default enemy updates--you should call this at the end of your enemy update function

        Args:
            delta_time: (Float) Time since the last frame in seconds
            player: (Player) Player instance
            object_list: (list) Global list of objects
        """
        # Die if dying
        if self.being_majestic:
            self.update_majestic_death(delta_time)

        # Move according to velocity
        if not self.move(self.velocity * delta_time, object_list):
            self.velocity = Vector(0, 0)

    def swipe(self, delta_time, player, object_list):
        """Performs default DynaSword melee attack

        Args:
            delta_time (int): Update timing.
            player (Player): The player object.
            object_list (list): List of all objects currently in game.
        """

        if self.dynasword is None:
            self.dynasword = DynaSword(self.x, self.y, self)
            object_list.append(self.dynasword)

        # Basic attack
        self.dynasword.mouse_x = player.x
        self.dynasword.mouse_y = player.y
        self.dynasword.attack()

    def chase_player(self, delta_time, player):
        """Accelerates toward the player

        Args:
            delta_time (float): Time, in seconds, since last frame
            player (Player): The player who shall be murdered by this noble enemy
        """
        to_player = Vector(player.x - self.x, player.y - self.y)
        to_player.normalise(delta_time * self.acceleration * (1 - self.player_distance / self.detection_range))

        self.velocity += to_player

    def die_majestically(self, timer):
        """Begins majestic death

        Args:
            timer: (Float) Number of seconds during which majestic dying takes place before disappearing"""
        if not self.being_majestic:
            self.being_majestic = True
            self.majestic_timer = timer
            self.velocity.point_at_angle(random.randrange(0, 360), 8)
            self.collision.solid = False

    def update_majestic_death(self, delta_time):
        """Updates majestic death--must be called by Enemies who engage in majestic deaths in their update function
            Args:
                delta_time: (Float) Time in seconds since the last frame"""
        self.sprite_angle += 1300 * delta_time
        self.majestic_timer -= delta_time

        if self.majestic_timer < 0:
            self.dead = True  # RIP

    def die(self):
        """Begins death sequence for enemy"""
        self.dead = True


class ChaserEnemy(Enemy):
    """Enemy which chases after the player with a terrifying sword

    Attributes:
        chasing (Boolean): Whether currently chasing the player
    """
    chasing = False

    def update(self, delta_time, player, object_list, map):
        """Update, scans surroundings and chases players that come near. Overrides Object.update."""

        # Get the player position and distance from enemy
        player_distance = distance((self.x, self.y), (self.player_x, self.player_y))

        # Check if the player is in range to chase
        if player_distance <= self.detection_range:
            # Chase them!
            self.chase_player(delta_time, player)

        # Check if in range to attack
        if player_distance <= self.attack_range:
            # Attack them!
            self.swipe(delta_time, player, object_list)

        # Do default enemy stuff
        self.default_update(delta_time, player, object_list)

    def die(self):
        """Overrides Enemy.die"""
        self.die_majestically(2)


class ArrowEnemy(Enemy):
    """Enemy which shoots the player with arrows

    Attributes:
        arrow_timer (float): Time, in seconds, until next arrow is fired
        arrow_rate (float): Number of arrows per second shot by this enemy
    """
    arrow_timer = 0
    arrow_rate = 1

    def update(self, delta_time, player, object_list, map):
        """Scans around for nearby players and chases them. Overrides Object.update"""
        # Shoot arrows if it's time
        self.arrow_timer -= delta_time
        if self.arrow_timer <= 0 and distance((player.x, player.y), (self.x, self.y)) < self.detection_range and not self.being_majestic:
            object_list.append(Projectiles.Arrow((self.x, self.y), (player.x, player.y), 5, map))
            self.arrow_timer = 1 / float(self.arrow_rate)

        # Do default enemy stuff
        self.default_update(delta_time, player, object_list)

    def die(self):
        """Overrides Enemy.die"""
        self.die_majestically(2)