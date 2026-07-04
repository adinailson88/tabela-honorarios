# tabela-honorarios

Repositorio de publicacao do painel e dos artefatos tecnicos da proposta de metodologia orientativa para a Tabela de Honorarios do SENGE/BA.

## Arquivo publicado

- index.html

## Estrutura enxuta do repositorio

- index.html
- README.md
- AGENTS.md
- .gitignore
- assets/dados_tos_valor_municipio.json
- docs/
- scripts/

## Scripts principais

- scripts/build_dashboard_tos_valor_municipio_layout_crea.py
- scripts/executar_tudo_sem_codex.ps1
- scripts/rodar_validacoes_locais.ps1
- scripts/00_inventariar_planilhas_arts.py
- scripts/01_validar_json_publico.py

## Regra metodologica

ART nao e contrato, nota fiscal nem prova isolada de honorario profissional.
O painel so exibe mediana e IQR monetarios para a base confiavel: Classe A + provavel honorario tecnico + n >= 5.

Quando a evidencia e insuficiente, usar: Informacao insuficiente para verificar.

## Pastas locais nao versionadas

- data/local/
- data/public/
- outputs/
- relatorios/

## Regerar painel

Rodar:

python .\scripts\build_dashboard_tos_valor_municipio_layout_crea.py

## Fluxo local sem Codex

.\scripts\executar_tudo_sem_codex.ps1 -InstalarDependencias
