<#
Executa validacoes locais basicas do projeto tabela-honorarios.
#>

$ErrorActionPreference = 'Stop'

Write-Host "`n== tabela-honorarios: validacoes locais ==" -ForegroundColor Cyan

$Raiz = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $Raiz

if (-not (Test-Path -LiteralPath 'relatorios')) {
    New-Item -ItemType Directory -Path 'relatorios' | Out-Null
}

Write-Host "`n1) Regenerando dashboard publico..." -ForegroundColor Yellow
python .\scripts\build_dashboard_publico.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n2) Validando JSONs publicos..." -ForegroundColor Yellow
python .\scripts\01_validar_json_publico.py --root .\assets --saida .\relatorios\validacao_json_publico.md
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n3) Compilando scripts Python principais..." -ForegroundColor Yellow
python -m py_compile .\scripts\publicar_datasets_publicos.py .\scripts\01_validar_json_publico.py .\scripts\build_dashboard_publico.py .\scripts\build_dashboard_tos_valor_municipio_layout_crea.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nRelatorios gerados em .\relatorios" -ForegroundColor Green
