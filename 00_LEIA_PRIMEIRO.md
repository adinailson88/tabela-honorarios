# 00 — LEIA PRIMEIRO
## Proposta de Nova Metodologia para a Tabela de Honorários do SENGE/BA

*Pacote técnico gerado em 2026-06-22. Todos os arquivos estão nesta pasta (`PROPOSTA CLAUDE`).
Nenhum arquivo original foi apagado, movido ou alterado.*

---

## O que foi analisado
- **Metodologia existente:** os 2 documentos da pasta `NOVA METODOLOGIA` (pré-projeto e projeto completo),
  mais os artefatos correlatos `TABELA TOS - 2.xlsx`, `CidadessCalculo` e a tabela de honorários atual.
- **Dados de ART:** `ARTs 2022 01022024.csv` (≈146 MB) — perfilado integralmente; demais bases inventariadas.
- **36 arquivos** no total, mapeados em `01_INVENTARIO_ARQUIVOS.csv`.

## Principais achados (verificáveis)
1. A metodologia atual reajusta tudo pelo **CUB** (índice de construção) — frágil para modalidades não-civis;
   o próprio projeto reconhece a limitação.
2. Existe uma **base empírica robusta**: 726.028 registros de atividade / 230.928 ARTs / 2022 / 97% Bahia.
3. Valores de ART são **muito heterogêneos** (mediana R$1.600; IQR R$520–8.000; máximo absurdo de 8,5×10¹¹):
   `valor_contrato` **não é honorário** — é evidência **indireta**, a usar com mediana/IQR.
4. Já há **dois protótipos** subaproveitados: matriz atividade→valor (`TABELA TOS`) e regionalização (`CidadessCalculo`).
5. **111 unidades** de medida — confirma a necessidade de kVA, kWp, hectare, m³ além do m².

## A proposta, em uma frase
Sair de "lista de preços reajustada por um índice" para um **modelo de governança de honorários em
3 camadas + calibração**: catálogo de atividades (CREA) → valor-base por esforço técnico → ajuste
regional → validação contra as ARTs, com saída em **faixas** (piso–referência–teto), caráter
**orientativo** (anti-aviltamento, não tabelamento) e **revisão anual** documentada.

## Limitações (honestidade metodológica)
- ART ≠ honorário; valores exigem revalidação de parsing antes de uso oficial.
- Arquivos .xls antigos (2015–2019) não lidos nesta sessão.
- Normas citadas (Lei 4.591/64, NBR 12.721, Lei 4.950-A/66, atos Confea/Crea) **a confirmar em fonte oficial**.
- Nenhum valor monetário foi calculado/inventado: itens sem base trazem "Informação insuficiente para verificar".

## Arquivos criados (ordem de leitura sugerida)
| # | Arquivo | Conteúdo |
|---|---|---|
| 01 | `01_INVENTARIO_ARQUIVOS.csv` | Todos os arquivos das pastas de entrada, classificados |
| 02 | `02_DIAGNOSTICO_METODOLOGIA_EXISTENTE.md` | O que existe, lacunas, riscos, oportunidades |
| 03 | `03_DIAGNOSTICO_DADOS_ART.md` | Estrutura, volume, qualidade e limites das ARTs |
| 04 | `04_MODELO_CONCEITUAL_TABELA_HONORARIOS.md` | Arquitetura do método (3 camadas + faixas) |
| 05 | `05_METODOLOGIA_ANALITICA_ARTS.md` | Como tratar as ARTs (pipeline reprodutível) |
| 06 | `06_MATRIZ_ATIVIDADES_HONORARIOS.csv` | Esqueleto da tabela (sem valores inventados) |
| 07 | `07_INDICADORES_E_GRAFICOS_RECOMENDADOS.md` | Painel de evidências para defender a proposta |
| 08 | `08_PROPOSTA_INSTITUCIONAL.md` | Documento apresentável (CREA/SENGE/entidades) |
| 09 | `09_ROTEIRO_APRESENTACAO_CREA_SENGE.md` | Roteiro de reunião slide a slide |
| 10 | `10_BACKLOG_PROXIMOS_PASSOS.md` | Tarefas com responsável, insumo e critério de aceite |
| 11 | `11_PROMPTS_CONTINUACAO.md` | Prompts prontos para continuar o trabalho |
| 12 | `12_LOG_EXECUCAO.md` | Registro do que foi feito |
| 13 | `13_CHECKPOINT_CONTINUACAO.md` | Estado e PROMPT PARA CONTINUAR em nova sessão |

## ▶️ Abra `_ABRIR_AQUI.html` (portal de 1 clique)
Um único arquivo que dá acesso a tudo: painel, apresentação, planilha, documentos e dados.

## 🆕 Dashboard, dados e planilha (já prontos)
- **`dashboard/index.html`** — painel interativo (1 clique; requer internet) com **mapa da Bahia
  (localização das ARTs)**, KPIs, gráficos por município/modalidade/unidade/tipo, e **faixas por
  atividade × unidade** (calibração). Para Google Sites: ver `COMO_PUBLICAR_E_ABRIR.md`.
- **`PLANILHA_MODELO_HONORARIOS.xlsx`** — estrutura da tabela com **1.047 itens** (Atividade × Unidade),
  faixas observadas (piso P25 / referência mediana / teto P75); honorário-referência pendente de
  pesquisa de preços (não inventado).
- **`APRESENTACAO_CREA_SENGE.pptx`** — deck editável (11 slides) para a reunião.
- **`NOTA_TECNICA.md`** e **`MINUTA_RECOMENDACAO_TECNICA.md`** — documentos institucionais.
- **`dados/`** — CSVs agregados (LGPD) + `data.json`; **`scripts/`** — pipeline reprodutível.
- **`COMO_PUBLICAR_E_ABRIR.md`** — abrir em 1 clique + publicar no Google Sites.

## Próximos passos imediatos (do backlog)
1. **A1** — Rotina de parsing robusto do CSV de ARTs.
2. **A3** — Dicionário atividade→código CREA (reusar `TABELA TOS`).
3. **B1/B2** — Definir valor-hora/tempo técnico e calibrar faixas (mediana/IQR).
4. **C1** — Pesquisa de preços com entidades (≥5 por item).
5. **D1** — Confirmar normas em fonte oficial.

---
*Este é um material de subsídio técnico. Os valores da tabela só devem ser preenchidos após
a pesquisa de preços e a calibração — sem invenção de números.*
