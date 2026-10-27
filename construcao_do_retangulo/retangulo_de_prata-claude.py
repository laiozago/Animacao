"""
Construção geométrica do Retângulo de Prata (razão 1 : 1 + √2) com Manim.

Renderizar (vertical 1080x1920):
    manim -pqh retangulo_de_prata.py RetanguloDePrata

Requer LaTeX instalado (MathTex).
"""
from manim import *
from pathlib import Path

config.media_dir = str(Path(__file__).resolve().parent / "media")
import numpy as np

# ---------------------------------------------------------------------------
# Configuração: vertical 9:16 (TikTok / Shorts), fundo branco
# ---------------------------------------------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 16.0
config.frame_width = 9.0
config.background_color = WHITE

# Paleta: preto em tudo; o amarelo é usado apenas no retângulo final
PRETO = BLACK
AMARELO = YELLOW

ESPESSURA = 5      # espessura das linhas
FONTE = 44         # tamanho dos rótulos


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------
def linha(p, q):
    return Line(p, q, color=PRETO, stroke_width=ESPESSURA)


def ponto(p):
    return Dot(p, radius=0.08, color=PRETO)


def vertice(nome, p, direcao):
    return MathTex(nome, color=PRETO, font_size=FONTE).next_to(p, direcao, buff=0.2)


def chave(p, q, direcao, tex, buff=0.75):
    """Chave (Brace) sob/ao lado do segmento pq, com o rótulo `tex`."""
    segmento = Line(p, q)
    brace = Brace(segmento, direcao, buff=buff, color=PRETO)
    brace.set_color(PRETO)
    rotulo = MathTex(tex, color=PRETO, font_size=FONTE).next_to(brace, direcao, buff=0.15)
    return VGroup(brace, rotulo)


class RetanguloDePrata(Scene):
    def mostrar_chave(self, grupo, run_time=1.2):
        self.play(GrowFromCenter(grupo[0]), FadeIn(grupo[1]), run_time=run_time)

    def construct(self):
        # -------------------------------------------------------------------
        # Geometria (l = L; todas as coordenadas derivam dele)
        # -------------------------------------------------------------------
        L = 2.8
        R2 = np.sqrt(2)
        largura_total = L * (1 + R2)          # largura do retângulo ABEF

        B = np.array([-largura_total / 2, -0.5, 0.0])   # figura centralizada
        C = B + RIGHT * L
        A = B + UP * L
        D = C + UP * L
        E = C + RIGHT * L * R2                # CE = l√2
        F = E + UP * L
        H = C + RIGHT * L                     # CH = l  (segundo quadrado)
        G = H + UP * L

        # -------------------------------------------------------------------
        # 1) Quadrado ABCD, vértices e medidas l
        # -------------------------------------------------------------------
        lados = [linha(A, B), linha(B, C), linha(C, D), linha(D, A)]
        self.play(LaggedStart(*[Create(s) for s in lados], lag_ratio=0.6), run_time=3)

        pontos_abcd = VGroup(*[ponto(p) for p in (A, B, C, D)])
        rotulos_abcd = VGroup(
            vertice("A", A, UL),
            vertice("B", B, DL),
            vertice("C", C, DOWN),
            vertice("D", D, UP),
        )
        self.play(FadeIn(pontos_abcd), FadeIn(rotulos_abcd))

        medida_base = chave(B, C, DOWN, "l")
        medida_altura = chave(B, A, LEFT, "l", buff=0.2)
        self.play(
            GrowFromCenter(medida_base[0]), FadeIn(medida_base[1]),
            GrowFromCenter(medida_altura[0]), FadeIn(medida_altura[1]),
            run_time=1.2,
        )
        self.wait(0.5)

        # -------------------------------------------------------------------
        # 2) Diagonal AC = l√2
        # -------------------------------------------------------------------
        diagonal = linha(A, C)
        self.play(Create(diagonal), run_time=1.5)

        normal = np.array([1.0, 1.0, 0.0]) / R2
        rotulo_diagonal = MathTex(r"l\sqrt{2}", color=PRETO, font_size=FONTE)
        rotulo_diagonal.move_to((A + C) / 2 + normal * 0.65)
        self.play(Write(rotulo_diagonal))
        self.wait(0.5)

        # -------------------------------------------------------------------
        # 3) Arco tracejado com centro em C e raio AC, de A até E
        # -------------------------------------------------------------------
        arco = DashedVMobject(
            Arc(
                radius=L * R2,
                start_angle=3 * PI / 4,      # direção de C para A
                angle=-3 * PI / 4,           # desce até o prolongamento de BC
                arc_center=C,
            ),
            num_dashes=45,
            dashed_ratio=0.55,
            color=PRETO,
        )
        arco.set_stroke(PRETO, width=ESPESSURA)
        self.play(Create(arco), run_time=3, rate_func=linear)

        ponto_E = ponto(E)
        rotulo_E = vertice("E", E, DOWN)
        self.play(FadeIn(ponto_E), FadeIn(rotulo_E))
        self.wait(0.5)

        # -------------------------------------------------------------------
        # 4) Fecha o retângulo ABEF; CE = l√2
        # -------------------------------------------------------------------
        base_CE = linha(C, E)
        lado_EF = linha(E, F)
        topo_DF = linha(D, F)
        self.play(Create(base_CE), run_time=1)
        self.play(Create(lado_EF), run_time=1)
        self.play(Create(topo_DF), run_time=1)

        ponto_F = ponto(F)
        rotulo_F = vertice("F", F, UP)
        self.play(FadeIn(ponto_F), FadeIn(rotulo_F))

        medida_CE = chave(C, E, DOWN, r"l\sqrt{2}")
        self.mostrar_chave(medida_CE)
        self.wait(0.8)

        # -------------------------------------------------------------------
        # 5) Segundo quadrado CDGH, colado à direita do original
        # -------------------------------------------------------------------
        quadrado2 = Polygon(C, D, G, H, color=PRETO, stroke_width=ESPESSURA)
        self.play(Create(quadrado2), run_time=2.5)

        pontos_gh = VGroup(ponto(G), ponto(H))
        rotulos_gh = VGroup(vertice("G", G, UR), vertice("H", H, DOWN))
        self.play(FadeIn(pontos_gh), FadeIn(rotulos_gh))

        medida_CH = chave(C, H, DOWN, "l")
        self.play(ReplacementTransform(medida_CE, medida_CH), run_time=1.5)
        self.wait(0.8)

        # -------------------------------------------------------------------
        # 6) Destaca o retângulo EFGH em amarelo
        # -------------------------------------------------------------------
        amarelo = Polygon(
            H, E, F, G,
            fill_color=AMARELO,
            fill_opacity=1,
            stroke_color=PRETO,
            stroke_width=ESPESSURA,
        )
        amarelo.set_z_index(-1)
        self.play(DrawBorderThenFill(amarelo), run_time=2)
        self.wait(0.8)

        # -------------------------------------------------------------------
        # 7) Chave sob a base do retângulo amarelo: l√2 − l
        # -------------------------------------------------------------------
        medida_HE = chave(H, E, DOWN, r"l\sqrt{2}-l")
        self.mostrar_chave(medida_HE, run_time=1.5)

        self.wait(3)