import pygame


class Tile:
    TILE_SIZE = 80

    weight = 0
    image = None
    walkable = True

    def __init__(self, weight, image, walkable):
        """
        Class constructor

        Args:
            weight (int): Spawn weighting.
            image (string): Image file path.
            walkable (bool): If the player can walk on this tile.
        """

        self.weight = weight
        self.image = pygame.image.load(image)
        self.walkable = walkable


class TILE_TYPES:
    """Map tile types are instantiated here"""

    # Passable tiles
    GRASS = Tile(20, "ImageFiles/Ground/temp_grass.jpg", True)
    GRASS2 = Tile(5, "ImageFiles/Ground/temp_grass2.jpg", True)
    SPOOKY = Tile(1, "ImageFiles/Ground/temp_spooky.jpg", True)

    # Impassable tiles
    MOUNTAIN = Tile(3, "ImageFiles/Ground/temp_mountain.jpg", False)
    ROCK = Tile(2, "ImageFiles/Ground/temp_rock.jpg", False)  # This could be changed to  be walkable. Too many impassable tiles may break game flow.

    # Sea tiles
    SEA = Tile(0, "ImageFiles/Sea/Sea.jpg", False)
    BEACH = Tile(0, "ImageFiles/Sea/Sand.jpg", True)

    # Testing tiles
    GRID_GRASS = Tile(20, "ImageFiles/Ground/test_grid_grass.jpg", True)
    GRID_MOUNTAIN = Tile(5, "ImageFiles/Ground/test_grid_mountain.jpg", False)