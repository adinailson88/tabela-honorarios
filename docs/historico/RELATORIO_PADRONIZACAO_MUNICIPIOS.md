# Relatório de padronização municipal

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Natureza:** relatório. Não altera arquivos originais.

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.

---

## 1. Quantidade de grafias originais
**[FATO VERIFICADO]** Na camada TOS (59.764 ARTs), o campo `Cidade da Obra/Serviço` gerou **1.204 chaves municipais distintas** após normalização. (Na base completa de 230.928 ARTs eram 1.984 grafias — a camada TOS é um subconjunto.)

## 2. Quantidade de municípios padronizados
**[FATO VERIFICADO]** (`diagnostico_padronizacao_municipios.csv`):
- **1.204** `municipio_key` distintos gerados.
- **160** com confiabilidade **média** (nome casa a lista local de municípios da Bahia).
- **1.044** com confiabilidade **baixa** (não confirmados na lista local, ou de outra UF).
- A normalização colapsou variações de acento/caixa/UF: ex. `SALVADOR`/`Salvador`; `CAMAÇARI`/`CAMAçARI`/`Camaçari`; `VITÓRIA DA CONQUISTA`/`VITORIA DA CONQUISTA`/`Vitória Da Conquista` → uma única chave cada.

## 3. Quantidade sem identificação confiável
**[FATO VERIFICADO]** 1.044 chaves em confiabilidade **baixa**.
**[INFERÊNCIA TÉCNICA]** O número alto decorre principalmente de a lista local de validação ser **parcial** (apenas **162** municípios; a Bahia tem mais de 400). Logo, muitos municípios legítimos caem em "baixa" por **ausência na lista de referência**, não por erro de grafia. Isso é uma limitação da fonte de validação, não da base de ARTs.

## 4. Exemplos de normalização
**[FATO VERIFICADO]**
- `SALVADOR` + `Salvador` → key `SALVADOR`, label `Salvador` (8.532 ARTs).
- `CAMAÇARI`, `CAMAçARI`, `Camaçari` → key `CAMACARI`, label `Camacari` (2.253 ARTs).
- `VITÓRIA DA CONQUISTA` (6 grafias) → key `VITORIA DA CONQUISTA`.
- `LUÍS EDUARDO MAGALHÃES` (6 grafias) → key `LUIS EDUARDO MAGALHAES`.
Regra: remoção de acentos (NFD), maiúsculas, colapso de espaços, remoção de sufixo de UF (`-BA`/`/BA`).

## 5. Houve uso de código IBGE?
**[FATO VERIFICADO] NÃO.** Não há lista oficial IBGE (código de 7 dígitos) confiável nos arquivos locais:
- `dim_municipios_bahia.csv` traz `codigo_ibge` = "Informação insuficiente para verificar".
- `CidadessCalculo atualizado 07.11.2024.xlsx` tem **população IBGE 2022/2023**, mas **não** o código municipal IBGE.
Portanto, `codigo_ibge` foi preenchido como **"Informação insuficiente para verificar"** em toda a base.

## 6. Limitações
**[INFERÊNCIA TÉCNICA]**
- Sem âncora IBGE, a chave municipal é por **nome normalizado**, sujeita a homônimos entre UFs (ex.: a chave `SALVADOR` apareceu com UF `BA` e `AL` — provável erro de digitação de UF na origem). O campo `uf` foi preservado para auditoria.
- A validação de nomes é limitada pela lista de 162 municípios.
- A camada cobre 59.764 ARTs (subconjunto); para o restante, "Informação insuficiente para verificar".

## 7. Risco de usar municípios sem validação
**[INFERÊNCIA TÉCNICA / RECOMENDAÇÃO]**
- Agregações por município em confiabilidade **baixa** podem conter duplicação residual ou município de outra UF; **não** devem ser apresentadas externamente como recorte territorial definitivo.
- Recortes município×serviço fragmentam a amostra: a maioria cairá em `n < 5`. Para esses, **suprimir valor** e manter só frequência.

## 8. Recomendação para agregação futura por inspetoria/SUREG
**[FATO VERIFICADO]** Não há fonte local segura que mapeie município → inspetoria/SUREG:
- `dim_municipio_crea.csv` e `dim_crea_unidades.csv` têm jurisdição toda em "Informação insuficiente para verificar".
- `inspetorias bahia.gsheet` é apenas um **ponteiro de Google Sheets** (sem dados locais).

**[RECOMENDAÇÃO]**
1. Obter a **lista oficial IBGE** dos municípios da Bahia (código de 7 dígitos) e a **lista oficial CREA-BA** município→inspetoria/SUREG.
2. Só então preencher `codigo_ibge` e criar o recorte por inspetoria/SUREG.
3. **Não inventar jurisdição** — até a fonte existir, qualquer mapa por inspetoria é "Informação insuficiente para verificar".
