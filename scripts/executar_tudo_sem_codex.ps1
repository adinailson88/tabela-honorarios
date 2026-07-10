<#
Executor local seguro para o projeto tabela-honorarios.

Nao faz `git pull` automatico.
Para atualizar o repositorio, revise o worktree e rode Git manualmente.
#>

param(
    [string]$RepoPath = ".",
    [string]$PastaPlanilhas = "",
    [string]$FonteArtsAnuais = "",
    [switch]$CopiarPlanilhas,
    [switch]$GerarAgregadosHistoricos,
    [switch]$PublicarDatasets,
    [switch]$RegenerarDashboard,
    [switch]$ExecutarInventario,
    [switch]$InstalarDependencias,
    [switch]$SomenteValidar
)

$ErrorActionPreference = 'Stop'
$Executed = New-Object System.Collections.Generic.List[string]
$Skipped = New-Object System.Collections.Generic.List[string]

function Run-Step($Title, $Command, $Arguments) {
    Write-Host "`n>> $Title" -ForegroundColor Yellow
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO: etapa falhou com codigo $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
    $Executed.Add($Title) | Out-Null
}

function Skip-Step($Title, $Reason) {
    $Skipped.Add("${Title}: ${Reason}") | Out-Null
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
    if (Test-Path -LiteralPath 'requirements.txt') {
        Run-Step "Instalando dependencias Python do projeto" $PythonCmd @('-m','pip','install','-r','requirements.txt')
    } else {
        Run-Step "Instalando dependencias Python usadas no build publico" $PythonCmd @('-m','pip','install','openpyxl','xlrd')
    }
}

$PublicacaoIntermediaria = 'data\local\processado\publicacao_intermediaria\dados_tos_valor_municipio.json'
$PublicacaoLegada = 'assets\dados_tos_valor_municipio.json'
$RunGerarAgregados = $GerarAgregadosHistoricos -or (-not $SomenteValidar -and -not [string]::IsNullOrWhiteSpace($FonteArtsAnuais))
$RunPublicar = $PublicarDatasets -or (-not $SomenteValidar)
$RunBuild = $RegenerarDashboard -or $SomenteValidar -or (-not $SomenteValidar)
$RunInventario = $ExecutarInventario -or ($SomenteValidar -and (Test-Path -LiteralPath 'scripts\00_inventariar_planilhas_arts.py'))

if ($RunGerarAgregados) {
    if ([string]::IsNullOrWhiteSpace($FonteArtsAnuais)) {
        Skip-Step "Gerando agregados historicos locais" "fonte anual nao informada"
    } elseif (-not (Test-Path -LiteralPath $FonteArtsAnuais)) {
        Write-Host "ERRO: FonteArtsAnuais nao encontrada: $FonteArtsAnuais" -ForegroundColor Red
        exit 1
    } else {
        Run-Step "Gerando agregados historicos locais" $PythonCmd @('scripts\agrega_anos_publico.py','--fonte-arts',$FonteArtsAnuais,'--saida-assets','data\local\processado\publicacao_intermediaria')
    }
}

if ($RunPublicar) {
    if ((Test-Path -LiteralPath $PublicacaoIntermediaria) -or (Test-Path -LiteralPath $PublicacaoLegada)) {
        Run-Step "Publicando datasets saneados em assets/datasets" $PythonCmd @('scripts\publicar_datasets_publicos.py')
    } else {
        Skip-Step "Publicando datasets saneados em assets/datasets" "insumo intermediario ou legado ausente"
    }
}

if ($RunBuild) {
    Run-Step "Regenerando dashboard publico" $PythonCmd @('scripts\build_dashboard_publico.py')
}
Run-Step "Validando JSONs publicos" $PythonCmd @('scripts\01_validar_json_publico.py','--root','assets','--saida','relatorios\validacao_json_publico.md')
Run-Step "Compilando scripts Python principais" $PythonCmd @('-m','py_compile','scripts\publicar_datasets_publicos.py','scripts\agrega_anos_publico.py','scripts\gerar_metodologia_servicos_tos_valor_municipio.py','scripts\01_validar_json_publico.py','scripts\build_dashboard_publico.py','scripts\build_dashboard_tos_valor_municipio_layout_crea.py')
Run-Step "Executando testes automatizados" $PythonCmd @('-m','unittest','discover','-s','tests','-p','test_*.py','-v')

if ($RunInventario) {
    if (Test-Path -LiteralPath 'scripts\00_inventariar_planilhas_arts.py') {
        Run-Step "Inventariando planilhas locais" $PythonCmd @('scripts\00_inventariar_planilhas_arts.py','--entrada','data\local','--saida','relatorios\inventario_planilhas')
    } else {
        Skip-Step "Inventariando planilhas locais" "script 00_inventariar_planilhas_arts.py ausente"
    }
}

Write-Host "`nResumo da execucao" -ForegroundColor Cyan
Write-Host "Etapas executadas: $($Executed.Count)" -ForegroundColor Green
foreach ($item in $Executed) {
    Write-Host " - $item" -ForegroundColor Green
}
Write-Host "Etapas puladas: $($Skipped.Count)" -ForegroundColor Yellow
foreach ($item in $Skipped) {
    Write-Host " - $item" -ForegroundColor Yellow
}
Write-Host "`nConcluido." -ForegroundColor Green
