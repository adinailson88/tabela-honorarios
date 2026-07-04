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

## Situação atual

O script `build_dashboard_tos_valor_municipio_layout_crea.py` ainda permanece na raiz por compatibilidade com a estrutura atual do projeto.

Uma migração futura para `scripts/` deve atualizar os caminhos de entrada e saída e validar o GitHub Pages antes de publicar.

## Scripts já disponíveis

### `executar_tudo_sem_codex.ps1`

Executor único para fluxo local sem Codex.

Uso principal:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\executar_tudo_sem_codex.ps1 -InstalarDependencias
```

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
python .\scripts\01_validar_json_publico.py --json .\dados_tos_valor_municipio.json --saida .\relatorios\validacao_json_publico.md
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
