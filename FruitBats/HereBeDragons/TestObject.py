import pygame

from Objects import Object
from Map import MAP
from Collision import CollisionParams


class PikachuStatue(Object):
    def __init__(self, x, y):
        self.sprite = pygame.image.load('graphics/pikachu.png')
        self.sprite = pygame.transform.smoothscale(
                        self.sprite, (MAP.TILE_SIZE, MAP.TILE_SIZE))
        self.sprite = self.sprite.convert(24)
        self.x = x
        self.y = y
        self.collision = CollisionParams((0.0, 0.0),
                                         (MAP.TILE_SIZE, MAP.TILE_SIZE),
                                         True)
