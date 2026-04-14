from typing import Literal


UfoProfileTypes = Literal["BIG", "SMALL"]

UFO_PROFILES: dict[UfoProfileTypes, dict] = {
    "BIG": {"score": 200, "aim": 0.2},
    "SMALL": {"score": 1000, "aim": 0.6},
}

AST_SCORES = {"L": 20, "M": 50, "S": 100}

# Mapeamento de Naves e Poderes
SHIP_DATA = {
    "INTANGIBLE": {
        "name": "Phase-Shift",
        "desc": "Fica intangivel por 5s",
        "duration": 5.0,
    },
    "TRIPLE": {
        "name": "Bomber-Spread",
        "desc": "Tiro triplo por 10s",
        "duration": 10.0,
    },
    "SHIELD": {
        "name": "Reflector",
        "desc": "Escudo que rebate por 10s",
        "duration": 10.0,
    },
    "TIMESTOP": {
        "name": "Chronos",
        "desc": "Para o tempo por 10s (2s imovel)",
        "duration": 10.0,
    },
    "RICOCHET": {
        "name": "Bouncer",
        "desc": "Tiro ricocheteia por 10s",
        "duration": 10.0,
    },
    "DEFAULT": {
        "name": "Teleporter",
        "desc": "Teletransporte instantaneo",
        "duration": 0.0,
    },
}
