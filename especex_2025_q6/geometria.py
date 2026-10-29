"""geometria.py — EsPCEx 2026, 2º dia, Questão 06 (7 paralelas dentro do triângulo).

Sem Manim: dados da questão, ENUNCIADO integral + recomposição, paleta/tema, zonas do
layout v2, geometria 2D da figura, fórmulas em LaTeX (fonte única) e testes
(`python3 geometria.py`).
"""
import math
from fractions import Fraction

# ---------------------------------------------------------------- tema
TEMA = "claro"      # "claro" (padrão, fundo branco) ou "escuro"
_PALETAS = {
    "claro": dict(FUNDO="#FFFFFF", TEXTO="#1B1B1B", CINZA="#7F868D", VERMELHO="#D32F2F",
                  VERDE="#2E7D32", AZUL="#1565C0", AMARELO="#A66B00", LARANJA="#D35400"),
    "escuro": dict(FUNDO="#10151C", TEXTO="#F2F2F2", CINZA="#8B949E", VERMELHO="#FF6B6B",
                   VERDE="#5CD65C", AZUL="#6CB6FF", AMARELO="#FFD54A", LARANJA="#FF9F43"),
}
_P = _PALETAS[TEMA]
FUNDO, TEXTO, CINZA = _P["FUNDO"], _P["TEXTO"], _P["CINZA"]
VERMELHO, VERDE, AZUL, AMARELO, LARANJA = (_P[k] for k in ("VERMELHO", "VERDE", "AZUL", "AMARELO", "LARANJA"))

