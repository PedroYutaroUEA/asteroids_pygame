from abc import ABC, abstractmethod
import pygame as pg
from src.core.entities.base import Entity


class EntityRenderer(ABC):
    """
    Entity Rendering Abstraction
    """

    @staticmethod
    @abstractmethod
    def draw(surface: pg.Surface, entity: "Entity"):
        """Renders whathever is necessary"""
