"""Geometria pura (sem Manim) da questão do prisma hexagonal.

Tudo que a cena precisa saber sobre a figura mora aqui, para poder ser
testado sem renderizar nada:  python3 geometria.py
"""
import numpy as np

# ---- dados da questão -------------------------------------------------------
H = 12.0                       # altura do prisma (cm)
ANGULO_DM = np.radians(60.0)   # ângulo de DM com o plano da base
PROJECAO = H / np.tan(ANGULO_DM)   # projeção de DM na base = 4*sqrt(3)
LADO = PROJECAO / 2.0              # diagonal maior = 2a  ->  a = 2*sqrt(3)

# índices dos vértices (hexágono com vértices em 0°, 60°, ... 300°):
#   k=2 -> "D" (em cima)   k=5 -> "M" (embaixo)   -> são vértices OPOSTOS
K_D = 2
K_M = 5

# ---- paleta (hex) -----------------------------------------------------------
# "claro": fundo branco, para sobrepor à folha da questão (cores mais escuras
#          para ter contraste no branco).  "escuro": a versão original.
# Se o branco da folha for um pouco diferente, ajuste FUNDO em "claro" com o
# conta-gotas do CapCut.
TEMA = "claro"

_TEMAS = {
    "escuro": dict(
        FUNDO="#0E1117",
        AZUL="#4FC3F7",      # x
        AMARELO="#FFD54A",   # x*sqrt(3)
        VERMELHO="#FF5252",  # 2x / "falta descobrir"
        VERDE="#5CE08A",     # "já resolvido"
        LARANJA="#FF9F43",   # base do prisma
        CINZA="#DDDDDD",     # texto e arestas
        PALETA6=["#4FC3F7", "#FFD54A", "#FF7A7A", "#5CE08A", "#B388FF", "#FF9F43"],
    ),
    "claro": dict(
        FUNDO="#FFFFFF",
        AZUL="#0277BD",
        AMARELO="#A67C00",
        VERMELHO="#D32F2F",
        VERDE="#178A45",
        LARANJA="#D35400",
        CINZA="#1F2933",
        PALETA6=["#0277BD", "#E0A800", "#E53935", "#178A45", "#7E57C2", "#E65100"],
    ),
}
_P = _TEMAS[TEMA]
FUNDO = _P["FUNDO"]
AZUL = _P["AZUL"]
AMARELO = _P["AMARELO"]
VERMELHO = _P["VERMELHO"]
VERDE = _P["VERDE"]
LARANJA = _P["LARANJA"]
CINZA = _P["CINZA"]
PALETA6 = _P["PALETA6"]


