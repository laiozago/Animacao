"""cena_base.py — base do padrão @proflaiozago (9:16, fundo branco, 3 caixinhas, sincronia com o SRT).

Pode ser usada por qualquer questão: a cena da questão só herda de `CenaBase` e descreve a
sequência. REGRA: todo método que toca animação recebe o instante `t` (s) como 1º argumento
e `dur=` por palavra-chave (o ensaio de tempos lê isso).
"""
import numpy as np
from manim import *

import geometria as G

# ------------------------------------------------------------------ formato 9:16
_FORMATOS = {480: (540, 960), 720: (720, 1280), 1080: (1080, 1920), 1440: (1440, 2560), 2160: (2160, 3840)}


def _ajusta_formato():
    config.frame_width, config.frame_height = 9.0, 16.0
    larg, alt = _FORMATOS.get(int(config.pixel_height), (1080, 1920))
    config.pixel_width, config.pixel_height = larg, alt


_ajusta_formato()


def _v(p, z=0.0):
    return np.array([float(p[0]), float(p[1]), z])


class CenaBase(Scene):
    """Relógio da fala + utilitários de fórmula, roteiro, enunciado e guias."""

    GUIAS = "auto"          # "auto" = só na prévia (-ql) · True · False
    FONTE = "Arial"

    # ------------------------------------------------------------ relógio
    def setup(self):
        self.camera.background_color = G.FUNDO
        self.atrasos = []
        self._t = 0.0

    def agora(self):
        r = getattr(self.renderer, "time", None)
        return float(r) if r is not None else self._t

    def ate(self, t):
        d = t - self.agora()
        if d > 1e-6:
            self.wait(d)
            self._t += d

    def passo(self, t, *anims, dur=0.5, nome=""):
        """Espera até o instante t da fala e toca as animações juntas (mesma dur)."""
        self.ate(t)
        atraso = self.agora() - t
        if atraso > 0.15:
            self.atrasos.append((nome or "?", t, round(atraso, 2)))
        if anims:
            self.play(*anims, run_time=dur)
            self._t += dur

    def fim_render(self):
        if self.atrasos:
            print("\n>>> PASSOS ATRASADOS (nome, instante pedido, atraso em s):")
            for a in self.atrasos:
                print("   ", a)
        else:
            print("\n>>> sincronia: nenhum passo atrasado")

    # ------------------------------------------------------------ texto / fórmulas
    def tex(self, *partes, escala=1.0, cor=None):
        """MathTex na cor do tema (MathTex nasce branco!)."""
        return MathTex(*partes, color=cor or G.TEXTO).scale(escala)

    def linha(self, partes, y, escala=G.ESC_CONTA, x0=G.X0_CONTA, alinhar=None, cores=None):
        """Fórmula peça por peça: nasce com opacidade 0; revele com `aparece(m[i])`.

        alinhar=(outra_linha, i) alinha a peça 0 desta linha com a peça i da outra.
        cores={i: COR} pinta peças antes de revelar."""
        m = self.tex(*partes, escala=escala)
        m.move_to(_v((x0 + m.width / 2, y)))
        if alinhar is not None:
            ref, i = alinhar
            m.shift(RIGHT * (ref[i].get_left()[0] - m[0].get_left()[0]))
        for i, c in (cores or {}).items():
            m[i].set_color(c)
        for p in m:
            p.set_opacity(0)
        self.add(m)
        return m

    @staticmethod
    def aparece(parte):
        return parte.animate.set_opacity(1)

    @staticmethod
    def some(parte):
        return parte.animate.set_opacity(0)

    # ------------------------------------------------------------ destaques
    def caixa(self, alvo, cor=G.AMARELO, buff=0.07, largura=3):
        return SurroundingRectangle(alvo, color=cor, buff=buff, stroke_width=largura)

    def sobreposto(self, mob, cor, largura=7):
        """Cópia grossa e colorida de uma linha/figura, para ligar/desligar sem mexer em opacidade."""
        ov = mob.copy()
        ov.set_color(cor)
        ov.set_stroke(width=largura)
        return ov

    def liga(self, t, ov, dur=0.3, nome=""):
        self.passo(t, FadeIn(ov), dur=dur, nome=nome)

    def desliga(self, t, ov, dur=0.3, nome=""):
        self.passo(t, FadeOut(ov), dur=dur, nome=nome)

    def pisca(self, t, ov, dur=0.7, nome=""):
        """Liga em t e desliga logo em seguida (dur total)."""
        self.liga(t, ov, dur=dur / 2, nome=nome)
        self.desliga(t + dur / 2, ov, dur=dur / 2, nome=nome)

    # ------------------------------------------------------------ roteiro (respostas parciais)
    def monta_roteiro(self, abertos, fechados):
        self.rot_aberto, self.rot_fechado, self.rot_vivo = [], [], [None] * len(abertos)
        for i, (a, f) in enumerate(zip(abertos, fechados)):
            ma = self.tex(*a, escala=G.ESC_ROT, cor=G.VERMELHO)
            mf = self.tex(*f, escala=G.ESC_ROT, cor=G.VERDE)
            for m in (ma, mf):
                m.move_to(_v((G.ROT_X0 + m.width / 2, G.ROT_Y[i])))
            self.rot_aberto.append(ma)
            self.rot_fechado.append(mf)

    def anim_rot_entra(self, i):
        self.rot_vivo[i] = self.rot_aberto[i]
        return FadeIn(self.rot_aberto[i])

    def anim_rot_resolve(self, i):
        self.rot_vivo[i] = self.rot_fechado[i]
        return ReplacementTransform(self.rot_aberto[i], self.rot_fechado[i])

    def rot_entra(self, t, i, dur=0.4):
        self.passo(t, self.anim_rot_entra(i), dur=dur, nome=f"roteiro {i} entra")

    def rot_resolve(self, t, i, dur=0.5):
        self.passo(t, self.anim_rot_resolve(i), dur=dur, nome=f"roteiro {i} resolve")

    # ------------------------------------------------------------ marca d'água e guias
    def marca_dagua(self):
        self.marca = Text("@proflaiozago", font=self.FONTE, color=G.CINZA, font_size=20)
        self.marca.scale_to_fit_width(min(1.85, self.marca.width))
        self.marca.move_to(_v(G.MARCA))
        self.add(self.marca)

    def pulso_marca(self, t, dur=0.8):
        self.passo(t, Indicate(self.marca, color=G.LARANJA, scale_factor=1.25), dur=dur, nome="marca")

    def guias(self):
        ligar = self.GUIAS is True or (self.GUIAS == "auto" and config.quality == "low_quality")
        if not ligar:
            return

        def moldura(z, cor):
            r = Rectangle(width=z[1] - z[0], height=z[3] - z[2], color=cor, stroke_width=2)
            r.move_to(_v(((z[0] + z[1]) / 2, (z[2] + z[3]) / 2)))
            return r

        # molduras separadas, sem nomes: rosto (vermelha), palco/conta, caixa da figura e respostas parciais (azuis)
        self.add(moldura(G.ROSTO, RED), moldura(G.PALCO, BLUE), moldura(G.FIGBOX, BLUE), moldura(G.RESP, BLUE))

    # ------------------------------------------------------------ enunciado integral recomposto
    def enunciado(self):
        """Monta o enunciado (melhor_composicao) com o texto REAL medido e devolve o grupo de linhas.

        O texto entra TODO DE UMA VEZ (pedido do professor); não é digitado palavra por palavra."""
        comp = G.melhor_composicao()
        em_alvo = comp["em"]
        linhas = []
        for it in comp["itens"]:
            tx = Text(it["texto"], font=self.FONTE, color=G.TEXTO, font_size=36,
                      weight=BOLD if it["negrito"] else NORMAL, disable_ligatures=True)
            linhas.append((it, tx))
        # escala: razão entre largura medida e largura da tabela (uniforme p/ o bloco todo)
        medido = sum(tx.width for _, tx in linhas)
        tabela = sum(G.larg_em(it["texto"], it["negrito"]) for it, _ in linhas)
        k = em_alvo / (medido / tabela)
        for _, tx in linhas:
            tx.scale(k)
        # descendente (g, p, q, y, parênteses...) corrigido: alinha pela linha de base
        desc = (Text("Ag", font=self.FONTE, font_size=36).height - Text("A", font=self.FONTE, font_size=36).height) * k
        tem_desc = set("gjpqyçÇ,;()[]")
        y = 0.0
        bases = []
        for idx, (it, tx) in enumerate(linhas):
            if idx > 0:
                y -= G.PASSO_LINHA * em_alvo
            y -= it["antes"] * em_alvo
            bases.append(y)
        # posiciona: borda esquerda comum, linha de base em bases[i]
        for (it, tx), yb in zip(linhas, bases):
            baixo = tx.get_bottom()[1]
            base_atual = baixo + (desc if any(c in tem_desc for c in it["texto"]) else 0.0)
            tx.shift(UP * (yb - base_atual))
        grupo = VGroup(*[tx for _, tx in linhas])
        for _, tx in linhas:
            tx.align_to(grupo, LEFT)
        # reajusta ao box do palco com o texto real (a fonte pode ser outra na máquina)
        bw, bh = G.BOX_ENUNCIADO
        if grupo.width > bw or grupo.height > bh:
            grupo.scale(min(bw / grupo.width, bh / grupo.height))
        cx = (G.PALCO[0] + G.PALCO[1]) / 2
        cy = (G.PALCO[2] + G.PALCO[3]) / 2
        grupo.move_to(_v((cx, cy)))
        return grupo
