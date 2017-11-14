# Standard imports
import math

# Third party imports
import pygame

# Project imports
from Characters import Character
from Map import MapClass
from Collision import CollisionParams
from Helpers import *
from DynaSword import DynaSword


class Player(Character):
    max_speed = 7.0  # The maximum running speed, in tiles/sec
    acceleration = 35.0  # Rate of acceleration while running, in tiles/sec/sec
    friction = 90.0  # Rate of slowdown when releasing movement keys
    x_velocity = 0.0  # Rate of movement per axis in tiles/sec
    y_velocity = 0.0
    dynasword = None  # Pointer to dynasword

    def __init__(self, x, y):
        """Init: Loads default player sprite and scales it up"""
        # Load character image
        self.sprite = pygame.image.load('graphics/game_character.png')
        # Scale character so we can see his beauty
        #self.sprite = pygame.transform.smoothscale(
        #                self.sprite,
        #                (MapClass.TILE_SIZE, MapClass.TILE_SIZE))
        self.x = x
        self.y = y

        self.size = self.sprite.get_size()
        # self.sprite_origin = (self.size[0] / 2), (self.size[1] / 2)    # Wasn't sure if origin should be set here or not.

        # self.collision = CollisionParams((10, 1), (39, 72), True)
        self.collision = CollisionParams((0 + 10, 0 + 10), (self.size[0] - 20, self.size[1] - 20), True)

    def update(self, delta_time, player, object_list, map):
        # Perform updates
        self.update_movement(delta_time, player, object_list, map)
        self.update_attacks(delta_time, player, object_list, map)

    def update_movement(self, delta_time, player, object_list, map):
        # Perform character movement
        key_pressed = pygame.key.get_pressed()

        # Make a normalised vector of movement based on user input
        move_x = 0.0
        move_y = 0.0
        if key_pressed[pygame.K_w]:
            move_y -= 1.0
        if key_pressed[pygame.K_s]:
            move_y += 1.0
        if key_pressed[pygame.K_d]:
            move_x += 1.0
        if key_pressed[pygame.K_a]:
            move_x -= 1.0

        vec_length = distance((0, 0), (move_x, move_y))
        # If the movement vector is nonzero, move; otherwise do friction
        # todo: determine why 'if vec_length is not 0.0' didn't work correctly
        if vec_length > 0.000:
            # Normalise
            move_x /= vec_length
            move_y /= vec_length

            # Accelerate according to the direction of the vector
            self.x_velocity += move_x * self.acceleration * delta_time
            self.y_velocity += move_y * self.acceleration * delta_time

            # Cap player max speed
            current_speed = distance((0, 0), (self.x_velocity, self.y_velocity))
            if current_speed > self.max_speed:
                self.x_velocity *= self.max_speed / current_speed
                self.y_velocity *= self.max_speed / current_speed
        else:
            # Normalise to friction speed at max
            current_speed = distance((0, 0),
                                     (self.x_velocity, self.y_velocity))
            decel_speed = self.friction  # speed of deceleration

            # If the player is moving slower than the friction rate,
            # cut the deceleration rate down to simply cancel out movement
            if current_speed < decel_speed * delta_time:
                decel_speed = current_speed / delta_time

            if current_speed > 0:
                move_x = -self.x_velocity * decel_speed / current_speed
                move_y = -self.y_velocity * decel_speed / current_speed

            # Decelerate accordingly
            self.x_velocity += move_x * delta_time
            self.y_velocity += move_y * delta_time

        # Move player by velocity
        moved = self.move((self.x_velocity * delta_time,
                           self.y_velocity * delta_time),
                          object_list)

        if self.sprite_angle >= 360:
            self.sprite_angle -= 360

        # Stop velocity if player collided with something
        if not moved:
            self.x_velocity = 0
            self.y_velocity = 0

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
