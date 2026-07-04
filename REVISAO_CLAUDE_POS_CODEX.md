# REVISÃO CLAUDE PÓS-CODEX
## Revisão crítica do pacote de correção do dashboard (Codex) — Proposta SENGE/BA

> Revisor: Claude (revisão técnico-institucional). Base: trabalho do Codex preservado.
> Nenhum arquivo do Codex foi apagado, movido ou sobrescrito. Eventual nova versão de
> dashboard, se criada, terá nome distinto (`dashboard_senge_honorarios_revisado_claude.html`).
> Data da revisão: 2026-06-23.

---

## 0. Método desta revisão

Foram lidos integralmente: `RELATORIO_CODEX_CORRECAO_DASHBOARD.md`, `CHECKLIST_TESTE_DASHBOARD.md`,
`LOG_CODEX_DASHBOARD.md`, `TESTE_FILTROS_DASHBOARD.md`, `teste_filtros_codex.py`,
`dim_crea_unidades.csv`, `dim_municipio_crea.csv`, `dim_municipios_bahia.csv` e o HTML
`dashboard_senge_honorarios_corrigido_codex.html`. Além de ler os relatórios do Codex, foram
feitas **verificações independentes** sobre os dados de base (`dados/flat_counts.json` e
`dados/data.json`) e sobre a estrutura do HTML, para confirmar ou contestar o que foi relatado.

---

## 1. O que o Codex corrigiu corretamente (verificado)

| Item | Status verificado |
|---|---|
| Filtros multisseleção (`select multiple`) | ✔ Confirmado — 6 ocorrências de `multiple` no HTML |
| Lógica centralizada `normalizeKey` | ✔ Confirmado — função presente no HTML e no `teste_filtros_codex.py` |
| Regra OU dentro do filtro / E entre filtros | ✔ Confirmado no código de teste e descrito na Metodologia |
| Botão "Limpar filtros" | ✔ Presente |
| Indicador de filtros ativos | ✔ Presente |
| Contador filtrado/total | ✔ Presente |
| Tabela agregada filtrada | ✔ Presente (seção "Tabela agregada filtrada") |
| Seção "Metodologia" no HTML | ✔ Presente |
| Frase-chave sobre ART como evidência auxiliar | ✔ Presente — texto exigido pelo usuário consta literalmente |
| Backup do dashboard original | ✔ Pasta `BACKUP_CODEX_DASHBOARD` criada |
| Dimensões territoriais sem invenção | ✔ Confirmado — CSVs preenchidos com "Informação insuficiente para verificar" e confiabilidade `baixa` |
| Charset UTF-8 no HTML | ✔ Confirmado — acentuação renderiza corretamente |

**Conclusão:** o núcleo funcional relatado pelo Codex é real e está implementado. Não há indício de
"correção declarada, mas não feita".

---

## 2. Problemas críticos que parecem resolvidos

1. **Seleção única → multisseleção.** O defeito central (não conseguir filtrar Itabuna + Ilhéus) foi
   efetivamente resolvido pela conversão para `select multiple` + conjuntos normalizados.
2. **Normalização inconsistente de chaves.** Centralizada em `normalizeKey` (remove acento, padroniza
   espaço, remove sufixo `-BA`/`/BA` no fim, compara em maiúsculas). Coerente entre HTML e teste Python.
3. **Ausência de transparência metodológica no painel.** Resolvido com a seção "Metodologia" embutida.
4. **Risco de invenção territorial.** Resolvido pela postura conservadora (campos marcados como não
   verificáveis em vez de preenchidos por suposição).

---

## 3. Achados independentes desta revisão (NÃO relatados pelo Codex)

> Estes são os pontos mais importantes desta revisão. Eles não contradizem a correção do Codex,
> mas mudam a leitura metodológica do painel e precisam ser tratados antes da apresentação.

### 3.1 A base do dashboard cobre 2015–2022, não apenas 2022 (corrige o diagnóstico anterior)
O `dados/flat_counts.json` contém **8 anos (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022)**,
46.134 registros agregados, somando **1.600.340 linhas de atividade**. Isso **contradiz** o diagnóstico
`03_DIAGNOSTICO_DADOS_ART.md`, que afirmava que apenas 2022 havia sido lido (726.028 linhas). Ou seja:
as bases históricas 2015–2021 **já foram incorporadas** à base agregada do painel em algum momento do
pipeline. Isso é uma **boa notícia** (há série histórica), mas precisa ser documentado e validado.

### 3.2 Inconsistência de metadados entre `flat_counts.json` e `data.json`
- `data.json → fonte` ainda diz: **"ARTs CREA-BA 2022 (ARTs 2022 01022024.csv)"**.
- `data.json → totais.linhas_atividade` = **726.028** (só 2022).
- Mas `flat_counts.json` soma **1.600.340** linhas (2015–2022).

Consequência prática: **os KPIs e os números do teste do Codex referem-se a 8 anos, não a 2022.**
Por isso Salvador aparece com **184.099** atividades no teste, enquanto o diagnóstico 2022 registrava
~85.347 para Salvador. **Os dois números estão certos — só são de períodos diferentes.** O painel
precisa deixar explícito a qual período cada número se refere, ou haverá leitura equivocada na reunião.

