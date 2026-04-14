import random

from src.core.entities.base.vector import PhysVec
from src.core.entities.implementations.ships.base import ShipEntity
import src.config.shared as SHARED


class DefaultShip(ShipEntity):
    """Nave 6: Teletransporte (Hyperspace)."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "DEFAULT"

    def activate_power(self):
        # Teletransporte é instantâneo, não tem duração
        self.pos = PhysVec(
            random.uniform(0, SHARED.WIDTH), random.uniform(0, SHARED.HEIGHT)
        )
        self.vel = PhysVec(0, 0)
        self.invuln_timer = 0.5
        return True
