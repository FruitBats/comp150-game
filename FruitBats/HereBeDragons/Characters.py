
from Objects import Object


class Character(Object):
    """Character: Base class for the player and enemies. Extends Object
        Attributes:
            max_health (float): Maximum health for this character
            health (float): Character's current health
            hand_x, hand_y (int): Coordinates of the character's DynaSword-wielding hand, in pixels relative to their sprite
    """
    max_health = 100
    health = max_health
    hand_x = 0
    hand_y = 0

    def hurt(self, damage):
        """Applies damage to this character, and kills it if it dead, bro

            Args:
                damage: (float) Amount of health to chop off
        """
        self.health -= damage

        if self.health <= 0:
            self.die()

    def get_hand_position(self):
        """Gets this character's absolute wielding hand position in tiles

            Returns:
                (Vector) Position, in tiles, of this character's hand
        """
        return self.get_pos_at_pixel((self.hand_x, self.hand_y))

    def die(self):
        """Called upon death. Begins class-specific death action."""
        pass  # Character should "die"
