"""EsPCEx 2025 - Questão 18 (prisma hexagonal) | @proflaiozago

Animação SINCRONIZADA com a fala (ESPECEX_2025_-_Q18.srt, já limpo).
Parte da figura como aparece na prova e vai resolvendo junto com o professor.
Reaproveita tudo de cena_prisma.py (câmera, wireframe, painel, roteiro).

    manim -pql cena_q18.py Questao18     # prévia 540x960
    manim -pqh cena_q18.py Questao18     # final 1080x1920

Cada evento abaixo tem o instante (em segundos) em que a frase COMEÇA no SRT.
Se um passo ficar adiantado/atrasado, ajuste só o número do tempo; ao final da
renderização o terminal lista os passos que começaram atrasados.
"""
import numpy as np
from manim import *
from pathlib import Path

config.media_dir = str(Path(__file__).resolve().parent / "media")

from cena_prisma import PrismaHexagonal, ESCALA
from geometria import (H, K_D, K_M, FUNDO, AZUL, AMARELO, VERMELHO, VERDE, LARANJA,
                       CINZA, PALETA6, mistura)

ELEV_PROVA = np.radians(12.0)        # a figura da prova é vista quase de lado
YAW_PROVA = 0.0
YAW_CIMA, ELEV_CIMA = np.radians(60.0), np.pi / 2
YAW_FRENTE, ELEV_FRENTE = np.radians(60.0), 0.0
YAW_FINAL, ELEV_FINAL = np.radians(25.0), np.radians(22.0)


