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
        if not pg.mixer.get_init():
            pg.mixer.init()

        self._load_fonts()
        self._load_sfx()

    def _load_fonts(self):
        # Localização: src/assets/fonts/
        path = os.path.join(os.getcwd(), "src", "assets", "fonts")
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
        """Lê todos os arquivos .wav da pasta sfx e usa o nome como chave."""
        path = os.path.join(os.getcwd(), "src", "assets", "sfx")

        if not os.path.exists(path):
            print(f"Warning: pasta de assets não encontrada: {path}")
            return

        for filename in os.listdir(path):
            if filename.endswith(".wav") or filename.endswith(".ogg"):
                # "shot.wav" -> chave: "shot"
                key = os.path.splitext(filename)[0]
                full_path = os.path.join(path, filename)

                try:
                    self.sounds[key] = pg.mixer.Sound(full_path)
                except Exception as e:
                    print(f"Erro ao carregar {filename}: {e}")

    def get_sound(self, key: str) -> pg.mixer.Sound:
        return self.sounds.get(key)

    def get_font(self, key: str) -> pg.font.Font:
        return self.fonts.get(key, self.fonts.get("main"))
