# Resolucao da piramide

Animacao em Manim da piramide quadrada e da planificacao usada para encontrar o menor caminho entre dois vertices. O formato horizontal ou vertical e detectado automaticamente pela resolucao informada ao renderizar; a planificacao, os rotulos e o enquadramento da piramide sao ajustados para cada orientacao.

## Ambiente e renderizacao 4K

Use o ambiente virtual compartilhado na raiz do repositorio. Se ainda nao o configurou, siga as instrucoes no [README principal](../README.md). No PowerShell, a partir da raiz, renderize as duas versoes com qualidade 4K a 60 quadros por segundo:

```powershell
.\.venv\Scripts\manim.exe render -qk -r 3840,2160 --media_dir .\questao_piramide\media .\questao_piramide\questao_piramide.py ResolucaoPiramide
.\.venv\Scripts\manim.exe render -qk -r 2160,3840 --media_dir .\questao_piramide\media .\questao_piramide\questao_piramide.py ResolucaoPiramide
```

O video horizontal (3840 x 2160) fica em `questao_piramide/media/videos/questao_piramide/2160p60/`; o vertical (2160 x 3840), em `questao_piramide/media/videos/questao_piramide/3840p60/`.
