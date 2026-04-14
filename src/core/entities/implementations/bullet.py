from typing import Literal

from src.core.entities.base.entity import Entity
from src.core.entities.base.vector import PhysVec
import src.config.server.physics as PHYS

BulletSource = Literal["SHIP", "UFO"]


class BulletEntity(Entity):
    def __init__(
        self,
        pos: PhysVec,
        vel: PhysVec,
        source: BulletSource,
        rad=2,
        can_ricochet=False,
        max_bounces=5,
    ):
        # Raio fixo de projétil
        super().__init__(pos, vel, rad, angle=0)
        self.type = "BULLET"
        self.source = source
        self.ttl = PHYS.SHIP_BULLET_TTL if hasattr(PHYS, "SHIP_BULLET_TTL") else 1.0
        self.can_ricochet = can_ricochet
        self.bounces = 0
        self.max_bounces = max_bounces

    def update(self, dt: float):
        self.ttl -= dt
        if self.ttl <= 0:
            self.is_active = False

    def react_to_boundary(self, width: int, height: int):
        if (
            self.can_ricochet and self.bounces < self.max_bounces
        ):  # Limite para não ficar infinito
            if self.pos.x <= 0 or self.pos.x >= width:
                self.vel.x *= -1
                self.bounces += 1
            if self.pos.y <= 0 or self.pos.y >= height:
                self.vel.y *= -1
                self.bounces += 1
        else:
            # Comportamento padrão (Wrap)
            self.pos.x %= width
            self.pos.y %= height
