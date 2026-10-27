"""PISM III 2025 — Questão 18 — x·y·z com potências e logaritmos (gabarito: letra C, 144).

Sincronizada com PISM_III_-_2025_-_Q18.srt (vídeo limpo, ~2m59s).
Layout padronizado na Questão 19 (rosto no meio-esquerda): palco em cima, coluna das contas à
esquerda, coluna das regras à direita, roteiro e marca d'água na faixa ao lado do rosto.

    manim -pql cena_q18_pism.py QuestaoPism18     # prévia 540x960 (com guias das zonas)
    manim -qh  cena_q18_pism.py QuestaoPism18     # final 1080x1920 (sem guias)

Ajuste de sincronia = trocar só o número do instante em cada passo(...).
"""
from manim import FadeIn, FadeOut, ReplacementTransform, Indicate, UP

import geometria as G
from cena_base import CenaBase, _v

# propriedades que o professor cita (coluna da direita)
R_SOMA = r"a^{m+n}=a^m\cdot a^n"
R_SUB = r"a^{m-n}=\dfrac{a^m}{a^n}"
R_PROD = r"a^{m\cdot n}=\bigl(a^m\bigr)^n"
R_PET1 = r"\log_a b^n=n\cdot\log_a b"
R_PET2 = r"\log_{a^m} b=\dfrac{1}{m}\log_a b"


