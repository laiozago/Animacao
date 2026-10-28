# -*- coding: utf-8 -*-
"""
Base dos vídeos Manim do @proflaiozago (padrão oficial + layout v2: rosto no meio-esquerda).
Manim Community >= 0.18.

Formato 9:16, fundo do tema, relógio da fala (ate / passo), roteiro na faixa, guias de prévia,
fórmulas peça por peça. Cada questão herda daqui e só descreve a sequência.

REGRA DOS MÉTODOS COM TEMPO: todo método que toca animação recebe o instante da fala `t`
como PRIMEIRO argumento depois de self, e a duração em `dur=` (o teste_tempos.py lê isso).
"""
import numpy as np
from manim import *

import geometria as G

# ------------------------------------------------------------------ formato 9:16
_ALVO = {480: (540, 960), 720: (720, 1280), 1080: (1080, 1920), 1440: (1440, 2560), 2160: (2160, 3840)}


def _formato_vertical():
    """-ql = 540x960 (prévia) · -qm = 720x1280 · -qh = 1080x1920 (final). Quadro sempre 9 x 16."""
    if config.pixel_height in _ALVO:
        config.pixel_width, config.pixel_height = _ALVO[config.pixel_height]
    config.frame_width, config.frame_height = 9.0, 16.0
    config.background_color = G.FUNDO


_formato_vertical()


def P(x, y):
    """Ponto 3D a partir de (x, y)."""
    return np.array([x, y, 0.0])


