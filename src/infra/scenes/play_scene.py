import pygame as pg

import src.config.client.styles as COLORS

from src.core.engine import SimulationEngine

from src.infra.controllers.player_controller import PlayerController
from src.infra.managers.input_manager import InputManager

from src.infra.managers.sound_manager import SoundManager
from src.infra.renderers.ui.hud import HUDRenderer
from src.infra.renderers.ui.hud_info import HUDInfo

from src.infra.renderers.entities.base import EntityRenderer
from src.infra.renderers.entities.ship import ShipRenderer
from src.infra.renderers.entities.asteroid import AsteroidRenderer
from src.infra.renderers.entities.ufo import UfoRenderer
from src.infra.renderers.entities.bullet import BulletRenderer

from .base_scene import BaseScene


class PlayScene(BaseScene):
    """Playing scene state manager"""

    def __init__(self, manager, assets, **kwargs):
        super().__init__(manager, assets)
        selected_ship = kwargs.get("selected_ship", "DEFAULT")
        self.engine = SimulationEngine(ship_type=selected_ship)
        self.input_manager = InputManager()
        self.sound_manager = SoundManager(assets)

        self.entity_sprite_map: dict[str, EntityRenderer] = {
            "SHIP": ShipRenderer,
            "BULLET": BulletRenderer,
            "UFO": UfoRenderer,
            "UFO_BULLET": BulletRenderer,
            "ASTEROID": AsteroidRenderer,
        }

    def handle_events(self, events: list[pg.event.Event]):
        self.input_manager.update(events)
        if self.input_manager.impulses["EXIT"]:
            self.sound_manager.stop_all()
            self.manager.switch_to("menu")

    def _handle_core_events(self, events: list[str]):
        for event in events:
            if event == "TIMESTOP_END":
                self.sound_manager.play_sfx("timeresume")
            if event == "UFO_FIRE":
                self.sound_manager.play_sfx("shot", volume=0.3)

    def _handle_game_over(self):
        self.sound_manager.stop_all()
        self.sound_manager.play_sfx("gameover")

        self.manager.switch_to(
            "game_over",
            final_score=self.engine.score,
            waves=self.engine.current_wave,
            ship_class=self.engine.ship_type,
            power_uses=self.engine.power_use_count,
            time=self.engine.play_time,
        )

    def update(self, dt: float):

        old_score = self.engine.score
        old_lives = self.engine.lives
        old_wave = self.engine.current_wave

        ship = next((e for e in self.engine.entities if e.type == "SHIP"), None)
        PlayerController.handle_actions(
            ship, self.input_manager, self.sound_manager, self.engine
        )

        # Atualiza simulação
        self.engine.update(dt)

        # SFX Reativo (mudanças de estados no Core)
        if self.engine.lives < old_lives:
            self.sound_manager.play_sfx("crash", volume=1.0)
        if self.engine.score > old_score:
            self.sound_manager.play_sfx("objectdestroyed", volume=0.6)
        if self.engine.current_wave != old_wave:
            self.sound_manager.play_sfx("wavestart", volume=0.8)

        # A. Loop do UFO (Apareceu/Sumiu)
        has_ufo = any(e.type == "UFO" for e in self.engine.entities)
        if has_ufo and self.engine.time_system.state != "TOTAL":
            self.sound_manager.start_loop("alien", "ufo_env", volume=0.5)
        else:
            self.sound_manager.stop_loop("ufo_env")

        # D. Eventos vindos do Core (TIRO DO UFO)
        self._handle_core_events(self.engine.events)

        # Game over
        if self.engine.game_over:
            self._handle_game_over()

    def draw(self, screen: pg.Surface):
        screen.fill(COLORS.BLACK)
        for ent in self.engine.entities:
            if ent.is_active:
                sprite = self.entity_sprite_map.get(ent.type)
                if sprite:
                    sprite.draw(screen, ent)

        ship = next((e for e in self.engine.entities if e.type == "SHIP"), None)
        info = HUDInfo(
            score=self.engine.score,
            lives=self.engine.lives,
            wave=self.engine.wave_system.wave_count,
            power_cooldown=ship.power_cooldown if ship else 0,
            power_ready=ship.can_activate_power() if ship else False,
        )
        HUDRenderer.draw(screen, self.assets, info)
