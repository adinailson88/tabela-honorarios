# 00 — LEIA PRIMEIRO: METODOLOGIA POR SERVIÇO
## Separação entre serviço, modalidade, formação e valor declarado nas ARTs — SENGE/BA

> Resumo executivo da rodada que reestrutura a metodologia em torno da **separação por serviço** e do
> **tratamento estatístico dos casos únicos, compostos, duplicados e ambíguos** das ARTs.
> Separa **fato verificado**, **inferência técnica** e **recomendação**. Data: 2026-06-23.
> Nenhum arquivo original foi apagado, movido ou sobrescrito; tudo novo está em `PROPOSTA CLAUDE`.

---

## 1. O que foi descoberto (FATO VERIFICADO)
1. A pasta `ATUALIZADO` contém uma **tabela de honorários utilizável e recente**: `29-07-2024 - Tabela
   Honorários Adinailson.xlsx`, **organizada por serviço**, com **atualização monetária via CUB**.
2. Nos dados de ART (base 2022; 726.028 linhas; 230.928 ARTs), o **valor declarado é da ART inteira, não
   da atividade**: entre as ARTs multi-linha, **99.982 repetem o mesmo valor** em todas as linhas. Somar
   linhas multiplica o valor.
3. **62,6%** das ARTs têm mais de uma linha; **26,5%** têm mais de um código de atividade (escopo
   composto); **32%** não têm valor utilizável.
4. O campo `titulos` traz **uma única modalidade por ART** (não há mistura de modalidade nesse campo);
   a heterogeneidade entra via **múltiplos códigos de atividade** e no nível do catálogo.
5. Há **serviços de alto volume ausentes na tabela**: energia solar **fotovoltaica (kWp)** e
   **receituário agronômico** são os mais evidentes.

## 2. A pasta ATUALIZADO contém tabela atual utilizável? (FATO)
**Sim.** É a base oficial mais recente (29/07/2024), por serviço, em 13 famílias, com duas versões
(2017 e 2024) convertidas por CUB. Detalhe em `ANALISE_TABELA_ATUALIZADA_SENGE.md`.

## 3. Como a tabela está estruturada (FATO)
13 famílias de serviço (consultoria, direção/administração, fiscalização, projetos civis, estradas/ruas,
cálculo estrutural, residências, edifícios, saneamento, instalações hidráulicas/mecânicas, elétricas/
comunicação, geologia/minas). Critério **misto**: BTN/m², BTN/m³, BTN/Km, BTN/ha, BTN/hora/mês, %CUB e
R$ fixo. Cada serviço é uma **matriz** [natureza da obra × subtipo] → valor (não um valor único).
Catálogo derivado em `MATRIZ_SERVICOS_TABELA_ATUAL.csv` (44 linhas; valores marcados como
"Informação insuficiente para verificar", pois cada serviço tem muitas células 2017/2024).

## 4. Como as ARTs podem ser cruzadas com a tabela (INFERÊNCIA/RECOMENDAÇÃO)
Mapeando o texto de atividade das ARTs para os serviços da tabela, com **tipo de correspondência** e
**confiabilidade** explícitos. Cruzamento em `MATRIZ_TABELA_ATUAL_X_ARTS.csv`: correspondências diretas/
aproximadas (ex.: alvenaria→projetos civis; estrutura de concreto→cálculo estrutural; baixa tensão→
instalações elétricas), **serviços novos** (fotovoltaica, receituário, automação, ambiental, agrimensura,
segurança do trabalho) e **serviços da tabela sem evidência** clara nas ARTs (ex.: direção/administração).

## 5. Quais casos podem ser usados para cálculo (INFERÊNCIA, dimensionada)
- **Classe A — alta confiabilidade (linha única, 1 código, 1 valor plausível): 53.190 ARTs = 23,0%**
  (mediana R$ 2.000). **Base primária** do cálculo monetário por serviço.
- **Classe B — composto homogêneo (multi-linha, mesmo código, valor constante): 38.631 = 16,7%.** Pode
  entrar em cálculo **secundário/simulação**, com regra explícita.

