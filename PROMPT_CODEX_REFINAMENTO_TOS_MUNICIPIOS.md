# Prompt para o Codex — refinamento TOS + padronização municipal

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Uso:** colar como instrução para o Codex executar a próxima rodada. Este é um prompt; **não** executa nada por si só.

---

## Contexto que o Codex deve assumir como verdadeiro

- Pasta de trabalho única: `C:\Users\adina\Meu Drive\SENGE\PROPOSTA CLAUDE`.
- Fonte de ARTs: `C:\Users\adina\Meu Drive\ARTS Adinailson\ARTs 2022 01022024.csv` (base 2022, 230.928 ARTs distintas).
- Pipeline atual: `gerar_metodologia_servicos.py` (classifica A/B/C/D no nível da ART; mapeia atividade→serviço por palavra-chave; gera CSVs + JSON) e `build_dashboard_metodologia.py` (monta o HTML).
- Classes de confiabilidade: A=cálculo monetário; B=secundário; C=frequência/diagnóstico; D=excluída do valor.
- Problema central: bucket **"Não mapeado"** = 102.554 ARTs (~44%), com 19.975 Classe A (~38% da base A).
- A base já tem coluna `codigo_atividade` numérica por ART.

## Regras inegociáveis (o Codex DEVE obedecer)

1. **Preservar todos os arquivos existentes.** Nunca sobrescrever. Toda saída nova leva sufixo `_TOS` (ou nome novo explícito). Se um nome já existir, criar versão `_TOS`.
2. **Não sobrescrever** `dashboard_senge_honorarios_metodologia_servicos.html`. Gerar um HTML novo (ex.: `dashboard_senge_honorarios_TOS.html`).
3. **Não somar** valores de linhas da mesma ART. Valor é da ART inteira.
4. **Não tratar** `valor_art` como honorário líquido. Rótulo obrigatório: "valor da ART, não honorário líquido".
5. **Não criar ranking** de profissionais, empresas ou contratantes. **Não expor** dados pessoais nem texto livre de atividade detalhado.
6. **Não inventar** códigos TOS, serviços, subgrupos, normas, fontes, municípios, jurisdição ou conclusões.
7. Onde algo não puder ser verificado, escrever **exatamente**: `Informação insuficiente para verificar`.
8. Manter o **gate**: KPIs monetários bloqueados para Classe C/D.
9. Aplicar a regra **`n < 5`** no nível de subserviço (não só família ampla).
10. Fazer **backup** de qualquer artefato antes de gerar novos (a pasta já tem `BACKUP_METODOLOGIA_SERVICOS/`).

## Tarefas (em ordem)

1. **Localizar/receber a TOS oficial.** Procurar na pasta de trabalho e nas pastas de contexto (`ATUALIZADO`, `NOVA METODOLOGIA`). Se não houver TOS oficial confiável, **parar e reportar** `Informação insuficiente para verificar` — não inventar a TOS. Não prosseguir com campos TOS sem fonte.
2. **Verificar `codigo_atividade` vs. TOS.** Extrair códigos distintos e frequências; cruzar com a TOS; reportar a **taxa de match** (% de ARTs com código casando na TOS). Decidir se o código é eixo primário de mapeamento.
3. **Melhorar o dicionário atividade→serviço.** Mapear primeiro por `codigo_atividade` (exato); usar palavra-chave só no resíduo (aproximado). Não remover regras existentes sem registrar.
4. **Reduzir o bucket "Não mapeado".** Reportar antes/depois (nº e % de "Não mapeado"; nº e % de Classe A em "Não mapeado").
5. **Criar campos TOS** na base nova `_TOS`: `grupo_tos`, `subgrupo_tos`, `servico_tos`, `complemento_tos`, `servico_honorarios_padronizado`, `nivel_confianca_mapeamento` (exato/aproximado/manual/nao_mapeado). Preencher só por lookup; sem fonte → "Informação insuficiente para verificar".
6. **Criar subserviços.** Agregado no nível serviço/complemento com colunas: família, grupo, subgrupo, serviço, complemento, unidade_referencia, modalidade, classe, n_arts_classe_a, mediana, q1, q3, iqr, nivel_confianca_mapeamento_predominante, regra_n5_aplicada, observacao.
7. **Aplicar `n < 5`** por subserviço/complemento: suprimir mediana/quartis (→ "Informação insuficiente para verificar"), manter frequência.
8. **Padronizar municípios por IBGE.** Reusar `norm_key`/`strip_accents`. Expandir abreviações (dicionário auditável). Casar contra lista IBGE oficial; preencher `codigo_ibge`/`municipio_label`/`nivel_confianca_municipio`. Sem lista IBGE → manter "Informação insuficiente para verificar". **Não** mapear inspetoria/SUREG sem fonte oficial CREA.
9. **Atualizar o dashboard (HTML novo)** com filtros novos: por grupo/subgrupo/serviço TOS, por nível de confiança do mapeamento e por município (codigo_ibge quando houver). Manter bloqueio de KPI para C/D. Manter rótulos de cautela.
10. **Gerar relatório de validação** `RELATORIO_VALIDACAO_TOS.md` com:
    - taxa de match do `codigo_atividade`;
    - "Não mapeado" antes/depois;
    - distribuição por nível de confiança (exato/aproximado/manual/nao_mapeado);
    - nº de subserviços com `n ≥ 5` e com `n < 5`;
    - municípios identificados vs. não identificados;
    - lista de serviços candidatos a "novo serviço" (lacunas da tabela atual);
    - mediana só-exatos vs. mediana-todos por serviço (para mostrar o efeito do mapeamento);
    - tudo separando FATO / INFERÊNCIA / RECOMENDAÇÃO.

## Saídas esperadas (nomes sugeridos)
- `base_servicos_metodologia_TOS.csv`
- `agregado_subservicos_classe_a_TOS.csv`
- `frequencia_subservicos_TOS.csv`
- `MATRIZ_TOS_X_TABELA_ATUAL.csv`
- `dim_municipios_bahia_TOS.csv`
- `dados_metodologia_TOS.json`
- `dashboard_senge_honorarios_TOS.html`
- `RELATORIO_VALIDACAO_TOS.md`

## Critério de aceite para o Codex
- Nenhum arquivo existente alterado/sobrescrito.
- "Não mapeado" reduzido **e** reportado com número antes/depois.
- Campos TOS presentes e preenchidos só com fonte; resto "Informação insuficiente para verificar".
- `n < 5` aplicado por subserviço.
- Municípios com confiança marcada; sem invenção de IBGE/jurisdição.
- Relatório de validação gerado.
- Se a TOS oficial não for localizada: parar, reportar e **não** inventar.
