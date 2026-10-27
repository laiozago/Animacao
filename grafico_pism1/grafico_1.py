from pathlib import Path

from manim import *

config.media_dir = str(Path(__file__).resolve().parent / "media")

class GraficoPISM(Scene):
    def construct(self):
        # 1. Eixos com numeração focada apenas nos valores críticos
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-4, 8, 2],
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": [4, 6, 9]},
            y_axis_config={"numbers_to_include": [-2, 7]},
            tips=False
        )

        # 2. Funções (Reta e Parábola)
        reta = axes.plot(lambda x: 6 - x, x_range=[1, 4], color=YELLOW, stroke_width=4)
        parabola = axes.plot(lambda x: x**2 - 12*x + 34, x_range=[4, 9], color=GREEN, stroke_width=4)

        # Animação 1: Cria eixos e gráficos de forma simultânea e rápida (Tempo: 2s)
        self.play(
            Create(axes), Create(reta), Create(parabola),
            run_time=2
        )

        # 3. Destacando o Vértice e o Fim da Parábola (Extremos da Imagem)
        vertice = Dot(axes.c2p(6, -2), color=RED)
        fim = Dot(axes.c2p(9, 7), color=RED)

        # Linhas tracejadas ligando os extremos ao eixo Y
        linha_v = axes.get_horizontal_line(vertice.get_center(), color=RED, line_func=DashedLine)
        linha_f = axes.get_horizontal_line(fim.get_center(), color=RED, line_func=DashedLine)

        # Animação 2: Puxa o olhar para o eixo Y (Tempo: 1.5s)
        self.play(
            FadeIn(vertice), Create(linha_v),
            FadeIn(fim), Create(linha_f),
            run_time=1.5
        )

        # 4. Destacando o Conjunto Imagem
        zona_imagem = Line(axes.c2p(0, -2), axes.c2p(0, 7), color=ORANGE, stroke_width=8)
        texto_imagem = Tex(r"Imagem: $[-2, 7]$", color=ORANGE, font_size=40).to_edge(UR)

        # Animação 3: Pinta o intervalo no eixo Y (Tempo: 2s)
        self.play(
            Create(zona_imagem),
            Write(texto_imagem),
            run_time=2
        )

        # 5. Ênfase visual explícita no Vértice
        alerta = Text("O vértice define o Mínimo!", color=RED, font_size=28).next_to(vertice, DOWN)

        # Animação 4: Pulsa o vértice e escreve o alerta (Tempo: 2s)
        self.play(Write(alerta), vertice.animate.scale(2), run_time=1.5)
        self.play(vertice.animate.scale(0.5), run_time=0.5)

        # Animação 5: Pausa final para o aluno ler (Tempo: 1.5s) -> Total = 9.0s
        self.wait(1.5)