import math
import pygame as pg
from src.core.entities.implementations.ship import ShipEntity
from src.infra.renderers.entities.base import EntityRenderer
import src.config.client as COLOR


class ShipRenderer(EntityRenderer):
    """PG implementation"""

    @staticmethod
    def draw(surface: pg.Surface, entity: "ShipEntity"):
        # 1. Calcular vértices do polígono baseado na entidade lógica
        points = ShipRenderer.__calc_vertices(entity)
        # 2. Desenhar a nave
        pg.draw.polygon(surface, COLOR.WHITE, points, width=1)

        # 3. Desenhar feedback visual de invulnerabilidade (se houver)
        if entity.invuln_timer > 0:
            ShipRenderer.__draw_invuln(surface, entity)

    @staticmethod
    def __calc_vertices(entity: "ShipEntity") -> list[tuple]:
        rad = math.radians(entity.angle)
        rad_l = math.radians(entity.angle + 140)
        rad_r = math.radians(entity.angle - 140)

        points = [
            (
                entity.pos.x + math.cos(rad) * entity.rad,
                entity.pos.y + math.sin(rad) * entity.rad,
            ),
            (
                entity.pos.x + math.cos(rad_l) * entity.rad * 0.9,
                entity.pos.y + math.sin(rad_l) * entity.rad * 0.9,
            ),
            (
                entity.pos.x + math.cos(rad_r) * entity.rad * 0.9,
                entity.pos.y + math.sin(rad_r) * entity.rad * 0.9,
            ),
        ]

        return points

    @staticmethod
    def __draw_invuln(surface: pg.Surface, entity: "ShipEntity"):
        pg.draw.circle(
            surface,
            COLOR.GRAY,
            (int(entity.pos.x), int(entity.pos.y)),
            entity.rad + 5,
            width=1,
        )
