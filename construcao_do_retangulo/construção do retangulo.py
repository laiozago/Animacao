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

# O Fundo Branco e linhas limpas para igualar a folha de prova
config.background_color = WHITE

class RetanguloPrata(Scene):
    def construct(self):
        # 1. Escala e ajuste para ficar bem centralizado no celular
        l = 3.2
        shift_vec = LEFT * 0.66 + DOWN * 1.6
        
        # Vértices exatos baseados na geometria da questão
        A = np.array([-l, l, 0]) + shift_vec
        B = np.array([-l, 0, 0]) + shift_vec
        C = np.array([0, 0, 0]) + shift_vec
        D = np.array([0, l, 0]) + shift_vec
        E = np.array([l * np.sqrt(2), 0, 0]) + shift_vec
        F = np.array([l * np.sqrt(2), l, 0]) + shift_vec
        G = np.array([l, l, 0]) + shift_vec
        H = np.array([l, 0, 0]) + shift_vec
        
        # Título
        titulo = Tex("Retângulo de Prata", color=BLACK).scale(1.5).move_to(UP * 6)
        self.play(Write(titulo))
        
        # 2. Construir o Quadrado 1 (ABCD)
        sq_ABCD = Polygon(A, B, C, D, color=BLACK, stroke_width=5)
        
        labels_ABCD = VGroup(
            Tex("A", color=BLACK).scale(1.2).next_to(A, UL, buff=0.1),
            Tex("B", color=BLACK).scale(1.2).next_to(B, DL, buff=0.1),
            Tex("C", color=BLACK).scale(1.2).next_to(C, DOWN, buff=0.1),
            Tex("D", color=BLACK).scale(1.2).next_to(D, UP, buff=0.1)
        )
        
        lbl_l1 = MathTex("l", color=BLACK).scale(1.3).next_to(Line(B, A).get_center(), LEFT, buff=0.2)
        lbl_l2 = MathTex("l", color=BLACK).scale(1.3).next_to(Line(B, C).get_center(), DOWN, buff=0.2)
        
        self.play(Create(sq_ABCD), run_time=1.5)
        self.play(Write(labels_ABCD), Write(lbl_l1), Write(lbl_l2))
        self.wait(1)
        
        # 3. Traçar a Diagonal AC (Com a sua cor vermelha)
        diag_AC = Line(A, C, color=RED, stroke_width=8)
        lbl_diag = MathTex(r"l\sqrt{2}", color=RED).scale(1.3).move_to(diag_AC.get_center() + UR * 0.4)
        
        self.play(Create(diag_AC))
        self.play(Write(lbl_diag))
        self.wait(1)
        
        # 4. Rotacionar a Diagonal e Formar o Arco Dotted
        arc = DashedVMobject(Arc(
            radius=l*np.sqrt(2), 
            arc_center=C, 
            start_angle=3*PI/4, 
            angle=-3*PI/4, 
            color=GRAY, 
            stroke_width=4
        ))
        
        diag_moving = diag_AC.copy()
        
        # A diagonal gira no exato compasso em que a linha pontilhada nasce
        self.play(
            Create(arc, rate_func=linear),
            Rotate(diag_moving, angle=-3*PI/4, about_point=C, rate_func=linear),
            run_time=2
        )
        self.wait(0.5)
        
        # 5. Fechar o Grande Retângulo (ABEF)
        line_CE = Line(C, E, color=BLACK, stroke_width=5)
        line_EF = Line(E, F, color=BLACK, stroke_width=5)
        line_DF = Line(D, F, color=BLACK, stroke_width=5)
        
        labels_EF = VGroup(
            Tex("E", color=BLACK).scale(1.2).next_to(E, DR, buff=0.1),
            Tex("F", color=BLACK).scale(1.2).next_to(F, UR, buff=0.1)
        )
        
        self.play(Create(line_CE), Create(line_EF), Create(line_DF))
        self.play(Write(labels_EF))
        
        # A diagonal viva some e vira a medida preta estática no chão
        lbl_CE = MathTex(r"l\sqrt{2}", color=BLACK).scale(1.3).next_to(line_CE.get_center(), DOWN, buff=0.2)
        self.play(
            FadeOut(diag_moving), 
            FadeOut(lbl_diag),
            Write(lbl_CE)
        )
        self.wait(1)
        
        # 6. MÁGICA: Rotacionar as linhas do quadrado para provar a formação de CDGH
        # Destaco a linha CD do meio (em azul para o aluno perceber a ação)
        line_CD = Line(C, D, color=BLUE, stroke_width=8)
        self.play(Create(line_CD))
        self.wait(0.5)
        
        # Copio a linha central e rodo ela pras laterais, como se deitasse ela
        line_CH = line_CD.copy()
        line_DG = line_CD.copy()
        
        self.play(
            Rotate(line_CH, angle=-PI/2, about_point=C),
            Rotate(line_DG, angle=PI/2, about_point=D),
            run_time=1.5
        )
        
        # Fecho o novo quadrado com a lateral azul também
        line_GH = Line(G, H, color=BLUE, stroke_width=8)
        labels_GH = VGroup(
            Tex("G", color=BLACK).scale(1.2).next_to(G, UP, buff=0.1),
            Tex("H", color=BLACK).scale(1.2).next_to(H, DOWN, buff=0.1)
        )
        self.play(Create(line_GH))
        self.play(Write(labels_GH))
        
        # Confirma as medidas "l" do novo quadrado
        lbl_l3 = MathTex("l", color=BLUE).scale(1.3).next_to(line_DG.get_center(), UP, buff=0.2)
        self.play(Write(lbl_l3))
        self.wait(1)
        
        # 7. Região Amarela (Retângulo EFGH)
        rect_EFGH = Polygon(H, E, F, G, fill_color="#F2A63A", fill_opacity=0.8, color=BLACK, stroke_width=5)
        
        # O rectângulo sobe. Para ele não encobrir as letras que estão no chão, trago elas pra frente
        self.play(
            FadeIn(rect_EFGH),
            labels_EF.animate.set_z_index(10),
            labels_GH.animate.set_z_index(10)
        )
        self.wait(1)
        
        # 8. Chave e resultado final das suas anotações
        brace = BraceBetweenPoints(H, E, direction=DOWN, color=BLACK).shift(DOWN * 0.3)
        lbl_brace = brace.get_tex(r"l\sqrt{2} - l").scale(1.2).set_color(BLACK)
        
        self.play(Create(brace), Write(lbl_brace))
        self.wait(3)