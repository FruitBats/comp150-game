import math

import pygame

from Map import MapClass, MAP
from Collision import CollisionBox
from Helpers import Vector


class Object(object):
    """Base class for movable game object (including characters)
        Args:
            x, y (float): Position of the objects, in game tile units
            sprite (pygame.Surface): Current object sprite
            collision (CollisionBox): Collision data, or None if there is no collision box
            sprite_angle (float property): Sprite angle of rotation, in anticlockwise degrees
            sprite_origin (Vector): Origin of the object, in pixels relative to its sprite image
            dead (Boolean): Whether the object is dead. When a dead object is acknowledged by the Game class, it is destroyed and removed from the object list
            debug_render_hitbox (Boolean): When True, draws the collision box over the object
    """
    x = 0
    y = 0
    sprite = None
    collision = None
    _sprite_angle = 0
    sprite_origin = None
    dead = False
    debug_render_hitbox = False

    parent_map = None # The map the object is created on
    debug_dyna = None

    def __init__(self, x, y, parent_map):
        """Initialise object at the given position
            Args:
                x (float): x position to spawn the object at, in tile units
                y (float): y position to spawn the object at, in tile units
                parent_map (MapClass): Map on which the object lives"""
        self.x = x
        self.y = y
        self.collision = CollisionBox((0.0, 0.0), (1.0, 1.0), True)
        self.parent_map = parent_map

    def update(self, delta_time, player, object_list, map):
        self.debug_dyna = player.dynasword
        pass  # to be overridden by subclasses

    def render(self, screen, camera):
        """Renders the object to the game screen
            Args:
                screen (pygame.Surface): Screen surface to render the sprite to
                camera (Camera): The game camera"""
        camera_vector = Vector(camera.x, camera.y)

        if self.sprite is not None:
            if self.sprite_angle is not 0:
                # Draw rotated sprite
                rotated_sprite = pygame.transform.rotate(self.sprite, self.sprite_angle)

                # Behold my somehow-rotate-around-an-origin code!
                # Declare X and Y position to draw at
                place = Vector(self.x * MAP.TILE_SIZE, self.y * MAP.TILE_SIZE)

                # Move back to centre of rotated image, which is always static
                place -= Vector(float(rotated_sprite.get_width()) / 2, float(rotated_sprite.get_height()) / 2)

                # Find the centre of the original image
                centre = Vector(self.sprite.get_width() / 2, self.sprite.get_height() / 2)

                if isinstance(self.sprite_origin, Vector):
                    # Perform a shift by the inverted origin, rotated
                    sine = math.sin(math.radians(self.sprite_angle))
                    cosine = math.cos(math.radians(self.sprite_angle))

                    # Shift along the X pixels by origin X
                    place.x -= cosine * (self.sprite_origin.x - centre.x)
                    place.y += sine * (self.sprite_origin.x - centre.x)
                    # Shift along the Y pixels by origin Y
                    place.x -= sine * (self.sprite_origin.y - centre.y)
                    place.y -= cosine * (self.sprite_origin.y - centre.y)
                else:
                    # Perform a shift by 0,0, rotated
                    sine = math.sin(math.radians(self.sprite_angle))
                    cosine = math.cos(math.radians(self.sprite_angle))

                    # Shift along the X pixels by origin X
                    place.x -= cosine * -centre.x
                    place.y += sine * -centre.x
                    # Shift along the Y pixels by origin Y
                    place.x -= sine * -centre.y
                    place.y -= cosine * -centre.y

                # Blit!
                screen.blit(rotated_sprite, tuple(place - camera_vector * MAP.TILE_SIZE))
            else:
                if isinstance(self.sprite_origin, Vector):
                    # Draw sprite at origin
                    screen.blit(self.sprite, ((self.x - camera.x) * MAP.TILE_SIZE - self.sprite_origin.x, (self.y - camera.y) * MAP.TILE_SIZE - self.sprite_origin.y))
                else:
                    # Draw regular sprite
                    screen.blit(self.sprite, ((self.x - camera.x) * MAP.TILE_SIZE, (self.y - camera.y) * MAP.TILE_SIZE))

        if self.debug_render_hitbox and self.collision:
            # Draw a collision box around the sprite
            # Prepare (potentially rotated) collision box vectors
            coll_origin = ((Vector(self.x, self.y) - camera_vector) + Vector(self.collision.x, self.collision.y)) * MAP.TILE_SIZE

            if self.sprite_origin:
                coll_origin -= self.get_right() * self.sprite_origin.x
                coll_origin -= self.get_down() * self.sprite_origin.y

            coll_right = self.get_right() * self.collision.width * MAP.TILE_SIZE
            coll_down = self.get_down() * self.collision.height * MAP.TILE_SIZE

            # Render sides of box
            # Draw pivot point
            if self.sprite_origin:
                centre_point = (Vector(self.x, self.y) - camera_vector) * MAP.TILE_SIZE
                pygame.draw.circle(screen, (255, 0, 0), (int(centre_point.x), int(centre_point.y)), 3, 1)
            else:
                pygame.draw.circle(screen, (255, 0, 0), (int(coll_origin.x), int(coll_origin.y)), 3, 1)
            # Draw left
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin), tuple(coll_origin + coll_down), 1)
            # Draw bottom
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_down), tuple(coll_origin + coll_down + coll_right), 1)
            # Draw right
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_down + coll_right), tuple(coll_origin + coll_right), 1)
            # Draw top
            pygame.draw.line(screen, (255, 0, 0), tuple(coll_origin + coll_right), tuple(coll_origin), 1)

            # Render bounding box
            if self.sprite_angle is not 0:
                x_off = (self.x - camera.x) * MAP.TILE_SIZE
                y_off = (self.y - camera.y) * MAP.TILE_SIZE
                bounds = self.collision.get_bounding_box(self.sprite_angle, self.sprite_origin)
                bounds_rect = pygame.Rect(x_off + bounds[0]*MAP.TILE_SIZE, y_off + bounds[1]*MAP.TILE_SIZE, (bounds[2] - bounds[0])*MAP.TILE_SIZE, (bounds[3] - bounds[1])*MAP.TILE_SIZE)
                pygame.draw.rect(screen, (0, 0, 0), bounds_rect, 1)

    def move(self, (move_x, move_y), object_list):
        """Performs collision checking and moves the object, if possible

            Args:
                (move_x, move_y) -- How far to move, in tile units
                object_list -- List of objects in the environment
            Returns:
                Whether or not the move was successful (False is returned if a collision occurs)
        """

        # Test one step ahead. If the area is clear, self.x and self.y are set to the desired movement location
        desired_x = self.x + move_x
        desired_y = self.y + move_y
        collided = False

        # Perform collision detection with objects
        if self.collision and self.collision.solid:
            # Determine current area of our collision box
            if self.sprite_origin:
                self_box = self.collision.get_bounding_box(self.sprite_angle, tuple(self.sprite_origin), (desired_x, desired_y))
            else:
                self_box = self.collision.get_bounding_box(self.sprite_angle, (0, 0), (desired_x, desired_y))

            # Check with other objects
            for obj in object_list:
                if obj == self:
                    continue  # don't collide with yourself plz
                if not (obj.collision and obj.collision.solid):
                    continue  # don't collide with non-solids

                if obj.sprite_origin:
                    obj_box = obj.collision.get_bounding_box(obj.sprite_angle, tuple(obj.sprite_origin), (obj.x, obj.y))
                else:
                    obj_box = obj.collision.get_bounding_box(obj.sprite_angle, (0, 0), (obj.x, obj.y))

                if not (self_box[0] >= obj_box[2] or self_box[2] <= obj_box[0] or self_box[1] >= obj_box[3] or self_box[3] <= obj_box[1]):
                    desired_x = self.x
                    desired_y = self.y
                    collided = True

            # Map Collision detection
            # Check walkable for all tiles surrounding object.
            for x in xrange(int(math.floor(self_box[0])), int(math.ceil(self_box[2]) + 1)):
                for y in xrange(int(math.floor(self_box[1])), int(math.ceil(self_box[3])+ 1)):
                    if MapClass.is_walkable(self.parent_map, x, y):
                        pass

                    else:
                        # Create tile's collision box
                        tile_box_left = x
                        tile_box_top = y
                        tile_box_right = x + 1
                        tile_box_bottom = y + 1

                        # Check collision
                        if not (self_box[0] >= tile_box_right or self_box[2] <= tile_box_left or self_box[1] >= tile_box_bottom or self_box[3] <= tile_box_top):
                            desired_x = self.x
                            desired_y = self.y
                            collided = True

        # Update position and return
        self.x = desired_x
        self.y = desired_y

        return not collided

    def get_pos_at_pixel(self, (pixel_x, pixel_y)):
        """Converts a position within the object's sprite to its exact tile position on a map. Useful with rotatable objects.
            Arguments:
                (pixel_x, pixel_y) (float): X and Y position in the sprite
            Returns:
                (Vector) The position on the map
        """
        if self.sprite_origin is not None:
            if self.sprite_angle == 0.0:
                return Vector(self.x + (float(pixel_x) - self.sprite_origin.x) / MAP.TILE_SIZE, self.y + (float(pixel_y) - self.sprite_origin.y) / MAP.TILE_SIZE)
            else:
                vec = Vector(self.x, self.y)
                vec += self.get_right() * ((float(pixel_x - self.sprite_origin.x)) / MAP.TILE_SIZE)
                vec += self.get_down() * ((float(pixel_y - self.sprite_origin.y)) / MAP.TILE_SIZE)
                return vec
        else:
            if self.sprite_angle == 0.0:
                return Vector(self.x + float(pixel_x) / MAP.TILE_SIZE, self.y + float(pixel_y) / MAP.TILE_SIZE)
            else:
                vec = Vector(self.x, self.y)
                vec += self.get_right() * (float(pixel_x) / MAP.TILE_SIZE)
                vec += self.get_down() * (float(pixel_y) / MAP.TILE_SIZE)
                return vec

    def get_down(self):
        """Returns local 'down' Vector according to sprite rotation. Default is 0,1"""
        return Vector(math.sin(math.radians(self.sprite_angle)), math.cos(math.radians(self.sprite_angle)))

    def get_right(self):
        """Returns local 'right' Vector according to sprite rotation. Default is 1,0"""
        return Vector(math.cos(math.radians(self.sprite_angle)), -math.sin(math.radians(self.sprite_angle)))

    @property
    def sprite_angle(self):
        """sprite_angle getter"""
        return self._sprite_angle

    @sprite_angle.setter
    def sprite_angle(self, angle):
        """sprite_angle setter: sets the sprite angle with a cyclic clamp to 0 or 360"""
        self._sprite_angle = angle

        # Clamp sprite_angle to 0 <= x < 360 with math magic
        if self._sprite_angle >= 360:
            self._sprite_angle -= int(self._sprite_angle / 360) * 360
        if self._sprite_angle < 0:
            self._sprite_angle -= int((self._sprite_angle / 360) - 1) * 360