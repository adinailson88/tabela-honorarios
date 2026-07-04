# tabela-honorarios

Repositório de publicação do painel e dos artefatos técnicos da proposta de metodologia orientativa para a Tabela de Honorários do SENGE/BA, com uso de ARTs do CREA-BA como evidência agregada, auxiliar e indireta.

## Página principal

O arquivo publicado é:

- `index.html`

Ele corresponde ao painel institucional TOS + natureza do valor + município, derivado de:

- `dashboard_senge_honorarios_tos_valor_municipio_layout_crea.html`
- `dados_tos_valor_municipio.json`

## Regra metodológica

ART não é contrato, nota fiscal nem prova isolada de honorário profissional. O painel só exibe mediana e IQR monetários para a base confiável: Classe A + provável honorário técnico + n >= 5.

Quando a evidência é insuficiente, o material usa: `Informação insuficiente para verificar.`

## Organização documental

A estrutura documental do projeto foi organizada sem mover os arquivos que sustentam o GitHub Pages.

- `AGENTS.md`: instruções para agentes de codificação e regras de segurança metodológica.
- `docs/metodologia.md`: premissas metodológicas do painel e do uso das ARTs.
- `docs/auditoria.md`: trilha mínima de auditoria para processamento das bases.
- `docs/dicionario-dados.md`: campos esperados, campos derivados e regras de publicação.
- `docs/limitacoes.md`: limitações conhecidas e cautelas interpretativas.
- `docs/fontes.md`: fontes confirmadas e fontes pendentes de verificação.
- `docs/checklist-processamento-anual.md`: checklist para inclusão de planilhas de outros anos.
- `data/`: organização futura dos dados, separando agregados públicos e bases locais.
- `scripts/`: organização futura dos scripts do pipeline.
- `outputs/`: organização futura dos artefatos gerados.

## Publicação

Para GitHub Pages, usar:

1. Branch: `main`
2. Source: `Deploy from a branch`
3. Folder: `/ (root)`
4. Arquivo de entrada: `index.html`

Enquanto essa configuração estiver ativa, `index.html` deve permanecer na raiz.

## Dados não publicados

Os CSVs linha-a-linha derivados das ARTs permanecem no diretório local, mas foram colocados no `.gitignore` porque contêm `id_art`, município, formação e valor declarado por registro:

- `base_servicos_tos_valor_municipio.csv`
- `base_classe_a_servicos_metodologia.csv`

A pasta `data/local/` também está protegida para evitar publicação acidental de bases brutas, intermediárias ou individualizadas. O repositório publica o painel e dados agregados necessários à reprodução visual, sem ranking de profissionais, empresas ou contratantes.

## Regerar o painel principal

```powershell
python build_dashboard_tos_valor_municipio_layout_crea.py
Copy-Item .\dashboard_senge_honorarios_tos_valor_municipio_layout_crea.html .\index.html -Force
```

## Próxima etapa recomendada

A próxima reorganização pode mover `dados_tos_valor_municipio.json`, scripts e HTMLs gerados para subpastas, mas somente depois de ajustar os caminhos do script de build e testar o GitHub Pages localmente.
