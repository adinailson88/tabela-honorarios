<#
Executa tudo que pode ser feito localmente sem Codex para o projeto tabela-honorarios.

Uso recomendado em qualquer PowerShell:

    powershell -ExecutionPolicy Bypass -File .\scripts\executar_tudo_sem_codex.ps1

Ou, se ainda nao estiver dentro do repositorio:

    powershell -ExecutionPolicy Bypass -File C:\Users\adina\repos\tabela-honorarios\scripts\executar_tudo_sem_codex.ps1

O script:
- localiza ou usa a pasta do repositorio;
- atualiza o repositorio com git pull;
- cria a estrutura local segura;
- procura planilhas em data/local e data/local/entrada;
- opcionalmente copia planilhas de uma pasta externa informada;
- instala/verifica openpyxl;
- valida o JSON publico;
- inventaria planilhas locais;
- verifica arquivos sensiveis;
- gera um relatorio consolidado.

Nao publica dados linha a linha. Nao faz commit. Nao faz push.
#>

param(
    [string]$RepoPath = "C:\Users\adina\repos\tabela-honorarios",
    [string]$PastaPlanilhas = "",
    [switch]$CopiarPlanilhas,
    [switch]$InstalarDependencias
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

function Escrever-Titulo($Texto) {
    Write-Host "`n============================================================" -ForegroundColor Cyan
    Write-Host $Texto -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
}

function Escrever-Etapa($Texto) {
    Write-Host "`n>> $Texto" -ForegroundColor Yellow
}

function Falhar($Texto) {
    Write-Host "ERRO: $Texto" -ForegroundColor Red
    exit 1
}

Escrever-Titulo "tabela-honorarios: executor unico sem Codex"

# 1. Resolver repositorio
if (-not (Test-Path -LiteralPath $RepoPath)) {
    $RepoPathAlternativo = Join-Path $PWD "tabela-honorarios"
    if (Test-Path -LiteralPath $RepoPathAlternativo) {
        $RepoPath = $RepoPathAlternativo
    } elseif ((Test-Path -LiteralPath ".git") -and (Test-Path -LiteralPath "README.md")) {
        $RepoPath = (Resolve-Path ".").Path
    } else {
        Falhar "Repositorio nao encontrado em '$RepoPath'. Informe -RepoPath ou execute dentro do repositorio."
    }
}

$RepoPath = (Resolve-Path -LiteralPath $RepoPath).Path
Set-Location -LiteralPath $RepoPath
Write-Host "Repositorio: $RepoPath" -ForegroundColor DarkCyan

# 2. Conferir Git e atualizar
Escrever-Etapa "Atualizando repositorio local"
if (Get-Command git -ErrorAction SilentlyContinue) {
    if (Test-Path -LiteralPath ".git") {
        git status --short
        git pull
    } else {
        Write-Host "Diretorio nao contem .git. Pulando git pull." -ForegroundColor DarkYellow
    }
} else {
    Write-Host "Git nao encontrado no PATH. Pulando atualizacao." -ForegroundColor DarkYellow
}

# 3. Criar estrutura local segura
Escrever-Etapa "Criando estrutura local segura"
$Pastas = @(
    "data",
    "data\public",
    "data\local",
    "data\local\entrada",
    "data\local\processado",
    "relatorios",
    "relatorios\logs"
)
foreach ($p in $Pastas) {
    if (-not (Test-Path -LiteralPath $p)) {
        New-Item -ItemType Directory -Path $p | Out-Null
        Write-Host "Criada: $p" -ForegroundColor DarkGray
    }
}

# 4. Opcionalmente copiar planilhas externas para data/local/entrada
if ($CopiarPlanilhas) {
    Escrever-Etapa "Copiando planilhas externas para data/local/entrada"
    if ([string]::IsNullOrWhiteSpace($PastaPlanilhas)) {
        Write-Host "-CopiarPlanilhas foi usado, mas -PastaPlanilhas nao foi informado. Pulando copia." -ForegroundColor DarkYellow
    } elseif (-not (Test-Path -LiteralPath $PastaPlanilhas)) {
        Write-Host "PastaPlanilhas nao encontrada: $PastaPlanilhas. Pulando copia." -ForegroundColor DarkYellow
    } else {
        $Extensoes = @("*.xlsx", "*.xlsm", "*.csv")
        $ArquivosCopiar = @()
        foreach ($ext in $Extensoes) {
            $ArquivosCopiar += Get-ChildItem -LiteralPath $PastaPlanilhas -Recurse -File -Filter $ext -ErrorAction SilentlyContinue
        }
        foreach ($arq in $ArquivosCopiar) {
            $dest = Join-Path "data\local\entrada" $arq.Name
            Copy-Item -LiteralPath $arq.FullName -Destination $dest -Force
            Write-Host "Copiado: $($arq.Name)" -ForegroundColor DarkGray
        }
        Write-Host "Total copiado: $($ArquivosCopiar.Count)" -ForegroundColor Green
    }
}

# 5. Conferir Python
Escrever-Etapa "Verificando Python"
$PythonCmd = $null
foreach ($cmd in @("python", "py")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $PythonCmd = $cmd
        break
    }
}
if (-not $PythonCmd) {
    Falhar "Python nao encontrado no PATH. Instale Python ou abra o PowerShell com Python disponivel."
}
Write-Host "Python: $PythonCmd" -ForegroundColor Green
& $PythonCmd --version

