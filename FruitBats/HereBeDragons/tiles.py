import pygame


class Tile:
    """
    Tile class. Contains the data for a single tile on the game map.

    Attributes:
        TILE_SIZE (int): The size of the tiles in pixels. (Tiles are square)

        weight (int): Higher weighting equals greater chance of a tile being generated.
        image (pygame.Surface): The image for the tile.
        walkable (bool): If the tile can be walked on by the player and enemies.
    """

    TILE_SIZE = 64

    weight = 0
    image = None
    walkable = True

    def __init__(self, weight, image, walkable, background_image=None):
        """
        Class constructor

        Args:
            weight (int): Spawn weighting.
            image (string): Image file path.
            walkable (bool): If the player can walk on this tile.
            background_image (string, optional): Defaults to None. The file path for the background image. To be used when the main image has transparent areas.
        """

        self.weight = weight
        self.image = pygame.transform.scale(pygame.image.load(image), (self.TILE_SIZE, self.TILE_SIZE))
        self.walkable = walkable

        if background_image is not None:
            self.background_image = pygame.transform.scale(pygame.image.load(background_image), (self.TILE_SIZE, self.TILE_SIZE))
            self.background_image.blit(self.image, self.background_image.get_rect())
            self.image = self.background_image


class TILE_TYPES:
    """Map tile types are instantiated here"""

    # Passable tiles
    GRASS = Tile(20, "ImageFiles/sprites test/terrain2.png", True)
    GRASS2 = Tile(5, "ImageFiles/sprites test/terrain3.png", True)

    FOREST = Tile(1, "ImageFiles/sprites test/terrain4.png", True, "ImageFiles/sprites test/terrain2.png")
    FOREST2 = Tile(1, "ImageFiles/sprites test/terrain5.png", True, "ImageFiles/sprites test/terrain2.png")
    FOREST3 = Tile(1, "ImageFiles/sprites test/terrain6.png", True, "ImageFiles/sprites test/terrain2.png")

    # Impassable tiles
    MOUNTAIN = Tile(3, "ImageFiles/sprites test/terrain10.png", False, "ImageFiles/sprites test/terrain2.png")
    MOUNTAIN2 = Tile(3, "ImageFiles/sprites test/terrain11.png", False, "ImageFiles/sprites test/terrain2.png")
    MOUNTAIN3 = Tile(3, "ImageFiles/sprites test/terrain12.png", False, "ImageFiles/sprites test/terrain2.png")

    TOWER = Tile(2, "ImageFiles/sprites test/terrain22.png", False, "ImageFiles/sprites test/terrain2.png")

    # Sea tiles
    SEA = Tile(0, "ImageFiles/Sea/Sea.jpg", False)  # TODO: Maybe change this to walkable for the demo, to reduce chances of being trapped by sea.
    BEACH = Tile(0, "ImageFiles/Sea/Sand.jpg", True)