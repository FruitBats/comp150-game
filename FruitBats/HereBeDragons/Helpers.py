import math


class Vector:
    """Vector container class for xy coordinates
       Can also be used as a tuple."""
    x = 0.0
    y = 0.0

    def normalise(self, value=1.0):
        """Scales the vector so that its length = value"""
        length = math.sqrt(self.x * self.x + self.y * self.y)
        if length > 0:
            return Vector(self.x * value / length, self.y * value / length)
        else:
            return Vector(0, 0)  # prevent division by zero

    def length(self):
        """Returns the length of the vector as a float"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, vec):
        """Adds two vectors"""
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        """Subtracts a vector from another"""
        return Vector(self.x - vec.x, self.y - vec.y)

    def __mul__(self, multiplier):
        """Multiply vector components by a scalar"""
        return Vector(self.x * multiplier, self.y * multiplier)

    def __iter__(self):
        """Iterator allows vectors to be used as tuples"""
        yield self.x
        yield self.y

    def __str__(self):
        """str allows vectors to be printed"""
        return "(" + str(self.x) + ", " + str(self.y) + ")"


# Global functions for simple math tasks
# Functions accepting tuples can also accept vectors
def distance((x1, y1), (x2, y2)):
    """Returns the distance between two points"""
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def direction((x1, y1), (x2, y2)):
    """Returns the direction between two points, in radians"""
    return math.atan2(y2 - y1, x2 - x1)