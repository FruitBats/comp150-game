import pygame

from Objects import *
from Helpers import *
from Map import MAP
from Characters import Character


class DynaAttack:
    NONE = 0
    SWIPING = 1
    BLOCKING = 2
    BOOMERANGING = 3
    COOLDOWN = 4


class DynaSword(Object):
    """DynaSword: The dynamic sword!

    Attributes:
        handle_origin (Vector): Origin of the handle on the sword sprite, in pixels
        centre_origin (Vector): Origin of the center of the sword sprite, in pixels
        attack_state (DynaAttack constant): Current state of attack
        current_attack_start_time (float): Initial value of attack timer during attack, in seconds
        current_attack_timer (float): Current state of the attack timer, i.e. progress of attack, in seconds
        current_attack_angle (float): Current angle of attack (LOOK AT thiS)
        current_attack_target (Vector): Position of the boomerang target, in tiles
        current_attack_cooldown (float): Current time til attack finishes cooldown, in seconds
        world_origin (Vector): Base position of the sword in the world disregarding its current movement/attacks, in tiles
        mouse (float): Absolute position of the mouse in the world, in tile units
    """
    handle_origin = None
    centre_origin = None
    attack_state = DynaAttack.NONE
    current_attack_start_time = 0
    current_attack_timer = 0
    current_attack_angle = 0
    current_attack_target = None
    current_attack_cooldown = 0
    world_origin = None
    world_mouse = None

    swipe_time = 0.1  # time, in seconds, a swipe will take
    swipe_range = 75  # range of swipe attack in degrees
    swipe_cooldown = 0.33  # cooldown time after a swipe

    boomerang_spin_speed = 1800  # speed of boomerang rotation in degrees/sec
    boomerang_time = 1  # time a boomerang will last in the air, in sec
    boomerang_cooldown = 0.6  # cooldown time after a boomerang

    block_time = 0.15  # time a block will last
    block_cooldown = 0.4  # cooldown time after a block

    owner = None  # Object that is using the dynasword

    def __init__(self, x, y, owner):
        """Construct the object at position

         Args:
             x: x position to spawn object
             y: y position to spawn object
             owner (Object): Object that is using the sword.
        """
        self.sprite = pygame.image.load("graphics/sword.png")
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * MAP.RATIO), int(self.sprite.get_height() * MAP.RATIO)))

        self.x = x
        self.y = y

        self.owner = owner

        self.handle_origin = Vector(self.sprite.get_width() / 3, self.sprite.get_height())
        self.centre_origin = Vector(self.sprite.get_width() / 2, self.sprite.get_height() / 2)

        self.world_origin = Vector(0, 0)
        self.world_mouse = Vector(0, 0)

        self.collision = CollisionBox((0, 0), (self.sprite.get_width(), self.sprite.get_height()), False)

    def update(self, delta_time, player, object_list, map):
        """Performs per-frame object update

        Args:
            delta_time: Number of seconds passed since last game frame
            player: Pointer to the player object
            object_list: Pointer to the list of game objects
            map: Pointer to the game map
        """

        # Set position
        hand = Vector(self.owner.x, self.owner.y)
        if isinstance(self.owner, Character):
            hand = self.owner.get_hand_position()

        self.world_origin = Vector(self.owner.x, self.owner.y)
        self.x = self.world_origin.x - math.sin(math.radians(self.current_attack_angle)) * float(self.owner.sprite.get_width()) / MAP.TILE_SIZE * 0.6
        self.y = self.world_origin.y - math.cos(math.radians(self.current_attack_angle)) * float(self.owner.sprite.get_height()) / MAP.TILE_SIZE * 0.6

        # Do attack-specific positioning and angling
        if self.attack_state == DynaAttack.NONE or self.attack_state == DynaAttack.COOLDOWN:
            # Default sword position
            self.sprite_angle = 0
            self.sprite_origin = self.handle_origin
            self.x = hand.x
            self.y = hand.y

            if self.attack_state == DynaAttack.COOLDOWN:
                # Decrement cooldown timer
                self.current_attack_cooldown -= delta_time

                if self.current_attack_cooldown < 0:
                    self.current_attack_cooldown = 0
                    self.attack_state = DynaAttack.NONE
        elif self.attack_state == DynaAttack.SWIPING:
            # Do a progressive swipe along attack_timer
            self.sprite_angle = self.current_attack_angle - self.swipe_range + (self.swipe_range * 2 * self.current_attack_timer / self.swipe_time)
            self.sprite_origin = self.handle_origin
        elif self.attack_state == DynaAttack.BLOCKING:
            # Do a 90-degree block
            self.current_attack_angle = math.degrees(direction(tuple(self.world_origin), tuple(self.world_mouse)))
            self.sprite_angle = self.current_attack_angle - 90
            self.sprite_origin = self.centre_origin
        elif self.attack_state == DynaAttack.BOOMERANGING:
            # Fly through the air, meeting at self.attack_target when
            # self.attack_timer == self.attack_timer_start / 2
            self.sprite_angle += self.boomerang_spin_speed * delta_time
            self.sprite_origin = self.centre_origin

            progress_factor = math.sin(math.radians(180) * self.current_attack_timer / self.current_attack_start_time)
            self.x = self.world_origin.x + ((self.current_attack_target.x - self.world_origin.x) * progress_factor)
            self.y = self.world_origin.y + ((self.current_attack_target.y - self.world_origin.y) * progress_factor)

        # Decrement attack timer and stop if attack is over
        self.current_attack_timer -= delta_time
        if self.current_attack_timer < 0:
            if self.attack_state is not DynaAttack.NONE:
                # Start cooldown timer
                if self.attack_state == DynaAttack.SWIPING:
                    self.current_attack_cooldown = self.swipe_cooldown
                elif self.attack_state == DynaAttack.BLOCKING:
                    self.current_attack_cooldown = self.block_cooldown
                elif self.attack_state == DynaAttack.BOOMERANGING:
                    self.current_attack_cooldown = self.boomerang_cooldown

                # Reset state
                self.attack_state = DynaAttack.COOLDOWN

            # Cap timer to 0
            self.current_attack_timer = 0

        # Check collisions between the centre line of this sword and characters
        centre_line_start = self.get_pos_at_pixel((self.sprite.get_width() / 2, self.sprite.get_height()))
        centre_line_end = self.get_pos_at_pixel((self.sprite.get_width() / 2, 0))

        for obj in object_list:
            if isinstance(obj, Character):
                origin = obj.sprite_origin

                if obj.sprite_origin is None:
                    origin = Vector(0, 0)

                if obj.collision.line_intersection(centre_line_start, centre_line_end, obj.sprite_angle, tuple(origin), (obj.x, obj.y)):
                    if obj is not self.owner:
                        # Hurt this character by 10hp for now
                        obj.hurt(10)

    def render(self, screen, camera):
        """Renders the object

        Args:
            screen: Surface representing the game screen
            camera: Pointer to the game camera object
        """
        self.world_mouse = camera.get_world_mouse_position()

        Object.render(self, screen, camera)

    def attack(self):
        """Performs swipe attack if not on cooldown"""
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.SWIPING
            self.current_attack_timer = self.swipe_time
            self.current_attack_angle = math.degrees(direction(tuple(self.world_origin), tuple(self.world_mouse)))

    def block(self):
        """Performs sideways block if not on cooldown"""
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.BLOCKING
            self.current_attack_timer = self.block_time
            self.current_attack_angle = math.degrees(direction(tuple(self.world_origin), tuple(self.world_mouse)))

    def boomerang(self):
        """Throws sword like a boomerang (if not on cooldown)"""
        if self.attack_state == DynaAttack.NONE:
            self.attack_state = DynaAttack.BOOMERANGING
            self.current_attack_target = Vector(self.world_mouse.x, self.world_mouse.y)
            self.current_attack_start_time = 0.25 * distance((self.x, self.y), self.current_attack_target)
            self.current_attack_timer = self.current_attack_start_time