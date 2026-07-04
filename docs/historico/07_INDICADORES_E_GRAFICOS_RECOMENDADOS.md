# 07 — Indicadores e Gráficos Recomendados

> Painel de evidências para defender a proposta perante CREA-BA, SENGE-BA e entidades.
> Todos baseados em campos reais da base de ARTs 2022 (ver doc. 03). Sempre agregados (LGPD).

---

## 1. Visão geral (cards de topo)

- Total de ARTs distintas: **230.928** · Linhas de atividade: **726.028** · Ano-base: **2022** · UF: **97% BA**.
- Nº de modalidades, nº de municípios cobertos, nº de unidades de medida (111).

## 2. Distribuição de ARTs por atividade/modalidade
- **Gráfico de barras horizontais** — top 15 modalidades (`titulos` padronizado).
- **Treemap** — participação por grupo de atividade.
- *Evidência:* mostra que civil, agronomia e elétrica concentram a demanda → priorização de itens.

## 3. Atividades mais frequentes
- **Barras** das atividades (mapeadas a códigos CREA) por nº de registros.
- Justifica **quais itens a tabela deve cobrir primeiro**.

## 4. Evolução temporal
- **Linha** de nº de ARTs e mediana de valor por ano (2015–2022), após consolidar as bases históricas.
- **Comparação reajuste CUB × evolução observada** → justifica revisão do índice.
- *Obs.:* o CSV atual só tem 2022; exige consolidação histórica (ver backlog).

## 5. Valores por faixa
- **Histograma / decis** de `valor_contrato` por atividade, **por unidade homogênea**.
- **Boxplot por atividade** (mediana + IQR + outliers) — o gráfico mais importante para mostrar
  dispersão e justificar **faixas** em vez de preço único.

## 6. Mediana e intervalo interquartil
- **Gráfico de faixas** (piso P25 – mediana – teto P75) por atividade × unidade.
- É a tradução visual direta do modelo de faixas do doc. 04.

## 7. Mapa por município
- **Mapa coroplético da Bahia** — contagem de ARTs e mediana por município.
- Destaca polos (Salvador, Feira, Vitória da Conquista, oeste agrícola) → base do fator regional.

## 8. Atividades com maior variabilidade
- **Barras de coeficiente de variação (CV)** por atividade.
- Sinaliza onde a faixa precisa ser mais larga e onde há maior risco de aviltamento.

## 9. Matriz atividade × complexidade
- **Heatmap** atividade (linhas) × nível de complexidade (colunas), célula = mediana ou n.
- Suporta os multiplicadores de complexidade do doc. 04.

## 10. Indicadores por modalidade
- **Tabela-painel**: por modalidade → nº ARTs, atividades típicas, unidades dominantes, mediana, IQR.

## 11. Comparação tabela proposta × evidência observada
- **Gráfico de dispersão / barras pareadas**: valor calculado pelo modelo (doc. 04) vs. faixa
  observada nas ARTs por item. Mede **aderência** e legitima o método.

---

## 12. Boas práticas de visualização (LGPD + robustez)
- Suprimir células/pontos com **n < 5**.
- Rotular sempre: ano-base, fonte (ARTs CREA-BA 2022), n, e a ressalva "valor de ART ≠ honorário".
- Preferir **mediana/IQR**; evitar média.
- Cores sóbrias, acessíveis; legendas claras.

## 13. Formato sugerido do painel
- **Dashboard estático** (HTML único ou PDF) com os blocos 1–11, atualizável a cada ciclo anual.
- Reaproveitar competência já existente do usuário em dashboards HTML (projeto Malha IA).

## 14. ✅ Dashboard JÁ IMPLEMENTADO (`dashboard/index.html`)
Foi gerado um painel HTML standalone com dados reais agregados das ARTs 2022:
- KPIs (726.028 linhas; 230.928 ARTs; mediana R$1.570; IQR R$540–8.000).
- **Mapa da Bahia com localização** (60 municípios; tamanho = nº de ARTs, cor = mediana).
- Top municípios, modalidades (nº e mediana), unidades, tipo de ART e faixas (percentis).
- Fontes: `dados/*.csv` e `dados/data.json`; geração por `scripts/agrega_arts.py` + `scripts/gera_dashboard.py`.
- Abre por duplo clique (requer internet para mapa/bibliotecas). Ver `dashboard/LEIA_DASHBOARD.md`.

---

*Documento derivado. Não altera os arquivos originais.*
