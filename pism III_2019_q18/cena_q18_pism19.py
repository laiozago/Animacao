# -*- coding: utf-8 -*-
"""
PISM III 2019 — Questão 18 (polinômio x³ − 8x² + 19x − 12: soma dos quadrados das raízes) — @proflaiozago

  manim -pql cena_q18_pism19.py QuestaoPism19     # prévia 540x960, com as 3 guias
  manim -qh  cena_q18_pism19.py QuestaoPism19     # final 1080x1920, sem guias

Sincronizada com "PISM III - 2019 - Q18.srt" (vídeo limpo, ~3m29s). Cada passo tem o instante da fala (s);
o terminal lista os passos atrasados no fim do render. Ajuste de sincronia = trocar só o número do instante.
Resolução (ordem e notação do professor): teste do 1 → Briot-Ruffini → x² − 7x + 12 → soma e produto
→ raízes 1, 3 e 4 → 1² + 3² + 4² = 26 (C) → pegadinha: o quadrado da soma daria 64 (E).
"""
from manim import *
import geometria as G
from geometria import F
from cena_base import CenaPadrao

TEXTO, VERMELHO, VERDE, AZUL = G.TEXTO, G.VERMELHO, G.VERDE, G.AZUL
AMARELO, LARANJA, CINZA = G.AMARELO, G.LARANJA, G.CINZA


