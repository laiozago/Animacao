# Planificacoes de solidos geometricos

Animacoes em Manim que mostram a planificacao de um cubo, um tetraedro, piramides, um cilindro e um cone.

## Ambiente e renderizacao

Use o ambiente virtual compartilhado na raiz do repositorio. Se ainda nao o configurou, siga as instrucoes no [README principal](../README.md). No PowerShell, a partir da raiz, ative o ambiente e entre nesta pasta:

```powershell
.\.venv\Scripts\Activate.ps1
Set-Location .\planificacoes
```

Renderize as cenas:

```powershell
manim -pqk planificacoes.py PlanificacaoCubo
manim -pqk planificacoes.py PlanificacaoTetraedro
manim -pqk planificacoes.py PlanificacaoPiramideQuadrada
manim -pqk planificacoes.py PlanificacaoPiramideHexagonal
manim -pqk planificacoes.py PlanificacaoCilindro
manim -pqk planificacoes.py PlanificacaoCone
```

Os videos sao gerados em `media/videos/planificacoes/2160p60`.
