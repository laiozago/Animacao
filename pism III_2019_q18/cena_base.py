# -*- coding: utf-8 -*-
"""
cena_base.py — base das animações @proflaiozago (padrão 9:16, fundo branco, três caixinhas).

  • formato 9x16 (prévia -ql = 540x960 · final -qh = 1080x1920);
  • relógio da fala: ate(t) / passo(t, *anims, dur=, nome=)  (relógio = renderer.time);
  • linha(partes, y) + aparece(parte): fórmula peça por peça (cada peça é LaTeX válido sozinha);
  • voa_copia, corte, legenda, txt (Text com tamanho em u/em), roteiro, guias (só em -ql), marca d'água;
  • enunciado integral recomposto, "digitado" palavra por palavra.

Regras que evitam armadilhas já vistas:
  - peça de MathTex some/aparece com set_opacity (nunca FadeOut/FadeIn/ReplacementTransform em FILHO de grupo);
  - figuras sem preenchimento (retângulos, linhas, setas) entram/saem com FadeIn/FadeOut/Create, nunca com set_opacity;
  - cor de "foco/contexto" em figura: set_color, nunca opacidade.
"""
from manim import *
import geometria as G


# ─── formato 9:16 ───────────────────────────────────────────────────────────
QUALIDADE = str(getattr(config, "quality", "") or "")     # lido ANTES de mexer nos pixels (no Manim, config.quality
                                                          # é derivado de largura/altura/fps e viraria None depois)


def _formato_9x16():
    config.frame_width = 9.0
    config.frame_height = 16.0
    q = QUALIDADE
    if q.startswith("low"):
        config.pixel_width, config.pixel_height = 540, 960
    elif q.startswith("medium"):
        config.pixel_width, config.pixel_height = 720, 1280
    else:
        config.pixel_width, config.pixel_height = 1080, 1920


_formato_9x16()


def _achata(xs):
    for x in xs:
        if isinstance(x, (list, tuple)):
            for y in _achata(x):
                yield y
        else:
            yield x


