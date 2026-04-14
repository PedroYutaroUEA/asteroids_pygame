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
        self.stats = kwargs
        self.input_manager = InputManager()
        self.fade_timer = 0.0

        self.font_big = self.assets.get_font("big")
        self.font_main = self.assets.get_font("main")

    def handle_events(self, events: list[pg.event.Event]):
        self.input_manager.update(events)
        # Só permite sair/reiniciar após o fade inicial (opcional, para impacto visual)
        if self.fade_timer > 0.5:
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
            center_x = SCREEN.WIDTH // 2
            TextComponent.draw(
                screen,
                "GAME OVER",
                (center_x, 100),
                self.font_big,
                COLORS.WHITE,
                center=True,
            )
            # Display Info
            info_y = 200
            stats_list = [
                f"Nave: {self.stats.get('ship_class')}",
                f"Pontuação: {self.stats.get('final_score'):06d}",
                f"Ondas Sobrevividas: {self.stats.get('waves')}",
                f"Poderes Ativados: {self.stats.get('power_uses')}",
                f"Tempo de Voo: {int(self.stats.get('time'))} segundos",
            ]

            for info in stats_list:
                TextComponent.draw(
                    screen,
                    info,
                    (center_x, info_y),
                    self.font_main,
                    COLORS.WHITE,
                    center=True,
                )
                info_y += 40

            TextComponent.draw(
                screen,
                "PRESSIONE ESC PARA VOLTAR AO MENU",
                (center_x, 550),
                self.font_main,
                COLORS.GRAY,
                center=True,
            )
