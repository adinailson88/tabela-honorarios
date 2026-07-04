# 12 — Log de Execução

## Sessão 1 — 2026-06-22

### Arquivos lidos / analisados
- `NOVA METODOLOGIA/Pré-Projeto tabela de honorários - SENGE.docx` (lido integralmente).
- `NOVA METODOLOGIA/Projeto tabela de honorários - SENGE.docx` (lido integralmente, 10 capítulos).
- `ARTS Adinailson/ARTs 2022 01022024.csv` (≈146 MB) — perfil agregado calculado direto do arquivo.
- `NOVO ARQUIVO/TABELA TOS - 2.xlsx` — abas e cabeçalhos inspecionados (matriz atividade→valor médio/unid.).
- `SENGE/CidadessCalculo atualizado 07.11.2024.xlsx` — inspecionado (modelo MCDM regional).
- `ARTS Adinailson/Análise ARTs.xlsx` — abas inspecionadas (metodologia de limpeza + semestres).
- Demais 36 arquivos: inventariados (metadados) em `01_INVENTARIO_ARQUIVOS.csv`.

### Arquivos criados (em PROPOSTA CLAUDE)
00_LEIA_PRIMEIRO.md · 01_INVENTARIO_ARQUIVOS.csv · 02_DIAGNOSTICO_METODOLOGIA_EXISTENTE.md ·
03_DIAGNOSTICO_DADOS_ART.md · 04_MODELO_CONCEITUAL_TABELA_HONORARIOS.md ·
05_METODOLOGIA_ANALITICA_ARTS.md · 06_MATRIZ_ATIVIDADES_HONORARIOS.csv ·
07_INDICADORES_E_GRAFICOS_RECOMENDADOS.md · 08_PROPOSTA_INSTITUCIONAL.md ·
09_ROTEIRO_APRESENTACAO_CREA_SENGE.md · 10_BACKLOG_PROXIMOS_PASSOS.md ·
11_PROMPTS_CONTINUACAO.md · 12_LOG_EXECUCAO.md · 13_CHECKPOINT_CONTINUACAO.md

### Decisões tomadas
- Tratar a ART como **evidência indireta** (não prova de honorário) — ressalva em todos os documentos.
- Adotar **mediana + IQR** e **faixas** (não média, não preço único).
- Integrar artefatos já existentes (TOS + CidadessCalculo + tabela atual) num modelo de 3 camadas.
- Não inventar valores: itens sem base recebem "Informação insuficiente para verificar".
- Parsing do CSV por **ancoragem pela direita** (campo `atividade` tem `;` interno).

### Achados principais (verificáveis)
- 726.028 linhas de atividade / 230.928 ARTs / ano 2022 / 97% BA.
- Valores: mediana R$1.600; IQR 520–8.000; máx. 8,5×10¹¹ (erros/heterogeneidade) → exige robustez.
- 111 unidades; m² e "unidade" dominam; kWp (40k) e kVA (11k) já relevantes.
- Modalidades: civil, agronomia, elétrica, segurança, mecânica, ambiental.
- Já existe protótipo de matriz (TABELA TOS) e de regionalização (CidadessCalculo).

### Limitações desta sessão
- Arquivos .xls (2015–2019) não lidos (biblioteca `xlrd` ausente).
- Grandes .xlsx (Relatorio_para_conselheiro, arquivo 2024) não abertos em profundidade.
- Valores do CSV exigem revalidação por rotina dedicada de parsing.
- Normas jurídicas citadas não confirmadas em fonte oficial.

### Pendências / próximos passos
- Ver `10_BACKLOG_PROXIMOS_PASSOS.md` (A1 parsing, A3 dicionário, B1 valor-hora, C1 pesquisa, D1 normas).

### Regras de segurança respeitadas
- Nenhum arquivo original apagado, movido ou alterado. Tudo criado **somente** em PROPOSTA CLAUDE.
- Nenhum dado pessoal exposto (somente agregados).

---

## Sessão 1 (continuação) — Execução A1/B2 + Dashboard