## 6. Quais casos excluir ou usar só para frequência (INFERÊNCIA)
- **Classe C — composto ambíguo (múltiplos códigos, valor único): 60.247 = 26,1%.** Apenas **frequência,
  demanda e identificação de novos serviços** — nunca cálculo de valor.
- **Classe D — inválido/sem valor: 76.751 = 33,2%** (+ 29 implausíveis). **Excluir** do cálculo; documentar
  volume e motivo. Detalhe em `TIPOLOGIA_CONFIABILIDADE_ARTS.md`.

## 7. A ponderação é recomendada? (RECOMENDAÇÃO)
**Não como base principal.** Para os casos compostos, o valor é único e replicado, sem informação que
permita repartir entre serviços; qualquer ponderação seria suposição. **Recomendação: usar a Classe A como
base principal e tratar ponderação apenas como análise exploratória secundária**, claramente separada
(detalhe em `METODO_PONDERACAO_SERVICOS_COMPOSTOS.md`).

## 8. Impacto no dashboard (RECOMENDAÇÃO)
Separar três contadores (ARTs / atividades / serviços); criar filtro de **classe de confiabilidade** e de
**serviço padronizado**; mostrar a **base de cálculo (Classe A) separada da base total**; exibir % A/B/C/D;
sinalizar quando o valor vem só de casos únicos ou quando há **apenas frequência** sem valor confiável;
**não** exibir KPIs monetários sobre Classe C/D; destacar **lacunas** da tabela e **novos serviços**.
Detalhe em `IMPACTO_DA_NOVA_METODOLOGIA_NO_DASHBOARD.md`.

## 9. Próximo passo para o Codex
Aplicar a classificação aos dados e ao dashboard sem quebrar os filtros já corrigidos: criar os campos
`id_art, atividade_original, atividade_key, servico_padronizado, grupo_servico, modalidade, formacao,
valor_art, classe_confiabilidade, usar_calculo_monetario, motivo_exclusao_calculo`; deduplicar valor por
ART; separar a base Classe A; gerar agregado por serviço (mediana/IQR/n, supressão n<5). Prompt pronto em
`PROMPT_CODEX_METODOLOGIA_SERVICOS.md`.

## 10. Próximo passo institucional
Apresentar ao CREA-BA/SENGE-BA a tese central: **a tabela segue por serviço; as ARTs entram como evidência
auxiliar; só a base de alta confiabilidade calcula valor**. Adendo institucional em
`ADENDO_METODOLOGICO_SERVICOS_E_ARTS.md`. Em seguida: pesquisa de preços por serviço (para os serviços com
base suficiente) e parecer jurídico do caráter **orientativo**.

---

## Os 12 arquivos desta rodada
1. `ANALISE_TABELA_ATUALIZADA_SENGE.md`
2. `MATRIZ_SERVICOS_TABELA_ATUAL.csv`
3. `DIAGNOSTICO_MISTURA_ATIVIDADE_MODALIDADE_VALOR.md`
4. `TIPOLOGIA_CONFIABILIDADE_ARTS.md`
5. `METODO_DEDUPLICACAO_ARTS.md`
6. `METODO_PONDERACAO_SERVICOS_COMPOSTOS.md`
7. `MODELO_RECOMENDADO_CALCULO_POR_SERVICO.md`
8. `MATRIZ_TABELA_ATUAL_X_ARTS.csv`
9. `IMPACTO_DA_NOVA_METODOLOGIA_NO_DASHBOARD.md`
10. `PROMPT_CODEX_METODOLOGIA_SERVICOS.md`
11. `ADENDO_METODOLOGICO_SERVICOS_E_ARTS.md`
12. `00_LEIA_PRIMEIRO_METODOLOGIA_SERVICOS.md` (este arquivo)

*Material de subsídio técnico. Caráter orientativo. Nenhum valor, norma ou conclusão foi inventado;
o que não pôde ser verificado está marcado como "Informação insuficiente para verificar".*
