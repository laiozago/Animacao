"""Base das cenas 9:16 do @proflaiozago (layout "rosto no meio-esquerda").

- quadro 9 x 16 unidades; -ql = 540x960, -qh = 1080x1920 (ajusta sozinha pela qualidade)
- relógio da fala: ate(t) / passo(t, *anims, dur=)  -> avisa no terminal os passos atrasados
- contas peça por peça: linha(...) cria a fórmula com tudo invisível; aparece(...) revela as partes
- roteiro na faixa ao lado do rosto (vermelho "?" -> verde quando resolvido)
- molduras-guia das zonas: DESLIGADAS por padrão (GUIAS = False); True/"auto" só para conferir layout
"""
import numpy as np
from manim import (Scene, config, MathTex, Tex, VGroup, Rectangle, RoundedRectangle, Polygon,
                   FadeIn, FadeOut, ReplacementTransform, Indicate)

import geometria as G


# ----------------------------------------------------------------------------------------------
# formato do quadro (roda ao importar, antes de a cena ser criada)
# ----------------------------------------------------------------------------------------------
_VERTICAL = {480: (540, 960), 720: (720, 1280), 1080: (1080, 1920),
             1440: (1440, 2560), 2160: (2160, 3840)}


def _configura_quadro():
    config.frame_width = 9.0
    config.frame_height = 16.0
    alt = int(config.pixel_height)
    if alt in _VERTICAL:                      # ainda horizontal: troca pela resolução vertical
        config.pixel_width, config.pixel_height = _VERTICAL[alt]


_configura_quadro()


def _v(x, y):
    return np.array([x, y, 0.0])


