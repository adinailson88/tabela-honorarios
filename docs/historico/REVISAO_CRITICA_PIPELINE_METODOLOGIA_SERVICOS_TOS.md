# Revisão crítica da pipeline de metodologia por serviço (visão TOS)

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Documento:** revisão técnico-metodológica da entrega atual
**Autor da revisão:** revisor técnico-metodológico (Claude)
**Data:** 2026-06-24
**Natureza:** documento de revisão. Não altera arquivos existentes, não roda pipeline, não reclassifica base.

> Convenção deste documento: cada bloco separa **[FATO VERIFICADO]** (confirmado nos arquivos/dados),
> **[INFERÊNCIA TÉCNICA]** (leitura do revisor a partir dos fatos) e **[RECOMENDAÇÃO]** (ação proposta).
> Onde não há base local para afirmar, registra-se literalmente: **"Informação insuficiente para verificar"**.

---

## 1. O que está tecnicamente correto

**[FATO VERIFICADO]**
- A classificação de confiabilidade opera **no nível da ART**, não no nível da linha de atividade. O script `gerar_metodologia_servicos.py` agrega por `id` da ART antes de classificar (`parse()` → `arts[_id]`).
- O valor é tratado como **valor da ART inteira**: quando várias linhas repetem o mesmo valor, o pipeline detecta isso (`vary`, `valor_replicado_linhas`) e **não soma** as linhas. Isso está coerente com o fato verificado da ART `2399866`.
- A regra de classe está implementada de forma rastreável em `classify()`:
  - **A** = ART de linha única (`n == 1`) com valor plausível;
  - **B** = composta homogênea (mesmo código, valor único replicado);
  - **C** = composta ambígua (múltiplos códigos/atividades ou valor variável não decomponível);
  - **D** = valor ausente, zerado ou implausível (`> R$ 1 bilhão`).
- A regra `n < 5` **já existe** no agregado por serviço (`agregado_servicos_classe_a.csv`): serviços com menos de 5 ARTs Classe A recebem "Informação insuficiente para verificar" em vez de mediana.
- O bloqueio de KPI monetário para Classe C/D está implementado e foi validado no dashboard (filtro C+D bloqueia KPIs).
- A base Classe A já carrega um campo **`codigo_atividade`** numérico por ART (ex.: `3367`), além de `municipio_key` já normalizado (sem acento, sem sufixo "-BA").

**[INFERÊNCIA TÉCNICA]**
A arquitetura central — *ART como unidade de valor, classe de confiabilidade como gate, serviço como eixo de agregação* — está correta e defensável. O desenho evita os dois erros mais graves apontados no contexto (tratar valor de linha como honorário individual; somar linhas da mesma ART).

---

## 2. O que foi implementado (inventário funcional)

**[FATO VERIFICADO]** Estão produzidos e populados:
- `base_classe_a_servicos_metodologia.csv` — base analítica Classe A (17 colunas, sem texto livre de atividade exposto: `atividade_original` = "Informação insuficiente para verificar" por decisão de não expor texto detalhado).
- `agregado_servicos_classe_a.csv` — 17 serviços com n, mediana, Q1, Q3, IQR, min, max, municípios e modalidades distintos.
- `frequencia_total_servicos.csv` — frequência por serviço e por classe (A / B / C+D).
- `resumo_classes_confiabilidade.csv` — quadro de classes com uso permitido/proibido.
- `dados_metodologia_servicos.json` + `dashboard_senge_honorarios_metodologia_servicos.html` — dashboard validado no navegador.
- Dimensões municipais auxiliares: `dim_municipios_bahia.csv`, `dim_municipio_crea.csv`, `dim_crea_unidades.csv` (estas com `codigo_ibge` e jurisdição CREA majoritariamente em "Informação insuficiente para verificar").

---

## 3. O que foi validado no dashboard

