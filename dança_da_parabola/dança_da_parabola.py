from pathlib import Path
from manim import *

# Destino de salvamento na pasta do projeto
config.media_dir = str(Path(__file__).resolve().parent / "media")

# Configuração para formato vertical (TikTok / Shorts / Reels)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0

class DancaParabola(Scene):
    def construct(self):
        titulo = Tex("A Dança da Parábola").scale(1.5).move_to(UP * 6)

        ax = Axes(
            x_range=[-5, 5, 1],
            y_range=[-8, 8, 2],
            x_length=8,
            y_length=9,
            axis_config={"color": WHITE, "include_numbers": False},
        ).shift(DOWN * 0.5)
        
        labels = ax.get_axis_labels(x_label="x", y_label="y")

        # Trackers dos três coeficientes
        a_tracker = ValueTracker(1.0)
        b_tracker = ValueTracker(0.0)
        c_tracker = ValueTracker(0.0)

        # Gráfico dinâmico
        def get_parabola():
            a = a_tracker.get_value()
            b = b_tracker.get_value()
            c = c_tracker.get_value()
            return ax.plot(lambda x: a * x**2 + b * x + c, color=YELLOW, x_range=[-4, 4])

        parabola = always_redraw(get_parabola)

        # Equação dinâmica no topo com os 3 coeficientes
        def get_equation():
            a = a_tracker.get_value()
            b = b_tracker.get_value()
            c = c_tracker.get_value()
            
            sinal_b = "+" if b >= 0 else "-"
            sinal_c = "+" if c >= 0 else "-"
            
            # y = [a]x^2 [+/- b]x [+/- c]
            eq = MathTex(
                "y = ", 
                f"{a:.1f}", "x^2 ", 
                f"{sinal_b} {abs(b):.1f}", "x ", 
                f"{sinal_c} {abs(c):.1f}"
            ).scale(1.3).next_to(titulo, DOWN, buff=0.5)
            
            eq[1].set_color(BLUE)   # Coeficiente a
            eq[3].set_color(RED)    # Coeficiente b
            eq[5].set_color(GREEN)  # Coeficiente c
            return eq

        equation = always_redraw(get_equation)
        
        # Textos Explicativos
        exp_a = Tex("O coeficiente ", "$a$", " controla a abertura!").scale(1.2).move_to(DOWN * 6.5)
        exp_a[1].set_color(BLUE)
        exp_a2 = Tex("Ficou negativo? Inverte a concavidade!").scale(1.1).move_to(DOWN * 6.5).set_color(BLUE)
        
        exp_b = Tex("O ", "$b$", " inclina o corte no eixo Y!").scale(1.2).move_to(DOWN * 6.5)
        exp_b[1].set_color(RED)
        
        exp_c = Tex("O coeficiente ", "$c$", " é o elevador!").scale(1.2).move_to(DOWN * 6.5)
        exp_c[1].set_color(GREEN)

        # ================= ANIMAÇÕES =================
        
        self.play(Write(titulo))
        self.play(Create(ax), Create(labels))
        self.play(Create(parabola), Write(equation))
        self.wait(1)

        # --- A DANÇA DO 'A' ---
        self.play(Write(exp_a))
        self.play(a_tracker.animate.set_value(3.0), run_time=1.5)
        self.play(a_tracker.animate.set_value(0.2), run_time=1.5)
        
        self.play(Transform(exp_a, exp_a2))
        self.play(a_tracker.animate.set_value(-2.0), run_time=1.5)
        
        self.play(FadeOut(exp_a))
        self.play(a_tracker.animate.set_value(1.0), run_time=1)
        self.wait(0.5)

        # --- A DANÇA DO 'B' (A Novidade!) ---
        self.play(Write(exp_b))
        # b positivo (corta subindo, vai pra esquerda)
        self.play(b_tracker.animate.set_value(3.0), run_time=1.5)
        # b negativo (corta descendo, vai pra direita)
        self.play(b_tracker.animate.set_value(-3.0), run_time=2)
        
        self.play(FadeOut(exp_b))
        self.play(b_tracker.animate.set_value(0.0), run_time=1)
        self.wait(0.5)

        # --- A DANÇA DO 'C' ---
        self.play(Write(exp_c))
        self.play(c_tracker.animate.set_value(5.0), run_time=1.5)
        self.play(c_tracker.animate.set_value(-4.0), run_time=1.5)
        
        self.play(FadeOut(exp_c))
        self.play(c_tracker.animate.set_value(0.0), run_time=1)

        # Encerramento
        final_text = Tex("Matemática é visual. Salve para revisar!").scale(1).move_to(DOWN * 6.5).set_color(YELLOW)
        self.play(Write(final_text))
        self.wait(3)