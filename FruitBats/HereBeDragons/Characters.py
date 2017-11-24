
from Objects import Object


class Character(Object):
    health = 0  # (float) Current health
    max_health = 100  # (float) Maximum health
    hand_x = 0  # (float) X position, in pixels relative to sprite, of this character's wielding hand
    hand_y = 0  # (float) Y position, in pixels relative to sprite, of this character's wielding hand

    def __init__(self, health=max_health):
        self.health = health

    def hurt(self, damage):
        """Applies damage to this character and kills if it if dead bro
            Arguments:
                damage: (float) Amount of health to chop off
        """
        self.health -= damage

        if self.health <= 0:
            self.die()

    def get_hand_position(self):
        """Gets this character's absolute wielding hand position in tiles
            Returns: (Vector) Position, in tiles, of this character's hand"""
        return self.get_pos_at_pixel((self.hand_x, self.hand_y))

    def die(self):
        pass  # Character should "die" # TODO maybe make 'dead' a boolean attribute of character. In Game update loop, check all enemies dead status and remove from objects/destroy if true.