**[FATO VERIFICADO]** (conforme contexto e dados):
- Sem filtro: 230.928 ARTs; base Classe A 53.190; classes A/B/C/D = 23,0% / 16,7% / 27,0% / 33,2%.
- Filtro Classe C+D bloqueia KPIs monetários.
- Filtro Fotovoltaica: 31.811 ARTs; Classe A 1.645; mediana R$ 1.000; IQR R$ 100–R$ 1.500 (coerente com `agregado_servicos_classe_a.csv`).

**[INFERÊNCIA TÉCNICA]** A validação foi de **comportamento de interface e coerência de totais**, não uma validação estatística do valor por serviço. São coisas diferentes: o painel "funciona", mas isso não certifica que cada mediana por serviço seja um parâmetro de honorário utilizável.

---

## 4. Quais números são confiáveis

**[FATO VERIFICADO / alta confiança estrutural]:**
- Totais de volume: 230.928 ARTs; distribuição por classe (53.190 / 38.631 / 62.327 / 76.780).
- Frequências por serviço (demanda relativa) — inclusive a evidência de **serviços novos/lacunas** com alta frequência (Fotovoltaica 31.811; Receituário 5.495; Topografia 5.422; Ambiental 5.003).
- A contagem `n` de Classe A por serviço.

**[INFERÊNCIA TÉCNICA]** Esses números são confiáveis **como medida de demanda e de existência de serviço**, que é exatamente o papel atribuído à base total e às classes C/D no desenho.

---

## 5. Quais números são preliminares

**[FATO VERIFICADO]**
- As **medianas/IQR por serviço** dependem de: (a) qualidade do mapeamento atividade→serviço (hoje por palavra-chave, ~55% de cobertura); (b) o pressuposto de que "valor da ART de linha única ≈ valor do serviço".
- O serviço **"Não mapeado"** concentra 102.554 ARTs (≈45%) e 19.975 Classe A, com mediana R$ 2.200 e IQR R$ 1.000–R$ 15.000 — ou seja, ~38% da base monetária Classe A está num bucket sem serviço atribuído.

**[INFERÊNCIA TÉCNICA]** Toda estatística monetária por serviço é **preliminar** enquanto 38% da base Classe A estiver fora de serviço identificado. Reclassificar o "Não mapeado" pode mover medianas de serviços específicos.

---

## 6. Quais valores por serviço exigem cautela (casos concretos)

**[FATO VERIFICADO]** em `agregado_servicos_classe_a.csv`:
- **Pavimentação / Estradas**: mediana **R$ 1.298.877,78**, Q3 R$ 10.000.000, max R$ 142.650.788 (n=846). Valor típico de **obra**, não de honorário — sinal claro de que ARTs de obra com valor de contrato estão entrando como "valor".
- **Receituário Agronômico**: mediana **R$ 1,72** (n=549). Provável valor simbólico/taxa, não honorário de projeto.
- **Climatização/Ventilação**: mediana R$ 9.465,80 com Q3 R$ 58.634 (n=956) — dispersão altíssima.
- **Estrutura/Cálculo Estrutural**: mediana R$ 5.000, Q3 R$ 30.434 (n=3.168).
- **"Não mapeado"**: max R$ 819.308.220 — confirma que mesmo Classe A contém valores de contrato/obra, não honorário líquido.

**[INFERÊNCIA TÉCNICA]** A mediana é robusta a outliers, mas **a natureza do valor declarado é heterogênea** (honorário, valor de obra, taxa simbólica). A classe A reduz o risco de *mistura entre atividades*, mas **não** separa "valor de honorário" de "valor de contrato de obra". Esse é um limite conceitual da fonte, não um erro do pipeline.

**[RECOMENDAÇÃO]** Nenhum valor por serviço deve ser apresentado como "honorário de referência" antes de: (i) reduzir o bucket "Não mapeado"; (ii) separar, por código TOS/CREA, atividades de elaboração técnica (projeto, laudo) de atividades de execução de obra. Até lá, usar sempre o rótulo "valor declarado em ART, não honorário líquido".

