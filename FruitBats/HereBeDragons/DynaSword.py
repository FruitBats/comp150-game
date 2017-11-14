import pygame

from Objects import *
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
    origin_x = 0  # position of the sword's origin (usually the player's hand)
    origin_y = 0  # position of the sword's origin (usually the player's hand)

    owner = None # Object that is using the dynasword

    def __init__(self, x, y, owner):
        """Construct the object at position

         Args:
             x: x position to spawn object
             y: y position to spawn object
             owner (Object): Object that is using the sword.
        """
        self.sprite = pygame.image.load("graphics/sword.png")
        self.x = x
        self.y = y

        self.owner = owner

        self.handle_origin = Vector(self.sprite.get_width() / 3,
                                    self.sprite.get_height())
        self.centre_origin = Vector(self.sprite.get_width() / 2,
                                    self.sprite.get_height() / 2)
        self.collision = CollisionParams((0, 0),
                                        (self.sprite.get_width(), self.sprite.get_height()), False)
        self.debug_render_hitbox = True

    def update(self, delta_time, player, object_list, map):
        """Performs per-frame object update

        Args:
            delta_time: Number of seconds passed since last game frame
            player: Pointer to the player object
            object_list: Pointer to the list of game objects
            map: Pointer to the game map
        """

        # Set position
        hand_x = self.owner.x + float(14) / MAP.TILE_SIZE
        hand_y = self.owner.y + float(47) / MAP.TILE_SIZE
        self.origin_x = self.owner.x + float(self.owner.sprite.get_width()) / 2 \
                          / MAP.TILE_SIZE
        self.origin_y = self.owner.y + float(self.owner.sprite.get_height()) / 2 \
                          / MAP.TILE_SIZE
        self.x = self.origin_x - math.sin(math.radians(self.attack_angle)) \
                    * float(self.owner.sprite.get_width()) / MAP.TILE_SIZE * 0.6
        self.y = self.origin_y - math.cos(math.radians(self.attack_angle)) \
                    * float(self.owner.sprite.get_height()) / MAP.TILE_SIZE * 0.6

        # Do attack-specific positioning and angling
        if self.attack_state == DynaAttack.NONE:
            # Default sword position
            self.sprite_angle = 0
            self.sprite_origin = self.handle_origin
            self.x = hand_x
            self.y = hand_y
        elif self.attack_state == DynaAttack.SWIPING:
            # Do a 45-degree progessive swipe along attack_timer
            attack_radius = 75
            self.sprite_angle = self.attack_angle - attack_radius \
                                + (attack_radius * 2 * self.attack_timer
                                    / self.attack_timer_start)
            self.sprite_origin = self.handle_origin
        elif self.attack_state == DynaAttack.BLOCKING:
            # Do a 90-degree block
            self.attack_angle = math.degrees(direction(
                                (self.origin_x, self.origin_y),
                                (self.mouse_x, self.mouse_y)))
            self.sprite_angle = self.attack_angle - 90
            self.sprite_origin = self.centre_origin
        elif self.attack_state == DynaAttack.BOOMERANGING:
            # Fly through the air, meeting at self.attack_target when
            # self.attack_timer == self.attack_timer_start / 2
            self.sprite_angle += 360 * 5 * delta_time
            self.sprite_origin = self.centre_origin

            progress_factor = math.sin(math.radians(180) * self.attack_timer
                                       / self.attack_timer_start)
            self.x = self.origin_x + ((self.attack_target.x - self.origin_x) \
                                      * progress_factor)
            self.y = self.origin_y + ((self.attack_target.y - self.origin_y) \
                                      * progress_factor)

        # Decrement attack timer and stop if attack is over
        self.attack_timer -= delta_time
        if self.attack_timer < 0:
            self.attack_timer = 0
            self.attack_state = DynaAttack.NONE

        self.collision_tests(object_list)

    def render(self, screen, camera):
        """Renders the object

        Args:
            screen: Surface representing the game screen
            camera: Pointer to the game camera object
        """
        # Hack: self.mouse_x and mouse_y are set here because the Update
        # function doesn't provide the camera whilst the render function does..

        self.mouse_x = (camera.x
                        + float(pygame.mouse.get_pos()[0]) / MAP.TILE_SIZE)
        self.mouse_y = (camera.y
                        + float(pygame.mouse.get_pos()[1]) / MAP.TILE_SIZE)

        Object.render(self, screen, camera)

    def attack(self):
        """Performs swipe attack if not on cooldown"""
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.SWIPING
            self.attack_timer_start = 0.1
            self.attack_timer = 1 # 0.1
            self.attack_angle = math.degrees(direction(
                (self.origin_x, self.origin_y),
                (self.mouse_x, self.mouse_y)))

    def block(self):
        """Performs sideways block if not on cooldown"""
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.BLOCKING
            self.attack_timer_start = 0.25
            self.attack_timer = 0.25
            self.attack_angle = math.degrees(direction(
                (self.origin_x, self.origin_y),
                (self.mouse_x, self.mouse_y)))

    def boomerang(self):
        """Throws sword like a boomerang (if not on cooldown)"""
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.BOOMERANGING
            self.attack_target = Vector(self.mouse_x, self.mouse_y)
            self.attack_timer = 0.25 * distance((self.x, self.y),
                                                self.attack_target)
            self.attack_timer_start = self.attack_timer

    def collision_tests(self, objects):
        collision = False
        # Todo
        if collision:
            self.attack_state = DynaAttack.NONE