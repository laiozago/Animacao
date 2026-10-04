# Desafio de geometria

Animacao em Manim que apresenta e resolve um desafio sobre a diagonal de um retangulo inscrito em um quarto de circulo.

## Ambiente e renderizacao

Use o ambiente virtual compartilhado na raiz do repositorio. Se ainda nao o configurou, siga as instrucoes no [README principal](../README.md). No PowerShell, a partir da raiz, ative o ambiente e entre nesta pasta:

```powershell
.\.venv\Scripts\Activate.ps1
Set-Location .\desafio
```

A cena esta configurada para video vertical 9:16 (1080 x 1920). Renderize:

```powershell
manim -p -r 1080,1920 desafio.py DesafioGeometria
```

O video vertical e salvo em `media/videos/desafio/`.
