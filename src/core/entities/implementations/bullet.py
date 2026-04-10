from src.core.entities.base import Entity, PhysVec
import src.config.server.physics as PHYS


class BulletEntity(Entity):
    def __init__(self, pos: PhysVec, vel: PhysVec):
        # Raio fixo de projétil
        super().__init__(pos, vel, rad=2, angle=0)
        self.type = "BULLET"  # Pode ser alterado para UfoBullet pelo Spawner
        self.ttl = PHYS.SHIP_BULLET_TTL if hasattr(PHYS, "SHIP_BULLET_TTL") else 1.0

    def update(self, dt: float):
        self.ttl -= dt
        if self.ttl <= 0:
            self.is_active = False

    def react_to_boundary(self, width: int, height: int):
        # Balas fazem wrap-around conforme o original
        self.pos.x %= width
        self.pos.y %= height
