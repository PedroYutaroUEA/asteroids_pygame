import os
import pygame as pg


class AssetManager:
    """
    Cache central de recursos. Carrega imagens, sons e fontes do disco
    para a memória RAM uma única vez.
    """

    def __init__(self):
        self.sounds: dict[str, pg.mixer.Sound] = {}
        self.fonts: dict[str, pg.font.Font] = {}
        self.images: dict[str, pg.Surface] = {}

    def load_all(self):
        """Carrega todos os assets definidos nos diretórios padrão."""
        if not pg.font.get_init():
            pg.font.init()
        self._load_fonts()
        self._load_sfx()

    def _load_fonts(self):
        # Localização: src/assets/fonts/
        path = "src/assets/fonts"
        required_fonts = {"main": 20, "big": 48}

        for key, size in required_fonts.items():
            font_loaded = False
            font_file = os.path.join(path, "consolas.ttf")

            if os.path.exists(font_file):
                try:
                    self.fonts[key] = pg.font.Font(font_file, size)
                    font_loaded = True
                except (IOError, TypeError):
                    print(f"Warning: Could not load fonts from {path}. Using default.")

            if not font_loaded:
                # Se não carregou do arquivo, usa a fonte do sistema (não retorna None)
                self.fonts[key] = pg.font.SysFont("Arial", size, bold=key == "big")

    def _load_sfx(self):
        # Localização: src/assets/sfx/
        path = "src/assets/sfx"
        if not os.path.exists(path):
            return

        # Mapeamento de arquivos para nomes lógicos
        sfx_files = {
            "fire": "fire.wav",
            "bang_l": "bangLarge.wav",
            "bang_m": "bangMedium.wav",
            "bang_s": "bangSmall.wav",
            "thrust": "thrust.wav",
            "ufo_fire": "ufo_fire.wav",
        }

        for key, filename in sfx_files.items():
            full_path = os.path.join(path, filename)
            if os.path.exists(full_path):
                try:
                    self.sounds[key] = pg.mixer.Sound(full_path)
                except (IOError, TypeError):
                    print(f"Warning: Could not load sfx from {path}. Using default.")

    def get_sound(self, key: str) -> pg.mixer.Sound:
        return self.sounds.get(key)

    def get_font(self, key: str) -> pg.font.Font:
        return self.fonts.get(key, self.fonts.get("main"))
