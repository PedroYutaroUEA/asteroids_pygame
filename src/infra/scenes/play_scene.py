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

    def handle_events(self, events: list[pg.event.Event]):
        # Atualiza o estado das teclas e impulsos (tiro, etc)
        self.input_manager.update(events)
        # Verifica se o usuário quer sair para o menu
        if self.input_manager.impulses["EXIT"]:
            self.manager.switch_to("menu")

    def update(self, dt: float):
        # 1. Busca a referência da nave no Core para aplicar comandos de movimento
        ship = next((e for e in self.engine.entities if e.type == "SHIP"), None)
        old_score = self.engine.score

        if ship and ship.is_active:
            # Comandos Contínuos (Movimentação)
            if self.input_manager.commands["LEFT"]:
                ship.rotate("L", dt)
            if self.input_manager.commands["RIGHT"]:
                ship.rotate("R", dt)
            if self.input_manager.commands["THRUST"]:
                ship.apply_thrust(dt)

            # Comandos de Impulso (Ações únicas)
            if self.input_manager.impulses["FIRE"]:
                fire_data = ship.get_fire_data()
                if fire_data:
                    self.engine.spawner.spawn_bullet(
                        fire_data["pos"], fire_data["vel"], "SHIP"
                    )
                    sound = self.assets.get_sound("fire")
                    if sound:
                        sound.play()

            if self.input_manager.impulses["HYPER"]:
                # Aplica o custo do hyperspace conforme logic do deprecated
                if self.engine.score >= BALANCE.HYPERSPACE_COST:
                    ship.hyperspace()
                    self.engine.score -= BALANCE.HYPERSPACE_COST

        # 2. Executa o passo da simulação física pura (Core)
        self.engine.update(dt)

        if self.engine.score > old_score:
            # Se o score aumentou, algo explodiu!
            sound = self.assets.get_sound("bang_s")
            if sound:
                sound.play()
        # 3. Transição de Estado: Game Over
        if self.engine.game_over:
            self.manager.switch_to("game_over", final_score=self.engine.score)

    def draw(self, screen: pg.Surface):
        # Limpa a tela com a cor de fundo
        screen.fill(COLORS.BLACK)

        # 1. Renderiza as Entidades usando a Infra
        for ent in self.engine.entities:
            if ent.is_active:
                sprite = self.entity_sprite_map.get(ent.type)
                if sprite:
                    sprite.draw(screen, ent)

        # 2. Renderiza o HUD (Score e Lives)
        info = HUDInfo(
            self.engine.score, self.engine.lives, self.engine.wave_system.wave_count
        )
        HUDRenderer.draw(screen, self.assets, info)
