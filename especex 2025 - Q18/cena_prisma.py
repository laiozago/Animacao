"""Volume do prisma hexagonal regular  |  @proflaiozago

Versão VERTICAL (9:16) para sobrepor à folha da questão / ficar por baixo do
recorte do professor. A geometria (vértices, arestas, câmera, paleta) vem de
geometria.py; aqui só decidimos o que desenhar e quando.

    python3 geometria.py                          # testa a geometria (sem Manim)
    manim -pql cena_prisma.py PrismaHexagonal     # prévia 540x960
    manim -pqh cena_prisma.py PrismaHexagonal     # final 1080x1920

Layout (quadro 9 x 16 unidades):
    y  +7.6 .. +1.0   figura (prisma) à esquerda, roteiro à direita
    y  +0.7 .. -2.6   contas
    y  < -2.7         zona livre para o rosto (embaixo, à esquerda)
    marca d'água      canto inferior direito

Código de cores (o mesmo da geometria.py):
    AZUL     x       = D'M  (projeção de DM na base)
    AMARELO  x*sqrt3 = DD'  (altura)
    VERMELHO 2x      = DM   (diagonal)   e também "falta descobrir"
    VERDE    "já resolvido"
    LARANJA  plano da base / ângulo de 60°
"""
import numpy as np
from manim import *
from pathlib import Path

config.media_dir = str(Path(__file__).resolve().parent / "media")

from geometria import (
    H, LADO, K_D, K_M,
    FUNDO, AZUL, AMARELO, VERMELHO, VERDE, LARANJA, CINZA, PALETA6,
    mistura, vertice, projeta, ARESTAS, aresta_visivel,
)

# ---- formato do vídeo: 9:16 -------------------------------------------------
# -ql / -qm  -> prévia 540x960   |   -qh / -qp  -> final 1080x1920
PREVIA = getattr(config, "quality", None) in ("low_quality", "medium_quality",
                                              "example_quality")
config.frame_width, config.frame_height = 9.0, 16.0
config.pixel_width, config.pixel_height = (540, 960) if PREVIA else (1080, 1920)

# ---- enunciado (já aparece na folha; deixe False se o vídeo mostra a questão) --
MOSTRAR_ENUNCIADO = False
ENUNCIADO = [
    "Num prisma hexagonal regular de altura 12 cm,",
    "a diagonal DM liga vértices opostos das duas bases",
    "e forma 60° com o plano da base.",
    "Qual é o volume do prisma?",
]
DESTAQUES = {"12 cm": AMARELO, "DM": VERMELHO, "plano da base": LARANJA}

# ---- câmera e layout --------------------------------------------------------
ESCALA = 0.43                        # cm da figura -> unidades do Manim
OX, OY = -1.5, 4.2                    # centro do prisma na tela
YAW0, ELEV0 = 0.0, np.radians(22.0)    # vista inicial (perspectiva "de revista")
YAW_FRENTE, ELEV_FRENTE = np.radians(60.0), 0.0    # D'M horizontal, DD' vertical
YAW_CIMA, ELEV_CIMA = np.radians(60.0), np.pi / 2  # hexágono visto de cima
YAW_FINAL, ELEV_FINAL = np.radians(25.0), np.radians(22.0)

X_PAINEL, Y_TOPO_PAINEL, LARG_PAINEL = -4.2, 0.7, 8.4     # contas (largura total)
X_ROTEIRO, Y_TOPO_ROTEIRO, LARG_ROTEIRO = 0.95, 7.45, 3.3  # roteiro (à direita da figura)
ESC_ROTEIRO = 0.75

PASSO_TRACEJADO = 0.8      # cm de aresta por traço (a mesma "cadência" em todas)
ESP_ARESTA, ESP_DESTAQUE = 4, 6    # espessuras de linha
COR_ARESTA = CINZA


