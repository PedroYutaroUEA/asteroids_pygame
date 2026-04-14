from src.infra.renderers.entities.ship import ShipRenderer
import src.config.client.styles as COLORS
import src.config.server.gameplay as GAMEPLAY
from src.infra.renderers.ui.components.text import TextComponent


class ShipSelectorComponent:
    """Componente visual e lógico para seleção de naves no menu"""

    @staticmethod
    def draw_selection_list(
        screen,
        assets,
        ship_keys: list[str],
        selected_index: int,
        previews: dict,
        start_y,
    ):
        """Ship selection selector list component"""
        font_main = assets.get_font("main")
        spacing = 75

        for i, key in enumerate(ship_keys):
            data = GAMEPLAY.SHIP_DATA[key]
            is_active = i == selected_index
            color = COLORS.SHIP_COLORS[key] if is_active else COLORS.GRAY
            y_pos = start_y + (i * spacing)

            # Preview da Nave
            ship = previews[key]
            ship.pos.x, ship.pos.y = 230, y_pos
            ShipRenderer.draw(screen, ship)

            # Info
            prefix = "> " if is_active else "  "
            TextComponent.draw(
                screen, f"{prefix}{data['name']}", (300, y_pos - 15), font_main, color
            )
            TextComponent.draw(
                screen, data["desc"], (300, y_pos + 5), font_main, COLORS.GRAY
            )
