# METODOLOGIA DO DASHBOARD — VERSÃO INSTITUCIONAL AMPLIADA
## Painel de evidências de ART para a nova metodologia de honorários do SENGE/BA

> Versão ampliada da seção "Metodologia" do dashboard, escrita para conselheiros do CREA-BA, dirigentes
> do SENGE-BA, câmaras especializadas, entidades de classe, profissionais de engenharia e a equipe técnica
> que implementará o painel/planilha. Esta versão **corrige** a seção atual do HTML em dois pontos: (i) o
> período real da base (2015–2022) e (ii) a lista de filtros realmente existentes.
> Data: 2026-06-23.

---

## 1. Finalidade do painel
O painel é um **instrumento de apoio à decisão**, não a tabela em si. Sua função é **organizar evidências
agregadas de ARTs** para subsidiar, de forma transparente e auditável, a construção de uma **referência
técnica e orientativa** de honorários de engenharia na Bahia. O painel **não** estabelece preço obrigatório,
tabela vinculante nem qualquer imposição concorrencial de valores. Ele responde a perguntas como: *quais
atividades são mais frequentes? em quais municípios e modalidades? quais unidades de medida predominam?
como as ARTs se distribuem no tempo?* — sempre em nível agregado.

## 2. Origem dos dados
Os dados provêm das **Anotações de Responsabilidade Técnica (ARTs) registradas no CREA-BA**. A base
agregada embarcada no painel reúne registros de **2015 a 2022** (oito anos). A base de 2022 vem do arquivo
consolidado `ARTs 2022 01022024.csv`; os anos 2015–2021 provêm das bases semestrais (.xls/.xlsx) já
existentes. **Observação importante:** parte dos metadados internos do painel ainda rotula a fonte apenas
como "2022"; este documento registra que o período correto da base é **2015–2022** e recomenda padronizar
os metadados antes da apresentação externa.

## 3. Tratamento e padronização
Os registros brutos de ART passam por: (a) **parsing robusto** (o campo de atividade contém `;` internos,
exigindo reconstrução das colunas ancorada pela direita); (b) **limpeza** (remoção de espaços, normalização
decimal, remoção de horário das datas); (c) **padronização de rótulos** de modalidade (unificação de
gênero e especialidades), de unidade de medida e de nome de município; (d) **tipagem** (data, valor,
quantidade, unidade); (e) **separação** de linhas incompletas (sem valor/unidade) das analisáveis. Apenas
o resultado **agregado** é embarcado no painel — os microdados não são publicados.

## 4. Normalização de municípios e filtros
Para que os filtros funcionem de forma consistente, todas as chaves de comparação passam por uma função de
**normalização** que: remove acentos, padroniza espaços, remove o sufixo de UF (`-BA`/`/BA`) ao final do
texto e compara os valores em maiúsculas. Assim, "Ilhéus", "ILHEUS" e "Ilhéus - BA" são tratados como a
mesma chave. **Regra de combinação dos filtros:**
- **Dentro do mesmo filtro**, múltiplas seleções funcionam como **OU** (ex.: Município IN {Itabuna, Ilhéus}).
- **Entre filtros diferentes**, a combinação funciona como **E** (ex.: Município E Ano E Modalidade).

**Filtros realmente disponíveis nesta versão (5):** Ano, Município, Modalidade, Unidade de medida e Tipo de
ART. Filtros por **inspetoria, supervisão regional/SUREG, situação, grupo de atividade e faixa de valor**
são **previstos para versões futuras** e dependem de dados que ainda não estão na base (ver itens 8 e 12).

## 5. Uso de dados agregados
Todas as visões são **agregadas por** ano, município, modalidade, unidade e tipo de ART. Não há, no painel,
qualquer registro individual de ART, profissional, empresa, contratante ou proprietário. A agregação é a
unidade mínima de informação exibida.

## 6. Proteção de dados pessoais (LGPD)
- Publicação **exclusivamente de agregados**; nenhum identificador (id de ART, nome, endereço) é exposto.
- Recomenda-se **supressão de células com n < 5** registros, para evitar reidentificação.
- **Proibição de ranking individual** de profissionais, empresas, contratantes ou proprietários.
- O painel é um derivado **anonimizado**; os microdados originais permanecem fora do artefato publicado.

