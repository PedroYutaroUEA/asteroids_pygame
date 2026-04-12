from dataclasses import dataclass


@dataclass
class HUDInfo:
    """Main info to show on HUD"""

    score: int
    lives: int
    wave: int
