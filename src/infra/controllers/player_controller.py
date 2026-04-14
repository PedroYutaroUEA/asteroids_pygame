import src.config.server.balancing as BALANCE
from src.core.engine import SimulationEngine
from src.core.entities.implementations.ships.base import ShipEntity
from src.infra.managers.input_manager import InputManager
from src.infra.managers.sound_manager import SoundManager


class PlayerController:
    """Gerencia a interação entre Inputs e a Entidade da Nave"""

    @staticmethod
    def __handle_movement(
        ship: ShipEntity,
        input_manager: InputManager,
        sound_manager: SoundManager,
    ):
        if input_manager.commands["LEFT"]:
            ship.rotate("L", 0.016)  # dt simplificado ou passado
        if input_manager.commands["RIGHT"]:
            ship.rotate("R", 0.016)

        if input_manager.commands["THRUST"]:
            ship.apply_thrust(0.016)
            sound_manager.start_loop("spaceship1", "thrust", volume=0.3)
        else:
            sound_manager.stop_loop("thrust")

    @staticmethod
    def __handle_power(
        ship: ShipEntity,
        sound_manager: SoundManager,
        engine: SimulationEngine,
    ):
        if ship.activate_power():
            ship.power_use_count += 1

            sfx_map = {
                "INTANGIBLE": "intangi",
                "TRIPLE": "bomber",
                "SHIELD": "shield",
                "TIMESTOP": "timestop",
                "RICOCHET": "ricoche",
            }
            sfx_key = sfx_map.get(ship.ship_class, "timeresume")
            sound_manager.play_sfx(sfx_key)

            if ship.ship_class == "TIMESTOP":
                engine.time_system.start_freeze()

    @staticmethod
    def __handle_shooting(
        ship: ShipEntity,
        sound_manager: SoundManager,
        engine: SimulationEngine,
    ):
        fire_list = ship.get_fire_data()
        if fire_list:
            for b in fire_list:
                engine.spawner.spawn_bullet(
                    b["pos"],
                    b["vel"],
                    "SHIP",
                    rad=b.get("rad", 2),
                    ricochet=b.get("can_ricochet", False),
                    max_bounces=b.get("max_bounces", 0),
                )
            sound_manager.play_sfx("shot", volume=0.5)

    @staticmethod
    def handle_actions(
        ship: ShipEntity,
        input_manager: InputManager,
        sound_manager: SoundManager,
        engine: SimulationEngine,
    ):
        """Handles Player's movement, powers and shooting"""
        if not ship or not ship.is_active:
            return
        # 1. Movimentação
        PlayerController.__handle_movement(ship, input_manager, sound_manager)
        # 2. Poder Especial
        if input_manager.impulses["HYPER"]:
            PlayerController.__handle_power(ship, sound_manager, engine)
        # 3. Disparo
        if input_manager.impulses["FIRE"]:
            PlayerController.__handle_shooting(ship, sound_manager, engine)
