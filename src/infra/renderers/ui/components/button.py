import pygame as pg
import src.config.client.styles as COLORS
from .text import TextComponent


class ButtonComponent:
    """Componente de botão interativo para menus."""

    def __init__(
        self, text: str, pos: tuple[int, int], size: tuple[int, int], font: pg.font.Font
    ):
        self.text = text
        self.rect = pg.Rect(pos, size)
        self.font = font
        self.is_hovered = False

    def update(self):
        """Verifica se o mouse está sobre o botão."""
        mouse_pos = pg.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pg.Surface):
        color = COLORS.WHITE if self.is_hovered else COLORS.GRAY
        # Borda do botão
        pg.draw.rect(surface, color, self.rect, width=2)
        # Texto centralizado
        TextComponent.draw(
            surface, self.text, self.rect.center, self.font, color, center=True
        )

    def is_clicked(self, event: pg.event.Event) -> bool:
        """Retorna True se o botão foi clicado com o botão esquerdo."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False