class CenaPadrao(Scene):
    GUIAS = "auto"          # "auto" = liga só em -ql · True/False força

    # ═══ início ═══════════════════════════════════════════════════════════
    def iniciar(self):
        self.camera.background_color = G.FUNDO
        self.fps = config.frame_rate
        self.atrasos = []
        self.eventos = []
        ref = Text("H", font=G.FONTE, font_size=100)
        self.u_fs = ref.height / G.ALTURA_CAPS / 100.0       # u por em, por unidade de font_size
        self._guias()
        self.marca = self.txt("@proflaiozago", 0.22, G.CINZA, pos=G.MARCA)
        self.add(self.marca)

    def _guias(self):
        ligado = self.GUIAS is True or (self.GUIAS == "auto" and QUALIDADE.startswith("low"))
        if not ligado:
            return
        # exatamente três molduras separadas, sem nomes: rosto (vermelha), palco/conta (azul), faixa/respostas parciais (azul)
        for zona, cor in ((G.ROSTO, G.VERMELHO), (G.PALCO, G.AZUL), (G.FAIXA, G.AZUL)):
            x0, x1, y0, y1 = zona
            r = Rectangle(width=x1 - x0, height=y1 - y0, color=cor, stroke_width=3)
            r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
            r.set_z_index(100)
            self.add(r)

    # ═══ relógio da fala ══════════════════════════════════════════════════
    def ate(self, t):
        """Espera até o instante t (relógio = quadros realmente renderizados)."""
        n = round((t - self.renderer.time) * self.fps)
        if n >= 1:
            self.wait((n + 0.25) / self.fps)

    def passo(self, t, *anims, dur=0.5, nome=""):
        """Espera até t e toca as animações juntas, todas com a mesma dur."""
        self.ate(t)
        real = self.renderer.time
        if real - t > 0.15:
            self.atrasos.append((nome, t, round(real - t, 2)))
        self.eventos.append((nome, t, round(real, 3)))
        anims = [a for a in _achata(anims) if a is not None]
        if anims:
            n = max(1, round(dur * self.fps))
            self.play(*anims, run_time=(n - 0.05) / self.fps)

    def sai(self, t, *mobs, dur=0.4, nome=""):
        """FadeOut de objetos de primeiro nível que ainda estão na cena."""
        vivos = [m for m in mobs if m in self.mobjects]
        self.passo(t, [FadeOut(m) for m in vivos], dur=dur, nome=nome or "limpa")

    def fim(self, t_fim):
        self.ate(t_fim)
        if self.atrasos:
            print("ATENCAO: passos atrasados (nome, instante pedido, atraso em s):")
            for a in self.atrasos:
                print("   ", a)
        else:
            print("Sincronia ok: nenhum passo atrasado.")

    # ═══ fórmulas e textos ════════════════════════════════════════════════
    def tex(self, s, cor=None, escala=1.0):
        return MathTex(s, color=cor or G.TEXTO).scale(escala)

    def celula(self, s, x, y, cor, esc=0.9):
        """Fórmula escondida (opacidade 0) já no lugar; revelar com aparece()."""
        m = self.tex(s, cor, esc).move_to([x, y, 0])
        m.set_opacity(0)
        self.add(m)
        return m

    def linha(self, partes, y, x=0.0, escala=0.9, cor=None, esq=None, max_larg=None):
        """Fórmula em peças, nasce invisível. m[i] = peça i (LaTeX válido sozinha)."""
        m = MathTex(*partes, color=cor or G.TEXTO).scale(escala)
        if max_larg and m.width > max_larg:
            m.scale(max_larg / m.width)
        if esq is None:
            m.move_to([x, y, 0])
        else:
            m.move_to([esq + m.width / 2, y, 0])
        m.set_opacity(0)
        self.add(m)
        return m

    def aparece(self, parte):
        return parte.animate.set_opacity(1)

    def apaga(self, parte):
        return parte.animate.set_opacity(0)

    def txt(self, s, s_em, cor, pos=None, neg=False, esq=None):
        """Text em Arial com tamanho dado em u/em (independe da escala interna do Manim)."""
        fs = s_em / self.u_fs
        t = Text(s, font=G.FONTE, font_size=fs, color=cor, weight=BOLD) if neg else Text(s, font=G.FONTE, font_size=fs, color=cor)
        if esq is not None and pos is not None:
            t.move_to([esq + t.width / 2, pos[1], 0])
        elif pos is not None:
            t.move_to([pos[0], pos[1], 0])
        return t

    def legenda(self, s, pos, cor, s_em=0.30, caixa=True):
        """Texto de regra/legenda; com caixa retorna VGroup(retângulo, texto) — entra com FadeIn."""
        t = self.txt(s, s_em, cor, pos=pos)
        if not caixa:
            return t
        r = SurroundingRectangle(t, color=cor, buff=0.13, stroke_width=3)
        return VGroup(r, t)

    def caixa(self, alvo, cor, buff=0.1):
        return SurroundingRectangle(alvo, color=cor, buff=buff, stroke_width=4)

    def corte(self, alvo, cor=None):
        """Risco de cancelamento (diagonal sobre o objeto); entra com Create."""
        return Line(alvo.get_corner(DL), alvo.get_corner(UR), color=cor or G.LARANJA, stroke_width=5)

    def voa_copia(self, t, origem, destino, dur=0.6, nome=""):
        """Uma cópia da origem viaja até o lugar do destino (escondido) e o revela."""
        self.ate(t)                      # a cópia só nasce no instante do voo (não fica duplicada nas esperas)
        nucleo = lambda m: m[0] if (isinstance(m, MathTex) and len(m) == 1) else m   # mesma profundidade nos dois lados
        cp = nucleo(origem).copy()
        alvo = nucleo(destino).copy()
        alvo.set_opacity(1)
        self.add(cp)
        self.passo(t, Transform(cp, alvo), dur=dur, nome=nome or "voa")
        destino.set_opacity(1)
        self.remove(cp)

    # ═══ roteiro (faixa ao lado do rosto) ═════════════════════════════════
    def monta_roteiro(self):
        self.rot = []
        for i, (pend, ok) in enumerate(zip(G.F["rot_pend"], G.F["rot_ok"])):
            y = G.ROT_Y[i]
            par = []
            for s, cor in ((pend, G.VERMELHO), (ok, G.VERDE)):
                m = MathTex(s, color=cor).scale(G.ROT_ESCALA)
                if m.width > G.ROT_LARG:
                    m.scale(G.ROT_LARG / m.width)
                m.move_to([G.X_ROT + m.width / 2, y, 0])
                m.set_opacity(0)
                self.add(m)
                par.append(m)
            self.rot.append(par)

    def rot_entra(self, i):
        return self.rot[i][0].animate.set_opacity(1)

    def rot_resolve(self, i):
        return [self.rot[i][0].animate.set_opacity(0), self.rot[i][1].animate.set_opacity(1)]

    def pulso_marca(self):
        return Indicate(self.marca, color=G.LARANJA, scale_factor=1.2)

    # ═══ enunciado integral recomposto ════════════════════════════════════
    def monta_enunciado(self, yc=None):
        """Texto integral da prova, na maior fonte que couber em BOX_ENUNCIADO; medido com o Text real."""
        c = G.melhor_composicao()
        box_w, box_h = G.BOX_ENUNCIADO
        if yc is None:
            yc = (G.PALCO[2] + G.PALCO[3]) / 2
        s = c["s"]
        fs = s / self.u_fs
        ref_g = Text("Ag", font=G.FONTE, font_size=fs)
        ref_a = Text("A", font=G.FONTE, font_size=fs)
        desc = ref_g.height - ref_a.height                       # profundidade do descendente
        textos = []
        for ln in c["linhas"]:
            if ln["neg"]:
                t = Text(ln["texto"], font=G.FONTE, font_size=fs, color=G.TEXTO, weight=BOLD)
            else:
                t = Text(ln["texto"], font=G.FONTE, font_size=fs, color=G.TEXTO)
            textos.append(t)
        W = max(t.width for t in textos)
        y0 = yc + c["altura"] / 2 - G.ALTURA_CAPS * s            # linha de base da 1ª linha
        for t, ln in zip(textos, c["linhas"]):
            tem_desc = any(ch in "gjpqy(),;ç" for ch in ln["texto"])
            base = y0 - ln["base"]
            t.align_to(LEFT * (W / 2), LEFT)
            t.shift(UP * ((base - (desc if tem_desc else 0.0)) - t.get_bottom()[1]))
        grupo = VGroup(*textos)
        if grupo.width > box_w or grupo.height > box_h:          # se a fonte real for maior que a da tabela, reajusta
            grupo.scale(min(box_w / grupo.width, box_h / grupo.height))
        grupo.move_to([0, yc, 0])
        covers, bordas = [], []
        for t, ln in zip(textos, c["linhas"]):
            cv = Rectangle(width=t.width + 0.5, height=t.height + 0.4, stroke_width=0, fill_color=G.FUNDO, fill_opacity=1)
            cv.move_to(t.get_center())
            cv.set_z_index(10)
            covers.append(cv)
            esq, larg = t.get_left()[0], t.width
            b = []
            for k in range(len(ln["palavras"])):
                if k == len(ln["palavras"]) - 1:
                    b.append(t.get_right()[0] + 0.3)
                else:
                    b.append(esq + (ln["cum_fim"][k] + ln["gap"] / 2) / ln["larg_em"] * larg)
            bordas.append(b)
        return dict(grupo=grupo, textos=textos, linhas=c["linhas"], covers=covers, bordas=bordas, s=s)

    def _destapa(self, cv, x_corte):
        """Move a borda esquerda da cobertura para x_corte (a direita fica parada)."""
        dir_x = cv.get_right()[0]
        larg = max(dir_x - x_corte, 1e-3)
        cv.stretch_to_fit_width(larg)
        cv.move_to([dir_x - larg / 2, cv.get_center()[1], 0])

    def digita(self, enun, t0, t1):
        """Revela o enunciado palavra por palavra entre t0 e t1 (coberturas brancas que recuam)."""
        ordem = [(i, k) for i, ln in enumerate(enun["linhas"]) for k in range(len(ln["palavras"]))]
        n = len(ordem)
        for j, (i, k) in enumerate(ordem):
            self.ate(t0 + (t1 - t0) * j / n)
            self._destapa(enun["covers"][i], enun["bordas"][i][k])
        self.ate(t1)
        for cv in enun["covers"]:
            self.remove(cv)
