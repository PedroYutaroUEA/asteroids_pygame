import src.config.shared as SHARED
from src.core.entities.base import Entity, PhysVec


class AsteroidEntity(Entity):
    def __init__(self, pos: PhysVec, vel: PhysVec, size: str):
        # O raio é buscado na config shared baseada no tamanho (L, M, S)
        rad = SHARED.AST_SIZES[size]["r"]
        super().__init__(pos, vel, rad, angle=0)
        self.type = "ASTEROID"
        self.size = size

    def update(self, dt: float):
        # Asteroides apenas mantém velocidade constante
        pass

    def react_to_boundary(self, width: int, height: int):
        # Asteroides fazem wrap-around
        self.pos.x %= width
        self.pos.y %= height
