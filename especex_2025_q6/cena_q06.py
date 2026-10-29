"""cena_q06.py — EsPCEx 2026 (2º dia), Questão 06: sete paralelas dentro do triângulo.

Render:  manim -pql cena_q06.py QuestaoEspcex06   (prévia 540x960, com 3 guias)
         manim -qh  cena_q06.py QuestaoEspcex06   (final 1080x1920, sem guias)
Sincronizada com ESPCEX_-_2025_-_Q6.srt (vídeo limpo, ~4m09s). Cada passo traz o instante da fala.
Cores: AMARELO = AC/x/AF (cateto vertical, altura) e regras · LARANJA = AB (base), α, DEFG (dados)
       AZUL = s (espacinho) e AGD (o pequeno) · VERMELHO = falta · VERDE = resolvido · CINZA = contexto
"""
import numpy as np
from manim import *

import geometria as G
from cena_base import CenaBase, _v


def L(p):
    """ponto em cm (x, y) → vetor da tela"""
    return _v(G.tela(*p))


class QuestaoEspcex06(CenaBase):

    # ================================================================ construção dos objetos
    def monta_figura(self):
        T = {n: _v(p) for n, p in G.PT_TELA.items()}
        self.T = T
        A, B, C = T["A"], T["B"], T["C"]
        pos = G.pos_rotulos()
        self.tri = Polygon(A, B, C, color=G.TEXTO, stroke_width=3)
        self.segs = []
        for j in range(G.N_SEG):
            p, q = G.seg_cm(j)
            self.segs.append(Line(L(p), L(q), color=G.TEXTO, stroke_width=2.5))
        r = 0.17
        self.reto = VMobject()
        self.reto.set_points_as_corners([A + RIGHT * r, A + RIGHT * r + UP * r, A + UP * r])
        self.reto.set_stroke(G.LARANJA, 3)
        self.pontos = VGroup(*[Dot(T[n], radius=0.04, color=G.TEXTO) for n in "ABCDEFG"])
        self.letras = {n: self.tex(n, escala=0.55).move_to(_v(pos[n])) for n in "ABCDEFG"}
        # α (como na prova): arco em D entre DG e DA
        self.arco = Arc(radius=0.26, start_angle=np.radians(180 - G.ANG_ALFA), angle=np.radians(G.ANG_ALFA),
                        arc_center=T["D"], color=G.LARANJA, stroke_width=3)
        self.alfa = self.tex(r"\alpha", escala=0.6, cor=G.LARANJA).move_to(_v(pos["alfa"]))
        self.alfa.set_stroke(G.FUNDO, 5, background=True)          # halo branco por cima das linhas
        # cota de 60 cm
        x60, y0, y1 = pos["60x"], G.PT_TELA["A"][1], G.tela(0, G.ALTURA_BASE)[1]
        self.cota = VGroup(Line(_v((x60, y0)), _v((x60, y1))),
                           Line(_v((x60 - 0.06, y0)), _v((x60 + 0.06, y0))),
                           Line(_v((x60 - 0.06, y1)), _v((x60 + 0.06, y1))))
        self.cota.set_stroke(G.TEXTO, 2)
        self.txt60 = self.tex(r"60\text{ cm}", escala=0.5).rotate(PI / 2).move_to(_v(pos["60cm"]))
        # s em cada espacinho (7: seis entre segmentos + o último até BC)
        self.s_lbl = [self.tex("s", escala=0.5, cor=G.AZUL).move_to(_v(p)) for p in pos["s"]]
        # polígonos de apoio (criados só quando usados)
        self.faixas = [Polygon(*[L(p) for p in G.faixa_cm(k)], color=G.AZUL if k % 2 == 0 else G.CINZA,
                               fill_color=G.AZUL if k % 2 == 0 else G.CINZA, fill_opacity=0.28, stroke_width=0)
                       for k in range(G.N_SEG) if k not in G.FAIXAS_FORA]
        self.defg = Polygon(T["G"], T["F"], T["E"], T["D"], color=G.LARANJA, fill_color=G.LARANJA,
                            fill_opacity=0.30, stroke_width=2)
        self.lbl720 = self.tex(r"720\text{ cm}^2", escala=0.5, cor=G.LARANJA).move_to(_v(pos["720"]))
        fio = Line(_v(pos["720_centro"]), _v(pos["720_fio_fim"]), color=G.LARANJA, stroke_width=1.8)
        self.txt720 = VGroup(self.lbl720, fio, Dot(_v(pos["720_centro"]), radius=0.03, color=G.LARANJA))
        self.afe = Polygon(A, T["F"], T["E"], color=G.AMARELO, stroke_width=4)
        self.agd = Polygon(A, T["G"], T["D"], color=G.AZUL, stroke_width=4)
        self.tris = [Polygon(A, L((0, G.h_seg(j))), L((G.K * G.h_seg(j), 0)), color=G.AZUL, stroke_width=2.2)
                     for j in range(G.N_SEG)]
        # sobreposições grossas (ligar/desligar)
        self.ov_AC = Line(A, C, color=G.AMARELO, stroke_width=7)
        self.ov_AB = Line(A, B, color=G.LARANJA, stroke_width=7)
        self.ov_AF = Line(A, T["F"], color=G.AMARELO, stroke_width=7)
        self.ov_AG = Line(A, T["G"], color=G.AZUL, stroke_width=7)
        self.ov_ABC = self.sobreposto(self.tri, G.AMARELO, 7)

    # ================================================================ roteiro da cena
    def construct(self):
        self.guias()
        self.marca_dagua()
        self.monta_roteiro(G.ROT_ABERTO, G.ROT_FECHADO)
        self.monta_figura()

        self.figura_inicial()             # a figura da prova já está na caixa grande desde o 1º quadro
        self.abertura(0.0, dur=0.3, sai=6.9)
        self.fase_dados(10.3)             # α, tg α = 2,5, 60 cm, 720, A_DEFG = AFE − AGD
        self.fase_tangente(33.0)          # tg α = AC/AB = 5/2 → AB = 0,4·AC   (regra 1)
        self.fase_semelhantes(58.6)       # todos os triângulos são semelhantes a ACB
        self.fase_x(77.4)                 # AC = x, AB = 0,4x, A = 0,2x²        (regra 2)
        self.fase_s(106.0)                # espacinhos, s, A_DEFG = AFE − AGD
        self.fase_areas(131.8)            # A_AFE e A_AGD em função de s
        self.fase_quadrados(153.1)        # 0,2[(60+4s)² − (60+2s)²] = 720
        self.fase_equacao(183.0)          # 2s(120+6s) = 3600 → s² + 20s − 300 = 0 → s = 10
        self.fase_final(210.5)            # AC = 130, AB = 52, A = 3380, letra A
        self.encerra(243.4)

    # ================================================================ abertura
    def abertura(self, t, *, dur=0.3, sai=6.9):
        """Enunciado INTEGRAL recomposto, TODO DE UMA VEZ desde o 1º quadro; sai quando ele começa a resolver."""
        self.enun = self.enunciado()
        self.add(self.enun)
        self.passo(sai, FadeOut(self.enun), dur=dur, nome="enunciado sai")

    def figura_inicial(self):
        """Figura completa, como na prova, na caixa grande (acima da marca d'água, fora do rosto): sem animação."""
        self.add(self.defg, self.tri, *self.segs, self.reto, self.pontos, *[self.letras[n] for n in "ABCDEFG"],
                 self.arco, self.alfa, self.cota, self.txt60)

    # ================================================================ 10 – 33 s: os dados
    def fase_dados(self, t):
        self.a_tg = self.linha(G.FORM["A_tg"], 4.90)
        self.a_dif = self.linha(G.FORM["A_dif"], 3.70, escala=G.ESC_DIF)
        tg, dif = self.a_tg, self.a_dif
        self.passo(10.3, Indicate(self.alfa, color=G.LARANJA, scale_factor=1.5), self.aparece(tg[0]), dur=0.7, nome="α")
        self.passo(12.7, self.aparece(tg[1]), self.aparece(tg[2]), dur=0.5, nome="tg = 2,5")
        self.passo(15.4, Indicate(self.txt60, color=G.LARANJA, scale_factor=1.3), dur=0.7, nome="60 cm")
        self.passo(17.6, Indicate(self.defg, color=G.LARANJA, scale_factor=1.0), dur=0.8, nome="DEFG")
        self.passo(18.9, FadeIn(self.txt720), dur=0.6, nome="720 cm²")
        self.passo(21.1, self.aparece(dif[0]), self.aparece(dif[1]), dur=0.5, nome="A_DEFG =")
        self.passo(23.4, self.aparece(dif[2]), FadeIn(self.afe), dur=0.8, nome="A_AFE")
        self.passo(25.0, self.aparece(dif[3]), dur=0.3, nome="menos")
        self.passo(25.5, self.aparece(dif[4]), FadeIn(self.agd), dur=0.8, nome="A_AGD")
        self.passo(29.2, self.aparece(dif[5]), self.aparece(dif[6]), dur=0.6, nome="= 720")
        self.passo(31.4, FadeOut(self.afe), FadeOut(self.agd), dur=0.5, nome="tira AFE/AGD")
        self.passo(33.0, FadeOut(tg), FadeOut(dif), dur=0.6, nome="limpa fase A")

    # ================================================================ 34 – 57 s: tg α = AC/AB
    def fase_tangente(self, t):
        b1 = self.linha(G.FORM["B_1"], 4.90, escala=G.ESC_B1)
        b2 = self.linha(G.FORM["B_2"], 3.50)
        b3 = self.linha(G.FORM["B_3"], 2.30)
        b4 = self.linha(G.FORM["B_4"], G.Y_REGRA1)
        self.b4 = b4
        self.passo(34.3, self.aparece(b1[0]), dur=0.4, nome="tg")
        self.passo(35.2, self.aparece(b1[1]), self.aparece(b1[2]), dur=0.5, nome="= 2,5")
        self.passo(36.9, self.aparece(b1[3]), self.aparece(b1[4]), dur=0.9, nome="oposto/adjacente")
        self.passo(40.0, *[self.aparece(p) for p in b2[:3]], FadeIn(self.ov_AC), dur=0.6, nome="AC")
        self.passo(42.7, FadeIn(self.ov_AB), dur=0.5, nome="AB")
        self.passo(44.3, self.aparece(b2[3]), dur=0.3, nome="=")
        self.passo(45.1, self.aparece(b2[4]), dur=0.5, nome="5/2")
        self.passo(46.4, FadeOut(self.ov_AC), FadeOut(self.ov_AB), dur=0.4, nome="tira AC/AB")
        self.passo(48.0, self.aparece(b3[0]), dur=0.4, nome="5AB")
        self.passo(49.8, self.aparece(b3[1]), self.aparece(b3[2]), dur=0.5, nome="= 2AC")
        self.passo(52.4, *[self.aparece(p) for p in b4[:4]], dur=0.8, nome="AB = 2/5 AC")
        self.passo(54.0, self.aparece(b4[4]), self.aparece(b4[5]), dur=0.5, nome="= 0,4AC")
        self.box_r1 = self.caixa(VGroup(*b4), G.AMARELO)
        self.passo(56.4, FadeIn(self.box_r1), dur=0.5, nome="regra 1")
        self.passo(57.1, FadeOut(b1), FadeOut(b2), FadeOut(b3), dur=0.5, nome="limpa fase B")

    # ================================================================ 58 – 74 s: semelhança
    def fase_semelhantes(self, t):
        c1 = self.linha(G.FORM["C_1"], 4.90)
        ov_j = self.sobreposto(self.tris[3], G.LARANJA, 6)
        self.passo(58.6, *[FadeIn(tr) for tr in self.tris], dur=0.8, nome="todos os triângulos")
        self.pisca(61.5, ov_j, dur=1.4, nome="qualquer um")
        self.passo(64.4, self.aparece(c1[0]), dur=0.4, nome="△_j")
        self.passo(65.2, self.aparece(c1[1]), dur=0.3, nome="∼")
        self.passo(66.5, self.aparece(c1[2]), FadeIn(self.ov_ABC), dur=0.6, nome="△ACB")
        self.passo(72.7, Indicate(self.box_r1, color=G.LARANJA, scale_factor=1.06), dur=0.8, nome="0,4 do outro")
        self.passo(74.2, *[FadeOut(tr) for tr in self.tris], FadeOut(self.ov_ABC), FadeOut(c1),
                   dur=0.5, nome="limpa fase C")

    # ================================================================ 74 – 106 s: AC = x, A = 0,2x²
    def fase_x(self, t):
        d1 = self.linha(G.FORM["D_1"], 5.00)
        d2 = self.linha(G.FORM["D_2"], 4.20)
        d3 = self.linha(G.FORM["D_3"], 3.40)
        d4 = self.linha(G.FORM["D_4"], 2.60, alinhar=(d3, 1))
        d5 = self.linha(G.FORM["D_5"], 1.95)
        self.passo(77.4, FadeIn(self.ov_AC), dur=0.5, nome="lado AC")
        self.passo(79.5, self.aparece(d1[0]), self.aparece(d1[1]), self.aparece(d1[2]), dur=0.6, nome="AC = x")
        self.passo(81.2, FadeIn(self.ov_AB), self.aparece(d2[0]), self.aparece(d2[1]), dur=0.4, nome="AB =")
        self.passo(81.95, self.aparece(d2[2]), dur=0.4, nome="0,4")
        self.passo(83.5, self.aparece(d2[3]), dur=0.3, nome="x")
        self.passo(84.0, self.aparece(d3[0]), self.aparece(d3[1]), dur=0.4, nome="A =")
        self.passo(85.75, self.aparece(d3[2]), dur=0.3, nome="x")
        self.passo(86.3, self.aparece(d3[3]), dur=0.3, nome="vezes")
        self.passo(87.0, self.aparece(d3[4]), dur=0.5, nome="0,4x")
        self.passo(88.0, self.aparece(d3[5]), self.aparece(d3[6]), dur=0.6, nome="÷ 2")
        self.passo(89.1, self.aparece(d4[0]), self.aparece(d4[1]), dur=0.5, nome="= 0,2")
        self.passo(90.6, self.aparece(d4[2]), FadeOut(self.ov_AC), FadeOut(self.ov_AB), dur=0.5, nome="x²")
        box_d4 = self.caixa(VGroup(d4[1], d4[2]), G.AMARELO)
        self.passo(93.1, FadeIn(box_d4), dur=0.5, nome="mesma área")
        self.passo(97.2, self.aparece(d5[0]), self.aparece(d5[1]), dur=0.4, nome="x =")
        self.passo(98.3, self.aparece(d5[2]), FadeIn(self.ov_AC), dur=0.5, nome="cateto vertical")
        self.passo(101.7, FadeOut(self.ov_AC), dur=0.4, nome="tira AC")
        # regra 2 (A = 0,2x²) fica embaixo; o resto sai
        self.r2 = self.linha(G.FORM["R2"], G.Y_REGRA2)
        self.box_r2 = self.caixa(VGroup(*self.r2), G.AMARELO)
        self.passo(106.0, FadeOut(d1), FadeOut(d2), FadeOut(d3), FadeOut(d4), FadeOut(d5), FadeOut(box_d4),
                   *[self.aparece(p) for p in self.r2], FadeIn(self.box_r2), dur=0.5, nome="regra 2")

    # ================================================================ 106 – 131 s: s e A_DEFG = AFE − AGD
    def fase_s(self, t):
        self.e1 = self.linha(G.FORM["E_1"], 5.10)
        self.e2 = self.linha(G.FORM["A_dif"], 4.30, escala=G.ESC_DIF)
        e1, e2 = self.e1, self.e2
        self.passo(107.4, LaggedStart(*[FadeIn(f) for f in self.faixas], lag_ratio=0.25), dur=2.6, nome="faixas")
        self.passo(110.8, self.aparece(e1[0]), dur=0.4, nome="espacinho")
        self.passo(112.0, self.aparece(e1[1]), self.aparece(e1[2]), *[FadeIn(s) for s in self.s_lbl],
                   self.anim_rot_entra(0), dur=0.6, nome="s")
        self.passo(114.1, *[FadeOut(f) for f in self.faixas], Indicate(self.defg, color=G.LARANJA, scale_factor=1.0),
                   dur=0.6, nome="área DEFG")
        self.passo(115.2, self.aparece(e2[0]), dur=0.5, nome="A_DEFG")
        self.passo(118.6, Indicate(self.lbl720, color=G.LARANJA, scale_factor=1.3), dur=0.6, nome="720")
        self.passo(120.9, self.aparece(e2[1]), dur=0.3, nome="=")
        self.passo(121.3, self.aparece(e2[2]), FadeIn(self.afe), dur=0.6, nome="triângulo AFE")
        self.passo(122.7, self.aparece(e2[3]), dur=0.25, nome="menos")
        self.passo(123.3, self.aparece(e2[4]), FadeIn(self.agd), dur=0.7, nome="triângulo AGD")
        self.passo(125.5, Indicate(self.defg, color=G.LARANJA, scale_factor=1.0), dur=0.8, nome="área rosinha")
        self.passo(126.8, self.aparece(e2[5]), self.aparece(e2[6]), dur=0.5, nome="= 720")

    # ================================================================ 131 – 153 s: AFE e AGD em função de s
    def fase_areas(self, t):
        self.f1 = self.linha(G.FORM["F_1"], 3.50)
        self.f2 = self.linha(G.FORM["F_2"], 2.80)
        f1, f2 = self.f1, self.f2
        s4 = VGroup(*self.s_lbl[0:4])
        s2 = VGroup(*self.s_lbl[0:2])
        self.passo(131.8, self.aparece(f1[0]), dur=0.5, nome="A_AFE")
        self.passo(134.0, self.aparece(f1[1]), FadeIn(self.ov_AF), dur=0.3, nome="AF")
        self.passo(134.9, LaggedStart(*[Indicate(l, color=G.AMARELO) for l in s4], lag_ratio=0.2),
                   dur=1.0, nome="4 espacinhos")
        self.passo(136.67, self.aparece(f1[2]), Indicate(self.box_r2, color=G.LARANJA, scale_factor=1.06),
                   dur=0.7, nome="0,2")
        self.passo(138.93, self.aparece(f1[3]), dur=0.5, nome="(60+4s)")
        self.passo(140.27, self.aparece(f1[4]), dur=0.4, nome="² (grande)")
        self.passo(141.0, FadeOut(self.ov_AF), dur=0.4, nome="tira AF")
        self.passo(142.87, self.aparece(f2[0]), dur=0.4, nome="A_AGD")
        self.passo(143.5, self.aparece(f2[1]), dur=0.3, nome="=")
        self.passo(144.4, self.aparece(f2[2]), dur=0.4, nome="0,2")
        self.passo(145.5, self.aparece(f2[3]), FadeIn(self.ov_AG), dur=0.6, nome="(60+2s)")
        self.passo(147.6, LaggedStart(*[Indicate(l, color=G.AMARELO) for l in s2], lag_ratio=0.3),
                   dur=0.9, nome="2 espacinhos")
        self.passo(151.9, self.aparece(f2[4]), FadeOut(self.ov_AG), dur=0.4, nome="² (pequeno)")

    # ================================================================ 153 – 183 s: diferença de quadrados
    def fase_quadrados(self, t):
        self.r3 = self.linha(G.FORM["R3"], G.Y_REGRA2)
        g1 = self.linha(G.FORM["G_1"], 4.90, escala=G.ESC_G)
        g2a = self.linha(G.FORM["G_2a"], 4.00, escala=G.ESC_G)
        g2b = self.linha(G.FORM["G_2b"], 3.10, escala=G.ESC_G)
        self.g_rows = [g1, g2a, g2b]
        r3 = self.r3
        self.passo(153.1, FadeOut(self.r2), FadeOut(self.box_r2), dur=0.4, nome="tira regra 2")
        self.passo(154.8, self.aparece(r3[0]), dur=0.6, nome="a² − b²")
        self.passo(156.9, FadeOut(self.f1), FadeOut(self.f2), FadeOut(self.e1), FadeOut(self.e2),
                   self.aparece(g1[0]), dur=0.5, nome="0,2 em evidência")
        self.passo(159.6, self.aparece(g1[1]), dur=0.3, nome="[")
        self.passo(161.7, self.aparece(g1[2]), dur=0.5, nome="(60+4s)²")
        self.passo(164.6, self.aparece(g1[3]), dur=0.3, nome="menos")
        self.passo(165.6, self.aparece(g1[4]), self.aparece(g1[5]), dur=0.6, nome="(60+2s)²")
        self.box_r3 = self.caixa(VGroup(*r3), G.AMARELO)
        self.passo(167.4, self.aparece(r3[1]), self.aparece(r3[2]), FadeIn(self.box_r3), dur=0.6,
                   nome="= (a+b)(a−b)")
        self.passo(168.1, self.aparece(g1[6]), self.aparece(g1[7]), dur=0.5, nome="= 720")
        self.passo(171.07, self.aparece(g2a[0]), dur=0.4, nome="0,2")
        self.passo(171.6, self.aparece(g2a[1]), dur=0.3, nome="[")
        self.passo(173.0, self.aparece(g2a[2]), dur=0.5, nome="(60+4s)")
        self.passo(174.4, self.aparece(g2a[3]), dur=0.3, nome="mais")
        self.passo(174.9, self.aparece(g2a[4]), self.aparece(g2a[5]), dur=0.6, nome="(60+2s)")
        self.passo(176.4, self.aparece(g2b[0]), dur=0.3, nome="vezes")
        self.passo(176.8, self.aparece(g2b[1]), dur=0.3, nome="[")
        self.passo(177.3, self.aparece(g2b[2]), dur=0.5, nome="(60+4s)")
        self.passo(178.7, self.aparece(g2b[3]), dur=0.3, nome="menos")
        self.passo(179.4, self.aparece(g2b[4]), self.aparece(g2b[5]), dur=0.6, nome="(60+2s)")
        self.passo(181.0, self.aparece(g2b[6]), self.aparece(g2b[7]), dur=0.6, nome="= 720")

    # ================================================================ 183 – 210 s: a equação e s = 10
    def fase_equacao(self, t):
        h1 = self.linha(G.FORM["H_1"], 4.90)
        h2 = self.linha(G.FORM["H_2"], 3.70)
        h3 = self.linha(G.FORM["H_3"], 2.80, cores={0: G.VERDE, 1: G.VERDE, 2: G.VERDE})
        nota = self.tex(*G.FORM["H_1n"], escala=0.55, cor=G.CINZA)
        nota.next_to(h1[4], DOWN, buff=0.12)
        for p in nota:
            p.set_opacity(0)
        self.add(nota)
        box_s = self.caixa(VGroup(*h3), G.VERDE)
        self.passo(183.0, *[FadeOut(m) for m in self.g_rows], FadeOut(self.afe), FadeOut(self.agd),
                   dur=0.5, nome="limpa fase G")
        self.passo(184.7, self.aparece(h1[0]), dur=0.4, nome="2s")
        self.passo(186.1, self.aparece(h1[1]), dur=0.3, nome="vezes")
        self.passo(186.5, self.aparece(h1[2]), dur=0.6, nome="(120+6s)")
        self.passo(188.2, self.aparece(h1[3]), self.aparece(h1[4]), dur=0.6, nome="= 3600")
        self.passo(189.3, *[self.aparece(p) for p in nota], dur=0.5, nome="720 ÷ 0,2")
        self.passo(191.6, self.aparece(h2[0]), dur=0.4, nome="s²")
        self.passo(192.2, self.aparece(h2[1]), dur=0.4, nome="+ 20s")
        self.passo(193.1, self.aparece(h2[2]), dur=0.4, nome="− 300")
        self.passo(193.8, self.aparece(h2[3]), dur=0.4, nome="= 0")
        self.passo(202.3, *[self.aparece(p) for p in h3], FadeIn(box_s), dur=0.6, nome="s = 10")
        self.rot_resolve(204.0, 0)
        self.h_rows = [h1, h2, h3, nota, box_s]

    # ================================================================ 210 – 240 s: AC, AB, área, letra A
    def fase_final(self, t):
        i1 = self.linha(G.FORM["I_1"], 5.00)
        i2 = self.linha(G.FORM["I_2"], 4.20, cores={3: G.VERDE, 4: G.VERDE})
        i3 = self.linha(G.FORM["I_3"], 3.40, cores={5: G.VERDE, 6: G.VERDE})
        i4 = self.linha(G.FORM["I_4"], 2.60, escala=G.ESC_I4, cores={7: G.VERDE, 8: G.VERDE})
        self.passo(210.5, *[FadeOut(m) for m in self.h_rows], FadeOut(self.r3), FadeOut(self.box_r3),
                   dur=0.5, nome="limpa fase H")
        self.passo(212.6, self.aparece(i1[0]), self.aparece(i1[1]), self.anim_rot_entra(1), FadeIn(self.ov_AC),
                   dur=0.5, nome="AC =")
        self.passo(215.0, self.aparece(i1[2]), self.aparece(i1[3]), dur=0.5, nome="60 +")
        self.passo(216.3, self.aparece(i1[4]),
                   LaggedStart(*[Indicate(l, color=G.AMARELO) for l in self.s_lbl], lag_ratio=0.12),
                   dur=1.6, nome="7 espacinhos")
        self.passo(218.65, self.aparece(i2[0]), self.aparece(i2[1]), self.aparece(i2[2]), FadeOut(self.ov_AC),
                   dur=0.6, nome="60 + 70")
        self.passo(219.95, self.aparece(i2[3]), self.aparece(i2[4]), dur=0.5, nome="= 130")
        self.rot_resolve(220.6, 1)
        self.passo(221.55, self.aparece(i3[0]), self.anim_rot_entra(2), FadeIn(self.ov_AB), dur=0.4, nome="AB")
        self.passo(223.15, self.aparece(i3[1]), self.aparece(i3[2]), Indicate(self.box_r1, color=G.LARANJA,
                   scale_factor=1.06), dur=0.8, nome="= 0,4")
        self.passo(226.1, self.aparece(i3[3]), dur=0.3, nome="vezes")
        self.passo(226.9, self.aparece(i3[4]), dur=0.4, nome="130")
        self.passo(228.4, self.aparece(i3[5]), self.aparece(i3[6]), dur=0.6, nome="= 52")
        self.rot_resolve(229.5, 2)
        self.passo(230.4, self.anim_rot_entra(3), FadeOut(self.ov_AB), FadeIn(self.ov_ABC), dur=0.5,
                   nome="área de ABC")
        self.passo(231.0, self.aparece(i4[0]), self.aparece(i4[1]), dur=0.5, nome="A_ABC =")
        self.passo(232.8, self.aparece(i4[2]), dur=0.4, nome="130")
        self.passo(233.7, self.aparece(i4[3]), dur=0.3, nome="vezes")
        self.passo(234.2, self.aparece(i4[4]), dur=0.4, nome="52")
        self.passo(235.6, self.aparece(i4[5]), self.aparece(i4[6]), dur=0.6, nome="÷ 2")
        self.passo(237.4, self.aparece(i4[7]), self.aparece(i4[8]), dur=0.6, nome="= 3380")
        self.rot_resolve(238.6, 3, dur=0.4)
        # a coluna vira a lista das alternativas, com moldura verde na letra A
        alts = VGroup(*[self.tex(*p, escala=1.1) for p in G.ALT_FORM]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        alts.move_to(_v((0.0, 3.1)))
        moldura = SurroundingRectangle(alts[0], color=G.VERDE, buff=0.12, stroke_width=4)
        self.passo(239.05, *[FadeOut(m) for m in (i1, i2, i3, i4, self.b4, self.box_r1, self.ov_ABC)],
                   dur=0.3, nome="limpa fase final")
        self.passo(239.4, FadeIn(alts), dur=0.5, nome="alternativas")
        self.passo(240.0, FadeIn(moldura), dur=0.5, nome="moldura na A")

    # ================================================================ 243 – 249 s: "salva e segue"
    def encerra(self, t):
        self.pulso_marca(243.4, dur=0.8)
        self.pulso_marca(247.6, dur=0.8)
        self.ate(249.0)
        self.fim_render()
