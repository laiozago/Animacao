# -*- coding: utf-8 -*-
"""
cena_base.py — base do padrão @proflaiozago (layout v2: rosto no meio-esquerda)

  • vertical 9:16, fundo claro, sem título, marca d'água @proflaiozago
  • a resolução acontece só no PALCO (parte branca de cima); o roteiro e a marca
    d'água ficam na FAIXA ao lado do rosto; zonas vermelhas do TikTok/Instagram
    nunca são usadas (ver geometria.py)
  • sincronia com a fala: ate(t) / passo(t, *anims, dur=)
  • GUIAS (zonas vermelhas, rosto, palco) ficam DESLIGADAS por padrão: o fundo é todo
    branco. Para conferir o layout, ponha GUIAS = True na classe da cena.
"""
import numpy as np
from manim import *
import geometria as G

# ── formato 9:16: a qualidade (-ql / -qh) decide só a resolução ──────────────
_ALTURAS = {480: 960, 720: 1280, 1080: 1920, 1440: 2560, 2160: 3840}
PREVIA = int(config.pixel_height) <= 480
_H = _ALTURAS.get(int(config.pixel_height), 1920)
config.frame_height = G.QUADRO.y1 - G.QUADRO.y0      # 16
config.frame_width = G.QUADRO.x1 - G.QUADRO.x0       # 9
config.pixel_height = _H
config.pixel_width = _H * 9 // 16
config.background_color = G.FUNDO


def p3(x, y=0.0):
    """(x, y) -> ponto 3D do Manim."""
    return np.array([float(x), float(y), 0.0])


# ═════════════════════════════════════════════════════════════════════════════
class Coluna:
    """Coluna das contas (palco, à direita do plano): linhas de peças MathTex,
    alinhadas à esquerda, de cima para baixo. Cada linha é uma lista de peças que
    aparecem uma a uma, no instante da fala."""

    def __init__(self, cena):
        self.c = cena
        self.reinicia()

    def reinicia(self):
        self.y = G.COLUNA.y1
        self.todas = []

    def _confere(self, pecas):
        direita = max(p.get_right()[0] for p in pecas)
        base = min(p.get_bottom()[1] for p in pecas)
        if direita > G.COLUNA.x1 + 1e-6:
            self.c.avisa(f"linha passa da coluna em {direita - G.COLUNA.x1:.2f} u")
        if base < G.COLUNA.y0 - 1e-6:
            self.c.avisa(f"coluna estourou embaixo em {G.COLUNA.y0 - base:.2f} u")

    def linha(self, *specs, escala=None, recuo=0.0, folga=0.16):
        """Cria (sem mostrar) uma linha de peças e devolve a lista. spec = texto TeX
        ou lista [(trecho, cor), ...] para colorir partes."""
        escala = escala or G.COL_ESCALA
        pecas = [self.c.tex(s, escala) for s in specs]
        altura = max(p.height for p in pecas)
        yc = self.y - altura / 2
        x = G.COLUNA.x0 + recuo
        for p in pecas:
            p.move_to(p3(x + p.width / 2, yc))
            x += p.width + G.COL_BUFF * escala
        self.y -= altura + folga
        self.todas += pecas
        self._confere(pecas)
        return pecas

    def sobre(self, velha, spec, escala=None):
        """Peça nova no MESMO lugar de `velha` (borda esquerda); troque com ReplacementTransform."""
        n = self.c.tex(spec, escala or G.COL_ESCALA)
        n.move_to(velha.get_left(), aligned_edge=LEFT)
        self.todas.append(n)
        self._confere([n])
        return n

    def limpa(self):
        """Animações que tiram da tela tudo que está na coluna; zera o cursor."""
        saem = [m for m in self.todas if m in self.c.mobjects]
        self.reinicia()
        return [FadeOut(m) for m in saem]


class Roteiro:
    """Itens do que se quer achar: vermelho com '?', viram verde quando resolvidos.
    Ficam na faixa ao lado do rosto, de cima para baixo na ordem em que são criados."""

    def __init__(self, cena):
        self.c = cena
        self.itens = {}

    def novo(self, chave, pendente, resolvido):
        y = G.ROTEIRO_Y[len(self.itens)]
        p = self.c.tex(pendente, G.ROTEIRO_ESCALA, G.VERMELHO)
        r = self.c.tex(resolvido, G.ROTEIRO_ESCALA, G.VERDE)
        for m in (p, r):
            m.move_to(p3(G.ROTEIRO_X, y), aligned_edge=LEFT)
        self.itens[chave] = (p, r)

    def mostra(self, chave):
        return FadeIn(self.itens[chave][0])

    def resolve(self, chave):
        p, r = self.itens[chave]
        return ReplacementTransform(p, r)


