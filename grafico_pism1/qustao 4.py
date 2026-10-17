from manim import *

class PitagorasRapido(Scene):
    def construct(self):
        # 1. Desenho do Triângulo à esquerda
        # Proporção exata do triângulo 3-4-5 (900-1200-1500)
        vertices = [ORIGIN, 3 * RIGHT, 4 * UP]
        triangulo = Polygon(*vertices, color=BLUE, stroke_width=4).shift(LEFT * 4 + DOWN * 2)

        # Ângulo Reto
        linha_base = Line(ORIGIN, 3 * RIGHT).shift(LEFT * 4 + DOWN * 2)
        linha_altura = Line(ORIGIN, 4 * UP).shift(LEFT * 4 + DOWN * 2)
        angulo_reto = RightAngle(linha_base, linha_altura, length=0.4, color=WHITE)

        # Rótulos (Catetos e Hipotenusa)
        label_900 = MathTex("900").next_to(linha_base, DOWN)
        label_h = MathTex("h").next_to(linha_altura, LEFT)

        meio_hip = (vertices[1] + vertices[2]) / 2 + LEFT * 4 + DOWN * 2
        label_1500 = MathTex("1500").move_to(meio_hip).shift(UR * 0.4)

        # Animação 1: O triângulo surge em 1.5s
        self.play(
            Create(triangulo), Create(angulo_reto),
            FadeIn(label_900), FadeIn(label_h), FadeIn(label_1500),
            run_time=1.5
        )

        # 2. Resolução do Teorema de Pitágoras à direita
        # Strings separadas garantem uma transição (morph) perfeita das letras e números
        p1 = MathTex("h^2", "+", "900^2", "=", "1500^2").shift(RIGHT * 2.5)
        p2 = MathTex("h^2", "=", "1500^2", "-", "900^2").shift(RIGHT * 2.5)
        p3 = MathTex("h^2", "=", "2250000", "-", "810000").shift(RIGHT * 2.5)
        p4 = MathTex("h^2", "=", "1440000").shift(RIGHT * 2.5)
        p5 = MathTex("h", "=", "\\sqrt{1440000}").shift(RIGHT * 2.5)
        p6 = MathTex("h", "=", "1200").shift(RIGHT * 2.5).scale(1.2).set_color(YELLOW)

        # Animação 2: Passos rápidos (1 segundo cada)
        self.play(Write(p1), run_time=1)
        self.play(TransformMatchingTex(p1, p2), run_time=1)
        self.play(TransformMatchingTex(p2, p3), run_time=1)
        self.play(TransformMatchingTex(p3, p4), run_time=1)
        self.play(TransformMatchingTex(p4, p5), run_time=1)
        self.play(TransformMatchingTex(p5, p6), run_time=1)

        # 3. Conclusão visual
        caixa = SurroundingRectangle(p6, color=GREEN)
        h_final = MathTex("1200").move_to(label_h).set_color(YELLOW)

        # Animação 3: Substitui o 'h' no triângulo pelo número 1200
        self.play(
            Create(caixa),
            Transform(label_h, h_final),
            run_time=1.5
        )

        self.wait(1)