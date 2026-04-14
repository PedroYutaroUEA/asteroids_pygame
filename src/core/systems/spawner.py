import math
import random
from src.core.entities.base.vector import PhysVec
import src.config.shared as SHARED
import src.config.server as SERVER
from src.core.entities.implementations.asteroid import AsteroidEntity
from src.core.entities.implementations.bullet import BulletEntity
from src.core.entities.implementations.ufo import UfoEntity


class SpawnerSystem:
    def __init__(self, engine):
        self.engine = engine

    def spawn_asteroid(self, pos: PhysVec, vel: PhysVec, size: str):
        asteroid = AsteroidEntity(pos, vel, size)
        self.engine.entities.append(asteroid)

    def spawn_ufo(self):
        # Verifica se já existe um UFO ativo (lógica original)
        if any(e.type == "UFO" for e in self.engine.entities):
            return

        is_small = random.random() < 0.5
        y = random.uniform(0, SHARED.HEIGHT)
        x = 0 if random.random() < 0.5 else SHARED.WIDTH

        pos = PhysVec(x, y)
        vel = PhysVec(SERVER.UFO_SPEED if x == 0 else -SERVER.UFO_SPEED, 0)

        ufo = UfoEntity(pos, vel, is_small)
        self.engine.entities.append(ufo)

    def spawn_bullet(
        self,
        pos: PhysVec,
        vel: PhysVec,
        source_type: str,
        rad=2,
        ricochet=False,
        max_bounces=5,
    ):
        bullet = BulletEntity(
            pos=pos,
            vel=vel,
            rad=rad,
            can_ricochet=ricochet,
            max_bounces=max_bounces,
            source=source_type,
        )
        bullet.type = "BULLET" if source_type == "SHIP" else "UFO_BULLET"
        self.engine.entities.append(bullet)

    def generate_random_asteroid_wave(self, count: int, ship_pos: PhysVec):
        for _ in range(count):
            pos = self._rand_edge_pos()
            # Garante distância mínima da nave
            while self._dist(pos, ship_pos) < 150:
                pos = self._rand_edge_pos()

            ang = random.uniform(0, math.tau)
            speed = random.uniform(SERVER.AST_VEL_MIN, SERVER.AST_VEL_MAX)
            vel = PhysVec(math.cos(ang) * speed, math.sin(ang) * speed)
            self.spawn_asteroid(pos, vel, "L")

    def _rand_edge_pos(self) -> PhysVec:
        if random.random() < 0.5:
            x = random.uniform(0, SHARED.WIDTH)
            y = 0 if random.random() < 0.5 else SHARED.HEIGHT
        else:
            x = 0 if random.random() < 0.5 else SHARED.WIDTH
            y = random.uniform(0, SHARED.HEIGHT)
        return PhysVec(x, y)

    def _dist(self, p1: PhysVec, p2: PhysVec) -> float:
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
