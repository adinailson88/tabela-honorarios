# PROMPT PARA O CODEX — METODOLOGIA DE PADRONIZAÇÃO E CLASSIFICAÇÃO DE SERVIÇOS (ARTs)

## Objetivo desta rodada
Construir a camada metodológica que liga **as ARTs** (atividades registradas) à **tabela de honorários
do SENGE-BA**, criando os campos de classificação, separando a base de cálculo confiável (Classe A),
gerando a base agregada por serviço (mediana/IQR/n com supressão) e atualizando o dashboard **sem
quebrar os filtros já corrigidos**. Esta rodada é de **tratamento de dados e classificação**, não de
redesenho visual.

> Copie o bloco de código abaixo e cole para o Codex. Não altere os números do contexto.
> Data: 2026-06-23.

---

## BLOCO PARA COLAR NO CODEX

```
Você é o engenheiro de dados que vai construir a camada de PADRONIZAÇÃO E CLASSIFICAÇÃO DE SERVIÇOS
das ARTs para o projeto SENGE-BA de honorários. NÃO refaça o dashboard do zero. Trabalhe de forma
incremental e versionada.

=== PASTA DE TRABALHO (única permitida) ===
C:\Users\adina\Meu Drive\SENGE\PROPOSTA CLAUDE

=== REGRAS DE SEGURANÇA (OBRIGATÓRIAS) ===
- NÃO apagar, NÃO mover e NÃO renomear nenhum arquivo original (CSV de ARTs, tabela de honorários,
  HTML do dashboard, JSONs em dados/, scripts existentes).
- NÃO sobrescrever saídas anteriores. Toda saída nova é VERSIONADA com novo nome (sufixo _v2, _v3…
  ou subpasta datada). Se precisar tocar em arquivo já existente, gere cópia nova; não edite o original.
- NÃO trabalhar fora da pasta PROPOSTA CLAUDE.
- NÃO inventar valores, normas, municípios, inspetorias, SUREG, códigos IBGE, vínculos ou conclusões.
- Usar SOMENTE dados AGREGADOS. Sem dados pessoais. Sem ranking de profissionais, empresas ou
  contratantes. Respeitar LGPD e cautela concorrencial.
- Onde faltar base para afirmar algo, escrever exatamente: "Informação insuficiente para verificar".
- Caráter ORIENTATIVO (referência técnica / parâmetro orientativo / subsídio metodológico), nunca
  impositivo. Evitar termos como "preço obrigatório", "preço mínimo compulsório", "tabela vinculante".
- Não recalcular nem rearredondar os números de contexto fornecidos abaixo; use-os como verificados.

=== ARQUIVOS DESTA RODADA (LER PRIMEIRO) ===
- ARTs (microdados base 2022): pasta "ARTS Adinailson", arquivo "ARTs 2022 01022024.csv".
  Separador ';'. ATENÇÃO ao parsing: o campo "atividade" contém ';' internos — faça a ancoragem
  pela DIREITA (o número fixo de colunas após "atividade" é estável; "atividade" é o campo elástico).
  Há 4 colunas finais vazias de exportação.
- Tabela de honorários (pasta ATUALIZADO): "29-07-2024 - Tabela Honorarios Adinailson.xlsx"
  (e .docx companheiro), data 29/07/2024. 13 abas temáticas por família de serviço; cada aba é uma
  matriz [natureza da obra (linhas)] x [subtipo (colunas)] -> valor; unidades heterogêneas
  (m2, m3, km, ha, hora, %CUB, R$ fixo); duas colunas de versão lado a lado (CUB 2017-11 = R$ 1369,12
  e CUB 2024-06 = R$ 1929,04; razão de atualização ~ +40,9%).
- Saídas já existentes a NÃO quebrar: dashboard_senge_honorarios_corrigido_codex.html, pasta dados/
  (data.json, flat_counts.json), teste_filtros_codex.py, dim_municipio_crea.csv,
  dim_municipios_bahia.csv, dim_crea_unidades.csv.

=== CAMPOS DE CONTEXTO (FATOS VERIFICADOS — NÃO ALTERAR) ===
- Volume: 726.028 linhas de atividade; 230.928 ARTs distintas (id).
- ARTs multi-linha: 62,6% (144.541). Linha única: 37,4% (86.387).
- ARTs com mais de um código de atividade distinto (escopo composto): 26,5% (61.284).
- Multi-modalidade no campo "titulos": 0% (cada ART tem EXATAMENTE um título/modalidade nesta base).
- VALOR REPLICADO: entre as multi-linha, 99.982 ARTs têm valor CONSTANTE em todas as linhas e apenas
  2.080 variam. Conclusão (fato): valor_contrato é o valor da ART INTEIRA, replicado por linha —
  NÃO é valor por atividade. SOMAR linhas multiplica o valor indevidamente. Exemplo real: ART id
  2399866 tem 2 linhas (Laudo e Vistoria) com 433.795,00 replicado.
- ARTs sem valor utilizável: 74.026 (32%).
- Distribuição no NÍVEL ART (deduplicado por id, valores positivos): mediana R$ 1.800; P25 800;
  P75 7.272; P90 200.000; máximo ~7,9x10^11 (outliers/erros). Mediana por LINHA ~1.570 difere da
  mediana por ART por causa da replicação.
- tipo_art (linhas): OBRA/SERVICO 628.768; RECEITUARIO AGRONOMICO 70.337; MULTIPLA MENSAL 21.851;
  CARGO-FUNCAO 4.093; REGISTRO FORA DE EPOCA 971.
- TIPOLOGIA DE CONFIABILIDADE (sobre 230.928 ids):
  * Classe A (linha única, 1 código, 1 valor plausível): 53.190 (23,0%). Valor: mediana 2.000;
    P25 800; P75 8.000; P90 145.363.
  * Classe B homogênea (multi-linha, MESMO código, valor constante = atividade repetida): 38.631 (16,7%).
  * Caso de valor que varia entre linhas (multi-linha, valor diferente): 2.080 (0,9%).
  * Classe C composta ambígua (multi-linha, MÚLTIPLOS códigos, valor único replicado): 60.247 (26,1%).
  * Classe D sem valor: 76.751 (33,2%); implausível (>R$ 1 bilhão): 29.

=== TAREFAS (EXECUTAR NESTA ORDEM) ===

(1) LER os arquivos desta rodada (ARTs CSV + tabela de honorários). Reportar contagens de leitura e
    confirmar que batem com os números de contexto (linhas 726.028; ids 230.928). Se NÃO baterem,
    PARAR e registrar a divergência no relatório de validação — não prosseguir com cálculo monetário.

(2) CRIAR/AJUSTAR scripts de tratamento em scripts/ (NOVOS arquivos, versionados; não sobrescrever):
    - scripts/01_parse_arts.py — leitura robusta do CSV (ancoragem pela direita do campo "atividade"),
      normalização de encoding (UTF-8), limpeza de valor_contrato (decimal BR -> float).
    - scripts/02_classificar_servicos.py — geração da tabela de classificação (campos abaixo).
    - scripts/03_base_classe_a.py — extração da base Classe A.
    - scripts/04_agregar_por_servico.py — base agregada por serviço com supressão n<5.
    - scripts/05_validacao.py — relatório de validação.

(3) CRIAR OS CAMPOS DE CLASSIFICAÇÃO (uma linha por linha de atividade, com chave de ART):
    - id_art                  : identificador único da ART (campo "id").
    - atividade_original      : texto livre do campo "atividade" (sem alteração).
    - atividade_key           : chave normalizada (minúsculas, sem acento, sem espaços duplos, código
                                de atividade quando existir) para agrupamento.
    - servico_padronizado     : nome canônico do serviço (dicionário de padronização versionado em
                                dados/dicionario_servicos_vN.csv; não inventar — onde não houver mapa,
                                preencher "Informação insuficiente para verificar").
    - grupo_servico           : família/eixo (ex.: Estrutural, Instalações, Saneamento, Fotovoltaica/
                                Energia, Agronomia, Ambiental, Geotecnia, etc.) coerente com as 13
                                famílias da tabela quando houver correspondência; "Sem correspondência
                                na tabela" quando for serviço novo (ex.: microgeração fotovoltaica).
    - modalidade              : do campo "titulos" (título profissional do responsável).
    - formacao                : normalização da modalidade (ex.: "Engenheiro Civil" -> "Engenharia Civil");
                                se ambígua, repetir o original e marcar para revisão.
    - valor_art               : valor da ART INTEIRA, deduplicado por id_art (ver tarefa 6).
    - classe_confiabilidade   : A / B / C / D conforme tipologia do contexto.
    - usar_calculo_monetario  : TRUE somente para Classe A (e Classe B com regra explícita de
                                simulação); FALSE para C e D.
    - motivo_exclusao_calculo : texto curto padronizado (ex.: "Sem valor utilizável",
                                "Escopo composto — valor não atribuível", "Valor implausível >1bi",
                                "Valor varia entre linhas").

(4) IDENTIFICAR ARTs MULTI-ATIVIDADE: marcar ids com mais de um código de atividade distinto
    (escopo composto). Esperado ~61.284 (26,5%). Reportar contagem obtida vs esperada.

(5) IDENTIFICAR MULTI-MODALIDADE: verificar se algum id_art carrega mais de um valor distinto em
    "titulos". Esperado 0% nesta base. Se aparecer >0, NÃO assumir erro: registrar a contagem e
    sinalizar para revisão humana (pode indicar mudança na base).

(6) TRATAR VALOR REPLICADO (passo crítico): para cada id_art, DEDUPLICAR o valor — o valor da ART é
    UM só, não a soma das linhas. Regra: se o valor é constante em todas as linhas do id, valor_art =
    esse valor. Se varia entre linhas (os 2.080 casos), marcar classe e motivo apropriados e NÃO
    somar. NUNCA somar valor_contrato entre linhas de uma mesma ART.

(7) SEPARAR A BASE CLASSE A: gerar dados/base_classe_a_vN.csv (linha única, 1 código, 1 valor
    plausível). Esperado 53.190 ARTs. É a base PRIMÁRIA de cálculo monetário. Reportar contagem.

(8) GERAR BASE AGREGADA POR SERVIÇO: a partir da Classe A (e, opcionalmente, Classe B como simulação
    rotulada), produzir dados/agregado_por_servico_vN.csv e o JSON correspondente em dados/, com, por
    serviço (e por recortes úteis: serviço×unidade, modalidade, município quando houver):
    - n (contagem de ARTs)
    - mediana
    - P25 (IQR inferior)
    - P75 (IQR superior)
    SUPRESSÃO OBRIGATÓRIA: para qualquer célula com n<5, NÃO publicar estatística — preencher
    "Informação insuficiente para verificar" e expor apenas a existência/frequência, nunca o valor.
    Não publicar média sem mediana; preferir mediana/IQR (robustez a outliers).

(9) ATUALIZAR O DASHBOARD SEM QUEBRAR OS FILTROS JÁ CORRIGIDOS:
    - Os 5 filtros reais já corrigidos (ano, município, modalidade, unidade, tipo de ART) devem
      continuar funcionando exatamente como hoje. NÃO alterar a lógica deles.
    - Adicionar uma seção "Distribuição estatística por serviço" alimentada pelo novo JSON agregado,
      respeitando a supressão n<5.
    - Gerar NOVA cópia versionada do HTML (ex.: dashboard_senge_honorarios_corrigido_codex_v2.html);
      não sobrescrever a versão anterior.
    - Deixar explícito no painel quais KPIs respondem aos filtros e quais são globais.

(10) GERAR RELATÓRIO DE VALIDAÇÃO em RELATORIO_VALIDACAO_METODOLOGIA_SERVICOS.md contendo:
    - Contagens obtidas vs esperadas (linhas, ids, multi-linha, multi-atividade, multi-modalidade,
      valor replicado, sem valor, e cada classe A/B/C/D). Marcar OK/DIVERGE em cada item.
    - Confirmação de que valor não foi somado entre linhas (mediana por ART deve dar ~1.800;
      por linha ~1.570). Se não bater, registrar.
    - Lista de serviços novos detectados sem correspondência na tabela (ex.: microgeração
      fotovoltaica/kWp, geração de energia/kW/kVA, agronomia/receituário, ambiental, agrimensura).
    - Lista de pendências e de tudo que ficou como "Informação insuficiente para verificar".
    - Validar node --check de qualquer JS extraído; reexecutar teste_filtros_codex.py e registrar.

=== ENTREGÁVEIS (todos versionados, dentro de PROPOSTA CLAUDE) ===
- scripts/01_parse_arts.py ... scripts/05_validacao.py (novos).
- dados/dicionario_servicos_vN.csv (mapa de padronização; vazio/parcial é aceitável, com lacunas
  marcadas).
- dados/arts_classificadas_vN.csv (linha por atividade, com todos os campos da tarefa 3).
- dados/base_classe_a_vN.csv.
- dados/agregado_por_servico_vN.csv + JSON correspondente em dados/.
- dashboard_senge_honorarios_corrigido_codex_v2.html (nova cópia; filtros intactos).
- RELATORIO_VALIDACAO_METODOLOGIA_SERVICOS.md.
- Atualizar LOG_CODEX_DASHBOARD.md anexando a seção desta rodada (sem apagar o histórico).

=== CRITÉRIOS DE ACEITE ===
- Nenhum arquivo original apagado/movido/sobrescrito.
- Valor NUNCA somado entre linhas de uma mesma ART (deduplicação por id confirmada no relatório).
- Toda estatística com n<5 suprimida.
- Contagens obtidas conferidas contra os números de contexto; divergências documentadas, não escondidas.
- Filtros existentes do dashboard continuam funcionando.
- Onde faltar base, consta literalmente "Informação insuficiente para verificar".
```

---

## Notas para você (Adinailson)
- O dicionário `dados/dicionario_servicos_vN.csv` (mapa de nome livre -> serviço canônico) é o ponto
  que mais depende de decisão humana. O Codex deve preencher só o que houver evidência e deixar o resto
  como "Informação insuficiente para verificar"; a curadoria fina do mapa fica para você/SENGE.
- A correspondência serviço (ART) -> família da tabela de honorários é parcial: vários serviços de alto
  volume nas ARTs (fotovoltaica/kWp, geração/kW/kVA, agronomia, ambiental, agrimensura) NÃO existem na
  tabela. Isso é a justificativa central para atualizar a metodologia — não é falha do tratamento.
- A base agregada filtrável de valor só vale para Classe A (e Classe B como simulação rotulada).
  Classe C entra apenas como frequência/detecção de serviços novos; Classe D é excluída do cálculo.
