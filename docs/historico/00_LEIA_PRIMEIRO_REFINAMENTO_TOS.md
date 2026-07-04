# 00 — Leia primeiro: refinamento TOS (resumo executivo)

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Para:** Adinailson G. de Oliveira (eng. eletricista, conselheiro CREA-BA) e grupo técnico SENGE.

---

## Estado atual
A metodologia "por serviço + classe de confiabilidade" está **implementada e o dashboard foi validado** no navegador. O desenho está conceitualmente correto: a ART é a unidade de valor, a classe (A/B/C/D) é o filtro de qualidade, e o serviço é o eixo de agregação. Base: 230.928 ARTs de 2022; Classe A = 53.190 (23%).

## O que já funciona (confiável)
- **Volume e demanda** por serviço e por classe (totais e frequências).
- **Identificação de lacunas** da tabela atual: fotovoltaica, receituário agronômico, topografia, ambiental, segurança do trabalho aparecem com alta frequência.
- **Gate de qualidade**: ARTs Classe C/D não formam preço; o painel bloqueia KPIs monetários para C/D.
- **Anti-erro estrutural**: não soma linhas da mesma ART; trata o valor como da ART inteira; regra `n < 5` já existe no nível de serviço.

## Maior limitação
O bucket **"Não mapeado"**: **102.554 ARTs (~44%)** sem serviço atribuído, contendo **19.975 Classe A (~38% da base monetária)**. Enquanto isso persistir, toda mediana por serviço é **preliminar**. Some-se a isso a natureza heterogênea do valor: há ARTs de **obra** entrando como valor (ex.: Pavimentação com mediana R$ 1,3 milhão; max R$ 819 milhões no próprio "Não mapeado") — valor de contrato, não honorário.

## Por que a TOS é a próxima etapa
A base **já tem um `codigo_atividade` numérico** por ART. Mapear por **código TOS** é exato; mapear por palavra-chave (atual, ~55% de cobertura) é aproximado. Usar a TOS deve reduzir o "Não mapeado", dar lastro auditável por código e permitir separar **elaboração técnica** (projeto, laudo) de **execução de obra** — a separação que falta para falar em honorário. Pré-requisito: localizar a TOS oficial; se não houver, **"Informação insuficiente para verificar"** e não inventar.

## Por que o município é a segunda etapa
`cidade_obra` tem 1.984 grafias; falta a **âncora IBGE oficial** (códigos hoje "Informação insuficiente para verificar"). É importante para recorte territorial, mas é **menos crítico que o mapeamento de serviço** — por isso vem depois. Inspetoria/SUREG só com fonte oficial CREA; não pode ser inventada.

## O que pode ser apresentado internamente
**Sim, com ressalvas:** diagnóstico de demanda, lacunas da tabela, prova de conceito da metodologia. Mantendo os rótulos de cautela e registrando que ~38% da base A está em "Não mapeado".

## O que ainda NÃO deve ser apresentado externamente
**Valores por serviço como referência de honorário**, enquanto: (1) "Não mapeado" ~44%; (2) valores de obra misturados; (3) sem separação TOS obra×elaboração. Externamente há risco **concorrencial** (parecer tabelamento) e **LGPD** (microdados). Só linguagem de *subsídio metodológico orientativo* e indicadores de demanda.

## Próxima ação recomendada
Executar a rodada do **`PROMPT_CODEX_REFINAMENTO_TOS_MUNICIPIOS.md`**, nesta ordem de prioridade:
1. Localizar a TOS oficial e verificar o match do `codigo_atividade`.
2. Reduzir o "Não mapeado" (reportando antes/depois) e criar campos TOS.
3. Criar subserviços com `n < 5` no nível certo.
4. Padronizar municípios por IBGE.
5. Gerar `RELATORIO_VALIDACAO_TOS.md`.

## Mapa dos documentos desta rodada
- `REVISAO_CRITICA_PIPELINE_METODOLOGIA_SERVICOS_TOS.md` — o que está certo, o que é preliminar, uso interno/externo.
- `DIAGNOSTICO_BUCKET_NAO_MAPEADO_TOS.md` — anatomia do maior risco.
- `ESPECIFICACAO_REFINAMENTO_TOS.md` — como usar a TOS e os campos novos.
- `MODELO_SUBSERVICOS_E_SUPRESSAO_N5.md` — granularidade e regra `n < 5`.
- `ESPECIFICACAO_PADRONIZACAO_MUNICIPIOS.md` — município/IBGE e jurisdição.
- `PROMPT_CODEX_REFINAMENTO_TOS_MUNICIPIOS.md` — instrução de execução.
- `00_LEIA_PRIMEIRO_REFINAMENTO_TOS.md` — este resumo.

---
**Regra de ouro da frente:** valor declarado em ART ≠ honorário líquido; tabela = referência técnica orientativa, nunca preço obrigatório.
