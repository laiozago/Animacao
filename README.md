# Projetos

Esta pasta reune projetos independentes. Cada projeto deve ficar em seu proprio diretorio e manter nele um `README.md` com sua descricao, requisitos, configuracao e instrucoes de uso.

## Projetos

- [Circulo trigonometrico](circulo%20trigonometrico/README.md): animacao em Manim do circulo trigonometrico e das curvas de seno e cosseno.
- [Planificacoes](planificacoes/README.md): animacoes em Manim das planificacoes de solidos geometricos.

## Ambiente Python

Os projetos compartilham um unico ambiente virtual e uma lista de dependencias na raiz. Requer Python 3.13. No PowerShell, a partir desta pasta, configure-o uma vez:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Ative `.venv` antes de executar os comandos de renderizacao descritos nos READMEs dos projetos.

## Organizacao

```text
pasta-mae/
|-- README.md
|-- requirements.txt
|-- .venv/
|-- circulo trigonometrico/
|   |-- README.md
|   `-- arquivos do projeto
`-- planificacoes/
    |-- README.md
    `-- planificacoes.py
```

Ao adicionar um projeto, crie um novo diretorio e inclua nele um README proprio. Mantenha neste arquivo apenas o catalogo e as orientacoes que se aplicam a pasta como um todo; detalhes especificos, dependencias e comandos devem ficar no README do respectivo projeto.

## Licenca

Salvo indicacao diferente no README ou em uma licenca dentro do proprio projeto, os projetos deste repositorio estao sob a GNU General Public License v3.0 (GPL-3.0). Essa licenca e menos permissiva do que MIT/Apache, exigindo que qualquer adaptacao ou redistribuicao continue aberto e sob os mesmos termos. Consulte [LICENSE](LICENSE).