# Relatório de localização da TOS

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Rodada:** TOS + Natureza do Valor + Município
**Data:** 2026-06-24
**Natureza:** relatório de localização. Não altera arquivos originais.

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.

---

## 1. Pastas pesquisadas
- `C:\Users\adina\Meu Drive\SENGE` (raiz e subpastas: `ANTIGO`, `ATUALIZADO`, `NOVA METODOLOGIA`, `NOVO ARQUIVO`, `PROPOSTA CLAUDE`)
- `C:\Users\adina\Meu Drive\SENGE\ATUALIZADO`
- `C:\Users\adina\Meu Drive\ARTS Adinailson` (e subpasta `analises`)
- `C:\Users\adina\Meu Drive\SENGE\PROPOSTA CLAUDE`

Termos buscados (recursivo, case-insensitive): TOS, tabela de obras, obras e serviços, codigo atividade, código atividade, atividade profissional, Confea, Crea, tabela auxiliar, grupo, subgrupo, complemento.

## 2. Arquivos encontrados (relevantes para TOS)
**[FATO VERIFICADO]**
- **`C:\Users\adina\Meu Drive\SENGE\NOVO ARQUIVO\TABELA TOS - 2.xlsx`** (≈17 MB) — **localizado**. Contém 3 abas:
  1. **`Honorários`** — referência de honorários por atividade com colunas: `Código Nível`, `Nivel`, `Código Atividade`, `Atividade`, `Cód. TOS`, `Descrição`, `Unidade de medida`, `Qtd atividades`, `Valor Médio/unidade`.
  2. **`Table 1`** — **hierarquia oficial TOS**: `Ordem`, `Código` (hierárquico: `1`, `1.1`, `1.1.1`, `1.1.1.1`…), `Grupo`, `Subgrupo`, `Obra/Servico`, `status`. **2.887 linhas; 2.882 códigos** resolvíveis.
  3. **`ARTs CREA 2022 (TOS)`** — ARTs de 2022 **já enriquecidas com Código TOS**: `Código da ART`, `Tipo`, `Data de emissão`, `Cidade da Obra/Serviço`, `UF`, `Títulos`, `Código Nível`, `Nível`, `Código Atividade Profissional`, `Atividade Profissional`, **`CÓDIGO TOS`**, **`Descrição TOS`**, `Unidade de medida`, `Valor da unidade`, `Valor do contrato`, etc. **182.261 linhas; 59.764 ARTs distintas.**
- Outros arquivos de contexto (não-TOS): tabela atual de honorários (`ATUALIZADO`), CUB (PDFs), `CidadessCalculo atualizado 07.11.2024.xlsx` (população IBGE, sem código IBGE), `inspetorias bahia.gsheet` (apenas ponteiro de Google Sheets, sem dados locais).

## 3. A TOS foi localizada?
**[FATO VERIFICADO] SIM.** A hierarquia TOS (aba `Table 1`) e a base de ARTs já mapeada para TOS (aba `ARTs CREA 2022 (TOS)`) estão presentes em `TABELA TOS - 2.xlsx`.

## 4. O arquivo parece oficial?
**[INFERÊNCIA TÉCNICA]** A estrutura é compatível com a TOS do sistema CONFEA/CREA (grupos/subgrupos/obras-serviços com codificação hierárquica e a base de ARTs com `CÓDIGO TOS`/`Descrição TOS`). **A condição de "arquivo oficial homologado" não pôde ser confirmada por metadados/assinatura: "Informação insuficiente para verificar"**. Para uso interno/validação, a estrutura é consistente e 100% resolvível contra a própria hierarquia.

## 5. Limitações
- **[FATO VERIFICADO]** A aba `ARTs CREA 2022 (TOS)` cobre **59.764 ARTs** — um **subconjunto** do universo de **230.928 ARTs** de 2022 usado no pipeline anterior. A interseção com a base Classe A anterior é de **11.051 de 53.190** ARTs.
- **[INFERÊNCIA TÉCNICA]** Logo, a camada TOS **não substitui** a base completa: ela é uma camada de **alta qualidade, porém parcial**. Para as ARTs fora dessa aba, o Código TOS é "Informação insuficiente para verificar".
- A aba inclui ARTs de outras UFs (≈3,3% não-BA); 96,7% são BA.

## 6. Decisão tomada
**[RECOMENDAÇÃO / executado nesta rodada]**
1. Usar **somente** a base local `TABELA TOS - 2.xlsx` (sem fontes externas).
2. Construir a camada TOS a partir da aba `ARTs CREA 2022 (TOS)`, resolvendo grupo/subgrupo/serviço pela aba `Table 1` (100% resolvido).
3. **Não** sobrescrever a base anterior (230.928 ARTs): a camada TOS é gerada em arquivos novos com sufixo `_tos_valor_municipio`.
4. Registrar explicitamente, no dashboard e nos relatórios, que a camada TOS é um **subconjunto** (59.764 de 230.928) e que o restante é "Informação insuficiente para verificar".
