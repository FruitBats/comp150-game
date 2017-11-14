import pygame

from Player import *


class Fog:

    SCREEN_WIDTH = 800*3
    SCREEN_HEIGHT = 600*3
    surface = None
    day = True

    def __init__(self):
        self.surface = self.lift_fog()

    def lift_fog(self):
        """Creates a black surface and then renders a circle getting less transparent as it
        spreads out, if its night time the circle of vision is much smaller"""
        self.surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 255))
        if self.day:
            m = 255/float(350)  # float used to multiply i increasing the alpha must be close
            # to range to avoid alpha being higher than 255
            for i in range(350, 1, -1):  # loop starts at first number and counts down by 1 until at 1
                pygame.draw.circle(self.surface, (0, 0, 0, i*m), (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2), i)
        else:
            m = 255/float(150)
            for i in range(150, 1, -1):
                pygame.draw.circle(self.surface, (0, 0, 0, i*m), (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2), i)
        return self.surface

