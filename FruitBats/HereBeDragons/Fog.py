import pygame

from Player import *
from Map import MAP
import time


class Fog:
    """
    Fog Class

    Attributes:
        SCREEN_WIDTH (int): The height of the screen, multiplied to ensure the fog always covers the screen.
        SCREEN_WIDTH (int): The width of the screen, multiplied to ensure the fog always covers the screen.
        surface (pygame.Surface): The Surface onto which the fog is drawn.
        day (bool): State of the day. True if day, False if night.
        length_of_day (int): Length of a day in seconds.
        length_of_night (int): Length of a night in seconds.
    """

    SCREEN_WIDTH = 800*3
    SCREEN_HEIGHT = 600*3
    surface = None
    day = True
    length_of_day = 0
    length_of_night = 0

    def __init__(self, start_time, length_of_day, length_of_night):
        """
        Class Constructor.

        Args:
            start_time (float): The initial start time of the game.
            length_of_day (int): The length of a day in seconds.
            length_of_night (int): The length of a night in seconds.
        """

        self.surface = self.lift_fog()
        self.start_time = start_time
        self.length_of_day = length_of_day
        self.length_of_night = length_of_night

    def lift_fog(self):
        """
        Creates a black surface and then renders a circle getting less transparent as it
        spreads out, if its night time the circle of vision is much smaller
        inspiration taken from https://github.com/paddypolson/Foggy/blob/master/gameplay.py
        """

        self.surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 255))

        if self.day:
            m = 255/float(350)  # float used to multiply i increasing the alpha must be close to range to avoid alpha being higher than 255
            for i in range(350, 1, -1):  # loop starts at first number and counts down by 1 until at 1
                pygame.draw.circle(self.surface, (0, 0, 0, i * m), (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2), i)

        else:
            m = 255/float(150)
            for i in range(150, 1, -1):
                pygame.draw.circle(self.surface, (0, 0, 0, i * m), (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2), i)

        return self.surface

    def update(self):
        """Updates the fog state from day to night and vice versa."""

        # Change day to true or false every #seconds, calls fog function to update surface
        current_time = time.time()
        interval = current_time - self.start_time  # gets difference between current time and start time

        if self.day and (interval >= self.length_of_day):
            self.day = not self.day
            self.start_time = current_time  # resets timer variable
            self.lift_fog()

        elif not self.day and (interval >= self.length_of_night):
            self.day = not self.day
            self.start_time = current_time  # resets timer variable
            self.lift_fog()

    def render(self, target):
        """
        Renders the fog. This whole function is too specific... i.e only works if the target is the main Game class and
        contains a player and camera object.

        Args:
            target (main Game class): The class to render the fog from.
        """

        target.screen.blit(self.surface, ((target.player.x - target.camera.x) * MAP.TILE_SIZE - int(target.SCREEN_WIDTH * 1.5 - target.player.sprite.get_width() / 2),
                                          (target.player.y - target.camera.y) * MAP.TILE_SIZE - int(target.SCREEN_HEIGHT * 1.5 - target.player.sprite.get_height() / 2)))
