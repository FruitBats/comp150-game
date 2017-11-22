import pygame

# TODO add colliders and check collision!

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
    GRASS = Tile(20, "ImageFiles/Ground/temp_grass.jpg", True)
    GRASS2 = Tile(5, "ImageFiles/Ground/temp_grass2.jpg", True)
    MOUNTAIN = Tile(3, "ImageFiles/Ground/temp_mountain.jpg", False)
    ROCK = Tile(2, "ImageFiles/Ground/temp_rock.jpg", False)
    SPOOKY = Tile(1, "ImageFiles/Ground/temp_spooky.jpg", True)

    GRID_GRASS = Tile(20, "ImageFiles/Ground/test_grid_grass.jpg", True)
    GRID_MOUNTAIN = Tile(5, "ImageFiles/Ground/test_grid_mountain.jpg", False)