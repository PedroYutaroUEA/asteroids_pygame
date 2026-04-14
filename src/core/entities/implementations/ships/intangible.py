from src.core.entities.implementations.ships.base import ShipEntity
import src.config.server.gameplay as GAMEPLAY


class IntangibleShip(ShipEntity):
    """Nave 1: Fica intangível por 5 segundos."""

    def __init__(self, x, y):
        self.ship_class = "INTANGIBLE"
        self.p_cooldown = GAMEPLAY.SHIP_DATA[self.ship_class]["cooldown"]
        self.p_duration = GAMEPLAY.SHIP_DATA[self.ship_class]["duration"]
        super().__init__(x, y, self.p_cooldown)

    def activate_power(self):
        if super().activate_power():
            self.power_timer = self.p_duration
            self.max_power_duration = self.p_duration
            self.is_intangible = True
            return True
        return False

    def deactivate_power(self):
        super().deactivate_power()
        self.is_intangible = False
