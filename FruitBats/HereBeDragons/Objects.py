import math

import pygame

from Map import MapClass
from Collision import CollisionParams
from Helpers import Vector


class Object:
    # Main variables for characters
    x = 0  # in game tile units (1.0 = 1 tile)
    y = 0  # in game tile units
    sprite = None  # current object sprite (todo: animations etc)
    sprite_angle = 0  # angle of rotation for this sprite in degrees
    sprite_origin = None  # origin of sprite
    collision = None  # collision data (instantiate this in __init__)

    def __init__(self, x, y):
        """Initialise object at the given position"""
        self.x = x
        self.y = y
        self.collision = CollisionParams((0.0, 0.0), (1.0, 1.0), True)

    def update(self, delta_time, player, object_list, map):
        pass  # to be overloaded by objects

    def render(self, screen):
        """Renders the object (function overloadable by subclasses)"""
        if self.sprite is not None:
            if self.sprite_angle is not 0:
                # Clamp sprite_angle to 0 <= x < 360 with math magic
                self.sprite_angle -= int(self.sprite_angle / 360) * 360
                if self.sprite_angle < 0:
                    self.sprite_angle -= int((self.sprite_angle / 360) - 1) \
                                            * 360

                # Draw rotated sprite
                rotated_sprite = pygame.transform.rotate(self.sprite,
                                                         self.sprite_angle)

                # Behold my somehow-rotate-around-an-origin code!
                # Declare X and Y position to draw...
                place_x = self.x * MapClass.TILE_SIZE
                place_y = self.y * MapClass.TILE_SIZE

                # Move back to centre of rotated image, which is always
                # static
                place_x -= rotated_sprite.get_width() / 2
                place_y -= rotated_sprite.get_height() / 2

                # Find the centre of the original image
                centre_x = self.sprite.get_width() / 2
                centre_y = self.sprite.get_height() / 2

                if isinstance(self.sprite_origin, Vector):
                    # Perform a shift by the inverted origin, rotated
                    sine = math.sin(math.radians(self.sprite_angle))
                    cosine = math.cos(math.radians(self.sprite_angle))

                    # Shift along the X pixels by origin X
                    place_x -= cosine * (self.sprite_origin.x - centre_x)
                    place_y += sine * (self.sprite_origin.x - centre_x)
                    # Shift along the Y pixels by origin Y
                    place_x -= sine * (self.sprite_origin.y - centre_y)
                    place_y -= cosine * (self.sprite_origin.y - centre_y)

                # Move to origin
                # TODO--Origin rotation, so hard

                # Blit!
                screen.blit(rotated_sprite, (place_x, place_y))
            else:
                if isinstance(self.sprite_origin, Vector):
                    # Draw sprite at origin
                    screen.blit(
                        self.sprite,
                        (self.x * MapClass.TILE_SIZE - self.sprite_origin.x,
                         self.y * MapClass.TILE_SIZE - self.sprite_origin.y))
                else:
                    # Draw regular sprite
                    screen.blit(self.sprite,
                                (self.x * MapClass.TILE_SIZE,
                                 self.y * MapClass.TILE_SIZE))

    def move(self, (move_x, move_y), object_list):
        """Performs collision checking and moves object by offset of
           move_x and move_y if possible

           (move_x, move_y) -- How far to move, in tile units
           object_list -- List of objects in the environment (for
                          collision)

           Todo: Push the player out of a surface in the opposite
           direction to their attempted movement, return a vector
           portraying how much they moved
        """

        # Decide where the object is (trying) to go
        desired_x = self.x + move_x
        desired_y = self.y + move_y
        collided = False

        # Perform collision detection with objects
        if self.collision and self.collision.solid:
            # Determine current area of our collision box
            box_left = desired_x + self.collision.x
            box_top = desired_y + self.collision.y
            box_right = box_left + self.collision.width
            box_bottom = box_top + self.collision.height
            # Check with other objects
            for object in object_list:
                if object == self:
                    continue  # don't collide with yourself plz
                if not (object.collision or object.collision.solid):
                    continue  # don't collide with nonsolids
                obj_box_left = object.x + object.collision.x
                obj_box_top = object.y + object.collision.y
                obj_box_right = obj_box_left + object.collision.width
                obj_box_bottom = obj_box_top + object.collision.height
                if not (box_left >= obj_box_right or
                                box_right <= obj_box_left or
                                box_top >= obj_box_bottom or
                                box_bottom <= obj_box_top):
                    desired_x = self.x
                    desired_y = self.y
                    collided = True

        self.x = desired_x
        self.y = desired_y
        return not collided
