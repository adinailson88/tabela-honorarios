# 05 — Metodologia Analítica das ARTs

> Método para usar os dados de ART como **evidência auxiliar de mercado** na fundamentação
> da tabela. Reprodutível, conservador e compatível com a LGPD.

---

## 0. Premissa metodológica central

> **A ART não é prova de honorário.** O campo `valor_contrato` pode ser valor da obra, valor do
> contrato ou valor declarado — não necessariamente o honorário do profissional. Portanto, a ART
> é **evidência indireta e auxiliar**, usada para **calibrar e validar faixas**, nunca como prova
> absoluta de preço. Toda saída deve trazer essa ressalva.

---

## 1. Limpeza e padronização

Reaproveitar a "Metodologia de limpeza" já documentada em `Análise ARTs.xlsx` e estender:

1. **Parsing robusto** do CSV (campo `atividade` tem `;` interno → ancorar colunas pela direita).
2. Remoção de espaços, normalização decimal (vírgula/ponto), remoção de horário de `emissao`.
3. **Padronização de rótulos**: unificar gênero ("Engenheiro/Engenheira Civil"), normalizar
   especialidades, normalizar nomes de cidade (acentos/caixa).
4. **Tipagem**: data, valor (float), quantidade (float), unidade (categórica).
5. Marcar e separar **linhas incompletas** (sem valor/atividade) das analisáveis.

## 2. Categorização de atividades

- Mapear o texto livre de `atividade` (≈27 mil variações) para o par **Nível + Atividade do CREA**,
  reutilizando o **dicionário já existente na `TABELA TOS`** (que liga atividade → Cód. TOS).
- Toda análise de valor é feita **por (Atividade × Unidade)** homogêneo — nunca misturando unidades.

## 3. Tratamento de valores (decisões adotadas)

- **Filtrar por unidade** antes de qualquer estatística (ex.: só `metro quadrado`).
- **Não precificáveis:** registros **sem valor e/ou sem unidade** (ex.: cargo-função, registros sem
  medida) **não entram** na precificação. Na base 2022, **~72% das atividades são precificáveis**;
  o restante é reportado à parte (ver `dados/precificabilidade_por_tipo.csv` e a aba "Precificabilidade"
  da planilha). Não se inventa unidade nem valor para esses casos.
- **Poda de outliers (adotada):** para cada Atividade × Unidade, **removem-se os 20% maiores e os 20%
  menores** valores antes de calcular a faixa (configurável p/ 30%). Resultado:
  **piso = P20 aparado · referência = mediana aparada · teto = P80 aparado**. Descarte prévio de
  valores implausíveis (> R$1 bilhão).
- **Sinal de confiabilidade:** combos cujo teto fica muito acima da mediana (> 20×) são marcados
  **"Baixa (provável mistura valor unitário/total)"** — caso típico de m² de obra que mistura preço
  por m² com valor total do contrato. Alta/Média/Baixa acompanham cada faixa.
- **Valores ausentes/zero:** excluídos (não imputar).

## 4. Estatística-resumo (a métrica recomendada)

Para cada **Atividade × Unidade × Região**:

- **Mediana** (tendência central robusta) — **não usar média**.
- **IQR (P25–P75)** como faixa observada.
- **n** (nº de registros) — e **suprimir células com n < 5** (LGPD + robustez).
- Opcional: P10 e P90 como referência ampla.

## 5. Análise por modalidade

Agrupar por `titulos` (modalidade) padronizado: civil, agronomia, elétrica, segurança,
mecânica, ambiental, etc. Reportar nº de ARTs, atividades típicas, unidades dominantes e faixas.

## 6. Análise por município/região

- Agregar por `cidade_obra` e por **macrorregião** (RMS, oeste, sul, sudoeste, norte…).
- Cruzar com o índice regional de `CidadessCalculo` para derivar/validar o **fator regional** (camada C do doc. 04).
- Mapa coroplético por município (contagem e faixa mediana).

## 7. Análise por faixa de valor

- Histograma/decis de `valor_contrato` por atividade, sempre por unidade homogênea.
- Identificar concentração (mediana) e dispersão (IQR/coeficiente de variação).

## 8. Análise temporal

- Com o CSV atual: só 2022 (corte transversal).
- **Recomendado:** consolidar 2015–2022 (bases .xls/.xlsx por semestre) para série histórica
  e medir evolução real vs. reajuste pelo CUB — **insumo forte para justificar troca de índice**.

## 9. Agregação para preservar privacidade (LGPD)

- Publicar **apenas agregados** (atividade/modalidade/cidade/unidade/faixa).
- **Suprimir** qualquer recorte com n < 5.
- **Nunca** expor `id`, profissional, contratante, endereço ou ART individual.
- **Nunca** produzir ranking individual.

## 10. Limitações da ART como proxy de honorários (declarar sempre)

1. `valor_contrato` mistura honorário, valor de obra e valor declarado.
2. Outliers e erros de digitação (até 10¹¹).
3. Heterogeneidade de unidades (111) e de texto de atividade (27 mil).
4. Possível subdeclaração/sobredeclaração de valores.
5. Corte transversal (só 2022 no CSV consolidado).

## 11. Indicadores recomendados (saída da análise)

| Indicador | Definição | Uso |
|---|---|---|
| Mediana por Atividade×Unidade | P50 robusto | Âncora da faixa de referência |
| IQR por Atividade×Unidade | P75–P25 | Faixa observada (piso/teto empírico) |
| n por célula | Contagem | Confiabilidade + corte LGPD |
| CV (coef. variação) | dispersão/centro | Sinaliza atividades voláteis |
| Frequência por modalidade | Contagem | Prioriza itens a tabelar |
| Fator regional | mediana cidade / mediana estadual | Calibra camada C |
| Aderência modelo×ART | valor calculado vs. faixa observada | Valida o modelo do doc. 04 |

---

## 12. Pipeline reprodutível (resumo)

```
CSV bruto
  → parsing robusto (ancorar pela direita)
  → limpeza + padronização (rótulos, unidades, datas)
  → mapear atividade → código CREA (dicionário TOS)
  → filtrar por unidade homogênea
  → winsorizar outliers por Atividade×Unidade
  → calcular mediana, IQR, n  (suprimir n<5)
  → agregar por modalidade / cidade / região
  → cruzar com CidadessCalculo (fator regional)
  → calibrar/validar faixas do modelo (doc. 04)
  → exportar SOMENTE agregados para PROPOSTA CLAUDE
```

---

*Documento derivado. Não altera os arquivos originais.*
