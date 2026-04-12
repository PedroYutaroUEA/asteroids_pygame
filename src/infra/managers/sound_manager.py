import pygame as pg


class SoundManager:
    """
    Gerenciador de execução de áudio.
    Controla volumes globais e canais de reprodução.
    """

    def __init__(self, assets):
        self.assets = assets
        self.channels = {}  # Para rastrear sons em loop (thrust, ufo)

    def play_sfx(self, key, volume=1.0, loops=0):
        sound = self.assets.get_sound(key)
        if sound:
            sound.set_volume(volume)
            return sound.play(loops=loops)
        return None

    def start_loop(self, key, name, volume=0.5):
        """Inicia um som em loop e guarda a referência para parar depois."""
        if name not in self.channels:
            sound = self.assets.get_sound(key)
            if sound:
                sound.set_volume(volume)
                channel = sound.play(loops=-1)
                self.channels[name] = sound

    def stop_loop(self, name):
        """Para um som em loop específico."""
        if name in self.channels:
            self.channels[name].stop()
            del self.channels[name]

    def stop_all(self):
        """Para absolutamente todos os sons (útil em transições de cena)."""
        pg.mixer.stop()
        self.channels.clear()
