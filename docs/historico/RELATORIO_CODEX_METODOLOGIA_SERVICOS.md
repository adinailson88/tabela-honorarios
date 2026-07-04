# RELATÓRIO — IMPLEMENTAÇÃO DA METODOLOGIA POR SERVIÇO E CLASSE DE CONFIABILIDADE
## Pipeline de tratamento das ARTs + dashboard (SENGE/BA)

> Implementação local da metodologia já definida pelo Claude. Não refez a metodologia; aplicou-a aos dados.
> Caráter **orientativo**; apenas agregados; sem dados pessoais; sem ranking. Data: 2026-06-24.

---

## 1. Arquivos lidos
- Referência metodológica: `00_LEIA_PRIMEIRO_METODOLOGIA_SERVICOS.md`, `TIPOLOGIA_CONFIABILIDADE_ARTS.md`,
  `METODO_DEDUPLICACAO_ARTS.md`, `METODO_PONDERACAO_SERVICOS_COMPOSTOS.md`,
  `MODELO_RECOMENDADO_CALCULO_POR_SERVICO.md`, `MATRIZ_SERVICOS_TABELA_ATUAL.csv`,
  `MATRIZ_TABELA_ATUAL_X_ARTS.csv`, `IMPACTO_DA_NOVA_METODOLOGIA_NO_DASHBOARD.md`.
- Dados: `C:\Users\adina\Meu Drive\ARTS Adinailson\ARTs 2022 01022024.csv` (base 2022).
- Tabela atual: `C:\Users\adina\Meu Drive\SENGE\ATUALIZADO` (estrutura por serviço, já analisada).

## 2. Campos encontrados nas ARTs
Separador `;`; o campo `atividade` contém `;` internos (parsing por ancoragem à direita).
Identificados: `id` (identificador único da ART), `tipo_art`, `emissao` (→ ano), `cidade_obra` (→ município),
`titulos` (modalidade/título = formação), `codigo` (código de atividade), `atividade` (texto livre),
`valor_contrato` (→ valor da ART), `quantidade`, `unidade`. **Período:** apenas **2022** (campo de emissão).

## 3. Regras implementadas
- **Deduplicação de valor por ART:** um valor por `id_art`; **nunca** somar linhas (o valor é replicado).
- **Estatística:** **mediana e IQR (Q1–Q3)**; **nunca média simples**.
- **Outliers:** descarte de valores ≤ 0 e implausíveis (> R$ 1 bilhão).
- **Supressão `n < 5`:** serviços sem base estatística recebem "Informação insuficiente para verificar".
- **Privacidade:** saída apenas agregada; o texto livre de atividade não é exposto (campo
  `atividade_original` registrado como "Informação insuficiente para verificar" na base publicada);
  sem identificadores, sem ranking.

## 4. Como foi feita a classificação A/B/C/D (no nível da ART)
- **Classe A** — 1 linha, 1 código, valor plausível (0 < v < 10⁹): valor associável com baixo risco de mistura.
- **Classe B** — multi-linha **homogênea** (mesmo código de atividade, valor único replicado).
- **Classe C** — multi-linha com **múltiplos códigos/atividades** ou valor variável entre linhas (composto
  ambíguo, valor único não decomponível).
- **Classe D** — valor ausente, zerado ou implausível.

## 5. Como foi feita a deduplicação
Agregação por `id_art`: contam-se linhas (`qtd_linhas_art`), códigos distintos (`qtd_codigos_atividade_art`)
e serviços distintos (`qtd_atividades_art`); detecta-se replicação de valor (`valor_replicado_linhas`).
Mantém-se **um** valor por ART. Três contadores ficam separados no painel: **ARTs**, **atividades** e
**serviços** — evitando dupla contagem.

## 6. Mapeamento atividade → serviço (INFERÊNCIA, aproximada)
Classificador por **palavra-chave** (ordem específico→genérico), apoiado também em `tipo_art`
(receituário, cargo-função). Resultado: **18 serviços padronizados**. Atividades sem correspondência
ficam em **"Não mapeado / Informação insuficiente para verificar"**. **Esta é a principal limitação**
(ver §10).

## 7. Quantidades por classe (FATO VERIFICADO — base 2022; 230.928 ARTs)
| Classe | ARTs | % | Uso |
|---|---|---|---|
| A | 53.190 | 23,0% | base principal de cálculo monetário |
| B | 38.631 | 16,7% | análise secundária/simulação |
| C | 62.327 | 27,0% | apenas frequência/diagnóstico |
| D | 76.780 | 33,2% | excluída do cálculo |
*(C inclui os ~2.080 casos de valor variável entre linhas; D inclui 29 valores implausíveis.)*

