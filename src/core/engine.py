import src.config.server as SERVER
import src.config.shared as SHARED

from src.core.systems.spawner import SpawnerSystem
from src.core.systems.collisions import CollisionSystem
from src.core.systems.time_freeze import TimeSystem
from src.core.systems.wave import WaveSystem

from .entities.base.entity import Entity
from .entities.implementations.ships.default import DefaultShip
from .entities.implementations.ships.intangible import IntangibleShip
from .entities.implementations.ships.triple_shot import TripleShotShip
from .entities.implementations.ships.shield_ship import ShieldShip
from .entities.implementations.ships.time_stop import TimeStopShip
from .entities.implementations.ships.ricochet_shot import RicochetShip


class SimulationEngine:
    """
    Manages Systems and Logic Entities interactions
    """

    def __init__(self, ship_type="DEFAULT"):
        self.entities: list[Entity] = []
        self.events: list[str] = []
        self.score = 0
        self.play_time = 0.0
        self.current_wave = 0
        self.power_use_count = 0
        self.lives = SERVER.START_LIVES
        self.game_over = False
        self.ship_type = ship_type

        # Injeção de dependência dos sistemas
        self.time_system = TimeSystem()
        self.spawner = SpawnerSystem(self)
        self.wave_system = WaveSystem(self)
        self.collision_system = CollisionSystem(self)

        # Inicializa a nave do jogador
        self.spawn_player()
        # Timer do UFO (Extraído do World.update do deprecated)
        self.ufo_spawn_timer = SERVER.UFO_SPAWN_EVERY

    def spawn_player(self):
        """creates player entity"""
        factory = {
            "INTANGIBLE": IntangibleShip,
            "TRIPLE": TripleShotShip,
            "SHIELD": ShieldShip,
            "TIMESTOP": TimeStopShip,
            "RICOCHET": RicochetShip,
            "DEFAULT": DefaultShip,
        }

        ship_constructor = factory.get(self.ship_type, DefaultShip)
        player = ship_constructor(SHARED.WIDTH / 2, SHARED.HEIGHT / 2)
        player.type = "SHIP"
        player.ship_class = self.ship_type
        player.invuln_timer = SERVER.SAFE_SPAWN_TIME
        self.entities.append(player)

    def update(self, dt: float):
        """Main game frame function"""
        if self.game_over:
            return
        self.events.clear()
        self.play_time += dt

        # Atualiza o estado do tempo (TimeStop)
        time_event = self.time_system.update(dt)
        if time_event:
            self.events.append(time_event)

        # Física Seletiva
        for ent in self.entities:
            is_player_bullet = (
                ent.type == "BULLET" and getattr(ent, "source", "") == "SHIP"
            )
            if self.time_system.should_update(ent.type) or is_player_bullet:
                ent.move(dt)
                ent.update(dt)
                ent.react_to_boundary(SHARED.WIDTH, SHARED.HEIGHT)

        # Sistemas de Mundo (Só rodam se o tempo não estiver totalmente parado)
        if self.time_system.state != "TOTAL":
            self.__update_ufo(dt)
            self.current_wave = self.wave_system.update(dt)

        # Colisão + Limpeza de Entidades Mortas
        self.collision_system.check_all(self.entities)
        self.entities = [e for e in self.entities if e.is_active]

    def __update_ufo(self, dt: float):
        ufo = next((e for e in self.entities if e.type == "UFO"), None)
        if not ufo:
            self.ufo_spawn_timer -= dt
            if self.ufo_spawn_timer <= 0:
                self.spawner.spawn_ufo()
                self.ufo_spawn_timer = SERVER.UFO_SPAWN_EVERY
        else:  # 3. Lógica de Ataque do UFO (se existir)
            ship = next((e for e in self.entities if e.type == "SHIP"), None)
            if ship:
                fire_data = ufo.try_fire_at(ship.pos, dt)
                if fire_data:
                    self.spawner.spawn_bullet(fire_data["pos"], fire_data["vel"], "UFO")
                    self.events.append("UFO_FIRE")
