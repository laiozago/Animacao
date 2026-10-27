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

class AreaCirculoCebola(Scene):
    def construct(self):
        # 1. Título isolado no topo
        titulo = Tex("A Área do Círculo").scale(1.3).move_to(UP * 6.5)
        
        # 2. Configuração dos Anéis (Subiu para UP * 4.5)
        R = 1.8
        n_rings = 18 # Aumentado para garantir o pontinho no topo do triângulo
        
        colors = color_gradient(["#001C44", "#0055CC", "#00AAFF", "#00E5FF"], n_rings)
        radii = np.linspace(0.01, R, n_rings) # Começa em 0.01 para o "bico" perfeito
        
        circles = VGroup()
        for i, r in enumerate(radii):
            ring = Circle(radius=r, color=colors[i], stroke_width=8).move_to(UP * 4.5)
            circles.add(ring)

        # O Raio Amarelo original (A referência de altura)
        radius_line_circle = Line(circles.get_center(), circles.get_center() + DOWN * R, color=YELLOW, stroke_width=6)
        txt_r_circle = MathTex("r").scale(1.2).next_to(radius_line_circle, RIGHT, buff=0.2).set_color(YELLOW)
            
        # 3. Mapeamento das posições para o Triângulo (Subiu para liberar o rodapé)
        w_max = 6.0  
        h_max = 3.5  
        tri_base_y = -1.0  # Base do triângulo bem mais alta
        x_left = -w_max / 2
        
        lines = VGroup()
        for i, r in enumerate(radii):
            length = w_max * (r / R)
            y = tri_base_y + h_max * ((R - r) / R)
            
            # A marcação amarela da "tampinha" à esquerda
            tip_len = 0.1
            if length < tip_len: 
                tip_len = length # Evita que o pontinho passe do tamanho da linha
                
            tip = Line([x_left, y, 0], [x_left + tip_len, y, 0], color=YELLOW, stroke_width=9)
            main_line = Line([x_left + tip_len, y, 0], [x_left + length, y, 0], color=colors[i], stroke_width=9)
            
            lines.add(VGroup(tip, main_line))

        # ================= ANIMAÇÕES =================
        
        # Apresentação do Círculo com o Raio Amarelo
        self.play(Write(titulo))
        self.play(FadeIn(circles, lag_ratio=0.03), run_time=1.5)
        self.play(Create(radius_line_circle), Write(txt_r_circle))
        self.wait(1)
        
        # --- TRANSIÇÃO PARA O TRIÂNGULO ---
        
        # 1ª Casca (A Base)
        self.play(circles[-1].animate.set_color(YELLOW).set_stroke(width=10), run_time=0.4)
        self.play(ReplacementTransform(circles[-1], lines[-1]), run_time=0.8)
        
        # 2ª Casca
        self.play(circles[-2].animate.set_color(YELLOW).set_stroke(width=10), run_time=0.3)
        self.play(ReplacementTransform(circles[-2], lines[-2]), run_time=0.7)
        
        # 3ª Casca
        self.play(circles[-3].animate.set_color(YELLOW).set_stroke(width=10), run_time=0.3)
        self.play(ReplacementTransform(circles[-3], lines[-3]), run_time=0.6)
        
        # O resto chovendo em cascata
        rest_of_rings = reversed(range(n_rings - 3))
        animations = [ReplacementTransform(circles[i], lines[i]) for i in rest_of_rings]
        self.play(AnimationGroup(*animations, lag_ratio=0.08), run_time=2.5)
        
        # Move o Raio original para provar a altura
        self.play(FadeOut(txt_r_circle))
        target_radius = Line([x_left, tri_base_y + h_max, 0], [x_left, tri_base_y, 0], color=YELLOW, stroke_width=6)
        self.play(Transform(radius_line_circle, target_radius), run_time=1.5)
        
        # Dimensionando o Triângulo
        brace_base = Brace(lines, DOWN, buff=0.15)
        txt_base = brace_base.get_text("$2\pi r$").scale(1.1).set_color(YELLOW)
        txt_altura = MathTex("r").scale(1.2).next_to(target_radius, LEFT, buff=0.2).set_color(YELLOW)
        
        self.play(Create(brace_base), Write(txt_base))
        self.play(Write(txt_altura))
        self.wait(1)
        
        # ================= CONTAS E CORTES (CASCATA) =================
        
        # Passo 1: Fórmula base
        eq_base = MathTex(r"A = \frac{\text{base} \times \text{altura}}{2}").scale(0.95).move_to(DOWN * 2.5)
        self.play(Write(eq_base))
        self.wait(1)
        
        # Construção minuciosa da fração para podermos cortar os números 2 sem erro
        num_2 = MathTex("2").scale(1.2)
        num_rest = MathTex(r"\pi r \times r").scale(1.2)
        num = VGroup(num_2, num_rest).arrange(RIGHT, buff=0.1)
        den = MathTex("2").scale(1.2)
        frac_bar = Line(num.get_corner(DL) + DOWN*0.1, num.get_corner(DR) + DOWN*0.1, stroke_width=3)
        den.next_to(frac_bar, DOWN, buff=0.1)
        
        frac = VGroup(num, frac_bar, den)
        eq_subst = VGroup(MathTex("A = ").scale(1.2), frac).arrange(RIGHT, buff=0.2).move_to(DOWN * 4.5)
        
        # Passo 2: Substituição na tela (Sem apagar a primeira)
        self.play(Write(eq_subst))
        self.wait(1)
        
        # Passo 3: Corta os números 2 na tela
        cross1 = Cross(num_2, stroke_color=RED, stroke_width=6)
        cross2 = Cross(den, stroke_color=RED, stroke_width=6)
        self.play(Create(cross1), Create(cross2))
        self.wait(1)
        
        # Passo 4: O grande final com o Pi R quadrado
        eq_final = MathTex(r"A = \pi r^2").scale(1.6).move_to(DOWN * 6.5).set_color(GREEN)
        self.play(Write(eq_final))
        self.play(eq_final.animate.scale(1.15), run_time=0.5)
        self.play(eq_final.animate.scale(1/1.15), run_time=0.5)
        self.wait(3.5)