# 6. Conferir openpyxl
Escrever-Etapa "Verificando dependencia openpyxl"
$OpenpyxlOk = $false
try {
    & $PythonCmd -c "import openpyxl; print('openpyxl OK')"
    $OpenpyxlOk = $true
} catch {
    $OpenpyxlOk = $false
}

if (-not $OpenpyxlOk) {
    if ($InstalarDependencias) {
        Write-Host "Instalando openpyxl..." -ForegroundColor Yellow
        & $PythonCmd -m pip install openpyxl
    } else {
        Write-Host "openpyxl nao encontrado. XLSX pode ficar com pendencia." -ForegroundColor DarkYellow
        Write-Host "Para instalar automaticamente, rode com -InstalarDependencias." -ForegroundColor DarkYellow
    }
}

# 7. Validar JSON publico
Escrever-Etapa "Validando JSON publico agregado"
if (Test-Path -LiteralPath "scripts\01_validar_json_publico.py") {
    & $PythonCmd "scripts\01_validar_json_publico.py" --json "dados_tos_valor_municipio.json" --saida "relatorios\validacao_json_publico.md"
} else {
    Write-Host "Script scripts\01_validar_json_publico.py nao encontrado." -ForegroundColor Red
}

# 8. Inventariar planilhas locais
Escrever-Etapa "Inventariando planilhas locais de ARTs"
if (Test-Path -LiteralPath "scripts\00_inventariar_planilhas_arts.py") {
    & $PythonCmd "scripts\00_inventariar_planilhas_arts.py" --entrada "data\local" --saida "relatorios\inventario_planilhas"
} else {
    Write-Host "Script scripts\00_inventariar_planilhas_arts.py nao encontrado." -ForegroundColor Red
}

# 9. Verificar arquivos sensiveis em locais perigosos
Escrever-Etapa "Verificando arquivos sensiveis na raiz e em data/public"
$PossiveisSensiveis = @(
    "base_servicos_tos_valor_municipio.csv",
    "base_classe_a_servicos_metodologia.csv"
)
$AlertasSensiveis = @()
foreach ($s in $PossiveisSensiveis) {
    if (Test-Path -LiteralPath $s) {
        $AlertasSensiveis += "Arquivo sensivel encontrado na raiz local: $s"
    }
}

