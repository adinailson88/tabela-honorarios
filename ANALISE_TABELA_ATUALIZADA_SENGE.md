# ANÁLISE DA TABELA ATUALIZADA — SENGE/BA
## Estrutura da tabela de honorários vigente (pasta `ATUALIZADO`)

> Análise da tabela de honorários mais recente disponível, base para a reestruturação por serviço.
> Separa **fato verificado** (lido do arquivo) de **inferência técnica** e de **recomendação**.
> Data: 2026-06-23. Não altera arquivos originais.

---

## 1. Qual é a versão atual/mais recente (FATO VERIFICADO)
A versão mais recente é **`29-07-2024 - Tabela Honorários Adinailson.xlsx`** (com documento companheiro
`29-07-2024 - Tabela honorarios Adinailson.docx`), datada de **29/07/2024**. A pasta `ATUALIZADO` contém
ainda dois PDFs de CUB (`2017-11` e `2024-06`), que são as **bases de conversão monetária** da tabela.

## 2. Como a tabela está estruturada (FATO VERIFICADO)
A planilha é **organizada por serviço**, distribuída em **13 abas temáticas** (famílias de serviço):

| Aba | Família de serviço | Critério de valor | Eixo de cruzamento |
|---|---|---|---|
| 1 | Consultoria | BTN/hora/mês | faixas de horas (até 20/30/40/80/>80) |
| 2 | Direção e Administração de Construções | R$/m² | natureza da obra × simples/correntes/não usual |
| 3 | Fiscalização | BTN/m² | natureza × estrutura/civis/elétricas/comunicações/hidro/gases/ar cond/urbanização |
| 4 | Projetos Civis | BTN/m² | natureza × faixas de área (≤120 … >10.000 m²) |
| 5 | Projeto de Engenharia (Estradas/Ruas) | BTN/Km | tipo de estudo × vias urbanas / estradas <7km / >7km |
| 6 | Cálculo Estrutural (1) | BTN/m² | natureza × tipo de estrutura |
| 6 | Cálculo Estrutural (2) | BTN/m³ | piscinas/reservatórios × faixas de volume |
| 7 | Cálculo Estrutural de residências | %CUB/m² + R$/m² | tipo + adicionais percentuais |
| 8 | Cálculo estrutural de edifícios | %CUB/m² + R$/m² | tipo de edifício |
| 9 | Saneamento | BTN/ha | tipo de rede × faixas de hectare |
| 10 | Instalações Hidráulicas e Mecânicas | BTN/m² | natureza × água/esgoto/ar comprimido/vácuo/vapor/gases/incêndio/ventilação/ar cond |
| 11 | Instalações Elétricas e de Comunicação | BTN/m² | natureza × elétricas/iluminação/rede lógica/telefonia/sonorização/relógio/sinalização/CFTV |
| 12 | Geologia e Minas | R$ fixo | item de serviço (consultoria, perícias, licenciamento, pesquisa DNPM) |

**Observação estrutural importante (FATO):** cada serviço **não tem um valor único** — é uma **matriz**
[natureza da obra (linhas) × subtipo (colunas)] → valor. Um único serviço comporta dezenas de células.

## 3. Critério de valor (FATO VERIFICADO)
O critério é **misto e por serviço**, não por valor fixo único nem por hora técnica geral:
- **por área** (BTN/m²) — predominante (projetos civis, estrutural, fiscalização, instalações);
- **por volume** (BTN/m³) — reservatórios/piscinas;
- **por extensão** (BTN/Km) — estradas e ruas;
- **por área de terreno** (BTN/ha) — saneamento;
- **por hora** (BTN/hora/mês) — consultoria;
- **por percentual do CUB** (%CUB/m²) — cálculo estrutural residencial/edifícios;
- **valor fixo em R$** — geologia e minas.

A unidade histórica de referência é o **BTN**, convertido a reais pelo **CUB**.

