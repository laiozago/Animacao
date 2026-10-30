# -*- coding: utf-8 -*-
"""
geometria.py — PISM III 2019, Questão 18 (polinômio x³ − 8x² + 19x − 12: soma dos quadrados das raízes)

NÃO importa Manim. Contém:
  • dados da questão (com conferência matemática);
  • ENUNCIADO integral (texto da prova) e melhor_composicao() (quebra de linhas + maior fonte que couber);
  • tema/paleta, zonas do layout 9:16 (palco / rosto / faixa);
  • fórmulas em LaTeX (fonte única: dicionário F) e posições do layout;
  • testes:  python3 geometria.py
"""
import sys

# ═════════════════════════════════════════════════════════════════════════
# TEMA E PALETA  (cores com significado fixo — ver padrao-manim.md)
# ═════════════════════════════════════════════════════════════════════════
TEMA = "claro"          # "claro" (padrão, fundo branco) ou "escuro"

_CLARO = dict(FUNDO="#FFFFFF", TEXTO="#1A1A1A", VERMELHO="#D32F2F", VERDE="#2E7D32",
              AZUL="#1565C0", AMARELO="#B58900", LARANJA="#E65100", CINZA="#8A8A8A")
_ESCURO = dict(FUNDO="#10141A", TEXTO="#F2F2F2", VERMELHO="#FF6B6B", VERDE="#5FD068",
               AZUL="#6CB6FF", AMARELO="#F2C94C", LARANJA="#FF9F43", CINZA="#9AA0A6")
CORES = _CLARO if TEMA == "claro" else _ESCURO
FUNDO, TEXTO = CORES["FUNDO"], CORES["TEXTO"]
VERMELHO, VERDE, AZUL = CORES["VERMELHO"], CORES["VERDE"], CORES["AZUL"]
AMARELO, LARANJA, CINZA = CORES["AMARELO"], CORES["LARANJA"], CORES["CINZA"]
FONTE = "Arial"

# Neste vídeo (detalhe das famílias de cor):
#   AZUL = coeficientes / números em trabalho · AMARELO = regra, ferramenta, legenda de método ·
#   LARANJA = produtos do dispositivo, pisca de atenção, cancelamento · VERMELHO = falta descobrir ·
#   VERDE = já resolvido · CINZA = contexto (os x do polinômio, o que não está em foco)

# ═════════════════════════════════════════════════════════════════════════
# ZONAS DO LAYOUT  (quadro 9 x 16 unidades; x ±4,5 · y ±8)   (x0, x1, y0, y1)
# ═════════════════════════════════════════════════════════════════════════
PALCO = (-4.1, 4.1, 0.4, 5.7)       # caixinha da CONTA (parte branca de cima)
ROSTO = (-4.1, 0.6, -4.6, 0.1)      # rosto (livre)
FAIXA = (0.8, 2.8, -4.6, 0.1)       # caixinha das RESPOSTAS PARCIAIS (ao lado do rosto)
MARCA = (1.85, -4.4)                # centro da marca d'água @proflaiozago
X_ROT, ROT_Y, ROT_ESCALA, ROT_LARG = 0.85, (-0.35, -1.15, -1.95, -2.75), 0.75, 1.95
BOX_ENUNCIADO = (7.6, 5.0)          # área do enunciado dentro do palco (palco: 8,2 x 5,3)
FONTE_MIN = 0.22                    # "couber" = pelo menos 0,22 u por em
FONTE_MAX = 0.60                    # teto de sanidade
FORMATO_ALTERNATIVAS = "auto"       # "auto" | "lista" | "linha"


def dentro(caixa, zona, folga=1e-6):
    x0, x1, y0, y1 = caixa
    X0, X1, Y0, Y1 = zona
    return x0 >= X0 - folga and x1 <= X1 + folga and y0 >= Y0 - folga and y1 <= Y1 + folga


def cruza(a, b):
    return not (a[1] <= b[0] or b[1] <= a[0] or a[3] <= b[2] or b[3] <= a[2])


def _lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = _lum(a), _lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


# ═════════════════════════════════════════════════════════════════════════
# DADOS DA QUESTÃO
# ═════════════════════════════════════════════════════════════════════════
COEFS = (1, -8, 19, -12)            # p(x) = x³ − 8x² + 19x − 12
RAIZ_TESTE = 1
ALTERNATIVAS = (("A", 12), ("B", 24), ("C", 26), ("D", 38), ("E", 64))
GABARITO = "C"


