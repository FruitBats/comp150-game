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
        timer (int): Timer for fog changes.
    """

    SCREEN_WIDTH = 800*3
    SCREEN_HEIGHT = 600*3
    surface = None
    day = True
    length_of_day = 0
    length_of_night = 0
    timer = 0

    def __init__(self, length_of_day, length_of_night):
        """
        Class Constructor.

        Args:
            length_of_day (int): The length of a day in seconds.
            length_of_night (int): The length of a night in seconds.
        """

        self.surface = self.lift_fog()
        self.length_of_day = length_of_day
        self.length_of_night = length_of_night
        self.timer = length_of_day

    def lift_fog(self):
        """
        Creates a black surface and then renders a circle getting less transparent as it
        spreads out, if its night time the circle of vision is much smaller
        inspiration taken from https://github.com/paddypolson/Foggy/blob/master/gameplay.py
        """

        self.surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.surface.fill((220, 220, 220, 255))

        # TODO: Make fog look nicer and fix functions below. Daytime iterates from alpha 255 to alpha 1 while stepping down the radius.
        # TODO: Nightime iterates from radius to 1, stepping down alpha at the same time. This works ok for night, but not for daytime, as it doesnt have a good cutoff.
        if self.day:
            self.surface.fill((220, 220, 220, 255))

            radius = 450
            for alpha in range(255, 1, -4):
                radius -= 2
                pygame.draw.circle(self.surface, (220, 220, 220, alpha), (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2), int(radius))

        else:
            self.surface.fill((0, 13, 26, 255))
            m = 255 / float(150)

            for i in range(150, 1, -1):
                alpha = i*m
                pygame.draw.circle(self.surface, (0, 13, 26, i * m), (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2), i)

        return self.surface

    def update(self, delta_time):
        """
        Updates the fog state from day to night and vice versa.

        Args:
            delta_time (float): Time passed since last frame.
        """

        # Change day to true or false every #seconds, calls fog function to update surface
        self.timer -= delta_time
        if self.timer <= 0:
            if self.day:
                self.day = not self.day
                self.timer = self.length_of_night # resets timer variable
                self.lift_fog()

            else:
                self.day = not self.day
                self.timer = self.length_of_day  # resets timer variable
                self.lift_fog()

    def render(self, screen):
        """
        Renders the fog. This whole function is too specific... i.e only works if the target is the main Game class and
        contains a player and camera object.

        Args:
            screen (pygame.Surface): The screen to draw the fog on.
        """

        screen.blit(self.surface, (-self.SCREEN_WIDTH / 2 + screen.get_width() / 2, -self.SCREEN_HEIGHT / 2 + screen.get_height() / 2))
