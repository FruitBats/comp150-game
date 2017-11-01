import pygame
import math

from Objects import Object
from Collision import CollisionParams
from Map import MapClass


class Swipe(Object):  # todo: load swipe animation
    original_sprite = None
    swiping = False
    swipe_progress = 0
    swipe_location = None
    swipe_direction = 1
    swipe_angle = 0

    def __init__(self, x, y):
        self.original_sprite = pygame.image.load("graphics/sword.png")
        self.sprite = self.original_sprite
        self.x = x
        self.y = y
        self.collision = CollisionParams((0, 0), (32, 32), False)

    def update(self, delta_time, player, object_list, map):
        mouse_x = float(pygame.mouse.get_pos()[0]) / MapClass.TILE_SIZE
        mouse_y = float(pygame.mouse.get_pos()[1]) / MapClass.TILE_SIZE
        angle_to_mouse = float(math.atan2((self.y - mouse_y),
                                          (mouse_x - self.x)))
        if not self.swiping:
            self.sprite_angle = float(math.degrees(angle_to_mouse) - 90)
        if pygame.mouse.get_pressed()[0]:
            self.swiping = True
            if self.swiping:
                self.sprite_angle -= 360 * delta_time
                self.swipe_angle += delta_time * 360
                if self.swipe_angle >= 45:
                    self.sprite_angle += 360 * delta_time
                    self.swipe_angle -= delta_time * 360
                if self.swipe_angle <= -45:
                    self.sprite_angle -= 360 * delta_time
                    self.swipe_angle += delta_time * 360
                # print self.swipe_angle
        if not pygame.mouse.get_pressed()[0]:
            self.swiping = False
            self.swipe_angle = 0


