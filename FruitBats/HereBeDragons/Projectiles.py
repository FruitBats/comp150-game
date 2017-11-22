import random
#import pygame

from Objects import *
from DynaSword import *

class Arrow(Object):
    life_time = 0
    start_life_time = 5
    flight_time = 1
    tilt_angle = 0
    deflected = False

    def __init__(self, (x, y), (x_velocity, y_velocity), angle):
        """Initialises an arrow projectile
            Arguments:
                (x, y) (float): Position to spawn arrow, in tiles
                (x_velocity, y_velocity) (float): Velocity of arrow on spawn, in tiles/sec
                angle (float): Initial angle of the arrow in degrees
        """
        # Initialise position and speed
        self.x = float(x)
        self.y = float(y)
        self.velocity = Vector(x_velocity, y_velocity)

        # Sprite
        self.sprite = pygame.image.load("graphics/arrow.png")
        self.sprite_angle = angle
        self.sprite_origin = Vector(6, 0)

        # Collision
        self.collision = CollisionBox((0, 0), (13, 53), True)

        # Arrow properties
        self.life_time = self.start_life_time

        if math.sin(math.radians(angle)) < 0:
            self.tilt_angle = 10
        else:
            self.tilt_angle = -10

    def update(self, delta_time, player, object_list, map):
        """Frame update function. Fly around all willy-nilly like an arrow. See Object for parameter details."""
        # If not flying, stay in position
        if self.flight_time <= 0:
            self.velocity.x = 0
            self.velocity.y = 0

        if not self.deflected and self.flight_time > 0:
            # Tilt up and down slightly while airborne
            self.sprite_angle -= math.radians(self.tilt_angle * math.sin(self.life_time / self.start_life_time * math.pi * 1.5))
            self.velocity.point_at_angle(self.sprite_angle, self.velocity.length())
            self.life_time -= delta_time

            # Collide with DynaSwords and deflect
            if not self.deflected:
                arrow_start = self.get_pos_at_pixel((6, 0))
                arrow_end = self.get_pos_at_pixel((6, 53))

                for obj in object_list:
                    if isinstance(obj, DynaSword):
                        # Because the default hitbox would be too large, use line collision
                        # Try to collide the line through this arrow with the line through the DynaSword
                        sword_start = obj.get_pos_at_pixel((0, 0))
                        sword_end = obj.get_pos_at_pixel((0, obj.sprite.get_height()))

                        if Vector.intersection(sword_start, sword_end, arrow_start, arrow_end):
                            # Bounce off the sword with unknown math magic
                            sword_normal = Vector(sword_end.y - sword_start.y, -(sword_end.x - sword_start.x))
                            self.velocity += sword_normal * -abs(Vector.dot(self.velocity, sword_normal)) * 2
                            self.deflected = True
                            self.collision.solid = False
        elif self.deflected and self.flight_time > 0:
            # Spin like mad
            self.sprite_origin = Vector(self.sprite.get_width() / 2, self.sprite.get_height() / 2)
            self.sprite_angle += random.randrange(3000, 4000) * delta_time

        # Move
        self.move(tuple(self.velocity * delta_time), object_list)

        # Update timers
        self.life_time -= delta_time
        self.flight_time -= delta_time

        if self.life_time <= 0:
            # Despawn - it lived too long and thus has to DIE
            object_list.remove(self)
            return