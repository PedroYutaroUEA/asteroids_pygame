import pygame as pg
import src.config.client.styles as COLORS
from src.core.entities.implementations.asteroid import AsteroidEntity
from .base import EntityRenderer


class AsteroidRenderer(EntityRenderer):
    """Asteroid Renderer"""

    @staticmethod
    def draw(surface: pg.Surface, entity: AsteroidEntity):
        # Transpõe os vértices relativos da entidade para a posição absoluta na tela
        points = [(entity.pos.x + v[0], entity.pos.y + v[1]) for v in entity.vertices]
        pg.draw.polygon(surface, COLORS.WHITE, points, width=1)
