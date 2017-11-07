import pygame

from Player import Player


class Fog:

    SCREEN_WIDTH = 640*3
    SCREEN_HEIGHT = 480*3
    fog = None

    def __init__(self):
        self.fog = self.lift_fog()

    def lift_fog(self):
        self.fog = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.fog.fill((0, 0, 0))
        pygame.draw.circle(self.fog, (60, 60, 60), (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2), int(self.SCREEN_HEIGHT * 0.15), 0)
        self.fog.set_colorkey((60, 60, 60))
        return self.fog

