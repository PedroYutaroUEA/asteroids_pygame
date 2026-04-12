import pygame as pg
from src.infra.managers.asset_manager import AssetManager
from src.infra.managers.scene_manager import SceneManager
import src.config.client.ui as UI
import src.config.shared.dimensions as SCREEN
from src.infra.scenes.menu_scene import MenuScene
from src.infra.scenes.game_over import GameOverScene
from src.infra.scenes.play_scene import PlayScene




class Game:
    """main game runner"""

    def __init__(self, cap: str):
        self.captions = cap

    def run(self):
        pg.init()
        # init audio
        pg.mixer.init()

        screen = pg.display.set_mode((SCREEN.WIDTH, SCREEN.HEIGHT))
        pg.display.set_caption(self.captions)
        # load resources
        assets = AssetManager()
        assets.load_all()

        # Init state manager
        manager = SceneManager(screen, assets)
        # Registra as cenas disponíveis
        manager.register_scenes(
            {"menu": MenuScene, "play": PlayScene, "game_over": GameOverScene}
        )
        # Começa pelo Menu
        manager.switch_to("menu")
        # Inicia o loop infinito
        manager.run(fps=UI.FPS)
