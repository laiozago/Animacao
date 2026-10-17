from manim import *
import numpy as np

class ResolucaoPiramide(ThreeDScene):
    def __init__(self, *args, **kwargs):
        config.frame_width = config.frame_height * config.pixel_width / config.pixel_height
        super().__init__(*args, **kwargs)

    def construct(self):
        vertical = config.pixel_height > config.pixel_width

        # --------------------------------------------------
        # 1. Configurações Globais
        # --------------------------------------------------
        self.camera.background_color = WHITE
        cor_aresta = BLACK
        cor_aresta_oculta = GRAY
        cor_trajeto = ORANGE

        # --------------------------------------------------
        # 2. Coordenadas Matemáticas (3D e 2D)
        # --------------------------------------------------
        a = 4  # Aresta
        h = a / np.sqrt(2) # Altura da pirâmide

        # Pontos em 3D
        E_3 = np.array([0, 0, h])
        A_3 = np.array([-a/2, -a/2, 0])
        B_3 = np.array([a/2, -a/2, 0])
        C_3 = np.array([a/2, a/2, 0])
        D_3 = np.array([-a/2, a/2, 0])
        F_3 = (B_3 + E_3) / 2

        # Pontos em 2D (Deslocados para centralizar)
        offset = np.array([-1.5, 0, 0])
        E_2 = np.array([0, 0, 0]) + offset

        # Faces Laterais em leque ao redor de E
        B_2  = E_2 + a * np.array([np.cos(270 * DEGREES), np.sin(270 * DEGREES), 0])
        C_2  = E_2 + a * np.array([np.cos(330 * DEGREES), np.sin(330 * DEGREES), 0])
        D_2  = E_2 + a * np.array([np.cos(30 * DEGREES), np.sin(30 * DEGREES), 0])
        A1_2 = E_2 + a * np.array([np.cos(210 * DEGREES), np.sin(210 * DEGREES), 0])
        A2_2 = E_2 + a * np.array([np.cos(90 * DEGREES), np.sin(90 * DEGREES), 0])

        # Base Quadrada (Acoplada à aresta CD)
        A_base_2 = D_2 + np.array([a, 0, 0])
        B_base_2 = C_2 + np.array([a, 0, 0])

        centro_planificacao = np.array([offset[0] + a / 2, 0, 0])

        def ajustar_ponto_2d(ponto):
            ponto = ponto - centro_planificacao
            if vertical:
                ponto = np.array([ponto[1], -ponto[0], ponto[2]]) * 0.43
            return ponto

        E_2, B_2, C_2, D_2, A1_2, A2_2, A_base_2, B_base_2 = (
            ajustar_ponto_2d(ponto)
            for ponto in (E_2, B_2, C_2, D_2, A1_2, A2_2, A_base_2, B_base_2)
        )

        def ajustar_direcao_texto(direcao):
            if vertical:
                return np.array([direcao[1], -direcao[0], direcao[2]])
            return direcao

        # --------------------------------------------------
        # 3. Interpolador Suave (ValueTracker) para o Morphing
        # --------------------------------------------------
        t = ValueTracker(0)

        def get_pt(p3, p2):
            return p3 * (1 - t.get_value()) + p2 * t.get_value()

        p_E = lambda: get_pt(E_3, E_2)
        p_B = lambda: get_pt(B_3, B_2)
        p_C = lambda: get_pt(C_3, C_2)
        p_D = lambda: get_pt(D_3, D_2)
        p_A1 = lambda: get_pt(A_3, A1_2)
        p_A2 = lambda: get_pt(A_3, A2_2)
        p_Abase = lambda: get_pt(A_3, A_base_2)
        p_Bbase = lambda: get_pt(B_3, B_base_2)
        p_F = lambda: (p_E() + p_B()) / 2

        # --------------------------------------------------
        # 4. Construção da Pirâmide 3D Inicial
        # --------------------------------------------------
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-60 * DEGREES,
            zoom=0.7 if vertical else 1,
        )

        l_AB_est = Line3D(A_3, B_3, color=cor_aresta)
        l_BC_est = Line3D(B_3, C_3, color=cor_aresta)
        l_EA_est = Line3D(E_3, A_3, color=cor_aresta)
        l_EB_est = Line3D(E_3, B_3, color=cor_aresta)
        l_EC_est = Line3D(E_3, C_3, color=cor_aresta)

        l_AD_est = DashedLine(A_3, D_3, color=cor_aresta_oculta)
        l_DC_est = DashedLine(D_3, C_3, color=cor_aresta_oculta)
        l_ED_est = DashedLine(E_3, D_3, color=cor_aresta_oculta)

        grupo_3d_estatico = VGroup(l_AB_est, l_BC_est, l_EA_est, l_EB_est, l_EC_est, l_AD_est, l_DC_est, l_ED_est)
        self.play(Create(grupo_3d_estatico), run_time=2)

        # Animação segura do ponto percorrendo o trajeto 3D
        ponto = Dot3D(A_3, color=cor_aresta, radius=0.08)
        self.play(FadeIn(ponto))

        # Trajeto AF
        t_af = ValueTracker(0)
        ponto.add_updater(lambda m: m.move_to(A_3 * (1 - t_af.get_value()) + F_3 * t_af.get_value()))
        trajeto_AF_est = Line3D(A_3, F_3, color=cor_trajeto, stroke_width=5)
        self.play(
            Create(trajeto_AF_est),
            t_af.animate.set_value(1),
            run_time=1.5,
            rate_func=linear,
        )
        ponto.clear_updaters()

        # Trajeto FC
        t_fc = ValueTracker(0)
        ponto.add_updater(lambda m: m.move_to(F_3 * (1 - t_fc.get_value()) + C_3 * t_fc.get_value()))
        trajeto_FC_est = Line3D(F_3, C_3, color=cor_trajeto, stroke_width=5)
        self.play(
            Create(trajeto_FC_est),
            t_fc.animate.set_value(1),
            run_time=1.5,
            rate_func=linear,
        )
        ponto.clear_updaters()
        self.wait(1)

        # --------------------------------------------------
        # 5. A Mágica do Morphing (De 3D para 2D)
        # --------------------------------------------------
        linhas_dinamicas = always_redraw(lambda: VGroup(
            Line(p_E(), p_A1(), color=cor_aresta),
            Line(p_E(), p_B(), color=cor_aresta),
            Line(p_E(), p_C(), color=cor_aresta),
            Line(p_E(), p_D(), color=cor_aresta),
            Line(p_E(), p_A2(), color=cor_aresta),
            Line(p_A1(), p_B(), color=cor_aresta),
            Line(p_B(), p_C(), color=cor_aresta),
            Line(p_C(), p_D(), color=cor_aresta),
            Line(p_D(), p_A2(), color=cor_aresta),
            Line(p_D(), p_Abase(), color=cor_aresta),
            Line(p_C(), p_Bbase(), color=cor_aresta),
            Line(p_Abase(), p_Bbase(), color=cor_aresta)
        ))

        trajeto_dinamico = always_redraw(lambda: VGroup(
            Line(p_A1(), p_F(), color=cor_trajeto, stroke_width=5),
            Line(p_F(), p_C(), color=cor_trajeto, stroke_width=5)
        ))

        ponto_dinamico = always_redraw(lambda: Dot3D(p_C(), color=cor_aresta, radius=0.08))

        self.add(linhas_dinamicas, trajeto_dinamico, ponto_dinamico)
        self.remove(grupo_3d_estatico, trajeto_AF_est, trajeto_FC_est, ponto)

        # Sincroniza o desdobramento com a rotação da câmara.
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            added_anims=[t.animate.set_value(1)],
            run_time=4,
            rate_func=smooth,
        )
        self.wait(1)

        # --------------------------------------------------
        # 6. Destaque do Triângulo Final e Rótulos
        # --------------------------------------------------
        lbl_A1 = Tex("A", color=cor_aresta).next_to(
            A1_2, ajustar_direcao_texto(LEFT)
        )
        lbl_E = Tex("E", color=cor_aresta).next_to(
            E_2, ajustar_direcao_texto(UP)
        )
        lbl_C = Tex("C", color=cor_aresta).next_to(
            C_2, LEFT if vertical else RIGHT
        )
        lbl_F = Tex("F", color=cor_aresta).next_to(
            (E_2 + B_2) / 2,
            UP + LEFT if vertical else UP + RIGHT,
            buff=0.1,
        )

        self.play(FadeIn(lbl_A1, lbl_E, lbl_C, lbl_F))

        triangulo_AEC = Polygon(
            A1_2, E_2, C_2,
            stroke_color=YELLOW_D, stroke_width=4,
            fill_color=YELLOW, fill_opacity=0.3
        )
        self.play(Create(triangulo_AEC))

        valor_AC = MathTex("2\\sqrt{3} \\text{ cm}", color=cor_aresta)
        if vertical:
            valor_AC.scale(0.55)
        valor_AC.next_to(
            Line(A1_2, C_2),
            ajustar_direcao_texto(DOWN),
            buff=0.55 if vertical else 0.2,
        )
        if vertical:
            valor_AC.shift(UP * 0.7)
        aresta_txt_E = Tex("aresta", color=cor_aresta).next_to(
            Line(A1_2, E_2).get_center(),
            ajustar_direcao_texto(UP + LEFT),
            buff=0.1,
        ).scale(0.7)
        aresta_txt_D = Tex("aresta", color=cor_aresta).next_to(
            Line(C_2, E_2).get_center(),
            ajustar_direcao_texto(UP + RIGHT),
            buff=0.1,
        ).scale(0.7)

        self.play(Write(valor_AC))
        self.play(Write(aresta_txt_E), Write(aresta_txt_D))
        self.wait(4)