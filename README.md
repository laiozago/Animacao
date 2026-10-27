# Projetos

Esta pasta reune as animacoes em Manim usadas nos videos. Cada animacao fica em seu proprio diretorio.

## Animacoes

| Pasta | Cena(s) / video(s) |
|---|---|
| `a_origem_do_pi` | OrigemDoPi |
| `area_circulo` | AreaCirculoCebola |
| `circulo_trigonometrico` | SenoCossenoAnimacao (ver README da pasta) |
| `construcao_do_retangulo` | RetanguloDePrata |
| `dança_da_parabola` | DancaParabola |
| `desafio` | DesafioGeometria (ver README da pasta) |
| `especex_2025_q18` | PrismaHexagonal |
| `especex_2025_q19` | Questao19 |
| `grafico_pism1` | graficos (grafico_1, questao_4) |
| `pism_2025_q18` | QuestaoPism18 |
| `planificacoes` | Planificacao de solidos (ver README da pasta) |
| `protetor_de_conteudo` | MarcaAguaQuicando |
| `quadrado_da_soma` | ProdutoNotavel |
| `questao_piramide` | ResolucaoPiramide (ver README da pasta) |
| `soma_fracoes` | SomaFracoes |

## Ambiente Python

Ha um unico ambiente virtual (`.venv`) e uma unica lista de dependencias (`requirements.txt`), ambos na raiz. Requer Python 3.13. No PowerShell, a partir desta pasta, configure uma vez:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Ative `.venv` antes de renderizar qualquer animacao. Nao crie outro `.venv` dentro das subpastas.

## Estrutura

```text
animacao/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- .venv/                (unico, ignorado pelo Git)
|-- <nome_da_animacao>/
|   |-- <script>.py
|   |-- README.md         (opcional, detalhes da animacao)
|   `-- media/            (saida dos videos, ignorada pelo Git)
`-- _lixo/                (temporario: apague quando quiser)
```

Ao adicionar uma animacao, crie um novo diretorio para ela.

## Saida dos videos

Cada script Manim deve salvar os resultados em uma pasta `media/` ao lado do proprio arquivo `.py`. Defina o destino no inicio do script, logo apos os imports:

```python
from pathlib import Path
from manim import *

config.media_dir = str(Path(__file__).resolve().parent / "media")
```

Assim, tanto a CLI do Manim quanto a execucao direta do script gravam videos, imagens e arquivos intermediarios no projeto correto, independentemente da pasta de onde o comando foi executado. Nao passe outro destino com `--media_dir`. As pastas `media/` e `__pycache__/` sao ignoradas pelo Git.

## Licenca

Salvo indicacao diferente no README ou em uma licenca dentro do proprio projeto, os projetos deste repositorio estao sob a GNU General Public License v3.0 (GPL-3.0). Consulte [LICENSE](LICENSE).
