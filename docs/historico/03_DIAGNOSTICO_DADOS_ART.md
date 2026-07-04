# 03 — Diagnóstico dos Dados de ART

> Análise da pasta `ARTS Adinailson`. Foco no arquivo de maior volume e mais estruturado:
> `ARTs 2022 01022024.csv`. Todos os números abaixo foram **calculados diretamente do arquivo**
> nesta sessão (perfil agregado). Nenhum dado pessoal é exposto.

---

## 1. Tipos de arquivo encontrados

| Grupo | Arquivos | Observação |
|---|---|---|
| CSV consolidado 2022 | `ARTs 2022 01022024.csv` (≈146 MB) | **Principal base empírica** — analisado |
| Análises já feitas | `Análise ARTs.xlsx`, `Análise ARTs Agronomia.xlsx`, `analises/2022.xlsx` | Contêm metodologia de limpeza e abas por semestre |
| Bases por semestre | `arts 2015…2022` (.xls / .xlsx) | Matéria-prima; **arquivos .xls (2015–2019) não foram lidos** nesta sessão (faltou a biblioteca `xlrd`). → *Validar depois.* |

**`Análise ARTs.xlsx`** já documenta uma "Metodologia de limpeza dos dados" (retirar espaços, substituir pontos, remover horários, filtrar coluna quantidade…) e tem abas por semestre (2020.1 a 2022.2). **Esse trabalho de limpeza deve ser reaproveitado.**

---

## 2. Estrutura do CSV 2022 (campos disponíveis)

O cabeçalho nomeia 14 colunas (+ 4 colunas vazias de exportação):

`id; tipo_art; formaderegistro; emissao; cidade_obra; uf; titulos; entidade; codigo; atividade; quantidade; unidade; valor_contrato; ano_registro_profissional`

> **Limitação técnica de parsing (importante):** o campo `atividade` contém `;` internos
> (ex.: `"Nível - Execução; Atividade - Laudo - ..."`), o que desalinha a separação simples por `;`.
> O perfil abaixo foi obtido **reconstruindo as colunas pela direita** (ancorando ano/valor/unidade/quantidade
> no fim da linha). Os valores devem ser **revalidados** numa rotina dedicada antes de uso oficial.

---

## 3. Volume e período

- **Linhas de atividade:** 726.028
- **ARTs distintas (id):** 230.928 — ou seja, uma ART pode ter várias atividades (linhas).
- **Período:** 100% emissão em **2022** (consistente com o nome do arquivo).
- **Cobertura geográfica:** 705.357 linhas em **BA** (97,2%); restante em PE, SP, MG, SE, PI, RN, CE, RJ, GO (obras fora do estado registradas por profissionais).

---

## 4. Modalidades profissionais (campo `titulos`) — top 10

| Modalidade | Linhas |
|---|---|
| Engenheiro(a) Civil | 280.497 + 49.632 |
| Engenheiro(a) Agrônomo(a) | 82.877 + 11.526 |
| Engenheiro(a) Eletricista (e Eletrotécnica/Eletrônica) | 72.097 + 26.967 + 11.583 + … |
| Engenheiro(a) de Segurança do Trabalho | 38.713 + 4.760 |
| Engenheiro(a) Mecânico(a) | 21.034 |
| Engenheiro(a) Ambiental | 17.172 + 5.799 |
| Engenheiro Agrimensor | 8.486 |
| Engenheiro de Minas | 5.876 |
| Geólogo | 5.238 |

> Nota: há entradas masculino/feminino separadas (ex.: "Engenheiro Civil" e "Engenheira Civil")
> e variações de especialidade — exigirá **padronização de rótulos** antes de agregar.

---

## 5. Localidades (campo `cidade_obra`) — top 10

| Cidade | Linhas |
|---|---|
| Salvador | 85.347 |
| Feira de Santana | 26.139 |
| Vitória da Conquista | 21.005 |
| Camaçari | 20.763 |
| Barreiras | 20.658 |
| Luís Eduardo Magalhães | 18.448 |
| Juazeiro | 13.832 |
| Teixeira de Freitas | 13.793 |
| Lauro de Freitas | 12.968 |
| Ilhéus | 11.245 |

Distribuição compatível com regionalização (RMS, agreste, oeste agrícola, sul, extremo sul).

---

## 6. Tipo de ART e atividades

