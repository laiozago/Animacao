# -*- coding: utf-8 -*-
"""
PISM II 2026 - Questão 13 (cone de areia ÷ barril cilíndrico) - @proflaiozago

Dados da questão, tema, zonas do layout, geometria 2D das figuras, fórmulas em
LaTeX (uma fonte só) e TESTES. NÃO importa Manim:  python3 geometria.py
"""
from fractions import Fraction as Fr

# ------------------------------------------------------------------ questão
R_CONE_M = 5            # raio do cone (m)
H_CONE_M = 3            # altura do cone (m)
D_BARRIL_M = 1          # diâmetro do barril (m)
H_BARRIL_CM = 80        # altura do barril (cm)
ALTERNATIVAS = [("A", "19"), ("B", "32"), ("C", "125"), ("D", "375"), ("E", r"1\,125")]
LETRA = "C"


def vol_cone_pi():
    """Volume do cone em múltiplos de pi (m³): 1/3 · 5² · 3."""
    return Fr(1, 3) * R_CONE_M ** 2 * H_CONE_M


def vol_barril_pi():
    """Volume do barril em múltiplos de pi (m³): (1/2)² · 4/5."""
    r = Fr(D_BARRIL_M, 2)
    h = Fr(H_BARRIL_CM, 100)
    return r * r * h


def n_barris():
    return vol_cone_pi() / vol_barril_pi()


# --------------------------------------------------------------------- tema
TEMA = "claro"          # "claro" (padrão) ou "escuro"
PALETAS = {
    "claro": dict(FUNDO="#FFFFFF", TEXTO="#111111", CINZA="#7A7A7A", AZUL="#1565C0",
                  AMARELO="#B87D00", VERMELHO="#D32F2F", VERDE="#2E7D32", LARANJA="#E65100"),
    "escuro": dict(FUNDO="#0B0B0F", TEXTO="#F2F2F2", CINZA="#9A9A9A", AZUL="#64B5F6",
                   AMARELO="#FFD54F", VERMELHO="#FF6B6B", VERDE="#66BB6A", LARANJA="#FFA040"),
}
# Neste vídeo: AZUL = raio · AMARELO = altura / regra · LARANJA = diâmetro, conversão e
# cancelamento (alerta) · VERMELHO = falta descobrir · VERDE = resolvido · CINZA = contexto
COR = PALETAS[TEMA]
FUNDO, TEXTO, CINZA, AZUL = COR["FUNDO"], COR["TEXTO"], COR["CINZA"], COR["AZUL"]
AMARELO, VERMELHO, VERDE, LARANJA = COR["AMARELO"], COR["VERMELHO"], COR["VERDE"], COR["LARANJA"]

# ------------------------------------------------------------ zonas (x0,y0,x1,y1)
# Layout padronizado na Q19 v2: rosto no meio-esquerda (quadro 9 x 16, x ±4,5; y ±8)
PALCO = (-4.1, 0.4, 4.1, 5.7)
ROSTO = (-4.1, -4.6, 0.6, 0.1)
FAIXA = (0.8, -4.6, 2.8, 0.1)
FIGURAS = (-4.1, 0.5, -1.0, 5.6)     # coluna das figuras (esquerda do palco)
PAINEL = (-0.9, 0.5, 4.05, 5.6)      # coluna das contas (direita do palco)
MARCA = (1.85, -4.4)
EVITAR_BOTOES = (2.9, -8.0, 4.5, 0.1)   # x > 2,9 abaixo de y = 0,1
EVITAR_LEGENDA = (-4.5, -8.0, 4.5, -4.7)  # y < -4,7
ROT_X = 0.85                          # borda esquerda do roteiro
ROT_Y = {"n": -0.5, "vcone": -1.3, "vbarril": -2.1}

# linhas do painel (y do centro)
Y_N = 5.25
Y_REGRA, Y_REGRA_ROT = 4.6, 3.98
Y_CONE = [3.3, 2.5]                  # conta do cone (2 linhas)
Y_BARRIL = [3.23, 2.17, 1.3]         # conta do barril (3 linhas; a 1ª tem parênteses altos)
Y_DIV = [3.7, 2.75, 2.0]             # divisão final (alturas medidas em LaTeX: teste_latex.py)
Y_ALT = [4.8, 4.0, 3.2, 2.4, 1.6]    # alternativas
X_REGRA = (0.3, 2.9)                 # centros das duas células de regra
LARG_REGRA = (2.27, 1.72)            # larguras medidas em LaTeX (escala 0,75), ver teste_latex.py
X_CONTA = -0.75                      # borda esquerda das contas
X_ALT = 0.7
# escalas do MathTex (font_size 48 · escala); medidas em LaTeX para caber nas colunas
ESC = dict(conta=0.85, regra=0.75, div=0.9, alt=0.95, rot=0.75, rotulo=0.65, r_barril=0.55)

