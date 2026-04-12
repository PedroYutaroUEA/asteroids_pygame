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

        # Guarda referência do som de thrust para controle contínuo
        self.thrust_sound = self.assets.get_sound("spaceship1")
        self.ufo_loop_sound = self.assets.get_sound(
            "bomber"
        )  # Usando bomber.wav para o UFO
        self.thrust_playing = False  # controla se o som já está tocando
        self.ufo_playing = False

    def handle_events(self, events: list[pg.event.Event]):
        self.input_manager.update(events)
        if self.input_manager.impulses["EXIT"]:
            # Garante que o som de thrust para ao sair
            if self.thrust_sound:
                self.thrust_sound.stop()
            self.manager.switch_to("menu")

    def _play_sfx(self, key, volume=1.0):
        sound = self.assets.get_sound(key)
        if sound:
            sound.set_volume(volume)
            sound.play()

    def _stop_all_loops(self):
        if self.thrust_sound:
            self.thrust_sound.stop()
        if self.ufo_loop_sound:
            self.ufo_loop_sound.stop()

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
                    self._play_sfx("shot", volume=0.5)

            # Hyperspace
            if self.input_manager.impulses["HYPER"]:
                if self.engine.score >= BALANCE.HYPERSPACE_COST:
                    ship.hyperspace()
                    self.engine.score -= BALANCE.HYPERSPACE_COST

        # Atualiza simulação
        self.engine.update(dt)

        # 4. PROCESSAMENTO DE EVENTOS SONOROS (INFRA)

        # A. Perda de Vida (Crash)
        if self.engine.lives < old_lives:
            self._play_sfx("crash", volume=0.7)

        # B. Pontuação (Destruição)
        if self.engine.score > old_score:
            self._play_sfx("objectdestroyed", volume=0.4)

        # C. Eventos do Core (Disparo do UFO)
        for event in self.engine.events:
            if event == "UFO_FIRE":
                self._play_sfx("shot", volume=0.3)  # Tiro do UFO é mais baixo

        # D. Loop do UFO (Apareceu/Sumiu)
        has_ufo = any(e.type == "UFO" for e in self.engine.entities)
        if has_ufo and not self.ufo_playing:
            if self.ufo_loop_sound:
                self.ufo_loop_sound.play(loops=-1)
                self.ufo_playing = True
        elif not has_ufo and self.ufo_playing:
            if self.ufo_loop_sound:
                self.ufo_loop_sound.stop()
                self.ufo_playing = False

        # Game over
        if self.engine.game_over:
            self._stop_all_loops()
            self._play_sfx("gameover")
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
