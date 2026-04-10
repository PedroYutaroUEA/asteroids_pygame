from src.core.entities.base import Entity
from src.core.entities.implementations.ship import ShipEntity
from src.core.systems import WaveSystem, SpawnerSystem, CollisionSystem
import src.config.server as SERVER
import src.config.shared as SHARED


class SimulationEngine:
    """
    Manages Systems and Logic Entities interactions
    """

    def __init__(self):
        self.entities: list[Entity] = []
        self.score = 0
        self.lives = SERVER.START_LIVES
        self.game_over = False

        # Injeção de dependência dos sistemas
        self.spawner = SpawnerSystem(self)
        self.wave_system = WaveSystem(self)
        self.collision_system = CollisionSystem(self)

        # Inicializa a nave do jogador
        self.spawn_player()

        # Timer do UFO (Extraído do World.update do deprecated)
        self.ufo_spawn_timer = SERVER.UFO_SPAWN_EVERY

    def spawn_player(self):
        player = ShipEntity(SHARED.WIDTH / 2, SHARED.HEIGHT / 2)
        player.invuln_timer = SERVER.SAFE_SPAWN_TIME
        self.entities.append(player)

    def update(self, dt: float):
        if self.game_over:
            return

        # 1. Atualização Individual (Física e Lógicas Internas)
        self.__update_physics(dt)

        # 2. Lógica de UFO (Timer de Spawn)
        self.__update_ufo(dt)

        # 4. Sistemas de Mundo
        self.wave_system.update(dt)
        self.collision_system.check_all(self.entities)

        # 5. Limpeza de Entidades Mortas
        self.entities = [e for e in self.entities if e.is_active]

    def __update_physics(self, dt: float):
        for ent in self.entities:
            ent.move(dt)
            ent.update(dt)  # Fricção, TTL, etc.
            ent.react_to_boundary(SHARED.WIDTH, SHARED.HEIGHT)

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
