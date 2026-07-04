# DIAGNÓSTICO TERRITORIAL — CREA-BA
## Unidades regionais, jurisdição e cartografia para o dashboard de honorários

> Objetivo: identificar, com base em fontes oficiais, a estrutura territorial do CREA-BA (sede,
> inspetorias, escritórios regionais, supervisões/SUREG) e a malha municipal da Bahia, para preparar
> o dashboard a analisar dados por recorte territorial **sem inventar jurisdições**.
> Data: 2026-06-23. Não altera o dashboard.

---

## 1. Fontes consultadas

| Fonte | Tipo | URL | Uso |
|---|---|---|---|
| CREA-BA — página de Inspetorias | Oficial (institucional) | https://www.creaba.org.br/inspetorias/ | Lista de inspetorias e escritórios |
| CREA-BA — Regulamento das Inspetorias Regionais | Oficial (norma interna) | http://www.creaba.org.br/wp-content/uploads/2020/11/Regulamento-Inspetorias-regionais-25-091.pdf | **A consultar** para jurisdição município→inspetoria |
| IBGE — Cidades e Estados / Bahia | Oficial (estatística) | https://www.ibge.gov.br/cidades-e-estados/ba.html | Nº de municípios; códigos IBGE |
| IBGE — malha municipal (API) | Oficial (cartografia) | https://servicodados.ibge.gov.br | Camada usada pelo mapa do painel |

> As bases legais citadas pela página do CREA-BA (Lei 5.194/66 e Resolução Confea nº 1.074/2016) devem
> ser confirmadas em fonte oficial antes de uso normativo. Marcação enquanto não confirmadas:
> "Informação insuficiente para verificar".

## 2. O que foi possível verificar

**Estrutura geral (fonte: CREA-BA / inspetorias):** as inspetorias regionais são órgãos executivos do
CREA-BA, criadas para fiscalizar o exercício profissional em sua área de jurisdição e representar o
Conselho no município/região. A descentralização teve início com a Inspetoria de Vitória da Conquista (1975).

**Malha municipal (fonte: IBGE):** a Bahia possui **417 municípios**. A base do dashboard contém **161
municípios** (apenas os que aparecem nos dados agregados de ART) — ou seja, o painel cobre um subconjunto.

## 3. Unidades identificadas (fonte: página oficial do CREA-BA)

### 3.1 Inspetorias Regionais (lista nominal por município-sede)
Alagoinhas · Barreiras · Bom Jesus da Lapa · Brumado · Camaçari · Cruz das Almas · Eunápolis ·
Feira de Santana · Guanambi · Ilhéus · Irecê · Itaberaba · Itabuna · Jacobina · Jequié · Juazeiro ·
Lauro de Freitas · Luís Eduardo Magalhães · Paulo Afonso · Ribeira do Pombal · Santa Maria da Vitória ·
Santo Antônio de Jesus · Seabra · Serrinha · Teixeira de Freitas · Valença · Vitória da Conquista.

### 3.2 Escritórios Regionais
Barra da Estiva · Campo Formoso · Itapetinga · Poções · Porto Seguro.

### 3.3 Sede
A sede do CREA-BA situa-se em **Salvador**. Endereço completo: *Informação insuficiente para verificar*
(confirmar no site oficial antes de publicar).

## 4. Divergências entre fontes

1. **Contagem de inspetorias.** A página oficial declara **"24 inspetorias"** no texto, mas **lista 27
   nomes**. Divergência da própria fonte → **exige confirmação institucional** antes de fixar o número.
2. **Cobertura municipal.** 417 municípios (IBGE) vs. 161 na base do painel — diferença esperada (só
   municípios com ART aparecem), mas precisa ser comunicada para não sugerir cobertura total.
3. **SUREG.** A sigla "SUREG" (Supervisão/Superintendência Regional) aparece em outros órgãos (Sesab/SGB),
   **não confirmada como estrutura do CREA-BA** nas fontes consultadas. Tratar como **a verificar** —
   não assumir que o CREA-BA usa "SUREG".

## 5. Limitações

- **Não há, nas fontes textuais consultadas, uma tabela município → inspetoria.** A página menciona um
  "mapa de regionalização" e endereços por inspetoria, mas não a jurisdição completa de cada uma.
- A jurisdição definitiva deve estar no **Regulamento das Inspetorias Regionais** (PDF oficial) — ainda
  **não extraído** nesta sessão. Sem ele, **não se deve atribuir** município a inspetoria.
- Códigos **IBGE** dos municípios: ainda "Informação insuficiente para verificar" nos CSVs do Codex;
  podem ser obtidos da tabela oficial de municípios do IBGE.

## 6. Campos recomendados para as dimensões territoriais
(ver detalhamento em `MODELO_TERRITORIAL_DASHBOARD.md`)
`municipio_label · municipio_key · codigo_ibge · unidade_crea_referencia · tipo_unidade ·
supervisao_regional · fonte · confiabilidade · observacao`.

## 7. Recomendação para construir a tabela município → unidade CREA
1. **Extrair** a jurisdição do **Regulamento das Inspetorias Regionais (PDF oficial)** ou solicitar ao
   CREA-BA a planilha oficial município→inspetoria.
2. **Cruzar** com a lista oficial de 417 municípios do IBGE (para obter `codigo_ibge`).
3. Preencher cada associação com **`fonte`** (documento/URL) e **`confiabilidade`** (alta = norma oficial;
   média = inferência geográfica documentada; baixa = não confirmada).
4. **Nunca** preencher por suposição: associação sem fonte permanece "Informação insuficiente para verificar".
5. Validar a tabela final com a área competente do CREA-BA antes de publicar.

## 8. O que ainda depende de confirmação institucional
- Número exato de inspetorias (24 vs. 27).
- Existência e papel de "SUREG"/supervisões no CREA-BA.
- Jurisdição município→inspetoria (Regulamento das Inspetorias).
- Endereço/sede e dados de contato oficiais.
- Códigos IBGE por município (obter da fonte oficial).

---

## Fontes
- CREA-BA — Inspetorias: https://www.creaba.org.br/inspetorias/
- CREA-BA — Regulamento das Inspetorias Regionais (PDF): http://www.creaba.org.br/wp-content/uploads/2020/11/Regulamento-Inspetorias-regionais-25-091.pdf
- IBGE — Bahia (Cidades e Estados): https://www.ibge.gov.br/cidades-e-estados/ba.html

*Documento de diagnóstico. Não atribui jurisdições não verificadas.*
