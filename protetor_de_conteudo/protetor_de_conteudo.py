from pathlib import Path
from manim import *
import numpy as np

# Destino de salvamento na pasta do projeto
config.media_dir = str(Path(__file__).resolve().parent / "media")

# Configuração para formato vertical
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0

# A MÁGICA AQUI: Fundo 100% transparente
config.transparent = True

class MarcaAguaQuicando(Scene):
    def construct(self):
        # Visual elegante: branco com leve cinza e opacidade de 30%
        marca_agua = Text("@proflaiozago", font="Arial", weight=BOLD).scale(0.68).set_color(WHITE).set_opacity(0.30)

        # Movimento orgânico e delicado, perfeito para loop contínuo
        centro = np.array([0.0, 1.8, 0.0])
        amplitudes = np.array([3.3, 1.9, 0.0])
        frequencias = np.array([1.0, 1.6, 0.0])
        fase = 0.0

        def update_marca(mob, dt):
            nonlocal fase
            fase += dt * 1.5

            x = centro[0] + amplitudes[0] * np.sin(fase * frequencias[0])
            y = centro[1] + amplitudes[1] * np.sin(fase * frequencias[1] + 0.75)
            mob.move_to([x, y, 0])

        marca_agua.add_updater(update_marca)
        self.add(marca_agua)

        # Loop curto e fluido para reprodução contínua
        self.wait(6)