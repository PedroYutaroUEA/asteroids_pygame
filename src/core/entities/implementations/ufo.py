import random
import math
from src.core.entities.base import Entity, PhysVec

import src.config.server.balancing as BALANCE
import src.config.server as SERVER
import src.config.shared as SHARED


class UfoEntity(Entity):
    def __init__(self, pos: PhysVec, vel: PhysVec, is_small: bool):
        self.profle: SERVER.UfoProfileTypes = "SMALL" if is_small else "BIG"
        gp_profile = SERVER.UFO_PROFILES[self.profle]

        radius = SHARED.UFO_RADIUS[self.profle]

        super().__init__(pos, vel, rad=radius, angle=0)

        self.type = "UFO"
        self.is_small = is_small
        self.aim_accuracy = gp_profile["aim"]

        self.cool = SERVER.UFO_FIRE_EVERY

    def update(self, dt: float):
        if self.cool > 0:
            self.cool -= dt

    def try_fire_at(self, target_pos: PhysVec, dt: float):
        """Calcula a lógica de disparo, mas não spawna (retorna dados)"""
        if self.cool > 0:
            return None

        # Cálculo de direção
        dx = target_pos.x - self.pos.x
        dy = target_pos.y - self.pos.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist == 0:
            return None

        # Normaliza e aplica erro de mira (aim accuracy)
        aim_vec = (dx / dist, dy / dist)
        max_error = (1.0 - self.aim_accuracy) * 60.0
        error_angle = random.uniform(-max_error, max_error)

        # Rotaciona o vetor de mira
        rad = math.radians(error_angle)
        sn, cs = math.sin(rad), math.cos(rad)
        final_dir = (
            aim_vec[0] * cs - aim_vec[1] * sn,
            aim_vec[0] * sn + aim_vec[1] * cs,
        )

        self.cool = BALANCE.UFO_FIRE_EVERY

        # Retorna posição inicial e velocidade para o spawner
        bullet_pos = PhysVec(
            self.pos.x + final_dir[0] * (self.rad + 5),
            self.pos.y + final_dir[1] * (self.rad + 5),
        )
        bullet_vel = PhysVec(
            final_dir[0] * SERVER.UFO_BULLET_SPEED,
            final_dir[1] * SERVER.UFO_BULLET_SPEED,
        )

        return {"pos": bullet_pos, "vel": bullet_vel}

    def react_to_boundary(self, width: int, height: int):
        # UFO morre ao sair das bordas laterais (não faz wrap)
        if self.pos.x < -self.rad * 2 or self.pos.x > width + self.rad * 2:
            self.is_active = False