# --------------------------------------------- figuras 2D (cone e barril, fora de escala)
CONE = dict(apice=(-2.7, 5.4), centro=(-2.7, 3.65), rx=1.05, ry=0.28)
BARRIL = dict(cx=-3.2, y_topo=2.05, y_base=0.85, rx=0.5, ry=0.17)
X_COTA_BARRIL = -2.5                 # linha de cota da altura do barril
# caixas (x0,y0,x1,y1) das figuras e dos rótulos, para o teste de sobreposição
CAIXAS = {
    "cone": (-3.75, 3.37, -1.65, 5.4),
    "barril": (-3.7, 0.68, -2.7, 2.22),
    "cota_barril": (-2.55, 0.85, -2.45, 2.05),
    "r_cone": (-2.3, 2.95, -1.7, 3.25),
    "h_cone": (-2.65, 4.0, -2.1, 4.3),
    "d": (-3.8, 2.4, -2.6, 2.7),
    "r_barril": (-3.65, 1.3, -2.75, 1.6),
    "h_barril": (-2.25, 1.3, -1.25, 1.6),
}
POS = {
    "r_cone": (-2.0, 3.1), "h_cone": (-2.38, 4.15), "d": (-3.2, 2.55),
    "r_barril": (-3.2, 1.45), "h_barril": (-1.75, 1.45),
}

# ------------------------------------------------------ fórmulas (cada parte é LaTeX válido sozinha)
M3 = r"\ \mathrm{m}^{3}"
LINHAS = {
    "n": [r"N", r"=", r"V_{cone}", r"\div", r"V_{barril}"],
    "regra_cone": [r"V=", r"\frac{1}{3}", r"\cdot A_b", r"\cdot h"],
    "regra_cil": [r"V=", r"A_b", r"\cdot h"],
    "cone1": [r"V_{cone}", r"=", r"\frac{1}{3}", r"\cdot\pi", r"\cdot 5^{2}", r"\cdot 3"],
    "cone2": [r"=25", r"\pi", M3],
    "barril1": [r"V_{barril}", r"=", r"\pi", r"\cdot\left(\frac{1}{2}\right)^{2}", r"\cdot\frac{4}{5}"],
    "barril2": [r"=\pi", r"\cdot\frac{1}{4}", r"\cdot\frac{4}{5}"],
    "barril3": [r"=\frac{\pi}{5}", M3],
    "div1": [r"N", r"=", r"25\pi", r"\div", r"\frac{\pi}{5}"],
    "div2": [r"=25\pi", r"\cdot\frac{5}{\pi}"],
    "div3": [r"=125", r"\ \text{barris}"],
}
ROTULOS = {
    "r_cone": r"5\ \mathrm{m}", "h_cone": r"3\ \mathrm{m}", "d": r"d=1\ \mathrm{m}",
    "r_seq": [r"r=?", r"r=0{,}5", r"r=\frac{1}{2}"],
    "h_seq": [r"80\ \mathrm{cm}", r"0{,}8\ \mathrm{m}", r"\frac{8}{10}\ \mathrm{m}", r"\frac{4}{5}\ \mathrm{m}"],
    "rot": {
        "n": (r"N=?", r"N=125"),
        "vcone": (r"V_{cone}=?", r"V_{cone}=25\pi"),
        "vbarril": (r"V_{barril}=?", r"V_{barril}=\frac{\pi}{5}"),
    },
}
ROTULO_REGRA = ("corpo piramidal", "chão = teto")
# ------------------------------------------------------------------ abertura: enunciado integral
# PADRÃO: o texto INTEGRAL da prova (palavra por palavra, com título e alternativas), digitado aqui e
# RECOMPOSTO para usar toda a largura do palco com a maior fonte que couber. Nada de resumir ("mastigar").
# Use ESPAÇO SEM QUEBRA (\u00a0) entre número e unidade ("5\u00a0m") para a linha não quebrar ali.
ENUNCIADO = dict(
    titulo="QUESTÃO 13.",
    paragrafos=[
        "Após a realização de uma obra, a areia que sobrou ficou empilhada, em formato de um cone "
        "circular reto cujo raio da base mede 5\u00a0m e, cuja altura, mede 3\u00a0m. Essa areia será "
        "armazenada em barris de formato cilíndrico cujas bases possuem diâmetro medindo 1\u00a0m e "
        "altura medindo 80\u00a0cm.",
        "Qual é a quantidade mínima de barris que serão utilizados para armazenar toda essa areia?",
    ],
)
BOX_ENUNCIADO = (7.6, 5.0)           # largura x altura máximas do texto no palco (palco: 8,2 x 5,3)
PASSO_LINHA = 1.32                   # distância entre linhas, em em
ESPACO_ENTRE = 0.55                  # espaço extra antes de cada bloco (parágrafo, alternativas), em em
FORMATO_ALTERNATIVAS = "auto"        # "auto" = o que dá a maior fonte · "lista" (uma por linha, como na prova) · "linha"
FONTE_ENUNCIADO = "Arial"            # mesma família da prova (se faltar, o Pango usa outra e a base reajusta)

