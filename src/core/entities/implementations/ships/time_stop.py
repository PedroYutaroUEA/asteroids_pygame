from src.core.entities.implementations.ships.base import ShipEntity
import src.config.server.gameplay as GAMEPLAY


class TimeStopShip(ShipEntity):
    """Nave 4: Chronos (Time Stop)."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_class = "TIMESTOP"

    def activate_power(self):
        if not self.power_active:
            self.power_active = True
            self.power_timer = GAMEPLAY.SHIP_DATA["TIMESTOP"]["duration"]
            return True
        return False
