import pygame


class Tile:
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
    """
    # Passable tiles
    GRASS = Tile(20, "ImageFiles/Ground/temp_grass.jpg", True)
    GRASS2 = Tile(5, "ImageFiles/Ground/temp_grass2.jpg", True)
    SPOOKY = Tile(1, "ImageFiles/Ground/temp_spooky.jpg", True)

    # Impassable tiles
    MOUNTAIN = Tile(3, "ImageFiles/Ground/temp_mountain.jpg", False)
    ROCK = Tile(2, "ImageFiles/Ground/temp_rock.jpg", False)  # This could be changed to  be walkable. Too many impassable tiles may break game flow.
    """

    # Sea tiles
    SEA = Tile(0, "ImageFiles/Sea/Sea.jpg", False)
    BEACH = Tile(0, "ImageFiles/Sea/Sand.jpg", True)

    # Testing tiles
    # Passable tiles
    GRASS = Tile(20, "ImageFiles/sprites test/terrain2.png", True)
    GRASS2 = Tile(5, "ImageFiles/sprites test/terrain3.png", True)
    SPOOKY = Tile(1, "ImageFiles/sprites test/terrain4.png", True, "ImageFiles/sprites test/terrain2.png")

    # Impassable tiles
    MOUNTAIN = Tile(3, "ImageFiles/sprites test/terrain10.png", False, "ImageFiles/sprites test/terrain2.png")
    ROCK = Tile(2, "ImageFiles/sprites test/terrain22.png", False, "ImageFiles/sprites test/terrain2.png")  # This could be changed to  be walkable. Too many impassable tiles may break game flow.