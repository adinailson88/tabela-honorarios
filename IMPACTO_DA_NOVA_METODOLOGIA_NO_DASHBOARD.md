# IMPACTO DA NOVA METODOLOGIA NO DASHBOARD
## Como a metodologia da tabela de honorários muda o painel de ARTs — SENGE/BA

> Este documento explica, ponto a ponto, as **10 mudanças** que a nova metodologia de honorários
> impõe ao dashboard de ARTs do CREA-BA. Conecta-se ao painel **já corrigido pelo Codex**
> (`dashboard_senge_honorarios_corrigido_codex.html`), que tem **filtros multisseleção** (ano,
> município, modalidade, unidade, tipo de ART; regra OU dentro do filtro / E entre filtros) e a
> **frase-chave** de que a ART é evidência auxiliar.
> Separa explicitamente **FATO VERIFICADO**, **INFERÊNCIA TÉCNICA** e **RECOMENDAÇÃO**.
> Data: 2026-06-23. Este documento NÃO altera o dashboard nem os dados.

---

## Cláusula metodológica central (já presente no painel corrigido)

> **"Os dados de ART são utilizados como evidência auxiliar, indireta e agregada de escopo,
> atividade, localidade, responsabilidade técnica e valor declarado, não como prova isolada do
> honorário profissional efetivamente contratado."**

Todas as 10 mudanças abaixo decorrem dessa cláusula. O painel é **subsídio metodológico** e
**parâmetro orientativo**, nunca tabela vinculante ou preço obrigatório.

---

## Mudança 1 — Separar contagem de ARTs, de atividades e de serviços

**FATO VERIFICADO.** A base tem **726.028 linhas de atividade** que correspondem a apenas
**230.928 ARTs distintas** (campo `id`). Além disso, **62,6%** das ARTs são multi-linha
(144.541 de 230.928) e **26,5%** (61.284) têm mais de um código de atividade distinto.

**INFERÊNCIA TÉCNICA.** Contar "linhas" e chamar de "ARTs" infla o volume em cerca de 3x.
São três níveis distintos de contagem: (i) **ARTs** (unidade administrativa, identificada por `id`);
(ii) **atividades/linhas** (cada item declarado); (iii) **serviços padronizados** (o vocabulário
técnico que a nova metodologia precisa precificar).

**RECOMENDAÇÃO.** O dashboard deve exibir **três KPIs separados e rotulados**: nº de ARTs distintas,
nº de linhas de atividade e nº de serviços padronizados. Nunca somar linhas como se fossem ARTs.
Conecta-se à seção "Visão Geral" do redesenho funcional (P0).

---

## Mudança 2 — Filtro de classe de confiabilidade (A / B / C / D)

**FATO VERIFICADO (dimensionamento sobre os 230.928 ids).**
- **Classe A** (linha única, 1 código, 1 valor plausível): **53.190 ARTs = 23,0%**.
- **Classe B** homogênea (multi-linha, mesmo código, valor constante): **38.631 = 16,7%**.
- **Classe C** composta ambígua (multi-linha, múltiplos códigos, valor único replicado): **60.247 = 26,1%**.
- **Classe D** sem valor: **76.751 = 33,2%** (implausível >R$ 1 bilhão: 29).
- Caso de valor que varia entre linhas: **2.080 = 0,9%**.

**INFERÊNCIA TÉCNICA.** Cada classe tem usos distintos: A serve para cálculo monetário; B para
simulação com regra explícita; C apenas para frequência/detecção; D deve ser excluída do cálculo.

**RECOMENDAÇÃO.** Incluir um **filtro de classe de confiabilidade (A/B/C/D)** que reaja como os
demais filtros multisseleção já corrigidos. O padrão de cálculo monetário deve vir pré-selecionado
em Classe A.

---

## Mudança 3 — Filtro de serviço padronizado

**FATO VERIFICADO.** O campo `atividade` é texto livre, no padrão
"Nível - X  Atividade - Y - DESCRIÇÃO", com `;` internos (parsing exige ancoragem pela direita).
O vocabulário real inclui itens como "ESPECIFICAÇÃO - RECEITUÁRIO AGRO" (60.378), "Execução de Obra
Técnica - EDF. DE ALVENARIA" (10.913) e "SISTEMA DE MICROGERAÇÃO".

**INFERÊNCIA TÉCNICA.** Sem um dicionário de serviços padronizados, o texto livre é heterogêneo e
não casa com as famílias da tabela de honorários (que é organizada por serviço em 13 abas temáticas).

**RECOMENDAÇÃO.** Adicionar um **filtro de serviço padronizado**, alimentado por um dicionário que
mapeie o texto livre da ART para as famílias da tabela. Enquanto o dicionário não existir, sinalizar
que o cruzamento é provisório. Conecta-se à seção "Atividades" (P0) e à matriz de complexidade.

