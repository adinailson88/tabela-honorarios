# scripts

Diretório reservado para scripts do pipeline.

## Situação atual

O script `build_dashboard_tos_valor_municipio_layout_crea.py` ainda permanece na raiz por compatibilidade com a estrutura atual do projeto.

Uma migração futura para `scripts/` deve atualizar os caminhos de entrada e saída e validar o GitHub Pages antes de publicar.

## Scripts já disponíveis

### `00_inventariar_planilhas_arts.py`

Inventaria planilhas locais de ARTs em `data/local/`, sem publicar dados linha a linha.

Uso:

```powershell
python .\scripts\00_inventariar_planilhas_arts.py --entrada .\data\local --saida .\relatorios\inventario_planilhas
```

Saídas:

- `relatorios/inventario_planilhas.md`
- `relatorios/inventario_planilhas.csv`

### `01_validar_json_publico.py`

Valida o JSON público agregado usado pelo painel.

Uso:

```powershell
python .\scripts\01_validar_json_publico.py --json .\dados_tos_valor_municipio.json --saida .\relatorios\validacao_json_publico.md
```

Saída:

- `relatorios/validacao_json_publico.md`

### `rodar_validacoes_locais.ps1`

Executa as validações locais principais em sequência.

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
