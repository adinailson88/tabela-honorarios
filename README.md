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

## Estrutura versionada

A estrutura do `main` foi enxugada para manter no GitHub apenas o que precisa ser público, metodológico ou reprodutível.

```text
.
├── index.html
├── dados_tos_valor_municipio.json
├── dashboard_senge_honorarios_tos_valor_municipio_layout_crea.html
├── build_dashboard_tos_valor_municipio_layout_crea.py
├── README.md
├── AGENTS.md
├── .gitignore
├── docs/
│   ├── metodologia.md
│   ├── auditoria.md
│   ├── dicionario-dados.md
│   ├── limitacoes.md
│   ├── fontes.md
│   ├── checklist-processamento-anual.md
│   ├── plano-trabalho-sem-codex.md
│   └── modelos/
│       └── manifesto_bases_anuais_modelo.csv
└── scripts/
    ├── README.md
    ├── executar_tudo_sem_codex.ps1
    ├── rodar_validacoes_locais.ps1
    ├── 00_inventariar_planilhas_arts.py
    └── 01_validar_json_publico.py
```

## Pastas locais não versionadas

As pastas abaixo podem existir no computador, mas não devem aparecer no GitHub:

- `data/local/`
- `data/public/`
- `outputs/`
- `relatorios/`

Elas são criadas pelos scripts quando necessário.

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

O repositório publica o painel e dados agregados necessários à reprodução visual, sem ranking de profissionais, empresas ou contratantes.

## Regerar o painel principal

```powershell
python build_dashboard_tos_valor_municipio_layout_crea.py
Copy-Item .\dashboard_senge_honorarios_tos_valor_municipio_layout_crea.html .\index.html -Force
```

## Fluxo local sem Codex

A partir da raiz do repositório:

```powershell
.\scripts\executar_tudo_sem_codex.ps1 -InstalarDependencias
```

Se houver planilhas locais de outros anos, coloque os arquivos em:

```text
data\local\entrada\
```

Essa pasta é local e não versionada.
