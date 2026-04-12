import pygame as pg

from src.infra.renderers.ui.components.text import TextComponent
from src.infra.managers.input_manager import InputManager
import src.config.client.styles as COLORS
import src.config.shared.dimensions as SCREEN
from .base_scene import BaseScene


class MenuScene(BaseScene):
    """Focada em exibir o título e aguardar o comando de início."""

    def __init__(self, manager, assets, **kwargs):
        super().__init__(manager, assets)
        self.input_manager = InputManager()
        self.font_big = self.assets.get_font("big")
        self.font_main = self.assets.get_font("main")

    def handle_events(self, events: list[pg.event.Event]):
        self.input_manager.update(events)
        # Se qualquer tecla de confirmação for pressionada, inicia o jogo
        if self.input_manager.impulses["CONFIRM"]:
            self.manager.switch_to("play")
        if self.input_manager.impulses["EXIT"]:
            self.manager.quit()

    def update(self, dt: float):
        pass

    def draw(self, screen: pg.Surface):
        screen.fill(COLORS.BLACK)

        # Título
        TextComponent.draw(
            screen,
            "ASTEROIDS",
            (SCREEN.WIDTH // 2, 200),
            self.font_big,
            COLORS.WHITE,
            center=True,
        )

        # Instruções
        TextComponent.draw(
            screen,
            "Setas/WASD: Mover | Espaço: Atirar | Shift: Hiper",
            (SCREEN.WIDTH // 2, 350),
            self.font_main,
            COLORS.GRAY,
            center=True,
        )

        TextComponent.draw(
            screen,
            "Pressione ESPAÇO ou ENTER para começar",
            (SCREEN.WIDTH // 2, 500),
            self.font_main,
            COLORS.WHITE,
            center=True,
        )
