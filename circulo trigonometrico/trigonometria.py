from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8
config.frame_width = config.frame_height * config.pixel_width / config.pixel_height


class SenoCossenoAnimacao(Scene):
    def construct(self):
        # --------------------------------------------------
        # 1. Configuração vertical: círculo acima, gráfico abaixo
        # --------------------------------------------------
        eixos_circulo = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=3.3,
            y_length=3.3,
            tips=False,
        ).shift(UP * 2.1)
        
        # O raio visual do círculo no sistema de coordenadas
        raio_circulo = eixos_circulo.c2p(1, 0)[0] - eixos_circulo.c2p(0, 0)[0]
        circulo = Circle(radius=raio_circulo, color=WHITE).move_to(eixos_circulo.c2p(0, 0))
        
        eixos_grafico = Axes(
            x_range=[0, 2 * PI + 0.5, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=3.6,
            y_length=2,
            tips=False,
        ).shift(DOWN * 2)

        self.play(Create(eixos_circulo), Create(circulo), Create(eixos_grafico))

        # --------------------------------------------------
        # 2. Adicionando Marcações (0, pi/2, pi, 3pi/2, 2pi)
        # --------------------------------------------------
        escala_label = 0.42
        
        # Labels do Círculo
        labels_circ = VGroup(
            MathTex("0", " / 2\\pi").next_to(eixos_circulo.c2p(1, 0), DOWN+RIGHT).scale(escala_label),
            MathTex("\\frac{\\pi}{2}").next_to(eixos_circulo.c2p(0, 1), UP).scale(escala_label),
            MathTex("\\pi").next_to(eixos_circulo.c2p(-1, 0), LEFT).scale(escala_label),
            MathTex("\\frac{3\\pi}{2}").next_to(eixos_circulo.c2p(0, -1), DOWN).scale(escala_label)
        )

        # Labels do Gráfico
        valores_x = [PI/2, PI, 3*PI/2, 2*PI]
        textos_x = ["\\frac{\\pi}{2}", "\\pi", "\\frac{3\\pi}{2}", "2\\pi"]
        labels_graf = VGroup(MathTex("0").next_to(eixos_grafico.c2p(0, 0), DOWN+RIGHT, buff=0.1).scale(escala_label))
        
        for val, tex in zip(valores_x, textos_x):
            labels_graf.add(MathTex(tex).scale(escala_label).next_to(eixos_grafico.c2p(val, 0), DOWN))

        self.play(FadeIn(labels_circ), FadeIn(labels_graf))

        # --------------------------------------------------
        # 3. Elementos Base: Raio, Ponto e Eixo Colorido
        # --------------------------------------------------
        theta = ValueTracker(0)

        raio = always_redraw(lambda: Line(
            start=eixos_circulo.c2p(0, 0),
            end=eixos_circulo.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())),
            color=YELLOW
        ))

        ponto_circulo = always_redraw(lambda: Dot(
            eixos_circulo.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())), 
            color=WHITE
        ))

        # Colore o eixo X do gráfico enquanto o ângulo cresce
        eixo_x_colorido = always_redraw(lambda: Line(
            start=eixos_grafico.c2p(0, 0),
            end=eixos_grafico.c2p(theta.get_value(), 0),
            color=YELLOW,
            stroke_width=6
        ))

        self.add(raio, ponto_circulo, eixo_x_colorido)

        # --------------------------------------------------
        # 4. Primeira Volta: Foco no Seno (Azul)
        # --------------------------------------------------
        linha_seno = always_redraw(lambda: Line(
            start=eixos_circulo.c2p(np.cos(theta.get_value()), 0),
            end=eixos_circulo.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())),
            color=BLUE, stroke_width=5
        ))

        curva_seno = always_redraw(lambda: eixos_grafico.plot(
            lambda x: np.sin(x), 
            x_range=[0, max(0.01, theta.get_value())], 
            color=BLUE
        ))

        ponto_seno = always_redraw(lambda: Dot(eixos_grafico.c2p(theta.get_value(), np.sin(theta.get_value())), color=BLUE))

        # Linha pontilhada conectando a altura no círculo ao gráfico
        conexao_seno = always_redraw(lambda: DashedLine(
            start=eixos_circulo.c2p(np.cos(theta.get_value()), np.sin(theta.get_value())),
            end=eixos_grafico.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=BLUE, dash_length=0.1
        ))

        self.add(linha_seno, curva_seno, ponto_seno, conexao_seno)
        
        # Animação do Seno
        self.play(theta.animate.set_value(2 * PI), run_time=6, rate_func=linear)
        self.wait(1)

        # Remove os rastreadores do seno (mantendo a curva estática no gráfico)
        curva_seno_estatica = eixos_grafico.plot(lambda x: np.sin(x), x_range=[0, 2*PI], color=BLUE)
        self.add(curva_seno_estatica)
        self.remove(curva_seno, conexao_seno, ponto_seno, linha_seno)
        
        # Reseta o ângulo para a próxima volta
        theta.set_value(0)
        self.wait(1)

        # --------------------------------------------------
        # 5. Segunda Volta: Foco no Cosseno (Vermelho)
        # --------------------------------------------------
        linha_cosseno = always_redraw(lambda: Line(
            start=eixos_circulo.c2p(0, 0),
            end=eixos_circulo.c2p(np.cos(theta.get_value()), 0),
            color=RED, stroke_width=5
        ))

        curva_cosseno = always_redraw(lambda: eixos_grafico.plot(
            lambda x: np.cos(x), 
            x_range=[0, max(0.01, theta.get_value())], 
            color=RED
        ))

        ponto_cosseno = always_redraw(lambda: Dot(eixos_grafico.c2p(theta.get_value(), np.cos(theta.get_value())), color=RED))

        # Linha pontilhada conectando a base no círculo à altura do gráfico
        conexao_cosseno = always_redraw(lambda: DashedLine(
            start=eixos_circulo.c2p(np.cos(theta.get_value()), 0),
            end=eixos_grafico.c2p(theta.get_value(), np.cos(theta.get_value())),
            color=RED, dash_length=0.1
        ))

        self.add(linha_cosseno, curva_cosseno, ponto_cosseno, conexao_cosseno)

        # Animação do Cosseno
        self.play(theta.animate.set_value(2 * PI), run_time=6, rate_func=linear)
        self.wait(1)

        # Remove conectores e mantém a curva estática
        curva_cosseno_estatica = eixos_grafico.plot(lambda x: np.cos(x), x_range=[0, 2*PI], color=RED)
        self.add(curva_cosseno_estatica)
        self.remove(curva_cosseno, conexao_cosseno, ponto_cosseno, eixo_x_colorido)

        # --------------------------------------------------
        # 6. Teorema Fundamental da Trigonometria
        # --------------------------------------------------
        # Retorna o raio para 45 graus (pi/4) e mostra os dois catetos
        self.play(theta.animate.set_value(PI / 4), run_time=2)
        
        linha_seno_final = Line(eixos_circulo.c2p(np.cos(PI/4), 0), eixos_circulo.c2p(np.cos(PI/4), np.sin(PI/4)), color=BLUE, stroke_width=5)
        self.add(linha_seno_final)

        triangulo = Polygon(
            eixos_circulo.c2p(0, 0),
            eixos_circulo.c2p(np.cos(PI/4), 0),
            eixos_circulo.c2p(np.cos(PI/4), np.sin(PI/4)),
            color=YELLOW, fill_opacity=0.3
        )
        self.play(Create(triangulo))

        # Adiciona rótulos no triângulo
        label_seno = MathTex("\\sin(\\theta)").set_color(BLUE).next_to(linha_seno_final, RIGHT, buff=0.1).scale(0.7)
        label_cosseno = MathTex("\\cos(\\theta)").set_color(RED).next_to(linha_cosseno, DOWN, buff=0.1).scale(0.7)
        label_raio = MathTex("1").set_color(YELLOW).next_to(raio, UP+LEFT, buff=0.1).scale(0.7)

        self.play(Write(label_seno), Write(label_cosseno), Write(label_raio))
        self.wait(1)

        self.play(*(FadeOut(mob) for mob in list(self.mobjects)))

        # A fórmula ganha uma tela livre para continuar legível no formato vertical.
        titulo_teorema = Text("Teorema de Pitágoras", font_size=34)
        titulo_teorema.scale_to_fit_width(config.frame_width - 0.4)
        titulo_teorema.to_edge(UP, buff=0.6)
        eq_pitagoras = MathTex("a^2", "+", "b^2", "=", "c^2").scale(1.2)
        eq_pitagoras[0].set_color(BLUE)
        eq_pitagoras[2].set_color(RED)
        eq_pitagoras[4].set_color(YELLOW)
        eq_pitagoras.move_to(ORIGIN)
        self.play(Write(titulo_teorema), Write(eq_pitagoras))
        self.wait(1)

        eq_final = MathTex(
            "\\sin^2(\\theta)", "+", "\\cos^2(\\theta)", "=", "1"
        ).scale_to_fit_width(config.frame_width - 0.4)
        eq_final[0].set_color(BLUE)
        eq_final[2].set_color(RED)
        eq_final[4].set_color(YELLOW)
        eq_final.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq_pitagoras, eq_final))
        self.wait(3)