## 7. Interpretação dos valores
Os valores observados nas ARTs devem ser lidos como **faixas**, nunca como preço único. A estatística de
referência é a **mediana** (tendência central robusta) acompanhada do **intervalo interquartil (IQR =
P25–P75)**. **A média não deve ser usada**, pois é distorcida por outliers extremos. Toda faixa deve trazer
o **n** (número de registros) e um **indicador de confiabilidade** (alta/média/baixa). Combinações em que o
teto se distancia exageradamente da mediana (>20×) são marcadas como de baixa confiabilidade (provável
mistura de valor unitário com valor total do contrato).

## 8. Limitações da ART como proxy de honorários
> **"Os dados de ART são utilizados como evidência auxiliar, indireta e agregada de escopo, atividade,
> localidade, responsabilidade técnica e valor declarado, não como prova isolada do honorário profissional
> efetivamente contratado."**

Em detalhe: (a) o valor de contrato pode refletir valor da obra, do contrato ou apenas declaração;
(b) há outliers e erros de digitação (até ~10¹¹); (c) há grande heterogeneidade de unidades (mais de uma
centena) e de texto de atividade (dezenas de milhares de variações); (d) pode haver sub ou
sobredeclaração; (e) a confiabilidade varia por atividade. Por isso a ART **calibra e valida faixas**, mas
não prova o honorário efetivamente praticado.

## 9. Indicadores estatísticos recomendados
| Indicador | Definição | Uso |
|---|---|---|
| Mediana por Atividade×Unidade | P50 robusto | Âncora da faixa de referência |
| IQR (P25–P75) | Dispersão central | Faixa observada (piso/teto empírico) |
| n por célula | Contagem de registros | Confiabilidade + corte LGPD (n<5) |
| Coef. de variação (CV) | Dispersão/centro | Sinaliza atividades voláteis |
| Frequência por modalidade/município | Contagem | Prioriza itens a tabelar |
| Fator regional | Mediana local / mediana estadual | Calibra ajuste regional |

## 10. Critérios para tabela orientativa
A tabela derivada deste painel deve: (a) organizar-se por **atividade (código CREA) × unidade × modalidade**;
(b) expressar **faixas** (piso técnico – referência – teto), não valor único; (c) registrar **fonte,
data-base e nota de confiabilidade** por item; (d) **não conter valores inventados** — campos sem base
empírica ou sem pesquisa de preços recebem "Informação insuficiente para verificar"; (e) ser **revisada
anualmente** com nota técnica e changelog.

## 11. Cuidados jurídicos e concorrenciais
A tabela é **referência técnica e instrumento de valorização profissional e combate ao aviltamento**, de
caráter **orientativo**. Deve-se **evitar** qualquer redação que sugira tabelamento, preço mínimo
compulsório ou restrição concorrencial. As normas eventualmente citadas (p. ex. Lei 4.950-A/66, Lei
5.194/66, Resolução Confea 1.074/2016, NBR 12.721) devem ser **confirmadas em fonte oficial** antes da
versão final — enquanto não confirmadas, marcar "Informação insuficiente para verificar".

## 12. Próximas etapas de validação
1. Padronizar o **período (2015–2022)** nos metadados e no cabeçalho do painel.
2. Implementar **distribuição estatística filtrável** (mediana/IQR/n por recorte, com supressão n<5).
3. Incorporar as **dimensões territoriais** (município → unidade CREA) somente após confirmação da fonte
   oficial (Regulamento das Inspetorias do CREA-BA) e dos códigos IBGE.
4. Validar visualmente o **mapa** (Leaflet/OSM/malha IBGE) com internet.
5. Confirmar a **base legal** citada.
6. Submeter o painel e a metodologia à apreciação das câmaras especializadas e entidades de classe.

---
*Esta versão institucional substitui, para fins de apresentação, a redação resumida embutida no HTML, e
deve ser refletida na próxima atualização do dashboard.*
