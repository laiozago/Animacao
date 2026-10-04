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

Adicione os executaveis do MiKTeX ao `PATH` da sessao e renderize a cena:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
manim -pql .\trigonometria.py SenoCossenoAnimacao
```

O argumento `-pql` renderiza em qualidade baixa e abre o video ao terminar. O resultado fica em `media/videos/trigonometria/480p15/`.

## Licenca

Este projeto agora e distribuido sob a GNU General Public License v3.0 (GPL-3.0). Esta licenca e menos permissiva que MIT/Apache, exigindo que qualquer distribuicao ou adaptacao do codigo continue aberto e sob os mesmos termos de uso, modificacao e redistribuicao.