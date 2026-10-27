# Limpeza da pasta "animacao": NAO apaga nada, move o obsoleto para _lixo.
# Uso (PowerShell, dentro desta pasta):  .\organizar.ps1
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$lixo = Join-Path $root '_lixo'
New-Item -ItemType Directory -Force -Path $lixo | Out-Null

# 1) media/ solta na raiz: devolve os 2 videos renderizados para as pastas deles
#    e manda o resto (cache de LaTeX/textos/imagens) para _lixo
$rootMedia = Join-Path $root 'media'
if (Test-Path -LiteralPath $rootMedia) {
    $devolver = @(
        @{ De = 'videos\cena_q18';                   Para = 'especex 2025 - Q18\media\videos\cena_q18' },
        @{ De = 'videos\retangulo_de_prata-claude';  Para = 'construcao_do_retangulo\media\videos\retangulo_de_prata-claude' }
    )
    foreach ($m in $devolver) {
        $src = Join-Path $rootMedia $m.De
        $dst = Join-Path $root $m.Para
        if (Test-Path -LiteralPath $src) {
            if (Test-Path -LiteralPath $dst) {
                Write-Host ('Ja existe, mantido na raiz: ' + $dst)
            } else {
                New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
                Move-Item -LiteralPath $src -Destination $dst
                Write-Host ('Video devolvido para: ' + $dst)
            }
        }
    }
    Move-Item -LiteralPath $rootMedia -Destination (Join-Path $lixo 'media_raiz')
    Write-Host 'Movido para _lixo: media/ da raiz'
}

# 2) Script antigo do retangulo (o mais antigo dos dois)
$velho = @(Get-ChildItem -LiteralPath (Join-Path $root 'construcao_do_retangulo') -Filter '*.py' |
    Where-Object { $_.Name -like 'constru*retangulo.py' })
foreach ($f in $velho) {
    Move-Item -LiteralPath $f.FullName -Destination (Join-Path $lixo 'construcao_do_retangulo_script_antigo.py')
    Write-Host ('Movido para _lixo: ' + $f.Name)
}

# 3) Todas as __pycache__ (o Python recria sozinho)
$caches = @(
    Get-ChildItem -LiteralPath $root -Directory |
        Where-Object { $_.Name -notin '.venv', '.git', '_lixo' } |
        ForEach-Object { Get-ChildItem -LiteralPath $_.FullName -Directory -Recurse -Force -Filter '__pycache__' }
)
foreach ($c in $caches) {
    $rel = $c.FullName.Substring($root.Length).TrimStart('\') -replace '[\\/ ]', '_'
    Move-Item -LiteralPath $c.FullName -Destination (Join-Path $lixo $rel)
}
Write-Host ('Movidas ' + $caches.Count + ' pastas __pycache__ para _lixo')

# 4) Residuo de outra cena em protetor_de_conteudo
$stale = Join-Path $root 'protetor_de_conteudo\media\videos\protetor_de_conteudo\1920p60\partial_movie_files\AreaCirculoCebola'
if (Test-Path -LiteralPath $stale) {
    Move-Item -LiteralPath $stale -Destination (Join-Path $lixo 'AreaCirculoCebola_residuo')
    Write-Host 'Movido para _lixo: residuo AreaCirculoCebola'
}

Write-Host 'Pronto. Revise a pasta _lixo e apague-a quando quiser.'
