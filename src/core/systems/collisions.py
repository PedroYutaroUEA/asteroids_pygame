import math
import random
from src.core.entities.base import PhysVec
import src.config.server as SERVER
import src.config.shared as SHARED
from src.core.engine import SimulationEngine


class CollisionSystem:
    def __init__(self, engine: SimulationEngine):
        self.engine = engine
        # Mapeamento de pares de tipos para métodos de reação.
        # O par é sempre ordenado alfabeticamente para evitar duplicidade (ex: SHIP antes de UFO).
        self.handlers = {
            ("ASTEROID", "BULLET"): self._handle_asteroid_projectile,
            ("ASTEROID", "UFO_BULLET"): self._handle_asteroid_projectile,
            ("ASTEROID", "SHIP"): self._handle_ship_collision,
            ("BULLET", "UFO"): self._handle_ufo_hit,
            ("SHIP", "UFO"): self._handle_ship_collision,
            ("SHIP", "UFO_BULLET"): self._handle_ship_collision,
        }

    def check_all(self, entities):
        """Varre todas as combinações de entidades para detectar colisões."""
        for i, a in enumerate(entities):
            for b in entities[i + 1 :]:
                if a.is_active and b.is_active and a.check_collision(b):
                    # Ordena os tipos para bater com as chaves do dicionário handlers
                    pair = tuple(sorted((a.type, b.type)))
                    if pair in self.handlers:
                        self.handlers[pair](a, b)

    # --- HANDLERS DE REAÇÃO ---

    def _handle_asteroid_projectile(self, obj_a, obj_b):
        """Lida com qualquer projétil (Player ou UFO) atingindo um asteroide."""
        asteroid = obj_a if obj_a.type == "ASTEROID" else obj_b
        projectile = obj_b if obj_a.type == "ASTEROID" else obj_a

        projectile.is_active = False
        asteroid.is_active = False

        # Pontuação apenas se for bala do jogador (BULLET)
        if projectile.type == "BULLET":
            self.engine.score += SERVER.AST_SCORES[asteroid.size]

        self._split_asteroid(asteroid)

    def _handle_ufo_hit(self, obj_a, obj_b):
        """Lida com a bala do jogador atingindo o UFO."""
        ufo = obj_a if obj_a.type == "UFO" else obj_b
        bullet = obj_b if obj_a.type == "UFO" else obj_a

        bullet.is_active = False
        ufo.is_active = False

        # Define score baseado no tipo de UFO (Small ou Big)
        score = SERVER.UFO_PROFILES[ufo.profile]["score"]
        self.engine.score += score

    def _handle_ship_collision(self, obj_a, obj_b):
        """Lida com a nave batendo em Asteroides, UFOs ou balas de UFO."""
        ship = obj_a if obj_a.type == "SHIP" else obj_b
        other = obj_b if obj_a.type == "SHIP" else obj_a

        # Só processa se a nave não estiver invulnerável (Safe Spawn)
        if ship.invuln_timer <= 0:
            if other.type == "UFO_BULLET":
                other.is_active = False

            self._ship_die(ship)

    # --- MÉTODOS AUXILIARES ---

    def _ship_die(self, ship):
        """Processa a perda de vida e reset da nave conforme o deprecated/systems.py."""
        self.engine.lives -= 1

        if self.engine.lives <= 0:
            self.engine.game_over = True
            ship.is_active = False
        else:
            # Lógica de Reset: Reposiciona no centro e dá tempo de proteção
            ship.pos = PhysVec(SHARED.WIDTH / 2, SHARED.HEIGHT / 2)
            ship.vel = PhysVec(0, 0)
            ship.angle = -90.0
            ship.invuln_timer = SERVER.SAFE_SPAWN_TIME

    def _split_asteroid(self, ast):
        """Cria os fragmentos menores quando um asteroide é destruído."""
        fragments = SHARED.AST_SIZES[ast.size]["split"]
        for size_code in fragments:
            # Ângulo aleatório para os pedaços se espalharem
            ang = random.uniform(0, math.tau)
            # Velocidade um pouco maior que o original para dar dinamismo
            speed = random.uniform(SERVER.AST_VEL_MIN, SERVER.AST_VEL_MAX) * 1.2
            vel = PhysVec(math.cos(ang) * speed, math.sin(ang) * speed)

            # Pede ao spawner para criar o novo asteroide na posição atual do pai
            self.engine.spawner.spawn_asteroid(
                PhysVec(ast.pos.x, ast.pos.y), vel, size_code
            )