## 4. Serviços que aparecem (FATO VERIFICADO)
Consultoria; direção/administração de obras; fiscalização; projetos civis (auditórios, escolas, hospitais,
conjuntos habitacionais, prédios comerciais/industriais etc.); projeto de estradas/ruas; cálculo estrutural
(estruturas convencionais, protendidas, pré-moldadas, lajes especiais; reservatórios, piscinas; residências
e edifícios); saneamento (drenagem, distribuição de água, esgoto); instalações hidráulicas e mecânicas
(água, esgoto, ar comprimido, vácuo, vapor, gases, incêndio, ventilação, ar condicionado); instalações
elétricas e de comunicação (elétricas, iluminação, rede lógica, telefonia, sonorização, CFTV, sinalização);
geologia e minas (perícias, licenciamento mineral, pesquisa DNPM).

## 5. Modalidades/áreas que aparecem (FATO/INFERÊNCIA)
A tabela é **fortemente civil e estrutural**, com instalações prediais (hidráulica/mecânica/elétrica),
saneamento e geologia/minas. **Inferência:** não há blocos próprios para **agronomia**, **engenharia
ambiental**, **segurança do trabalho**, **automação/controle**, **telecom moderno** ou **energia
fotovoltaica** — áreas que, nos dados de ART, têm volume expressivo (ver item 8).

## 6. Unidades de referência que aparecem (FATO VERIFICADO)
m², m³, km, ha, hora/mês, %CUB e R$ fixo. **Ausentes:** **kWp** (fotovoltaica), **kVA/kW** (elétrica de
potência) e **hectare na lógica agronômica** — unidades de alto volume nas ARTs.

## 7. Há atualização monetária? (FATO VERIFICADO)
**Sim.** Cada aba traz **duas versões lado a lado**: coluna **2017-11 (CUB R$ 1.369,12)** e coluna
**2024-06 (CUB R$ 1.929,04)**. O **mecanismo de atualização é a razão do CUB** (variação ~+40,9% de 2017
a 2024). **Inferência:** a atualização é real, porém **amarrada a um único índice (CUB da construção)**,
o que é frágil para modalidades não-civis (problema já reconhecido no projeto interno).

## 8. Atividades ausentes ou defasadas (INFERÊNCIA, confronto tabela × ARTs)
Confrontando a tabela com o vocabulário real das ARTs (FATO verificado nos dados), faltam/estão defasados:
- **Energia solar fotovoltaica / microgeração distribuída** (unidade **kWp**) — dezenas de milhares de
  registros nas ARTs (ex.: "SISTEMA DE MICROGERAÇÃO FOTOVOLTAICA", "geração de energia", "solar");
- **Receituário agronômico / agronomia** (≈60 mil registros) — sem bloco na tabela;
- **Automação/controle**, **telecom moderno**, **eficiência energética**;
- **Engenharia ambiental / licenciamento ambiental**;
- **Agrimensura / georreferenciamento**.

## 9. Indício de que a tabela não incorpora serviços novos (INFERÊNCIA)
Sim. A estrutura é a de uma tabela clássica de obras civis/prediais convertida por CUB. A **ausência de
fotovoltaica (kWp)** — hoje um dos serviços mais frequentes nas ARTs de engenharia elétrica — é o indício
mais claro de que a tabela **não acompanha dinamicamente** o surgimento de novos serviços.

## 10. Campos úteis para a nova matriz de serviços (RECOMENDAÇÃO)
Aproveitáveis da tabela atual: **família/grupo de serviço** (as 13 abas), **serviço**, **natureza da obra**,
**subtipo**, **unidade de referência** e **critério de valor**. Recomenda-se derivar a matriz de serviços
a partir desses campos (ver `MATRIZ_SERVICOS_TABELA_ATUAL.csv`) e **acrescentar** colunas de
*modalidade associada*, *fonte*, *data-base* e *nota de confiabilidade*, além de **novos serviços**
identificados nas ARTs (ver `MATRIZ_TABELA_ATUAL_X_ARTS.csv`).

---

## Síntese
- **Fato:** tabela de 29/07/2024, **por serviço**, 13 famílias, critério misto (m²/m³/km/ha/hora/%CUB/R$),
  com **atualização via CUB** (versões 2017 e 2024).
- **Inferência:** boa base estrutural, mas **defasada em serviços novos** (fotovoltaica, agronomia,
  automação, ambiental) e **dependente de um único índice**.
- **Recomendação:** preservar a lógica **por serviço**, modernizar o catálogo com os novos serviços
  evidenciados nas ARTs e substituir o índice único por atualização **aderente a cada modalidade**.

*Documento derivado. Não altera arquivos originais. Nenhum valor foi inventado.*
