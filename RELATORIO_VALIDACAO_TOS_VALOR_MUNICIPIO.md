# Relatório de validação — TOS + Natureza do Valor + Município

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Natureza:** relatório de validação da rodada. Não altera arquivos originais.

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.

---

## 1. Arquivos usados
**[FATO VERIFICADO]**
- Entrada TOS: `C:\Users\adina\Meu Drive\SENGE\NOVO ARQUIVO\TABELA TOS - 2.xlsx` (abas `Table 1` e `ARTs CREA 2022 (TOS)`).
- Validação municipal: `dim_municipios_bahia.csv` + `CidadessCalculo atualizado 07.11.2024.xlsx` (lista de nomes; sem IBGE).
- Scripts gerados: `gerar_metodologia_servicos_tos_valor_municipio.py`, `build_dashboard_tos_valor_municipio.py`.
- Backup: `BACKUP_TOS_VALOR_MUNICIPIO\` (dashboard anterior, JSON, scripts originais).

## 2. TOS localizada?
**[FATO VERIFICADO] SIM** — ver `RELATORIO_LOCALIZACAO_TOS.md`. Hierarquia com 2.882 códigos; ARTs com Código TOS em 100% das linhas. Cobertura: **subconjunto de 59.764 ARTs** (de 230.928).

## 3. Significado de `codigo_atividade`
**[FATO VERIFICADO]** — ver `DIAGNOSTICO_CODIGO_ATIVIDADE_TOS.md`:
- `codigo_atividade` da base **original** = código interno de atividade do CREA (`73`/`3367`), **não** é TOS.
- O `CÓDIGO TOS` (hierárquico, ex.: `34.6.1.2`) existe **só** no xlsx e resolve 100% pela hierarquia.

## 4. Redução do "Não mapeado" (mesmo subconjunto de 59.764 ARTs)
**[FATO VERIFICADO]**

| Método | "Não mapeado" | % |
|---|---|---|
| Antes — dicionário por palavra-chave (sobre `Atividade Profissional`) | 51.383 | **86,0%** |
| Depois — por Código TOS (nível grupo/subgrupo/serviço) | 0 | **0,0%** |
| Resíduo — sem correspondência na tabela SENGE (candidatos a novo serviço) | 9.164 | **15,3%** |

**[INFERÊNCIA TÉCNICA]** No nível TOS a redução é total (0% não mapeado). No nível da tabela atual do SENGE, restam 15,3% como **candidatos a novo serviço** (lacunas), não como erro. O número "antes" (86%) é alto porque a `Atividade Profissional` da aba TOS é genérica para palavra-chave — o que reforça o valor do mapeamento por código.

## 5. Antes/depois do mapeamento
**[FATO VERIFICADO]** Camada TOS — distribuição por classe: A=17.582; B=13.384; C=28.362; D=436 (total 59.764).
**[INFERÊNCIA TÉCNICA]** A camada TOS tem proporção de Classe A maior (29,4%) que a base completa anterior (23,0%) — esperado, por ser um recorte mais bem estruturado.

## 6. Distribuição de natureza do valor
**[FATO VERIFICADO]** (ver `DIAGNOSTICO_NATUREZA_VALOR_ART.md` / `resumo_natureza_valor.csv`):
- provável obra/contrato: 39.569 (66,2%)
- informação insuficiente: 9.083 (15,2%)
- **provável honorário técnico: 6.947 (11,6%)**
- simbólico/taxa: 2.966 (5,0%)
- inconsistente/extremo: 1.199 (2,0%) — inclui 763 outliers IQR reclassificados.

## 7. Serviços com valor confiável
**[FATO VERIFICADO]** (`agregado_servicos_tos_classe_a_valor_confiavel.csv`; Classe A + provável honorário + n≥5): **12 serviços** com referência. Exemplos:
- Meio Ambiente / Licenciamento — n=1.206, mediana R$ 800,00 (IQR R$ 500–R$ 1.200)
- Laudo Técnico — n=340, mediana R$ 700,00
- Consultoria Técnica — n=238, mediana R$ 900,00
- Instalações Elétricas — n=209, mediana R$ 1.200,00
- Vistoria / Perícia — n=108, mediana R$ 1.746,30

## 8. Serviços com valor insuficiente
**[FATO VERIFICADO]** **3 serviços** com n<5 (→ "Informação insuficiente para verificar"): Climatização/Ventilação (n=2), Microgeração/Fotovoltaica (n=1), Receituário Agronômico (n=1). O baixo n decorre do filtro duplo (Classe A **e** provável honorário), que reduz fortemente a amostra desses serviços.

## 9. Municípios padronizados
**[FATO VERIFICADO]** 1.204 chaves; 160 confiabilidade média, 1.044 baixa; `codigo_ibge` = "Informação insuficiente para verificar" (sem fonte IBGE local). Detalhe em `RELATORIO_PADRONIZACAO_MUNICIPIOS.md`.

## 10. Limitações
**[INFERÊNCIA TÉCNICA]**
- Camada TOS = subconjunto (59.764 de 230.928 ARTs); restante "Informação insuficiente para verificar".
- Natureza do valor é inferência conservadora (nível + unidade), não declaração direta.
- Sem IBGE oficial; validação municipal limitada por lista parcial (162 nomes).
- Valor confiável continua sendo **valor declarado em ART, não honorário líquido**.
- Filtro duplo (A + honorário) reduz a amostra de vários serviços a n<5.

## 11. Validação visual — alinhamento das tabelas
**[FATO VERIFICADO]** Testado no navegador (servidor local, dashboard novo):
- `th` com `text-align:center; vertical-align:middle` (confirmado: `thAlign = center`).
- `td` numérico centralizado (`tdNumAlign = center`).
- coluna textual (`td.col-texto`) alinhada à esquerda (`tdTextoAlign = left`).

## 12. Validação visual — formatação monetária em reais
**[FATO VERIFICADO]** Testado no navegador:
- KPI Mediana confiável: **R$ 1.000,00**; IQR: **R$ 600,00 – R$ 1.800,00**.
- Células da tabela de serviços em R$ (ex.: R$ 800,00; R$ 1.200,00; R$ 1.261,44).
- Contagens (n=1.206) **não** formatadas como moeda; percentuais como `%` (ex.: 86,0%, 66,2%); códigos não formatados como moeda.
- Bloqueio monetário confirmado: filtro Classe C → mediana "—" + aviso; natureza "obra/contrato" → mediana "—" + aviso; natureza "honorário" → mediana exibida.
- Sem erros no console (`preview_console_logs` nível error: vazio).

## 13. Próximos passos
**[RECOMENDAÇÃO]**
1. Obter fonte que estenda o Código TOS às 230.928 ARTs (hoje 59.764).
2. Obter lista IBGE oficial (código 7 dígitos) e de-para CREA município→inspetoria/SUREG.
3. Refinar natureza do valor para unidades de energia (kWp/kW) com regra específica.
4. Cruzar o agregado confiável com a tabela atual do SENGE (unidades BTN/m², % CUB) para a etapa de calibração de referência.
5. Formalizar os "candidatos a novo serviço" (15,3%) como backlog de atualização da tabela.
