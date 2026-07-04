<#
Executa validacoes locais do projeto tabela-honorarios.

Uso, a partir da raiz do repositorio:

    powershell -ExecutionPolicy Bypass -File .\scripts\rodar_validacoes_locais.ps1

Este script nao publica dados. Ele cria relatorios locais em .\relatorios.
#>

$ErrorActionPreference = 'Stop'

Write-Host "\n== tabela-honorarios: validacoes locais ==" -ForegroundColor Cyan

$Raiz = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $Raiz

Write-Host "Raiz do repositorio: $Raiz" -ForegroundColor DarkCyan

$Pastas = @(
    'data\local',
    'data\local\entrada',
    'data\local\processado',
    'data\public',
    'relatorios'
)

foreach ($p in $Pastas) {
    if (-not (Test-Path -LiteralPath $p)) {
        New-Item -ItemType Directory -Path $p | Out-Null
        Write-Host "Criada pasta: $p" -ForegroundColor DarkGray
    }
}

Write-Host "\n1) Validando JSON publico agregado..." -ForegroundColor Yellow
python .\scripts\01_validar_json_publico.py --json .\dados_tos_valor_municipio.json --saida .\relatorios\validacao_json_publico.md

Write-Host "\n2) Inventariando planilhas locais de ARTs..." -ForegroundColor Yellow
python .\scripts\00_inventariar_planilhas_arts.py --entrada .\data\local --saida .\relatorios\inventario_planilhas

Write-Host "\n3) Verificando arquivos sensiveis potencialmente rastreados..." -ForegroundColor Yellow
$Sensiveis = @(
    'base_servicos_tos_valor_municipio.csv',
    'base_classe_a_servicos_metodologia.csv'
)

foreach ($s in $Sensiveis) {
    if (Test-Path -LiteralPath $s) {
        Write-Host "ATENCAO: arquivo sensivel existe na raiz local: $s" -ForegroundColor Red
        Write-Host "Confirme se permanece ignorado pelo Git antes de qualquer commit." -ForegroundColor Red
    }
}

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "\n4) Status Git resumido..." -ForegroundColor Yellow
    git status --short
} else {
    Write-Host "Git nao encontrado no PATH. Pulando status." -ForegroundColor DarkYellow
}

Write-Host "\nRelatorios gerados em: .\relatorios" -ForegroundColor Green
Write-Host "Arquivos principais:" -ForegroundColor Green
Write-Host "- .\relatorios\validacao_json_publico.md"
Write-Host "- .\relatorios\inventario_planilhas.md"
Write-Host "- .\relatorios\inventario_planilhas.csv"
