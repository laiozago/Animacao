# Animacao de Trigonometria

Cena Manim que demonstra o circulo trigonometrico, as curvas de seno e cosseno e a identidade fundamental $\sin^2(\theta) + \cos^2(\theta) = 1$.

## Requisitos

- Python 3.13
- MiKTeX, necessario para renderizar os elementos `MathTex`

## Configuracao

Use o ambiente virtual compartilhado na raiz do repositorio. Se ainda nao o configurou, siga as instrucoes no [README principal](../README.md). No PowerShell, a partir da raiz, ative o ambiente e entre nesta pasta:

```powershell
.\.venv\Scripts\Activate.ps1
Set-Location ".\circulo trigonometrico"
```

Se o Python 3.13 nao estiver instalado, instale-o primeiro e confirme que o launcher `py` o reconhece com `py -0p`.

## Renderizar

As cenas estao configuradas para video vertical 9:16 (1080 x 1920). Adicione os executaveis do MiKTeX ao `PATH` da sessao e renderize:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
manim -p -r 1080,1920 .\trigonometria.py SenoCossenoAnimacao
```

O video vertical e salvo em `media/videos/trigonometria/`.

## Licenca

Este projeto agora e distribuido sob a GNU General Public License v3.0 (GPL-3.0). Esta licenca e menos permissiva que MIT/Apache, exigindo que qualquer distribuicao ou adaptacao do codigo continue aberto e sob os mesmos termos de uso, modificacao e redistribuicao.