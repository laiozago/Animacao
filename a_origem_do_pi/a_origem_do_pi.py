from pathlib import Path
from manim import *
import numpy as np

# Destino de salvamento na pasta do projeto
config.media_dir = str(Path(__file__).resolve().parent / "media")

# Configuração para formato vertical (TikTok / Shorts / Reels)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0

class OrigemDoPi(Scene):
    def construct(self):
        # 1. Título no topo (subiu mais para dar espaço)
        titulo = Tex("De onde vem o $\pi$?").scale(1.5).move_to(UP * 6)
        
        # 2. Geometria Base (Raio reduzido e círculo mais baixo)
        R = 2.8  # Era 3.2
        centro_pos = DOWN * 2.5  # Desceu mais para liberar o topo
        
        circle = Circle(radius=R, color=WHITE, stroke_opacity=0.3).move_to(centro_pos)
        center = Dot(centro_pos)
        
        # Linha pontilhada de referência (Diâmetro / 180 graus)
        diam_line = DashedLine(centro_pos + LEFT * R, centro_pos + RIGHT * R, color=GRAY, stroke_opacity=0.5)
        
        # O Raio original (linha reta)
        raio_line = Line(centro_pos, centro_pos + RIGHT * R, color=YELLOW, stroke_width=8)
        txt_r = MathTex("r").scale(1.5).next_to(raio_line, DOWN, buff=0.3)
        
        # 3. Os Arcos (Os "Raios Curvados")
        arc1 = Arc(radius=R, start_angle=0, angle=1, color=RED, stroke_width=10, arc_center=centro_pos)
        arc2 = Arc(radius=R, start_angle=1, angle=1, color=GREEN, stroke_width=10, arc_center=centro_pos)
        arc3 = Arc(radius=R, start_angle=2, angle=1, color=BLUE, stroke_width=10, arc_center=centro_pos)
        
        # A "Gordurinha" final 
        arc_gap = Arc(radius=R, start_angle=3, angle=PI-3, color=PURPLE, stroke_width=10, arc_center=centro_pos)
        
        # 4. Textos dos Arcos
        def pos_texto(angulo, offset=1.2):
            cx, cy, _ = centro_pos
            return np.array([
                cx + R * offset * np.cos(angulo),
                cy + R * offset * np.sin(angulo),
                0
            ])

        lbl_arc1 = MathTex("1r").move_to(pos_texto(0.5)).set_color(RED).scale(1.3)
        lbl_arc2 = MathTex("2r").move_to(pos_texto(1.5)).set_color(GREEN).scale(1.3)
        lbl_arc3 = MathTex("3r").move_to(pos_texto(2.5)).set_color(BLUE).scale(1.3)
        
        # Novo posicionamento seguro para o 0,14 não sair da tela
        lbl_gap = MathTex("0,14...").scale(0.9).set_color(PURPLE)
        lbl_gap.next_to(arc_gap, LEFT, buff=0.15).shift(UP * 0.3)

        # ================= ANIMAÇÕES =================
        
        self.play(Write(titulo))
        self.play(Create(circle), Create(center), Create(diam_line))
        
        self.play(Create(raio_line), Write(txt_r))
        self.wait(1)
        
        self.play(TransformFromCopy(raio_line, arc1), run_time=1.5)
        self.play(Write(lbl_arc1))
        self.wait(0.5)
        
        self.play(TransformFromCopy(raio_line, arc2), run_time=1.5)
        self.play(Write(lbl_arc2))
        self.wait(0.5)
        
        self.play(TransformFromCopy(raio_line, arc3), run_time=1.5)
        self.play(Write(lbl_arc3))
        self.wait(1)
        
        self.play(Create(arc_gap), run_time=1)
        self.play(Write(lbl_gap))
        self.wait(1.5)
        
        # 5. Conclusão Matemática (Textos reposicionados e encurtados)
        conc1 = MathTex(r"\text{Meia Volta} = 3,14... \times r").scale(1.2).move_to(UP * 3.5)
        conc2 = MathTex(r"\text{Meia Volta} = \pi \times r").scale(1.3).move_to(UP * 3.5).set_color(YELLOW)
        
        # Volta completa formatada para tela vertical (sem estourar as laterais)
        conc3 = MathTex(r"\text{Volta Completa } (C) = 2\pi r").scale(1.3).move_to(UP * 1.5).set_color(GREEN)
        
        self.play(Write(conc1))
        self.wait(1.5)
        
        self.play(ReplacementTransform(conc1, conc2))
        self.wait(1)
        
        self.play(Write(conc3))
        self.play(conc3.animate.scale(1.1), run_time=0.5)
        self.play(conc3.animate.scale(1/1.1), run_time=0.5)
        self.wait(4)