class QuestaoPism18(CenaBase):

    def construct(self):
        self.prepara()
        self.enunciado()        #   0,0 –   4,9  enunciado recomposto em texto
        self.parte_x()          #   4,9 –  53,0  x = 40
        self.parte_y()          #  53,0 –  82,4  y = 9/5
        self.parte_z()          #  82,4 – 162,0  z = 2
        self.produto()          # 162,0 – 173,3  x·y·z = 144, letra C
        self.final()            # 173,3 – 179,0  salva e segue
        self.fim()

    # ================================================================== preparo
    def prepara(self):
        self.desenha_guias()
        self.marca_dagua()
        self.cria_roteiro([("x", "=", "?"), ("y", "=", "?"), ("z", "=", "?"),
                           (r"x\cdot y\cdot z", "=", "?")])
        # cabeçalho: as três definições em uma linha (entram em 4,9, vindas do enunciado)
        self.cab = [self.tex(s, escala=G.CAB_ESCALA, cor=G.CINZA)
                    for s in (G.TEX_X, G.TEX_Y, G.TEX_Z)]
        gap = 0.45
        x = -(sum(m.width for m in self.cab) + 2 * gap) / 2
        for m in self.cab:
            m.move_to(_v(x + m.width / 2, G.CAB_Y))
            x += m.width + gap

    # ================================================================== 0 – 4,9
    def enunciado(self):
        self.e_intro = self.texto(r"Considere os números $x$, $y$ e $z$ definidos por",
                                  escala=0.8, larg_max=7.8)
        self.e_intro.move_to(_v(0, 5.0))
        self.e_exp = []
        for s, y in zip((G.TEX_X, G.TEX_Y, G.TEX_Z), (4.0, 3.1, 2.2)):
            m = self.tex(s, escala=1.0)
            m.move_to(_v(0, y))
            m.shift(_v(-1.9 - m.get_left()[0], 0))
            self.e_exp.append(m)
        self.e_valor = self.texto(r"O valor de $x\cdot y\cdot z$ é", escala=0.9)
        self.e_valor.move_to(_v(0, 1.2))

        self.passo(0.1, FadeIn(self.e_intro), *[FadeIn(m) for m in self.e_exp],
                   FadeIn(self.e_valor), dur=0.6)

    def troca_cab(self, de, para):
        """Animações que passam o destaque do cabeçalho de `de` para `para`."""
        nova = self.caixa(self.cab[para], G.AZUL, folga=0.1)
        anims = [ReplacementTransform(self.cab_box, nova),
                 self.cab[de].animate.set_color(G.CINZA),
                 self.cab[para].animate.set_color(G.TEXTO)]
        self.cab_box = nova
        return anims

    def troca_regra(self, t, partes, dur=0.7):
        """A caixa de cima da coluna da direita troca de propriedade."""
        novo = self.regra_tex(partes, G.SLOT1_Y)
        ant = self.r1
        self.regras[self.regras.index(ant)] = novo
        self.r1 = novo
        self.passo(t, ReplacementTransform(ant, novo), dur=dur)

    # ================================================================== x  (4,9 – 53,0)
    def parte_x(self):
        XI, Y0, P = G.XI_XY, G.CONTA_Y0, G.CONTA_PASSO
        L1 = self.linha("x", "=", "2", r"{}^{3+\log_2 5}", y=Y0, x_igual=XI, idx=1)
        L2 = self.linha("=", r"2^3", r"\cdot", r"2^{\log_2 5}", y=Y0 - P, x_igual=XI, idx=0)
        L3 = self.linha("=", r"2^3", r"\cdot", "5", y=Y0 - 2 * P, x_igual=XI, idx=0)
        L4 = self.linha("=", "8", r"\cdot", "5", y=Y0 - 3 * P, x_igual=XI, idx=0)
        L5 = self.linha("=", "40", y=Y0 - 4 * P, x_igual=XI, idx=0)

        # "bom começa pelo x": enunciado vira cabeçalho, roteiro entra
        self.cab[0].set_color(G.TEXTO)
        self.cab_box = self.caixa(self.cab[0], G.AZUL, folga=0.1)
        self.passo(4.9,
                   *[ReplacementTransform(a, b) for a, b in zip(self.e_exp, self.cab)],
                   FadeOut(self.e_intro), FadeOut(self.e_valor), FadeIn(self.cab_box),
                   *[FadeIn(r) for r in self.rot], dur=0.8)

        # 5,7  x = 2^(3 + log2 5)
        self.passo(5.7, *self.aparece(L1, 0, 1, 2, 3), dur=0.5)

        # 6,5  "soma no expoente e vira produto de potência"
        cx = self.guarda(self.caixa_expoente(L1[3], G.AZUL))
        self.r1_caixa = self.caixa_regra(G.SLOT1_Y, G.SLOT1_H)
        self.r1 = self.regra_tex([R_SOMA], G.SLOT1_Y)
        self.regras += [self.r1_caixa, self.r1]
        self.passo(6.5, FadeIn(cx), FadeIn(self.r1_caixa), FadeIn(self.r1), dur=0.6)

        # 8,9  "dois ao cubo, vezes, dois elevado ao log de cinco na base dois"
        self.passo(8.9, *self.aparece(L2, 0, 1), dur=0.5)
        self.passo(9.9, *self.aparece(L2, 2), dur=0.3)
        self.passo(10.3, *self.aparece(L2, 3), dur=0.5)

        # 12,97  "e aqui tá o macete"
        self.m_caixa = self.caixa_regra(G.SLOT2_Y, G.SLOT2_H)
        self.m_rot = self.texto(r"\textbf{macete}", escala=0.65, cor=G.AMARELO)
        self.m_rot.move_to(_v(G.REGRA_X, G.SLOT2_Y + G.SLOT2_H / 2 + 0.2))
        self.m_rule = self.regra_tex([r"a^{\log_a b}", "=", "b"], G.SLOT2_Y)
        self.m_rule.set_opacity(0)
        self.add(self.m_rule)
        self.leg = self.texto(r"\textbf{logaritmando}", escala=0.65, cor=G.VERDE)
        self.leg.move_to(_v(G.REGRA_X, G.LEGENDA_Y))
        self.regras += [self.m_caixa, self.m_rot, self.m_rule, self.leg]
        self.passo(12.97, FadeIn(self.m_caixa), FadeIn(self.m_rot), dur=0.5)

        self.passo(16.4, *self.aparece(self.m_rule, 0), dur=0.6)             # potência com expoente log
        self.passo(19.57, Indicate(self.m_rule[0], color=G.LARANJA), dur=0.8)  # base = base do log
        self.passo(22.7, *self.aparece(self.m_rule, 1), *self.aparece(self.m_rule, 2, cor=G.VERDE),
                   dur=0.5)                                                   # a resposta é o logaritmando
        self.passo(24.57, FadeIn(self.leg), dur=0.5)                          # parte de cima do log
        self.passo(27.2, Indicate(self.m_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.7)

        # 30,8  volta para a conta: separa o mais
        self.passo(30.8, Indicate(L1, color=G.LARANJA, scale_factor=1.08), dur=0.8)
        self.passo(33.6, Indicate(L1[3], color=G.LARANJA), dur=0.6)
        self.passo(36.5, Indicate(cx, color=G.LARANJA), dur=0.7)              # o mais vira produto
        self.passo(38.2, Indicate(self.r1_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.7)
        self.passo(40.9, Indicate(L2[1], color=G.LARANJA), dur=0.6)           # 2^3
        self.passo(43.2, Indicate(L2[3], color=G.LARANJA), dur=0.6)           # 2^(log2 5)

        # 46,2  "a base é igual, então esse resultado vai dar cinco"
        cin = self.guarda(self.caixa(L2[3], G.AMARELO, folga=0.08))
        self.passo(46.2, FadeIn(cin), dur=0.5)
        lb5 = self.tex("5", escala=0.7, cor=G.VERDE)
        lb5.move_to(_v(cin.get_center()[0], cin.get_bottom()[1] - 0.22))
        self.guarda(lb5)
        self.passo(47.3, FadeIn(lb5), dur=0.5)

        # 48,8  2^3 · 5  ->  8 · 5  ->  40
        self.passo(48.8, *self.aparece(L3, 0, 1, 2), *self.aparece(L3, 3, cor=G.VERDE),
                   *self.some(cin, lb5), dur=0.6)
        self.passo(50.4, *self.aparece(L4, 0, 1, 2, 3), dur=0.6)
        self.passo(51.3, *self.aparece(L5, 0, 1, cor=G.VERDE), dur=0.5)
        cv = self.guarda(self.caixa(L5, G.VERDE, folga=0.1))
        self.passo(51.8, FadeIn(cv), self.resolve_roteiro(0, ("x", "=", "40")), dur=0.6)

    def some(self, *ms):
        """FadeOut de objetos soltos, tirando-os da lista de trabalho."""
        for m in ms:
            if m in self.trab:
                self.trab.remove(m)
        return [FadeOut(m) for m in ms]

    # ================================================================== y  (53,0 – 82,4)
    def parte_y(self):
        XI, Y0, P = G.XI_XY, G.CONTA_Y0, G.CONTA_PASSO
        # "deixarei guardado, agora o y"
        self.limpa_trabalho(53.2, dur=0.7, extra=self.troca_cab(0, 1))

        Y1 = self.linha("y", "=", "3", r"{}^{2-\log_3 5}", y=Y0, x_igual=XI, idx=1)
        Y2 = self.linha("=", r"3^2", r"\div", r"3^{\log_3 5}", y=Y0 - P, x_igual=XI, idx=0)
        Y3 = self.linha("=", r"3^2", r"\div", "5", y=Y0 - 2 * P, x_igual=XI, idx=0)
        Y4 = self.linha("=", r"\dfrac{9}{5}", y=Y0 - 3 * P, x_igual=XI, idx=0)

        self.passo(54.1, *self.aparece(Y1, 0, 1, 2, 3), dur=0.5)
        cx = self.guarda(self.caixa_expoente(Y1[3], G.AZUL))
        self.passo(54.9, FadeIn(cx), dur=0.5)                                  # "aquele menos"
        self.passo(57.0, Indicate(self.r1_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.6)
        self.troca_regra(59.6, [R_SUB])                                        # o menos veio da divisão
        self.passo(61.3, Indicate(self.r1_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.6)
        self.passo(62.7, Indicate(cx, color=G.LARANJA), dur=0.6)               # subtrai os expoentes

        self.passo(64.4, *self.aparece(Y2, 0, 1), dur=0.5)                     # 3^2
        self.passo(66.7, *self.aparece(Y2, 2), dur=0.3)                        # dividido por
        self.passo(67.4, *self.aparece(Y2, 3), dur=0.5)                        # 3^(log3 5)
        self.passo(70.4, *self.aparece(Y3, 0, 1), dur=0.5)                     # isso vai dar 3^2
        self.passo(71.9, *self.aparece(Y3, 2, 3), dur=0.5)                     # dividido por cinco
        self.passo(73.9, Indicate(self.m_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.8)
        self.passo(76.0, Indicate(Y3, color=G.LARANJA, scale_factor=1.06), dur=0.7)
        self.passo(77.5, *self.aparece(Y4, 0, 1, cor=G.VERDE), dur=0.6)        # nove sobre cinco
        cv = self.guarda(self.caixa(Y4, G.VERDE, folga=0.1))
        self.passo(78.8, FadeIn(cv), dur=0.5)                                  # guardadinho
        self.passo(80.4, self.resolve_roteiro(1, ("y", "=", r"\dfrac{9}{5}")), dur=0.6)

    # ================================================================== z  (82,4 – 162,0)
    def parte_z(self):
        XI, Y0, P = G.XI_XY, G.CONTA_Y0, G.CONTA_PASSO
        # "agora bora no z"
        self.limpa_trabalho(82.4, dur=0.7, extra=self.troca_cab(1, 2))

        Z1 = self.linha("z", "=", "6", r"{}^{(\log_9 4)(\log_6 3)}", y=Y0, x_igual=XI, idx=1)
        Z2 = self.linha("=", r"\bigl(", r"6^{\log_6 3}", r"\bigr)^{\log_9 4}",
                        y=Y0 - P, x_igual=XI, idx=0)
        Z3 = self.linha("=", "3", r"{}^{\log_9 4}", y=Y0 - 2 * P, x_igual=XI, idx=0)
        S1 = self.linha(r"\log_9 4", "=", r"\log_{3^2}2^2", y=Y0 - P, x_esq=-3.9)   # conta lateral: alinha pela esquerda
        S2 = self.linha("=", "2", r"\cdot", r"\dfrac{1}{2}", r"\cdot", r"\log_3 2",
                        y=Y0 - 2 * P, x_igual=XI, idx=0)
        Z4 = self.linha("=", r"3^{\log_3 2}", y=Y0 - 3 * P, x_igual=XI, idx=0)
        Z5 = self.linha("=", "2", y=Y0 - 4 * P, x_igual=XI, idx=0)

        self.passo(83.4, *self.aparece(Z1, 0, 1, 2, 3), dur=0.5)
        self.passo(87.9, Indicate(self.m_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.8)   # mesma propriedade
        self.passo(90.5, Indicate(self.m_rule[0], color=G.LARANJA), dur=0.8)                   # base = base do log

        # 93,7  produto no expoente = expoente dentro e expoente fora
        cz = self.guarda(self.caixa_expoente(Z1[3], G.AZUL))
        self.passo(93.8, FadeIn(cz), dur=0.5)
        self.troca_regra(96.8, [R_PROD])

        # 102,4  (6^(log6 3))^(log9 4)
        self.passo(102.4, *self.aparece(Z2, 0, 1, 2), dur=0.6)
        self.passo(105.9, *self.aparece(Z2, 3), dur=0.6)

        # 111,1  agora o seis está elevado ao log de três na base seis -> dá três
        cin = self.guarda(self.caixa(Z2[2], G.AMARELO, folga=0.08))
        self.passo(111.1, FadeIn(cin), dur=0.5)
        self.passo(113.8, Indicate(self.m_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.7)
        lb3 = self.tex("3", escala=0.7, cor=G.VERDE)
        lb3.move_to(_v(cin.get_center()[0], cin.get_bottom()[1] - 0.2))
        self.guarda(lb3)
        self.passo(115.0, FadeIn(lb3), dur=0.5)
        self.passo(116.1, *self.aparece(Z3, 0, 1, 2), *self.some(cin, lb3), dur=0.6)

        # 119,4  "agora olha só uma coisa": fica só o 3^(log9 4) em cima
        self.passo(119.4, *self.some(Z1, Z2, cz), Z3.animate.shift(UP * 2 * P), dur=0.8)
        self.troca_regra(121.1, [R_PET1])                                      # expoente em cima do log
        self.passo(128.5, Indicate(self.r1_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.7)
        self.troca_regra(135.3, [R_PET2])                                      # expoente na base
        self.passo(139.7, Indicate(self.r1_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.7)

        # 141,3  olhando pra aquele log de quatro na base nove
        cl = self.guarda(self.caixa_expoente(Z3[2], G.AZUL))
        self.passo(141.3, FadeIn(cl), dur=0.5)
        self.passo(143.6, *self.aparece(S1, 0, 1, 2), dur=0.7)                 # log_(3^2) 2^2
        self.passo(146.7, Indicate(S1[2], color=G.LARANJA), dur=0.6)           # ao quadrado do quatro
        self.passo(148.7, *self.aparece(S2, 0, 1), dur=0.5)                    # ... multiplicando por 2
        self.passo(149.9, Indicate(S1[2], color=G.LARANJA), dur=0.6)           # ao quadrado do três
        self.passo(153.4, *self.aparece(S2, 2, 3), dur=0.6)                    # de cabeça pra baixo: 1/2
        self.passo(154.9, *self.aparece(S2, 4, 5), dur=0.5)                    # a gente ficou com log_3 2
        self.passo(156.4, *self.aparece(Z4, 0, 1), dur=0.6)                    # 3^(log3 2)
        self.passo(159.4, Indicate(self.m_caixa, color=G.LARANJA, scale_factor=1.08), dur=0.7)
        self.passo(160.8, *self.aparece(Z5, 0, 1, cor=G.VERDE), dur=0.5)       # isso vai dar dois
        cv = self.guarda(self.caixa(Z5, G.VERDE, folga=0.1))
        self.passo(161.4, FadeIn(cv), self.resolve_roteiro(2, ("z", "=", "2")), dur=0.5)

    # ================================================================== produto  (162,0 – 173,3)
    def produto(self):
        XP, Y0, P = G.XI_PROD, G.CONTA_Y0, G.CONTA_PASSO
        # "é só a gente multiplicar": limpa contas, regras e destaque do cabeçalho
        extra = [FadeOut(m) for m in self.regras] + [FadeOut(self.cab_box)]
        self.regras = []
        self.limpa_trabalho(162.0, dur=0.7, extra=extra)

        P1 = self.linha(r"x\cdot y\cdot z", "=", "40", r"\cdot", r"\dfrac{9}{5}", r"\cdot", "2",
                        y=Y0, x_igual=XP, idx=1)
        P2 = self.linha("=", "8", r"\cdot", "9", r"\cdot", "2", y=Y0 - P, x_igual=XP, idx=0)
        P3 = self.linha("=", "72", r"\cdot", "2", y=Y0 - 2 * P, x_igual=XP, idx=0)
        P4 = self.linha("=", "144", y=Y0 - 3 * P, x_igual=XP, idx=0)
        ann = self.tex(r"40\div 5=8", escala=0.7, cor=G.VERDE)
        ann.move_to(_v(P2.get_right()[0] + 0.25 + ann.width / 2, Y0 - P))
        self.guarda(ann)

        self.passo(162.9, *self.aparece(P1, 0, 1, 2), dur=0.5)                 # x·y·z = 40
        self.passo(164.2, *self.aparece(P1, 3, 4), dur=0.6)                    # · 9/5
        self.passo(165.8, *self.aparece(P1, 5, 6), dur=0.4)                    # · 2
        self.passo(166.4, FadeIn(ann), dur=0.5)                                # quarenta por cinco
        self.passo(167.0, *self.aparece(P2, 0, 1), dur=0.4)                    # dá oito
        self.passo(167.95, *self.aparece(P2, 2, 3), dur=0.3)                   # oito vezes nove
        self.passo(168.35, *self.aparece(P2, 4, 5), dur=0.3)
        self.passo(168.8, *self.aparece(P3, 0, 1), dur=0.4)                    # que dá setenta e dois
        self.passo(169.7, *self.aparece(P3, 2, 3), dur=0.4)                    # vezes dois

        # alternativas (coluna da direita) e resultado
        alts = []
        for i, (letra, tx, _) in enumerate(G.ALTERNATIVAS):
            m = self.texto(r"(%s)\quad $%s$" % (letra, tx), escala=0.7, larg_max=2.75)
            m.move_to(_v(0, G.ALT_YS[i]))
            m.shift(_v(G.ALT_X - m.get_left()[0], 0))
            alts.append(m)
        self.passo(170.3, *[FadeIn(m) for m in alts], dur=0.6)
        self.passo(171.5, *self.aparece(P4, 0, 1, cor=G.VERDE),
                   self.resolve_roteiro(3, (r"x\cdot y\cdot z", "=", "144")), dur=0.6)
        letra_c = [m for m, a in zip(alts, G.ALTERNATIVAS) if a[0] == G.GABARITO][0]
        self.passo(172.7, FadeIn(self.caixa(letra_c, G.VERDE, folga=0.08)), dur=0.5)   # letra C

    # ================================================================== final  (173,3 – 179,0)
    def final(self):
        self.passo(174.6, Indicate(self.marca, color=G.AZUL, scale_factor=1.3), dur=0.8)   # salva
        self.passo(176.5, Indicate(self.marca, color=G.AZUL, scale_factor=1.3), dur=0.8)   # segue
        self.ate(179.0)
