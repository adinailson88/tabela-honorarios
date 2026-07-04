# REDESENHO FUNCIONAL DO DASHBOARD (PÓS-CODEX)
## Arquitetura de páginas/seções recomendada para o painel de honorários SENGE/BA

> Avalia o dashboard atual (página única com seções) e propõe a organização funcional ideal por página.
> O painel corrigido pelo Codex é uma **página única** com as seções: Mapa, Top 10 municípios, Tipo de
> ART, Atividades por modalidade, Atividades por unidade, % precificável, Evolução por ano, CUB,
> Precificação por atividade (TOS), Faixas por atividade×unidade, Precificabilidade por tipo, Tabela
> agregada filtrada, Metodologia. Data: 2026-06-23.

---

## Legenda de prioridade
**P0** = já existe / consolidar · **P1** = próxima rodada · **P2** = quando houver fonte/dado · **P3** = futuro.

---

### 1. Visão Geral
- **Objetivo:** retrato rápido da base (volume, período, cobertura) e mensagem institucional.
- **Filtros:** todos (Ano, Município, Modalidade, Unidade, Tipo).
- **KPIs:** nº de linhas de atividade, nº de ARTs distintas, nº de municípios, período (2015–2022).
- **Gráficos:** evolução anual (linha); top municípios (barras).
- **Tabela:** —
- **Mensagem institucional:** "Subsídio técnico orientativo; ART é evidência auxiliar; não é tabelamento."
- **Riscos de interpretação:** confundir período (deixar 2015–2022 explícito); contagem ≠ honorário.
- **Prioridade:** **P0** (consolidar; hoje espalhado em várias seções).

### 2. Atividades
- **Objetivo:** o que é feito (atividades, modalidades, unidades).
- **Filtros:** todos.
- **KPIs:** nº de atividades; modalidade dominante; unidade dominante.
- **Gráficos:** atividades por modalidade; atividades por unidade; top atividades (TOS).
- **Tabela:** top atividades com contagem.
- **Mensagem:** "Contagens são confiáveis; refletem frequência, não valor."
- **Riscos:** texto livre de atividade é heterogêneo (depende de dicionário/normalização).
- **Prioridade:** **P0**.

### 3. Honorários e valores declarados
- **Objetivo:** faixas de valor por atividade×unidade (piso/referência/teto).
- **Filtros:** Modalidade, Unidade, Município, Ano (ver limitação).
- **KPIs:** mediana, P25, P75 (atualmente **globais**, não filtrados — ver lacuna).
- **Gráficos:** faixas por combinações atividade×unidade.
- **Tabela:** calibração atividade×unidade (mediana/IQR/n/confiabilidade).
- **Mensagem:** "Valor declarado ≠ honorário; usar mediana e IQR, nunca média."
- **Riscos:** **KPIs de valor hoje não respondem aos filtros** (base sem microdados monetários).
- **Prioridade:** **P1** (tornar filtrável — maior ganho analítico).

### 4. Distribuição estatística
- **Objetivo:** dispersão e outliers (mediana, quartis, IQR, CV) por recorte.
- **Filtros:** todos.
- **KPIs:** mediana, IQR, CV, n (com supressão n<5).
- **Gráficos:** boxplot/violino por modalidade ou unidade; histograma de faixas.
- **Tabela:** estatística-resumo por recorte.
- **Mensagem:** "Outliers exigem mediana/IQR; média é enganosa."
- **Riscos:** exige agregado estatístico por recorte (ainda inexistente na base interativa).
- **Prioridade:** **P1** (depende de novo agregado — ver `PROMPT_CODEX_PROXIMA_RODADA.md`).

### 5. Municípios
- **Objetivo:** distribuição geográfica das atividades.
- **Filtros:** todos.
- **KPIs:** município líder; nº de municípios com ART (161 de 417).
- **Gráficos:** top municípios; (futuro) mediana por município.
- **Tabela:** atividades por município.
- **Mensagem:** "Cobertura parcial (161/417 municípios); leitura comparativa, não censitária."
- **Prioridade:** **P0**.

### 6. Inspetorias e SUREG
- **Objetivo:** análise por unidade territorial do CREA-BA.
- **Filtros:** Unidade CREA, Tipo de unidade, Supervisão (quando existirem).
- **KPIs:** atividades por inspetoria; municípios por inspetoria.
- **Gráficos:** barras por inspetoria.
- **Tabela:** município → unidade CREA (com fonte/confiabilidade).
- **Mensagem:** "Associação só com fonte oficial; sem isso, 'Informação insuficiente para verificar'."
- **Riscos:** **inventar jurisdição** — proibido. Depende do Regulamento das Inspetorias.
- **Prioridade:** **P2** (depende de fonte oficial — ver `DIAGNOSTICO_TERRITORIAL_CREA_BA.md`).

### 7. Modalidades profissionais
- **Objetivo:** perfil por modalidade (civil, elétrica, agronomia, etc.).
- **Filtros:** todos.
- **KPIs:** modalidade líder; nº de modalidades.
- **Gráficos:** atividades por modalidade; unidades dominantes por modalidade.
- **Tabela:** modalidade × atividades típicas.
- **Mensagem:** "Cada modalidade tem unidades próprias (kVA, kWp, hectare) — não usar só m²."
- **Prioridade:** **P0**.

### 8. Mapa
- **Objetivo:** visão coroplética por município.
- **Filtros:** todos (espelham a base filtrada).
- **KPIs:** —
- **Gráficos:** mapa Leaflet + malha IBGE; destaque do município selecionado.
- **Mensagem:** "Requer internet (Leaflet/OSM/IBGE)."
- **Riscos:** indisponível offline; casamento de nomes município↔malha.
- **Prioridade:** **P0** (validar visualmente) / coroplético por valor → **P1**.

### 9. Metodologia
- **Objetivo:** transparência (origem, tratamento, limites, LGPD, concorrência).
- **Conteúdo:** versão ampliada (`METODOLOGIA_DASHBOARD_VERSAO_INSTITUCIONAL.md`).
- **Mensagem:** frase-chave da ART como evidência auxiliar.
- **Prioridade:** **P0** (substituir redação atual pela versão institucional; corrigir período e filtros).

### 10. Dados e limitações
- **Objetivo:** ficha técnica honesta da base.
- **Conteúdo:** período (2015–2022), volume, cobertura (161/417), o que NÃO é possível afirmar,
  pendências (territorial, normas, distribuição filtrável), data de geração.
- **Mensagem:** "Material de subsídio; valores monetários só após pesquisa de preços."
- **Prioridade:** **P1** (hoje diluído; consolidar em uma seção própria).

---

## Recomendação de organização
Manter **página única navegável** (mais simples de publicar no Google Sites), porém com um **menu/âncoras
no topo** agrupando as seções nas 10 categorias acima. Promover **Visão Geral**, **Metodologia** e
**Dados e limitações** a blocos de destaque. As páginas 4 (Distribuição) e 6 (Inspetorias) ficam como
**placeholders honestos** ("em construção / depende de dado") até as próximas rodadas.

---
*Documento de redesenho. Não altera o dashboard.*
