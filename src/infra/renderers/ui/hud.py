import pygame as pg
import src.config.client.styles as COLORS
import src.config.shared.dimensions as SCREEN
from src.infra.managers.asset_manager import AssetManager
from src.infra.renderers.ui.components.text import TextComponent
from src.infra.renderers.ui.hud_info import HUDInfo


class HUDRenderer:
    """Responsável por desenhar as informações de estado da partida na tela."""

    @staticmethod
    def draw(surface: pg.Surface, assets: AssetManager, info: HUDInfo):
        font = assets.get_font("main")

        # 1. Desenha Score (Canto superior esquerdo)
        TextComponent.draw(
            surface, f"SCORE {info.score:06d}", (20, 15), font, COLORS.WHITE
        )

        # 2. Desenha Wave (Centro)
        TextComponent.draw(
            surface,
            f"WAVE {info.wave}",
            (SCREEN.WIDTH // 2, 15),
            font,
            COLORS.WHITE,
            center=True,
        )

        # 3. Desenha Vidas (Canto superior direito)
        TextComponent.draw(
            surface, f"LIVES {info.lives}", (SCREEN.WIDTH - 120, 15), font, COLORS.WHITE
        )

        # 4. Linha decorativa inferior do HUD
        pg.draw.line(surface, COLORS.HUD_LINE, (0, 50), (SCREEN.WIDTH, 50), 1)
