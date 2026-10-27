"""PISM III 2025 — Questão 18 (potências e logaritmos) — @proflaiozago

Dados da questão, paleta/tema, zonas do palco (layout "rosto no meio-esquerda", o mesmo da
Questão 19 da EsPCEx) e TESTES. Não usa Manim.

    python3 geometria.py          # roda todos os testes (matemática, contraste, layout)
"""
import math

# ----------------------------------------------------------------------------------------------
# TEMA  ("claro" é o padrão; "escuro" só se o professor pedir)
# ----------------------------------------------------------------------------------------------
TEMA = "claro"

TEMAS = {
    "claro": dict(FUNDO="#FFFFFF", TEXTO="#111827", CINZA="#6B7280", AZUL="#1565C0",
                  AMARELO="#A16207", VERMELHO="#D32F2F", VERDE="#2E7D32", LARANJA="#C2410C"),
    "escuro": dict(FUNDO="#0F1115", TEXTO="#F3F4F6", CINZA="#9CA3AF", AZUL="#64B5F6",
                   AMARELO="#FFD54F", VERMELHO="#FF6B6B", VERDE="#6EE7A0", LARANJA="#FFA94D"),
}
_P = TEMAS[TEMA]
FUNDO, TEXTO, CINZA = _P["FUNDO"], _P["TEXTO"], _P["CINZA"]
AZUL, AMARELO, VERMELHO, VERDE, LARANJA = (_P[k] for k in ("AZUL", "AMARELO", "VERMELHO", "VERDE", "LARANJA"))

# Significado das cores NESTE vídeo (álgebra, sem figura):
#   AZUL     = o expoente que vai ser trabalhado (caixa em volta do expoente)
#   AMARELO  = propriedade / "macete" (caixas da coluna da direita, base igual à do log)
#   VERMELHO = "falta descobrir" (roteiro com "?")        VERDE = "já resolvido" (valores guardados)
#   LARANJA  = destaque de reforço (pisca)                 CINZA = contexto / apagado

# ----------------------------------------------------------------------------------------------
# ZONAS DO QUADRO 9x16 (x ±4,5 ; y ±8) — padronizadas na Questão 19 (v2)
# cada zona: (x0, x1, y0, y1)
# ----------------------------------------------------------------------------------------------
PALCO = (-4.1, 4.1, 0.4, 5.7)        # parte branca de cima (acima de +5,7 ficam as abas do TikTok)
ROSTO = (-4.1, 0.6, -4.6, 0.1)       # rosto do professor: LIVRE
FAIXA = (0.8, 2.8, -4.6, 0.1)        # ao lado do rosto: roteiro + marca d'água
EVITA_BOTOES = (2.9, 4.5, -8.0, 0.1)   # botões do TikTok (x > 2,9 abaixo de y = 0,1)
EVITA_LEGENDA = (-4.5, 4.5, -8.0, -4.7)  # legenda do TikTok (y < -4,7)
MARCA_POS = (1.85, -4.4)             # marca d'água @proflaiozago

PROIBIDAS = {"ROSTO": ROSTO, "BOTOES": EVITA_BOTOES, "LEGENDA": EVITA_LEGENDA}
PERMITIDAS = {"PALCO": PALCO, "FAIXA": FAIXA}

# ----------------------------------------------------------------------------------------------
# GRADE DO PALCO
# ----------------------------------------------------------------------------------------------
CAB_Y = 5.2                 # linha do cabeçalho (definições de x, y, z)
CAB_ESCALA = 0.66
CONTA_Y0 = 4.3              # primeira linha das contas
CONTA_PASSO = 0.8           # distância entre linhas
ESCALA_CONTA = 0.9
CONTA_X_ESQ = -4.0          # borda esquerda das contas
XI_XY = -2.9                # abscissa do "=" nas contas de x, y e z
XI_PROD = -2.2              # abscissa do "=" na conta do produto
LARG_MAX = 8.0              # nenhuma fórmula passa disso

REGRA_X = 2.275             # coluna da direita (regras): x +0,5 … +4,05 (as contas à esquerda acabam em ~+0,2)
REGRA_W = 3.5
REGRA_ESCALA = 0.8
SLOT1_Y = 3.7               # caixa da propriedade que muda (soma, subtração, potência de potência, peteleco)
SLOT1_H = 1.15
SLOT2_Y = 2.2               # caixa do macete a^{log_a b} = b
SLOT2_H = 0.9
LEGENDA_Y = 1.45            # "logaritmando"
ALT_X = 1.45                # alternativas (coluna da direita, no fim)
ALT_YS = (3.1, 2.55, 2.0, 1.45, 0.9)

ROT_X = 0.92                # roteiro na faixa ao lado do rosto
ROT_YS = (-0.3, -1.1, -1.9, -2.7)
ROT_ESCALA = 0.75
ROT_LARG = 1.85

# ----------------------------------------------------------------------------------------------
# A QUESTÃO
# ----------------------------------------------------------------------------------------------
TEX_X = r"x=2^{3+\log_2 5}"
TEX_Y = r"y=3^{2-\log_3 5}"
TEX_Z = r"z=6^{(\log_9 4)(\log_6 3)}"


def lg(base, x):
    return math.log(x) / math.log(base)


def valor_x():
    return 2 ** (3 + lg(2, 5))


def valor_y():
    return 3 ** (2 - lg(3, 5))


def valor_z():
    return 6 ** (lg(9, 4) * lg(6, 3))