def contraste(c1, c2):
    """Razão de contraste WCAG entre duas cores '#RRGGBB' (1 a 21)."""
    def lum(c):
        v = [int(c[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def mistura(c1, c2, t):
    """Interpola duas cores '#RRGGBB'."""
    t = float(min(1.0, max(0.0, t)))
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    r = [round(a[i] * (1 - t) + b[i] * t) for i in range(3)]
    return "#%02X%02X%02X" % tuple(r)


def vertice(k, z=0.0):
    ang = np.radians(60.0 * k)
    return np.array([LADO * np.cos(ang), LADO * np.sin(ang), z])


def profundidade(p, yaw):
    """Coordenada de profundidade (maior = mais ao fundo)."""
    return p[0] * np.sin(yaw) + p[1] * np.cos(yaw)


def projeta(p, yaw, elev, escala, ox, oy):
    """Projeção do ponto 3D (cm) na tela (unidades do Manim).

    yaw  = giro do prisma em torno do eixo vertical
    elev = elevação da câmera (0 = vista lateral, pi/2 = vista de cima)
    """
    x, y, z = p[0], p[1], p[2] - H / 2.0
    xr = x * np.cos(yaw) - y * np.sin(yaw)
    yr = x * np.sin(yaw) + y * np.cos(yaw)
    sy = z * np.cos(elev) + yr * np.sin(elev)
    return np.array([ox + escala * xr, oy + escala * sy, 0.0])


# ---- arestas e visibilidade -------------------------------------------------
# Faces: "T" (topo), "B" (base) e 0..5 (laterais). A lateral k liga os vértices
# k e k+1 e tem a normal apontando para 60*k + 30 graus.
def _monta_arestas():
    """As 18 arestas como (ponta1, ponta2, (face_vizinha_1, face_vizinha_2))."""
    lista = []
    for k in range(6):                                   # 6 arestas do topo
        lista.append((vertice(k, H), vertice((k + 1) % 6, H), ("T", k)))
    for k in range(6):                                   # 6 arestas da base
        lista.append((vertice(k), vertice((k + 1) % 6), ("B", k)))
    for k in range(6):                                   # 6 arestas verticais
        lista.append((vertice(k), vertice(k, H), ((k - 1) % 6, k)))
    return lista


ARESTAS = _monta_arestas()


def face_frontal(face, yaw, elev, tol=1e-9):
    """True se a face está virada para a câmera (câmera acima: elev >= 0).

    A câmera olha de -y (frente) e de +z (cima), no referencial já girado
    pelo yaw; a face é frontal quando (normal . direção_da_câmera) > 0.
    """
    if face == "T":
        return np.sin(elev) > tol
    if face == "B":
        return -np.sin(elev) > tol
    normal = np.radians(60.0 * face + 30.0)
    return -np.cos(elev) * np.sin(normal + yaw) > tol


def aresta_visivel(faces, yaw, elev):
    """A aresta aparece contínua se alguma das 2 faces vizinhas está de frente."""
    return any(face_frontal(f, yaw, elev) for f in faces)


# ---- testes -----------------------------------------------------------------
def _testes():
    # 1) D e M são vértices opostos: a projeção de DM é a diagonal maior (2a)
    d_base, m_base = vertice(K_D), vertice(K_M)
    assert abs(np.linalg.norm(m_base - d_base) - 2 * LADO) < 1e-9

    # 2) o ângulo entre DM e a base mede mesmo 60°
    d_topo = vertice(K_D, H)
    dm = vertice(K_M) - d_topo
    ang = np.degrees(np.arctan2(abs(dm[2]), np.hypot(dm[0], dm[1])))
    assert abs(ang - 60.0) < 1e-9, ang

    # 3) triângulo 30-60-90: x, x*sqrt(3), 2x
    x = np.linalg.norm(m_base - d_base)
    assert abs(x - 4 * np.sqrt(3)) < 1e-9
    assert abs(H - x * np.sqrt(3)) < 1e-9              # DD' = x*sqrt(3) = 12
    assert abs(np.linalg.norm(dm) - 2 * x) < 1e-9

    # 4) lado, área da base e volume
    assert abs(LADO - 2 * np.sqrt(3)) < 1e-9
    area_tri = LADO ** 2 * np.sqrt(3) / 4
    assert abs(area_tri - 3 * np.sqrt(3)) < 1e-9
    area_base = 6 * area_tri
    assert abs(area_base - 18 * np.sqrt(3)) < 1e-9
    assert abs(area_base * H - 216 * np.sqrt(3)) < 1e-9

    # 5) câmera "de frente": yaw=60°, elev=0 deixa D'M horizontal, D acima de D'
    yaw, el = np.radians(60), 0.0
    Dp = projeta(vertice(K_D), yaw, el, 1, 0, 0)
    M = projeta(vertice(K_M), yaw, el, 1, 0, 0)
    D = projeta(vertice(K_D, H), yaw, el, 1, 0, 0)
    assert abs(Dp[1] - M[1]) < 1e-9 and M[0] > Dp[0]
    assert abs(D[0] - Dp[0]) < 1e-9 and D[1] > Dp[1]
    assert abs(M[0] - Dp[0] - 2 * LADO) < 1e-9

    # 6) vista de cima: topo e base coincidem, D'M continua horizontal
    el = np.pi / 2
    Dp = projeta(vertice(K_D), yaw, el, 1, 0, 0)
    D = projeta(vertice(K_D, H), yaw, el, 1, 0, 0)
    M = projeta(vertice(K_M), yaw, el, 1, 0, 0)
    assert np.allclose(Dp, D) and abs(Dp[1] - M[1]) < 1e-9

    # 7) vista inicial (yaw=0): L e R na silhueta, BL e BR ao fundo (tracejados)
    assert abs(profundidade(vertice(3), 0.0)) < 1e-9
    assert abs(profundidade(vertice(0), 0.0)) < 1e-9
    assert profundidade(vertice(1), 0.0) > 0 and profundidade(vertice(2), 0.0) > 0
    assert profundidade(vertice(4), 0.0) < 0 and profundidade(vertice(5), 0.0) < 0

    # 8) arestas: 18 no total e quantas ficam ocultas (tracejadas) em cada vista
    def n_ocultas(yaw_, elev_):
        return sum(not aresta_visivel(f, yaw_, elev_) for _, _, f in ARESTAS)

    assert len(ARESTAS) == 18
    # inicial: 3 da base e 2 verticais ao fundo
    assert n_ocultas(0.0, np.radians(22)) == 5
    # de frente: 3 do topo + 3 da base + 2 verticais ao fundo (no mesmo traço do topo/base)
    assert n_ocultas(np.radians(60), 0.0) == 8
    # de cima: só as 6 arestas do topo aparecem; base e verticais ficam por baixo
    assert n_ocultas(np.radians(60), np.pi / 2) == 12
    # as verticais por D' e por M ficam na silhueta da vista de frente: aparecem
    yf = np.radians(60)
    assert aresta_visivel(((K_D - 1) % 6, K_D), yf, 0.0)
    assert aresta_visivel(((K_M - 1) % 6, K_M), yf, 0.0)

    # 9) legibilidade: nos DOIS temas, cores de destaque >= 3:1 e texto >= 7:1
    for nome, t in _TEMAS.items():
        for cor in ("AZUL", "AMARELO", "VERMELHO", "VERDE", "LARANJA"):
            assert contraste(t[cor], t["FUNDO"]) >= 3.0, (nome, cor)
        assert contraste(t["CINZA"], t["FUNDO"]) >= 7.0, (nome, "CINZA")

    print("geometria OK  (lado=%.4f, 2a=%.4f, V=%.4f = 216*sqrt3=%.4f)"
          % (LADO, 2 * LADO, area_base * H, 216 * np.sqrt(3)))


if __name__ == "__main__":
    _testes()
