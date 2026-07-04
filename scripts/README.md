# scripts

Diretório reservado para scripts do pipeline.

## Comando único recomendado

Para executar tudo que já está automatizado sem Codex, rode a partir da raiz do repositório:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\executar_tudo_sem_codex.ps1 -InstalarDependencias
```

Se quiser copiar automaticamente planilhas de uma pasta externa para `data/local/entrada`, use:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\executar_tudo_sem_codex.ps1 -InstalarDependencias -CopiarPlanilhas -PastaPlanilhas "C:\CAMINHO\DA\PASTA\COM\PLANILHAS"
```

O executor único:

- atualiza o repositório local com `git pull`, quando possível;
- cria pastas locais seguras;
- verifica Python;
- instala/verifica `openpyxl`, se solicitado;
- valida o JSON público agregado;
- inventaria as planilhas locais;
- verifica alertas simples de arquivos sensíveis em locais públicos;
- testa o build atual do painel;
- gera relatório consolidado em `relatorios/relatorio_consolidado_sem_codex.md`.

## Situacao atual

Os scripts ativos ficam nesta pasta. O arquivo publicado pelo GitHub Pages continua sendo `index.html` na raiz do repositorio.

## Scripts já disponíveis

### `executar_tudo_sem_codex.ps1`

Executor único para fluxo local sem Codex.

Uso principal:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\executar_tudo_sem_codex.ps1 -InstalarDependencias
```

### `agrega_anos_publico.py`

Le as planilhas anuais locais (2015-2022) e gera os agregados publicos: o
combinado `assets/dados_tos_valor_municipio.json` e um arquivo por ano em
`assets/anos/dados_tos_valor_municipio_AAAA.json`. Tambem atualiza o
manifesto `docs/modelos/manifesto_bases_anuais_modelo.csv` e o relatorio
`relatorios/auditoria_bases_anuais.md`. Nao publica linha a linha.

Uso:

```powershell
python .\scripts\agrega_anos_publico.py --fonte-arts "C:\CAMINHO\COM\PLANILHAS\DE\ARTS"
```

Sem `--fonte-arts`, usa o caminho local padrao documentado em `docs/fontes.md`.

### `build_dashboard_tos_valor_municipio_layout_crea.py`

Gera `index.html` (e uma copia em `outputs/`) a partir dos agregados em
`assets/`. Por padrao, o painel carrega so o ano mais recente disponivel em
`assets/anos/` ao abrir; trocar o filtro de ano busca sob demanda o JSON
daquele ano (ou o combinado, na opcao "Todos os anos"). Isso evita embutir
todos os anos de uma vez no HTML.

### `00_inventariar_planilhas_arts.py`

Inventaria planilhas locais de ARTs em `data/local/`, sem publicar dados linha a linha.

Uso isolado:

```powershell
python .\scripts\00_inventariar_planilhas_arts.py --entrada .\data\local --saida .\relatorios\inventario_planilhas
```

Saídas:

- `relatorios/inventario_planilhas.md`
- `relatorios/inventario_planilhas.csv`

### `01_validar_json_publico.py`

Valida o JSON público agregado usado pelo painel.

Uso isolado:

```powershell
python .\scripts\01_validar_json_publico.py --json .\assets\dados_tos_valor_municipio.json --saida .\relatorios\validacao_json_publico.md
```

Saída:

- `relatorios/validacao_json_publico.md`

### `rodar_validacoes_locais.ps1`

Executa apenas as validações locais principais em sequência. Foi mantido como alternativa simples.

Uso:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\rodar_validacoes_locais.ps1
```

## Scripts esperados em evolução futura

- ingestão de planilhas anuais;
- validação de colunas obrigatórias;
- deduplicação por ART;
- mapeamento TOS;
- classificação da natureza do valor;
- padronização municipal com IBGE;
- tratamento de outliers;
- agregação pública;
- geração de relatórios de auditoria;
- build do painel.

## Regra

Scripts devem preservar dados linha a linha fora da publicação e gerar somente artefatos agregados para o GitHub Pages.