ALTERNATIVAS = [
    ("A", r"52", 52.0),
    ("B", r"72", 72.0),
    ("C", r"144", 144.0),
    ("D", r"156\cdot 6^{\log_9 4}", 156 * 6 ** lg(9, 4)),
    ("E", r"216\cdot 6^{\log_9 4}", 216 * 6 ** lg(9, 4)),
]
GABARITO = "C"


# ----------------------------------------------------------------------------------------------
# TESTES
# ----------------------------------------------------------------------------------------------
def _lum(hex_):
    h = hex_.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contraste(a, b):
    la, lb = _lum(a), _lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def teste_matematica():
    close = lambda a, b: abs(a - b) < 1e-9
    # macete: a^{log_a b} = b
    assert close(2 ** lg(2, 5), 5) and close(3 ** lg(3, 5), 5) and close(6 ** lg(6, 3), 3)
    # x
    assert close(2 ** 3 * 5, 40) and close(valor_x(), 40)
    # y
    assert close(3 ** 2 / 5, 9 / 5) and close(valor_y(), 9 / 5)
    # z: (6^{log_6 3})^{log_9 4} = 3^{log_9 4}; log_9 4 = log_{3^2} 2^2 = 2 * (1/2) * log_3 2 = log_3 2
    assert close(valor_z(), 3 ** lg(9, 4))
    assert close(lg(9, 4), 2 * (1 / 2) * lg(3, 2)) and close(lg(9, 4), lg(3, 2))
    assert close(3 ** lg(3, 2), 2) and close(valor_z(), 2)
    # peteleco: log_a b^n = n log_a b ;  log_{a^m} b = (1/m) log_a b
    assert close(lg(3, 2 ** 2), 2 * lg(3, 2)) and close(lg(3 ** 2, 2), 0.5 * lg(3, 2))
    # propriedades das regras mostradas
    a, m, n = 7.0, 1.3, 0.4
    assert close(a ** (m + n), a ** m * a ** n) and close(a ** (m - n), a ** m / a ** n)
    assert close(a ** (m * n), (a ** m) ** n)
    # produto: 40 * 9/5 * 2 = 8 * 9 * 2 = 72 * 2 = 144
    assert close(40 * 9 / 5 * 2, 8 * 9 * 2) and 8 * 9 == 72 and 72 * 2 == 144
    assert close(valor_x() * valor_y() * valor_z(), 144)
    # gabarito: só uma alternativa vale o produto
    certas = [l for l, _, v in ALTERNATIVAS if abs(v - 144) < 1e-9]
    assert certas == [GABARITO], certas
    print("matemática ok:  x = %.0f   y = %.2f (9/5)   z = %.0f   x·y·z = %.0f   letra %s"
          % (valor_x(), valor_y(), valor_z(), valor_x() * valor_y() * valor_z(), GABARITO))


def teste_contraste():
    for nome, p in TEMAS.items():
        piso = {}
        for k, v in p.items():
            if k == "FUNDO":
                continue
            r = contraste(v, p["FUNDO"])
            piso[k] = r
            minimo = 7.0 if k == "TEXTO" else 3.0
            assert r >= minimo, "tema %s: %s tem contraste %.2f (< %.1f)" % (nome, k, r, minimo)
        print("contraste ok (%s): mínimo %.1f (%s)" % (nome, min(piso.values()), min(piso, key=piso.get)))


def _dentro(r, z, tol=1e-6):
    return r[0] >= z[0] - tol and r[1] <= z[1] + tol and r[2] >= z[2] - tol and r[3] <= z[3] + tol


def _cruza(r, z):
    return r[0] < z[1] and r[1] > z[0] and r[2] < z[3] and r[3] > z[2]


def teste_layout():
    assert _dentro(PALCO, (-4.5, 4.5, -8, 8)) and PALCO[3] <= 5.7
    assert not _cruza(PALCO, ROSTO) and not _cruza(FAIXA, ROSTO)       # palco e faixa não pisam no rosto
    assert not _cruza(PALCO, EVITA_BOTOES) and not _cruza(FAIXA, EVITA_BOTOES)
    assert not _cruza(PALCO, EVITA_LEGENDA) and not _cruza(FAIXA, EVITA_LEGENDA)
    # linhas das contas cabem no palco (5 linhas, meia altura 0,3)
    ult = CONTA_Y0 - 4 * CONTA_PASSO
    assert ult - 0.3 >= PALCO[2], ult
    assert CAB_Y + 0.3 <= PALCO[3]
    # coluna da direita e roteiro
    assert REGRA_X - REGRA_W / 2 >= -4.1 and REGRA_X + REGRA_W / 2 <= PALCO[1]
    assert ALT_YS[-1] - 0.25 >= PALCO[2]
    assert ROT_X >= FAIXA[0] and ROT_X + ROT_LARG <= FAIXA[1] + 1e-9
    assert all(FAIXA[2] <= y <= FAIXA[3] for y in ROT_YS)
    assert FAIXA[0] < MARCA_POS[0] < FAIXA[1] and FAIXA[2] < MARCA_POS[1] < FAIXA[3]
    print("layout ok: palco x%+.1f…%+.1f y%+.1f…%+.1f | rosto livre | faixa x%+.1f…%+.1f"
          % (PALCO[0], PALCO[1], PALCO[2], PALCO[3], FAIXA[0], FAIXA[1]))


def testes():
    teste_matematica()
    teste_contraste()
    teste_layout()
    print("TODOS OS TESTES DE GEOMETRIA PASSARAM")


if __name__ == "__main__":
    testes()
