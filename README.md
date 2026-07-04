# tabela-honorarios

Repositorio de publicacao do painel e dos artefatos tecnicos da proposta de metodologia orientativa para a Tabela de Honorarios do SENGE/BA.

## Publicacao

- `index.html`: pagina publicada pelo GitHub Pages na raiz do repositorio.
- `assets/dados_tos_valor_municipio.json`: agregado publico consumido pelo painel.
- `assets/anos/`: agregados publicos por ano.

## Estrutura versionada

- `AGENTS.md`: regras metodologicas e operacionais do repositorio.
- `README.md`: este guia de estrutura e execucao.
- `assets/`: dados agregados publicos do painel.
- `assets/referencia/`: CSVs e JSONs agregados de referencia, sem linhas individuais de ART.
- `dados/`: dados auxiliares agregados usados por scripts e painel.
- `docs/modelos/`: modelos e manifestos tecnicos atuais.
- `docs/entregaveis/`: arquivos finais entregaveis.
- `docs/historico/`: documentacao, dashboards e scripts anteriores preservados como historico.
- `scripts/`: pipeline, validadores e scripts operacionais ativos.

## Scripts principais

- `scripts/agrega_anos_publico.py`: agrega bases anuais locais em JSON/CSV publico, preservando unidade de medida.
- `scripts/build_dashboard_tos_valor_municipio_layout_crea.py`: regenera o `index.html`.
- `scripts/01_validar_json_publico.py`: valida o JSON publico.
- `scripts/rodar_validacoes_locais.ps1`: executa validacoes locais basicas.
- `scripts/executar_tudo_sem_codex.ps1`: fluxo operacional local sem Codex.

## Regra metodologica

ART nao e contrato, nota fiscal nem prova isolada de honorario profissional. O painel so exibe mediana e IQR monetarios para a base confiavel: Classe A + provavel honorario tecnico + n >= 5. A unidade de medida deve ser preservada no agrupamento estatistico.

Quando a evidencia e insuficiente, usar exatamente: `Informação insuficiente para verificar.`

## Pastas locais nao versionadas

- `data/local/`
- `data/public/`
- `outputs/`
- `relatorios/`

## Regerar painel

```powershell
python .\scripts\build_dashboard_tos_valor_municipio_layout_crea.py
python .\scripts\01_validar_json_publico.py --json .\assets\dados_tos_valor_municipio.json --saida .\relatorios\validacao_json_publico.md
```

## Fluxo local sem Codex

```powershell
.\scripts\executar_tudo_sem_codex.ps1 -InstalarDependencias
```
