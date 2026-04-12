import pygame as pg


class TextComponent:
    """Utilitário para renderização de texto com suporte a alinhamento."""

    @staticmethod
    def draw(
        surface: pg.Surface,
        text: str,
        pos: tuple[int, int],
        font: pg.font.Font,
        color: tuple[int, int, int],
        center=False,
    ):
        """Desenha texto na tela. Se center=True, pos será o centro do texto."""
        img = font.render(text, True, color)
        rect = img.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos

        surface.blit(img, rect)
