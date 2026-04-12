import pygame as pg
from typing import Optional, Dict
import os

class SoundManager:
    """
    Gerenciador central de sons.
    Carrega e reproduz efeitos sonoros do jogo.
    """

    def __init__(self):
        self.sounds: Dict[str, pg.mixer.Sound] = {}
        self.important_channel: Optional[pg.mixer.Channel] = None
        self.master_volume: float = 1.0
        self.sound_enabled: bool = True

        if not pg.mixer.get_init():
            pg.mixer.init()

        self.important_channel = pg.mixer.Channel(0)

        # sound_manager.py está em: src/infra/managers/
        # Precisa subir 3 níveis para chegar à raiz do projeto
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(   # raiz/
            os.path.dirname(                    # src/
                os.path.dirname(self.base_dir)  # infra/
            )
        )

    def load_sounds(self, asset_path: str = None):
        """
        Carrega todos os sons dos arquivos WAV.
        """
        # Monta o path absoluto até src/assets
        if asset_path is None:
            asset_path = os.path.join(self.project_root, "src", "assets")

        print(f"Procurando sons em: {asset_path}")
        print(f"Diretório atual: {os.getcwd()}")
        print(f"Raiz do projeto: {self.project_root}")

        sound_files = {
            "bomber":          "bomber.wav",
            "gameover":        "gameover.wav",
            "intangi":         "intangi.wav",
            "objectdestroyed": "objectdestroyed.wav",
            "ricoche":         "ricoche.wav",
            "shield":          "shield.wav",
            "shot":            "shot.wav",
            "spaceship1":      "spaceship1.wav",
            "timeresume":      "timeresume.wav",
            "timestop":        "timestop.wav"
        }

        success_count = 0
        for sound_name, filename in sound_files.items():
            full_path = os.path.join(asset_path, filename)
            try:
                if os.path.exists(full_path):
                    self.sounds[sound_name] = pg.mixer.Sound(full_path)
                    success_count += 1
                    print(f"✓ Carregado: {sound_name} -> {full_path}")
                else:
                    print(f"✗ Arquivo não encontrado: {full_path}")
            except Exception as e:
                print(f"✗ Erro ao carregar {sound_name}: {e}")

        print(f"Carregados {success_count}/{len(sound_files)} sons")
        self._apply_volume_to_all()

    # ========== FUNÇÕES INDIVIDUAIS PARA CADA SOM ==========

    def play_bomber(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som do bomber/explosão."""
        if self.sound_enabled and "bomber" in self.sounds:
            self.sounds["bomber"].play(loops, maxtime, fade_ms)

    def play_gameover(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som de game over."""
        if self.sound_enabled and "gameover" in self.sounds:
            self.sounds["gameover"].play(loops, maxtime, fade_ms)

    def play_intangi(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som de intangibilidade/invencibilidade."""
        if self.sound_enabled and "intangi" in self.sounds:
            self.sounds["intangi"].play(loops, maxtime, fade_ms)

    def play_objectdestroyed(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som de objeto destruído."""
        if self.sound_enabled and "objectdestroyed" in self.sounds:
            self.sounds["objectdestroyed"].play(loops, maxtime, fade_ms)

    def play_ricoche(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som de ricochete."""
        if self.sound_enabled and "ricoche" in self.sounds:
            self.sounds["ricoche"].play(loops, maxtime, fade_ms)

    def play_shield(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som do escudo."""
        if self.sound_enabled and "shield" in self.sounds:
            self.sounds["shield"].play(loops, maxtime, fade_ms)

    def play_shot(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som do tiro."""
        if self.sound_enabled and "shot" in self.sounds:
            self.sounds["shot"].play(loops, maxtime, fade_ms)

    def play_spaceship1(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som da nave espacial."""
        if self.sound_enabled and "spaceship1" in self.sounds:
            self.sounds["spaceship1"].play(loops, maxtime, fade_ms)

    def play_timeresume(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som de retomada do tempo."""
        if self.sound_enabled and "timeresume" in self.sounds:
            self.sounds["timeresume"].play(loops, maxtime, fade_ms)

    def play_timestop(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        """Toca o som de parada do tempo."""
        if self.sound_enabled and "timestop" in self.sounds:
            self.sounds["timestop"].play(loops, maxtime, fade_ms)

    # ========== FUNÇÕES UTILITÁRIAS ==========

    def play_important_sound(self, sound_name: str):
        """Toca um som em canal prioritário."""
        if self.sound_enabled and sound_name in self.sounds and self.important_channel:
            self.important_channel.play(self.sounds[sound_name])

    def stop_sound(self, sound_name: str):
        """Para um som específico."""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()

    def stop_all_sounds(self):
        """Para todos os sons em reprodução."""
        for sound in self.sounds.values():
            sound.stop()
        if self.important_channel:
            self.important_channel.stop()

    def stop_all_except(self, exceptions: list[str]):
        """Para todos os sons, exceto os listados."""
        for sound_name, sound in self.sounds.items():
            if sound_name not in exceptions:
                sound.stop()

    def set_sound_volume(self, sound_name: str, volume: float):
        """Ajusta o volume de um som específico (0.0 a 1.0)."""
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(max(0.0, min(1.0, volume)))

    def set_master_volume(self, volume: float):
        """Ajusta o volume global (0.0 a 1.0)."""
        self.master_volume = max(0.0, min(1.0, volume))
        self._apply_volume_to_all()

    def toggle_sound(self):
        """Liga/desliga todos os sons."""
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            self.stop_all_sounds()

    def _apply_volume_to_all(self):
        """Aplica o volume master a todos os sons carregados."""
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume)

    def is_playing(self, sound_name: str) -> bool:
        """Verifica se algum som está tocando no mixer."""
        if sound_name in self.sounds:
            return pg.mixer.get_busy()
        return False

    def get_sound_duration(self, sound_name: str) -> float:
        """Retorna a duração do som em segundos."""
        if sound_name in self.sounds:
            return self.sounds[sound_name].get_length()
        return 0.0

    def preload_all_sounds(self):
        """Compatibilidade — sons já são carregados no load_sounds()."""
        pass
    
if __name__ == "__main__":
        pg.init()
    
        sound_mgr = SoundManager()
        sound_mgr.load_sounds()  # sem argumento, usa o path automático
    
        print(f"\nSons carregados: {list(sound_mgr.sounds.keys())}")
    
        pg.quit()

    