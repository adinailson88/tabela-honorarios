# tabela-honorarios

Repositorio de publicacao do painel e dos artefatos tecnicos da proposta metodologica orientativa para a Tabela de Honorarios do SENGE/BA.

## Painel publicado

https://adinailson88.github.io/tabela-honorarios/

## Publicacao atual

- `index.html`: pagina publicada pelo GitHub Pages na raiz do repositorio.
- `assets/datasets/historico/manifest.json`: manifesto dos datasets historicos publicados.
- `assets/datasets/historico/combinado.json`: agregado historico 2015-2022 saneado.
- `assets/datasets/historico/anos/*.json`: agregados historicos anuais saneados.
- `assets/datasets/precos/resumos.json`: evidencia monetaria agregada elegivel.
- `assets/datasets/tos-2022/manifest.json`: camada TOS explicitamente desabilitada enquanto a fonte local verificavel nao estiver disponivel.
- `assets/datasets/qualidade/manifest.json`: manifesto de qualidade, privacidade e cobertura.

## Estrutura versionada

- `AGENTS.md`: regras metodologicas e operacionais do repositorio.
- `README.md`: este guia.
- `assets/datasets/`: datasets publicos efetivamente consumidos pelo painel.
- `assets/referencia/`: arquivos agregados de referencia para mapa e apoio metodologico, sem vetores por ART.
- `dados/`: insumos auxiliares e historicos ainda em revisao.
- `docs/`: documentacao metodologica, limitacoes, fontes, auditoria e historico.
- `scripts/`: pipeline, validadores e scripts operacionais ativos.

## Regra metodologica minima

ART nao e contrato, nota fiscal, recibo nem prova isolada de honorario profissional. A evidencia monetaria publicada usa somente agregados com:

- Classe A;
- natureza `provavel_honorario_tecnico`;
- `n >= 5`;
- unidade preservada sem mistura.

Quando a evidencia e insuficiente, usar exatamente: `Informação insuficiente para verificar.`

## Regerar publicacao

Quando houver fontes privadas disponiveis, gere primeiro os agregados intermediarios locais em `data/local/processado/publicacao_intermediaria/` e depois publique os datasets saneados:

```powershell
python .\scripts\agrega_anos_publico.py --fonte-arts "C:\caminho\para\ARTS"
python .\scripts\publicar_datasets_publicos.py
python .\scripts\build_dashboard_publico.py
python .\scripts\01_validar_json_publico.py --root .\assets --saida .\relatorios\validacao_json_publico.md
python -m unittest discover -s .\tests -p "test_*.py" -v
```

## Fluxo local sem Codex

```powershell
.\scripts\executar_tudo_sem_codex.ps1 -SomenteValidar
```

Exemplo com geracao local e publicacao:

```powershell
.\scripts\executar_tudo_sem_codex.ps1 -FonteArtsAnuais "C:\caminho\para\ARTS" -GerarAgregadosHistoricos -PublicarDatasets -RegenerarDashboard -ExecutarInventario
```
