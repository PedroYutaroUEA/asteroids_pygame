import pygame as pg


class InputManager:
    """
    Gerenciador central de entradas.
    Abstrai teclas físicas (Setas/WASD/Espaço) em comandos lógicos.
    """

    def __init__(self):
        # Comandos que podem ser mantidos pressionados (Contínuos)
        self.commands = {
            "THRUST": False,
            "LEFT": False,
            "RIGHT": False,
        }

        # Comandos de clique único (Impulsos)
        # Devem ser consumidos pela Scene e resetados
        self.impulses = {"FIRE": False, "HYPER": False, "EXIT": False, "CONFIRM": False}

    def update(self, events: list[pg.event.Event]):
        """
        Atualiza o estado dos comandos baseando-se nas teclas pressionadas
        e na fila de eventos do Pygame.
        """
        # 1. Atualiza estados contínuos (Movimentação)
        keys = pg.key.get_pressed()

        self.commands["THRUST"] = keys[pg.K_UP] or keys[pg.K_w]
        self.commands["LEFT"] = keys[pg.K_LEFT] or keys[pg.K_a]
        self.commands["RIGHT"] = keys[pg.K_RIGHT] or keys[pg.K_d]

        # 2. Reseta impulsos do frame anterior
        for key in self.impulses:
            self.impulses[key] = False

        # 3. Processa eventos discretos (Cliques únicos)
        for event in events:
            if event.type == pg.KEYDOWN:
                # Ação de Atirar
                if event.key == pg.K_SPACE:
                    self.impulses["FIRE"] = True

                # Ação de Hyperspace
                if event.key == pg.K_LSHIFT:
                    self.impulses["HYPER"] = True

                # Confirmação (Menus/Game Over)
                if event.key in (pg.K_RETURN, pg.K_KP_ENTER, pg.K_SPACE):
                    self.impulses["CONFIRM"] = True

                # Sair / Voltar
                if event.key == pg.K_ESCAPE:
                    self.impulses["EXIT"] = True

    def any_key_pressed(self, events: list[pg.event.Event]) -> bool:
        """Útil para a tela de menu 'Pressione qualquer tecla'."""
        for event in events:
            if event.type == pg.KEYDOWN:
                return True
        return False
