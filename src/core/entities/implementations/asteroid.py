import math
import random

import src.config.shared as SHARED
from src.core.entities.base.entity import Entity
from src.core.entities.base.vector import PhysVec


class AsteroidEntity(Entity):
    def __init__(self, pos: PhysVec, vel: PhysVec, size: str):
        # O raio é buscado na config shared baseada no tamanho (L, M, S)
        rad = SHARED.AST_SIZES[size]["r"]
        super().__init__(pos, vel, rad, angle=0)
        self.type = "ASTEROID"
        self.size = size
        self.vertices = self._generate_vertices()

    def update(self, dt: float):
        # Asteroides apenas mantém velocidade constante
        pass

    def _generate_vertices(self):
        steps = 12 if self.size == "L" else 10 if self.size == "M" else 8
        points = []
        for i in range(steps):
            ang = i * (math.tau / steps)
            jitter = random.uniform(0.75, 1.2)
            dist = self.rad * jitter
            points.append((math.cos(ang) * dist, math.sin(ang) * dist))
        return points

    def react_to_boundary(self, width: int, height: int):
        # Asteroides fazem wrap-around
        self.pos.x %= width
        self.pos.y %= height
