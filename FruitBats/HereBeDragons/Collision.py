from Map import MAP


class CollisionParams:
    shape = 0  # Todo: Add sphere collision etc?
    x = 0  # X offset of collision box in tiles (relative to parent object)
    y = 0  # Y offset of collision box in tiles
    width = 0  # Width of collision box in tiles
    height = 0  # Height of collision box in tiles
    solid = False  # Whether this collision box should block objects in move()

    def __init__(self, (x, y), (width, height), solid):
        """Initialises collision box, in pixels

        Arguments:
            (x, y): Origin of the collision box, in pixels
            (width, height): Dimensions of the collision box, in pixels
            solid: (bool) Whether the collision box is currently solid
        Returns: none
        """
        self.x = float(x) / float(MAP.TILE_SIZE)
        self.y = float(y) / float(MAP.TILE_SIZE)
        self.width = float(width) / float(MAP.TILE_SIZE)
        self.height = float(height) / float(MAP.TILE_SIZE)
        self.solid = solid