### Feito
- **A1/B2 executados:** `scripts/agrega_arts.py` processou o CSV completo (726.028 linhas) e gerou
  agregados (mediana/IQR/n, supressão n<5, winsorização valor>1e9) em `dados/`:
  `por_municipio.csv`, `por_modalidade.csv`, `por_unidade.csv`, `por_tipo_art.csv`,
  `faixas_valor.csv`, `top_atividades.csv`, `data.json`.
- **Dashboard HTML** criado: `dashboard/index.html` (standalone, JSON embutido) com **mapa da Bahia
  (localização)** + gráficos; `scripts/gera_dashboard.py` o regenera; `dashboard/LEIA_DASHBOARD.md`.

### Resultados verificados
- Mediana geral R$1.570; IQR R$540–8.000; máx. R$841,7 mi (outliers → uso de mediana/IQR confirmado).
- 895 municípios com registro; mapa cobre os 60 maiores (coordenadas aproximadas).
- Modalidades padronizadas: Civil (324.741) > Eletricista (118.365) > Agrônomo (92.344) > Segurança (49.443)...
- Validações: 0 placeholders no HTML; JSON embutido parseável; 60/60 municípios com coordenada.

### Observações
- Medianas por unidade não-homogênea (ex.: metro cúbico, quilômetro) ficam altas por refletirem
  valor total de obra — reforça a ressalva ART≠honorário; calibração fina deve ser por Atividade×Unidade.
- Dashboard requer internet (tiles OSM + Chart.js/Leaflet via CDN).

---

## Sessão 1 (continuação 2) — Calibração A3 + Planilha-modelo + Publicação

### Feito
- **A3/B2 calibração:** `scripts/calibra_atividade.py` extrai Nível+Atividade do texto da ART e calcula
  faixas (mediana/P25/P75) por **Atividade × Unidade homogênea** → `dados/calibracao_atividade_unidade.csv`
  (**1.047 combinações válidas**, n≥5). Top 22 (n≥50) embutidas no dashboard.
- **Dashboard atualizado:** novo gráfico "Faixas por atividade × unidade" (barra IQR + mediana).
- **Planilha-modelo:** `PLANILHA_MODELO_HONORARIOS.xlsx` (abas Leia-me / Tabela (modelo) 1.047 itens / Resumo).
  Faixas observadas preenchidas; `honorario_referencia_R$` = "Informação insuficiente para verificar"
  (não inventado; depende de pesquisa de preços + valor-hora).
- **Guia:** `COMO_PUBLICAR_E_ABRIR.md` (1 clique local + Google Sites por URL/GitHub Pages).

### Resultados verificados
- Calibração coerente: Projeto/m² mediana R$1.500 (IQR 800–5.000); Projeto/kWp R$1.000 (552–2.000);
  Execução instalação/kW R$1.100 (1.000–3.000). Planilha valida (1.048 linhas, 12 colunas).

### Backlog concluído nesta sessão
- A3 (dicionário/normalização de atividade — via parsing do texto), F1 (dashboard), G1 (planilha-modelo).

---

## Sessão 1 (continuação 3) — Documentos institucionais + Deck

### Feito
- `NOTA_TECNICA.md` (subsídio fundamentado nos dados verificados).
- `MINUTA_RECOMENDACAO_TECNICA.md` (caráter orientativo; campos normativos a confirmar).
- `APRESENTACAO_CREA_SENGE.pptx` — 11 slides, gerado por `scripts/gera_apresentacao.py` (python-pptx).
  Paleta profissional (Ocean), sem barras/sublinhados de "slide IA"; QA de conteúdo OK (sem placeholders).
- `COMO_PUBLICAR_E_ABRIR.md` — 1 clique local + Google Sites (URL/GitHub Pages).

### Limitação
- Render visual do .pptx não executado (LibreOffice/soffice ausente no ambiente). Layout feito com
  margens conservadoras; conteúdo conferido via extração de texto. Revisar visualmente ao abrir.

---

## Sessão 1 (continuação 4) — Série temporal + CUB verificável

### Feito
- Instalado `xlrd 2.0.2`; lidas as bases históricas por semestre 2015–2021 (.xls/.xlsx).
- `scripts/serie_temporal.py` → `dados/serie_temporal.csv` (mediana anual 2015–2022).
  Mediana: 2015 R$1.200 → 2022 R$1.570 (~+31%); 2017 R$999,50 → 2022 R$1.570 (~+57%).
