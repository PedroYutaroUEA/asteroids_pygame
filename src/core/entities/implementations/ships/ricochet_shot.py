from src.core.entities.implementations.ships.base import ShipEntity
import src.config.server.gameplay as GAMEPLAY


class RicochetShip(ShipEntity):
    """Nave 5: Tiro de Ricochete."""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_class = "RICOCHET"

    def activate_power(self):
        if not self.power_active:
            self.power_active = True
            self.power_timer = GAMEPLAY.SHIP_DATA["RICOCHET"]["duration"]
            return True
        return False

    def get_fire_data(self):
        data = super().get_fire_data()
        if data and self.power_active:
            for b in data:
                b["can_ricochet"] = True
                b["rad"] = 4  # Bala um pouco maior
        return data