class QuestaoPism19(CenaPadrao):
    GUIAS = "auto"
    T_FIM = 209.0

    def construct(self):
        self.iniciar()
        self.monta_roteiro()
        self.abertura()
        self.cabecalho()
        self.rotulo_briot()
        self.teste_do_um()
        self.abaixa_o_grau()
        self.dispositivo()
        self.novo_polinomio()
        self.soma_e_produto()
        self.soma_dos_quadrados()
        self.pegadinha()
        self.final()
        self.fim(self.T_FIM)

    # ═══ 0–10 s · enunciado integral, digitado ════════════════════════════
    def abertura(self):
        self.enun = self.monta_enunciado()
        self.add(self.enun["grupo"], *self.enun["covers"])
        self.digita(self.enun, 0.3, 3.9)
        self.passo(9.5, FadeOut(self.enun["grupo"]), dur=0.4, nome="enunciado sai")

    # ═══ 10 s · p(x) no cabeçalho (fica até o fim) ═══════════════════════
    def cabecalho(self):
        self.hdr = self.linha(F["px"], G.Y_CAB, escala=0.9)
        self.passo(10.0, self.aparece(self.hdr), dur=0.5, nome="p(x) no cabeçalho")

    # ═══ 13–18 s · "uma ferramenta chamada Briot-Ruffini" ════════════════
    def rotulo_briot(self):
        self.lbl_briot = self.legenda("Briot-Ruffini", (0, 3.4), AMARELO, s_em=0.36)
        self.passo(13.4, FadeIn(self.lbl_briot), dur=0.5, nome="Briot-Ruffini")
        self.sai(17.9, self.lbl_briot, dur=0.4, nome="Briot-Ruffini sai")

    # ═══ 18–55 s · teste do 1 raiz ═══════════════════════════════════════
    def teste_do_um(self):
        hdr = self.hdr
        l1 = self.linha(F["t1"], G.Y_T1, escala=0.95)               # p(1) = 1 − 8 + 19 − 12
        for i in (2, 3, 4, 5):
            l1[i].set_color(AZUL)
        l2 = self.linha(F["t2"], G.Y_T2, escala=0.95)               # = 20 − 20
        l3 = self.linha(F["t3"], G.Y_T3, escala=0.95)               # = 0
        l3.set_color(VERDE)
        for m in (l2, l3):                                          # alinha o "=" com o "=" da 1ª linha
            m.shift(RIGHT * (l1[1].get_left()[0] - m.get_left()[0]))
        regra = self.legenda("se der 0, o 1 é raiz", (0, G.Y_REGRA), AMARELO, s_em=0.30)
        raiz_ok = self.txt("o 1 é raiz", 0.34, VERDE, pos=(2.55, G.Y_T3))

        self.passo(20.0, self.aparece(l1[0]), self.aparece(l1[1]), dur=0.4, nome="p(1) =")
        self.passo(21.6, self.rot_entra(0), dur=0.4, nome="roteiro p(1)=?")
        self.passo(24.8, [Indicate(hdr[i], color=LARANJA, scale_factor=1.3) for i in (1, 3, 5)], dur=0.6, nome="tira o x")
        self.passo(27.3, [hdr[i].animate.set_color(CINZA) for i in (1, 3, 5)],
                   [hdr[i].animate.set_color(AZUL) for i in (2, 4, 6)], dur=0.5, nome="joga o x fora")
        self.passo(30.6, FadeIn(regra), dur=0.5, nome="regra: se der 0")
        self.passo(41.4, self.aparece(l1[2]), dur=0.3, nome="1")
        self.passo(42.75, self.aparece(l1[3]), dur=0.3, nome="-8")
        self.passo(43.6, self.aparece(l1[4]), dur=0.3, nome="+19")
        self.passo(44.8, self.aparece(l1[5]), dur=0.3, nome="-12")
        self.passo(46.7, Indicate(l1[2], color=LARANJA), Indicate(l1[4], color=LARANJA), dur=0.5, nome="1 + 19")
        self.passo(47.7, self.aparece(l2[0]), dur=0.3, nome="= 20")
        self.passo(48.4, Indicate(l1[3], color=LARANJA), Indicate(l1[5], color=LARANJA), dur=0.5, nome="-8 - 12")
        self.passo(50.0, self.aparece(l2[1]), dur=0.3, nome="-20")
        self.passo(51.3, self.aparece(l3[0]), dur=0.4, nome="= 0")
        self.passo(53.3, FadeIn(raiz_ok), self.rot_resolve(0), dur=0.5, nome="o 1 é raiz")
        self.sai(55.3, regra, l1, l2, l3, raiz_ok, dur=0.4, nome="limpa teste")

    # ═══ 55–77 s · abaixar o grau (3 → 2) · soma e produto/Bhaskara · três raízes ═══
    def abaixa_o_grau(self):
        pB = self.linha(F["pB"], G.Y_PQ, x=-2.6, escala=1.0)
        qB = self.linha(F["qB"], G.Y_PQ, x=1.0, escala=1.0)
        g3 = self.txt("grau 3", 0.30, CINZA, pos=(-2.6, G.Y_GRAU))
        g2 = self.txt("grau 2", 0.30, CINZA, pos=(1.0, G.Y_GRAU))
        seta = Arrow([-1.6, G.Y_PQ, 0], [0.0, G.Y_PQ, 0], buff=0, color=TEXTO, stroke_width=5,
                     max_tip_length_to_length_ratio=0.2)
        f1 = self.legenda("Soma e Produto", (-1.9, G.Y_FERR), AMARELO)
        f2 = self.legenda("Bhaskara", (1.9, G.Y_FERR), AMARELO)
        ou = self.txt("ou", 0.28, CINZA, pos=(0.0, G.Y_FERR))
        slots = self.linha(F["slots"], G.Y_SLOTS, escala=0.9)
        slots[0].set_color(VERDE)
        slots[1].set_color(VERMELHO)
        slots[2].set_color(VERMELHO)

        self.passo(56.7, self.rot_entra(1), dur=0.4, nome="roteiro q(x)=?")
        self.passo(57.5, self.aparece(pB), dur=0.4, nome="p(x)")
        self.passo(58.5, FadeIn(g3), dur=0.4, nome="grau 3")
        self.passo(59.7, FadeIn(seta), self.aparece(qB), FadeIn(g2), dur=0.5, nome="pra grau 2")
        self.passo(62.8, Indicate(g2, color=LARANJA), dur=0.5, nome="com grau 2")
        self.passo(65.7, FadeIn(f1), dur=0.5, nome="soma e produto")
        self.passo(67.4, FadeIn(ou), FadeIn(f2), dur=0.5, nome="ou Bhaskara")
        self.passo(69.4, self.aparece(slots), dur=0.5, nome="as outras duas raízes")
        self.passo(72.0, Indicate(g3, color=LARANJA), dur=0.5, nome="se é grau 3")
        self.passo(74.3, [Indicate(slots[i], color=LARANJA) for i in (0, 1, 2)], dur=0.6, nome="três raízes")
        self.sai(76.6, pB, qB, g3, g2, seta, f1, f2, ou, slots, dur=0.4, nome="limpa grau")

    # ═══ 77–145 s · dispositivo de Briot-Ruffini ═════════════════════════
    def dispositivo(self):
        hdr = self.hdr
        X, Y = G.COL_X, None
        titulo = self.txt("Briot-Ruffini", 0.34, AMARELO, pos=(-2.6, G.Y_TITULO))
        barra = Line([G.X_BARRA, G.Y_BARRA[0], 0], [G.X_BARRA, G.Y_BARRA[1], 0], color=TEXTO, stroke_width=4)
        traco = Line([G.X_BARRA, G.Y_TRACO, 0], [G.X_FIM, G.Y_TRACO, 0], color=TEXTO, stroke_width=4)
        coef = [self.celula(F["coef"][i], X[i], G.Y_COEF, AZUL) for i in range(4)]
        raiz = self.celula(F["raiz"], G.X_RAIZ, G.Y_COEF, VERDE)
        lbl_raiz = self.txt("raiz", 0.26, CINZA, pos=(G.X_RAIZ, G.Y_COEF - 0.6))
        prod = [None] + [self.celula(F["prod"][i], X[i + 1], G.Y_PROD, LARANJA, esc=0.6) for i in range(3)]
        res = [self.celula(F["res"][i], X[i], G.Y_RES, AZUL) for i in range(4)]
        setas = [Arrow([X[i] + 0.3, G.Y_RES + 0.18, 0], [X[i + 1] - 0.3, G.Y_PROD - 0.2, 0], buff=0, color=LARANJA,
                       stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(3)]
        cap1 = self.legenda("multiplica\ne soma", (G.X_CAP, G.Y_CAP[0]), AMARELO, s_em=0.26)
        cap2 = self.legenda("dá zero:\né raiz", (G.X_CAP, G.Y_CAP[1]), VERDE, s_em=0.26)
        cap3 = self.legenda("novo\npolinômio", (G.X_CAP, G.Y_CAP[2]), AMARELO, s_em=0.26)
        zero = self.caixa(res[3], VERDE, buff=0.1)
        # "grau 3 → grau 2" (entre o dispositivo e o novo polinômio)
        t_g3 = self.txt("grau 3", 0.30, CINZA, pos=(-2.7, G.Y_QLINHA))
        s_g = Arrow([-1.8, G.Y_QLINHA, 0], [-0.6, G.Y_QLINHA, 0], buff=0, color=TEXTO, stroke_width=5,
                    max_tip_length_to_length_ratio=0.2)
        t_g2 = self.txt("grau 2", 0.30, CINZA, pos=(0.3, G.Y_QLINHA))
        self.C = [titulo, barra, traco, raiz, lbl_raiz, *coef, *prod[1:], *res, *setas, zero, cap1, cap2, cap3]
        self.res = res

        self.passo(76.9, FadeIn(titulo), dur=0.4, nome="título Briot-Ruffini")
        self.passo(80.0, Create(barra), Create(traco), dur=0.7, nome="estrutura")
        self.passo(83.5, self.aparece(coef[0]), Indicate(hdr[1], color=LARANJA, scale_factor=1.3), dur=0.5, nome="coef 1")
        self.voa_copia(85.4, hdr[2], coef[1], dur=0.7, nome="coef -8")
        self.voa_copia(87.3, hdr[4], coef[2], dur=0.7, nome="coef 19")
        self.voa_copia(89.2, hdr[6], coef[3], dur=0.7, nome="coef -12")
        self.passo(94.0, self.aparece(raiz), dur=0.4, nome="o 1 que já testamos")
        self.passo(95.9, FadeIn(lbl_raiz), dur=0.4, nome="é raiz")
        self.voa_copia(106.5, coef[0], res[0], dur=0.7, nome="o 1 desce")
        self.passo(108.2, FadeIn(cap1), dur=0.5, nome="multiplica e soma")
        self.passo(110.4, Create(setas[0]), self.aparece(prod[1]), dur=0.4, nome="1 vezes 1")
        self.passo(111.9, Indicate(coef[1], color=LARANJA), Indicate(prod[1], color=LARANJA), dur=0.5, nome="1 menos 8")
        self.passo(113.4, self.aparece(res[1]), dur=0.4, nome="-7")
        self.passo(114.5, Create(setas[1]), self.aparece(prod[2]), dur=0.4, nome="-7 vezes 1")
        self.passo(115.2, Indicate(coef[2], color=LARANJA), Indicate(prod[2], color=LARANJA), dur=0.5, nome="mais 19")
        self.passo(116.5, self.aparece(res[2]), dur=0.4, nome="12")
        self.passo(118.2, Create(setas[2]), self.aparece(prod[3]), dur=0.4, nome="1 vezes 12")
        self.passo(120.1, Indicate(coef[3], color=LARANJA), Indicate(prod[3], color=LARANJA), dur=0.5, nome="menos 12")
        self.passo(120.9, self.aparece(res[3]), dur=0.4, nome="zero")
        self.passo(121.9, FadeIn(zero), res[3].animate.set_color(VERDE), dur=0.4, nome="deu zero")
        self.passo(122.7, FadeIn(cap2), dur=0.5, nome="é raiz")
        self.passo(127.7, res[0].animate.set_color(VERDE), dur=0.3, nome="o 1")
        self.passo(128.3, res[1].animate.set_color(VERDE), dur=0.3, nome="o -7")
        self.passo(128.9, res[2].animate.set_color(VERDE), dur=0.3, nome="o 12")
        self.passo(131.2, FadeIn(cap3), dur=0.5, nome="novo polinômio")
        self.passo(135.9, FadeIn(t_g3), dur=0.4, nome="era grau 3")
        self.passo(137.6, FadeIn(s_g), FadeIn(t_g2), dur=0.4, nome="abaixou pra grau 2")
        self.sai(139.7, t_g3, s_g, t_g2, dur=0.3, nome="limpa grau")

    # ═══ 140–145 s · o novo polinômio x² − 7x + 12 ═══════════════════════
    def novo_polinomio(self):
        res = self.res
        q = self.linha(F["q"], G.Y_QLINHA, x=-1.0, escala=0.9)
        for i in (1, 2, 3):
            q[i].set_color(VERDE)
        self.q = q
        self.passo(140.1, self.aparece(q[0]), dur=0.3, nome="q(x) =")
        self.passo(141.5, self.aparece(q[1]), Indicate(res[0], color=LARANJA), dur=0.4, nome="x²")
        self.passo(143.3, self.aparece(q[2]), Indicate(res[1], color=LARANJA), dur=0.4, nome="-7x")
        self.passo(144.0, self.aparece(q[3]), Indicate(res[2], color=LARANJA), dur=0.35, nome="+12")
        self.passo(144.45, self.rot_resolve(1), dur=0.35, nome="roteiro q resolvido")
        # limpa o dispositivo; o polinômio sobe e fica centralizado, sem o "q(x) ="
        resto = VGroup(q[1], q[2], q[3], q[4])
        self.passo(145.0, [FadeOut(m) for m in self.C if m in self.mobjects], self.apaga(q[0]),
                   resto.animate.move_to([0, G.Y_EQ, 0]), dur=0.7, nome="igualando a zero")

    # ═══ 145–162 s · soma e produto → raízes 3 e 4 ═══════════════════════
    def soma_e_produto(self):
        q = self.q
        soma = self.linha(F["soma"], G.Y_SOMA, x=G.X_COL1, escala=0.9, cor=AZUL)
        prod_t = self.linha(F["produto"], G.Y_PROD2, x=G.X_COL1, escala=0.9, cor=AZUL)
        ss = self.linha(F["slots_s"], G.Y_SOMA, x=G.X_COL2, escala=0.9)
        sp = self.linha(F["slots_p"], G.Y_PROD2, x=G.X_COL2, escala=0.9)
        for m in (ss, sp):
            m[0].set_color(VERMELHO)
            m[2].set_color(VERMELHO)
        n = {}
        for nome, m, i, cifra in (("3s", ss, 0, F["n3"]), ("4s", ss, 2, F["n4"]),
                                  ("3p", sp, 0, F["n3"]), ("4p", sp, 2, F["n4"])):
            c = m[i].get_center()
            n[nome] = self.celula(cifra, c[0], c[1], VERDE)
        rz = self.linha(F["raizes"], G.Y_RAIZES, escala=0.9)
        for i in (0, 1, 2):
            rz[i].set_color(VERDE)
        self.rz = rz
        self.D = [q, soma, prod_t, ss, sp, *n.values(), rz]

        self.passo(147.4, self.aparece(q[4]), dur=0.4, nome="= 0")
        self.passo(149.6, Indicate(q[2], color=LARANJA), self.aparece(soma), dur=0.5, nome="a soma é 7")
        self.passo(150.7, Indicate(q[3], color=LARANJA), self.aparece(prod_t), dur=0.5, nome="o produto é 12")
        self.passo(152.0, self.aparece(ss), dur=0.5, nome="dois números que somam 7")
        self.passo(154.6, self.aparece(sp), dur=0.5, nome="e produto 12")
        self.passo(156.2, self.apaga(ss[0]), self.apaga(sp[0]), self.aparece(n["3s"]), self.aparece(n["3p"]),
                   dur=0.4, nome="três")
        self.passo(156.8, self.apaga(ss[2]), self.apaga(sp[2]), self.aparece(n["4s"]), self.aparece(n["4p"]),
                   dur=0.4, nome="quatro")
        self.passo(157.9, [Indicate(n[k], color=LARANJA) for k in ("3s", "4s", "3p", "4p")], dur=0.5, nome="são os números")
        self.passo(160.3, self.aparece(rz[0]), dur=0.3, nome="raízes: um")
        self.passo(161.0, self.aparece(rz[1]), dur=0.3, nome="três")
        self.passo(161.45, self.aparece(rz[2]), dur=0.3, nome="quatro")
        self.passo(162.0, self.rot_resolve(2), dur=0.4, nome="roteiro raízes resolvido")

    # ═══ 162–177 s · soma dos quadrados das raízes ═══════════════════════
    def soma_dos_quadrados(self):
        esc = 0.9
        self.titS = self.txt("S = soma dos quadrados das raízes", 0.28, TEXTO, pos=(0, G.Y_TIT_S), esq=G.ESQ_E)
        E1 = self.linha(F["E1"], G.Y_E1, escala=esc, esq=G.ESQ_E)
        for i in (1, 2, 3):
            E1[i].set_color(AZUL)
        x_eq = E1[0].get_right()[0] - 0.389 * esc                   # onde está o "=" da 1ª linha
        E2 = self.linha(F["E2"], G.Y_E2, escala=esc, esq=x_eq)
        E3 = self.linha(F["E3"], G.Y_E3, escala=esc, esq=x_eq)
        E3[2].set_color(VERDE)
        self.E = (E1, E2, E3)
        self.sai(162.6, *self.D, dur=0.4, nome="limpa soma e produto")
        self.passo(163.3, FadeIn(self.titS), self.rot_entra(3), dur=0.5, nome="soma dos quadrados")
        self.passo(165.0, self.aparece(E1[0]), dur=0.3, nome="S =")
        self.passo(165.9, self.aparece(E1[1]), dur=0.3, nome="1²")
        self.passo(166.8, self.aparece(E2[0]), dur=0.3, nome="= 1")
        self.passo(167.6, self.aparece(E1[2]), dur=0.3, nome="3²")
        self.passo(168.2, self.aparece(E2[1]), dur=0.3, nome="+ 9")
        self.passo(169.0, self.aparece(E1[3]), dur=0.3, nome="4²")
        self.passo(170.0, self.aparece(E2[2]), dur=0.3, nome="+ 16")
        self.passo(171.5, Indicate(E2, color=LARANJA, scale_factor=1.1), dur=0.6, nome="soma essa galera")
        self.passo(173.5, self.aparece(E3[0]), dur=0.3, nome="= 10")
        self.passo(174.1, self.aparece(E3[1]), dur=0.3, nome="+ 16")
        self.passo(175.0, self.aparece(E3[2]), dur=0.4, nome="= 26")
        self.passo(175.8, self.rot_resolve(3), dur=0.4, nome="roteiro S resolvido")
        self.passo(176.3, Indicate(E3[2], color=LARANJA, scale_factor=1.3), dur=0.5, nome="é isso daí")

    # ═══ 177–203 s · a pegadinha do 64 (quadrado da soma) ════════════════
    def pegadinha(self):
        E1, E2, E3 = self.E
        alts = []
        for i, (a, v) in enumerate(G.ALTERNATIVAS):
            t = self.txt("(%s) %s" % (a, v), 0.36, TEXTO)
            t.move_to([G.X_ALT + t.width / 2, G.Y_ALT - i * G.DY_ALT, 0])
            alts.append(t)
        self.alts = alts
        lista = VGroup(*alts)
        lbl = self.txt("quadrado\nda soma", 0.26, LARANJA, pos=G.POS_LBL_QUAD)
        err = self.linha(F["errada"], G.Y_ERR, escala=0.9, esq=G.ESQ_E)
        b1 = self.txt("1º", 0.30, LARANJA, pos=(G.ESQ_E - 0.45, G.Y_E1))
        b2 = self.txt("2º", 0.30, LARANJA, pos=(G.ESQ_E - 0.45, G.Y_E3))
        self.err, self.lbl, self.b1, self.b2, self.lista = err, lbl, b1, b2, lista

        self.passo(182.0, FadeIn(lista), dur=0.5, nome="alternativas")
        self.passo(183.2, Indicate(alts[4], color=LARANJA), dur=0.5, nome="o 64")
        self.passo(185.0, alts[4].animate.set_color(CINZA), dur=0.4, nome="não é o 64")
        self.passo(186.4, FadeIn(lbl), dur=0.4, nome="não é o quadrado da soma")
        self.passo(188.0, Indicate(self.titS, color=LARANJA, scale_factor=1.08), dur=0.5, nome="é a soma dos quadrados")
        self.passo(189.7, Indicate(lbl, color=LARANJA), dur=0.5, nome="o quadrado da soma seria")
        self.passo(191.9, self.aparece(err[0]), dur=0.3, nome="(1")
        self.passo(192.5, self.aparece(err[1]), dur=0.3, nome="+3")
        self.passo(193.1, self.aparece(err[2]), dur=0.3, nome="+4)²")
        self.passo(193.9, self.aparece(err[3]), dur=0.3, nome="= 8")
        self.passo(194.5, self.aparece(err[4]), dur=0.3, nome="elevar ao quadrado")
        self.passo(195.5, self.aparece(err[5]), dur=0.3, nome="= 64")
        self.passo(196.5, Create(self.corte(err)), err.animate.set_color(CINZA), dur=0.4, nome="não é isso")
        self.passo(197.8, Indicate(E1, color=VERDE, scale_factor=1.05), Indicate(E3, color=VERDE, scale_factor=1.05),
                   dur=0.5, nome="a soma dos quadrados")
        self.passo(199.4, FadeIn(b1), Indicate(E1, color=LARANJA, scale_factor=1.08), dur=0.5, nome="primeiro: ao quadrado")
        self.passo(202.0, FadeIn(b2), Indicate(E3, color=LARANJA, scale_factor=1.08), dur=0.5, nome="depois: soma")

    # ═══ 203–209 s · letra C e "salva e segue" ═══════════════════════════
    def final(self):
        moldura = self.caixa(self.alts[2], VERDE, buff=0.12)
        self.passo(203.5, FadeIn(moldura), Indicate(self.alts[2], color=VERDE, scale_factor=1.1), dur=0.5, nome="letra C")
        self.passo(204.3, self.pulso_marca(), dur=0.6, nome="salva esse vídeo")
        self.passo(206.8, self.pulso_marca(), dur=0.6, nome="e segue")
