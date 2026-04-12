import pygame as pg

from src.infra.renderers.ui.components.text import TextComponent
from src.infra.managers.input_manager import InputManager
import src.config.client.styles as COLORS
import src.config.client.ui as UI
import src.config.shared.dimensions as SCREEN

from .base_scene import BaseScene

class GameOverScene(BaseScene):
    """Lida com a exibição da pontuação final e o temporizador de fade-in."""
    
    def __init__(self, manager, assets, **kwargs):
        super().__init__(manager, assets)
        self.input_manager = InputManager()
        self.final_score = kwargs.get("final_score", 0)
        self.fade_timer = 0.0
        self.font_big = self.assets.get_font("big")
        self.font_main = self.assets.get_font("main")

    def handle_events(self, events: list[pg.event.Event]):
        self.input_manager.update(events)
        # Só permite sair/reiniciar após o fade inicial (opcional, para impacto visual)
        if self.fade_timer > 0.5:
            if self.input_manager.impulses["CONFIRM"]:
                self.manager.switch_to("play")
            if self.input_manager.impulses["EXIT"]:
                self.manager.switch_to("menu")

    def update(self, dt: float):
        self.fade_timer += dt

    def draw(self, screen: pg.Surface):
        # Efeito de Fade-in (Preto semi-transparente sobre o último frame do jogo)
        alpha = min(255, int(255 * self.fade_timer / UI.GAME_OVER_FADE_DURATION))
        overlay = pg.Surface((SCREEN.WIDTH, SCREEN.HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))

        if alpha > 100:
            TextComponent.draw(
                screen,
                "GAME OVER",
                (SCREEN.WIDTH // 2, SCREEN.HEIGHT // 2 - 100),
                self.font_big,
                COLORS.WHITE,
                center=True,
            )

            TextComponent.draw(
                screen,
                f"Pontuação Final: {self.final_score:06d}",
                (SCREEN.WIDTH // 2, SCREEN.HEIGHT // 2),
                self.font_main,
                COLORS.WHITE,
                center=True,
            )

            TextComponent.draw(
                screen,
                "ENTER: Jogar Novamente | ESC: Menu",
                (SCREEN.WIDTH // 2, SCREEN.HEIGHT // 2 + 80),
                self.font_main,
                COLORS.GRAY,
                center=True,
            )