# ------------------------------- larguras de letra (milésimos de em) — Arial/Liberation Sans
LARG_R = {' ': 278, '(': 333, ')': 333, ',': 278, '-': 333, '.': 278, '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556, '8': 556, '9': 556, ':': 278, ';': 278, '=': 584, 'A': 667, 'B': 667, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'N': 722, 'O': 778, 'Q': 778, 'S': 667, 'T': 611, 'U': 722, '[': 278, ']': 278, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 556, 'f': 278, 'g': 556, 'i': 222, 'l': 222, 'm': 833, 'n': 556, 'o': 556, 'p': 556, 'q': 556, 'r': 333, 's': 500, 't': 278, 'u': 556, 'v': 500, 'x': 500, '\xa0': 278, '²': 333, 'Ã': 667, 'á': 556, 'â': 556, 'ç': 500, 'é': 556, 'α': 578, '–': 556}
LARG_B = {' ': 278, '(': 333, ')': 333, ',': 278, '-': 333, '.': 278, '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556, '8': 556, '9': 556, ':': 333, ';': 333, '=': 584, 'A': 722, 'B': 722, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'N': 722, 'O': 778, 'Q': 778, 'S': 667, 'T': 611, 'U': 722, '[': 333, ']': 333, 'a': 556, 'b': 611, 'c': 556, 'd': 611, 'e': 556, 'f': 333, 'g': 611, 'i': 278, 'l': 278, 'm': 889, 'n': 611, 'o': 611, 'p': 611, 'q': 611, 'r': 389, 's': 556, 't': 333, 'u': 611, 'v': 556, 'x': 556, '\xa0': 278, '²': 333, 'Ã': 722, 'á': 556, 'â': 556, 'ç': 556, 'é': 556, 'α': 615, '–': 556}

# =====================================================================
# DADOS DA QUESTÃO
# =====================================================================
TG = Fraction(5, 2)          # tg α = 2,5
ALTURA_BASE = 60             # cm: de A até o 1º segmento (o "pedaço" de 60 cm)
N_SEG = 7                    # segmentos paralelos a BC
AREA_DEFG = 720              # cm²
IDX_G, IDX_F = 2, 4          # G = 3º segmento, F = 5º (contando de baixo, j = 0..6)
K = 1 / TG                   # AB = K · AC  (= 0,4)


def area_tri(h):
    """Área de um triângulo semelhante a ACB com cateto vertical h."""
    return K * h * h / 2


def resolve():
    """Acha s (o 'espacinho') por busca inteira: 0,2[(60+4s)² − (60+2s)²] = 720."""
    sols = []
    for s in range(1, 400):
        h = lambda j: ALTURA_BASE + j * s
        if area_tri(h(IDX_F)) - area_tri(h(IDX_G)) == AREA_DEFG:
            sols.append(s)
    assert len(sols) == 1, sols
    s = sols[0]
    ac = ALTURA_BASE + N_SEG * s          # 60 + 7 espacinhos
    ab = K * ac
    return dict(s=s, AC=ac, AB=ab, area=ac * ab / 2)


_R = resolve()
S, AC, AB, AREA = _R["s"], _R["AC"], int(_R["AB"]), int(_R["area"])
ALTERNATIVAS = [("A", 3380), ("B", 2400), ("C", 2580), ("D", 2800), ("E", 3120)]
GABARITO = "A"

# =====================================================================
# ENUNCIADO INTEGRAL (conferido no print da prova) — espaço sem quebra
# =====================================================================
NB = " "
TITULO = "QUESTÃO 06"
PARAGRAFOS = [
    "No interior do triângulo retângulo ABC foram traçados 7 segmentos paralelos "
    "ao lado BC, com extremidades nos lados AB e AC, sendo iguais as distâncias "
    "entre dois segmentos consecutivos quaisquer e entre o maior desses segmentos "
    "e o lado BC, conforme mostra a figura.",
    f"Sabendo que tg{NB}α{NB}={NB}2,5 e que a área do quadrilátero DEFG é "
    f"720{NB}cm², a área do triângulo ABC corresponde a",
]
ALT_TEXTOS = [
    (f"(A) 3{NB}380{NB}cm²."),
    (f"(B) 2{NB}400{NB}cm²."),
    (f"(C) 2{NB}580{NB}cm²."),
    (f"(D) 2{NB}800{NB}cm²."),
    (f"(E) 3{NB}120{NB}cm²."),
]
BOX_ENUNCIADO = (7.6, 5.0)   # largura x altura úteis (palco 8,2 x 5,3)
EM_MIN = 0.22                # "couber" = fonte mínima (u por em)
PASSO_LINHA = 1.30           # espaçamento entre linhas (em)
GAP_TITULO, GAP_PARAG, GAP_ALT = 0.55, 0.40, 0.60   # espaços extras (em)
FORMATO_ALTERNATIVAS = "auto"   # "auto" | "linha" | "duas" | "lista"


def larg_em(txt, negrito=False):
    tab = LARG_B if negrito else LARG_R
    return sum(tab.get(c, 556) for c in txt) / 1000.0


def quebra(texto, largura_em):
    """Quebra gulosa em linhas de no máximo largura_em (só em espaços normais)."""
    linhas, atual = [], ""
    for p in texto.split(" "):
        cand = p if not atual else atual + " " + p
        if not atual or larg_em(cand) <= largura_em:
            atual = cand
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def _alt_linhas(formato, largura_em):
    sep = NB * 4
    if formato == "lista":
        return list(ALT_TEXTOS)
    if formato == "linha":
        return [sep.join(ALT_TEXTOS)]
    if formato == "duas":
        return [sep.join(ALT_TEXTOS[:3]), sep.join(ALT_TEXTOS[3:])]
    raise ValueError(formato)


def compoe(em, formato):
    """Monta o bloco para um tamanho de fonte; devolve None se não couber no box."""
    larg_em_max = BOX_ENUNCIADO[0] / em
    itens = [dict(texto=TITULO, negrito=True, antes=0.0, tipo="titulo")]
    for i, par in enumerate(PARAGRAFOS):
        for k, ln in enumerate(quebra(par, larg_em_max)):
            itens.append(dict(texto=ln, negrito=False, tipo="texto",
                              antes=(GAP_TITULO if (i == 0 and k == 0) else
                                     GAP_PARAG if k == 0 else 0.0)))
    for k, ln in enumerate(_alt_linhas(formato, larg_em_max)):
        itens.append(dict(texto=ln, negrito=False, tipo="alt", antes=GAP_ALT if k == 0 else 0.0))
    larg = max(larg_em(it["texto"], it["negrito"]) for it in itens) * em
    alt = (len(itens) - 1) * PASSO_LINHA * em + sum(it["antes"] for it in itens) * em + em * 1.2
    if larg > BOX_ENUNCIADO[0] + 1e-9 or alt > BOX_ENUNCIADO[1] + 1e-9:
        return None
    return dict(em=em, formato=formato, itens=itens, largura=larg, altura=alt)


def melhor_composicao(formato=None):
    formato = formato or FORMATO_ALTERNATIVAS
    ordem = ["linha", "duas", "lista"] if formato == "auto" else [formato]
    em = 0.60
    while em >= 0.10:
        for f in ordem:                      # empate: prefere o formato mais compacto
            c = compoe(round(em, 4), f)
            if c:
                return c
        em -= 0.005
    raise RuntimeError("enunciado não cabe")


def texto_normalizado(s):
    return " ".join(s.replace(NB, " ").split())


# =====================================================================
# ZONAS DO LAYOUT v3 (quadro 9 x 16: x ±4,5 · y ±8)  — (x0, x1, y0, y1)
# Tiradas do ESBOÇO do professor sobre o frame de abertura (424 px = 9 u): quadradinho à esquerda =
# rosto; caixa grande ao lado = figura da questão (+ marca d'água). APROXIMADAS: o esboço não foi medido.
# =====================================================================
PALCO = (-4.1, 4.1, 0.4, 5.7)          # caixinha da CONTA (agora com a largura toda)
ROSTO = (-3.93, -1.12, -4.36, -1.77)   # livre
FIGBOX = (0.04, 4.08, -4.74, 0.10)     # caixa grande: FIGURA + marca d'água
RESP = (-3.93, -1.12, -1.75, 0.0)      # respostas parciais: no vão acima do rosto
MARCA = (1.85, -4.4)
EVITAR = [(2.9, 4.5, -8.0, 0.1), (-4.5, 4.5, -8.0, -4.7)]   # botões (x > 2,9) e legenda (y < −4,7)
X_MAX_FIG = 2.9                        # figura e rótulos não passam daqui (botões do TikTok)
ROT_X0, ROT_Y = -3.85, [-0.20, -0.64, -1.08, -1.52]         # itens do roteiro (dentro de RESP)
ESC_ROT = 0.80

# coluna das contas (palco inteiro): linhas novas por fase + duas regras fixas embaixo
X0_CONTA = -3.95
ESC_CONTA = 1.0
ESC_DIF = ESC_B1 = ESC_G = ESC_I4 = ESC_CONTA     # (a figura saiu do palco: tudo cabe a 1,0)
Y_REGRA1, Y_REGRA2 = 0.95, 1.95        # AB = 0,4AC · A = 0,2x² (depois a² − b² = (a+b)(a−b))
CONTA = (X0_CONTA, 4.05, 0.4, 5.7)


# =====================================================================
# FIGURA (cm → tela), na caixa grande
# =====================================================================
ORIG = (0.95, -3.85)         # onde fica o ponto A
ESC_FIG = 3.7 / AC           # u por cm (mesma escala nos dois eixos)


def tela(x, y):
    return (ORIG[0] + float(x) * ESC_FIG, ORIG[1] + float(y) * ESC_FIG)


def h_seg(j):
    return ALTURA_BASE + S * j


def seg_cm(j):
    h = h_seg(j)
    return (0, h), (K * h, 0)


PT = {"A": (0, 0), "B": (AB, 0), "C": (0, AC),
      "G": (0, h_seg(IDX_G)), "F": (0, h_seg(IDX_F)),
      "D": (K * h_seg(IDX_G), 0), "E": (K * h_seg(IDX_F), 0)}
PT_TELA = {n: tela(*p) for n, p in PT.items()}

ANG_ALFA = math.degrees(math.atan(float(TG)))     # ≈ 68,2°
FAIXAS_FORA = (IDX_G, IDX_G + 1)       # as duas faixas que formam DEFG (ficam alaranjadas, sempre)


def faixa_cm(k):
    """Faixa entre o segmento k e o seguinte (k = 0..6; a 7ª vai até BC)."""
    h1 = h_seg(k)
    h2 = h_seg(k + 1) if k < N_SEG - 1 else AC
    return [(0, h1), (K * h1, 0), (K * h2, 0), (0, h2)]


def pos_rotulos():
    """Posições (tela) dos rótulos: letras, s em cada espacinho, 60 cm, 720 cm²."""
    A, B, C = PT_TELA["A"], PT_TELA["B"], PT_TELA["C"]
    pos = {
        "A": (A[0] - 0.22, A[1] - 0.22), "B": (B[0] + 0.12, B[1] - 0.22),
        "C": (C[0] - 0.22, C[1] + 0.18),
        "D": (PT_TELA["D"][0] - 0.07, A[1] - 0.22), "E": (PT_TELA["E"][0] + 0.07, A[1] - 0.22),
        "F": (PT_TELA["F"][0] - 0.40, PT_TELA["F"][1]), "G": (PT_TELA["G"][0] - 0.40, PT_TELA["G"][1]),
    }
    mids = [ALTURA_BASE + S * (j + 0.5) for j in range(N_SEG)]
    pos["s"] = [(A[0] - 0.17, tela(0, m)[1]) for m in mids]
    ang = math.radians(180 - ANG_ALFA / 2)
    pos["alfa"] = (PT_TELA["D"][0] + 0.42 * math.cos(ang), PT_TELA["D"][1] + 0.42 * math.sin(ang))
    pos["60x"] = A[0] - 0.50
    pos["60cm"] = (A[0] - 0.76, tela(0, ALTURA_BASE / 2)[1])
    # "720 cm²": à direita de BC, bem afastado da reta; fio inclinado até o centro de DEFG
    pos["720"] = (2.50, tela(0, 70)[1])
    pos["720_centro"] = tela(18, 45)
    pos["720_fio_fim"] = (pos["720"][0] - 0.36 - 0.10, pos["720"][1])
    return pos


# =====================================================================
# FÓRMULAS (fonte única) — cada parte é LaTeX válido SOZINHA
# =====================================================================
FORM = {
    # fase A (7 – 32 s)
    "A_tg":      [r"\tan\alpha", "=", r"2{,}5"],
    "A_dif":     [r"A_{DEFG}", "=", r"A_{AFE}", "-", r"A_{AGD}", "=", "720"],
    # fase B (34 – 57 s)
    "B_1":       [r"\tan\alpha", "=", r"2{,}5", "=", r"\frac{\text{cat. oposto}}{\text{cat. adjacente}}"],
    "B_2":       [r"\tan\alpha", "=", r"\frac{AC}{AB}", "=", r"\frac{5}{2}"],
    "B_3":       [r"5\,AB", "=", r"2\,AC"],
    "B_4":       ["AB", "=", r"\frac{2}{5}", "AC", "=", r"0{,}4\,AC"],      # vira REGRA 1
    # fase C (57 – 74 s)
    "C_1":       [r"\triangle_j", r"\sim", r"\triangle ACB"],
    # fase D (74 – 106 s)
    "D_1":       ["AC", "=", "x"],
    "D_2":       ["AB", "=", r"0{,}4", "x"],
    "D_3":       ["A", "=", "x", r"\cdot", r"0{,}4x", r"\div", "2"],
    "D_4":       ["=", r"0{,}2", r"x^2"],
    "D_5":       [r"x", "=", r"\text{cateto vertical}"],
    "R2":        ["A", "=", r"0{,}2", r"x^2"],                               # REGRA 2
    # fase E/F (106 – 153 s)
    "E_1":       [r"\text{espacinho}", "=", "s"],
    "F_1":       [r"A_{AFE}", "=", r"0{,}2", r"(60+4s)", r"{}^{2}"],
    "F_2":       [r"A_{AGD}", "=", r"0{,}2", r"(60+2s)", r"{}^{2}"],
    # fase G (153 – 183 s)
    "R3":        [r"a^2-b^2", "=", r"(a+b)(a-b)"],                          # REGRA 3
    "G_1":       [r"0{,}2", r"\bigl[", r"(60+4s)^2", "-", r"(60+2s)^2", r"\bigr]", "=", "720"],
    "G_2a":      [r"0{,}2", r"\bigl[", r"(60+4s)", "+", r"(60+2s)", r"\bigr]"],
    "G_2b":      [r"\cdot", r"\bigl[", r"(60+4s)", "-", r"(60+2s)", r"\bigr]", "=", "720"],
    # fase H (183 – 210 s)
    "H_1":       [r"2s", r"\cdot", r"(120+6s)", "=", "3600"],
    "H_1n":      [r"720\div 0{,}2"],
    "H_2":       [r"s^2", "+20s", "-300", "=0"],
    "H_3":       ["s", "=", "10"],
    # fase I (210 – 240 s)
    "I_1":       ["AC", "=", "60", "+", r"7\cdot 10"],
    "I_2":       ["AC", "=", "60+70", "=", "130"],
    "I_3":       ["AB", "=", r"0{,}4", r"\cdot", "130", "=", "52"],
    "I_4":       [r"A_{ABC}", "=", "130", r"\cdot", "52", r"\div", "2", "=", "3380"],
}
ROT_ABERTO = [["s", "=", "?"], ["AC", "=", "?"], ["AB", "=", "?"], [r"A_{ABC}", "=", "?"]]
ROT_FECHADO = [["s", "=", "10"], ["AC", "=", "130"], ["AB", "=", "52"], [r"A_{ABC}", "=", "3380"]]
ALT_FORM = [[rf"\text{{({l})}}", rf"{v//1000}\,{v%1000:03d}\ \text{{cm}}^2"] for l, v in ALTERNATIVAS]


# =====================================================================
# TESTES  (python3 geometria.py)
# =====================================================================
def _dentro(p, z, folga=0.0):
    return z[0] - folga <= p[0] <= z[1] + folga and z[2] - folga <= p[1] <= z[3] + folga


def _inter(a, b):
    return not (a[1] <= b[0] or b[1] <= a[0] or a[3] <= b[2] or b[3] <= a[2])


def _testes():
    ok, falhas = 0, []

    def t(nome, cond, info=""):
        nonlocal ok
        if cond:
            ok += 1
        else:
            falhas.append(f"{nome} {info}")

    # --- matemática
    t("s = 10", S == 10)
    t("AC = 130", AC == 130)
    t("AB = 52 = 0,4·AC", AB == 52 and AB == K * AC)
    t("área ABC = 3380", AREA == 3380)
    t("gabarito A bate", dict(ALTERNATIVAS)[GABARITO] == AREA)
    t("alternativas distintas", len({v for _, v in ALTERNATIVAS}) == 5)
    t("tg α = AC/AB", Fraction(AC, AB) == TG)
    t("DEFG = AFE − AGD = 720", area_tri(h_seg(IDX_F)) - area_tri(h_seg(IDX_G)) == 720)
    t("s²+20s−300 = 0", S * S + 20 * S - 300 == 0)
    t("2s(120+6s) = 3600", 2 * S * (120 + 6 * S) == 3600)
    t("720/0,2 = 3600", Fraction(720) / Fraction(1, 5) == 3600)
    t("(120+6s) = 180 e 2s = 20", 120 + 6 * S == 180 and 2 * S == 20)
    t("F a 100 e G a 80 do A", PT["F"][1] == 100 and PT["G"][1] == 80)
    t("D = 32 e E = 40 no lado AB", PT["D"][0] == 32 and PT["E"][0] == 40)
    t("maior segmento a 1 espaço de BC", AC - h_seg(N_SEG - 1) == S)
    t("ANG_ALFA ≈ 68,2°", abs(ANG_ALFA - 68.1986) < 1e-3)
    # cada segmento é paralelo a BC: inclinação −2,5
    for j in range(N_SEG):
        (x1, y1), (x2, y2) = seg_cm(j)
        t(f"seg {j} paralelo a BC", abs((y2 - y1) / (x2 - x1) + float(TG)) < 1e-9)

    # --- tema / contraste
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

    def contr(a, b):
        la, lb = sorted((lum(a), lum(b)), reverse=True)
        return (la + 0.05) / (lb + 0.05)

    for tema, p in _PALETAS.items():
        for nome, cor in p.items():
            if nome == "FUNDO":
                continue
            minimo = 7.0 if nome == "TEXTO" else 3.0
            t(f"contraste {tema}/{nome}", contr(cor, p["FUNDO"]) >= minimo,
              f"{contr(cor, p['FUNDO']):.2f}")

    # --- zonas (layout v3: conta no palco · rosto · figura na caixa grande · respostas acima do rosto)
    for a, b, nome in ((ROSTO, PALCO, "rosto/palco"), (FIGBOX, PALCO, "figura/palco"), (RESP, PALCO, "respostas/palco"),
                       (ROSTO, FIGBOX, "rosto/figura"), (RESP, ROSTO, "respostas/rosto"), (RESP, FIGBOX, "respostas/figura")):
        t(f"zonas separadas: {nome}", not _inter(a, b))
    for z in EVITAR:
        t("evitar não encosta no rosto", not _inter(z, ROSTO))
        t("evitar não encosta nas respostas", not _inter(z, RESP))
    t("marca d'água na caixa da figura", _dentro(MARCA, FIGBOX))
    t("roteiro dentro das respostas parciais", all(RESP[2] + 0.2 <= y <= RESP[3] for y in ROT_Y))
    t("conta usa o palco todo", CONTA[0] >= PALCO[0] and CONTA[1] <= PALCO[1])

    # --- figura dentro da caixa grande e fora da zona dos botões
    pr = pos_rotulos()
    pts = list(PT_TELA.values()) + [pr[n] for n in "ABCDEFG"]
    pts += pr["s"] + [pr["60cm"], pr["alfa"]]
    t("tudo da figura cabe na caixa grande", all(_dentro(p, FIGBOX) for p in pts),
      str([p for p in pts if not _dentro(p, FIGBOX)]))
    t("figura não entra na zona dos botões (x <= 2,9)", all(p[0] <= X_MAX_FIG for p in pts + [pr["B"]]))
    t("letra A acima da marca d'água", pr["A"][1] - 0.12 >= MARCA[1] + 0.10, f"{pr['A'][1] - 0.12:.2f}")
    t("letras D e E separadas", pr["E"][0] - pr["D"][0] >= 0.17)
    t("letras E e B separadas", pr["B"][0] - pr["E"][0] >= 0.17)
    t("C não encosta no último s", pr["C"][1] - pr["s"][-1][1] >= 0.25, f"{pr['C'][1] - pr['s'][-1][1]:.2f}")
    t("s afastados das letras F e G", all(abs(sx - pr["F"][0]) >= 0.2 for sx, _ in pr["s"]))
    # 720 cm²: afastado de BC (folga >= 0,30), dentro da caixa e fora dos botões, fio chega ao centro de DEFG
    p720, c720, fim720 = pr["720"], pr["720_centro"], pr["720_fio_fim"]
    B_, C_ = PT_TELA["B"], PT_TELA["C"]
    x_bc = B_[0] + (C_[0] - B_[0]) * (p720[1] - B_[1]) / (C_[1] - B_[1])
    meia = 0.36                     # meia largura estimada de "720 cm²" (escala 0,5)
    t("rótulo 720 afastado de BC (>= 0,30)", fim720[0] - x_bc >= 0.30, f"{fim720[0] - x_bc:.2f}")
    t("rótulo 720 dentro da caixa e fora dos botões", p720[0] + meia <= X_MAX_FIG and _dentro((p720[0] + meia, p720[1]), FIGBOX))
    G_, F_, E_, D_ = (PT_TELA[n] for n in "GFED")
    def x_em_y(p, q, y):
        return p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])
    t("centro de DEFG está dentro de DEFG", x_em_y(G_, D_, c720[1]) <= c720[0] <= x_em_y(F_, E_, c720[1]))
    t("fio do 720 cruza o triângulo na diagonal (inclinação 0,3..1,5)",
      0.3 <= abs((fim720[1] - c720[1]) / (fim720[0] - c720[0])) <= 1.5)

    # --- enunciado
    c = melhor_composicao()
    t("enunciado: fonte >= mínimo", c["em"] >= EM_MIN, f"em={c['em']}")
    t("enunciado cabe no box (largura)", c["largura"] <= BOX_ENUNCIADO[0] + 1e-9)
    t("enunciado cabe no box (altura)", c["altura"] <= BOX_ENUNCIADO[1] + 1e-9)
    t("box cabe no palco", BOX_ENUNCIADO[0] <= PALCO[1] - PALCO[0] and BOX_ENUNCIADO[1] <= PALCO[3] - PALCO[2])
    esperado = texto_normalizado(" ".join([TITULO] + PARAGRAFOS + ALT_TEXTOS))
    obtido = texto_normalizado(" ".join(it["texto"] for it in c["itens"]))
    t("o texto recomposto tem todo o texto da prova, na ordem", esperado == obtido)
    t("alternativas A..E presentes", all(f"({l})" in obtido for l, _ in ALTERNATIVAS))
    for f in ("linha", "duas", "lista"):
        cf = compoe(0.22, f)
        t(f"formato {f} existe/mede", cf is None or cf["largura"] > 0)
    # fonte da prova (print) ≈ 0,17 u por em: recomposto deve ser maior
    t("fonte maior que a do print (0,17)", c["em"] > 0.17)

    # --- fórmulas
    for k, v in FORM.items():
        t(f"fórmula {k} sem parte vazia", all(p.strip() for p in v))
        t(f"fórmula {k} chaves balanceadas",
          all(p.count("{") == p.count("}") for p in v))
    t("roteiro 4 itens aberto e fechado", len(ROT_ABERTO) == 4 == len(ROT_FECHADO) == len(ROT_Y))
    t("alternativas em LaTeX 5", len(ALT_FORM) == 5)

    print(f"melhor composição: em={c['em']:.3f} u/em · formato={c['formato']} · "
          f"{c['largura']:.2f} x {c['altura']:.2f} u "
          f"({100 * c['largura'] / (PALCO[1] - PALCO[0]):.0f}% da largura do palco) · "
          f"{len(c['itens'])} linhas")
    print(f"{ok} testes ok" + (f", {len(falhas)} FALHAS:" if falhas else " — tudo certo"))
    for f in falhas:
        print("  ✗", f)
    return not falhas


if __name__ == "__main__":
    raise SystemExit(0 if _testes() else 1)