def p(x):
    return sum(c * x ** (3 - i) for i, c in enumerate(COEFS))


def briot_ruffini(coefs, r):
    """Dispositivo de Briot-Ruffini: devolve (resultados, produtos, resto).
    produtos[i] = r·resultados[i-1] (o 1º não tem produto)."""
    res, prod = [coefs[0]], [None]
    for c in coefs[1:]:
        pr = r * res[-1]
        prod.append(pr)
        res.append(c + pr)
    return res, prod, res[-1]


RES, PROD, RESTO = briot_ruffini(COEFS, RAIZ_TESTE)      # [1,-7,12,0], [None,1,-7,12], 0
QUAD = RES[:3]                                           # x² − 7x + 12
RAIZES = (1, 3, 4)
SOMA_QUAD = sum(r * r for r in RAIZES)                   # 26
QUADRADO_DA_SOMA = sum(RAIZES) ** 2                      # 64 (a pegadinha da alternativa E)

# ═════════════════════════════════════════════════════════════════════════
# ENUNCIADO INTEGRAL (conferido no print da prova) — NBSP (\u00a0) mantém a fórmula numa linha só
# ═════════════════════════════════════════════════════════════════════════
NB = "\u00a0"
ENUNCIADO = dict(
    titulo="QUESTÃO 18",
    paragrafos=[
        "Considere o polinômio p(x)" + NB + "=" + NB + "x³" + NB + "−" + NB + "8x²" + NB + "+" + NB +
        "19x" + NB + "−" + NB + "12.",
        "A soma dos quadrados das raízes desse polinômio é",
    ],
    alternativas=[(a, str(v)) for a, v in ALTERNATIVAS],
)
# transcrição palavra por palavra do print (para o teste "tem todo o texto da prova, na ordem")
TRANSCRICAO = ("QUESTÃO 18 Considere o polinômio p(x) = x³ − 8x² + 19x − 12. "
               "A soma dos quadrados das raízes desse polinômio é "
               "(A) 12 (B) 24 (C) 26 (D) 38 (E) 64")

# ─── larguras da Arial/Helvetica (unidades de 1/1000 em; ASCII 32..126 + extras) ───
_REG = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556,
        556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278,
        500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469,
        556, 333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500,
        278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584]
_NEG = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556,
        556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278,
        556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584,
        556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556,
        333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584]
_REG_EX = {'À': 667, 'Á': 667, 'Â': 667, 'Ã': 667, 'Ç': 722, 'É': 667, 'Ê': 667, 'Í': 278, 'Ó': 778, 'Ô': 778,
           'Õ': 778, 'Ú': 722, 'à': 556, 'á': 556, 'â': 556, 'ã': 556, 'ç': 500, 'é': 556, 'ê': 556, 'í': 278,
           'ó': 556, 'ô': 556, 'õ': 556, 'ú': 556, 'ü': 556, '²': 333, '³': 333, '−': 584, '–': 556, '—': 1000,
           '·': 333, '×': 584, '÷': 549, '≠': 549, 'º': 365, '\xa0': 278}
_NEG_EX = {'À': 722, 'Á': 722, 'Â': 722, 'Ã': 722, 'Ç': 722, 'É': 667, 'Ê': 667, 'Í': 278, 'Ó': 778, 'Ô': 778,
           'Õ': 778, 'Ú': 722, 'à': 556, 'á': 556, 'â': 556, 'ã': 556, 'ç': 556, 'é': 556, 'ê': 556, 'í': 278,
           'ó': 611, 'ô': 611, 'õ': 611, 'ú': 611, 'ü': 611, '²': 333, '³': 333, '−': 584, '–': 556, '—': 1000,
           '·': 333, '×': 584, '÷': 549, '≠': 549, 'º': 365, '\xa0': 278}
ESPACO_EM = 0.278
SEP_ALT = " " + NB * 3                    # separador das alternativas numa linha só (1 espaço + 3 NBSP)
GAP_ALT_EM = ESPACO_EM * 4


def larg_em(txt, neg=False):
    """Largura (em unidades de 'em') de um texto em Arial regular ou negrito."""
    t, ex = (_NEG, _NEG_EX) if neg else (_REG, _REG_EX)
    tot = 0
    for ch in txt:
        o = ord(ch)
        if 32 <= o <= 126:
            tot += t[o - 32]
        elif ch in ex:
            tot += ex[ch]
        else:
            raise ValueError("caractere fora da tabela de larguras: %r" % ch)
    return tot / 1000.0