$PublicFiles = Get-ChildItem -LiteralPath "data\public" -Recurse -File -ErrorAction SilentlyContinue
foreach ($pf in $PublicFiles) {
    if ($pf.Name -match "(?i)(art|cpf|cnpj|profissional|contratante|empresa|linha|bruto)") {
        $AlertasSensiveis += "Possivel arquivo sensivel em data/public: $($pf.FullName)"
    }
}

if ($AlertasSensiveis.Count -eq 0) {
    Write-Host "Nenhum alerta obvio de arquivo sensivel em local publico." -ForegroundColor Green
} else {
    foreach ($a in $AlertasSensiveis) {
        Write-Host "ATENCAO: $a" -ForegroundColor Red
    }
}

# 10. Testar build do painel sem alterar index se script existir
Escrever-Etapa "Verificando build do painel atual"
if (Test-Path -LiteralPath "build_dashboard_tos_valor_municipio_layout_crea.py") {
    try {
        & $PythonCmd "build_dashboard_tos_valor_municipio_layout_crea.py"
        if (Test-Path -LiteralPath "dashboard_senge_honorarios_tos_valor_municipio_layout_crea.html") {
            Write-Host "Build gerou/atualizou dashboard_senge_honorarios_tos_valor_municipio_layout_crea.html" -ForegroundColor Green
        }
    } catch {
        Write-Host "Falha ao executar build do painel: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "Script de build principal nao encontrado. Pulando." -ForegroundColor DarkYellow
}

# 11. Gerar relatorio consolidado
Escrever-Etapa "Gerando relatorio consolidado"
$Agora = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$Relatorio = @()
$Relatorio += "# Relatorio consolidado sem Codex"
$Relatorio += ""
$Relatorio += "Gerado em: $Agora"
$Relatorio += "Repositorio: `$RepoPath`"
$Relatorio += ""
$Relatorio += "## Acoes executadas"
$Relatorio += ""
$Relatorio += "- Repositorio localizado."
$Relatorio += "- Estrutura local criada/verificada."
$Relatorio += "- JSON publico validado, quando script disponivel."
$Relatorio += "- Planilhas locais inventariadas, quando script disponivel."
$Relatorio += "- Arquivos sensiveis em locais publicos verificados por heuristica simples."
$Relatorio += "- Build do painel testado, quando script disponivel."
$Relatorio += ""
$Relatorio += "## Relatorios gerados"
$Relatorio += ""
$Relatorio += "- `relatorios/validacao_json_publico.md`"
$Relatorio += "- `relatorios/inventario_planilhas.md`"
$Relatorio += "- `relatorios/inventario_planilhas.csv`"
$Relatorio += ""
$Relatorio += "## Alertas"
$Relatorio += ""
if ($AlertasSensiveis.Count -eq 0) {
    $Relatorio += "- Nenhum alerta obvio de arquivo sensivel em local publico."
} else {
    foreach ($a in $AlertasSensiveis) { $Relatorio += "- $a" }
}
$Relatorio += ""
$Relatorio += "## Proximo passo"
$Relatorio += ""
$Relatorio += "Enviar o conteudo de `relatorios/inventario_planilhas.md` para revisao das colunas disponiveis por ano."

$RelatorioPath = "relatorios\relatorio_consolidado_sem_codex.md"
$Relatorio -join "`n" | Set-Content -LiteralPath $RelatorioPath -Encoding UTF8
Write-Host "Relatorio consolidado: $RelatorioPath" -ForegroundColor Green

# 12. Status Git final
Escrever-Etapa "Status final"
if (Get-Command git -ErrorAction SilentlyContinue) {
    git status --short
}

Write-Host "`nCONCLUIDO." -ForegroundColor Green
Write-Host "Abra estes arquivos:" -ForegroundColor Green
Write-Host "- relatorios\relatorio_consolidado_sem_codex.md"
Write-Host "- relatorios\inventario_planilhas.md"
Write-Host "- relatorios\validacao_json_publico.md"
