from src.core.entities.implementations.ships.base import ShipEntity
import src.config.server.gameplay as GAMEPLAY


class ShieldShip(ShipEntity):
    """Nave 3: Shield Ship"""

    def __init__(self, x, y):
        self.ship_class = "SHIELD"
        self.p_cooldown = GAMEPLAY.SHIP_DATA[self.ship_class]["cooldown"]
        self.p_duration = GAMEPLAY.SHIP_DATA[self.ship_class]["duration"]
        super().__init__(x, y, self.p_cooldown)
        self.has_reflector = False

    def activate_power(self):
        if super().activate_power():
            self.power_timer = self.p_duration
            self.max_power_duration = self.p_duration
            self.has_reflector = True
            return True
        return False

    def deactivate_power(self):
        super().deactivate_power()
        self.has_reflector = False
