# 00 — LEIA PRIMEIRO (PÓS-CODEX)
## Estado atual da proposta de nova metodologia da tabela de honorários — SENGE/BA

> Resumo executivo após a correção do dashboard pelo Codex e a revisão técnico-institucional pelo Claude.
> Nenhum arquivo original foi apagado, movido ou sobrescrito. Data: 2026-06-23.

---

## O que o CODEX fez
- Criou versão corrigida do dashboard: `dashboard_senge_honorarios_corrigido_codex.html` (original preservado).
- Implementou **filtros multisseleção** (ano, município, modalidade, unidade, tipo de ART) com lógica
  centralizada `normalizeKey`, regra **OU dentro do filtro / E entre filtros**, **botão limpar**,
  **indicador de filtros ativos** e **contador filtrado/total**.
- Adicionou **tabela agregada filtrada** e seção **Metodologia** (com a frase-chave da ART como evidência
  auxiliar).
- Criou dimensões territoriais **sem inventar** (CSVs com "Informação insuficiente para verificar").
- Fez backup (`BACKUP_CODEX_DASHBOARD`), teste Python (`teste_filtros_codex.py`) e `node --check` do JS.

## O que o CLAUDE revisou (e descobriu)
- Confirmou que as correções do Codex são **reais** (verificadas no HTML e nos dados).
- **Achado novo importante:** a base do painel cobre **2015–2022** (não só 2022); soma ~1,6 milhão de
  linhas de atividade. Os números do teste (ex.: Salvador = 184.099) são de **8 anos**, não de 2022.
- **Inconsistência de metadados:** `data.json` ainda diz fonte "2022" e total de 726.028 (só 2022).
- A **Metodologia descreve filtros que não existem** (inspetoria/SUREG/situação/grupo/faixa).
- **KPIs de valor não respondem aos filtros** (base interativa só tem contagens; sem microdado monetário).
- Pesquisou as **unidades territoriais oficiais do CREA-BA** (27 inspetorias listadas / "24" declaradas;
  5 escritórios regionais) e confirmou **417 municípios** na Bahia (IBGE).
- Produziu 11 documentos de revisão (lista no fim).

## Estado atual do dashboard
**Funcional e metodologicamente honesto no essencial.** Filtros, agregações, tabela e Metodologia operam.
Pendências: período ambíguo nos metadados, redação à frente da base, distribuição estatística não
filtrável, dimensão territorial vazia, mapa não validado visualmente.

## Riscos remanescentes
| Risco | Ação |
|---|---|
| Leitura errada do período (2015–2022 vs "2022") | Padronizar metadados + rótulo visível |
| Metodologia promete filtros inexistentes | Corrigir redação |
| KPIs de valor não filtram | Sinalizar como global; planejar distribuição filtrável |
| Território (município→inspetoria) vazio | Só preencher com fonte oficial (Regulamento CREA-BA) |
| Mapa depende de internet | Validar visualmente com rede |
| 2024/2026 → 0 silencioso | Adicionar aviso padrão |

## O que VOCÊ deve testar manualmente
Rodar `ROTEIRO_TESTE_VISUAL_USUARIO.md` com **internet ligada** (17 passos com campos de aprovação).

## O que depende de FONTE OFICIAL
- Jurisdição município → inspetoria (Regulamento das Inspetorias do CREA-BA).
- Número exato de inspetorias e existência de "SUREG" no CREA-BA.
- Códigos IBGE dos municípios.
- Confirmação das normas citadas (Lei 4.950-A/66, Lei 5.194/66, Resolução Confea 1.074/2016, NBR 12.721).

## O que JÁ PODE ser apresentado
- A **arquitetura metodológica** (faixas + calibração + governança) e a proposta institucional.
- O **painel como instrumento de apoio**, desde que dito em voz alta que o período é **2015–2022** e que
  ART é **evidência auxiliar**, não prova de honorário.
- O **diagnóstico territorial** (unidades identificadas) como mapa de trabalho.

## O que AINDA NÃO deve ser apresentado como definitivo
- Qualquer **valor monetário de honorário** (depende de pesquisa de preços).
- Qualquer **associação município → inspetoria** (depende de fonte oficial).
- A **distribuição estatística filtrável** (ainda não existe no painel).
- Números como se fossem de 2022 sem corrigir o rótulo de período.

## Próximos passos (em ordem)
1. Rodar o teste visual (`ROTEIRO_TESTE_VISUAL_USUARIO.md`).
2. Enviar `PROMPT_CODEX_PROXIMA_RODADA.md` ao Codex com os achados do teste.
3. Padronizar período/fonte e corrigir a Metodologia do painel.
4. Solicitar ao CREA-BA a jurisdição oficial + códigos IBGE.
5. Planejar a distribuição estatística filtrável.
6. Pesquisa de preços + parecer jurídico de enquadramento orientativo.
7. Publicar a v1 com nota técnica e changelog.

---

## Documentos desta revisão (criados nesta rodada)
1. `REVISAO_CLAUDE_POS_CODEX.md` — revisão crítica do pacote Codex.
2. `AUDITORIA_METODOLOGICA_DASHBOARD.md` — auditoria dos 14 critérios.
3. `METODOLOGIA_DASHBOARD_VERSAO_INSTITUCIONAL.md` — metodologia ampliada.
4. `DIAGNOSTICO_TERRITORIAL_CREA_BA.md` — unidades CREA-BA + fontes oficiais.
5. `MODELO_TERRITORIAL_DASHBOARD.md` — modelo de dados territorial.
6. `REDESENHO_FUNCIONAL_DASHBOARD_POS_CODEX.md` — páginas/seções recomendadas.
7. `ROTEIRO_TESTE_VISUAL_USUARIO.md` — teste passo a passo.
8. `PROPOSTA_INSTITUCIONAL_TABELA_HONORARIOS_POS_DASHBOARD.md` — proposta institucional.
9. `ROTEIRO_APRESENTACAO_CREA_SENGE_POS_CODEX.md` — roteiro de reunião.
10. `PROMPT_CODEX_PROXIMA_RODADA.md` — prompt para o Codex.
11. `00_LEIA_PRIMEIRO_POS_CODEX.md` — este resumo.

*Material de subsídio técnico. Caráter orientativo. Nenhum valor, norma ou jurisdição foi inventado.*
