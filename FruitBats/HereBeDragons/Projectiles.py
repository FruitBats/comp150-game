import random
#import pygame

import Enemy
from DynaSword import *


class Arrow(Object):
    """Arrow projectile
    Attributes:
        life_time (float): Current time until despawn, in seconds
        start_life_time (float): Initial time length before despawn, in seconds
        start_flight_time (float): Initial time expected to fly in the air (varies depending on initial distance and speed)
        flight_time (float): Current time until flight ends and arrow lands on the ground, in seconds
        tilt_angle (float): Angle toward which the arrow will tilt during flight, in degrees
        deflected (boolean): Whether the arrow has been deflected by the player or an enemy
        power (float): Amount of damage the arrow deals in a collision with a character
    """
    life_time = 0.0
    flight_time = 1.5
    start_life_time = 5
    start_flight_time = 1.5
    tilt_angle = 0
    deflected = False
    power = 10

    def __init__(self, (x, y), (target_x, target_y), speed, parent_map):
        """Initialises an arrow projectile
            Arguments:
                (x, y) (float): Position to spawn arrow, in tiles
                (target_x, target_y) (float): Rough position for the arrow to land (slightly randomised)
                speed (float): Arrow flight speed in tiles/sec
                parent_map (MapClass): Map that owns this object
        """
        # Initialise position and speed
        self.x = float(x)
        self.y = float(y)
        self.velocity = Vector((target_x - x), (target_y - y))
        self.velocity.normalise(speed)

        # Sprite
        self.sprite = pygame.image.load("graphics/arrow.png")
        self.sprite_angle = math.degrees(direction((x, y), (target_x, target_y)))
        self.sprite_origin = Vector(6, 0)

        # Collision
        self.collision = CollisionBox((0, 0), (13, 53), False)

        # Arrow properties
        self.parent_map = parent_map

        # Setup flight time and angle changes
        self.life_time = self.start_life_time
        self.start_flight_time = (distance((x, y), (target_x, target_y)) + 0 * 0.1) / self.velocity.length()

        if math.sin(math.radians(self.sprite_angle)) < 0:
            self.sprite_angle += 20
            self.tilt_angle = -20
        else:
            self.sprite_angle -= 20
            self.tilt_angle = 20

        self.start_flight_time *= 1.02  # Estimated factor for arc length (hacky, but it works)

        self.flight_time = self.start_flight_time

    def update(self, delta_time, player, object_list, map):
        """Frame update function. Fly around all willy-nilly like an arrow. Overrides Object.update"""
        # If not flying, stay in position
        if self.flight_time <= 0:
            self.velocity = Vector(0, 0)

        # Note collision line
        arrow_start = self.get_pos_at_pixel((6, 0))
        arrow_end = self.get_pos_at_pixel((6, 53))

        if not self.deflected and self.flight_time > 0:
            # While airborne, tilt up and down slightly
            self.sprite_angle += self.tilt_angle * 2 * delta_time / self.start_flight_time
            self.velocity.point_at_angle(self.sprite_angle, self.velocity.length())

            # Collide with DynaSwords and deflect
            for obj in object_list:
                if isinstance(obj, DynaSword):
                    if obj.attack_state is not DynaAttack.BLOCKING:
                        continue

                    # Because the default hitbox would be too large, use line collision
                    # Try to collide the line through this arrow with DynaSword
                    if obj.collision.line_intersection(arrow_start, arrow_end, obj.sprite_angle, (obj.sprite_origin.x, obj.sprite_origin.y), (obj.x, obj.y)):#Vector.intersection(sword_start, sword_end, arrow_start, arrow_end):
                        sword_start = obj.get_pos_at_pixel((0, 0))
                        sword_end = obj.get_pos_at_pixel((0, obj.sprite.get_height()))

                        # Bounce off the sword with unknown math magic
                        sword_normal = Vector(sword_end.y - sword_start.y, -(sword_end.x - sword_start.x))
                        sword_normal.normalise()
                        self.velocity += sword_normal * -abs(Vector.dot(self.velocity, sword_normal)) * 2 + player.velocity

                        self.sprite_angle = math.degrees(direction((0, 0), tuple(self.velocity)))
                        self.deflected = True
                        self.flight_time = self.start_flight_time

            # Collide with player
            player_origin = player.sprite_origin

            if player_origin is None:
                player_origin = Vector(0, 0)  # todo: sort out this dumb issue

            if player.collision.line_intersection(arrow_start, arrow_end, player.sprite_angle, tuple(player_origin), (player.x, player.y)):
                # Hurt the player
                player.hurt(self.power)
                object_list.remove(self)
                return

        elif self.deflected and self.flight_time > 0:
            for obj in object_list:
                if isinstance(obj, Enemy.Enemy):
                    origin = obj.sprite_origin

                    if origin is None:
                        origin = Vector(0, 0)

                    if obj.collision.line_intersection(arrow_start, arrow_end, obj.sprite_angle, (origin.x, origin.y), (obj.x, obj.y)):
                        # Hurt the enemy and land
                        self.flight_time = 0
                        obj.hurt(self.power)
                        break

        # Move
        self.move(tuple(self.velocity * delta_time), object_list)

        # Update timers
        self.life_time -= delta_time
        self.flight_time -= delta_time

        if self.life_time <= 0:
            # Despawn - it lived too long and thus has to DIE
            object_list.remove(self)
            return