- Extraídos valores **verificáveis do CUB** dos PDFs Sinduscon-BA → `dados/REFERENCIA_CUB.md`:
  R-1 Normal Nov/2017 R$1.724,35 → Jun/2024 R$2.341,44 (**+35,8%**).
- Dashboard ganhou **gráfico de evolução (2015–2022)** e **comparação base-100 mercado × CUB**.
- Achado normativo: PDFs citam **NBR 12.721:2006** (projeto dizia "/93") → registrado em doc 02 e REFERENCIA_CUB.

### Ressalvas
- Arquivos .xls têm teto de 65.536 linhas/semestre → contagens 2015–2019 são mínimas (possível truncamento);
  mediana usada como indicativa. Mercado e CUB são grandezas distintas (comparação só de tendência).

---

## Sessão 1 (continuação 5) — Redesign do painel (estilo CREA-BA) + verificação no navegador

### Feito
- `scripts/flat_counts.py` → `dados/flat_counts.json`: contagens por (ano, município, modalidade, unidade, tipo),
  TODOS os anos 2015–2022 (1.600.340 atividades; 46.134 grupos; 739 KB). Corrigidos bugs de `uf` com espaços (.xls)
  e data serial. Contagens aditivas → filtros cruzados corretos.
- **Painel redesenhado** (`scripts/gera_painel.py` → `dashboard/index.html`, 769 KB) no padrão da referência do usuário:
  sidebar com filtros (Ano/Município/Modalidade/Unidade/Tipo), KPIs com ícones, **choropleth oficial do IBGE**
  (malha UF 29 + localidades, join por nome normalizado), gauge, e painéis analíticos (faixas, mercado×CUB).
- **Verificado no navegador** (preview local http.server + Chrome headless):
  417 polígonos IBGE, 158/160 municípios coloridos; KPIs e todos os gráficos OK; filtro cruzado funciona
  (Eng. Civil → 727.107 atividades; mediana base 2022 Civil R$2.800 / Eletricista R$1.500 / Agrônomo R$187 / Segurança R$500).
- Restaurado `.claude/launch.json` (mantidas as duas configs).

### Ressalva
- Screenshot automático expira (carregamento de tiles OSM); verificação feita via DOM/Chart/Leaflet (sem erros de console).

---

## Sessão 1 (continuação 6) — Não-precificáveis, poda de outliers e seletor de atividade (TOS)

### Pedidos do usuário atendidos
1. **Atividades sem unidade não precificáveis:** `calibra_atividade.py` agora tabula precificabilidade por
   tipo de ART (`dados/precificabilidade_por_tipo.csv`) → **~72% precificável**; 198.715 registros sem
   valor/unidade. Dashboard: gauge "% precificável" + card "Precificabilidade por tipo".
2. **Poda de outliers:** faixas recalculadas removendo **20% em cada cauda** (TRIM=0.20, configurável p/ 0.30):
   piso=P20 / referência=mediana / teto=P80, aparados. Flag de **confiabilidade** marca "Baixa (provável
   mistura valor unitário/total)" quando teto>20×mediana.
3. **Seleção de atividade conforme TOS:** novo seletor com **97 atividades**; ao escolher, mostra tabela
   por unidade (piso/ref/teto/confiabilidade). `data.json` ganhou `calibracao_full`, `precificabilidade`,
   `nao_precificavel`, `trim_pct`.

### Atualizados
- `scripts/calibra_atividade.py`, `scripts/gera_painel.py`, `scripts/gera_planilha.py` (faixas aparadas +
  aba "Precificabilidade"), `05_METODOLOGIA_ANALITICA_ARTS.md`, `dashboard/LEIA_DASHBOARD.md`.

### Verificado no navegador
- Gauge 72%; "Projeto" → 47 unidades; Projeto/m² 500/1.500/6.000 (Alta); Projeto/unidade teto 4,6 mi → "Baixa".
- Planilha: 4 abas (Leia-me, Tabela 1.047 itens, Precificabilidade, Resumo).