class PrismaHexagonal(Scene):
    """Calcula o volume do prisma a partir do ângulo que DM faz com a base."""

    def construct(self):
        self.camera.background_color = FUNDO
        # "câmera" virtual: giro do prisma (yaw) e elevação (elev)
        self.yaw = ValueTracker(YAW0)
        self.elev = ValueTracker(ELEV0)
        self.add(self.yaw, self.elev)

        self.abertura()
        self.prisma_aparece()
        self.marca_pontos()
        self.vista_de_frente()
        self.resolve_triangulo()
        self.vista_de_cima()
        self.acha_lado()
        self.area_da_base()
        self.volume()

    # ------------------------------------------------------------------
    # auxiliares: pontos de tela, câmera, painel de contas
    # ------------------------------------------------------------------
    def P(self, k, z=0.0):
        """Vértice k, na altura z, na tela (com a câmera neste instante)."""
        return projeta(vertice(k, z), self.yaw.get_value(),
                       self.elev.get_value(), ESCALA, OX, OY)

    def centro(self, z=0.0):
        return projeta(np.array([0.0, 0.0, z]), self.yaw.get_value(),
                       self.elev.get_value(), ESCALA, OX, OY)

    def pD(self):
        return self.P(K_D, H)        # D: vértice de cima

    def pDp(self):
        return self.P(K_D, 0.0)      # D': pé da perpendicular de D na base

    def pM(self):
        return self.P(K_M, 0.0)      # M: vértice de baixo (oposto a D')

    def gira_camera(self, yaw, elev, tempo=3.0):
        self.play(self.yaw.animate.set_value(yaw),
                  self.elev.animate.set_value(elev), run_time=tempo)

    @staticmethod
    def ajusta(mob, largura=LARG_PAINEL):
        """Reduz o objeto se passar da largura disponível."""
        if mob.width > largura:
            mob.scale_to_fit_width(largura)
        return mob

    def texto(self, s, tam=28, cor=CINZA):
        return Text(s, font_size=tam, color=cor)

    def tex(self, *partes, cor=CINZA):
        """MathTex já com a cor de texto do tema (o padrão do Manim é branco)."""
        return MathTex(*partes, color=cor)

    def rotulo(self, tex, cor=CINZA, escala=0.95):
        """Rótulo de figura: contorno da cor do fundo para ler sobre as arestas."""
        m = self.tex(tex, cor=cor).scale(escala)
        m.set_stroke(FUNDO, 6, background=True)
        return m

    def monta_painel(self, *itens):
        """Empilha as linhas na faixa das contas, sempre alinhadas pelo topo."""
        grupo = VGroup(*itens).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.ajusta(grupo)
        grupo.align_to(X_PAINEL * RIGHT, LEFT).align_to(Y_TOPO_PAINEL * UP, UP)
        return grupo

    def revela(self, painel, pausa=1.2):
        """Título do painel e, depois, uma linha de cada vez."""
        self.play(FadeIn(painel[0], shift=RIGHT * 0.2))
        for linha in painel[1:]:
            self.play(Write(linha))
            self.wait(pausa)

    def resolve_item(self, i, tex):
        """Troca '? vermelho' do roteiro pelo valor encontrado, em verde."""
        antigo = self.roteiro[i]
        novo = self.tex(tex, cor=VERDE).scale(ESC_ROTEIRO).move_to(antigo, aligned_edge=LEFT)
        self.play(ReplacementTransform(antigo, novo))
        self.roteiro[i] = novo

    # ------------------------------------------------------------------
    # figura: o prisma como "fio de arame" (arestas ocultas tracejadas)
    # ------------------------------------------------------------------
    def aresta(self, a, b, oculta, n):
        """Aresta em n pedaços: contínua se visível, tracejada se oculta.

        O nº de pedaços não muda com a câmera -> o always_redraw (become)
        sempre compara estruturas iguais.
        """
        if np.linalg.norm(b - a) < 1e-6:          # aresta vista "de ponta"
            b = b + np.array([1e-4, 0.0, 0.0])
        pedacos = VGroup()
        for i in range(n):
            t0 = i / n
            t1 = (i + 0.5) / n if oculta else (i + 1) / n
            pedacos.add(Line(a + (b - a) * t0, a + (b - a) * t1,
                             color=COR_ARESTA, stroke_width=ESP_ARESTA,
                             stroke_opacity=0.55 if oculta else 1.0))
        return pedacos

    def wireframe(self):
        yaw, elev = self.yaw.get_value(), self.elev.get_value()
        arestas = VGroup()
        for p, q, faces in ARESTAS:
            a = projeta(p, yaw, elev, ESCALA, OX, OY)
            b = projeta(q, yaw, elev, ESCALA, OX, OY)
            n = max(2, int(round(np.linalg.norm(q - p) / PASSO_TRACEJADO)))
            arestas.add(self.aresta(a, b, not aresta_visivel(faces, yaw, elev), n))
        return arestas

    # ------------------------------------------------------------------
    # cenas
    # ------------------------------------------------------------------
    def abertura(self):
        """Marca do canal (e o enunciado, se pedido). Sem título."""
        marca = Text("@proflaiozago", font_size=26,
                     color=mistura(FUNDO, CINZA, 0.55)).to_corner(DR, buff=0.3)
        self.add(marca)
        if not MOSTRAR_ENUNCIADO:
            self.wait(0.5)
            return

        linhas = VGroup(*[Text(t, font_size=30, color=CINZA, t2c=DESTAQUES)
                          for t in ENUNCIADO])
        linhas.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.ajusta(linhas, LARG_PAINEL)
        linhas.move_to(UP * 3)
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in linhas],
                              lag_ratio=0.5), run_time=3)
        self.wait(2.5)
        self.play(FadeOut(linhas))

    def prisma_aparece(self):
        """Roteiro (verde = dado/resolvido, vermelho = falta) e o prisma."""
        itens = [
            self.tex(r"h = 12\ \text{cm}", cor=VERDE),
            self.tex(r"a = \,?", cor=VERMELHO),
            self.tex(r"A_b = \,?", cor=VERMELHO),
            self.tex(r"V = \,?", cor=VERMELHO),
        ]
        self.roteiro = VGroup(*itens).scale(ESC_ROTEIRO)
        self.roteiro.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.ajusta(self.roteiro, LARG_ROTEIRO)
        self.roteiro.align_to(X_ROTEIRO * RIGHT, LEFT).align_to(Y_TOPO_ROTEIRO * UP, UP)
        self.play(FadeIn(self.roteiro, shift=LEFT * 0.3), run_time=0.8)

        # entra "desenhando"; depois troca pela versão que acompanha a câmera
        estatico = self.wireframe()
        self.play(Create(estatico, lag_ratio=0.03), run_time=3)
        self.remove(estatico)
        self.wire = always_redraw(self.wireframe)
        self.add(self.wire)
        self.wait(0.5)

    def marca_pontos(self):
        """Pontos D, D', M e os segmentos DM, DD' e D'M."""
        def segue(mob, ponto, direcao, buff=0.12):
            mob.add_updater(lambda m: m.next_to(ponto(), direcao, buff=buff),
                            call_updater=True)
            return mob

        def pino(ponto):
            d = Dot(ponto(), radius=0.08, color=CINZA)
            d.add_updater(lambda m: m.move_to(ponto()))
            return d

        def segmento(f1, f2, cor):
            lin = Line(f1(), f2(), color=cor, stroke_width=ESP_DESTAQUE)
            lin.add_updater(lambda m: m.put_start_and_end_on(f1(), f2()))
            return lin

        self.pino_D, self.pino_Dp, self.pino_M = pino(self.pD), pino(self.pDp), pino(self.pM)
        self.rot_D = segue(self.rotulo("D"), self.pD, UP)
        self.rot_Dp = segue(self.rotulo("D'"), self.pDp, DL)
        self.rot_M = segue(self.rotulo("M"), self.pM, DR)
        self.dm = segmento(self.pD, self.pM, VERMELHO)
        self.dpm = segmento(self.pDp, self.pM, AZUL)
        self.ddp = segmento(self.pD, self.pDp, AMARELO)

        # triângulo DD'M levemente preenchido (acompanha a câmera)
        self.tri = Polygon(self.pDp(), self.pM(), self.pD(),
                           color=AZUL, fill_opacity=0.14, stroke_width=0)
        self.tri.add_updater(lambda m: m.set_points_as_corners(
            [self.pDp(), self.pM(), self.pD(), self.pDp()]))

        self.play(FadeIn(VGroup(self.pino_D, self.pino_Dp, self.pino_M)),
                  FadeIn(VGroup(self.rot_D, self.rot_Dp, self.rot_M)))

        legendas = VGroup(
            self.texto("DM = diagonal do prisma", cor=VERMELHO),
            self.texto("DD' = altura  (D' é o pé de D na base)", cor=AMARELO),
            self.texto("D'M = projeção de DM na base", cor=AZUL),
        )
        legendas.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.ajusta(legendas)
        legendas.align_to(X_PAINEL * RIGHT, LEFT).align_to(Y_TOPO_PAINEL * UP, UP)

        # (linha, legenda) na ordem em que são explicados
        for linha, legenda in ((self.dm, legendas[0]), (self.ddp, legendas[1]),
                               (self.dpm, legendas[2])):
            self.play(FadeIn(linha), FadeIn(legenda, shift=RIGHT * 0.2))
            self.wait(0.9)
        self.play(FadeIn(self.tri))
        self.wait(1.2)
        self.play(FadeOut(legendas))

    def vista_de_frente(self):
        """Gira até D'M ficar horizontal e DD' vertical: triângulo retângulo."""
        self.gira_camera(YAW_FRENTE, ELEV_FRENTE, tempo=3.5)

        Dp, M, D = self.pDp(), self.pM(), self.pD()
        # ângulo reto em D'
        s = 0.32
        reto = VMobject(color=CINZA).set_points_as_corners(
            [Dp + s * RIGHT, Dp + s * (RIGHT + UP), Dp + s * UP])
        reto.set_stroke(width=3)
        # ângulo de 60° em M (entre MD e MD')
        a1 = np.arctan2(D[1] - M[1], D[0] - M[0])
        a2 = np.arctan2(Dp[1] - M[1], Dp[0] - M[0])
        arco = Arc(radius=0.85, start_angle=a1, angle=(a2 - a1) % TAU,
                   arc_center=M, color=LARANJA, stroke_width=5)
        meio = a1 + ((a2 - a1) % TAU) / 2
        ang = self.rotulo(r"60^\circ", cor=LARANJA)
        ang.move_to(M + 1.3 * np.array([np.cos(meio), np.sin(meio), 0.0]))

        # lados do triângulo: x, x*sqrt(3) e 2x
        self.l_x = self.rotulo("x", AZUL).next_to((Dp + M) / 2, DOWN, buff=0.18)
        self.l_xr3 = self.rotulo(r"x\sqrt{3}", AMARELO).next_to((D + Dp) / 2, LEFT, buff=0.18)
        self.l_2x = self.rotulo("2x", VERMELHO).next_to((D + M) / 2, UR, buff=0.1)

        self.marcas_frente = VGroup(reto, arco, ang)
        self.play(FadeIn(reto), Create(arco), Write(ang))
        self.wait(0.6)
        self.play(LaggedStart(Write(self.l_x), Write(self.l_xr3), Write(self.l_2x),
                              lag_ratio=0.5), run_time=2)
        self.wait(0.8)

    def resolve_triangulo(self):
        """Triângulo 30-60-90: lados proporcionais a x, x*sqrt(3) e 2x."""
        cab = self.texto("Triângulo retângulo DD'M  (30°, 60°, 90°)", tam=30)
        e1 = self.tex(r"D'M = ", r"x", r",\ \ DD' = ", r"x\sqrt{3}", r",\ \ DM = ", r"2x")
        e1[1].set_color(AZUL)
        e1[3].set_color(AMARELO)
        e1[5].set_color(VERMELHO)
        e2 = self.tex(r"DD' = h \;\Rightarrow\; ", r"x\sqrt{3}", r" = 12")
        e2[1].set_color(AMARELO)
        e3 = self.tex(r"x", r" = \dfrac{12}{\sqrt{3}} = \dfrac{12\sqrt{3}}{3} = ",
                      r"4\sqrt{3}\ \text{cm}")
        e3[0].set_color(AZUL)
        e3[2].set_color(AZUL)
        for e in (e1, e2, e3):
            e.scale(0.9)
        self.painel_a = self.monta_painel(cab, e1, e2, e3)

        self.play(FadeIn(self.painel_a[0], shift=RIGHT * 0.2))
        self.play(Write(self.painel_a[1]))
        self.wait(1.2)
        # DD' é a altura: na figura, x*sqrt(3) vira 12
        self.play(Write(self.painel_a[2]))
        n12 = self.rotulo("12", AMARELO).move_to(self.l_xr3, aligned_edge=RIGHT)
        self.play(ReplacementTransform(self.l_xr3, n12))
        self.l_xr3 = n12
        self.wait(1.0)
        # x = 4*sqrt(3), então DM = 2x = 8*sqrt(3)
        self.play(Write(self.painel_a[3]))
        nx = self.rotulo(r"4\sqrt{3}", AZUL).move_to(self.l_x)
        n2x = self.rotulo(r"8\sqrt{3}", VERMELHO).move_to(self.l_2x, aligned_edge=DL)
        self.play(ReplacementTransform(self.l_x, nx), ReplacementTransform(self.l_2x, n2x))
        self.l_x, self.l_2x = nx, n2x
        self.wait(2)

    def vista_de_cima(self):
        """Só D'M interessa agora: ela é a diagonal maior do hexágono."""
        saem = [self.painel_a, self.marcas_frente, self.l_x, self.l_xr3, self.l_2x,
                self.dm, self.ddp, self.tri, self.pino_D, self.rot_D]
        self.play(*[FadeOut(m) for m in saem])
        self.gira_camera(YAW_CIMA, ELEV_CIMA, tempo=3.5)

        c = self.centro()
        Dp, M = self.pDp(), self.pM()
        # raios do centro aos 6 vértices: 6 triângulos equiláteros de lado a
        self.raios = VGroup(*[Line(c, self.P(k), color=mistura(FUNDO, CINZA, 0.6),
                                   stroke_width=2) for k in range(6)])
        self.play(Create(self.raios, lag_ratio=0.15), run_time=1.5)

        la1 = self.rotulo("a", VERDE).next_to((c + Dp) / 2, UP, buff=0.08)
        la2 = self.rotulo("a", VERDE).next_to((c + M) / 2, UP, buff=0.08)
        # chave logo abaixo do hexágono (meia altura = lado * sen60° * escala)
        folga = np.sqrt(3) / 2 * ESCALA * LADO + 0.3
        chave = BraceBetweenPoints(Dp + DOWN * folga, M + DOWN * folga,
                                   direction=DOWN, color=AZUL)
        l2a = self.rotulo("2a", AZUL).next_to(chave, DOWN, buff=0.1)
        self.cima = VGroup(la1, la2, chave, l2a)
        self.play(Write(la1), Write(la2))
        self.play(GrowFromCenter(chave), Write(l2a))
        self.wait(1)

    def acha_lado(self):
        """D'M = 2a = 4*sqrt(3)  ->  a = 2*sqrt(3)."""
        cab = self.texto("D'M é a diagonal maior do hexágono:", tam=30)
        e1 = self.tex(r"D'M = ", r"2a")
        e1[0].set_color(AZUL)
        e1[1].set_color(AZUL)
        e2 = self.tex(r"2a = x = 4\sqrt{3}")
        e3 = self.tex(r"a = ", r"2\sqrt{3}\ \text{cm}")
        e3[1].set_color(VERDE)
        for e in (e1, e2, e3):
            e.scale(0.95)
        painel = self.monta_painel(cab, e1, e2, e3)
        self.revela(painel)
        self.resolve_item(1, r"a = 2\sqrt{3}\ \text{cm}")
        self.wait(1)
        self.painel_b = painel

    def area_da_base(self):
        """Hexágono = 6 triângulos equiláteros de lado a."""
        self.play(FadeOut(self.painel_b))
        c = self.centro()
        self.fatias = VGroup(*[
            Polygon(c, self.P(k), self.P((k + 1) % 6), color=PALETA6[k],
                    fill_opacity=0.35, stroke_width=0)
            for k in range(6)])
        self.play(LaggedStart(*[FadeIn(f) for f in self.fatias], lag_ratio=0.2),
                  run_time=2)

        cab = self.texto("6 triângulos equiláteros de lado a:", tam=30)
        e1 = self.tex(r"A_b = 6\cdot\dfrac{a^2\sqrt{3}}{4}")
        e2 = self.tex(r"a^2 = (2\sqrt{3})^2 = 12")
        e3 = self.tex(r"A_b = 6\cdot\dfrac{12\sqrt{3}}{4} = ", r"18\sqrt{3}\ \text{cm}^2")
        e3[1].set_color(VERDE)
        for e in (e1, e2, e3):
            e.scale(0.85)
        painel = self.monta_painel(cab, e1, e2, e3)
        self.revela(painel)
        self.resolve_item(2, r"A_b = 18\sqrt{3}\ \text{cm}^2")
        self.wait(1)
        self.painel_c = painel

    def volume(self):
        """Volta para a perspectiva 3D e fecha com V = A_b * h."""
        self.play(FadeOut(self.painel_c), FadeOut(self.fatias), FadeOut(self.raios),
                  FadeOut(self.cima))
        self.gira_camera(YAW_FINAL, ELEV_FINAL, tempo=3)

        cab = self.texto("Volume do prisma:", tam=30)
        e1 = self.tex(r"V = A_b \cdot h")
        e2 = self.tex(r"V = 18\sqrt{3}\cdot 12")
        e3 = self.tex(r"V = ", r"216\sqrt{3}\ \text{cm}^3")
        e3[1].set_color(VERDE)
        for e in (e1, e2, e3):
            e.scale(1.0)
        painel = self.monta_painel(cab, e1, e2, e3)
        self.revela(painel)
        self.resolve_item(3, r"V = 216\sqrt{3}\ \text{cm}^3")
        caixa = SurroundingRectangle(painel[3], color=VERDE, buff=0.18)
        self.play(Create(caixa))
        self.wait(3)
