# 10 — Backlog de Próximos Passos

> Tarefas com: prioridade · descrição · responsável sugerido · insumo necessário · produto esperado · risco · critério de aceite.
> Prioridade: **P1** (crítica) · **P2** (importante) · **P3** (desejável).

---

## A. Dados

**A1 — Rotina de parsing robusto do CSV de ARTs · P1**
- Resp.: Adinailson/analista de dados. Insumo: `ARTs 2022 01022024.csv`.
- Produto: script que reconstrói colunas (atividade com `;` interno) e exporta agregados.
- Risco: desalinhamento de campos → valores errados. Aceite: amostra de 100 linhas conferida manualmente.

**A2 — Consolidar série histórica 2015–2022 · P2**
- Insumo: bases .xls/.xlsx por semestre (instalar leitor de .xls). Produto: base única limpa.
- Risco: formatos heterogêneos. Aceite: contagens por ano batem com os arquivos de origem.

**A3 — Dicionário atividade→código CREA · P1**
- Insumo: `TABELA TOS - 2.xlsx`. Produto: tabela de-para texto livre → Nível+Atividade.
- Risco: cobertura parcial (27 mil variações). Aceite: ≥80% dos registros mapeados.

## B. Metodologia

**B1 — Definir valor-hora de referência e tempo técnico por atividade · P1**
- Resp.: comissão técnica. Insumo: piso profissional (confirmar Lei 4.950-A/66), parâmetros de engenharia.
- Produto: parâmetros do valor-base (doc. 04). Risco: arbitrariedade. Aceite: parâmetros documentados e aprovados.

**B2 — Calibrar faixas (piso/ref/teto) com mediana e IQR das ARTs · P1**
- Insumo: A1+A3. Produto: faixas por atividade×unidade×região. Aceite: faixas com n≥5 e ressalva metodológica.

**B3 — Definir índice de atualização por modalidade · P2**
- Produto: regra de reajuste fundamentada (CUB e alternativas). Aceite: justificativa por fonte oficial.

## C. Validação técnica

**C1 — Pesquisa de preços com entidades (≥5 por item) · P1**
- Resp.: comissão + entidades. Produto: base de preços regionalizada. Aceite: cobertura mínima dos itens prioritários.

**C2 — Teste de aderência modelo × ART × pesquisa · P2**
- Produto: relatório de aderência. Aceite: divergências explicadas item a item.

## D. Validação jurídica

**D1 — Confirmar normas citadas em fonte oficial · P1**
- Itens: Lei 4.591/64, NBR 12.721, Lei 4.950-A/66, atos Confea/Crea. Aceite: cada citação com referência oficial.

**D2 — Parecer sobre caráter orientativo (anti-cartel) · P1**
- Resp.: assessoria jurídica do SENGE. Produto: parecer. Aceite: redação da tabela ajustada ao parecer.

## E. Comunicação institucional

**E1 — Nota técnica de lançamento · P2** — Produto: nota assinada. Aceite: aprovada pela diretoria.
**E2 — Apresentação para CREA-BA/entidades · P2** — Insumo: doc. 09. Aceite: agenda realizada.

## F. Dashboard

**F1 — Painel de evidências (HTML/PDF) · P2**
- Insumo: agregados (A1). Produto: dashboard (doc. 07). Aceite: gráficos 1–11 com n e ressalvas, sem dado pessoal.

## G. Planilha

**G1 — Planilha-modelo da tabela (faixas) · P2**
- Insumo: B2. Produto: .xlsx versionável. Aceite: estrutura do doc. 08 §8, sem valores inventados.

## H. Apresentação

**H1 — Slides finais · P3** — Insumo: doc. 09 + dashboard. Aceite: deck revisado.

## I. Consulta às entidades

**I1 — Consulta pública/coleta de feedback · P2** — Produto: consolidado de sugestões. Aceite: respostas tratadas.

## J. Governança de atualização

**J1 — Definir ciclo anual + responsáveis + versionamento · P2**
- Produto: regimento de atualização. Aceite: aprovado e publicado.
**J2 — Política de dados/LGPD do projeto · P1** — Produto: política escrita. Aceite: cobre agregação, supressão n<5, vedação a ranking.

---

*Documento derivado. Não altera os arquivos originais.*
