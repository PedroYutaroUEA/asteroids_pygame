from src.core.entities.implementations.ships.base import ShipEntity
import src.config.server.gameplay as GAMEPLAY


class ShieldShip(ShipEntity):
    """Nave 3: Shield Ship"""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_class = "SHIELD"
        self.has_reflector = False

    def activate_power(self):
        if not self.power_active:
            self.power_active = True
            self.power_timer = GAMEPLAY.SHIP_DATA["SHIELD"]["duration"]
            self.has_reflector = True
            return True
        return False

    def deactivate_power(self):
        super().deactivate_power()
        self.has_reflector = False
