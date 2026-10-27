from pathlib import Path
from manim import *

# Destino de salvamento na pasta do projeto
config.media_dir = str(Path(__file__).resolve().parent / "media")

# Configuração para formato vertical (TikTok / Shorts / Reels)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0

class ProdutoNotavel(Scene):
    def construct(self):
        # 1. Título e Fórmula no topo
        titulo_pt1 = MathTex("(a+b)^2").scale(1.5)
        titulo_pt2 = MathTex("= a^2 + 2ab + b^2").scale(1.5)
        titulo_completo = VGroup(titulo_pt1, titulo_pt2).arrange(RIGHT).move_to(UP * 4)

        # 2. Definição das medidas
        a = 3.2
        b = 1.4
        
        # Ponto de referência: Topo-Esquerdo (Top-Left) do quadrado maior final
        # Centralizando o desenho na tela
        TL = UP * 1.5 + LEFT * 2.3 

        # ================= PEÇAS E POSIÇÕES =================
        
        # Quadrado A (Sempre no Topo-Esquerdo)
        sq_a = Square(side_length=a, fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE)
        sq_a.move_to(TL + RIGHT*(a/2) + DOWN*(a/2))
        txt_a2 = MathTex("a^2").scale(1.5).move_to(sq_a.get_center())

        # Quadrado B (Posição 1: Nasce do lado direito para apresentação)
        pos_B_start_TL = TL + RIGHT*(a + 0.5) # Um pouco separado do A
        sq_b = Square(side_length=b, fill_color=YELLOW, fill_opacity=0.8, stroke_color=WHITE)
        sq_b.move_to(pos_B_start_TL + RIGHT*(b/2) + DOWN*(b/2))
        txt_b2 = MathTex("b^2").scale(1.2).move_to(sq_b.get_center())

        # Quadrado B (Posição 2: Empilhado embaixo de A para somar a+b)
        pos_B_stacked = TL + DOWN*a + RIGHT*(b/2) + DOWN*(b/2)

        # Quadrado B (Posição 3: Final, deslizado para o canto inferior direito)
        pos_B_final = TL + DOWN*a + RIGHT*a + RIGHT*(b/2) + DOWN*(b/2)

        # Retângulos (Verdes)
        rect_ab = Rectangle(width=b, height=a, fill_color=GREEN, fill_opacity=0.8, stroke_color=WHITE)
        rect_ab.move_to(TL + RIGHT*a + RIGHT*(b/2) + DOWN*(a/2))
        txt_ab1 = MathTex("ab").scale(1.2).move_to(rect_ab.get_center())

        rect_ba = Rectangle(width=a, height=b, fill_color=GREEN, fill_opacity=0.8, stroke_color=WHITE)
        rect_ba.move_to(TL + DOWN*a + RIGHT*(a/2) + DOWN*(b/2))
        txt_ab2 = MathTex("ab").scale(1.2).move_to(rect_ba.get_center())

        # Fronteira do Quadrado Maior
        borda_maior = Square(side_length=a+b, stroke_color=WHITE, stroke_width=4)
        borda_maior.move_to(TL + RIGHT*((a+b)/2) + DOWN*((a+b)/2))

        # ================= CHAVES E TEXTOS (BRACES) =================
        
        brace_top_a = BraceBetweenPoints(TL, TL + RIGHT*a, UP)
        lbl_top_a = brace_top_a.get_text("$a$").scale(1.2)

        brace_top_b_start = BraceBetweenPoints(pos_B_start_TL, pos_B_start_TL + RIGHT*b, UP)
        lbl_top_b_start = brace_top_b_start.get_text("$b$").scale(1.2)

        brace_left_a = BraceBetweenPoints(TL + DOWN*a, TL, LEFT)
        lbl_left_a = brace_left_a.get_text("$a$").scale(1.2)

        brace_left_b = BraceBetweenPoints(TL + DOWN*(a+b), TL + DOWN*a, LEFT)
        lbl_left_b = brace_left_b.get_text("$b$").scale(1.2)

        brace_left_total = BraceBetweenPoints(TL + DOWN*(a+b), TL, LEFT)
        lbl_left_total = brace_left_total.get_text("$a+b$").scale(1.5).set_color(YELLOW)

        brace_top_total = BraceBetweenPoints(TL, TL + RIGHT*(a+b), UP)
        lbl_top_total = brace_top_total.get_text("$a+b$").scale(1.5).set_color(YELLOW)

        # ================= ANIMAÇÕES =================

        # Passo 1: Apresenta os dois quadrados separados com seus lados e áreas
        self.play(Write(titulo_pt1))
        self.play(FadeIn(sq_a), FadeIn(sq_b))
        self.play(
            Create(brace_top_a), Write(lbl_top_a),
            Create(brace_top_b_start), Write(lbl_top_b_start)
        )
        self.play(Write(txt_a2), Write(txt_b2))
        self.wait(1.5)

        # Passo 2: Empilha o quadrado B embaixo do A
        self.play(
            sq_b.animate.move_to(pos_B_stacked),
            txt_b2.animate.move_to(pos_B_stacked),
            FadeOut(brace_top_b_start),
            FadeOut(lbl_top_b_start),
            run_time=1.5
        )
        self.wait(0.5)

        # Passo 3: Mostra que a lateral esquerda agora mede a+b
        self.play(
            Create(brace_left_a), Write(lbl_left_a),
            Create(brace_left_b), Write(lbl_left_b)
        )
        self.wait(1)
        self.play(
            ReplacementTransform(VGroup(brace_left_a, brace_left_b), brace_left_total),
            ReplacementTransform(VGroup(lbl_left_a, lbl_left_b), lbl_left_total)
        )
        self.wait(1)

        # Passo 4: Desenha o quadrado maior baseado no lado a+b
        self.play(
            Create(borda_maior),
            ReplacementTransform(brace_top_a, brace_top_total),
            ReplacementTransform(lbl_top_a, lbl_top_total),
            run_time=1.5
        )
        self.wait(1.5)

        # Passo 5: O movimento mágico - desliza B para o canto inferior direito
        self.play(
            sq_b.animate.move_to(pos_B_final),
            txt_b2.animate.move_to(pos_B_final),
            run_time=1.5
        )
        self.wait(1)

        # Passo 6: Preenche os retângulos verdes que faltam
        self.play(
            FadeIn(rect_ab), Write(txt_ab1),
            FadeIn(rect_ba), Write(txt_ab2),
            run_time=1.5
        )
        self.wait(1)

        # Passo 7: Finaliza completando a fórmula
        self.play(Write(titulo_pt2))
        self.play(titulo_completo.animate.scale(1.1), run_time=0.5)
        self.play(titulo_completo.animate.scale(1/1.1), run_time=0.5)
        self.wait(3.5)