# ═════════════════════════════════════════════════════════════════════════════
class CenaBase(Scene):
    GUIAS = False         # False = tudo branco (padrão) · True = guias vermelhas/rosto · "auto" = só no -ql

    def setup(self):
        self.t = 0.0              # relógio da fala (s), contado em quadros reais
        self.atrasos = []
        self.avisos = []
        self.always_update_mobjects = True   # esperas quadro a quadro: o relógio fecha com a fala

    # ── relógio da fala ──────────────────────────────────────────────────────
    @staticmethod
    def _quadros(dur):
        return len(np.arange(0, dur, 1.0 / config.frame_rate))

    def _gasta(self, dur):
        self.t += self._quadros(dur) / config.frame_rate

    def ate(self, t):
        """Espera até o instante t (s) da fala."""
        falta = t - self.t
        if falta >= 1.0 / config.frame_rate:
            self.wait(falta)
            self._gasta(falta)

    def passo(self, t, *anims, dur=0.6):
        """Espera até t e toca as animações. Se começar >0,15 s depois de t, anota o atraso."""
        atraso = self.t - t
        if atraso > 0.15:
            self.atrasos.append((t, round(atraso, 2)))
        self.ate(t)
        dur = max(dur, 1.0 / config.frame_rate)
        if anims:
            self.play(*anims, run_time=dur)
        else:
            self.wait(dur)
        self._gasta(dur)

    def avisa(self, texto):
        self.avisos.append(texto)
        print(f"[aviso] {texto}")

    def tear_down(self):
        super().tear_down()
        print(f"\n[sincronia] animação terminou em {self.t:.2f} s")
        if self.atrasos:
            print("[sincronia] passos que começaram atrasados (instante pedido, atraso em s):")
            for t, a in self.atrasos:
                print(f"    {t:7.2f}  +{a}")
        else:
            print("[sincronia] todos os passos começaram no instante pedido.")
        if self.avisos:
            print("[layout] avisos:")
            for a in self.avisos:
                print("    ", a)

    # ── fábrica de objetos no padrão ─────────────────────────────────────────
    def tex(self, texto, escala=1.0, cor=None):
        """MathTex nasce BRANCO: aqui já sai na cor do tema. `texto` pode ser uma
        lista [(trecho, cor), ...] para colorir partes."""
        if isinstance(texto, (list, tuple)):
            m = MathTex(*[t for t, _ in texto], color=cor or G.TEXTO)
            for i, (_, c) in enumerate(texto):
                if c:
                    m[i].set_color(c)
        else:
            m = MathTex(texto, color=cor or G.TEXTO)
        return m.scale(escala)

    def rotulo(self, chave, cor=None, fundo=True):
        """Rótulo da figura na posição de geometria.ROTULOS (com fundo branco para
        não ser cortado por grade/eixo)."""
        r = G.ROTULOS[chave]
        t = self.tex(r["tex"], r["esc"], cor)
        t.move_to(p3(*r["pos"]), aligned_edge=LEFT if r["modo"] == "L" else ORIGIN)
        if not fundo:
            return t
        bg = BackgroundRectangle(t, color=G.FUNDO, fill_opacity=0.9, buff=0.04)
        return VGroup(bg, t)

    def marca_dagua(self):
        m = Text("@proflaiozago", font_size=18, color=G.CINZA)
        if m.width > G.MARCA_LARG_MAX:
            m.scale_to_fit_width(G.MARCA_LARG_MAX)
        m.move_to(p3(*G.MARCA_CENTRO))
        return m

    def ajusta(self, mob, largura_max, altura_max=None):
        """Reduz `mob` (nunca amplia) para caber na largura/altura dadas."""
        k = 1.0
        if mob.width > largura_max:
            k = min(k, largura_max / mob.width)
        if altura_max and mob.height > altura_max:
            k = min(k, altura_max / mob.height)
        if k < 1.0:
            mob.scale(k)
        return mob

    # ── guias da prévia ──────────────────────────────────────────────────────
    def guias_ligadas(self):
        return PREVIA if self.GUIAS == "auto" else bool(self.GUIAS)

    def guias(self):
        """Zonas vermelhas, quadrado do rosto e palco (só para conferir no CapCut)."""
        def caixa(c, **kw):
            r = Rectangle(width=c.x1 - c.x0, height=c.y1 - c.y0, **kw)
            return r.move_to(p3((c.x0 + c.x1) / 2, (c.y0 + c.y1) / 2))
        g = VGroup()
        for z in G.EVITAR:
            g.add(caixa(z, stroke_width=0, fill_color="#FF2A00", fill_opacity=0.22))
        g.add(caixa(G.ROSTO, stroke_color="#00A651", stroke_width=3, fill_color="#00A651", fill_opacity=0.06))
        g.add(caixa(G.PALCO, stroke_color=G.AZUL, stroke_width=1.5, fill_opacity=0))
        g.add(caixa(G.FAIXA, stroke_color=G.AZUL, stroke_width=1.5, fill_opacity=0))
        g.add(Text("ROSTO", font_size=26, color="#00A651").move_to(
            p3((G.ROSTO.x0 + G.ROSTO.x1) / 2, (G.ROSTO.y0 + G.ROSTO.y1) / 2)))
        g.set_z_index(1000)
        return g