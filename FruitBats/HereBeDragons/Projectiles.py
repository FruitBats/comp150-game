import pygame

from Objects import *
from DynaSword import *

class Arrow(Object):
    life_time = 1
    start_life_time = 5
    tilt_angle = 0
    deflected = False

    def __init__(self, (x, y), (x_velocity, y_velocity), angle):
        """Initialises an arrow projectile
            Arguments:
                (x, y) (float): Position to spawn arrow, in tiles
                (x_velocity, y_velocity) (float): Velocity of arrow on spawn, in tiles/sec
                angle (float): Initial angle of the arrow in degrees
        """
        self.x = float(x)
        self.y = float(y)
        self.collision = CollisionBox((0, 0), (13, 53), True)
        self.sprite = pygame.image.load("graphics/arrow.png")
        self.sprite_angle = angle
        self.sprite_origin = Vector(6, 0)
        self.velocity = Vector(x_velocity, y_velocity)
        self.life_time = self.start_life_time

        if math.sin(math.radians(angle)) < 0:
            self.tilt_angle = 30
        else:
            self.tilt_angle = -30

    def update(self, delta_time, player, object_list, map):
        self.move(tuple(self.velocity * delta_time), object_list)

        if not self.deflected:
            # Tilt up and down slightly while airborne
            #self.sprite_angle -= math.radians(self.tilt_angle * math.sin(self.life_time / self.start_life_time * math.pi * 1.5))
            self.velocity.point_at_angle(self.sprite_angle, self.velocity.length())
            self.life_time -= delta_time

            # Collide with DynaSwords
            if not self.deflected:
                arrow_start = self.get_pos_at_pixel((6, 0))
                arrow_end = self.get_pos_at_pixel((6, 53))
                for obj in object_list:
                    if isinstance(obj, DynaSword):
                        # Because the default hitbox would be too large, use an alternative collision method for this
                        # Try to collide the line through this arrow with the line through the DynaSword
                        sword_start = obj.get_pos_at_pixel((0, 0))
                        sword_end = obj.get_pos_at_pixel((0, obj.sprite.get_height()))

                        if Vector.intersection(sword_start, sword_end, arrow_start, arrow_end):
                            self.sprite_angle -= 180
                            self.velocity *= -1
                            normal_velocity = self.velocity
                            normal_sword = sword_end - sword_start
                            normal_velocity.normalise()
                            normal_sword.normalise()
                            self.velocity += normal_sword * abs(-Vector.dot(self.velocity, normal_sword)) * self.velocity.length()
                            self.deflected = True
                            self.collision.solid = False
        else:
            self.sprite_origin = Vector(self.sprite.get_width() / 2, self.sprite.get_height() / 2)
            self.sprite_angle = math.degrees(direction((0, 0), tuple(self.velocity)))
            #self.sprite_angle += 5000 * delta_time


        if self.life_time <= 0:
            object_list.remove(self)
            return