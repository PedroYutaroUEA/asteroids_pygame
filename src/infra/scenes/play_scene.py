import pygame as pg

import src.config.client.styles as COLORS
import src.config.server.balancing as BALANCE

from src.core.engine import SimulationEngine

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
        self.engine = SimulationEngine()
        self.input_manager = InputManager()
        self.sound_manager = SoundManager(assets)

        self.entity_sprite_map: dict[str, EntityRenderer] = {
            "SHIP": ShipRenderer,
            "ASTEROID": AsteroidRenderer,
            "UFO": UfoRenderer,
            "BULLET": BulletRenderer,
            "UFO_BULLET": BulletRenderer,
        }

    def handle_events(self, events: list[pg.event.Event]):
        self.input_manager.update(events)
        if self.input_manager.impulses["EXIT"]:
            self.sound_manager.stop_all()
            self.manager.switch_to("menu")

    def update(self, dt: float):
        old_score = self.engine.score
        old_lives = self.engine.lives

        ship = next((e for e in self.engine.entities if e.type == "SHIP"), None)
        if ship and ship.is_active:
            # Movimentação contínua
            if self.input_manager.commands["LEFT"]:
                ship.rotate("L", dt)
            if self.input_manager.commands["RIGHT"]:
                ship.rotate("R", dt)

            # Thrust com som contínuo
            if self.input_manager.commands["THRUST"]:
                ship.apply_thrust(dt)
                self.sound_manager.start_loop("spaceship1", "thrust", volume=0.4)
            else:
                self.sound_manager.stop_loop("thrust")

            # Tiro
            if self.input_manager.impulses["FIRE"]:
                fire_data = ship.get_fire_data()
                if fire_data:
                    self.engine.spawner.spawn_bullet(
                        fire_data["pos"], fire_data["vel"], "SHIP"
                    )
                    self.sound_manager.play_sfx("shot", volume=0.5)

            # Hyperspace
            if self.input_manager.impulses["HYPER"]:
                if self.engine.score >= BALANCE.HYPERSPACE_COST:
                    ship.hyperspace()
                    self.engine.score -= BALANCE.HYPERSPACE_COST

        # Atualiza simulação
        self.engine.update(dt)

        # A. Loop do UFO (Apareceu/Sumiu)
        has_ufo = any(e.type == "UFO" for e in self.engine.entities)
        if has_ufo:
            self.sound_manager.start_loop("alien", "ufo_env", volume=0.5)
        else:
            self.sound_manager.stop_loop("ufo_env")

        # B. Perda de Vida (Crash)
        if self.engine.lives < old_lives:
            self.sound_manager.play_sfx("crash", volume=1.0)

        # C. Pontuação (Destruição)
        if self.engine.score > old_score:
            self.sound_manager.play_sfx("objectdestroyed", volume=0.6)

        # D. Eventos vindos do Core (TIRO DO UFO)
        for event in self.engine.events:
            if event == "UFO_FIRE":
                self.sound_manager.play_sfx("shot", volume=0.3)

        # Game over
        if self.engine.game_over:
            self.sound_manager.stop_all()
            self.sound_manager.play_sfx("gameover")
            self.manager.switch_to("game_over", final_score=self.engine.score)

    def draw(self, screen: pg.Surface):
        screen.fill(COLORS.BLACK)
        for ent in self.engine.entities:
            if ent.is_active:
                sprite = self.entity_sprite_map.get(ent.type)
                if sprite:
                    sprite.draw(screen, ent)

        info = HUDInfo(
            self.engine.score, self.engine.lives, self.engine.wave_system.wave_count
        )
        HUDRenderer.draw(screen, self.assets, info)
