import math
import random
from typing import Literal
import src.config.server.physics as PHYS
import src.config.server.balancing as BALANCE
import src.config.shared as SHARED

from src.core.entities.base.entity import Entity
from src.core.entities.base.vector import PhysVec


class ShipEntity(Entity):
    def __init__(self, x, y):
        super().__init__(
            pos=PhysVec(x, y), vel=PhysVec(0, 0), angle=-90, rad=SHARED.SHIP_RADIUS
        )
        self.type = "SHIP"
        self.thrust_power = PHYS.SHIP_THRUST
        self.friction = PHYS.SHIP_FRICTION
        self.invuln_timer = 0.0
        self.fire_cool = 0.0

    def rotate(self, direction: Literal["L", "R"], dt: float):
        factor = 1 if direction == "R" else -1
        self.angle += factor * PHYS.SHIP_TURN_SPEED * dt

    def apply_thrust(self, dt: float):
        rad = math.radians(self.angle)
        self.vel.x += math.cos(rad) * self.thrust_power * dt
        self.vel.y += math.sin(rad) * self.thrust_power * dt

    def hyperspace(self):
        """Teletransporte aleatório (Mecânica clássica)"""
        self.pos = PhysVec(
            random.uniform(0, SHARED.WIDTH), random.uniform(0, SHARED.HEIGHT)
        )
        self.vel = PhysVec(0, 0)
        self.invuln_timer = 0.5  # Pequeno frame de segurança

    def get_fire_data(self):
        """Retorna dados para o Spawner criar a bala"""
        if self.fire_cool > 0:
            return None

        rad = math.radians(self.angle)
        dir_v = (math.cos(rad), math.sin(rad))

        # Posição na ponta da nave
        b_pos = PhysVec(
            self.pos.x + dir_v[0] * (self.rad + 5),
            self.pos.y + dir_v[1] * (self.rad + 5),
        )
        # Velocidade herdada + velocidade do projétil
        b_vel = PhysVec(
            self.vel.x + dir_v[0] * PHYS.SHIP_BULLET_SPEED,
            self.vel.y + dir_v[1] * PHYS.SHIP_BULLET_SPEED,
        )

        self.fire_cool = BALANCE.SHIP_FIRE_RATE
        return {"pos": b_pos, "vel": b_vel}

    def update(self, dt: float):
        self.vel.x *= self.friction
        self.vel.y *= self.friction

        if self.invuln_timer > 0:
            self.invuln_timer -= dt
        if self.fire_cool > 0:
            self.fire_cool -= dt

    def react_to_boundary(self, width, height):
        self.pos.x %= width
        self.pos.y %= height
