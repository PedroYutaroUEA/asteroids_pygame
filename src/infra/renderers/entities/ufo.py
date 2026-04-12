import pygame as pg
from src.core.entities.implementations.ufo import UfoEntity
import src.config.client.styles as COLORS
from .base import EntityRenderer


class UfoRenderer(EntityRenderer):
    @staticmethod
    def draw(surface: pg.Surface, entity: UfoEntity):
        # Corpo principal (Elipse)
        w, h = entity.rad * 2, entity.rad
        rect = pg.Rect(0, 0, w, h)
        rect.center = (entity.pos.x, entity.pos.y)
        pg.draw.ellipse(surface, COLORS.WHITE, rect, width=1)

        # Cúpula superior
        cup_w, cup_h = w * 0.5, h * 0.7
        cup_rect = pg.Rect(0, 0, cup_w, cup_h)
        cup_rect.center = (entity.pos.x, entity.pos.y - h * 0.3)
        pg.draw.ellipse(surface, COLORS.WHITE, cup_rect, width=1)
