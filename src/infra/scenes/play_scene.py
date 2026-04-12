import pygame as pg

import src.config.client.styles as COLORS
import src.config.server.balancing as BALANCE

from src.core.engine import SimulationEngine

from src.infra.managers.input_manager import InputManager

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

        self.entity_sprite_map: dict[str, EntityRenderer] = {
            "SHIP": ShipRenderer,
            "ASTEROID": AsteroidRenderer,
            "UFO": UfoRenderer,
            "BULLET": BulletRenderer,
            "UFO_BULLET": BulletRenderer,
        }

        # Ajusta volumes iniciais
        if self.assets.get_sound("shot"):
            self.assets.get_sound("shot").set_volume(0.6)
        if self.assets.get_sound("objectdestroyed"):
            self.assets.get_sound("objectdestroyed").set_volume(0.5)
        if self.assets.get_sound("spaceship1"):
            self.assets.get_sound("spaceship1").set_volume(0.4)
        if self.assets.get_sound("gameover"):
            self.assets.get_sound("gameover").set_volume(0.4)

        # Guarda referência do som de thrust para controle contínuo
        self.thrust_sound = self.assets.get_sound("spaceship1")
        self.thrust_playing = False  # controla se o som já está tocando

    def handle_events(self, events: list[pg.event.Event]):
        self.input_manager.update(events)
        if self.input_manager.impulses["EXIT"]:
            # Garante que o som de thrust para ao sair
            if self.thrust_sound:
                self.thrust_sound.stop()
            self.manager.switch_to("menu")

    def update(self, dt: float):
        ship = next((e for e in self.engine.entities if e.type == "SHIP"), None)
        old_score = self.engine.score

        if ship and ship.is_active:
            # Movimentação contínua
            if self.input_manager.commands["LEFT"]:
                ship.rotate("L", dt)
            if self.input_manager.commands["RIGHT"]:
                ship.rotate("R", dt)

            # Thrust com som contínuo
            thrusting = self.input_manager.commands["THRUST"]
            if thrusting:
                ship.apply_thrust(dt)
                if self.thrust_sound and not self.thrust_playing:
                    self.thrust_sound.play(loops=-1)
                    self.thrust_playing = True
            else:
                if self.thrust_sound and self.thrust_playing:
                    self.thrust_sound.stop()
                    self.thrust_playing = False

            # Tiro
            if self.input_manager.impulses["FIRE"]:
                fire_data = ship.get_fire_data()
                if fire_data:
                    self.engine.spawner.spawn_bullet(
                        fire_data["pos"], fire_data["vel"], "SHIP"
                    )
                    sound = self.assets.get_sound("shot")
                    if sound:
                        sound.play()

            # Hyperspace
            if self.input_manager.impulses["HYPER"]:
                if self.engine.score >= BALANCE.HYPERSPACE_COST:
                    ship.hyperspace()
                    self.engine.score -= BALANCE.HYPERSPACE_COST

        # Atualiza simulação
        self.engine.update(dt)

        # Som de explosão quando score aumenta
        if self.engine.score > old_score:
            sound = self.assets.get_sound("objectdestroyed")
            if sound:
                sound.play()

        # Game over
        if self.engine.game_over:
            if self.thrust_sound:
                self.thrust_sound.stop()
                self.thrust_playing = False
            self.manager.switch_to("game_over", final_score=self.engine.score)
            sound = self.assets.get_sound("gameover")
            if sound:
                sound.play()

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