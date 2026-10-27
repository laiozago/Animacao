# -*- coding: utf-8 -*-
"""
cena_q19.py — EsPCEx 2025, Questão 19 (geometria analítica) — @proflaiozago

Sincronizada com ESPCEX_2025_-_Q19.srt (vídeo limpo, ~1m50s). Cada passo traz o
instante da fala em segundos; troque só o número para ajustar a sincronia. O
terminal avisa no fim os passos que começaram atrasados.

    manim -pql cena_q19.py Questao19     # prévia 540x960 (com guias das zonas)
    manim -qh  cena_q19.py Questao19     # final 1080x1920 (sem guias)

Arquivos na mesma pasta: geometria.py, cena_base.py, cena_q19.py.

Layout (quadro 9x16):  palco (parte branca de cima) = plano à esquerda + contas à
direita · quadrado do rosto livre no meio-esquerda · faixa ao lado do rosto = roteiro
e marca d'água · zonas vermelhas do TikTok/Instagram intocadas.
"""
import numpy as np
from manim import *
import geometria as G
from cena_base import CenaBase, Coluna, Roteiro, p3


class Questao19(CenaBase):

    def construct(self):
        self.monta_tudo()
        # t = 0: o enunciado já está na tela (2 s sem fala para dar tempo de ler/pausar)
        self.add(self.enunciado, self.marca)
        if self.guias_ligadas():
            self.add(self.guias_prev)

        self.parte_1_enunciado_e_plano()          # 0     –  8,7 s
        self.parte_2_triangulo_e_reta()           # 8,8   – 19   s
        self.parte_3_ponto_medio()                # 19    – 40   s
        self.parte_4_mediana_altura_mediatriz()   # 40    – 63   s
        self.parte_5_coef_angular_de_AB()         # 64,7  – 78   s
        self.parte_6_coef_da_perpendicular()      # 78,5  – 87   s
        self.parte_7_valor_de_n()                 # 87,5  – 101  s
        self.parte_8_resposta()                   # 101   – 110  s
        self.ate(110.8)

    # ═════════════════════════════════════════════════════════════════════════
    # CONSTRUÇÃO (nada aparece ainda; cada parte mostra no instante certo)
    # ═════════════════════════════════════════════════════════════════════════
    def monta_tudo(self):
        self.col = Coluna(self)
        self.rot = Roteiro(self)
        self.marca = self.marca_dagua()
        self.guias_prev = self.guias()
        self.monta_enunciado()
        self.monta_plano()
        self.monta_figura()
        self.monta_roteiro()

    def monta_enunciado(self):
        """Enunciado recomposto em texto nítido (o print da prova ficaria borrado em 1080 px)."""
        corpo = Tex(
            r"\begin{minipage}{7.2cm}\raggedright\fbox{\textbf{19}}\quad "
            r"No plano cartesiano, $A(-2,1)$ e $B(4,7)$ são dois vértices de um triângulo "
            r"retângulo isósceles $ABC$. Sabendo que $\overline{AB}$ é a hipotenusa, que a abscissa "
            r"do ponto $C$ é um número positivo, e que $y=mx+n$ é a reta que passa pelo vértice $C$ "
            r"e pelo ponto médio de $\overline{AB}$, a soma $m+n$ é igual a:\end{minipage}",
            color=G.TEXTO)
        alts = Tex(r"[A] 2 \quad [B] 3 \quad [C] 4 \quad [D] 5 \quad [E] 6", color=G.TEXTO)
        bloco = VGroup(corpo, alts).arrange(DOWN, buff=0.6)
        k = min((G.PALCO.x1 - G.PALCO.x0 - 0.1) / bloco.width,
                (G.PALCO.y1 - G.PALCO.y0 - 0.3) / bloco.height)
        bloco.scale(k)
        bloco.move_to(p3((G.PALCO.x0 + G.PALCO.x1) / 2, (G.PALCO.y0 + G.PALCO.y1) / 2))
        self.enunciado = bloco

    def eixo(self, p, q):
        """Eixo com ponta de seta (de p até q)."""
        d = (q - p) / np.linalg.norm(q - p)
        n = np.array([-d[1], d[0], 0.0])
        ponta = Polygon(q, q - 0.2 * d + 0.07 * n, q - 0.2 * d - 0.07 * n,
                        color=G.EIXO, fill_opacity=1, stroke_width=0)
        return VGroup(Line(p, q - 0.1 * d, color=G.EIXO, stroke_width=2.5), ponta)

    def monta_plano(self):
        """Grade clara + eixos + poucos números. Escala igual nos dois eixos."""
        P = lambda x, y: p3(*G.para_tela(x, y))
        x0, x1 = G.DOM_X
        y0, y1 = G.DOM_Y
        g = VGroup()
        for x in range(int(x0), int(x1) + 1):
            g.add(Line(P(x, y0), P(x, y1), color=G.GRADE, stroke_width=1.2))
        for y in range(0, int(y1) + 1):
            g.add(Line(P(x0, y), P(x1, y), color=G.GRADE, stroke_width=1.2))
        g.add(self.eixo(P(x0, 0), P(x1, 0)), self.eixo(P(0, y0), P(0, y1)))
        for k in ("nx-2", "nx2", "nx4", "ny2", "ny4", "ny6"):
            g.add(self.rotulo(k, cor=G.CINZA, fundo=False))
        for k in ("eixo_x", "eixo_y"):
            g.add(self.rotulo(k, cor=G.EIXO, fundo=False))
        self.plano = g

    def angulo_reto(self, v, d1, d2, tam, cor):
        """Símbolo de ângulo reto no vértice v, entre as direções d1 e d2."""
        d1 = d1 / np.linalg.norm(d1)
        d2 = d2 / np.linalg.norm(d2)
        m = VMobject()
        m.set_points_as_corners([v + tam * d1, v + tam * (d1 + d2), v + tam * d2])
        m.set_stroke(cor, 3.5)
        m.set_fill(opacity=0)
        return m

    def tique(self, p, q):
        """Marquinha dupla no meio do segmento pq (lados iguais)."""
        meio = (p + q) / 2
        d = (q - p) / np.linalg.norm(q - p)
        n = np.array([-d[1], d[0], 0.0])
        return VGroup(*[Line(meio + s * 0.05 * d - 0.09 * n, meio + s * 0.05 * d + 0.09 * n,
                             color=G.CINZA, stroke_width=3) for s in (-1, 1)])

    def monta_figura(self):
        T = lambda p: p3(*G.para_tela(*p))
        pA, pB, pC, pM = T(G.A), T(G.B), T(G.C), T(G.M)
        r0, r1 = G.reta_visivel(G.RETA_M, G.RETA_N)

        # pontos dados e segmento AB (vermelho = hipotenusa; nasce neutro)
        self.dA = Dot(pA, radius=0.075, color=G.TEXTO)
        self.dB = Dot(pB, radius=0.075, color=G.TEXTO)
        self.rA, self.rB = self.rotulo("A"), self.rotulo("B")
        self.AB = Line(pA, pB, color=G.TEXTO, stroke_width=5)

        # triângulo ABC (cinza, neutro) + ângulo reto em C + lados iguais
        self.tri_fundo = Polygon(pA, pB, pC, color=G.CINZA, fill_opacity=0.08, stroke_width=0)
        self.AC = Line(pA, pC, color=G.CINZA, stroke_width=3)
        self.BC = Line(pB, pC, color=G.CINZA, stroke_width=3)
        self.dC = Dot(pC, radius=0.075, color=G.TEXTO)
        self.rC = self.rotulo("C")
        self.ang_C = self.angulo_reto(pC, pA - pC, pB - pC, G.R_ANG, G.LARANJA)
        self.tiques = VGroup(self.tique(pA, pC), self.tique(pB, pC))

        # a reta y = mx + n (amarelo = altura/mediatriz) e o rótulo que muda
        self.reta = Line(T(r0), T(r1), color=G.AMARELO, stroke_width=3.5)
        self.rReta0 = self.rotulo("reta0", G.AMARELO)
        self.rReta1 = self.rotulo("reta1", G.AMARELO)
        self.rReta2 = self.rotulo("reta2", G.AMARELO)

        # ponto médio (vermelho = falta descobrir → verde = resolvido)
        self.dM = Dot(pM, radius=0.085, color=G.VERMELHO)
        self.rM0 = self.rotulo("M0", G.VERMELHO)
        self.rM1 = self.rotulo("M1", G.VERDE)

        # mediana CM (destaque grosso) e o ângulo de 90° em M (entre MB e a reta, para cima)
        self.CM = Line(pC, pM, color=G.AMARELO, stroke_width=8)
        cima_esq = T(r0) - pM
        self.ang_M = self.angulo_reto(pM, pB - pM, cima_esq, 0.2, G.LARANJA)
        self.rAng = self.rotulo("ang", G.LARANJA)

        # catetos "de inclinação" (Δy e Δx) em azul
        self.perna_v = Line(pC, pB, color=G.AZUL, stroke_width=5)
        self.perna_h = Line(pA, pC, color=G.AZUL, stroke_width=5)
        self.rSeisV = self.rotulo("seis_v", G.AZUL)
        self.rSeisH = self.rotulo("seis_h", G.AZUL)

        # intercepto n na reta (0, 5)
        self.dN = Dot(T((0, G.RETA_N)), radius=0.085, color=G.VERDE)
        self.rN = self.rotulo("n", G.VERDE)

        # camadas: linhas < pontos < ângulos < rótulos
        self.tri_fundo.set_z_index(1)
        for m in (self.AB, self.AC, self.BC, self.tiques, self.perna_v, self.perna_h):
            m.set_z_index(2)
        self.reta.set_z_index(3)
        self.CM.set_z_index(3)
        for m in (self.ang_C, self.ang_M):
            m.set_z_index(4)
        for m in (self.dA, self.dB, self.dC, self.dM, self.dN):
            m.set_z_index(5)
        for m in (self.rA, self.rB, self.rC, self.rM0, self.rM1, self.rReta0, self.rReta1,
                  self.rReta2, self.rAng, self.rSeisV, self.rSeisH, self.rN):
            m.set_z_index(6)

    def monta_roteiro(self):
        self.rot.novo("soma", r"m+n=?", r"m+n=4")
        self.rot.novo("M", r"M=?", r"M=(1,4)")
        self.rot.novo("m", r"m=?", r"m=-1")
        self.rot.novo("n", r"n=?", r"n=5")

    # ═════════════════════════════════════════════════════════════════════════
    # SEQUÊNCIA (instantes em segundos, do SRT limpo)
    # ═════════════════════════════════════════════════════════════════════════
    def parte_1_enunciado_e_plano(self):
        # 0 → 6,3 s: só o enunciado na tela
        self.passo(6.3, FadeOut(self.enunciado), FadeIn(self.plano), dur=0.6)   # "olha só"
        self.passo(7.0, FadeIn(self.dA), FadeIn(self.rA), dur=0.4)              # "temos A"
        self.passo(7.6, FadeIn(self.dB), FadeIn(self.rB), dur=0.4)              # "e B"
        self.passo(8.2, Create(self.AB), dur=0.5)                               # "e o segmento"

    def parte_2_triangulo_e_reta(self):
        self.passo(8.8, self.AB.animate.set_color(G.VERMELHO), dur=0.5)         # "AB é a hipotenusa"
        self.passo(10.4, FadeIn(self.tri_fundo), Create(self.AC), Create(self.BC),
                   FadeIn(self.dC), FadeIn(self.rC), dur=0.7)                   # "de um triângulo"
        self.passo(11.2, FadeIn(self.ang_C), dur=0.3)                           # "retângulo"
        self.passo(11.6, FadeIn(self.tiques), dur=0.4)                          # "isósceles"
        self.passo(12.2, Create(self.reta), FadeIn(self.rReta0), dur=1.2)       # "a reta passa por C e pelo ponto médio"
        self.passo(15.9, self.rot.mostra("soma"),
                   Indicate(self.rReta0[1], scale_factor=1.15, color=G.AMARELO),
                   dur=0.6)                                                     # "querendo m + n"
        self.passo(17.3, self.rot.mostra("M"), dur=0.5)                         # "primeiro vamos achar o ponto médio"
        self.passo(19.0, FadeIn(self.dM), FadeIn(self.rM0), dur=0.5)            # "aí o ponto médio"

    def parte_3_ponto_medio(self):
        col = self.col
        # linhas criadas já na posição final (x e y em dois blocos)
        x1 = col.linha(r"x_M=", r"\frac{x_A+x_B}{2}")
        x2 = col.linha(r"\phantom{x_M}=", r"\frac{2}{2}", [(r"=1", G.VERDE)], folga=0.3)
        y1 = col.linha(r"y_M=", r"\frac{y_A+y_B}{2}")
        y2 = col.linha(r"\phantom{y_M}=", r"\frac{8}{2}", [(r"=4", G.VERDE)], folga=0.3)
        res = col.linha([(r"M=(1,4)", G.VERDE)])
        xn = col.sobre(x1[1], r"\frac{-2+4}{2}")
        yn = col.sobre(y1[1], r"\frac{1+7}{2}")

        self.passo(23.3, FadeIn(x1[0]), FadeIn(x1[1]), dur=0.5)                 # "x de um com x do outro / 2"
        self.passo(25.6, FadeIn(y1[0]), FadeIn(y1[1]), dur=0.5)                 # "y de um mais y do outro / 2"
        self.passo(28.3, ReplacementTransform(x1[1], xn), dur=0.5)              # "−2 mais 4"
        self.passo(30.67, FadeIn(x2[0]), FadeIn(x2[1]), dur=0.35)               # "tá dois"
        self.passo(31.33, FadeIn(x2[2]), dur=0.35)                              # "a metade é um"
        self.passo(32.5, ReplacementTransform(y1[1], yn), dur=0.5)              # "a soma das ordenadas y"
        self.passo(35.0, FadeIn(y2[0]), FadeIn(y2[1]), dur=0.4)                 # "dá oito"
        self.passo(35.9, FadeIn(y2[2]), dur=0.4)                                # "a metade é quatro"
        self.passo(37.13, FadeIn(res[0]), self.dM.animate.set_color(G.VERDE),
                   FadeOut(self.rM0), FadeIn(self.rM1), self.rot.resolve("M"),
                   dur=0.6)                                                     # "ponto médio = (1, 4)"
        self.passo(39.9, *col.limpa(), dur=0.5)                                 # "agora vem o pulo do gato"

    def parte_4_mediana_altura_mediatriz(self):
        col = self.col
        l1 = col.linha([(r"\overline{CM}", G.AMARELO), (r"=\text{mediana}", G.TEXTO)])
        l2 = col.linha(r"\phantom{\overline{CM}}=\text{altura}")
        l3 = col.linha(r"\phantom{\overline{CM}}=\text{mediatriz}", folga=0.4)
        l4 = col.linha([(r"\overline{CM}", G.AMARELO), (r"\perp", G.TEXTO), (r"\overline{AB}", G.VERMELHO)])

        self.passo(40.9, Indicate(self.ang_C, scale_factor=1.7, color=G.LARANJA), dur=0.7)  # "triângulo retângulo isósceles"
        self.passo(43.4, Create(self.CM), FadeIn(l1[0]), dur=1.0)               # "a mediana: de C ao meio da hipotenusa"
        self.passo(48.4, FadeIn(l2[0]), dur=0.5)                                # "também é a altura"
        self.passo(50.3, FadeIn(l4[0]), FadeIn(self.ang_M), dur=0.5)            # "CM é perpendicular a AB"
        self.passo(56.7, FadeIn(self.rAng), dur=0.4)                            # "ângulo de 90 graus"
        self.passo(59.4, FadeIn(l3[0]), self.reta.animate.set_stroke(width=5.5), dur=0.5)  # "é a mediatriz"
        self.passo(61.7, FadeOut(self.dC), FadeOut(self.rC), FadeOut(self.AC), FadeOut(self.BC),
                   FadeOut(self.tri_fundo), FadeOut(self.ang_C), FadeOut(self.tiques),
                   FadeOut(self.CM), dur=0.6)                                   # "então esquece o C"
        self.passo(62.9, *col.limpa(), dur=0.5)                                 # "já sabemos tudo que precisa"

    def parte_5_coef_angular_de_AB(self):
        col = self.col
        c1 = col.linha(r"m_{AB}=", r"\frac{\Delta y}{\Delta x}")
        c2 = col.linha(r"\phantom{m_{AB}}=", r"\frac{7-1}{4-(-2)}")
        c3 = col.linha(r"\phantom{m_{AB}}=", r"\frac{6}{6}", [(r"=1", G.VERDE)])

        self.passo(64.7, FadeIn(c1[0]), dur=0.4)                                # "coeficiente angular de AB"
        self.passo(66.2, FadeIn(c1[1]), dur=0.5)                                # "variação de y / variação de x"
        self.passo(69.3, Create(self.perna_v), FadeIn(c2[0]), FadeIn(c2[1]), dur=0.8)  # "sete menos um"
        self.passo(70.3, FadeIn(self.rSeisV), dur=0.4)                          # "dá seis"
        self.passo(71.4, Create(self.perna_h), dur=0.8)                         # "a variação de x é 4 …"
        self.passo(73.8, FadeIn(self.rSeisH), dur=0.4)                          # "… menos (−2), que dá seis"
        self.passo(75.3, FadeIn(c3[0]), FadeIn(c3[1]), dur=0.4)                 # "seis sobre seis"
        self.passo(76.5, FadeIn(c3[2]), dur=0.4)                                # "dá um"
        self.passo(78.5, FadeOut(self.perna_v), FadeOut(self.perna_h),
                   FadeOut(self.rSeisV), FadeOut(self.rSeisH), *col.limpa(),
                   self.rot.mostra("m"), dur=0.4)                               # "agora … da reta perpendicular"

    def parte_6_coef_da_perpendicular(self):
        col = self.col
        d0 = col.linha([(r"m_{AB}=1", G.VERDE)])
        d1 = col.linha(r"m=-\frac{1}{m_{AB}}")
        d2 = col.linha(r"m=-\frac{1}{1}", [(r"=-1", G.VERDE)])

        self.passo(79.0, FadeIn(d0[0]), dur=0.4)                                # (lembrete do que acabou de achar)
        self.passo(81.4, FadeIn(d1[0]), dur=0.5)                                # "o inverso do oposto"
        self.passo(83.3, FadeIn(d2[0]), dur=0.5)                                # "no nosso caso: o m da nossa reta"
        self.passo(85.6, Indicate(self.rot.itens["m"][0], scale_factor=1.15, color=G.VERMELHO),
                   dur=0.6)                                                     # "o que a gente tá querendo"
        self.passo(86.5, FadeIn(d2[1]), self.rot.resolve("m"), dur=0.5)         # "é o menos um"

    def parte_7_valor_de_n(self):
        col = self.col
        self.passo(87.5, *col.limpa(), dur=0.4)                                 # "agora que a gente já sabe …"
        e1 = col.linha(r"y=-x+n")
        e2 = col.linha([(r"x=1", G.VERDE), (r",\;", G.TEXTO), (r"y=4", G.VERDE)])
        e3 = col.linha([(r"4", G.VERDE), (r"=-", G.TEXTO), (r"1", G.VERDE), (r"+n", G.TEXTO)])
        e4 = col.linha(r"4+1=n")
        e5 = col.linha([(r"n=5", G.VERDE)])

        self.passo(90.4, FadeIn(e1[0]), FadeOut(self.rReta0), FadeIn(self.rReta1), dur=0.5)  # "y = −x + n"
        self.passo(92.6, Indicate(self.dM, scale_factor=1.9, color=G.VERDE), dur=0.6)       # "passa pelo ponto (1, 4)"
        self.passo(94.2, FadeIn(e2[0]), dur=0.5)                                # "substituir o x e o y por 1 e por 4"
        self.passo(96.13, FadeIn(e3[0]), self.rot.mostra("n"), dur=0.5)         # "pra calcular o valor de n"
        self.passo(98.7, FadeIn(e4[0]), dur=0.4)                                # "vai pra lá"
        self.passo(99.87, FadeIn(e5[0]), self.rot.resolve("n"),
                   FadeIn(self.dN), FadeIn(self.rN),
                   FadeOut(self.rReta1), FadeIn(self.rReta2), dur=0.6)          # "n é igual a cinco"

    def parte_8_resposta(self):
        col = self.col
        self.passo(101.07, *col.limpa(), dur=0.4)                               # "agora respondendo a pergunta"
        f1 = col.linha(r"m+n=", [(r"-1", G.VERDE), (r"+", G.TEXTO), (r"5", G.VERDE)])
        f2 = col.linha(r"\phantom{m+n}=", [(r"4", G.VERDE)], folga=0.35)
        opcoes = [col.linha(r"\text{[%s]}\;%d" % (letra, valor), escala=0.7, folga=0.1)[0]
                  for letra, valor in G.ALTERNATIVAS]

        self.passo(102.67, FadeIn(f1[0]), dur=0.4)                              # "quanto que é m + n"
        self.passo(104.17, FadeIn(f1[1]), dur=0.4)                              # "menos um mais cinco"
        self.passo(105.2, FadeIn(f2[0]), FadeIn(f2[1]), self.rot.resolve("soma"), dur=0.5)  # "que é igual a quatro"
        self.passo(105.9, *[FadeIn(o) for o in opcoes], dur=0.5)                # "alternativa"
        i = [letra for letra, _ in G.ALTERNATIVAS].index(G.LETRA_CORRETA)
        moldura = SurroundingRectangle(opcoes[i], color=G.VERDE, buff=0.12, stroke_width=4)
        self.passo(106.53, Create(moldura), opcoes[i].animate.set_color(G.VERDE),
                   *[o.animate.set_opacity(0.25) for k, o in enumerate(opcoes) if k != i],
                   dur=0.6)                                                     # "letra C"
        self.passo(109.07, Indicate(self.marca, scale_factor=1.3, color=G.AZUL), dur=0.8)  # "salva esse vídeo, segue"
