import math

import pygame

from Map import MapClass, MAP
from Collision import CollisionParams
from Helpers import Vector


class Object:
    # Main variables for characters
    x = 0  # in game tile units (1.0 = 1 tile)
    y = 0  # in game tile units
    sprite = None  # current object sprite (todo: animations etc)
    collision = None  # collision data (None=no collision/ghost)
    sprite_angle = 0  # angle of rotation for this sprite in degrees
    sprite_origin = None  # origin of sprite
    debug_render_hitbox = False  # whether to render the hitbox (for debugging)
    debug_dyna = None

    def __init__(self, x, y):
        """Initialise object at the given position"""
        self.x = x
        self.y = y
        self.collision = CollisionParams((0.0, 0.0), (1.0, 1.0), True)

    def update(self, delta_time, player, object_list, map):
        self.debug_dyna = player.dynasword
        pass  # to be overloaded by objects

    def render(self, screen, camera):
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
                # Declare X and Y position to draw at
                place_x = self.x * MAP.TILE_SIZE
                place_y = self.y * MAP.TILE_SIZE

                # Move back to centre of rotated image, which is always static
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

                # Blit!
                screen.blit(rotated_sprite,
                            (place_x - camera.x * MAP.TILE_SIZE,
                             place_y - camera.y * MAP.TILE_SIZE))
            else:
                if isinstance(self.sprite_origin, Vector):
                    # Draw sprite at origin
                    screen.blit(self.sprite, ((self.x - camera.x) * MAP.TILE_SIZE - self.sprite_origin.x, (self.y - camera.y) * MAP.TILE_SIZE - self.sprite_origin.y))
                else:
                    # Draw regular sprite
                    screen.blit(self.sprite,
                                ((self.x - camera.x) * MAP.TILE_SIZE,
                                 (self.y - camera.y) * MAP.TILE_SIZE))
        if self.debug_render_hitbox and self.collision:
            # Draw a collision box around the sprite
            camera_vector = Vector(camera.x, camera.y)

            coll_origin = (Vector(self.x, self.y) - camera_vector) * MAP.TILE_SIZE + Vector(self.collision.x, self.collision.y)

            if self.sprite_origin:
                coll_origin -= self.get_right() * self.sprite_origin.x
                coll_origin -= self.get_down() * self.sprite_origin.y

            coll_right = self.get_right() * self.collision.width * MAP.TILE_SIZE
            coll_down = self.get_down() * self.collision.height * MAP.TILE_SIZE

            # Check collision with player dynasword
            if self.debug_dyna:
                other_coll_origin = Vector(self.debug_dyna.x, self.debug_dyna.y)

                if self.debug_dyna.sprite_origin:
                    other_coll_origin -= self.debug_dyna.get_right() * self.debug_dyna.sprite_origin.x
                    other_coll_origin -= self.debug_dyna.get_down() * self.debug_dyna.sprite_origin.y

                other_coll_right = self.debug_dyna.get_right() * self.debug_dyna.collision.width * MAP.TILE_SIZE
                other_coll_down = self.debug_dyna.get_down() * self.debug_dyna.collision.height * MAP.TILE_SIZE

            # Render sides of box
            # Draw origin
            pygame.draw.circle(screen, (255, 0, 0), (int(coll_origin.x), int(coll_origin.y)), 3, 1)
            # Draw left
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin), tuple(coll_origin + coll_down), 1)
            # Draw bottom
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_down), tuple(coll_origin + coll_down + coll_right), 1)
            # Draw right
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_down + coll_right), tuple(coll_origin + coll_right), 1)
            # Draw top
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_right), tuple(coll_origin), 1)

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
            box_origin = Vector(self.x, self.y) + Vector(self.collision.x, self.collision.y)
            if self.sprite_origin:
                box_origin -= self.get_right() * self.sprite_origin.x / MAP.TILE_SIZE
                box_origin -= self.get_down() * self.sprite_origin.y / MAP.TILE_SIZE
            box_right = self.get_right() * self.collision.width
            box_down = self.get_down() * self.collision.height

            box_top_left = box_origin
            box_top_right = box_origin + box_right
            box_bottom_right = box_top_right + box_down
            box_bottom_left = box_origin + box_down

            # Check with other objects
            for object in object_list:
                if object == self:
                    continue  # don't collide with yourself plz
                if not (object.collision and object.collision.solid):
                    continue  # don't collide with nonsolids
                obj_box_origin = Vector(object.x, object.y) + Vector(object.collision.x, object.collision.y)
                if object.sprite_origin:
                    obj_box_origin -= object.get_right() * object.sprite_origin.x / MAP.TILE_SIZE
                    obj_box_origin -= object.get_down() * object.sprite_origin.y / MAP.TILE_SIZE
                obj_box_right = object.get_right() * object.collision.width
                obj_box_down = object.get_down() * object.collision.height

                obj_box_top_left = obj_box_origin
                obj_box_top_right = obj_box_origin + obj_box_right
                obj_box_bottom_right = obj_box_top_right + obj_box_down
                obj_box_bottom_left = obj_box_origin + obj_box_down

                for i in xrange(0, 1)
                    desired_x = self.x
                    desired_y = self.y
                    collided = True
"""        if self.collision and self.collision.solid:
            # Determine current area of our collision box
            box_left = desired_x + self.collision.x
            box_top = desired_y + self.collision.y
            box_right = box_left + self.collision.width
            box_bottom = box_top + self.collision.height

            # Check with other objects
            for object in object_list:
                if object == self:
                    continue  # don't collide with yourself plz
                if not (object.collision and object.collision.solid):
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
                    collided = True"""

        self.x = desired_x
        self.y = desired_y
        return not collided

    def get_down(self):
        """Returns local 'down' Vector according to sprite rotation. Default is 0,1"""
        return Vector(math.sin(math.radians(self.sprite_angle)), math.cos(math.radians(self.sprite_angle)))

    def get_right(self):
        """Returns local 'right' Vector according to sprite rotation. Default is 1,0"""
        return Vector(math.cos(math.radians(self.sprite_angle)), -math.sin(math.radians(self.sprite_angle)))