---

## 7. Riscos do bucket "Não mapeado"

**[FATO VERIFICADO]** 102.554 ARTs (≈45% do total), 19.975 Classe A (≈38% da base monetária A).
**[INFERÊNCIA TÉCNICA]** É o **maior risco metodológico atual**. Detalhado em `DIAGNOSTICO_BUCKET_NAO_MAPEADO_TOS.md`.

## 8. Riscos da granularidade ampla

**[FATO VERIFICADO]** A granularidade atual é de ~18 famílias amplas; nenhum serviço ficou com `n < 5` nessa granularidade.
**[INFERÊNCIA TÉCNICA]** Famílias amplas (ex.: "Instalações Elétricas") agregam subserviços com unidades de referência distintas (BTN/m², kWp, hora). Uma mediana de família ampla **mistura modalidades** e perde aderência à lógica da tabela atual (por serviço). Ao descer para subserviço, muitos cairão em `n < 5` — por isso a regra de supressão precisa operar **no nível de subserviço** (ver `MODELO_SUBSERVICOS_E_SUPRESSAO_N5.md`).

## 9. Riscos da padronização municipal

**[FATO VERIFICADO]** `cidade_obra` tem 1.984 grafias distintas; as dimensões municipais existentes têm `codigo_ibge` = "Informação insuficiente para verificar".
**[INFERÊNCIA TÉCNICA]** Sem chave IBGE validada, qualquer recorte territorial é por grafia, sujeito a duplicações (acentos, abreviações, "-BA"). Recortes por inspetoria/SUREG **não podem** ser feitos hoje sem inventar jurisdição (ver `ESPECIFICACAO_PADRONIZACAO_MUNICIPIOS.md`).

---

## 10. O painel pode ser usado internamente?

**[RECOMENDAÇÃO] SIM, com ressalvas**, para uso interno do SENGE/grupo técnico, como:
- ferramenta de **diagnóstico de demanda** (frequência por serviço, identificação de lacunas);
- **prova de conceito** da metodologia (ART como unidade, classe de confiabilidade, gate C/D);
- base de discussão para definir granularidade e prioridades.

Condições para uso interno: manter os rótulos de cautela visíveis; não tratar mediana por serviço como preço; registrar que 38% da base A está em "Não mapeado".

## 11. O painel pode ser apresentado externamente?

**[RECOMENDAÇÃO] AINDA NÃO** para apresentação externa (assembleia ampla, contratantes, público, imprensa, outros conselhos), enquanto:
- o bucket "Não mapeado" representar ~45% da base e ~38% da base A;
- valores de obra (ex.: Pavimentação R$ 1,3 mi) aparecerem misturados a honorários;
- não houver separação por código TOS entre elaboração técnica e execução de obra.

**Risco concorrencial/LGPD:** apresentar "valores por serviço" externamente, mesmo como mediana, pode ser lido como **tabela de preços/tabelamento**, com risco concorrencial; e a base contém microdados que não devem circular. Externamente, só linguagem de *referência técnica orientativa* e indicadores de demanda — nunca valor como preço.

## 12. Em que condições liberar para externo

**[RECOMENDAÇÃO]** Apresentação externa fica condicionada a, no mínimo:
1. bucket "Não mapeado" reduzido a patamar defensável (meta a definir; ver diagnóstico);
2. separação obra × elaboração técnica via TOS;
3. subserviços com unidade de referência coerente com a tabela atual;
4. municípios padronizados por IBGE;
5. texto institucional explícito de que se trata de **subsídio metodológico orientativo**, não preço mínimo/obrigatório.

---

## Síntese da revisão
A pipeline está **conceitualmente correta e bem implementada** no que se propôs. O gargalo não é o HTML nem o cálculo: é a **qualidade do mapeamento atividade→serviço** e a **natureza heterogênea do valor declarado**. A próxima etapa correta é refinamento por TOS + padronização municipal — não retrabalho do dashboard.