# larguras (por 1000 em) da Helvetica/Arial: dispensa PIL e fontes; letra acentuada = letra base
_AFM = {" ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 191, "(": 333, ")": 333,
        "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278, ":": 278, ";": 278, "<": 584, "=": 584,
        ">": 584, "?": 556, "@": 1015, "[": 278, "\\": 278, "]": 278, "^": 469, "_": 556, "`": 333, "{": 334,
        "|": 260, "}": 334, "~": 584, "\u00a0": 278}
_AFM.update({c: 556 for c in "0123456789"})
_AFM.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833,
                                                722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_AFM.update(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833,
                                                556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))


def largura_em(texto, negrito=False):
    """Largura estimada do texto, em em (erro < 1% contra a Liberation Sans, que tem a métrica do Arial)."""
    import unicodedata
    w = sum(_AFM.get(unicodedata.normalize("NFD", c)[0], 556) for c in texto) / 1000.0
    return w * (1.06 if negrito else 1.0)


def quebra(texto, larg_em):
    """Quebra gulosa em linhas de até larg_em (só nos espaços normais; \u00a0 gruda as palavras)."""
    linhas, atual = [], ""
    for pal in texto.split(" "):
        tent = pal if not atual else atual + " " + pal
        if atual and largura_em(tent) > larg_em:
            linhas.append(atual)
            atual = pal
        else:
            atual = tent
    return linhas + [atual]


def _alt_texto():
    return [("(%s)\u00a0%s" % (l, v.replace("\\,", "\u00a0"))) for l, v in ALTERNATIVAS]


def compoe_enunciado(larg_em, alternativas):
    """Monta as linhas do enunciado para uma largura de quebra. `alternativas` = "lista" (uma por linha,
    como na prova) ou "linha" (todas numa linha só). Devolve (linhas, largura_max_em, altura_em);
    linhas = [(texto, negrito, y_em)] com y descendo a partir de 0."""
    itens = [(ENUNCIADO["titulo"], True, 0.0)]
    for p in ENUNCIADO["paragrafos"]:
        for i, l in enumerate(quebra(p, larg_em)):
            itens.append((l, False, ESPACO_ENTRE if i == 0 else 0.0))
    alts = _alt_texto()
    if alternativas == "lista":
        itens += [(a, False, ESPACO_ENTRE if i == 0 else 0.0) for i, a in enumerate(alts)]
    else:
        itens.append(("    ".join(alts), False, ESPACO_ENTRE))
    y, linhas = 0.0, []
    for k, (t, neg, antes) in enumerate(itens):
        y += (PASSO_LINHA if k else 0.0) + antes
        linhas.append((t, neg, y))
    return linhas, max(largura_em(t, n) for t, n, _ in linhas), y + 1.0


def melhor_composicao(formato=None):
    """Procura a largura de quebra (e, em "auto", o formato das alternativas) que dão a MAIOR fonte no
    BOX_ENUNCIADO. Devolve dict(linhas, em_u (unidades por em), larg_em, altura_em, alternativas, larg_u, alt_u)."""
    formato = formato or FORMATO_ALTERNATIVAS
    melhor = None
    for alt in (("linha", "lista") if formato == "auto" else (formato,)):
        for i in range(160, 520):
            linhas, wmax, h = compoe_enunciado(i / 10.0, alt)
            em_u = min(BOX_ENUNCIADO[0] / wmax, BOX_ENUNCIADO[1] / h)
            if melhor is None or em_u > melhor["em_u"] + 1e-9:
                melhor = dict(linhas=linhas, em_u=em_u, larg_em=wmax, altura_em=h, alternativas=alt,
                              larg_u=wmax * em_u, alt_u=h * em_u)
    return melhor


