import math
from dataclasses import dataclass


@dataclass
class PhysVec:
    """Physic Vector abstraction"""

    x: float
    y: float

    def __add__(self, other):
        return PhysVec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return PhysVec(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return PhysVec(self.x * scalar, self.y * scalar)

    def length(self):
        """get vector len"""
        return math.sqrt(self.x**2 + self.y**2)
