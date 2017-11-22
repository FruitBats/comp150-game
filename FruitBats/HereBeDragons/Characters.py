
from Objects import Object


class Character(Object):
    hitpoints = 0 # Character's hp
    etc = 0  # Todo

    def die(self):
        pass  # Character should "die" # TODO maybe make 'dead' a boolean attribute of character. In Game update loop, check all enemies dead status and remove from objects/destroy if true.