---

## Mudança 4 — Mostrar a base usada para cálculo monetário separada da base total

**FATO VERIFICADO.** Das 230.928 ARTs, **74.026 (32%)** não têm valor utilizável; a Classe D sem
valor é **76.751 (33,2%)**. A precificabilidade por tipo é: OBRA/SERVIÇO 69,7%; RECEITUÁRIO
AGRONÔMICO 93,9%; MÚLTIPLA MENSAL 62,8%; CARGO-FUNÇÃO 61,4%.

**INFERÊNCIA TÉCNICA.** A "base total" e a "base que sustenta um cálculo de valor" são conjuntos
diferentes. Apresentar valor sobre a base total dá a falsa impressão de robustez.

**RECOMENDAÇÃO.** O painel deve exibir, lado a lado, **base total** (todos os registros do recorte)
e **base de cálculo monetário** (apenas registros com valor plausível, tipicamente Classe A), com o
número absoluto e o percentual de cada uma sempre visíveis junto a qualquer KPI de valor.

---

## Mudança 5 — Percentual de registros A / B / C / D

**FATO VERIFICADO.** As proporções globais já constam da Mudança 2 (A 23,0%; B 16,7%; C 26,1%;
D 33,2%; valor variável 0,9%).

**INFERÊNCIA TÉCNICA.** Esses percentuais são um **indicador de qualidade do recorte**: um recorte
dominado por C/D não suporta conclusão monetária; um recorte rico em A, sim.

**RECOMENDAÇÃO.** Mostrar, para cada recorte filtrado, a **composição percentual A/B/C/D** (barra
empilhada ou KPIs). Esse painel de composição deve responder aos filtros multisseleção já corrigidos.

---

## Mudança 6 — Indicar quando o valor é calculado só com casos únicos (Classe A)

**FATO VERIFICADO (Classe A).** Mediana **R$ 2.000**; P25 **R$ 800**; P75 **R$ 8.000**;
P90 **R$ 145.363**. Para o conjunto geral deduplicado por ART: mediana **R$ 1.800**; P25 **800**;
P75 **7.272**; P90 **200.000**; máximo ~7,9×10¹¹ (outliers/erros).

**INFERÊNCIA TÉCNICA.** A mediana por linha (~R$ 1.570) difere da mediana por ART (R$ 1.800)
justamente por causa da **replicação de valor** entre linhas — evidência de mistura. Por isso só
mediana e IQR são defensáveis; **média é inútil** dado o teto extremo.

**RECOMENDAÇÃO.** Quando um KPI de valor for produzido apenas com Classe A, o painel deve **rotular
explicitamente**: "valor calculado somente com casos únicos verificáveis (Classe A); mediana e IQR,
nunca média". Aplicar **supressão n<5** para serviços raros.

---

## Mudança 7 — Indicar quando há apenas frequência, sem valor confiável

**FATO VERIFICADO.** Classe C (60.247) e Classe D (76.751) somam **59,3%** dos ids; nesses casos não
é possível atribuir valor a um serviço (C tem valor único replicado sobre múltiplos códigos; D não
tem valor).

**INFERÊNCIA TÉCNICA.** Para grande parte da base, o dado é útil para **detectar a existência e a
frequência** de um serviço, mas não para precificá-lo.

**RECOMENDAÇÃO.** Quando o recorte só tiver registros C/D (ou n<5 em A/B), o painel deve substituir
o KPI de valor pela frase padrão **"Informação insuficiente para verificar"** e mostrar apenas a
**frequência/contagem** do serviço, deixando claro que não há valor confiável.

---

## Mudança 8 — Evitar KPIs monetários baseados em registros ambíguos (Classe C / D)

**FATO VERIFICADO.** Em ARTs multi-linha, **99.982** têm valor constante replicado e apenas **2.080**
variam. Exemplo real: ART `id 2399866` tem 2 linhas (Laudo e Vistoria), ambas com R$ 433.795,00
replicado. Conclusão de fato: `valor_contrato` é o valor da **ART inteira**, replicado por linha —
não é o valor por atividade. Somar linhas multiplica o valor indevidamente.

**INFERÊNCIA TÉCNICA.** Calcular valor sobre Classe C (múltiplos códigos, valor único) atribui o
valor de toda a ART a um serviço isolado; sobre Classe D não há valor. Ambos contaminam o KPI.

**RECOMENDAÇÃO.** O motor do dashboard deve **bloquear, por construção**, qualquer KPI monetário
derivado de Classe C ou D, permitindo essas classes apenas em contagem/frequência. Documentar o
volume excluído e o motivo (transparência metodológica).

---

## Mudança 9 — Mostrar as lacunas da tabela atual