# ─── composição ───
LH = 1.30            # entrelinha (em)
GAP_BLOCO = 0.55     # espaço extra entre blocos (em)
ALTURA_CAPS, PROFUND = 0.716, 0.21


def _guloso(palavras, lim):
    linhas, atual = [[]], 0.0
    for pal in palavras:
        w = larg_em(pal)
        novo = w if not linhas[-1] else atual + ESPACO_EM + w
        if linhas[-1] and novo > lim:
            linhas.append([pal])
            atual = w
        else:
            linhas[-1].append(pal)
            atual = novo
    return linhas


def _quebra(palavras, w_max_em):
    """Quebra gulosa em w_max_em e depois BALANCEIA: o menor limite que ainda dá o mesmo número de linhas
    (a fonte não muda; só evita 'polinômio é' sozinho na última linha)."""
    base = _guloso(palavras, w_max_em)
    lo, hi = max(larg_em(p) for p in palavras), w_max_em
    if lo > hi:
        return base
    for _ in range(40):
        mid = (lo + hi) / 2
        if len(_guloso(palavras, mid)) <= len(base):
            hi = mid
        else:
            lo = mid
    return _guloso(palavras, hi)


def _monta(s, formato, box=BOX_ENUNCIADO):
    """Tenta compor o enunciado com fonte s (u por em). Devolve None se não couber."""
    W, H = box
    wem = W / s
    L = [dict(tipo="titulo", palavras=ENUNCIADO["titulo"].split(" "), neg=True, bloco=0, gap=ESPACO_EM)]
    for i, par in enumerate(ENUNCIADO["paragrafos"]):
        for ln in _quebra(par.split(" "), wem):
            L.append(dict(tipo="paragrafo", palavras=ln, neg=False, bloco=1 + i, gap=ESPACO_EM))
    b_alt = 1 + len(ENUNCIADO["paragrafos"])
    alts = ["(%s)%s%s" % (a, NB, v) for a, v in ENUNCIADO["alternativas"]]
    if formato == "linha":
        L.append(dict(tipo="alternativas", palavras=alts, neg=False, bloco=b_alt, gap=GAP_ALT_EM))
    else:
        for a in alts:
            L.append(dict(tipo="alternativas", palavras=[a], neg=False, bloco=b_alt, gap=ESPACO_EM))
    base, ult_bloco = 0.0, 0
    for k, ln in enumerate(L):
        ln["larg_em"] = sum(larg_em(w, ln["neg"]) for w in ln["palavras"]) + ln["gap"] * (len(ln["palavras"]) - 1)
        sep = SEP_ALT if (ln["tipo"] == "alternativas" and len(ln["palavras"]) > 1) else " "
        ln["texto"] = sep.join(ln["palavras"])
        if k > 0:
            base += LH * s + (GAP_BLOCO * s if ln["bloco"] != ult_bloco else 0.0)
        ult_bloco = ln["bloco"]
        ln["base"] = base                     # distância (u) da linha de base desta linha à da 1ª linha
        cum, acc = [], 0.0                    # fim de cada palavra (em) — para o "digitar" palavra por palavra
        for j, w in enumerate(ln["palavras"]):
            acc += larg_em(w, ln["neg"])
            cum.append(acc)
            acc += ln["gap"]
        ln["cum_fim"] = cum
        if ln["larg_em"] * s > W + 1e-9:
            return None
    altura = L[-1]["base"] + (ALTURA_CAPS + PROFUND) * s
    if altura > H + 1e-9:
        return None
    return dict(s=s, formato=formato, linhas=L, largura=max(l["larg_em"] for l in L) * s, altura=altura)


def melhor_composicao(formato=None):
    """Maior fonte (u por em) com que o enunciado integral cabe em BOX_ENUNCIADO."""
    formato = formato or FORMATO_ALTERNATIVAS
    formatos = ["linha", "lista"] if formato == "auto" else [formato]
    melhor = None
    for f in formatos:
        s = FONTE_MAX
        while s >= 0.10:
            c = _monta(round(s, 3), f)
            if c:
                if melhor is None or c["s"] > melhor["s"] + 1e-9:
                    melhor = c
                break
            s -= 0.005
    return melhor


def texto_recomposto(c):
    return " ".join(l["texto"] for l in c["linhas"])


