from abc import ABC, abstractmethod

from .vector import PhysVec


class Entity(ABC):
    """Entity abs"""

    def __init__(self, pos: PhysVec, vel: PhysVec, rad: int, angle: float):
        self.pos = pos
        self.vel = vel
        self.rad = rad
        self.angle = angle
        self.is_active = True
        self.type = "Base"  # Definido pelas subclasses

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def react_to_boundary(self, width: int, height: int):
        pass

    def move(self, dt: float):
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt

    def check_collision(self, other: "Entity") -> bool:
        distance_sq = (self.pos.x - other.pos.x) ** 2 + (self.pos.y - other.pos.y) ** 2
        return distance_sq < (self.rad + other.rad) ** 2
