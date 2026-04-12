import src.config.server as SERVER


class WaveSystem:
    def __init__(self, engine):
        self.engine = engine
        self.wave_count = 0
        self.wave_timer = SERVER.WAVE_DELAY

    def update(self, dt):
        # Filtra asteroides ativos
        asteroids = [e for e in self.engine.entities if e.type == "ASTEROID"]

        if not asteroids:
            if self.wave_timer <= 0:
                self._start_next_wave()
                self.wave_timer = SERVER.WAVE_DELAY
            else:
                self.wave_timer -= dt

    def _start_next_wave(self):
        self.wave_count += 1
        num_asteroids = 3 + self.wave_count
        ship = next((e for e in self.engine.entities if e.type == "SHIP"), None)

        if ship:
            self.engine.spawner.generate_random_asteroid_wave(num_asteroids, ship.pos)
