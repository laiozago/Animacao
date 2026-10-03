# Animacao de Trigonometria

Cena Manim que demonstra o circulo trigonometrico, as curvas de seno e cosseno e a identidade fundamental $\sin^2(\theta) + \cos^2(\theta) = 1$.

## Requisitos

- Python 3.13
- MiKTeX, necessario para renderizar os elementos `MathTex`

## Configuracao

No PowerShell, crie o ambiente virtual e instale o Manim:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install manim==0.21.0
```

Se o Python 3.13 nao estiver instalado, instale-o primeiro e confirme que o launcher `py` o reconhece com `py -0p`.

## Renderizar

Adicione os executaveis do MiKTeX ao `PATH` da sessao e renderize a cena:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
.\.venv\Scripts\manim.exe -pql .\trigonometria.py SenoCossenoAnimacao
```

O argumento `-pql` renderiza em qualidade baixa e abre o video ao terminar. O resultado fica em `media/videos/trigonometria/480p15/`.