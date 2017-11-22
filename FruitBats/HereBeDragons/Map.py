import pygame
import random
from tiles import Tile, TILE_TYPES


class MAP:
    """
    Constants for the map.

    Attributes:
        SEA_CHANCE (int): The chance to spawn sea tiles. Larger number is a lower chance.
        TILE_SIZE (int): The length of each side of a tile in pixels. Tiles are square.
        SIZE_Y (int): The height of the map in tiles.
        Size_X (int): The width of the map in tiles.
        POSSIBLE_TILES (list of Tiles): A list of the possible tiles that can be generated. Tiles are instantiated in TILE_TYPES
    """

    SEA_CHANCE = 20  # Larger number, lower sea chance
    TILE_SIZE = Tile.TILE_SIZE  # size of game tiles in pixels
    SIZE_Y = 60
    SIZE_X = 60

    POSSIBLE_TILES = [TILE_TYPES.GRASS, TILE_TYPES.GRASS2, TILE_TYPES.MOUNTAIN, TILE_TYPES.ROCK, TILE_TYPES.SPOOKY]


class MapClass:
    """
    Fully extendable map class. Map dimensions, tile size and the tiles used to generate the map can be set in MAP.

    Attributes:
        map (2d array of Tiles): The game map.
        sea (2d array of Tiles): A temporary array used to generate the sea before it is added to the map.
        img (pygame.Surface): The map image. The tile images are blitted to this surface when the map is generated.
    """

    map = [[0 for x in range(0, MAP.SIZE_X)] for y in range(0, MAP.SIZE_Y)]
    sea = [[None for x in range(0, MAP.SIZE_X)] for y in range(0, MAP.SIZE_Y)]

    img = pygame.Surface((MAP.SIZE_X, MAP.SIZE_Y))

    def __init__(self, seed=0):
        """
        Constructor for MapClass. Creates a map from a seed.

        Args:
            seed (int, optional):  A seed to remember the random map created. Using the same seed to generate a map multiple times will always result in the same map.
        """

        if not (seed == 0):
            random.seed(seed)

        total_weight = 0

        for tile in MAP.POSSIBLE_TILES:
            total_weight += tile.weight  # Gets the total weight if everything in MAP.TILE_INFO

        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                rand = random.randint(0, total_weight)
                ndone = True

                # For each map cell, iterate through possible tiles
                for tile in MAP.POSSIBLE_TILES:  # Turns random number into Map tile
                    rand -= tile.weight

                    if rand <= 0 and ndone:
                        ndone = False
                        self.map[x][y] = tile

                print("Map cell " + str(x) + ", " + str(y) + ": " + str(self.map[x][y]))

        self.map_render()
        self.create_sea()
        self.img = self.sea_render()

    def map_render(self):
        """Renders map array onto img surface."""

        rect = pygame.Surface((MAP.SIZE_X * MAP.TILE_SIZE, MAP.SIZE_Y * MAP.TILE_SIZE))

        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                temp_img = self.map[x][y].image
                rect.blit(temp_img, (x * MAP.TILE_SIZE, y * MAP.TILE_SIZE))

        self.img = rect

    def is_walkable(self, x, y):
        """
        Checks if a tile is walkable.

        Args:
            x (int): x position of tile to check.
            y (int): y position of tile to check.

        Returns:
            Tile.walkable (bool): True if walkable, False if not. Also returns False if the position being checked is outside the array bounds.
        """

        if x >= MAP.SIZE_X or x < 0 or y >= MAP.SIZE_Y or y < 0:
            return False
        else:
            return self.map[x][y].walkable

    def create_sea(self):
        """Checks each on x,1 and 1,y to see if a sea starts, 1 is used as the array has a boarder"""

        for y in range(0, MAP.SIZE_Y):  # Spawns sea starts on the y axis
            number = random.randint(0, MAP.SEA_CHANCE)  # Generate random number to see if sea spawns

            if number == 0:  # If number is 0 change array position to True and run sea_flow_y
                self.sea[0][y] = TILE_TYPES.SEA
                MapClass.sea_flow_y(self, y)

        for x in range(0, MAP.SIZE_X):  # Spawns sea starts on the x axis
            number = random.randint(0, MAP.SEA_CHANCE)

            if number == 0:  # If number is 0 change array position to True and run sea_flow_x
                self.sea[x][0] = TILE_TYPES.SEA
                MapClass.sea_flow_x(self, x)

    def sea_flow_y(self, y):
        """
        Loops placing True in the array until hitting the edge of array.
        Randomly picks the direction starting on y axis.

        Args:
            y (int): y position of sea tile being placed
        """

        x = 0
        while not x >= MAP.SIZE_X-1 and not x < 0 and not y >= MAP.SIZE_Y-1 and not y < 0:
            # While not past the array boundary's
            which_tile = random.randint(0, 3)  # Random int used to pick which direction

            if which_tile == 0:
                if not y == 0:  # Don't check if at top of map
                    y -= 1
                    self.sea[x][y] = TILE_TYPES.SEA  # Up

            if which_tile == 1:
                if not y == MAP.SIZE_Y-1:  # Don't check if at bottom of map
                    y += 1
                    self.sea[x][y] = TILE_TYPES.SEA  # Down

            if which_tile >= 2:
                if not x == MAP.SIZE_X-1:  # Don't check if at right side of map
                    x += 1
                    self.sea[x][y] = TILE_TYPES.SEA  # Right

    def sea_flow_x(self, x):
        """
        Loops placing True in the array until hitting the edge of array.
        Randomly picks the direction starting on x axis.

        Args:
            x (int): x position of sea tile being placed
        """

        y = 0
        while not y >= MAP.SIZE_Y-1 and not y < 0 and not x >= MAP.SIZE_X-1 and not x < 0:
            # While not past the array boundary's
            which_tile = random.randint(0, 3)  # Random int used to pick which direction

            if which_tile == 0:
                if not x == 0:  # Don't check if at left side of map
                    x -= 1
                    self.sea[x][y] = TILE_TYPES.SEA  # Left

            if which_tile == 1:
                if not x == MAP.SIZE_X-1:  # Don't check if at right side of map'
                    x += 1
                    self.sea[x][y] = TILE_TYPES.SEA  # Right

            if which_tile >= 2:
                if not y == MAP.SIZE_Y-1:  # Don't check if at bottom of map
                    y += 1
                    self.sea[x][y] = TILE_TYPES.SEA  # Down

    def sea_render(self):
        """Blits sea images depending on what other places adjacent are seas and sand to some of the edges"""

        surf = self.img

        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                adj = MapClass.sea_check(self, x, y)  # Runs function to check whats next to current tile

                if x <= MAP.SIZE_X and y <= MAP.SIZE_Y:
                    if adj == 1 or adj == 10 or adj == 100 or adj == 1000:  # If at the edge of the sea
                        self.map[x][y] = TILE_TYPES.BEACH  # Changes map array at location for sand
                        temp_sea = self.map[x][y].image  # Get sand
                        surf.blit(temp_sea, ((x * MAP.TILE_SIZE), (y * MAP.TILE_SIZE)))

                    elif adj != 0 and adj != 1 and adj != 10 and adj != 100 and adj != 1000:  # If multiple sea connections
                        self.map[x][y] = TILE_TYPES.SEA  # Changes map array at location for sea
                        temp_sea = self.map[x][y].image # Get sea
                        surf.blit(temp_sea, ((x * MAP.TILE_SIZE), (y * MAP.TILE_SIZE)))

        return surf  # Return edited image

    def sea_check(self, x, y):
        """
        Checks tiles adjacent to the current tile to see if they are sea tiles.

        Args:
            x (int): x position of current tile.
            y (int): y position of current tile.

        Returns:
            num_adj (int): The number of sea tiles adjacent to the current tile.
        """

        num_adj = 0  # Variable to return

        if not x == 0:
            if self.sea[x - 1][y] == TILE_TYPES.SEA:  # Check left
                num_adj += 1

        if not y == MAP.SIZE_Y - 1:
            if self.sea[x][y + 1] == TILE_TYPES.SEA:  # Check up
                num_adj += 10

        if not y == 0:
            if self.sea[x][y - 1] == TILE_TYPES.SEA:  # Check down
                num_adj += 100

        if not x == MAP.SIZE_X - 1:
            if self.sea[x + 1][y] == TILE_TYPES.SEA:  # Check right
                num_adj += 1000

        return num_adj

