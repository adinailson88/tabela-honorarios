<#
Executor local seguro para o projeto tabela-honorarios.

Nao faz `git pull` automatico.
Para atualizar o repositorio, revise o worktree e rode Git manualmente.
#>

param(
    [string]$RepoPath = ".",
    [string]$PastaPlanilhas = "",
    [switch]$CopiarPlanilhas,
    [switch]$InstalarDependencias,
    [switch]$SomenteValidar
)

$ErrorActionPreference = 'Stop'

function Run-Step($Title, $Command, $Arguments) {
    Write-Host "`n>> $Title" -ForegroundColor Yellow
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO: etapa falhou com codigo $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

$ResolvedRepo = (Resolve-Path -LiteralPath $RepoPath).Path
Set-Location -LiteralPath $ResolvedRepo
Write-Host "Repositorio: $ResolvedRepo" -ForegroundColor Cyan

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "`n>> Status Git atual" -ForegroundColor Yellow
    git status --short
}

foreach ($p in @('data','data\local','data\local\entrada','data\local\processado','relatorios')) {
    if (-not (Test-Path -LiteralPath $p)) {
        New-Item -ItemType Directory -Path $p | Out-Null
    }
}

if ($CopiarPlanilhas -and -not [string]::IsNullOrWhiteSpace($PastaPlanilhas) -and (Test-Path -LiteralPath $PastaPlanilhas)) {
    Write-Host "`n>> Copiando planilhas para data\local\entrada" -ForegroundColor Yellow
    foreach ($ext in @('*.xlsx','*.xlsm','*.xls','*.csv')) {
        Get-ChildItem -LiteralPath $PastaPlanilhas -Recurse -File -Filter $ext -ErrorAction SilentlyContinue | ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination (Join-Path 'data\local\entrada' $_.Name) -Force
        }
    }
}

$PythonCmd = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { $null }
if (-not $PythonCmd) {
    Write-Host "ERRO: Python nao encontrado no PATH." -ForegroundColor Red
    exit 1
}

if ($InstalarDependencias) {
    Run-Step "Instalando dependencias Python usadas no build publico" $PythonCmd @('-m','pip','install','openpyxl')
}

if (-not $SomenteValidar -and (Test-Path -LiteralPath 'assets\dados_tos_valor_municipio.json')) {
    Run-Step "Migrando artefatos legados para assets/datasets" $PythonCmd @('scripts\publicar_datasets_publicos.py')
}

Run-Step "Regenerando dashboard publico" $PythonCmd @('scripts\build_dashboard_publico.py')
Run-Step "Validando JSONs publicos" $PythonCmd @('scripts\01_validar_json_publico.py','--root','assets','--saida','relatorios\validacao_json_publico.md')
Run-Step "Compilando scripts Python principais" $PythonCmd @('-m','py_compile','scripts\publicar_datasets_publicos.py','scripts\01_validar_json_publico.py','scripts\build_dashboard_publico.py','scripts\build_dashboard_tos_valor_municipio_layout_crea.py')

if (Test-Path -LiteralPath 'scripts\00_inventariar_planilhas_arts.py') {
    Run-Step "Inventariando planilhas locais" $PythonCmd @('scripts\00_inventariar_planilhas_arts.py','--entrada','data\local','--saida','relatorios\inventario_planilhas')
}

Write-Host "`nConcluido." -ForegroundColor Green