class Questao18(PrismaHexagonal):
    """Volume do prisma: 216*sqrt(3) cm^3 (letra D)."""

    # ------------------------------------------------------------------
    # relógio da fala
    # ------------------------------------------------------------------
    def ate(self, t):
        """Espera até o instante t (s) do SRT; se já passou, só anota o atraso."""
        folga = t - self.t
        if folga > 0.02:
            self.wait(folga)
            self.t = t
        elif folga < -0.15:
            self.atrasos.append((t, round(-folga, 2)))

    def passo(self, t, *anims, dur=0.8):
        self.ate(t)
        self.play(*anims, run_time=dur)
        self.t += dur

    # ------------------------------------------------------------------
    # pequenos construtores (acompanham a câmera por updater)
    # ------------------------------------------------------------------
    def seg(self, f1, f2, cor, esp=6):
        lin = Line(f1(), f2(), color=cor, stroke_width=esp)
        lin.add_updater(lambda m: m.put_start_and_end_on(f1(), f2()))
        return lin

    def pino(self, f):
        d = Dot(f(), radius=0.08, color=CINZA)
        d.add_updater(lambda m: m.move_to(f()))
        return d

    def nome(self, tex, f, direcao, cor=CINZA):
        m = self.rotulo(tex, cor)
        m.add_updater(lambda x: x.next_to(f(), direcao, buff=0.12), call_updater=True)
        return m

    def rot_seg(self, tex, cor, f1, f2, direcao, buff=0.18):
        """Rótulo no meio de um segmento."""
        m = self.rotulo(tex, cor)
        m.add_updater(lambda x: x.next_to((f1() + f2()) / 2, direcao, buff=buff),
                      call_updater=True)
        return m

    def base_hex(self, cor, op):
        """Hexágono da base, preenchido, acompanhando a câmera."""
        pts = lambda: [self.P(k) for k in range(6)]
        p = Polygon(*pts(), color=cor, fill_opacity=op, stroke_width=0)
        p.add_updater(lambda m: m.set_points_as_corners(pts() + [pts()[0]]))
        return p

    def arco(self, centro, ponta1, ponta2, raio, cor):
        """Arco do ângulo em 'centro' entre as direções para ponta1 e ponta2."""
        a1 = np.arctan2(ponta1[1] - centro[1], ponta1[0] - centro[0])
        a2 = np.arctan2(ponta2[1] - centro[1], ponta2[0] - centro[0])
        return Arc(radius=raio, start_angle=a1, angle=(a2 - a1) % TAU,
                   arc_center=centro, color=cor, stroke_width=5), a1, (a2 - a1) % TAU

    def tex_parcial(self, *partes):
        """Fórmula em partes, todas invisíveis; reveladas uma a uma depois."""
        m = self.tex(*partes)
        m.set_opacity(0)
        return m

    def revela_partes(self, formula, tempos, dur=0.6):
        for parte, t in zip(formula, tempos):
            self.passo(t, parte.animate.set_opacity(1), dur=dur)

    # ------------------------------------------------------------------
    # cena
    # ------------------------------------------------------------------
    def construct(self):
        self.camera.background_color = FUNDO
        self.t = 0.0
        self.atrasos = []
        self.yaw = ValueTracker(YAW_PROVA)
        self.elev = ValueTracker(ELEV_PROVA)
        self.add(self.yaw, self.elev)

        self.figura_da_prova()      # t = 0 (figura como na questão)
        self.triangulo_padrao()     # 0:00 - 0:15   30-60-90 e a altura 12
        self.formula_do_volume()    # 0:15 - 0:44   V = A_b.h  e  A_b = 6 l^2 V3/4
        self.hexagono_de_cima()     # 0:44 - 0:57   diagonais e 6 triângulos
        self.triangulo_retangulo()  # 0:57 - 1:29   12, 12/V3
        self.metade_da_diagonal()   # 1:29 - 1:41   l = 6/V3
        self.conta_final()          # 1:41 - 2:18   V = 216 V3

        self.ate(138.7)
        self.wait(1.0)
        if self.atrasos:
            print("\n[sincronia] passos que começaram atrasados (t_SRT, atraso em s):",
                  self.atrasos)
        else:
            print("\n[sincronia] todos os passos começaram no tempo da fala.")

    # ---- t = 0 ---------------------------------------------------------
    def figura_da_prova(self):
        """Prisma como na prova: D no alto, M embaixo, DM, D'M e o ângulo de 60°."""
        self.wire = always_redraw(self.wireframe)
        self.add(self.wire)
        marca = Text("@proflaiozago", font_size=26,
                     color=mistura(FUNDO, CINZA, 0.55)).to_corner(DR, buff=0.3)
        self.add(marca)

        self.dm0 = self.seg(self.pD, self.pM, CINZA, 4)
        self.dpm = self.seg(self.pDp, self.pM, CINZA, 4)      # vira AZUL depois
        M, Dp, D = self.pM(), self.pDp(), self.pD()
        self.arco0, a1, ang = self.arco(M, D, Dp, 0.7, CINZA)
        self.lab60_0 = self.rotulo(r"60^\circ", CINZA, 0.8)
        meio = a1 + ang / 2
        self.lab60_0.move_to(M + 1.05 * np.array([np.cos(meio), np.sin(meio), 0.0]))
        self.pD_pino, self.pD_rot = self.pino(self.pD), self.nome("D", self.pD, UP)
        self.pM_pino, self.pM_rot = self.pino(self.pM), self.nome("M", self.pM, DR)
        self.add(self.dm0, self.dpm, self.arco0, self.lab60_0,
                 self.pD_pino, self.pD_rot, self.pM_pino, self.pM_rot)

        # roteiro (3 itens): h, V, l  -> entram ao longo da fala
        itens = [self.tex(r"h = 12\ \text{cm}", cor=VERDE),
                 self.tex(r"V = \,?", cor=VERMELHO),
                 self.tex(r"\ell = \,?", cor=VERMELHO)]
        self.roteiro = VGroup(*itens).scale(0.75)
        self.roteiro.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.roteiro.align_to(0.95 * RIGHT, LEFT).align_to(7.45 * UP, UP)

    # ---- 0:00 - 0:15 ---------------------------------------------------
    def triangulo_padrao(self):
        cab = self.texto("Triângulo 30° · 60° · 90°", tam=30)
        razoes = self.tex(r"m,\ \ m\sqrt{3},\ \ 2m").scale(0.95)
        razoes[0].set_color(AZUL)
        self.p0 = self.monta_painel(cab, razoes)
        self.passo(0.07, FadeIn(self.p0[0], shift=RIGHT * 0.2), dur=0.7)
        self.passo(4.6, Write(self.p0[1]), dur=1.2)

        self.passo(9.63, FadeIn(self.roteiro[0], shift=LEFT * 0.2), dur=0.6)   # h = 12
        # a altura marcada na figura: DD' em amarelo, com o "12"
        self.ddp = self.seg(self.pD, self.pDp, AMARELO)
        self.lab12 = self.rot_seg("12", AMARELO, self.pD, self.pDp, LEFT)
        self.passo(12.27, FadeIn(self.ddp), FadeIn(self.lab12), dur=0.8)

    # ---- 0:15 - 0:44 ---------------------------------------------------
    def formula_do_volume(self):
        self.passo(15.57, FadeOut(self.p0), FadeIn(self.roteiro[1], shift=LEFT * 0.2), dur=0.7)
        v = self.tex(r"V = A_b \cdot h").scale(0.95)
        ab = self.tex(r"A_b = 6\cdot\dfrac{\ell^2\sqrt{3}}{4}").scale(0.95)
        self.p1 = self.monta_painel(v, ab)
        self.passo(25.33, Write(self.p1[0]), dur=1.4)

        self.fundo_base = self.base_hex(LARANJA, 0.28)           # "área da base"
        self.passo(30.03, FadeIn(self.fundo_base), dur=0.8)
        self.passo(34.3, Write(self.p1[1]), dur=2.5)

        # "o lado do hexágono": destaca uma aresta da base e escreve l
        self.aresta_l = self.seg(lambda: self.P(4), lambda: self.P(5), LARANJA, 7)
        self.lab_l = self.rot_seg(r"\ell", LARANJA, lambda: self.P(4), lambda: self.P(5), DOWN)
        self.passo(40.9, FadeIn(self.aresta_l), FadeIn(self.lab_l),
                   FadeIn(self.roteiro[2], shift=LEFT * 0.2), dur=0.8)

    def resolve_em(self, t, i, tex, dur=0.8):
        """Troca o '?' vermelho do roteiro pelo valor, em verde, no instante t."""
        antigo = self.roteiro[i]
        novo = self.tex(tex, cor=VERDE).scale(0.75).move_to(antigo, aligned_edge=LEFT)
        self.passo(t, ReplacementTransform(antigo, novo), dur=dur)
        self.roteiro[i] = novo

    def gira_em(self, t, yaw, elev, dur, saem=()):
        """Gira a câmera a partir do instante t, retirando 'saem' da tela."""
        self.passo(t, self.yaw.animate.set_value(yaw), self.elev.animate.set_value(elev),
                   *[FadeOut(m) for m in saem], dur=dur)

    # ---- 0:44 - 0:57 ---------------------------------------------------
    def hexagono_de_cima(self):
        """Vista de cima: as diagonais se cruzam no centro -> 6 triângulos."""
        # DD' vira um ponto visto de cima: sai antes de a câmera chegar lá
        self.gira_em(44.4, YAW_CIMA, ELEV_CIMA, 3.0,
                     saem=[self.ddp, self.lab12, self.dm0, self.arco0, self.lab60_0,
                           self.pD_pino, self.pD_rot])
        c = self.centro()
        cor_raio = mistura(FUNDO, CINZA, 0.6)
        self.raios = VGroup(*[Line(c, self.P(k), color=cor_raio, stroke_width=2)
                              for k in range(6)])
        self.passo(48.0, Create(self.raios, lag_ratio=0.15), dur=1.8)
        self.fatias = VGroup(*[Polygon(c, self.P(k), self.P((k + 1) % 6), color=PALETA6[k],
                                       fill_opacity=0.35, stroke_width=0) for k in range(6)])
        self.passo(50.27, FadeOut(self.fundo_base),
                   LaggedStart(*[FadeIn(f) for f in self.fatias], lag_ratio=0.2), dur=3.2)

    # ---- 0:57 - 1:29 ---------------------------------------------------
    def triangulo_retangulo(self):
        """De frente: triângulo DD'M, 60° olha pro 12, 30° olha pro 12/V3."""
        self.gira_em(57.5, YAW_FRENTE, ELEV_FRENTE, 3.0,
                     saem=[self.fatias, self.raios, self.p1, self.aresta_l, self.lab_l])
        Dp, M, D = self.pDp(), self.pM(), self.pD()

        # o triângulo retângulo, com a altura 12 (60.5 s)
        self.pD2, self.pD2_rot = self.pino(self.pD), self.nome("D", self.pD, UP)
        self.pDp_pino, self.pDp_rot = self.pino(self.pDp), self.nome("D'", self.pDp, DL)
        self.ddp = self.seg(self.pD, self.pDp, AMARELO)
        self.lab12 = self.rot_seg("12", AMARELO, self.pD, self.pDp, LEFT)
        self.tri = Polygon(Dp, M, D, color=AZUL, fill_opacity=0.14, stroke_width=0)
        self.tri.add_updater(lambda m: m.set_points_as_corners(
            [self.pDp(), self.pM(), self.pD(), self.pDp()]))
        s = 0.32
        self.reto = VMobject(color=CINZA).set_points_as_corners(
            [Dp + s * RIGHT, Dp + s * (RIGHT + UP), Dp + s * UP]).set_stroke(width=3)
        self.passo(60.5, FadeIn(self.tri), FadeIn(self.ddp), FadeIn(self.lab12),
                   FadeIn(self.pD2), FadeIn(self.pD2_rot), FadeIn(self.pDp_pino),
                   FadeIn(self.pDp_rot), FadeIn(self.reto), dur=0.7)

        # o ângulo de 60 graus (62.9 s) e "60 olha pro 12" (64.3 s)
        self.arco60, a1, ang = self.arco(M, D, Dp, 0.85, LARANJA)
        self.lab60 = self.rotulo(r"60^\circ", LARANJA)
        self.lab60.move_to(M + 1.3 * np.array([np.cos(a1 + ang / 2), np.sin(a1 + ang / 2), 0.0]))
        self.passo(62.93, Create(self.arco60), Write(self.lab60), dur=0.9)

        t1 = self.tex(r"60^\circ", r"\ \to\ ", r"12")
        t1[0].set_color(LARANJA)
        t1[2].set_color(AMARELO)
        t2 = self.tex(r"30^\circ", r"\ \to\ ", r"\dfrac{12}{\sqrt{3}}")
        t2[0].set_color(LARANJA)
        t2[2].set_color(AZUL)
        for e in (t1, t2):
            e.scale(0.95)
        self.p2 = self.monta_painel(t1, t2)
        self.passo(64.27, Write(self.p2[0]), dur=0.9)

        # o ângulo de 30 graus em D (65.5 s)
        self.arco30, b1, ang30 = self.arco(D, Dp, M, 0.8, LARANJA)
        self.lab30 = self.rotulo(r"30^\circ", LARANJA)
        self.lab30.move_to(D + 1.25 * np.array([np.cos(b1 + ang30 / 2),
                                                np.sin(b1 + ang30 / 2), 0.0]))
        self.passo(65.5, Create(self.arco30), Write(self.lab30), Write(self.p2[1]), dur=1.4)

        # hipotenusa = 2m (70.0 s) ; D'M = m (73.0 s) ; DD' = m V3 (75.8 s)
        self.dm = self.seg(self.pD, self.pM, VERMELHO)
        self.lab2m = self.rot_seg("2m", VERMELHO, self.pD, self.pM, UR, 0.1)
        self.passo(70.03, FadeIn(self.dm), FadeIn(self.lab2m), dur=0.7)
        self.lab_m = self.rot_seg("m", AZUL, self.pDp, self.pM, DOWN)
        self.passo(73.0, self.dpm.animate.set_color(AZUL), FadeIn(self.lab_m), dur=0.6)
        novo = self.rot_seg(r"m\sqrt{3}", AMARELO, self.pD, self.pDp, LEFT)
        self.passo(75.8, ReplacementTransform(self.lab12, novo), dur=0.6)
        self.lab12 = novo

        # 12 = m V3 (76.7 s) ; m = 12/V3 (79.3 s)
        a = self.tex(r"12", r" = ", r"m\sqrt{3}")
        a[0].set_color(AMARELO)
        a[2].set_color(AMARELO)
        b = self.tex(r"m", r" = \dfrac{12}{\sqrt{3}}")
        b[0].set_color(AZUL)
        c = self.tex(r"\ell", r" = \dfrac{m}{2} = \dfrac{6}{\sqrt{3}}")
        c[0].set_color(VERDE)
        for e in (a, b, c):
            e.scale(0.95)
        self.p3 = self.monta_painel(a, b, c)
        self.passo(76.73, FadeOut(self.p2), Write(self.p3[0]), dur=1.5)
        self.passo(79.33, Write(self.p3[1]), dur=1.4)

        # o lado da base vale 12/V3 (83.0 s) e é "o tamanho todo" (88.0 s)
        self.lab_dpm = self.rot_seg(r"\dfrac{12}{\sqrt{3}}", AZUL, self.pDp, self.pM, DOWN)
        self.passo(83.0, ReplacementTransform(self.lab_m, self.lab_dpm), dur=0.8)
        self.passo(88.0, Indicate(self.lab_dpm), dur=0.8)

    # ---- 1:29 - 1:41 ---------------------------------------------------
    def metade_da_diagonal(self):
        """De cima: D'M foi cortada no meio pelo centro -> cada metade e 6/V3."""
        self.gira_em(89.17, YAW_CIMA, ELEV_CIMA, 2.8,
                     saem=[self.tri, self.ddp, self.lab12, self.dm, self.lab2m,
                           self.arco60, self.lab60, self.arco30, self.lab30, self.reto,
                           self.pD2, self.pD2_rot])
        c = self.centro()
        Dp, M = self.pDp(), self.pM()
        cor_raio = mistura(FUNDO, CINZA, 0.6)
        self.raios2 = VGroup(*[Line(c, self.P(k), color=cor_raio, stroke_width=2)
                               for k in range(6)])
        self.centro_pt = Dot(c, radius=0.08, color=VERMELHO)
        self.passo(92.0, Create(self.raios2, lag_ratio=0.15), FadeIn(self.centro_pt), dur=1.3)

        self.la1 = self.rotulo(r"\dfrac{6}{\sqrt{3}}", VERDE, 0.85).next_to((c + Dp) / 2, UP, buff=0.1)
        self.la2 = self.rotulo(r"\dfrac{6}{\sqrt{3}}", VERDE, 0.85).next_to((c + M) / 2, UP, buff=0.1)
        self.passo(98.33, Write(self.la1), Write(self.la2), Write(self.p3[2]), dur=1.5)
        self.resolve_em(99.9, 2, r"\ell = \dfrac{6}{\sqrt{3}}")

    # ---- 1:41 - 2:18 ---------------------------------------------------
    def conta_final(self):
        """V = 6 (6/V3)^2 V3 . 12 / 4  ->  216 V3  (letra D)."""
        q1 = self.tex_parcial(r"V = ", r"6", r"\cdot\left(\dfrac{6}{\sqrt{3}}\right)^2",
                              r"\cdot\sqrt{3}", r"\cdot 12", r"\div 4")
        q2a = self.tex(r"V = 6\cdot\dfrac{36}{3}")
        q2b = self.tex(r"V = 6\cdot 12", r"\cdot\sqrt{3}", r"\cdot\dfrac{12}{4}")
        q3 = self.tex(r"V = ", r"216\sqrt{3}\ \text{cm}^3")
        q3[1].set_color(VERDE)
        for e in (q1, q2a, q2b, q3):
            e.scale(0.95)
        self.p5 = self.monta_painel(q1, q2a, q3)
        q2b.move_to(q2a, aligned_edge=LEFT)
        q2b[1].set_opacity(0)
        q2b[2].set_opacity(0)
        q2a.set_opacity(1)

        self.gira_em(101.2, YAW_FINAL, ELEV_FINAL, 2.8,
                     saem=[self.p3, self.la1, self.la2, self.raios2, self.centro_pt,
                           self.lab_dpm])
        self.add(q1)
        self.passo(104.0, q1[0].animate.set_opacity(1), q1[1].animate.set_opacity(1), dur=0.6)
        self.revela_partes(list(q1)[2:], [105.4, 109.0, 110.4, 111.9], dur=0.7)

        self.passo(122.93, Write(q2a), dur=1.2)
        self.passo(125.07, ReplacementTransform(q2a, q2b), dur=0.8)
        self.passo(126.2, q2b[1].animate.set_opacity(1), dur=0.6)
        self.passo(128.3, q2b[2].animate.set_opacity(1), dur=0.8)

        self.passo(130.77, Write(self.p5[2]), dur=1.4)
        self.resolve_em(132.3, 1, r"V = 216\sqrt{3}\ \text{cm}^3")
        caixa = SurroundingRectangle(self.p5[2], color=VERDE, buff=0.18)
        letra = Text("Alternativa D", font_size=34, color=VERDE, weight=BOLD)
        letra.next_to(caixa, RIGHT, buff=0.4)    # ao lado (e não embaixo): longe do rosto
        self.passo(134.4, Create(caixa), FadeIn(letra, shift=UP * 0.15), dur=0.8)
