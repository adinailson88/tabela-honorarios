# 13 — Checkpoint de Continuação

## Estado atual (2026-06-22)
Pacote técnico inicial **completo** na pasta `PROPOSTA CLAUDE`. Os 14 arquivos mínimos foram criados.
Diagnóstico de metodologia e de dados concluídos; modelo conceitual, metodologia analítica, matriz,
indicadores, proposta institucional, roteiro, backlog e prompts redigidos. Faltam as etapas de
**execução** (parsing/análise fina, pesquisa de preços, calibração de valores, validação jurídica).

## Ciclos concluídos
- Ciclo 1 — Inventário ✔
- Ciclo 2 — Leitura da metodologia ✔
- Ciclo 3 — Leitura dos dados de ART (perfil agregado de 2022) ✔
- Ciclo 4 — Base metodológica ✔
- Ciclo 5 — Matriz de honorários (conceitual, sem valores) ✔
- Ciclo 6 — Proposta institucional ✔
- Ciclo 7 — Visualização (recomendações) ✔
- Ciclo 8 — Backlog e continuidade ✔
- Ciclo 9 — Pacote final (00_LEIA_PRIMEIRO) ✔
- Ciclo 10 — Aprofundamento: **parcial** (feito no nível conceitual; falta execução de dados)

## Arquivos criados
00 a 13 (ver `12_LOG_EXECUCAO.md`).

## Execução já realizada (sessão 1)
- ✅ A1/B2 — agregados em `dados/` (município, modalidade, unidade, tipo, faixas, top atividades + data.json).
- ✅ A3/B2 — calibração por **Atividade × Unidade** (1.047 combos) → `dados/calibracao_atividade_unidade.csv`.
- ✅ F1 — `dashboard/index.html` com **mapa (Bahia)** + gráficos + faixas por atividade.
- ✅ G1 — `PLANILHA_MODELO_HONORARIOS.xlsx` (1.047 itens; honorário-referência pendente, não inventado).
- ✅ Guia `COMO_PUBLICAR_E_ABRIR.md` (1 clique local + Google Sites).

- ✅ A2 — série temporal 2015–2022 (`dados/serie_temporal.csv`) + CUB verificável (`dados/REFERENCIA_CUB.md`); ambos no dashboard.
- ✅ NOTA_TECNICA, MINUTA_RECOMENDACAO, APRESENTACAO_CREA_SENGE.pptx.
- ✅ PAINEL REDESENHADO (estilo CREA-BA): sidebar com filtros cruzados, KPIs, **choropleth oficial IBGE** (417 munic.),
  gauge, painéis de valor. Base achatada `dados/flat_counts.json` (todos os anos). **Verificado no navegador.**
  Gerado por `scripts/flat_counts.py` + `scripts/gera_painel.py`.
- ✅ AJUSTES PEDIDOS: (a) não-precificáveis flag (`dados/precificabilidade_por_tipo.csv`, ~72% precificável);
  (b) **poda de 20%** nas caudas das faixas + confiabilidade (mistura valor unitário/total); (c) **seletor de
  97 atividades (TOS)** no painel. Planilha com faixas aparadas + aba Precificabilidade. **Verificado no navegador.**
  Para mudar a poda p/ 30%: editar `TRIM=0.30` em `scripts/calibra_atividade.py` e rodar calibra→painel→planilha.

## Arquivos pendentes (execução, não documentação)
- Definir valor-hora/tempo técnico e **preencher honorario_referencia** (backlog B1 + pesquisa de preços C1).
- Mapear texto→código CREA **oficial** via `TABELA TOS` (refinar agrupamento atual por texto).
- Choropleth por polígonos municipais (GeoJSON) — hoje o mapa usa bolhas com coords aproximadas.
- Validação jurídica e confirmação de normas (Lei 4.591/64; NBR 12.721:2006; Lei 4.950-A/66).

## Principais achados
- Base 2022: 726.028 atividades / 230.928 ARTs / 97% BA; mediana R$1.600, IQR 520–8.000.
- ART ≠ honorário; usar como calibração com mediana/IQR por unidade homogênea.
- Já existem TABELA TOS (matriz) e CidadessCalculo (regionalização) a integrar.

## Riscos
- Valores do CSV exigem revalidação de parsing antes de uso oficial.
- Normas jurídicas a confirmar em fonte oficial.
- Enquadramento concorrencial: manter caráter orientativo (anti-cartel).

## PROMPT PARA CONTINUAR (cole em nova conversa)
```
Retome o projeto da nova metodologia de tabela de honorários do SENGE/BA. Leia a pasta
C:\Users\adina\Meu Drive\SENGE\PROPOSTA CLAUDE, começando por 00_LEIA_PRIMEIRO.md e
13_CHECKPOINT_CONTINUACAO.md. Mantenha as regras: não apagar/mover/alterar originais; criar somente
em PROPOSTA CLAUDE; não inventar valores/normas (use "Informação insuficiente para verificar"); só
dados agregados (LGPD), sem ranking individual. Próxima ação recomendada: executar o backlog A1
(parsing robusto do CSV de ARTs) e B2 (calibrar faixas com mediana/IQR por Atividade x Unidade x
Município, suprimindo n<5), salvando apenas CSVs agregados. Depois, gerar o dashboard (prompt 3) e a
planilha-modelo (prompt 7) do arquivo 11_PROMPTS_CONTINUACAO.md.
```
