# -*- coding: utf-8 -*-
"""
geometria.py — EsPCEx 2025, Questão 19 (geometria analítica) — @proflaiozago

SEM Manim. Aqui ficam: dados da questão, tema/cores, zonas do quadro 9x16
(layout novo: rosto no meio-esquerda), mapeamento plano -> tela, posição dos
rótulos da figura e os TESTES.

    python3 geometria.py      # roda todos os testes
"""
from collections import namedtuple
from fractions import Fraction as Fr
import math

INF = 1e9

# ═══════════════════════════════════════════════════════════════════════════
# 1. DADOS DA QUESTÃO
# ═══════════════════════════════════════════════════════════════════════════
A = (Fr(-2), Fr(1))
B = (Fr(4), Fr(7))
ALTERNATIVAS = [("A", 2), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]
LETRA_CORRETA = "C"


def ponto_medio(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def coef_angular(p, q):
    return (q[1] - p[1]) / (q[0] - p[0])


M = ponto_medio(A, B)                 # (1, 4)
M_AB = coef_angular(A, B)             # 1
RETA_M = -1 / M_AB                    # -1  (perpendicular: inverso do oposto)
RETA_N = M[1] - RETA_M * M[0]         # 5
SOMA = RETA_M + RETA_N                # 4


def candidatos_C():
    """Os dois vértices do ângulo reto possíveis: M mais/menos a meia-hipotenusa girada 90°."""
    dx, dy = (B[0] - A[0]) / 2, (B[1] - A[1]) / 2
    return [(M[0] - dy, M[1] + dx), (M[0] + dy, M[1] - dx)]


C = [c for c in candidatos_C() if c[0] > 0][0]     # abscissa positiva -> (4, 1)

# ═══════════════════════════════════════════════════════════════════════════
# 2. TEMA (claro = padrão)
# ═══════════════════════════════════════════════════════════════════════════
TEMA = "claro"          # "claro" (padrão) ou "escuro"
TEMAS = {
    "claro": dict(FUNDO="#FFFFFF", TEXTO="#1B1B1B", GRADE="#E6E9ED", EIXO="#6B7280",
                  CINZA="#6B7280", AZUL="#1E63C9", AMARELO="#B97A00",
                  VERMELHO="#D32F2F", VERDE="#1B8A3A", LARANJA="#E65100"),
    "escuro": dict(FUNDO="#0E1116", TEXTO="#F2F2F2", GRADE="#262B33", EIXO="#9AA3AE",
                   CINZA="#9AA3AE", AZUL="#64B5F6", AMARELO="#FFD54F",
                   VERMELHO="#FF6B6B", VERDE="#5BD68A", LARANJA="#FFA040"),
}
_T = TEMAS[TEMA]
FUNDO, TEXTO, GRADE, EIXO, CINZA = _T["FUNDO"], _T["TEXTO"], _T["GRADE"], _T["EIXO"], _T["CINZA"]
# Significado fixo (padrão @proflaiozago):
AZUL = _T["AZUL"]          # lado menor / projeção (aqui: Δx e Δy do coef. angular)
AMARELO = _T["AMARELO"]    # altura (aqui: a reta CM = altura = mediatriz)
VERMELHO = _T["VERMELHO"]  # hipotenusa (AB) e "falta descobrir"
VERDE = _T["VERDE"]        # "já resolvido"
LARANJA = _T["LARANJA"]    # ângulos (o 90°)

# ═══════════════════════════════════════════════════════════════════════════
# 3. ZONAS DO QUADRO 9 x 16 (unidades Manim; x para a direita, y para cima)
#    Medidas a partir do print do CapCut: rosto = quadrado no meio-esquerda.
# ═══════════════════════════════════════════════════════════════════════════
Caixa = namedtuple("Caixa", "x0 x1 y0 y1")


def _cx(c): return (c.x0 + c.x1) / 2
def _cy(c): return (c.y0 + c.y1) / 2
def _larg(c): return c.x1 - c.x0
def _alt(c): return c.y1 - c.y0


def cruza(a, b, folga=0.0):
    """True se as caixas se sobrepõem (folga > 0 exige distância mínima)."""
    return not (a.x1 + folga <= b.x0 or b.x1 + folga <= a.x0 or
                a.y1 + folga <= b.y0 or b.y1 + folga <= a.y0)


def contem(grande, pequena, tol=1e-6):
    return (pequena.x0 >= grande.x0 - tol and pequena.x1 <= grande.x1 + tol and
            pequena.y0 >= grande.y0 - tol and pequena.y1 <= grande.y1 + tol)


QUADRO = Caixa(-4.5, 4.5, -8.0, 8.0)
PALCO = Caixa(-4.1, 4.1, 0.4, 5.7)        # parte branca de cima: a resolução acontece AQUI
ROSTO = Caixa(-4.1, 0.6, -4.6, 0.1)       # quadrado do rosto (livre, sem animação)
FAIXA = Caixa(0.8, 2.8, -4.6, 0.1)        # branco ao lado do rosto: roteiro + marca d'água
EVITAR = [Caixa(2.9, 4.5, -8.0, 0.1),     # botões do TikTok/Instagram (coluna direita)
          Caixa(-4.5, 4.5, -8.0, -4.7)]   # legenda/@/música embaixo

# Plano cartesiano dentro do palco (escala igual nos dois eixos: 1 unidade = 0,6)
ESCALA = 0.6
DOM_X = (-3.0, 5.0)
DOM_Y = (-0.5, 8.0)
PLANO = Caixa(-4.1, -4.1 + ESCALA * (DOM_X[1] - DOM_X[0]),
              0.5, 0.5 + ESCALA * (DOM_Y[1] - DOM_Y[0]))          # (-4.1, 0.7, 0.5, 5.6)

COLUNA = Caixa(0.95, 4.05, 0.4, 5.5)      # coluna das contas (à direita do plano)
COL_ESCALA = 0.8                          # escala das fórmulas da coluna
COL_BUFF = 0.14                           # espaço entre peças de uma mesma linha (x escala)

ROTEIRO_X = 0.95                          # borda esquerda dos itens do roteiro
ROTEIRO_Y = [-0.5, -1.45, -2.4, -3.35]    # um item por vez, de cima para baixo
ROTEIRO_ESCALA = 0.75
MARCA_CENTRO = (1.85, -4.4)               # marca d'água na base da faixa
MARCA_LARG_MAX = 1.8


def para_tela(x, y):
    """Ponto do plano cartesiano (x, y) -> posição (X, Y) no quadro do Manim."""
    return (PLANO.x0 + ESCALA * (float(x) - DOM_X[0]),
            PLANO.y0 + ESCALA * (float(y) - DOM_Y[0]))


def reta_visivel(m, n, margem=0.3):
    """Pontas (no plano) do trecho da reta y = mx + n que cabe no domínio mostrado."""
    m, n = float(m), float(n)
    x0, x1 = DOM_X[0] + margem, DOM_X[1] - margem
    y0, y1 = DOM_Y[0] + margem, DOM_Y[1] - margem
    if m != 0:
        a, b = (y0 - n) / m, (y1 - n) / m
        x0, x1 = max(x0, min(a, b)), min(x1, max(a, b))
    return (x0, m * x0 + n), (x1, m * x1 + n)


# ═══════════════════════════════════════════════════════════════════════════
# 4. RÓTULOS DA FIGURA (a cena lê estas posições; os testes conferem colisões)
#    Larguras/alturas medidas compilando o LaTeX (unidades Manim, escala 1).
# ═══════════════════════════════════════════════════════════════════════════
TAM_TEX = {   # tex: (largura, altura) com escala 1
    r"A(-2,1)": (1.875, 0.5), r"B(4,7)": (1.515, 0.5), r"M(1,4)": (1.651, 0.5),
    r"M": (0.54, 0.342), r"C": (0.393, 0.342), r"y=mx+n": (2.566, 0.389),
    r"y=-x+n": (2.516, 0.389), r"y=-x+5": (2.466, 0.419), r"n=5": (1.217, 0.322),
    r"90^\circ": (0.73, 0.369), r"6": (0.25, 0.322), r"-2": (0.639, 0.364),
    r"2": (0.25, 0.322), r"4": (0.25, 0.322), r"x": (0.286, 0.215), r"y": (0.27, 0.3),
}


def _d(p, dx=0.0, dy=0.0):
    X, Y = para_tela(*p)
    return (X + dx, Y + dy)


# modo "C": pos = centro do rótulo; modo "L": pos = meio da borda esquerda
ROTULOS = {
    "A":      dict(tex=r"A(-2,1)", esc=0.55, pos=_d(A, 0, -0.35), modo="C", janela=(7.0, INF)),
    "B":      dict(tex=r"B(4,7)",  esc=0.55, pos=_d(B, 0, 0.32),  modo="C", janela=(7.6, INF)),
    "C":      dict(tex=r"C",       esc=0.55, pos=_d(C, 0.26, 0.24),  modo="C", janela=(10.4, 61.7)),
    "M0":     dict(tex=r"M",       esc=0.55, pos=_d(M, 0.24, 0),  modo="L", janela=(19.0, 37.1)),
    "M1":     dict(tex=r"M(1,4)",  esc=0.55, pos=_d(M, 0.24, 0),  modo="L", janela=(37.1, INF)),
    "reta0":  dict(tex=r"y=mx+n",  esc=0.55, pos=(-1.5, 4.75),    modo="C", janela=(12.2, 90.4)),
    "reta1":  dict(tex=r"y=-x+n",  esc=0.55, pos=(-1.5, 4.75),    modo="C", janela=(90.4, 99.87)),
    "reta2":  dict(tex=r"y=-x+5",  esc=0.55, pos=(-1.5, 4.75),    modo="C", janela=(99.87, INF)),
    "n":      dict(tex=r"n=5",     esc=0.55, pos=(-2.95, 3.62),   modo="C", janela=(99.87, INF)),
    "ang":    dict(tex=r"90^\circ", esc=0.5, pos=_d(M, 0, 0.58),  modo="C", janela=(56.7, INF)),
    "seis_v": dict(tex=r"6",       esc=0.6,  pos=_d((4, 4), 0.26, 0), modo="C", janela=(70.3, 78.3)),
    "seis_h": dict(tex=r"6",       esc=0.6,  pos=_d((1, 1), 0, -0.28), modo="C", janela=(73.8, 78.3)),
    # numerais e nomes dos eixos (sempre visíveis depois que o plano entra)
    "nx-2":   dict(tex=r"-2", esc=0.42, pos=_d((-2, 0), 0, -0.2), modo="C", janela=(6.3, INF)),
    "nx2":    dict(tex=r"2",  esc=0.42, pos=_d((2, 0), 0, -0.2),  modo="C", janela=(6.3, INF)),
    "nx4":    dict(tex=r"4",  esc=0.42, pos=_d((4, 0), 0, -0.2),  modo="C", janela=(6.3, INF)),
    "ny2":    dict(tex=r"2",  esc=0.42, pos=_d((0, 2), -0.2, 0),  modo="C", janela=(6.3, INF)),
    "ny4":    dict(tex=r"4",  esc=0.42, pos=_d((0, 4), -0.2, 0),  modo="C", janela=(6.3, INF)),
    "ny6":    dict(tex=r"6",  esc=0.42, pos=_d((0, 6), -0.2, 0),  modo="C", janela=(6.3, INF)),
    "eixo_x": dict(tex=r"x",  esc=0.5,  pos=_d((4.8, 0), 0, -0.22), modo="C", janela=(6.3, INF)),
    "eixo_y": dict(tex=r"y",  esc=0.5,  pos=_d((0, 7.7), 0.22, 0),  modo="C", janela=(6.3, INF)),
}


def caixa_rotulo(r, margem=0.04):
    w, h = TAM_TEX[r["tex"]]
    w, h = w * r["esc"] + 2 * margem, h * r["esc"] + 2 * margem
    x, y = r["pos"]
    if r["modo"] == "L":
        return Caixa(x, x + w, y - h / 2, y + h / 2)
    return Caixa(x - w / 2, x + w / 2, y - h / 2, y + h / 2)


# Segmentos da figura (em coordenadas do plano) e quando existem
_R0, _R1 = reta_visivel(RETA_M, RETA_N)
SEGMENTOS = {
    "AB":      (A, B, (8.2, INF)),
    "AC":      (A, C, (10.4, 61.7)),
    "BC":      (B, C, (10.4, 61.7)),
    "reta":    (_R0, _R1, (12.2, INF)),
    "CM":      (C, M, (43.4, 61.7)),
    "perna_v": (C, B, (69.3, 78.3)),
    "perna_h": (A, C, (71.4, 78.3)),
    "eixo_x":  ((DOM_X[0], 0), (DOM_X[1], 0), (6.3, INF)),
    "eixo_y":  ((0, DOM_Y[0]), (0, DOM_Y[1]), (6.3, INF)),
}
# Pontos/marcas pequenos (caixas na tela) que os rótulos não podem cobrir
R_ANG = 0.22      # lado do símbolo de ângulo reto
MARCAS = {
    "ptA": (Caixa(_d(A)[0] - .08, _d(A)[0] + .08, _d(A)[1] - .08, _d(A)[1] + .08), (7.0, INF)),
    "ptB": (Caixa(_d(B)[0] - .08, _d(B)[0] + .08, _d(B)[1] - .08, _d(B)[1] + .08), (7.6, INF)),
    "ptC": (Caixa(_d(C)[0] - .08, _d(C)[0] + .08, _d(C)[1] - .08, _d(C)[1] + .08), (10.4, 61.7)),
    "ptM": (Caixa(_d(M)[0] - .09, _d(M)[0] + .09, _d(M)[1] - .09, _d(M)[1] + .09), (19.0, INF)),
    "ptN": (Caixa(_d((0, RETA_N))[0] - .09, _d((0, RETA_N))[0] + .09,
                  _d((0, RETA_N))[1] - .09, _d((0, RETA_N))[1] + .09), (99.87, INF)),
    "ang_C": (Caixa(_d(C)[0] - R_ANG, _d(C)[0], _d(C)[1], _d(C)[1] + R_ANG), (11.2, 61.7)),
    "ang_M": (Caixa(_d(M)[0] - 0.16, _d(M)[0] + 0.16, _d(M)[1], _d(M)[1] + 0.3), (50.3, INF)),
    "tique1": (Caixa(_d((1, 1))[0] - .1, _d((1, 1))[0] + .1, _d((1, 1))[1] - .12, _d((1, 1))[1] + .12), (11.6, 61.7)),
    "tique2": (Caixa(_d((4, 4))[0] - .12, _d((4, 4))[0] + .12, _d((4, 4))[1] - .1, _d((4, 4))[1] + .1), (11.6, 61.7)),
}


# ═══════════════════════════════════════════════════════════════════════════
# 5. TESTES
# ═══════════════════════════════════════════════════════════════════════════
def _luminancia(hexa):
    r, g, b = [int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(c1, c2):
    l1, l2 = sorted((_luminancia(c1), _luminancia(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def _janelas_se_cruzam(j1, j2):
    return j1[0] < j2[1] and j2[0] < j1[1]


def _segmento_toca_caixa(p, q, cx, n=400):
    for i in range(n + 1):
        t = i / n
        x, y = p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])
        if cx.x0 < x < cx.x1 and cx.y0 < y < cx.y1:
            return True
    return False


def testa_matematica():
    assert M == (1, 4), M
    assert M_AB == 1
    assert RETA_M == -1 and RETA_N == 5 and SOMA == 4
    assert M_AB * RETA_M == -1                                   # perpendiculares
    assert dict(ALTERNATIVAS)[LETRA_CORRETA] == SOMA
    assert C == (4, 1), C
    # C: ângulo reto, isósceles, abscissa positiva; a outra opção tem abscissa negativa
    ca = (A[0] - C[0], A[1] - C[1]); cb = (B[0] - C[0], B[1] - C[1])
    assert ca[0] * cb[0] + ca[1] * cb[1] == 0
    assert ca[0] ** 2 + ca[1] ** 2 == cb[0] ** 2 + cb[1] ** 2
    assert [c for c in candidatos_C() if c[0] > 0] == [C]
    # a reta y = mx + n passa por C e por M
    assert RETA_M * C[0] + RETA_N == C[1] and RETA_M * M[0] + RETA_N == M[1]
    # C - M é perpendicular a AB (mediana = altura)
    cm = (C[0] - M[0], C[1] - M[1]); ab = (B[0] - A[0], B[1] - A[1])
    assert cm[0] * ab[0] + cm[1] * ab[1] == 0
    # contas ditas no vídeo
    assert (A[0] + B[0]) == 2 and (A[1] + B[1]) == 8
    assert (B[1] - A[1]) == 6 and (B[0] - A[0]) == 6
    assert 4 - RETA_M * 1 == RETA_N        # 4 = -1 + n  ->  n = 4 + 1
    return "matemática"


def testa_zonas():
    assert contem(QUADRO, PALCO) and contem(QUADRO, ROSTO) and contem(QUADRO, FAIXA)
    assert not cruza(PALCO, ROSTO), "palco invade o rosto"
    assert PALCO.y0 - ROSTO.y1 >= 0.25, "pouca folga entre palco e rosto"
    assert not cruza(FAIXA, ROSTO) and FAIXA.x0 > ROSTO.x1
    for z in EVITAR:
        assert not cruza(FAIXA, z), f"faixa invade zona vermelha {z}"
        assert not cruza(ROSTO, z), f"rosto invade zona vermelha {z}"
        assert not cruza(PALCO, z), f"palco invade zona vermelha {z}"
    assert contem(PALCO, PLANO), PLANO
    assert contem(PALCO, COLUNA)
    assert not cruza(PLANO, COLUNA), "plano invade a coluna de contas"
    # roteiro e marca d'água dentro da faixa
    larg_roteiro = max(2.114, 2.317, 2.267) * ROTEIRO_ESCALA     # m+n=?, M=(1,4), m+n=4 medidos
    assert ROTEIRO_X >= FAIXA.x0 and ROTEIRO_X + larg_roteiro <= FAIXA.x1, larg_roteiro
    assert all(FAIXA.y0 <= y <= FAIXA.y1 for y in ROTEIRO_Y)
    marca = Caixa(MARCA_CENTRO[0] - MARCA_LARG_MAX / 2, MARCA_CENTRO[0] + MARCA_LARG_MAX / 2,
                  MARCA_CENTRO[1] - 0.15, MARCA_CENTRO[1] + 0.15)
    assert contem(FAIXA, marca), marca
    assert marca.y1 < ROTEIRO_Y[-1] - 0.3, "marca d'água encosta no roteiro"
    return "zonas"


def testa_pontos():
    for nome, p in dict(A=A, B=B, C=C, M=M, N=(0, RETA_N)).items():
        X, Y = para_tela(*p)
        assert contem(PLANO, Caixa(X, X, Y, Y)), (nome, X, Y)
    for p in (_R0, _R1):
        X, Y = para_tela(*p)
        assert contem(PLANO, Caixa(X, X, Y, Y)), p
    # a reta visível realmente está sobre y = -x + 5
    for (x, y) in (_R0, _R1):
        assert abs(y - (float(RETA_M) * x + float(RETA_N))) < 1e-9
    # escala igual nos dois eixos -> 45° no plano = 45° na tela (perpendicularidade fiel)
    (xa, ya), (xb, yb) = para_tela(*A), para_tela(*B)
    assert abs((yb - ya) - (xb - xa)) < 1e-9
    return "pontos"


def testa_rotulos():
    nomes = list(ROTULOS)
    caixas = {k: caixa_rotulo(ROTULOS[k]) for k in nomes}
    for k, cx in caixas.items():
        assert contem(PLANO, cx, tol=0.02), f"rótulo {k} sai do plano: {cx}"
    # rótulo x rótulo (só os que existem ao mesmo tempo)
    for i, k1 in enumerate(nomes):
        for k2 in nomes[i + 1:]:
            if _janelas_se_cruzam(ROTULOS[k1]["janela"], ROTULOS[k2]["janela"]):
                assert not cruza(caixas[k1], caixas[k2], folga=0.02), f"{k1} x {k2} se sobrepõem"
    # rótulo x segmento
    for k, cx in caixas.items():
        for s, (p, q, jan) in SEGMENTOS.items():
            if _janelas_se_cruzam(ROTULOS[k]["janela"], jan):
                P, Q = para_tela(*p), para_tela(*q)
                assert not _segmento_toca_caixa(P, Q, cx), f"rótulo {k} cruza o segmento {s}"
    # rótulo x pontos/marcas
    for k, cx in caixas.items():
        for mnome, (mc, jan) in MARCAS.items():
            if _janelas_se_cruzam(ROTULOS[k]["janela"], jan):
                assert not cruza(cx, mc), f"rótulo {k} cobre a marca {mnome}"
    return "rótulos"


def testa_contraste():
    for tema, t in TEMAS.items():
        for nome in ("AZUL", "AMARELO", "VERMELHO", "VERDE", "LARANJA", "CINZA", "EIXO"):
            assert contraste(t[nome], t["FUNDO"]) >= 3.0, (tema, nome, contraste(t[nome], t["FUNDO"]))
        assert contraste(t["TEXTO"], t["FUNDO"]) >= 7.0, (tema, "TEXTO")
        assert contraste(t["GRADE"], t["FUNDO"]) >= 1.05, (tema, "GRADE some no fundo")
        assert contraste(t["GRADE"], t["FUNDO"]) <= 1.6, (tema, "GRADE forte demais")
    return "contraste (claro e escuro)"


TESTES = [testa_matematica, testa_zonas, testa_pontos, testa_rotulos, testa_contraste]

if __name__ == "__main__":
    for t in TESTES:
        print("ok  ", t())
    print("\nC =", tuple(map(int, C)), "| M =", tuple(map(int, M)), "| y = %dx + %d" % (RETA_M, RETA_N),
          "| m+n =", int(SOMA), "| letra", LETRA_CORRETA)
    print("plano na tela:", tuple(round(v, 2) for v in PLANO), "| palco:", tuple(PALCO))
