import pygame as pg

from src.core.entities.implementations.ships.base import ShipEntity
from src.infra.renderers.entities.ship import ShipRenderer
from src.infra.renderers.ui.components.ship_selector import ShipSelectorComponent
from src.infra.renderers.ui.components.text import TextComponent
from src.infra.managers.input_manager import InputManager
import src.config.client.styles as COLORS
import src.config.shared.dimensions as SCREEN
import src.config.server.gameplay as GAMEPLAY
from .base_scene import BaseScene


class MenuScene(BaseScene):
    """Focada em exibir o título e aguardar o comando de início."""

    def __init__(self, manager, assets, **kwargs):
        super().__init__(manager, assets)
        self.input_manager = InputManager()
        self.font_big = self.assets.get_font("big")
        self.font_main = self.assets.get_font("main")

        self.previews = {}
        self.selected_index = 0
        self.ship_keys = list(GAMEPLAY.SHIP_DATA.keys())

        for key in self.ship_keys:
            dummy = ShipEntity(0, 0)
            dummy.type = "SHIP"
            dummy.ship_class = key
            self.previews[key] = dummy

    def handle_events(self, events: list[pg.event.Event]):
        self.input_manager.update(events)

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.selected_index = (self.selected_index - 1) % len(
                        self.ship_keys
                    )
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.selected_index = (self.selected_index + 1) % len(
                        self.ship_keys
                    )

                if self.input_manager.impulses["CONFIRM"]:
                    selected_key = self.ship_keys[self.selected_index]
                    self.manager.switch_to("play", selected_ship=selected_key)
                if self.input_manager.impulses["EXIT"]:
                    self.manager.quit()

    def update(self, dt: float):
        for ship in self.previews.values():
            ship.angle += 45 * dt

    def draw(self, screen: pg.Surface):
        screen.fill(COLORS.BLACK)

        # Título
        TextComponent.draw(
            screen,
            "ESTEROIDES",
            (SCREEN.WIDTH // 2, 80),
            self.font_big,
            COLORS.WHITE,
            center=True,
        )

        # Instruções
        TextComponent.draw(
            screen,
            "Setas/WASD: Mover | Espaço: Atirar | Shift: Hiper",
            (SCREEN.WIDTH // 2, 120),
            self.font_main,
            COLORS.GRAY,
            center=True,
        )

        start_y = 200
        ShipSelectorComponent.draw_selection_list(
            screen,
            self.assets,
            self.ship_keys,
            self.selected_index,
            self.previews,
            start_y,
        )

        TextComponent.draw(
            screen,
            "Use SETAS para navegar e ESPAÇO para confirmar",
            (SCREEN.WIDTH // 2, SCREEN.HEIGHT - 50),
            self.font_main,
            COLORS.GRAY,
            center=True,
        )
