import pygame

from Characters import Character
from Helpers import *
from Collision import CollisionParams


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