class CenaBase(Scene):
    GUIAS = False             # molduras-guia: False = nenhuma (padrão) | True = sempre | "auto" = só na prévia (-ql)

    # ------------------------------------------------------------------ preparo e relógio
    def setup(self):
        self.camera.background_color = G.FUNDO
        self.t = 0.0                  # relógio planejado (reserva); o real é agora()
        self.atrasos = []             # (instante pedido, atraso)
        self.trab = []                # tudo que está hoje na coluna esquerda das contas
        self.regras = []              # tudo que está hoje na coluna direita (regras)

    def agora(self):
        """Tempo já renderizado (s). Usa o relógio do Manim (conta quadros de verdade), de modo que o
        arredondamento por quadro nunca acumula; se não existir, cai para o relógio planejado."""
        tm = getattr(getattr(self, "renderer", None), "time", None)
        return float(tm) if isinstance(tm, (int, float)) else self.t

    def ate(self, t):
        """Espera até o instante t da fala."""
        falta = t - self.agora()
        if falta > 0.5 / config.frame_rate:
            self.wait(falta)
        self.t = max(self.t, t)

    def passo(self, t, *anims, dur=0.6):
        """Espera até t e toca as animações juntas (duram dur)."""
        self.ate(t)
        atraso = self.agora() - t
        if atraso > 0.15:
            self.atrasos.append((t, round(atraso, 2)))
        if anims:
            self.play(*anims, run_time=dur)
        else:
            self.wait(dur)
        self.t = max(self.t, t) + dur

    def fim(self):
        if self.atrasos:
            print("\n=== PASSOS ATRASADOS (instante pedido, atraso em s) ===")
            for t, a in self.atrasos:
                print("  %7.2f s   atrasou %.2f s" % (t, a))
        else:
            print("\nSincronia ok: nenhum passo atrasou mais de 0,15 s.")
        print("Duração da animação: %.1f s" % self.agora())

    # ------------------------------------------------------------------ objetos
    def ajusta(self, m, larg_max=None):
        larg_max = larg_max or G.LARG_MAX
        if m.width > larg_max:
            m.scale(larg_max / m.width)
        return m

    def tex(self, *partes, escala=0.9, cor=None, larg_max=None):
        """Fórmula na cor do tema (MathTex nasce branco!)."""
        m = MathTex(*partes, color=cor or G.TEXTO)
        m.scale(escala)
        return self.ajusta(m, larg_max)

    def texto(self, s, escala=0.8, cor=None, larg_max=None):
        """Texto corrido (LaTeX, aceita $...$)."""
        m = Tex(s, color=cor or G.TEXTO)
        m.scale(escala)
        return self.ajusta(m, larg_max)

    def linha(self, *partes, y, x_igual=None, idx=0, x_esq=None, escala=None, cor=None, oculta=True):
        """Linha de conta. Todas as partes nascem invisíveis; use aparece() nos instantes certos.
        x_igual: abscissa onde fica a borda esquerda do "=" (a parte de índice idx) — alinha as contas.
        """
        m = self.tex(*partes, escala=escala or G.ESCALA_CONTA, cor=cor)
        m.move_to(_v(0, y))
        if x_igual is not None:
            m.shift(_v(x_igual - m[idx].get_left()[0], 0))
        else:
            m.shift(_v((G.CONTA_X_ESQ if x_esq is None else x_esq) - m.get_left()[0], 0))
        if oculta:
            m.set_opacity(0)
        self.add(m)
        self.trab.append(m)
        return m

    def aparece(self, m, *idx, cor=None):
        """Animações que revelam as partes idx da fórmula m (opcionalmente numa cor)."""
        anims = []
        for i in idx:
            a = m[i].animate.set_opacity(1)
            if cor:
                a = a.set_color(cor)
            anims.append(a)
        return anims

    def caixa(self, m, cor, folga=0.1, espessura=3):
        r = Rectangle(width=m.width + 2 * folga, height=m.height + 2 * folga,
                      color=cor, stroke_width=espessura, fill_opacity=0)
        r.move_to(m.get_center())
        return r

    def caixa_expoente(self, parte, cor, folga=0.07):
        """Caixa em volta do expoente. `parte` é a peça da fórmula que contém SÓ o expoente,
        escrita como r"{}^{...}" logo depois da base (compõe igual a base^{...})."""
        return self.caixa(parte, cor, folga=folga)

    def guarda(self, *ms):
        """Registra objetos extras (caixas, rótulos) para sumirem junto com a coluna das contas."""
        for m in ms:
            self.trab.append(m)
        return ms[0] if len(ms) == 1 else ms

    def limpa_trabalho(self, t, dur=0.7, extra=()):
        fades = [FadeOut(m) for m in self.trab]
        self.trab = []
        self.passo(t, *fades, *extra, dur=dur)

    # ------------------------------------------------------------------ coluna das regras (direita)
    def caixa_regra(self, y, h=0.95, cor=None):
        r = RoundedRectangle(corner_radius=0.12, width=G.REGRA_W, height=h,
                             color=cor or G.AMARELO, stroke_width=3, fill_opacity=0)
        r.move_to(_v(G.REGRA_X, y))
        return r

    def regra_tex(self, partes, y, cor=None):
        m = self.tex(*partes, escala=G.REGRA_ESCALA, cor=cor, larg_max=G.REGRA_W - 0.3)
        m.move_to(_v(G.REGRA_X, y))
        return m

    # ------------------------------------------------------------------ roteiro (faixa ao lado do rosto)
    def item_roteiro(self, i, partes, cor):
        m = self.tex(*partes, escala=G.ROT_ESCALA, cor=cor, larg_max=G.ROT_LARG)
        m.move_to(_v(0, G.ROT_YS[i]))
        m.shift(_v(G.ROT_X - m.get_left()[0], 0))
        return m

    def cria_roteiro(self, itens):
        self.rot = [self.item_roteiro(i, p, G.VERMELHO) for i, p in enumerate(itens)]
        return self.rot

    def resolve_roteiro(self, i, partes):
        """Troca o item i do roteiro por uma versão verde (resolvido). Retorna a animação."""
        novo = self.item_roteiro(i, partes, G.VERDE)
        anim = ReplacementTransform(self.rot[i], novo)
        self.rot[i] = novo
        return anim

    # ------------------------------------------------------------------ marca d'água e guias
    def marca_dagua(self):
        self.marca = Tex("@proflaiozago", color=G.CINZA).scale(0.5)
        self.ajusta(self.marca, 1.8)
        self.marca.move_to(_v(*G.MARCA_POS))
        self.add(self.marca)
        return self.marca

    def desenha_guias(self):
        """Molduras-guia opcionais (desligadas por padrão): rosto (vermelha) e resolução (azul = palco +
        faixa do roteiro), sem nomes. GUIAS = True liga sempre; "auto" liga só na prévia (-ql)."""
        ativo = self.GUIAS is True or (self.GUIAS == "auto" and config.pixel_width <= 540)
        if not ativo:
            return
        px0, px1, py0, py1 = G.PALCO
        fx0, fx1, fy0, _fy1 = G.FAIXA
        contorno = [(px0, py1), (px1, py1), (px1, py0), (fx1, py0), (fx1, fy0),
                    (fx0, fy0), (fx0, py0), (px0, py0)]
        resolucao = Polygon(*[_v(x, y) for x, y in contorno], color="#1E88E5",
                            stroke_width=2, stroke_opacity=0.7, fill_opacity=0)
        x0, x1, y0, y1 = G.ROSTO
        rosto = Rectangle(width=x1 - x0, height=y1 - y0, color="#E53935",
                          stroke_width=2, stroke_opacity=0.7, fill_opacity=0)
        rosto.move_to(_v((x0 + x1) / 2, (y0 + y1) / 2))
        self.guias = VGroup(resolucao, rosto)
        self.add(self.guias)
