# ASTEROIDE SINGLEPLAYER v1.0
# This file starts the application and launches the main game loop.
from src.game import Game

if __name__ == "__main__":
    app = Game(cap="Asteroids Pygame - 2.0")
    app.run()
