# Diagnóstico da natureza do valor declarado em ART

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Natureza:** diagnóstico. Não altera arquivos originais.

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.

---

## 1. Por que a Classe A não basta

**[FATO VERIFICADO]** A Classe A garante que a ART tem **uma única atividade/linha com valor associável** (baixo risco de mistura *entre atividades*). Mas o campo de valor é o **valor do contrato/serviço da ART**, que pode ser:
- honorário técnico (elaboração, projeto, laudo, consultoria);
- **valor de obra/contrato** (execução, fiscalização);
- taxa ou valor simbólico;
- valor inconsistente/extremo.

**[INFERÊNCIA TÉCNICA]** A classe de confiabilidade resolve a **decomponibilidade** do valor, não a **natureza** dele. Logo, é necessário um segundo filtro — a natureza do valor — antes de usar a mediana como referência de honorário.

## 2. Diferença entre valor de ART, honorário técnico e valor de obra/contrato

**[INFERÊNCIA TÉCNICA]**
- **Valor de ART** = valor declarado no registro (genérico).
- **Honorário técnico** = remuneração pela atividade intelectual (projeto, laudo, consultoria) — tipicamente medido por `unidade`, `mês`, `hora`.
- **Valor de obra/contrato** = custo da execução física — medido por `metro quadrado`, `metro cúbico`, `hectare`, `quilômetro`, e associado a níveis de **Execução/Fiscalização**.

## 3. Critérios usados (conservadores, sem inventar)

**[FATO VERIFICADO]** Campos disponíveis na aba TOS: `Nível da atividade` e `Unidade de medida`. Distribuição observada:
- Níveis: Execução (119.116 linhas), Elaboração (39.208), Consultoria (6.549), Fiscalização (3.631), Assessoria (2.968), Coordenação (2.073)…
- Unidades: metro quadrado (58.610), unidade (38.001), kWp (25.341), kW (23.816), hectare (8.840), kVA (6.147), metro (5.132), metro cúbico (3.624), mês (686), hora (1.202)…

**[RECOMENDAÇÃO / regra implementada]** Por ART (usando nível e unidade **modais** da ART):
1. `valor_inconsistente_ou_extremo`: valor ausente/zerado/negativo; ou ≥ R$ 1 bilhão; ou **outlier** acima de **Q3 + 3·IQR** dentro do serviço (calculado só sobre candidatos a honorário, n≥30).
2. `valor_simbolico_ou_taxa`: 0 < valor ≤ R$ 10.
3. `provavel_valor_obra_contrato`: nível de execução (Execução, Fiscalização, Direção de obra, Supervisão, Coordenação…) **ou** unidade de obra (m², m³, m, km, hectare).
4. `provavel_honorario_tecnico`: nível técnico (Elaboração, Consultoria, Assessoria, Assistência, Orientação, Concepção…) **e** unidade técnica (unidade, mês, ano, dia, hora, homem-hora).
5. `informacao_insuficiente`: qualquer combinação não conclusiva (regra padrão na dúvida).

**[INFERÊNCIA TÉCNICA]** Unidades de energia (kWp, kW, kVA, MW) ficam deliberadamente em `informacao_insuficiente` quando não acompanhadas de nível técnico claro, pois podem ser tanto projeto (honorário) quanto instalação (obra). Optou-se por **não** classificá-las como honorário para evitar superestimar a base confiável.

## 4. Distribuição por natureza (camada TOS, 59.764 ARTs)

**[FATO VERIFICADO]** (`resumo_natureza_valor.csv`):

| Natureza | ARTs | % | Mediana | Q1 | Q3 |
|---|---|---|---|---|---|
| provável obra/contrato | 39.569 | 66,2% | R$ 2.000,00 | R$ 1.000,00 | R$ 6.500,00 |
| informação insuficiente | 9.083 | 15,2% | R$ 1.400,00 | R$ 690,00 | R$ 5.000,00 |
| **provável honorário técnico** | **6.947** | **11,6%** | **R$ 1.000,00** | **R$ 600,00** | **R$ 2.000,00** |
| simbólico/taxa | 2.966 | 5,0% | R$ 1,00 | R$ 1,00 | R$ 1,00 |
| inconsistente/extremo | 1.199 | 2,0% | — | — | — |

**[INFERÊNCIA TÉCNICA]** **Apenas ≈11,6% das ARTs** (e, dentre as Classe A, ≈3.745 ARTs) são prováveis honorários técnicos. Isso confirma quantitativamente a tese de que **a maior parte do valor declarado em ART não é honorário** — é valor de obra/contrato (66,2%).

## 5. Serviços com risco de valor de obra

**[FATO VERIFICADO / INFERÊNCIA]** Os grupos dominados por nível de Execução e unidades físicas (m²/m³/hectare/km) concentram `provavel_valor_obra_contrato`: Construção Civil, Estruturas, Pavimentação/Transportes, Saneamento. **Comparação direta:** no agregado anterior (sem filtro de natureza), Pavimentação aparecia com mediana **R$ 1.298.877**; no agregado confiável atual (Classe A + honorário), Pavimentação cai para **R$ 3.000 (n=9)** — a contaminação por valor de obra foi removida.

## 6. Serviços com valor simbólico

**[FATO VERIFICADO]** 2.966 ARTs com valor ≤ R$ 10 (mediana R$ 1,00). Concentram-se onde o valor declarado é nominal — incluindo registros de Receituário Agronômico (que no agregado anterior tinha mediana R$ 1,72). Tratados como `valor_simbolico_ou_taxa` e **excluídos** do cálculo de referência.

## 7. Limitações

**[INFERÊNCIA TÉCNICA]**
- A natureza é **preliminar e conservadora**, inferida de nível + unidade; não há campo que declare diretamente "isto é honorário". Onde houve dúvida → `informacao_insuficiente` (15,2%).
- Unidades de energia ficam fora do honorário por precaução, o que pode **subestimar** a base confiável de serviços elétricos/fotovoltaicos.
- A camada cobre 59.764 ARTs (subconjunto); a natureza do valor para o restante do universo é "Informação insuficiente para verificar".
- Mesmo a parcela `provavel_honorario_tecnico` continua sendo **valor declarado em ART, não honorário líquido contratado**.
