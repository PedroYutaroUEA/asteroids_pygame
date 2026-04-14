from src.core.entities.implementations.ships.base import ShipEntity
import src.config.server.gameplay as GAMEPLAY


class IntangibleShip(ShipEntity):
    """Nave 1: Fica intangível por 5 segundos."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "INTANGIBLE"

    def activate_power(self):
        if not self.power_active:
            self.power_active = True
            self.power_timer = GAMEPLAY.SHIP_DATA["INTANGIBLE"]["duration"]
            self.is_intangible = True
            return True
        return False

    def deactivate_power(self):
        super().deactivate_power()
        self.is_intangible = False
