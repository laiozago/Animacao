from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8
config.frame_width = config.frame_height * config.pixel_width / config.pixel_height


class DesafioGeometria(Scene):
    def construct(self):
        # --------------------------------------------------
        # 1. APRESENTAÇÃO DO PROBLEMA
        # --------------------------------------------------
        raio_visual = 2.25  # Tamanho na tela vertical
        valor_raio = "10"  # Valor matemático do problema
        
        # Centro (origem)
        centro = DOWN * 0.1 + LEFT * 1.05
        
        # Desenhando o quarto de círculo
        arco = Arc(radius=raio_visual, start_angle=0, angle=PI/2, arc_center=centro, color=WHITE, stroke_width=4)
        linha_base = Line(centro, centro + RIGHT * raio_visual, color=WHITE, stroke_width=4)
        linha_altura = Line(centro, centro + UP * raio_visual, color=WHITE, stroke_width=4)
        
        quarto_circulo = VGroup(arco, linha_base, linha_altura)
        
        self.play(Create(linha_base), Create(linha_altura))
        self.play(Create(arco))
        self.wait(0.5)

        # Informação do Raio
        raio_label = MathTex(f"R = {valor_raio}").scale(0.7).next_to(linha_base, DOWN)
        self.play(Write(raio_label))
        self.wait(1)

        # Inserindo o Retângulo
        # Escolhemos um ângulo qualquer para o ponto tocar no arco (ex: 35 graus)
        angulo = 35 * DEGREES
        ponto_arco = centro + np.array([raio_visual * np.cos(angulo), raio_visual * np.sin(angulo), 0])
        ponto_x = centro + np.array([raio_visual * np.cos(angulo), 0, 0])
        ponto_y = centro + np.array([0, raio_visual * np.sin(angulo), 0])

        retangulo = Polygon(
            centro, ponto_x, ponto_arco, ponto_y,
            color=BLUE, fill_opacity=0.2, stroke_width=3
        )
        self.play(DrawBorderThenFill(retangulo), run_time=1.5)
        self.wait(1)

        # A Pergunta (Diagonal Vermelha)
        diagonal_pergunta = Line(ponto_x, ponto_y, color=RED, stroke_width=5)
        pergunta_texto = Text("Qual é o comprimento da linha vermelha?", font_size=30)
        pergunta_texto.scale_to_fit_width(config.frame_width - 0.4)
        pergunta_texto.to_edge(UP, buff=0.45)
        interrogacao = MathTex("?").set_color(RED).next_to(diagonal_pergunta, UP+RIGHT, buff=0.1)

        self.play(Create(diagonal_pergunta))
        self.play(Write(pergunta_texto), Write(interrogacao))
        self.wait(2)

        # Simula a "pausa" típica dos vídeos
        pausa_texto = Text("(Pause o vídeo se quiser tentar resolver)", font_size=20, color=GRAY)
        pausa_texto.scale_to_fit_width(config.frame_width - 0.5)
        pausa_texto.next_to(pergunta_texto, DOWN, buff=0.2)
        self.play(FadeIn(pausa_texto))
        self.wait(3)
        self.play(FadeOut(pausa_texto))

        # --------------------------------------------------
        # 2. A RESOLUÇÃO (O momento "Aha!")
        # --------------------------------------------------
        resolucao_texto = Text("Resolução:", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Transform(pergunta_texto, resolucao_texto))

        desenho = VGroup(quarto_circulo, raio_label, retangulo, diagonal_pergunta, interrogacao)
        desenho_center = desenho.get_center()
        desenho_target = DOWN * 1.15
        desenho_scale = 0.68
        self.play(
            desenho.animate.scale(desenho_scale).move_to(desenho_target),
            run_time=0.8,
        )
        transform_point = lambda point: desenho_target + desenho_scale * (point - desenho_center)
        centro = transform_point(centro)
        ponto_x = transform_point(ponto_x)
        ponto_y = transform_point(ponto_y)
        ponto_arco = transform_point(ponto_arco)
        
        # Passo 1: Propriedade do retângulo
        dica_1 = Text("1. As diagonais de um retângulo são iguais.", font_size=22)
        dica_1.scale_to_fit_width(config.frame_width - 0.4)
        dica_1.next_to(pergunta_texto, DOWN, buff=0.2)
        self.play(Write(dica_1))
        
        # Desenha a segunda diagonal
        diagonal_2 = Line(centro, ponto_arco, color=YELLOW, stroke_width=5)
        self.play(Create(diagonal_2))
        self.wait(1)
        
        # Transforma a vermelha na amarela para provar
        self.play(ReplacementTransform(diagonal_pergunta, diagonal_2.copy().set_color(RED)))
        self.remove(interrogacao)
        self.wait(1)

        # Passo 2: O truque visual (A diagonal é o raio!)
        dica_2 = Text("2. A outra diagonal vai do centro até a borda.", font_size=22)
        dica_2.scale_to_fit_width(config.frame_width - 0.4)
        dica_2.next_to(dica_1, DOWN, buff=0.15)
        self.play(Write(dica_2))
        self.wait(1)
        
        dica_3 = Text("3. Portanto, ela é exatamente o RAIO!", font_size=22, color=GREEN)
        dica_3.scale_to_fit_width(config.frame_width - 0.4)
        dica_3.next_to(dica_2, DOWN, buff=0.15)
        self.play(Write(dica_3))
        
        # Gira o raio para provar que é igual à base
        raio_giratorio = Line(centro, ponto_arco, color=GREEN, stroke_width=6)
        self.play(Create(raio_giratorio))
        self.play(Rotate(raio_giratorio, angle=-angulo, about_point=centro), run_time=1.5)
        self.wait(1)

        # Conclusão
        # Diminuímos a escala para 1.1 e ancoramos na borda direita da tela
        resposta_final = MathTex("\\text{Comprimento} = 10").scale_to_fit_width(config.frame_width - 1).set_color(RED)
        resposta_final.next_to(retangulo, DOWN, buff=0.35).shift(DOWN * 0.65)
        
        # Cria uma caixa de destaque ao redor da resposta
        caixa_resposta = SurroundingRectangle(resposta_final, color=YELLOW, buff=0.2)
        
        self.play(Write(resposta_final))
        self.play(Create(caixa_resposta))
        self.wait(3)