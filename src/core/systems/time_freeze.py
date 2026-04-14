from typing import Literal

import src.config.server.gameplay as GAMEPLAY

TimeStopState = Literal["NORMAL", "PARTIAL", "TOTAL"]


class TimeSystem:
    """Time freeze controll"""

    def __init__(self):
        self.state: TimeStopState = "NORMAL"
        self.timer = 0.0

    def start_freeze(self):
        self.state = "TOTAL"
        self.timer = GAMEPLAY.SHIP_DATA["TIMESTOP"]["duration"]

    def update(self, dt) -> str | None:
        if self.state == "NORMAL":
            return None

        self.timer -= dt
        # Lógica Nave 4: Primeiros 2s = TOTAL, o restante = PARTIAL
        total_duration = GAMEPLAY.SHIP_DATA["TIMESTOP"]["duration"]
        elapsed = total_duration - self.timer

        if self.timer <= 0:
            self.state = "NORMAL"
            event = "TIMESTOP_END"
            return event

        if elapsed > 2.0:
            self.state = "PARTIAL"
        else:
            self.state = "TOTAL"
        return None

    def should_update(self, entity_type: str) -> bool:
        """ship movement ennibhitor"""
        if self.state == "NORMAL":
            return True
        if self.state == "TOTAL":
            return False
        if self.state == "PARTIAL":
            return entity_type == "SHIP"  # Só a nave move no tempo parado
        return True
