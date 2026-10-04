# Planificacoes de solidos geometricos

Animacoes em Manim que mostram a planificacao de um cubo, um tetraedro, piramides, um cilindro e um cone.

## Ambiente e renderizacao

As cenas estao configuradas para video vertical 9:16 (1080 x 1920). Use o ambiente virtual compartilhado na raiz do repositorio. Se ainda nao o configurou, siga as instrucoes no [README principal](../README.md). No PowerShell, a partir da raiz, ative o ambiente e entre nesta pasta:

```powershell
.\.venv\Scripts\Activate.ps1
Set-Location .\planificacoes
```

Renderize as cenas:

```powershell
manim -p -r 1080,1920 planificacoes.py PlanificacaoCubo
manim -p -r 1080,1920 planificacoes.py PlanificacaoTetraedro
manim -p -r 1080,1920 planificacoes.py PlanificacaoPiramideQuadrada
manim -p -r 1080,1920 planificacoes.py PlanificacaoPiramideHexagonal
manim -p -r 1080,1920 planificacoes.py PlanificacaoCilindro
manim -p -r 1080,1920 planificacoes.py PlanificacaoCone
```

Os videos verticais sao salvos em `media/videos/planificacoes/`.