- **tipo_art:** OBRA/SERVIÇO 628.768 · RECEITUÁRIO AGRONÔMICO 70.337 · MÚLTIPLA MENSAL 21.851 · CARGO-FUNÇÃO 4.093 · REGISTRO FORA DE ÉPOCA 971.
- **Atividades distintas (texto, truncado a 80 chars):** ≈ 27.447 → vocabulário muito heterogêneo; precisa de **dicionário/normalização** (mapear texto livre para os códigos CREA de Nível+Atividade, como já feito na `TABELA TOS`).

---

## 7. Unidades de medida (campo `unidade`) — top 10

| Unidade | Linhas |
|---|---|
| metro quadrado | 200.541 |
| unidade | 150.661 |
| quilowatt | 46.798 |
| quilowatt(s) pico (kWp) | 40.177 |
| hectare | 17.793 |
| metro | 12.957 |
| quilovolt-ampère (kVA) | 11.443 |
| metro cúbico | 10.765 |
| quilômetro | 3.964 |
| dia / ano / hora / mês | (diversas) |

São **111 unidades distintas** — confirma a crítica do projeto de que m² não serve para tudo
(kWp para fotovoltaica, kVA para elétrica, hectare para agronomia já aparecem com força).

---

## 8. Valores (`valor_contrato`) — distribuição

Sobre 519.779 valores numéricos diferentes de zero (6.415 zerados; 64 ilegíveis; 199.770 linhas "curtas" sem valor, ex.: CARGO-FUNÇÃO):

| Estatística | Valor (R$) |
|---|---|
| Mínimo | 0,01 |
| P10 | 10,00 |
| P25 | 520,00 |
| **Mediana** | **1.600,00** |
| P75 | 8.000,00 |
| P90 | 584.000,00 |
| P99 | 37.361.846,69 |
| Máximo | 856.681.029.828,14 |

**Leitura crítica:** o salto da mediana (R$1.600) para o P90 (R$584 mil) e o máximo absurdo
(centenas de bilhões) revelam que `valor_contrato` **mistura coisas diferentes**: valor unitário,
valor total do contrato/obra, e erros de digitação. **A média seria inútil; só mediana e
intervalo interquartil (IQR), por atividade × unidade, são defensáveis.**

---

## 9. Limitações e inconsistências

1. **`valor_contrato` ≠ honorário.** Pode ser valor da obra, valor do contrato, ou valor declarado — **não necessariamente o honorário do profissional**. Esta é a ressalva central.
2. **Outliers extremos e erros** (até 10¹¹). Exigem winsorização/filtro por unidade.
3. **Heterogeneidade de unidades** (111) e de **texto de atividade** (27 mil variações).
4. **Linhas incompletas** (199.770) sem valor/atividade — receituários, cargo-função, etc.
5. **Rótulos não padronizados** (gênero, especialidades).
6. **Desalinhamento de colunas** por `;` interno — exige rotina de parsing dedicada.
7. **Apenas 2022 no CSV consolidado.** Série histórica 2015–2021 está em .xls/.xlsx não consolidados (parte não lida nesta sessão).

---

## 10. Possibilidade de uso estatístico

**Sim, com cautela e como evidência auxiliar.** A base permite, de forma robusta:

- Frequência de atividades por modalidade/cidade/unidade (contagens são confiáveis).
- **Faixas de valor por atividade × unidade** usando mediana + IQR, após limpeza e por unidade homogênea (ex.: só `metro quadrado`, só `kWp`).
- Análise regional (97% BA, boa cobertura municipal).
- Validação cruzada: comparar a faixa observada nas ARTs com o valor calculado pelo modelo de esforço técnico (ver doc. 04/05).

**Não permite**, com a qualidade atual: afirmar "o honorário de mercado é X"; usar média; comparar valores entre unidades distintas sem conversão.

---

## 11. Cuidados com LGPD

- O CSV provavelmente associa atividade a profissional/contratante via `id` da ART (dado identificável). **Nenhum relatório institucional deve expor id, nome, contratante, endereço ou ART individual.**
- Regra de ouro adotada nesta proposta: **só publicar agregados** (por atividade, modalidade, cidade, unidade, faixa) e **suprimir células com poucos registros** (ex.: n < 5) para evitar reidentificação.
- **Proibido ranking individual de profissionais** (regra do projeto e boa prática LGPD).
- As cópias derivadas (se criadas) ficam **apenas** em `PROPOSTA CLAUDE` e devem conter somente dados agregados.

---

*Documento derivado. Não altera os arquivos originais.*