class CenaBase(Scene):
    GUIAS = "auto"            # "auto" = liga só na prévia (-ql); True/False força

    # -------------------------------------------------------------- preparo e fim
    def setup(self):
        self.atrasos = []     # (instante pedido, atraso em s, nome)
        self.rot = {}         # itens do roteiro por chave
        self.painel = []      # tudo o que mora na coluna das contas (para limpar de uma vez)

    def tear_down(self):
        super().tear_down()
        print("\n>>> Duração da animação: %.2f s" % self.renderer.time)
        if self.atrasos:
            print(">>> PASSOS ATRASADOS (instante pedido | atraso | passo) - ajuste só o número do instante:")
            for t, a, nome in self.atrasos:
                print("      %7.2f s | +%.2f s | %s" % (t, a, nome))
        else:
            print(">>> Sincronia OK: nenhum passo atrasado.")

    # -------------------------------------------------------------- relógio da fala
    def ate(self, t):
        """Espera até o instante t (s) da fala. Não faz nada se já passou."""
        falta = t - self.renderer.time
        if falta >= 0.5 / config.frame_rate:
            self.wait(falta)

    def passo(self, t, *anims, dur=0.8, nome=""):
        """Espera até t e toca as animações juntas, com a mesma duração."""
        self.ate(t)
        atraso = self.renderer.time - t
        if atraso > 0.15:
            self.atrasos.append((t, round(atraso, 2), nome or "passo"))
        if anims:
            self.play(*anims, run_time=dur)

    # -------------------------------------------------------------- criação de objetos
    def tex(self, *partes, cor=None, escala=1.0):
        """MathTex na cor do tema (MathTex nasce branco). Sempre use isto."""
        return MathTex(*partes, color=cor or G.TEXTO).scale(escala)

    def texto(self, s, cor=None, escala=1.0):
        return Text(s, color=cor or G.TEXTO, font_size=48).scale(escala)

    def ajusta(self, m, larg_max):
        if m.width > larg_max:
            m.scale(larg_max / m.width)
        return m

    def linha(self, partes, y, escala=None, x_esq=None, cx=None, cores=None, larg_max=None):
        """Fórmula peça por peça: nasce INVISÍVEL; use aparece(...) nos instantes da fala.
        Cada parte tem de ser LaTeX válido sozinha. `x_esq` = borda esquerda, `cx` = centro,
        `cores` = {índice: cor}."""
        escala = escala or G.ESC["conta"]
        m = MathTex(*partes, color=G.TEXTO).scale(escala)
        if larg_max and m.width > larg_max:
            m.scale(larg_max / m.width)
        m.move_to(P(cx if cx is not None else 0, y))
        if x_esq is not None:
            m.shift(RIGHT * (x_esq - m.get_left()[0]))
        for i, c in (cores or {}).items():
            m[i].set_color(c)
        m.set_opacity(0)
        self.add(m)
        self.painel.append(m)
        return m

    def alinha_igual(self, l2, l1, i1=1):
        """Alinha o '=' do começo de l2 (peça 0) com o '=' de l1 (peça i1)."""
        l2.shift(RIGHT * (l1[i1].get_left()[0] - l2[0].get_left()[0]))

    def aparece(self, *partes):
        """Animações que revelam partes de uma fórmula criada com linha()."""
        return [p.animate.set_opacity(1) for p in partes]

    # -------------------------------------------------------------- cancelar / destacar
    def glifo(self, parte, modo):
        """Escolhe um símbolo dentro de uma parte: 'dir' (mais à direita), 'baixo' (denominador),
        'cima' (numerador). Cai para a parte inteira se ela não tiver símbolos separados."""
        subs = list(parte.submobjects)
        if len(subs) < 2:
            return parte
        if modo == "dir":
            return max(subs, key=lambda m: m.get_center()[0])
        if modo == "baixo":
            return min(subs, key=lambda m: m.get_center()[1])
        return max(subs, key=lambda m: m.get_center()[1])

    def corte(self, alvo, cor=None, ext=0.05):
        """Risco diagonal sobre `alvo` (cancelamento). Toque com Create(...)."""
        r = Line(alvo.get_corner(DL) + P(-ext, -ext), alvo.get_corner(UR) + P(ext, ext),
                 color=cor or G.LARANJA, stroke_width=5)
        self.painel.append(r)
        return r

    def pulso(self, alvo, cor=None, fator=1.18):
        return Indicate(alvo, color=cor or G.LARANJA, scale_factor=fator)

    def sai(self, mobs=None):
        """FadeOut de tudo o que está na coluna das contas (ou só de `mobs`)."""
        alvo = list(mobs) if mobs is not None else list(self.painel)
        for m in alvo:
            if m in self.painel:
                self.painel.remove(m)
        return [FadeOut(m) for m in alvo]

    def voa_copia(self, t, origem, destino, dur=0.8):
        """Uma cópia de `origem` (visível) viaja e vira `destino` (peça escondida de linha())."""
        copia = origem.copy()
        alvo = destino.copy().set_opacity(1)
        self.add(copia)
        self.passo(t, Transform(copia, alvo), dur=dur, nome="voa_copia")
        destino.set_opacity(1)
        self.remove(copia)

    # -------------------------------------------------------------- roteiro (faixa ao lado do rosto)
    def _rot(self, tex, cor, chave):
        m = MathTex(tex, color=cor).scale(G.ESC["rot"])
        self.ajusta(m, G.FAIXA[2] - G.ROT_X)
        m.move_to(P(G.ROT_X, G.ROT_Y[chave]), aligned_edge=LEFT)
        return m

    def anim_rot_entra(self, chave):
        """Animação (não toca) de entrada do item do roteiro, em vermelho ('falta descobrir')."""
        m = self._rot(G.ROTULOS["rot"][chave][0], G.VERMELHO, chave)
        self.rot[chave] = m
        return FadeIn(m, shift=0.2 * LEFT)

    def anim_rot_resolve(self, chave):
        """Animação (não toca): o item vira verde com o valor ('já resolvido')."""
        novo = self._rot(G.ROTULOS["rot"][chave][1], G.VERDE, chave)
        anim = ReplacementTransform(self.rot[chave], novo)
        self.rot[chave] = novo
        return anim

    def roteiro_entra(self, t, chave, dur=0.5):
        self.passo(t, self.anim_rot_entra(chave), dur=dur, nome="roteiro " + chave)

    def roteiro_resolve(self, t, chave, dur=0.7):
        self.passo(t, self.anim_rot_resolve(chave), dur=dur, nome="resolve " + chave)

    # -------------------------------------------------------------- marca d'água e guias
    def marca_dagua(self):
        m = Text("@proflaiozago", font_size=22, color=G.CINZA)
        self.ajusta(m, 1.9)
        m.move_to(P(*G.MARCA))
        self.add(m)
        self.marca = m

    def _moldura(self, zona, cor):
        x0, y0, x1, y1 = zona
        r = Rectangle(width=x1 - x0, height=y1 - y0, color=cor, stroke_width=3)
        return r.move_to(P((x0 + x1) / 2, (y0 + y1) / 2))

    def guias(self):
        """Prévia (-ql): três molduras SEPARADAS, sem nomes: rosto (vermelha), conta = palco (azul) e
        respostas parciais = faixa ao lado do rosto (azul). Nenhuma liga com a outra."""
        ligar = self.GUIAS is True or (self.GUIAS == "auto" and config.pixel_height < 1000)
        if not ligar:
            return
        self.add(self._moldura(G.ROSTO, G.VERMELHO), self._moldura(G.PALCO, G.AZUL),
                 self._moldura(G.FAIXA, G.AZUL))

    # -------------------------------------------------------------- enunciado em texto
    def enunciado(self):
        """Abertura (PADRÃO): o texto INTEGRAL da prova (título, enunciado e alternativas), recomposto para
        usar toda a largura do palco com a maior fonte que couber. As quebras de linha vêm de
        geometria.melhor_composicao(); aqui só se mede o texto real e ajusta ao palco."""
        comp = G.melhor_composicao()
        fs = 40
        mk = lambda s, neg: Text(s, font=G.FONTE_ENUNCIADO, font_size=fs, color=G.TEXTO,
                                 weight=BOLD if neg else NORMAL)
        linhas = [(mk(t.replace("\u00a0", " "), neg), t, y) for t, neg, y in comp["linhas"]]
        # unidades por em medidas no texto de verdade (a fonte pode ser outra se não houver Arial)
        mais_larga = max(linhas, key=lambda x: G.largura_em(x[1]))
        em_u = mais_larga[0].width / G.largura_em(mais_larga[1])
        # profundidade dos descendentes (g, p, q...), para alinhar as linhas pela linha de base e não pelo contorno
        prof = mk("Ag", False).height - mk("A", False).height
        g = VGroup()
        for m, t, y_em in linhas:
            desce = 1.0 if any(c in "gjpqyçÇ()" for c in t) else (0.55 if any(c in ",;" for c in t) else 0.0)
            m.align_to(P(0, -y_em * em_u - desce * prof), DOWN)
            m.align_to(P(-1, 0), LEFT)
            g.add(m)
        larg, alt = G.BOX_ENUNCIADO
        g.scale(min(larg / g.width, alt / g.height))
        return g.move_to(P(0, (G.PALCO[1] + G.PALCO[3]) / 2))
