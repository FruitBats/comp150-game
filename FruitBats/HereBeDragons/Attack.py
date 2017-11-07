import pygame
import math

from Objects import Object
from Collision import CollisionParams
from Map import MapClass, MAP


class Swipe(Object):
    original_sprite = None
    swiping = False  # swipe animation set to false
    swipe_direction = 0  #
    swipe_angle = 0  # angle of a swipe animation that started upon mouse click

    def __init__(self, x, y):
        self.original_sprite = pygame.image.load("graphics/sword.png")
        self.sprite = self.original_sprite  # making a copy of an image
        self.x = x
        self.y = y
        self.collision = CollisionParams((0, 0), (32, 32), False)

    def update(self, delta_time, player, object_list, map):
        # looking for mouse's x value
        mouse_x = float(pygame.mouse.get_pos()[0]) / MAP.TILE_SIZE
        # looking for mouse's y value
        mouse_y = float(pygame.mouse.get_pos()[1]) / MAP.TILE_SIZE
        # sets and object (sword) to point at mouse position
        angle_to_mouse = float(math.atan2((self.y - mouse_y),
                                          (mouse_x - self.x)))
        if not self.swiping:
            # making sword stay horizontally so that it points at a mouse
            self.sprite_angle = float(math.degrees(angle_to_mouse) - 90)
        if pygame.mouse.get_pressed()[0]:
            self.swiping = True  # sets swiping to True upon mouse click
            if self.swipe_direction == 0:
                # checks if mouse button has just been clicked
                self.sprite_angle -= 360 * delta_time
                # makes sword swipe down
                self.swipe_angle += delta_time * 360
                # sets angle of a swipe for later check
                if self.swipe_angle >= 45:
                    # checks if swipe angle reached 45 degrees
                    # to change direction
                    self.swipe_direction = 1
            elif self.swipe_direction == 1:
                # checks if swipe angle has reached its first limit
                self.sprite_angle += 360 * delta_time
                # makes sword swipe up
                self.swipe_angle -= delta_time * 360
                # changed swipe angle backwards
                if self.swipe_angle <= -45:
                    # checks if swipe angle has reached 45 degrees
                    # in the other direction to change its direction again
                    self.swipe_direction = -1
            elif self.swipe_direction == -1:
                # checks if swipe angle has reached its limit
                # when swiping backwards to make it swipe infinitely
                # back and forth if mouse button is held
                self.sprite_angle -= 360 * delta_time
                self.swipe_angle += delta_time * 360
                if self.swipe_angle >= 45:
                    self.swipe_direction = 1
        if not pygame.mouse.get_pressed()[0]:
            # sets everything to default when mouse button is released
            self.swiping = False
            self.swipe_angle = 0
            self.swipe_direction = 0


