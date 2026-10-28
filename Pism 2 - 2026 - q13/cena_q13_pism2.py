# -*- coding: utf-8 -*-
"""
PISM II 2026 - Questão 13 (cone de areia ÷ barril cilíndrico) - @proflaiozago
Resposta: N = 25π ÷ (π/5) = 125 barris  -> letra C.

Sincronizada com "PISM II - 2026 - Q13.srt" (~1m37s). Cada passo traz o instante da fala (s).
Se o terminal avisar passos atrasados no fim do render, troque só o número do instante.

  prévia (540x960, com guias):  manim -pql cena_q13_pism2.py QuestaoPism13
  final  (1080x1920, sem guias): manim -qh  cena_q13_pism2.py QuestaoPism13

No SRT o π foi transcrito como "e" / "três" (ex.: "três vezes o um sobre dois ao quadrado");
aqui está como π, que é o que o professor fala.
"""
from cena_base import *
import geometria as G


class QuestaoPism13(CenaBase):

    def construct(self):
        self.marca_dagua()
        self.guias()
        self.monta_figuras()
        self.abertura()           # 0 - 4,6   enunciado integral da prova
        self.figuras()            # 4,7 - 11,4  cone e barril com os dados
        self.objetivo()           # 12,4 - 16,5  N = V_cone ÷ V_barril
        self.volume_cone()        # 16,9 - 37,6
        self.barril_unidades()    # 37,9 - 60,5  raio e altura do barril
        self.volume_barril()      # 66,4 - 79,8
        self.divisao()            # 79,9 - 92,4
        self.final()              # 92,5 - 97,1  alternativas, letra C, "salva e segue"

    # ------------------------------------------------------------------ objetos (sem tocar)
    def arco(self, cx, cy, a, b, t0, t1):
        return ParametricFunction(lambda t: P(cx + a * np.cos(t), cy + b * np.sin(t)),
                                  t_range=[t0, t1, 0.05], color=G.TEXTO, stroke_width=4)

    def rotulo_fig(self, tex, chave, cor, escala=None):
        m = self.tex(tex, cor=cor, escala=escala or G.ESC["rotulo"])
        return m.move_to(P(*G.POS[chave]))

    def monta_figuras(self):
        # cone: duas geratrizes, base (frente cheia, fundo tracejado), altura tracejada e raio
        ax, ay = G.CONE["centro"]
        px, py = G.CONE["apice"]
        rx, ry = G.CONE["rx"], G.CONE["ry"]
        lados = [Line(P(ax - rx, ay), P(px, py), color=G.TEXTO, stroke_width=4),
                 Line(P(ax + rx, ay), P(px, py), color=G.TEXTO, stroke_width=4)]
        frente = self.arco(ax, ay, rx, ry, PI, TAU)
        fundo = DashedVMobject(self.arco(ax, ay, rx, ry, 0, PI), num_dashes=16)
        self.c_corpo = VGroup(*lados, frente, fundo)
        self.c_altura = DashedLine(P(px, py), P(ax, ay), color=G.AMARELO, stroke_width=4)
        self.c_raio = Line(P(ax, ay), P(ax + rx, ay), color=G.AZUL, stroke_width=6)
        self.c_r_rot = self.rotulo_fig(G.ROTULOS["r_cone"], "r_cone", G.AZUL)
        self.c_h_rot = self.rotulo_fig(G.ROTULOS["h_cone"], "h_cone", G.AMARELO)
        # barril: topo (elipse inteira), laterais, fundo (só a frente), cota da altura
        bx, yt, yb = G.BARRIL["cx"], G.BARRIL["y_topo"], G.BARRIL["y_base"]
        brx, bry = G.BARRIL["rx"], G.BARRIL["ry"]
        topo = Ellipse(width=2 * brx, height=2 * bry, color=G.TEXTO, stroke_width=4).move_to(P(bx, yt))
        base = self.arco(bx, yb, brx, bry, PI, TAU)
        paredes = [Line(P(bx - brx, yt), P(bx - brx, yb), color=G.TEXTO, stroke_width=4),
                   Line(P(bx + brx, yt), P(bx + brx, yb), color=G.TEXTO, stroke_width=4)]
        self.b_corpo = VGroup(topo, base, *paredes)
        self.b_d_linha = Line(P(bx - brx, yt), P(bx + brx, yt), color=G.LARANJA, stroke_width=5)
        self.b_r_linha = Line(P(bx, yt), P(bx + brx, yt), color=G.AZUL, stroke_width=6)
        xc = G.X_COTA_BARRIL
        self.b_cota = VGroup(Line(P(xc, yb), P(xc, yt)), Line(P(xc - .08, yb), P(xc + .08, yb)),
                             Line(P(xc - .08, yt), P(xc + .08, yt))).set_color(G.AMARELO).set_stroke(width=4)
        self.b_d_rot = self.rotulo_fig(G.ROTULOS["d"], "d", G.LARANJA)
        # rótulos que se sucedem no mesmo lugar (ReplacementTransform): r = ? -> 0,5 -> 1/2 ; 80 cm -> ... -> 4/5 m
        r_cores = [G.VERMELHO, G.VERDE, G.VERDE]
        self.b_r_rot = [self.rotulo_fig(s, "r_barril", c, G.ESC["r_barril"])
                        for s, c in zip(G.ROTULOS["r_seq"], r_cores)]
        h_cores = [G.AMARELO, G.AMARELO, G.AMARELO, G.VERDE]
        self.b_h_rot = [self.rotulo_fig(s, "h_barril", c) for s, c in zip(G.ROTULOS["h_seq"], h_cores)]

    # ------------------------------------------------------------------ 0 - 4,6 s
    def abertura(self):
        self.enun = self.enunciado()
        self.passo(0.0, FadeIn(self.enun), dur=0.8, nome="enunciado")
        self.passo(4.2, FadeOut(self.enun), dur=0.4, nome="enunciado sai")

    # ------------------------------------------------------------------ 4,7 - 11,4 s
    def figuras(self):
        # "é um cone com cinco metros de raio e três metros de altura"
        self.passo(4.7, Create(self.c_corpo), dur=0.9, nome="cone")
        self.passo(5.75, Create(self.c_raio), FadeIn(self.c_r_rot), dur=0.5, nome="raio 5 m")
        self.passo(6.65, Create(self.c_altura), FadeIn(self.c_h_rot), dur=0.5, nome="altura 3 m")
        # "e o barril cilíndrico, um metro de diâmetro e oitenta centímetros de altura"
        self.passo(8.15, Create(self.b_corpo), dur=0.9, nome="barril")
        self.passo(9.8, Create(self.b_d_linha), FadeIn(self.b_d_rot), dur=0.5, nome="d = 1 m")
        self.passo(10.75, Create(self.b_cota), FadeIn(self.b_h_rot[0]), dur=0.6, nome="80 cm")

    # ------------------------------------------------------------------ 12,4 - 16,5 s
    def objetivo(self):
        # "dividir o volume do cone pelo volume do cilindro"  ->  N = V_cone ÷ V_barril
        self.l_n = self.linha(G.LINHAS["n"], G.Y_N, x_esq=G.X_CONTA)
        n = self.l_n
        self.passo(12.4, *self.aparece(n[0], n[1]), self.anim_rot_entra("n"), dur=0.5, nome="N =")
        self.passo(14.6, *self.aparece(n[2]), self.anim_rot_entra("vcone"), dur=0.4, nome="V_cone")
        self.passo(15.05, *self.aparece(n[3]), dur=0.4, nome="dividido")
        self.passo(15.95, *self.aparece(n[4]), self.anim_rot_entra("vbarril"), dur=0.5, nome="V_barril")

    # ------------------------------------------------------------------ 16,9 - 37,6 s
    def volume_cone(self):
        n = self.l_n
        # "o volume do cone": o barril vira contexto (cinza), V_cone em destaque
        self.passo(16.9, self.b_corpo.animate.set_color(G.CINZA), self.pulso(n[2]), dur=0.7,
                   nome="foco no cone")
        # regras: corpo piramidal -> 1/3·A_b·h ; chão = teto -> A_b·h  (duas células lado a lado)
        amarelo = lambda k: {i: G.AMARELO for i in range(k)}
        rc = self.linha(G.LINHAS["regra_cone"], G.Y_REGRA, escala=G.ESC["regra"], cx=G.X_REGRA[0],
                        cores=amarelo(4))
        rt = self.linha(G.LINHAS["regra_cil"], G.Y_REGRA, escala=G.ESC["regra"], cx=G.X_REGRA[1],
                        cores=amarelo(3))
        rt.shift(UP * (rc[0].get_center()[1] - rt[0].get_center()[1]))   # "V =" das duas regras na mesma altura
        r1 = self.ajusta(self.texto(G.ROTULO_REGRA[0], cor=G.AMARELO, escala=0.45), G.LARG_REGRA[0])
        r2 = self.ajusta(self.texto(G.ROTULO_REGRA[1], cor=G.AMARELO, escala=0.45), G.LARG_REGRA[1])
        r1.move_to(P(G.X_REGRA[0], G.Y_REGRA_ROT))
        r2.move_to(P(G.X_REGRA[1], G.Y_REGRA_ROT))
        self.painel += [r1, r2]
        self.passo(19.5, *self.aparece(rc[0]), FadeIn(r1), dur=0.5, nome="regra cone: V =")
        self.passo(20.15, *self.aparece(rc[1]), dur=0.4, nome="um terço")
        self.passo(20.7, *self.aparece(rc[2]), dur=0.4, nome="área da base")
        self.passo(21.5, *self.aparece(rc[3]), dur=0.4, nome="vezes a altura")
        self.passo(24.0, FadeIn(r2), dur=0.5, nome="chão = teto")
        self.passo(25.5, *self.aparece(rt[0]), dur=0.4, nome="regra cilindro: V =")
        self.passo(26.3, *self.aparece(rt[1]), dur=0.4, nome="área da base (2)")
        self.passo(27.0, *self.aparece(rt[2]), dur=0.4, nome="vezes a altura (2)")
        # conta do cone: V = 1/3 · π · 5² · 3  ->  25π m³
        c1 = self.linha(G.LINHAS["cone1"], G.Y_CONE[0], x_esq=G.X_CONTA)
        c2 = self.linha(G.LINHAS["cone2"], G.Y_CONE[1], cores={0: G.VERDE, 1: G.VERDE, 2: G.VERDE})
        self.alinha_igual(c2, c1)
        self.passo(28.7, *self.aparece(c1[0], c1[1]), dur=0.4, nome="V_cone =")
        self.passo(29.7, *self.aparece(c1[2]), dur=0.35, nome="1/3")
        self.passo(30.35, *self.aparece(c1[3]), dur=0.35, nome="· π")
        self.passo(31.3, *self.aparece(c1[4]), dur=0.35, nome="· 5²")
        self.passo(32.5, *self.aparece(c1[5]), dur=0.35, nome="· 3")
        # "um terço corta com aquele três"
        k1 = self.corte(c1[2])
        tres = self.glifo(c1[5], "dir")
        k2 = self.corte(tres)
        self.passo(33.4, Create(k1), c1[2].animate.set_color(G.CINZA), dur=0.4, nome="corta 1/3")
        self.passo(34.25, Create(k2), tres.animate.set_color(G.CINZA), dur=0.4, nome="corta 3")
        # "sobra vinte e cinco pi, metros cúbicos"
        self.passo(35.2, *self.aparece(c2[0]), dur=0.4, nome="= 25")
        self.passo(35.75, *self.aparece(c2[1]), dur=0.3, nome="π")
        self.passo(36.4, *self.aparece(c2[2]), dur=0.4, nome="m³")
        self.roteiro_resolve(36.9, "vcone", dur=0.7)
        self.conta_cone = [c1, c2, k1, k2]

    # ------------------------------------------------------------------ 37,9 - 60,5 s
    def barril_unidades(self):
        # "agora o barril": a conta do cone sai, o cone vira contexto e o barril volta ao normal
        self.passo(37.9, *self.sai(self.conta_cone), self.c_corpo.animate.set_color(G.CINZA),
                   self.b_corpo.animate.set_color(G.TEXTO), dur=0.6, nome="agora o barril")
        # "prestar atenção: a informação foi o diâmetro"
        self.passo(41.4, self.pulso(self.b_d_linha), self.pulso(self.b_d_rot), dur=0.8, nome="atenção: diâmetro")
        # "então o raio dele é zero vírgula cinco, um sobre dois"
        self.passo(43.3, Create(self.b_r_linha), FadeIn(self.b_r_rot[0]), dur=0.5, nome="raio?")
        self.passo(44.5, ReplacementTransform(self.b_r_rot[0], self.b_r_rot[1]), dur=0.5, nome="r = 0,5")
        self.passo(45.7, ReplacementTransform(self.b_r_rot[1], self.b_r_rot[2]), dur=0.5, nome="r = 1/2")
        # "a altura veio em centímetros, passa pra metros: 0,8 m = 8/10 = 4/5"
        self.passo(48.6, self.pulso(self.b_h_rot[0]), dur=0.8, nome="atenção: centímetros")
        self.passo(55.2, ReplacementTransform(self.b_h_rot[0], self.b_h_rot[1]), dur=0.6, nome="0,8 m")
        self.passo(58.4, ReplacementTransform(self.b_h_rot[1], self.b_h_rot[2]), dur=0.5, nome="8/10")
        self.passo(59.9, ReplacementTransform(self.b_h_rot[2], self.b_h_rot[3]), dur=0.6, nome="4/5 m")

    # ------------------------------------------------------------------ 66,4 - 79,8 s
    def volume_barril(self):
        # V = π · (1/2)² · 4/5  ->  π · 1/4 · 4/5  ->  π/5 m³
        b1 = self.linha(G.LINHAS["barril1"], G.Y_BARRIL[0], x_esq=G.X_CONTA)
        b2 = self.linha(G.LINHAS["barril2"], G.Y_BARRIL[1])
        b3 = self.linha(G.LINHAS["barril3"], G.Y_BARRIL[2], cores={0: G.VERDE, 1: G.VERDE})
        self.alinha_igual(b2, b1)
        self.alinha_igual(b3, b1)
        self.passo(66.4, *self.aparece(b1[0], b1[1]), dur=0.4, nome="V_barril =")
        self.passo(67.75, *self.aparece(b1[2]), dur=0.3, nome="π")
        self.passo(68.5, *self.aparece(b1[3]), dur=0.5, nome="(1/2)²")
        self.passo(70.1, *self.aparece(b1[4]), dur=0.5, nome="· 4/5")
        self.passo(72.0, *self.aparece(b2[0]), dur=0.3, nome="= π")
        self.passo(72.45, *self.aparece(b2[1]), dur=0.4, nome="· 1/4")
        self.passo(72.95, *self.aparece(b2[2]), dur=0.4, nome="· 4/5 (desce)")
        # "esse quatro corta com o quatro do quatro sobre cinco"
        q1 = self.glifo(b2[1], "baixo")
        q2 = self.glifo(b2[2], "cima")
        k1 = self.corte(q1)
        k2 = self.corte(q2)
        self.passo(73.5, Create(k1), q1.animate.set_color(G.CINZA), dur=0.4, nome="corta o 4 de baixo")
        self.passo(74.2, Create(k2), q2.animate.set_color(G.CINZA), dur=0.4, nome="corta o 4 de cima")
        # "fica com π sobre cinco, metros cúbicos"
        self.passo(77.45, *self.aparece(b3[0]), dur=0.5, nome="= π/5")
        self.passo(78.75, *self.aparece(b3[1]), dur=0.4, nome="m³ (barril)")
        self.roteiro_resolve(79.2, "vbarril", dur=0.6)

    # ------------------------------------------------------------------ 79,9 - 92,4 s
    def divisao(self):
        # "dividir um pelo outro": 25π ÷ π/5 -> repete a primeira, multiplica pelo inverso da segunda
        self.passo(79.9, *self.sai([m for m in self.painel if m is not self.l_n]), dur=0.5,
                   nome="limpa o painel")
        d1 = self.linha(G.LINHAS["div1"], G.Y_DIV[0], escala=G.ESC["div"], x_esq=G.X_CONTA)
        d2 = self.linha(G.LINHAS["div2"], G.Y_DIV[1], escala=G.ESC["div"])
        d3 = self.linha(G.LINHAS["div3"], G.Y_DIV[2], escala=G.ESC["div"], cores={0: G.VERDE, 1: G.VERDE})
        self.alinha_igual(d2, d1)
        self.alinha_igual(d3, d1)
        self.passo(80.5, *self.aparece(d1[0], d1[1]), dur=0.4, nome="N =")
        self.passo(81.85, *self.aparece(d1[2]), dur=0.5, nome="25π")
        self.passo(82.5, *self.aparece(d1[3]), dur=0.3, nome="÷")
        self.passo(83.0, *self.aparece(d1[4]), dur=0.5, nome="π/5")
        self.passo(84.0, self.pulso(d1[2]), dur=0.6, nome="repete a primeira")
        self.passo(85.3, self.pulso(d1[4]), dur=0.6, nome="inverso da segunda")
        self.passo(86.0, *self.aparece(d2[0]), dur=0.4, nome="= 25π")
        self.voa_copia(86.95, d1[4], d2[1], dur=0.8)
        # "e aí a gente chega em cento e vinte e cinco": π corta com π
        p1 = self.glifo(d2[0], "dir")
        p2 = self.glifo(d2[1], "baixo")
        k1 = self.corte(p1)
        k2 = self.corte(p2)
        self.passo(88.4, Create(k1), Create(k2), p1.animate.set_color(G.CINZA), p2.animate.set_color(G.CINZA),
                   dur=0.5, nome="corta os π")
        self.passo(89.2, *self.aparece(d3[0]), dur=0.4, nome="= 125")
        self.roteiro_resolve(90.1, "n", dur=0.7)
        self.passo(92.1, *self.aparece(d3[1]), dur=0.3, nome="barris")

    # ------------------------------------------------------------------ 92,5 - 97,1 s
    def final(self):
        # alternativas, moldura verde na letra C, pulso na marca d'água ("salva e segue")
        self.passo(92.5, *self.sai(), dur=0.3, nome="limpa o painel (fim)")
        linhas = []
        for (letra, val), y in zip(G.ALTERNATIVAS, G.Y_ALT):
            m = MathTex(r"\text{(%s)}" % letra, r"\ " + val, color=G.TEXTO).scale(G.ESC["alt"])
            m.move_to(P(G.X_ALT, y), aligned_edge=LEFT)
            linhas.append(m)
        certa = linhas["ABCDE".index(G.LETRA)]
        self.passo(92.8, LaggedStart(*[FadeIn(m, shift=0.2 * LEFT) for m in linhas], lag_ratio=0.15),
                   dur=0.7, nome="alternativas")
        moldura = SurroundingRectangle(certa, color=G.VERDE, buff=0.15, corner_radius=0.12, stroke_width=5)
        self.passo(93.55, Create(moldura), certa.animate.set_color(G.VERDE), dur=0.4, nome="letra C")
        self.passo(94.0, self.pulso(self.marca, G.AZUL, 1.25), dur=0.7, nome="salva")
        self.passo(96.1, self.pulso(self.marca, G.AZUL, 1.25), dur=0.7, nome="segue")
        self.ate(97.1)
