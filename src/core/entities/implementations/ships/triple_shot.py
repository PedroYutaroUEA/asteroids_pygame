import math
from src.core.entities.base.vector import PhysVec
from src.core.entities.implementations.ships.base import ShipEntity
import src.config.server.gameplay as GAMEPLAY
import src.config.server.physics as PHYS


class TripleShotShip(ShipEntity):
    """Nave 2: Tiro Triplo."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_class = "TRIPLE"

    def activate_power(self) -> bool:
        if super().activate_power():
            self.power_timer = GAMEPLAY.SHIP_DATA["TRIPLE"]["duration"]
            return True
        return False

    def _get_dir(self, angle):
        rad = math.radians(angle)
        return PhysVec(math.cos(rad), math.sin(rad))

    def get_fire_data(self) -> list[dict]:
        if self.fire_cool > 0:
            return None

        angles = (
            [self.angle - 15, self.angle, self.angle + 15]
            if self.power_active
            else [self.angle]
        )
        self.fire_cool = 0.1 if self.power_active else PHYS.SHIP_FIRE_RATE

        return [
            {
                "pos": self.pos + self._get_dir(a) * (self.rad + 5),
                "vel": self._get_dir(a) * PHYS.SHIP_BULLET_SPEED,
            }
            for a in angles
        ]
