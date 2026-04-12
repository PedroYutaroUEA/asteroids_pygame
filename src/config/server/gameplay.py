from typing import Literal


UfoProfileTypes = Literal["BIG", "SMALL"]

UFO_PROFILES: dict[UfoProfileTypes, dict] = {
    "BIG": {"score": 200, "aim": 0.2},
    "SMALL": {"score": 1000, "aim": 0.6},
}

AST_SCORES = {"L": 20, "M": 50, "S": 100}
