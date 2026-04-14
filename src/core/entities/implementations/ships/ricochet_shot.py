from src.core.entities.implementations.ships.base import ShipEntity
import src.config.server.gameplay as GAMEPLAY


class RicochetShip(ShipEntity):
    """Nave 5: Tiro de Ricochete."""

    def __init__(self, x, y):
        self.ship_class = "RICOCHET"
        self.p_cooldown = GAMEPLAY.SHIP_DATA[self.ship_class]["cooldown"]
        self.p_duration = GAMEPLAY.SHIP_DATA[self.ship_class]["duration"]
        super().__init__(x, y, self.p_cooldown)

    def activate_power(self):
        if super().activate_power():
            self.power_timer = self.p_duration
            self.max_power_duration = self.p_duration
            return True
        return False

    def get_fire_data(self):
        data = super().get_fire_data()
        if data and self.power_active:
            for b in data:
                b["can_ricochet"] = True
                b["rad"] = 4  # Bala um pouco maior
        return data