## 8. Serviços com base suficiente (n ≥ 5, Classe A): **17**
Maiores (mediana | IQR | n): Estrutura/Cálculo Estrutural (R$ 5.000 | 1.300–30.435 | 3.168);
Instalações Elétricas (R$ 2.500 | 1.000–11.289 | 2.929); Edificação em Alvenaria (R$ 1.600 | 800–10.000 | 5.137);
Vistoria/Perícia (R$ 1.500 | 700–4.576 | 2.446); Laudo Técnico (R$ 1.200 | 500–3.000 | 2.510);
Microgeração/Fotovoltaica (R$ 1.000 | 100–1.500 | 1.645); Receituário Agronômico (R$ 1,72 | 1,0–160 | 549).
*(Lista completa em `agregado_servicos_classe_a.csv`.)*

## 9. Serviços com informação insuficiente (n < 5, Classe A): **0**
Nenhum serviço mapeado ficou com n<5 nesta granularidade (há poucas famílias, todas frequentes). A regra de
supressão está implementada e **será acionada** quando o catálogo for refinado em subserviços mais finos.
O serviço **"Não mapeado"** (n=19.975 na Classe A) recebe confiabilidade **baixa** e observação de uso apenas
diagnóstico — não deve ser lido como referência de honorário.

## 10. Limitações
1. **Cobertura do mapeamento (principal):** ~45% das ARTs caem em "Não mapeado" (102.554 no total; 19.975 na
   Classe A). O dicionário por palavra-chave é uma **aproximação** — recomenda-se refiná-lo com os **códigos
   da TABELA TOS / catálogo CREA** para elevar a cobertura.
2. **Período:** apenas **2022** (o CSV traz só emissões de 2022); sem série histórica nesta base.
3. **Granularidade:** 18 famílias amplas; subserviços (por natureza/porte) ainda não separados.
4. **Valor declarado ≠ honorário:** mesmo na Classe A, o valor é evidência **auxiliar/indireta**; medianas
   altas com IQR enorme (ex.: Pavimentação) indicam mistura valor-unitário/total — sinalizar.
5. **Municípios:** 1.984 chaves distintas em `cidade_obra` (inclui grafias e localidades fora da BA) — a base
   precisa de padronização de municípios para análise territorial fina.
6. **Composto (múltiplos serviços):** 30.139 ARTs com mais de um serviço não entram no cálculo por serviço
   (corretamente), apenas em frequência.

## 11. Como testar o dashboard
Abrir `dashboard_senge_honorarios_metodologia_servicos.html` (duplo clique; não requer internet).
Roteiro detalhado em `CHECKLIST_DASHBOARD_METODOLOGIA_SERVICOS.md`. **Verificação automatizada já executada**
(via inspeção do DOM), com resultados confirmados:
- sem filtro: ARTs **230.928**, atividades **320.551**, base Classe A **53.190**, mediana **R$ 2.000**, IQR **800–8.000**;
- barra de classes **A 23,0% · B 16,7% · C 27,0% · D 33,2%**;
- filtro **só C+D**: ARTs **139.107**, base A **0**, KPIs monetários **ocultados** e **aviso exibido**;
- filtro **Microgeração/Fotovoltaica**: ARTs **31.811**, base A **1.645**, mediana **R$ 1.000**, IQR **100–1.500**;
- **Limpar filtros** restaura a base completa.

## 12. Arquivos criados nesta rodada
`base_classe_a_servicos_metodologia.csv` · `agregado_servicos_classe_a.csv` ·
`frequencia_total_servicos.csv` · `resumo_classes_confiabilidade.csv` ·
`dashboard_senge_honorarios_metodologia_servicos.html` · `RELATORIO_CODEX_METODOLOGIA_SERVICOS.md` ·
`CHECKLIST_DASHBOARD_METODOLOGIA_SERVICOS.md` · scripts `gerar_metodologia_servicos.py` e
`build_dashboard_metodologia.py` (reprodutíveis) · `dados_metodologia_servicos.json` (dados do painel).
Backup do painel anterior em `BACKUP_METODOLOGIA_SERVICOS/`. O painel anterior
`dashboard_senge_honorarios_corrigido_codex.html` foi **preservado**.

*Documento técnico. Caráter orientativo. Nenhum valor foi inventado; o não verificável está marcado.*