### 3.3 A Metodologia do HTML descreve filtros que não existem na base
O texto da seção Metodologia menciona filtros por **"inspetoria, supervisão regional, situação, grupo
de atividade, faixa de valor"**. A base `flat_counts.json` só tem **5 dimensões reais**: ano, município,
modalidade, unidade, tipo de ART. A redação está **à frente da implementação** — descreve capacidade
futura como se fosse atual. Precisa ser ajustada (ver `METODOLOGIA_DASHBOARD_VERSAO_INSTITUCIONAL.md`).

### 3.4 Distribuição monetária NÃO responde aos filtros
Confirmado o que o Codex registrou em "Limitações": `flat_counts.json` contém **apenas contagens**, sem
microdados monetários. Logo, **mediana/IQR não são recalculadas** ao filtrar por município ou modalidade.
As estatísticas de valor exibidas vêm de agregados pré-computados em `data.json` (faixas globais e por
combinação atividade×unidade). **A "Distribuição estatística" filtrável (mediana/quartis por recorte)
ainda não existe** — é a maior lacuna analítica remanescente.

### 3.5 Discrepância na contagem de inspetorias (fonte oficial)
A página oficial do CREA-BA declara **"24 inspetorias"** mas lista **27 nomes** (ver
`DIAGNOSTICO_TERRITORIAL_CREA_BA.md`). Divergência da própria fonte — exige confirmação institucional.

---

## 4. Problemas que permanecem

| # | Problema | Severidade |
|---|---|---|
| P1 | Período da base ambíguo (2015–2022 nos dados vs. "2022" nos metadados) | **Alta** — risco de leitura errada |
| P2 | Metodologia descreve filtros inexistentes (inspetoria/SUREG/situação/grupo/faixa) | Média |
| P3 | Sem distribuição estatística filtrável (mediana/IQR por recorte) | **Alta** (analítica) |
| P4 | Dimensão territorial (município→unidade CREA) vazia | Média — depende de fonte oficial |
| P5 | Mapa, destaque de município e malha IBGE não verificados visualmente | Média — depende de teste em navegador |
| P6 | Filtro 2024/2026 retorna 0 silenciosamente (sem aviso ao usuário) | Baixa/Média (UX) |
| P7 | KPIs de valor não mudam com filtro (pode confundir o usuário) | Média (UX/interpretação) |

---

## 5. Pontos que precisam de validação VISUAL no navegador
(roteiro detalhado em `ROTEIRO_TESTE_VISUAL_USUARIO.md`)
- Se a seção "Metodologia" está realmente visível e acessível na página.
- Se os filtros multisseleção funcionam por clique (Ctrl/Shift) na prática.
- Se KPIs, gráficos e tabela mudam ao filtrar (e quais NÃO mudam — esperado para valores).
- Se o contador filtrado/total muda.
- Se o botão "Limpar filtros" zera a seleção.
- Se o mapa carrega e se o município selecionado é destacado.

## 6. Pontos que dependem de INTERNET
- Carregamento do **Leaflet** (via `unpkg`/CDN).
- **Tiles** do mapa base (OpenStreetMap).
- **Malha municipal** da Bahia (API `servicodados.ibge.gov.br`).
- Sem internet: KPIs, gráficos, tabela e filtros funcionam; **só o mapa** fica indisponível.

## 7. Pontos que dependem de FONTE OFICIAL (CREA-BA / IBGE)
- Lista definitiva de inspetorias/escritórios/SUREG e respectiva **jurisdição municipal**.
- Códigos **IBGE** dos municípios (hoje "Informação insuficiente para verificar" nos 3 CSVs).
- Confirmação das normas citadas na proposta (Lei 4.950-A/66, Lei 5.194/66, Resolução Confea 1.074/2016,
  NBR 12.721) em fonte oficial.

## 8. Pontos que NÃO podem ser verificados nesta sessão
- Se `valor_contrato` de cada ART corresponde a honorário, valor de obra ou valor declarado
  (limitação intrínseca do dado — ver auditoria metodológica).
- Comportamento do mapa em rede real (precisa do teste do usuário).
- Jurisdição exata município→inspetoria sem o Regulamento das Inspetorias do CREA-BA.

---

## 9. Prioridade das próximas ações

1. **(P1) Padronizar o período da base no painel.** Decidir e rotular: o painel é 2015–2022. Corrigir
   `data.json → fonte`/`totais` ou adicionar nota explícita no cabeçalho e na Metodologia.
2. **(Teste) Rodar o roteiro visual** (`ROTEIRO_TESTE_VISUAL_USUARIO.md`) com internet ligada.
3. **(P3) Especificar a distribuição estatística filtrável** como próxima entrega ao Codex
   (exige microdados agregados de valor por recorte — ver `PROMPT_CODEX_PROXIMA_RODADA.md`).
4. **(P4) Confirmar a tabela território** com o CREA-BA (Regulamento das Inspetorias) e IBGE.
5. **(P2/P6/P7) Ajustes de redação/UX**: alinhar Metodologia à base real; avisar quando filtro retorna 0;
   sinalizar que KPIs de valor são globais.
6. **(Normas)** Confirmar a base legal antes da versão institucional final.

---

*Documento de revisão. Não altera o trabalho do Codex.*
