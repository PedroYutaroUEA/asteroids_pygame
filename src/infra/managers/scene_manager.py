import sys
import pygame as pg

from src.infra.scenes.base_scene import BaseScene


class SceneManager:
    """
    Gerenciador central de cenas (FSM - Finite State Machine).
    Responsável por orquestrar a troca de telas e manter o loop principal.
    """

    def __init__(self, screen: pg.Surface, assets):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.scenes: dict[str, BaseScene] = (
            {}
        )  # Dicionário para mapear nomes de cenas para classes
        self.current_scene: BaseScene = None
        self.running = True
        self.assets = assets

    def register_scenes(self, scene_map: dict):
        """Mapeia nomes (strings) para as classes das cenas."""
        self.scenes = scene_map

    def switch_to(self, scene_name: str, **kwargs):
        """
        Instancia e troca para a nova cena.
        **kwargs permite passar dados entre cenas (ex: score para o Game Over).
        """
        if scene_name in self.scenes:
            # Cria uma nova instância da cena passando o manager e os dados extras
            self.current_scene = self.scenes[scene_name](self, self.assets, **kwargs)
        else:
            print(f"Erro: Cena '{scene_name}' não encontrada no registro.")

    def quit(self):
        """Encerra o loop do jogo com segurança."""
        self.running = False

    def run(self, fps: int):
        """
        O "Coração" do jogo.
        Este é o único loop 'while True' que deve existir no sistema.
        """
        while self.running:
            # 1. Cálculo do Delta Time (tempo entre frames em segundos)
            # Essencial para a física do Core ser independente do hardware
            dt = self.clock.tick(fps) / 1000.0

            # 2. Captura de Eventos do Sistema
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.quit()

            # 3. Delegação para a Cena Atual
            if self.current_scene:
                # A cena decide o que fazer com os eventos (teclado/input)
                self.current_scene.handle_events(events)

                # A cena atualiza sua lógica (que por sua vez atualiza o Core Engine)
                self.current_scene.update(dt)

                # A cena desenha os elementos (usando os Renderers da Infra)
                self.current_scene.draw(self.screen)

            # 4. Atualiza o display físico
            pg.display.flip()

        pg.quit()
        sys.exit()