**FATO VERIFICADO.** A tabela mais recente ("29-07-2024 - Tabela Honorários Adinailson.xlsx",
data 29/07/2024) é organizada por serviço em **13 abas** fortemente civis/estruturais, com unidades
heterogêneas (m², m³, km, ha, hora, %CUB, R$ fixo) e atualização monetária por razão do CUB
(de R$ 1.369,12 em 2017-11 para R$ 1.929,04 em 2024-06, ~+40,9%).

**INFERÊNCIA TÉCNICA.** Confrontada com o vocabulário das ARTs, a tabela **não contempla** serviços
modernos de alto volume: energia solar fotovoltaica/microgeração (kWp), geração de energia,
automação/controle, telecom moderno, eficiência energética, meio ambiente/licenciamento,
agronomia/receituário agronômico e agrimensura/georreferenciamento. Unidades presentes nas ARTs e
ausentes na tabela: **kWp, kVA, kW, hectare (agronomia)**.

**RECOMENDAÇÃO.** Incluir uma seção/indicador de **cobertura da tabela**: para cada serviço
identificado nas ARTs, marcar se há ou não correspondência na tabela atual, evidenciando as lacunas
como pauta de atualização da metodologia.

---

## Mudança 10 — Mostrar os novos serviços identificados nas ARTs

**FATO VERIFICADO (vocabulário e medianas).**
- Receituário agronômico: **60.378** ocorrências (modalidade Agrônomo: 92.344 registros, mediana
  R$ 186,55).
- Microgeração/solar/fotovoltaica: vários itens de 4.500 a 7.700 ocorrências cada.
- Unidades emergentes (mediana de valor): **quilowatt** 46.174 (R$ 1.500); **kWp** 39.751 (R$ 1.000);
  **hectare** 17.259 (R$ 2.000); **kVA** 10.534 (R$ 5.000).
- Modalidades emergentes (mediana): Ambiental 35.828 (R$ 2.470); Controle/Automação 5.729 (R$ 5.000);
  Geólogo 5.932 (R$ 3.000); Agrimensor 9.092 (R$ 2.000).

**INFERÊNCIA TÉCNICA.** Esses serviços são de alto volume e/ou alto valor unitário, mas estão
ausentes da tabela atual — são candidatos prioritários a novas famílias na metodologia.

**RECOMENDAÇÃO.** Criar no painel um indicador de **"serviços novos / não cobertos"**, listando por
frequência os serviços presentes nas ARTs sem correspondência na tabela (fotovoltaica, receituário
agronômico, automação, ambiental, agrimensura). Esse indicador usa **frequência** (confiável) e, onde
houver Classe A suficiente, mediana/IQR com supressão n<5.

---

## Conexão com o dashboard já corrigido

| Mudança | Apoia-se em recurso já corrigido | Próxima rodada |
|---|---|---|
| 1 (3 contagens) | KPIs da Visão Geral | separar e rotular |
| 2 (filtro A/B/C/D) | motor de filtros multisseleção | criar a dimensão classe |
| 3 (serviço padronizado) | filtros multisseleção | dicionário de serviços |
| 4 (base de cálculo vs total) | base filtrada | par de contadores |
| 5 (% A/B/C/D) | reatividade aos filtros | barra de composição |
| 6 (só Classe A) | frase ART como evidência auxiliar | rótulo + supressão n<5 |
| 7 (só frequência) | frase "Informação insuficiente" | regra de fallback |
| 8 (bloquear C/D em valor) | dedup por `id` | trava no motor |
| 9 (lacunas da tabela) | seção Metodologia | indicador de cobertura |
| 10 (serviços novos) | seções de atividades/unidades | indicador dedicado |

As Mudanças 1, 4, 5, 6, 7, 8, 9 e 10 podem ser comunicadas com a base de contagens atual
(`flat_counts.json`); as Mudanças 2 e 3, e os recortes monetários por filtro das Mudanças 6 e 10,
dependem de **novo agregado** (classe de confiabilidade + dicionário de serviços + mediana/IQR/n por
recorte com supressão n<5), conforme `PROMPT_CODEX_PROXIMA_RODADA.md`.

---

## Pontos marcados como "Informação insuficiente para verificar"

- **Recorte filtrado dominado por Classe C/D ou com n<5 em A/B** (Mudança 7): sem valor confiável,
  exibir apenas frequência.
- **Mediana/IQR por filtro (atividade × unidade, modalidade, município/região)**: ainda não existe na
  base interativa atual; depende de novo agregado (Mudanças 5/6/10).
- **Correspondência exata serviço-ART ↔ família da tabela** (Mudanças 3 e 9): provisória até existir o
  dicionário de serviços padronizados.

---
*Documento de impacto metodológico. Caráter orientativo, não impositivo. Não altera o dashboard nem os dados.*
