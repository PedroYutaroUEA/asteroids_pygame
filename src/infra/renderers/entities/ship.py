import math
import pygame as pg
from src.core.entities.implementations.ships.base import ShipEntity
from src.infra.renderers.entities.base import EntityRenderer
import src.config.client.styles as STYLES


class ShipRenderer(EntityRenderer):
    """PG implementation"""

    @staticmethod
    def draw(surface: pg.Surface, entity: "ShipEntity"):
        # 1. Pega a cor temática baseada na classe da nave
        base_color = STYLES.SHIP_COLORS.get(entity.ship_class, STYLES.WHITE)

        # 2. Efeito Visual: Intangibilidade (Piscar)
        if hasattr(entity, "is_intangible") and entity.is_intangible:
            if (pg.time.get_ticks() // 100) % 2 == 0:
                base_color = (50, 50, 50)  # "Sombra" da nave

        # 1. Calcular vértices do polígono baseado na entidade lógica e desenha
        points = ShipRenderer.__calc_vertices(entity)
        pg.draw.polygon(surface, base_color, points, width=1)

        # 6. Invulnerabilidade de Spawn (Blink padrão)
        if entity.invuln_timer > 0 and (pg.time.get_ticks() // 100) % 2 == 0:
            ShipRenderer.__draw_invuln(surface, entity)

        # 4. Feedback Visual: Escudo (Nave 3)
        if hasattr(entity, "has_reflector") and entity.has_reflector:
            ShipRenderer.__draw_reflector(surface, entity)

        # 5. Feedback Visual: Time Stop (Aura dourada se o tempo estiver parado)
        if entity.power_active and entity.ship_class == "TIMESTOP":
            ShipRenderer.__draw_timestop(surface, entity)

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
            STYLES.WHITE,
            (int(entity.pos.x), int(entity.pos.y)),
            entity.rad + 2,
            width=1,
        )

    @staticmethod
    def __draw_reflector(surface: pg.Surface, entity: "ShipEntity"):
        """Círculo pulsante ao redor"""
        pulse = math.sin(pg.time.get_ticks() * 0.01) * 3
        pg.draw.circle(
            surface,
            STYLES.SHIP_COLORS["SHIELD"],
            (int(entity.pos.x), int(entity.pos.y)),
            int(entity.rad + 10 + pulse),
            width=1,
        )

    @staticmethod
    def __draw_timestop(surface: pg.Surface, entity: "ShipEntity"):
        pg.draw.circle(
            surface,
            STYLES.SHIP_COLORS["TIMESTOP"],
            (int(entity.pos.x), int(entity.pos.y)),
            entity.rad + 5,
            width=1,
        )