# ═════════════════════════════════════════════════════════════════════════
# FÓRMULAS EM LaTeX  (fonte única — cada peça é LaTeX válido sozinha)
# ═════════════════════════════════════════════════════════════════════════
F = dict(
    # cabeçalho: p(x) em peças (os "x" podem ficar cinza, os coeficientes azuis)
    px=["p(x)=", "x^3", "-8", "x^2", "+19", "x", "-12"],
    # teste do 1 raiz
    t1=["p(1)", "=", "1", "-8", "+19", "-12"],
    t2=["=20", "-20"],
    t3=["=0"],
    # abaixar o grau
    pB=["p(x)"],
    qB=["q(x)"],
    slots=["r_1=1", ",\\ r_2=?", ",\\ r_3=?"],
    # dispositivo de Briot-Ruffini (cada célula é uma fórmula)
    coef=["1", "-8", "19", "-12"],
    prod=["1", "-7", "12"],
    res=["1", "-7", "12", "0"],
    raiz="1",
    # novo polinômio
    q=["q(x)=", "x^2", "-7x", "+12", "=0"],
    # soma e produto
    soma=["\\text{soma}=7"],
    produto=["\\text{produto}=12"],
    slots_s=["?", "+", "?", "=7"],
    slots_p=["?", "\\cdot", "?", "=12"],
    n3="3", n4="4",
    raizes=["r_1=1", ",\\ r_2=3", ",\\ r_3=4"],
    # soma dos quadrados
    E1=["S=", "1^2", "+3^2", "+4^2"],
    E2=["=1", "+9", "+16"],
    E3=["=10", "+16", "=26"],
    # a pegadinha: quadrado da soma
    errada=["(1", "+3", "+4)^2", "=8", "{}^2", "=64"],
    # roteiro (faixa ao lado do rosto): pendente (vermelho, com ?) → resolvido (verde)
    rot_pend=["p(1)=?", "q(x)=?", "r_2,r_3=?", "S=?"],
    rot_ok=["p(1)=0", "x^2-7x+12", "r_2,r_3=3\\ \\text{e}\\ 4", "S=26"],
)

# textos (Text, Arial) usados na cena — só para conferir acentos/larguras
TEXTOS = dict(
    briot="Briot-Ruffini", regra_zero="se der 0, o 1 é raiz", raiz_ok="o 1 é raiz",
    g3="grau 3", g2="grau 2", t_sp="Soma e Produto", t_bh="Bhaskara", ou="ou", raiz="raiz",
    cap1="multiplica\ne soma", cap2="dá zero:\né raiz", cap3="novo\npolinômio",
    tit_S="S = soma dos quadrados das raízes", lbl_quad="quadrado\nda soma", b1="1º", b2="2º",
)

# ═════════════════════════════════════════════════════════════════════════
# POSIÇÕES DO LAYOUT (dentro do palco)
# ═════════════════════════════════════════════════════════════════════════
Y_CAB = 5.10                         # cabeçalho p(x)
Y_TITULO = 4.25                      # "Briot-Ruffini" / título de bloco
# dispositivo de Briot-Ruffini
Y_COEF, Y_PROD, Y_TRACO, Y_RES = 3.45, 2.80, 2.50, 2.10
X_RAIZ, X_BARRA = -3.55, -2.95
COL_X = (-2.25, -1.15, -0.05, 1.05)
X_FIM = 1.75
Y_BARRA = (3.85, 1.75)               # (topo, base) da barra vertical
X_CAP = 2.95                         # centro da coluna de legendas (direita)
Y_CAP = (3.55, 2.55, 1.55)
Y_QLINHA = 1.00                      # linha do novo polinômio (abaixo do dispositivo)
# teste do 1
Y_REGRA, Y_T1, Y_T2, Y_T3 = 4.10, 3.20, 2.30, 1.45
# abaixar o grau
Y_PQ, Y_GRAU, Y_FERR, Y_SLOTS = 3.55, 2.80, 1.90, 1.00
# soma e produto
Y_EQ, Y_SOMA, Y_PROD2, Y_RAIZES = 4.05, 3.10, 2.25, 1.20
X_COL1, X_COL2 = -2.15, 1.20
# soma dos quadrados + pegadinha
Y_TIT_S, Y_E1, Y_E2, Y_E3, Y_ERR = 4.30, 3.50, 2.70, 1.90, 0.95
ESQ_E = -3.15                        # borda esquerda das linhas da soma dos quadrados
X_ALT, Y_ALT, DY_ALT = 2.15, 4.35, 0.65     # lista de alternativas (borda esquerda, 1º y, passo)
POS_LBL_QUAD = (3.05, 0.95)

# ═════════════════════════════════════════════════════════════════════════
# TESTES
# ═════════════════════════════════════════════════════════════════════════
_falhas = []


