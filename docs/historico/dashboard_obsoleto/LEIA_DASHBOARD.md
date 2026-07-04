# Painel de Honorários & ARTs (estilo CREA-BA)

## Como abrir (1 clique)
Dê **duplo clique em `index.html`** (abre no navegador). Requer **internet** para o mapa
(malha IBGE + tiles OSM) e as bibliotecas de gráfico (Chart.js, Leaflet via CDN).
Os dados já estão **embutidos** no arquivo.

## O que tem
- **Sidebar com filtros cruzados:** Ano, Município, Modalidade, Unidade, Tipo de ART (contagens reagem a todos).
- **KPIs:** atividades de ART, municípios, modalidades, mediana (R$), faixa P25–P75, unidades.
- **Mapa coroplético da Bahia** (malha oficial do IBGE, 417 municípios) — cor = nº de atividades no filtro.
- **Gráficos:** top municípios, modalidades, unidades, tipo de ART (rosca), evolução por ano.
- **Gauge "% precificável":** mostra que ~72% das atividades têm valor+unidade; o resto (cargo-função,
  registros sem medida) **não é precificável**. Card "Precificabilidade por tipo de ART" detalha por tipo.
- **Precificação por atividade (TOS):** selecione 1 das 97 atividades e veja a faixa por unidade
  (piso/referência/teto, **com poda de 20% nas pontas**) + **confiabilidade** (sinaliza mistura valor unitário/total).
- **Painéis analíticos (base 2022/histórico):** faixas por atividade × unidade, Mercado × CUB (base 2017=100).

## Verificação (feita no navegador)
- 1.600.340 atividades (2015–2022, BA); 417 polígonos IBGE; 158 municípios coloridos pelo join por nome.
- Filtro por modalidade confere mediana base 2022: Civil R$2.800 · Eletricista R$1.500 · Agrônomo R$187 · Segurança R$500.

## Limites
- **ART ≠ honorário** (valor declarado pode ser de obra/contrato) → mediana/IQR como evidência indireta.
- Contagens de 2015–2019 são **mínimas** (arquivos .xls têm teto de 65.536 linhas/semestre).
- Os painéis de valor são referenciados à base 2022; a mediana do KPI ajusta quando 1 modalidade/unidade é selecionada.

## Regenerar
```
python ../scripts/agrega_arts.py        # agregados base 2022
python ../scripts/calibra_atividade.py  # faixas por atividade x unidade
python ../scripts/serie_temporal.py     # série anual + injeta no data.json
python ../scripts/flat_counts.py        # base achatada p/ filtros cruzados (todos os anos)
python ../scripts/gera_painel.py        # reconstrói este index.html
```
