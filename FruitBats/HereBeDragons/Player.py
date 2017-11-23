# Standard imports
import math

# Third party imports
import pygame

# Project imports
from Characters import Character
from Map import *
from Collision import CollisionBox
from Helpers import *
from DynaSword import DynaSword


class Player(Character):
    max_speed = 7.0  # The maximum running speed, in tiles/sec
    acceleration = 35.0  # Rate of acceleration while running, in tiles/sec/sec
    friction = 70.0  # Rate of slowdown when releasing movement keys
    velocity = None  # (Vector) Rate of movement per axis in tiles/sec
    dynasword = None  # Pointer to dynasword

    def __init__(self, x, y, parent_map):
        """Init: Loads default player sprite and scales it up"""
        # Load character image
        self.sprite = pygame.image.load('graphics/game_character.png')
        # Scale character so we can see his beauty
        #self.sprite = pygame.transform.smoothscale(
        #                self.sprite,
        #                (MapClass.TILE_SIZE, MapClass.TILE_SIZE))
        self.x = x
        self.y = y
        self.parent_map = parent_map

        self.size = self.sprite.get_size()
        # self.sprite_origin = (self.size[0] / 2), (self.size[1] / 2)    # Wasn't sure if origin should be set here or not.

        # self.collision = CollisionParams((10, 1), (39, 72), True)
        self.collision = CollisionBox((0 + 10, 0 + 10), (self.size[0] - 20, self.size[1] - 20), True)
        self.velocity = Vector(0, 0)

    def update(self, delta_time, player, object_list, map):
        # Perform updates
        self.update_movement(delta_time, player, object_list, map)
        self.update_attacks(delta_time, player, object_list, map)

    def update_movement(self, delta_time, player, object_list, map):
        # Perform character movement
        key_pressed = pygame.key.get_pressed()

        # Make a normalised vector of movement based on user input
        move = Vector(0.0, 0.0)

        if key_pressed[pygame.K_w]:
            move.y -= 1.0
        if key_pressed[pygame.K_s]:
            move.y += 1.0
        if key_pressed[pygame.K_d]:
            move.x += 1.0
        if key_pressed[pygame.K_a]:
            move.x -= 1.0

        # If the movement vector is nonzero, stretch it by the player's acceleration factor to move; otherwise, change it to an opposite vector for friction
        move_length = move.length()
        current_speed = self.velocity.length()

        # Do player acceleration
        if move_length > 0.000:
            # Scale movement vector to acceleration speed
            move.normalise(self.acceleration + self.friction)  # + deceleration to fight the friction that immediately follows

        # Do player deceleration
        deceleration_speed = self.friction

        # Cap the deceleration speed to <= current_speed (to avoid boosting in the opposite direction!)
        if current_speed < deceleration_speed * delta_time:
            deceleration_speed = current_speed / delta_time

        if current_speed > 0:
            move -= self.velocity * (deceleration_speed / self.velocity.length())

        # Accelerate or decelerate accordingly
        self.velocity += move * delta_time

        # Cap player speed
        if self.velocity.length() > self.max_speed:
            self.velocity.normalise(self.max_speed)

        # Move player by velocity
        moved = self.move(tuple(self.velocity * delta_time), object_list)

        # Stop velocity if player collided with something
        if not moved:
            self.velocity = Vector(0, 0)

    def update_attacks(self, delta_time, player, object_list, map):
        # Create sword
        # TODO: Consult Michael about this. There should be a way to call
        # game.CreateObject or something like that. Should be done on init.
        if self.dynasword is None:
            self.dynasword = DynaSword(self.x, self.y, self)
            object_list.append(self.dynasword)

        # Basic attack
        if pygame.mouse.get_pressed()[0]:
            self.dynasword.attack()
        if pygame.mouse.get_pressed()[2]:
            self.dynasword.block()
        if pygame.mouse.get_pressed()[1]:
            self.dynasword.boomerang()