def _ok(cond, msg):
    if not cond:
        _falhas.append(msg)
        print("  FALHA:", msg)
    return cond


def testes(verbose=True):
    global _falhas
    _falhas = []
    n = 0

    def T(cond, msg):
        nonlocal n
        n += 1
        return _ok(cond, msg)

    # 1) contraste dos dois temas
    for nome, tema in (("claro", _CLARO), ("escuro", _ESCURO)):
        for k, v in tema.items():
            if k == "FUNDO":
                continue
            minimo = 7.0 if k == "TEXTO" else 3.0
            T(contraste(v, tema["FUNDO"]) >= minimo, "contraste %s/%s = %.2f < %.1f" % (nome, k, contraste(v, tema["FUNDO"]), minimo))

    # 2) zonas
    T(not cruza(PALCO, ROSTO), "palco e rosto não podem se cruzar")
    T(not cruza(PALCO, FAIXA), "palco e faixa não podem se cruzar")
    T(not cruza(ROSTO, FAIXA), "rosto e faixa não podem se cruzar")
    T(dentro(ROSTO, (-4.5, 4.5, -8, 8)) and dentro(PALCO, (-4.5, 4.5, -8, 8)), "zonas dentro do quadro 9x16")
    T(PALCO[3] <= 5.7 + 1e-9, "acima de +5,7 ficam as abas do TikTok")
    T(FAIXA[1] <= 2.9, "faixa não invade os botões (x > +2,9)")
    T(FAIXA[2] >= -4.7, "faixa não invade a legenda (y < −4,7)")
    T(dentro((MARCA[0] - 0.75, MARCA[0] + 0.75, MARCA[1] - 0.15, MARCA[1] + 0.15), FAIXA), "marca d'água dentro da faixa")
    T(ROT_Y[0] + 0.3 <= FAIXA[3] and ROT_Y[-1] - 0.3 >= FAIXA[2] + 0.5, "roteiro cabe na faixa (acima da marca)")
    T(X_ROT >= FAIXA[0] and X_ROT + ROT_LARG <= FAIXA[1] + 1e-9, "largura do roteiro dentro da faixa")

    # 3) matemática
    T(p(1) == 0, "p(1) deve ser 0")
    T(p(3) == 0 and p(4) == 0, "3 e 4 também são raízes")
    T(RES == [1, -7, 12, 0], "Briot-Ruffini com raiz 1 deve dar 1, −7, 12, 0 (deu %s)" % RES)
    T(PROD == [None, 1, -7, 12], "produtos do dispositivo: 1, −7, 12 (deu %s)" % PROD)
    T(RESTO == 0, "resto do dispositivo deve ser 0")
    T(QUAD == [1, -7, 12], "novo polinômio x² − 7x + 12")
    T(7 == -QUAD[1] and 12 == QUAD[2] and 3 + 4 == 7 and 3 * 4 == 12, "soma 7 e produto 12 → 3 e 4")
    T(sorted(RAIZES) == [1, 3, 4] and all(p(r) == 0 for r in RAIZES), "raízes 1, 3 e 4")
    T(SOMA_QUAD == 1 + 9 + 16 == 26, "soma dos quadrados = 26")
    e1, e2 = sum(RAIZES), 1 * 3 + 1 * 4 + 3 * 4
    T(e1 == 8 and e2 == 19 and 1 * 3 * 4 == 12, "Vieta: 8, 19, 12 (coeficientes de p)")
    T(e1 * e1 - 2 * e2 == 26, "conferência por Vieta: 8² − 2·19 = 26")
    T(QUADRADO_DA_SOMA == 64 and 1 + 3 + 4 == 8, "pegadinha: (1+3+4)² = 64")
    T(dict(ALTERNATIVAS)["C"] == 26 and GABARITO == "C", "gabarito: letra C = 26")
    T(dict(ALTERNATIVAS)["E"] == 64, "alternativa E = 64 (o quadrado da soma)")
    T((10 == 9 + 1) and (10 + 16 == 26), "conta da fala: 9 + 1 = 10; 10 + 16 = 26")
    T((1 - 8 + 19 - 12 == 0) and (1 + 19 == 20) and (-8 - 12 == -20), "conta da fala: 1+19=20; −8−12=−20; 20−20=0")

    # 4) enunciado integral recomposto
    c = melhor_composicao()
    T(c is not None, "enunciado não coube")
    if c:
        T(c["s"] >= FONTE_MIN, "fonte do enunciado %.3f < mínimo %.2f — avisar o professor (opções a/b/c)" % (c["s"], FONTE_MIN))
        rec = texto_recomposto(c).replace(NB, " ").replace("   ", " ")
        rec = " ".join(rec.split())
        T(rec == TRANSCRICAO, "texto recomposto difere da transcrição:\n   %r\n   %r" % (rec, TRANSCRICAO))
        T(c["largura"] <= BOX_ENUNCIADO[0] + 1e-9 and c["altura"] <= BOX_ENUNCIADO[1] + 1e-9, "enunciado fora da caixa")
        T(dentro((-c["largura"] / 2, c["largura"] / 2, PALCO[2], PALCO[2] + c["altura"]), (PALCO[0], PALCO[1], PALCO[2], PALCO[3] + 10)), "enunciado mais largo que o palco")
        T(all(len(l["cum_fim"]) == len(l["palavras"]) for l in c["linhas"]), "marcos de palavra por linha")
    for fmt in ("linha", "lista"):
        T(melhor_composicao(fmt) is not None, "formato %s não coube" % fmt)
    for nome, txt in TEXTOS.items():
        for sub in txt.split("\n"):
            try:
                larg_em(sub.replace("º", "o"))
            except ValueError as e:
                T(False, "TEXTOS[%s]: %s" % (nome, e))
    T(True, "")

    # 5) fórmulas: peças somam a expressão esperada
    T("".join(F["px"]) == "p(x)=x^3-8x^2+19x-12", "F['px'] não reconstrói p(x)")
    T("".join(F["t1"]) == "p(1)=1-8+19-12", "F['t1'] não reconstrói p(1) = 1 − 8 + 19 − 12")
    T("".join(F["q"]) == "q(x)=x^2-7x+12=0", "F['q']")
    T("".join(F["E1"]) == "S=1^2+3^2+4^2" and "".join(F["E2"]) == "=1+9+16" and "".join(F["E3"]) == "=10+16=26", "F['E*']")
    T("".join(F["errada"]).replace("{}", "") == "(1+3+4)^2=8^2=64", "F['errada']")
    T(len(F["rot_pend"]) == len(F["rot_ok"]) == len(ROT_Y), "roteiro: itens x posições")

    # 6) layout do dispositivo
    T(all(PALCO[0] < x < PALCO[1] for x in COL_X + (X_RAIZ, X_BARRA, X_FIM)), "dispositivo dentro do palco (x)")
    T(all(COL_X[i + 1] - COL_X[i] >= 1.0 for i in range(3)), "colunas do dispositivo com folga (≥ 1,0)")
    T(Y_PROD > Y_TRACO > Y_RES and Y_BARRA[0] > Y_COEF and Y_BARRA[1] < Y_RES, "ordem vertical do dispositivo")
    T(Y_COEF - Y_PROD >= 0.6 and Y_TRACO - Y_RES >= 0.35, "linhas do dispositivo sem sobreposição")
    T(Y_BARRA[1] - (Y_QLINHA + 0.45) >= 0.15, "linha do novo polinômio abaixo do dispositivo")
    T(X_CAP - 1.1 > X_FIM, "coluna de legendas à direita do dispositivo")
    T(Y_CAB - 0.35 > Y_TITULO + 0.25 and Y_CAB + 0.4 <= PALCO[3], "cabeçalho acima do título e dentro do palco")
    T(Y_ERR - 0.4 >= PALCO[2] and Y_E3 - Y_ERR >= 0.8, "linha da pegadinha cabe abaixo da soma dos quadrados")
    T(Y_ALT - 4 * DY_ALT - 0.25 > POS_LBL_QUAD[1] + 0.4, "lista de alternativas não encosta no rótulo 'quadrado da soma'")
    T(ESQ_E - 0.45 >= PALCO[0], "espaço para as plaquinhas 1º/2º")

    if verbose:
        if c:
            print("enunciado: formato=%s  fonte=%.3f u/em  caixa=%.2f x %.2f u (%.0f%% da largura do palco)  linhas=%d"
                  % (c["formato"], c["s"], c["largura"], c["altura"], 100 * c["largura"] / (PALCO[1] - PALCO[0]), len(c["linhas"])))
            for l in c["linhas"]:
                print("   [%-12s] %s" % (l["tipo"], l["texto"].replace(NB, "·")))
        print("%d testes, %d falha(s)" % (n, len(_falhas)))
    return not _falhas


if __name__ == "__main__":
    sys.exit(0 if testes() else 1)