def todas_as_formulas():
    """Todas as strings LaTeX (cada parte e cada linha inteira) para o teste de compilação."""
    out = []
    for partes in LINHAS.values():
        out += partes + [" ".join(partes)]
    for k in ("r_cone", "h_cone", "d"):
        out.append(ROTULOS[k])
    out += ROTULOS["r_seq"] + ROTULOS["h_seq"]
    for q, ok in ROTULOS["rot"].values():
        out += [q, ok]
    for letra, val in ALTERNATIVAS:
        out += [r"\text{(%s)}" % letra, r"\ " + val]
    return out


# ===================================================================== testes
def _lum(hexcor):
    r, g, b = (int(hexcor[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _inter(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def _dentro(a, b):
    return a[0] >= b[0] and a[1] >= b[1] and a[2] <= b[2] and a[3] <= b[3]


def testes():
    ok = []

    def ck(nome, cond):
        assert cond, "FALHOU: " + nome
        ok.append(nome)

    # matemática
    ck("V_cone = 25 pi", vol_cone_pi() == 25)
    ck("V_barril = pi/5", vol_barril_pi() == Fr(1, 5))
    ck("altura do barril = 4/5 m", Fr(H_BARRIL_CM, 100) == Fr(4, 5) == Fr(8, 10))
    ck("raio do barril = 1/2 = 0,5", Fr(D_BARRIL_M, 2) == Fr(1, 2) == Fr(5, 10))
    ck("N = 125 (inteiro, então o mínimo é 125)", n_barris() == 125 and n_barris().denominator == 1)
    ck("125 está na letra C", dict(ALTERNATIVAS)[LETRA] == "125")
    ck("25 pi · 5/pi = 125", Fr(25) * 5 == 125)
    ck("1/4 · 4/5 = 1/5", Fr(1, 4) * Fr(4, 5) == Fr(1, 5))
    # contraste (as duas paletas)
    for tema, p in PALETAS.items():
        for nome, c in p.items():
            if nome == "FUNDO":
                continue
            minimo = 7.0 if nome == "TEXTO" else 3.0
            ck("contraste %s/%s >= %.0f" % (tema, nome, minimo), contraste(c, p["FUNDO"]) >= minimo)
    # zonas
    ck("palco acima do rosto", PALCO[1] > ROSTO[3])
    ck("rosto e faixa não se cruzam", not _inter(ROSTO, FAIXA))
    ck("faixa não invade os botões", not _inter(FAIXA, EVITAR_BOTOES) or FAIXA[2] <= EVITAR_BOTOES[0])
    ck("faixa e rosto fora da legenda", not _inter(FAIXA, EVITAR_LEGENDA) and not _inter(ROSTO, EVITAR_LEGENDA))
    ck("marca d'água dentro da faixa", FAIXA[0] <= MARCA[0] <= FAIXA[2] and FAIXA[1] <= MARCA[1] <= FAIXA[3])
    ck("roteiro dentro da faixa", all(FAIXA[1] <= y <= FAIXA[3] for y in ROT_Y.values()) and ROT_X >= FAIXA[0])
    ck("figuras e painel dentro do palco", _dentro(FIGURAS, PALCO) and _dentro(PAINEL, PALCO))
    ck("figuras e painel não se cruzam", not _inter(FIGURAS, PAINEL))
    # figuras
    for nome, c in CAIXAS.items():
        ck("caixa '%s' dentro da coluna das figuras" % nome, _dentro(c, FIGURAS))
    # rótulos que ficam DENTRO da figura (de propósito): têm de estar contidos nela
    dentro_de = {"h_cone": "cone", "r_barril": "barril"}
    for rot, fig in dentro_de.items():
        ck("rótulo '%s' contido em '%s'" % (rot, fig), _dentro(CAIXAS[rot], CAIXAS[fig]))
    nomes = list(CAIXAS)
    for i, a in enumerate(nomes):
        for b in nomes[i + 1:]:
            if dentro_de.get(a) == b or dentro_de.get(b) == a:
                continue
            ck("sem sobreposição %s x %s" % (a, b), not _inter(CAIXAS[a], CAIXAS[b]))
    ck("barril cabe sob o cone", CAIXAS["barril"][3] < CAIXAS["cone"][1])
    ck("rótulos nas posições das caixas",
       all(CAIXAS[k][0] <= x <= CAIXAS[k][2] and CAIXAS[k][1] <= y <= CAIXAS[k][3] for k, (x, y) in POS.items()))
    ck("cota do barril na caixa", CAIXAS["cota_barril"][0] <= X_COTA_BARRIL <= CAIXAS["cota_barril"][2])
    ck("barril bate com a caixa",
       abs(BARRIL["cx"] - BARRIL["rx"] - CAIXAS["barril"][0]) < 1e-9
       and abs(BARRIL["cx"] + BARRIL["rx"] - CAIXAS["barril"][2]) < 1e-9)
    ck("cone bate com a caixa",
       abs(CONE["centro"][0] - CONE["rx"] - CAIXAS["cone"][0]) < 1e-9
       and abs(CONE["centro"][1] - CONE["ry"] - CAIXAS["cone"][1]) < 1e-9
       and abs(CONE["apice"][1] - CAIXAS["cone"][3]) < 1e-9)
    # painel (linhas) dentro do painel e com espaço entre si
    todas_y = [Y_N, Y_REGRA, Y_REGRA_ROT] + Y_CONE + Y_BARRIL + Y_DIV + Y_ALT
    ck("linhas dentro do painel", all(PAINEL[1] + 0.25 <= y <= PAINEL[3] - 0.1 for y in todas_y))
    ck("N acima das regras, regras acima dos rótulos, rótulos acima das contas",
       Y_N > Y_REGRA > Y_REGRA_ROT > Y_CONE[0] and Y_REGRA_ROT > Y_BARRIL[0])
    ck("linhas de cada conta em ordem decrescente",
       all(a > b for L in (Y_CONE, Y_BARRIL, Y_DIV) for a, b in zip(L, L[1:])))
    ck("divisão abaixo do N", Y_DIV[0] < Y_N - 0.6)
    ck("alternativas com passo >= 0,6", all(a - b >= 0.6 for a, b in zip(Y_ALT, Y_ALT[1:])))
    # enunciado integral recomposto
    comp = melhor_composicao()
    pars = [" ".join(p.split()) for p in ENUNCIADO["paragrafos"]]
    corpo = " ".join(t.replace("\u00a0", " ") for t, n, _ in comp["linhas"][1:])
    esperado = " ".join(pars) + " " + " ".join(a.replace("\u00a0", " ") for a in _alt_texto())
    ck("enunciado recomposto tem TODO o texto, na ordem (nada resumido)",
       " ".join(corpo.split()) == " ".join(esperado.split()))
    ck("título da prova preservado", comp["linhas"][0][0] == ENUNCIADO["titulo"])
    ck("enunciado cabe no palco (%.2f x %.2f u)" % (comp["larg_u"], comp["alt_u"]),
       comp["larg_u"] <= BOX_ENUNCIADO[0] + 1e-6 and comp["alt_u"] <= BOX_ENUNCIADO[1] + 1e-6
       and BOX_ENUNCIADO[0] <= PALCO[2] - PALCO[0] and BOX_ENUNCIADO[1] <= PALCO[3] - PALCO[1])
    ck("enunciado usa mais de 90%% da largura do palco (%.0f%%)" % (100 * comp["larg_u"] / (PALCO[2] - PALCO[0])),
       comp["larg_u"] >= 0.9 * (PALCO[2] - PALCO[0]))
    ck("fonte do enunciado >= 0,22 u por em (o print antigo tinha 0,17)", comp["em_u"] >= 0.22)
    ck("palco e faixa são caixas separadas (nenhuma moldura une as duas)", not _inter(PALCO, FAIXA))
    c1, c2 = X_REGRA
    w1, w2 = LARG_REGRA
    ck("regras cabem lado a lado, dentro do painel",
       c1 - w1 / 2 >= PAINEL[0] and c1 + w1 / 2 + 0.3 <= c2 - w2 / 2 and c2 + w2 / 2 <= PAINEL[2])
    ck("5 alternativas, uma por letra", [a for a, _ in ALTERNATIVAS] == list("ABCDE"))
    ck("fórmulas: nenhuma chave desbalanceada",
       all(s.count("{") == s.count("}") for s in todas_as_formulas()))
    print("OK - %d testes passaram" % len(ok))
    return True


if __name__ == "__main__":
    testes()
