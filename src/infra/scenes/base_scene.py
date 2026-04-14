from abc import ABC, abstractmethod
import pygame as pg


class BaseScene(ABC):
    """Generic methods for base scene"""

    def __init__(self, manager, assets):
        self.manager = manager  # Referência para o SceneManager (troca de telas)
        self.assets = assets  # troca de assets

    @abstractmethod
    def handle_events(self, events: list[pg.event.Event]):
        """Processa eventos do Pygame (teclado, mouse)"""

    @abstractmethod
    def update(self, dt: float):
        """Atualiza a lógica da cena"""

    @abstractmethod
    def draw(self, screen: pg.Surface):
        """Renderiza os elementos na tela"""
