import pygame

from Objects import Object
from Map import MapClass
from Collision import CollisionParams


class PikachuStatue(Object):
    def __init__(self, x, y):
        self.sprite = pygame.image.load('graphics/pikachu.png')
        self.sprite = pygame.transform.smoothscale(
                        self.sprite,
                        (MapClass.TILE_SIZE, MapClass.TILE_SIZE))
        self.sprite = self.sprite.convert(24)
        self.x = x
        self.y = y
        self.collision = CollisionParams((0.0, 0.0),
                                         (MapClass.TILE_SIZE,
                                          MapClass.TILE_SIZE),
                                         True)
