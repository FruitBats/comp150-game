import math

from Map import MAP
from Helpers import *

class CollisionBox:
    x = 0  # X offset of collision box in tiles (relative to sprite) (todo sprite origin compatibility)
    y = 0  # Y offset of collision box in tiles
    width = 0  # Width of collision box in tiles
    height = 0  # Height of collision box in tiles
    solid = False  # Whether this collision box should block objects in move()

    def __init__(self, (x, y), (width, height), solid):
        """Initialises collision box, in pixels

        Arguments:
            (x, y): Origin of the collision box (sprite_origin ignored!)
            (width, height): Dimensions of the collision box, in pixels
            solid: (bool) Whether the collision box is currently solid
        Returns: none
        """
        self.x = float(x) / float(MAP.TILE_SIZE)
        self.y = float(y) / float(MAP.TILE_SIZE)
        self.width = float(width) / float(MAP.TILE_SIZE)
        self.height = float(height) / float(MAP.TILE_SIZE)
        self.solid = solid

    def get_bounding_box(self, rotation=0, (x_origin, y_origin)=(0, 0), (x_offset, y_offset)=(0, 0)):
        """Returns the absolute bounding box of this collision box when hypothetically rotated around an origin, returning a pygame.Rect

        Arguments:
            rotation (float): Angle of the box in degrees
            (x_origin, y_origin) (int): Origin of the rotation in pixels.
            (x_offset, y_offset) (float): Offset to add to the box in tiles
        Returns (float): tuple containing left x, top y, right x and bottom y of the bounding box, in tiles
        """
        if rotation is None or float(rotation) is 0.0:
            # Return a simple bounding box instead of processing a zero rotation
            return (self.x - x_origin/float(MAP.TILE_SIZE) + x_offset, self.y - y_origin/float(MAP.TILE_SIZE) + y_offset,
                    self.x + self.width - x_origin/float(MAP.TILE_SIZE) + x_offset, self.y + self.height - y_origin/float(MAP.TILE_SIZE) + y_offset)

        # Define tile origin in tile units
        tile_origin = (x_origin / float(MAP.TILE_SIZE), y_origin / float(MAP.TILE_SIZE))

        # Define initial border, shifted according to sprite_origin
        x1 = self.x - tile_origin[0]
        y1 = self.y - tile_origin[1]
        x2 = x1 + self.width
        y2 = y1 + self.height

        # Rotate the border points
        rot_sin = math.sin(math.radians(rotation))
        rot_cos = math.cos(math.radians(rotation))
        corners = [x1, y1, x2, y1, x2, y2, x1, y2]  # points (could be tuples; raw coordinates are instead used for performance)

        # Initialise borders using te first point as reference (main alternative is using magic numbers...)
        border_x1 = corners[0] * rot_cos + corners[1] * rot_sin
        border_y1 = corners[1] * rot_cos - corners[0] * rot_sin
        border_x2 = border_x1
        border_y2 = border_y1

        for i in xrange(2, 8, 2):
            rot_x = corners[i] * rot_cos + corners[i + 1] * rot_sin
            rot_y = corners[i + 1] * rot_cos - corners[i] * rot_sin
            if rot_x < border_x1:
                border_x1 = rot_x
            if rot_x > border_x2:
                border_x2 = rot_x
            if rot_y < border_y1:
                border_y1 = rot_y
            if rot_y > border_y2:
                border_y2 = rot_y

        return (border_x1 + x_offset, border_y1 + y_offset, border_x2 + x_offset, border_y2 + y_offset)

    def line_intersection(self, line_start, line_end, rotation=0, (x_origin, y_origin)=(0, 0), (x_offset, y_offset)=(0, 0)):
        """Tests if a line collides with this collision box
            Arguments:
                line_start: (Vector) Starting point of the line
                line_end: (Vector) Ending point of the line
                rotation: (float) Rotation of the collision box in degrees
                (x_origin, y_origin): (float) Origin of rotation, in pixels (usually mapped to sprite)
                (x_offset, y_offset): (float) Position of this collision box, in tiles
            Returns:
                (Boolean) Whether or not the line intersects the collision box"""
        down = Vector(math.sin(math.radians(rotation)), math.cos(math.radians(rotation))) * self.height
        right = Vector(math.cos(math.radians(rotation)), -math.sin(math.radians(rotation))) * self.width

        corners = [Vector(x_offset + self.x, y_offset + self.y) - down * ((y_origin / MAP.TILE_SIZE) / self.height) - right * ((x_origin / MAP.TILE_SIZE) / self.width)]
        corners.append(corners[0] + right)
        corners.append(corners[1] + down)
        corners.append(corners[0] + down)

        for i in xrange(0, 4):
            if Vector.intersection(line_start, line_end, corners[i], corners[(i + 1) % 4]):
                return True
        return False