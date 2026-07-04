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

## Publicação

Para GitHub Pages, usar:

1. Branch: `main`
2. Source: `Deploy from a branch`
3. Folder: `/ (root)`
4. Arquivo de entrada: `index.html`

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

