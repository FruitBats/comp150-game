import math


class Vector():
    """Vector container class for xy coordinates
       Can also be used as a tuple."""
    x = 0.0
    y = 0.0

    def dot(self, other):
        """Returns the dot product of two Vectors as a float"""
        return float(self.x) * other.x + float(self.y) * other.y

    def normalise(self, value=1.0):
        """Scales the vector so that its length = value"""
        length = math.sqrt(self.x * self.x + self.y * self.y)

        if length > 0:
            self.x = self.x * value / length
            self.y = self.y * value / length
        else:
            self.x = 1  # how to error handling??
            self.y = 0

    def length(self):
        """Returns the length of the vector as a float"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def point_at_angle(self, angle, length):
        """Points the vector towards 'angle' with a specified length
            Arguments:
                angle (float): Angle of vector, in degrees
                length (float): Length of the vector
        """
        self.x = -math.sin(math.radians(angle)) * length
        self.y = -math.cos(math.radians(angle)) * length

    @staticmethod
    def to_angle(angle, length):
        """Returns a new vector pointing toward an angle
            Arguments:
                angle (float): Angle of the new vector, in degrees
                length (float): Length of the new vector
            Returns:
                (Vector) A vector pointing toward an angle with magnitude 'length'"""
        return Vector(-math.sin(math.radians(angle)) * length, -math.cos(math.radians(angle)) * length)

    @staticmethod
    def intersection(start1, end1, start2, end2):
        """Checks two lines between Vector points start1, end1 and start2, end2, and returns whether they intersect (boolean)"""
        opp = Vector(-(end2.y - start2.y), end2.x - start2.x)
        opp.normalise()

        dot_range = Vector.dot(start1 - start2, opp) - Vector.dot(end1 - start2, opp)

        if dot_range <= 0.0001:
            return False

        coll_cross_factor = (Vector.dot(start1 - start2, opp) / dot_range)
        other_check = Vector.dot(start1 + (end1 - start1) * coll_cross_factor - start2, end2 - start2)

        if coll_cross_factor >= 0 and coll_cross_factor < 1 and other_check >= 0 and other_check < Vector.dot(end2 - start2, end2 - start2):
            return True
        else:
            return False

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

    def __div__(self, divisor):
        """Divide vector components by a scalar"""
        return Vector(self.x / divisor, self.y / divisor)

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
    """Returns: (float) the distance between two points"""
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def direction((x1, y1), (x2, y2)):
    """Returns: (float) the direction between two points, in radians"""
    return math.radians(270) - math.atan2(y2 - y1, x2 - x1)