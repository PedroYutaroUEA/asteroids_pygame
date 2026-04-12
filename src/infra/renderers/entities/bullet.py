import pygame as pg
from src.core.entities.base.entity import Entity
import src.config.client.styles as COLORS
from .base import EntityRenderer


class BulletRenderer(EntityRenderer):
    @staticmethod
    def draw(surface: pg.Surface, entity: Entity):
        # Desenha um círculo preenchido para balas do player e UFO
        color = COLORS.WHITE
        pg.draw.circle(
            surface, color, (int(entity.pos.x), int(entity.pos.y)), entity.rad
        )
