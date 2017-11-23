import random
#import pygame

from Objects import *
from DynaSword import *


class Arrow(Object):
    life_time = 0
    start_life_time = 5
    start_flight_time = 1.5
    flight_time = 1.5
    tilt_angle = 0
    deflected = False

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
        self.life_time = self.start_life_time
        self.start_flight_time = (distance((x, y), (target_x, target_y)) + random.randrange(0, 3) * 0.1) / self.velocity.length()
        self.flight_time = self.start_flight_time
        self.parent_map = parent_map

        if math.sin(math.radians(self.sprite_angle)) < 0:
            #self.sprite_angle += 20
            self.tilt_angle = -20
        else:
            #self.sprite_angle -= 20
            self.tilt_angle = 20

    def update(self, delta_time, player, object_list, map):
        """Frame update function. Fly around all willy-nilly like an arrow. See Object for parameter details."""
        # If not flying, stay in position
        if self.flight_time <= 0:
            self.velocity = Vector(0, 0)

        if not self.deflected and self.flight_time > 0:
            # While airborne, tilt up and down slightly
            #self.sprite_angle += math.radians(self.tilt_angle * math.sin((self.flight_time / self.start_flight_time) * math.pi))
            self.velocity.point_at_angle(self.sprite_angle, self.velocity.length())

            # Collide with DynaSwords and deflect
            if not self.deflected:
                arrow_start = self.get_pos_at_pixel((6, 0))
                arrow_end = self.get_pos_at_pixel((6, 53))

                for obj in object_list:
                    if isinstance(obj, DynaSword):
                        if obj.attack_state is not DynaSword.BLOCKING:
                            continue

                        # Because the default hitbox would be too large, use line collision
                        # Try to collide the line through this arrow with the line through the DynaSword
                        sword_start = obj.get_pos_at_pixel((0, 0))
                        sword_end = obj.get_pos_at_pixel((0, obj.sprite.get_height()))

                        if Vector.intersection(sword_start, sword_end, arrow_start, arrow_end):
                            # Bounce off the sword with unknown math magic
                            sword_normal = Vector(sword_end.y - sword_start.y, -(sword_end.x - sword_start.x))
                            sword_normal.normalise()
                            self.velocity += sword_normal * -abs(Vector.dot(self.velocity, sword_normal)) * 2 + player.velocity

                            self.sprite_angle = math.degrees(direction((0, 0), tuple(self.velocity)))
                            self.deflected = True
                            self.flight_time = self.start_flight_time
        elif self.deflected and self.flight_time > 0:
            # Spin like mad
            pass
            #self.sprite_origin = Vector(self.sprite.get_width() / 2, self.sprite.get_height() / 2)
            #self.sprite_angle += random.randrange(3000, 4000) * delta_time

        # Move
        self.move(tuple(self.velocity * delta_time), object_list)

        # Update timers
        self.life_time -= delta_time
        self.flight_time -= delta_time

        if self.life_time <= 0:
            # Despawn - it lived too long and thus has to DIE
            object_list.remove(self)
            return