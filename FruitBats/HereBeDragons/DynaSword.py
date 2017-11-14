import pygame

from Objects import Object
from Helpers import *
from Map import MAP


class DynaAttack:
    NONE = 0
    SWIPING = 1
    BLOCKING = 2
    BOOMERANGING = 3


class DynaSword(Object):
    handle_origin = None  # sprite origin = sword handle
    centre_origin = None  # sprite origin = center of image
    attack_state = DynaAttack.NONE  # current DynaAttack state
    attack_timer = 0  # time til current attack ends, in seconds
    attack_timer_start = 0
    attack_angle = 0  # central angle of attack in degrees
    attack_target = None  # Vector position of boomerang target
    mouse_x = 0  # mouse position relative to world
    mouse_y = 0  # mouse position relative to world

    def __init__(self, x, y):
        self.sprite = pygame.image.load("graphics/sword.png")
        self.x = x
        self.y = y
        self.handle_origin = Vector(self.sprite.get_width() / 3,
                                    self.sprite.get_height())
        self.centre_origin = Vector(self.sprite.get_width() / 2,
                                    self.sprite.get_height() / 2)

    def update(self, delta_time, player, object_list, map):
        # Set position
        hand_x = player.x + float(14) / MAP.TILE_SIZE
        hand_y = player.y + float(47) / MAP.TILE_SIZE
        origin_x = player.x + float(player.sprite.get_width()) / 2 / MAP.TILE_SIZE
        origin_y = player.y + float(player.sprite.get_height()) / 2 / MAP.TILE_SIZE
        self.x = origin_x - math.sin(math.radians(self.attack_angle)) * float(player.sprite.get_width()) / MAP.TILE_SIZE * 0.6
        self.y = origin_y - math.cos(math.radians(self.attack_angle)) * float(player.sprite.get_height()) / MAP.TILE_SIZE * 0.6

        # Do attack-specific positioning and angling
        if self.attack_state == DynaAttack.NONE:
            # Default sword position
            self.sprite_angle = 0
            self.sprite_origin = self.handle_origin
            self.x = hand_x
            self.y = hand_y
        elif self.attack_state == DynaAttack.SWIPING:
            # Do a 45-degree progessive swipe along attack_timer
            attack_radius = 45
            self.sprite_angle = self.attack_angle - attack_radius \
                                + (attack_radius * 2 * self.attack_timer
                                    / self.attack_timer_start)
            self.sprite_origin = self.handle_origin
        elif self.attack_state == DynaAttack.BLOCKING:
            # Do a 90-degree block
            self.attack_angle = math.degrees(direction((self.x, self.y),
                                          (self.mouse_x, self.mouse_y)))
            self.sprite_angle = self.attack_angle - 90
            self.sprite_origin = self.centre_origin
        elif self.attack_state == DynaAttack.BOOMERANGING:
            # Fly through the air, meeting at self.attack_target when
            # self.attack_timer == self.attack_timer_start / 2
            self.sprite_angle += 360 * 5 * delta_time
            self.sprite_origin = self.centre_origin

            progress_factor = math.sin(math.radians(180) * self.attack_timer / self.attack_timer_start)
            self.x = origin_x + ((self.attack_target.x - origin_x) * progress_factor)
            self.y = origin_y + ((self.attack_target.y - origin_y) * progress_factor)

        # Decrement attack timer and stop if attack is over
        self.attack_timer -= delta_time
        if self.attack_timer < 0:
            self.attack_timer = 0
            self.attack_state = DynaAttack.NONE

    def render(self, screen, camera):
        self.mouse_x = (camera.x
                        + float(pygame.mouse.get_pos()[0]) / MAP.TILE_SIZE)
        self.mouse_y = (camera.y
                        + float(pygame.mouse.get_pos()[1]) / MAP.TILE_SIZE)
        Object.render(self, screen, camera)

    def attack(self):
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.SWIPING
            self.attack_timer_start = 0.1
            self.attack_timer = 1 # 0.1
            self.attack_angle = math.degrees(direction(
                (self.x, self.y),
                (self.mouse_x, self.mouse_y)))

    def block(self):
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.BLOCKING
            self.attack_timer_start = 0.25
            self.attack_timer = 0.25
            self.attack_angle = math.degrees(direction(
                (self.x, self.y),
                (self.mouse_x, self.mouse_y)))

    def boomerang(self):
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.BOOMERANGING
            self.attack_target = Vector(self.mouse_x, self.mouse_y)
            self.attack_timer = 0.25 * distance((self.x, self.y),
                                                self.attack_target)
            self.attack_timer_start = self.attack_timer
