import pygame

from Objects import Object
from Map import MAP
from Collision import CollisionBox


class PikachuStatue(Object):
    def __init__(self, x, y):
        self.sprite = pygame.image.load('graphics/pikachu.png')
        self.sprite = pygame.transform.smoothscale(self.sprite, (MAP.TILE_SIZE, MAP.TILE_SIZE))
        self.x = x
        self.y = y
        self.collision = CollisionBox((0.0, 0.0), (MAP.TILE_SIZE, MAP.TILE_SIZE), True)
