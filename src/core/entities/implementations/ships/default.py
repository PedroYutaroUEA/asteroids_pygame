import random

from src.core.entities.base.vector import PhysVec
from src.core.entities.implementations.ships.base import ShipEntity
import src.config.shared as SHARED
import src.config.server.gameplay as GAMEPLAY


class DefaultShip(ShipEntity):
    """Nave 6: Teletransporte (Hyperspace)."""

    def __init__(self, x, y):
        self.ship_class = "DEFAULT"
        self.p_cooldown = GAMEPLAY.SHIP_DATA[self.ship_class]["cooldown"]
        self.p_duration = GAMEPLAY.SHIP_DATA[self.ship_class]["duration"]
        super().__init__(x, y, self.p_cooldown)

    def activate_power(self):
        if super().activate_power():
            self.pos = PhysVec(
                random.uniform(0, SHARED.WIDTH), random.uniform(0, SHARED.HEIGHT)
            )
            self.vel = PhysVec(0, 0)
            self.invuln_timer = 0.5
            return True
        return False
