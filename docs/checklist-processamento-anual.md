# Checklist de processamento anual

Use este checklist para incorporar planilhas de ARTs de outros anos ao pipeline.

## 1. Identificação da base

- [ ] Ano de referência informado.
- [ ] Arquivo de origem identificado.
- [ ] Aba ou planilha de origem identificada.
- [ ] Data de obtenção registrada, quando disponível.
- [ ] Responsável pelo processamento registrado.
- [ ] Confirmado que a base linha a linha não será publicada no GitHub Pages.

## 2. Validação de colunas

- [ ] Campo identificador da ART localizado.
- [ ] Campo de município localizado.
- [ ] Campo de valor declarado localizado.
- [ ] Campo de serviço/atividade localizado.
- [ ] Campo TOS localizado, quando existir.
- [ ] Campo de data/ano localizado, quando necessário.
- [ ] Campos ausentes registrados como `Informação insuficiente para verificar.`

## 3. Ingestão

- [ ] Total de linhas lidas registrado.
- [ ] Total de linhas vazias ou inválidas registrado.
- [ ] Encoding e separador validados, quando CSV.
- [ ] Planilha lida sem alteração manual silenciosa.

## 4. Deduplicação

- [ ] Deduplicação por ART executada.
- [ ] Total de ARTs únicas registrado.
- [ ] Total de duplicidades removidas registrado.
- [ ] Regra de desempate documentada, se houver duplicidade conflitante.

## 5. TOS

- [ ] TOS identificado diretamente, quando campo existir.
- [ ] TOS inferido somente por regra documentada.
- [ ] TOS inconsistente sinalizado.
- [ ] Registros sem TOS contabilizados.
- [ ] Limitação de cobertura TOS registrada.

## 6. Natureza do valor

- [ ] Valor declarado normalizado.
- [ ] Valor ausente contabilizado.
- [ ] Valor zerado contabilizado.
- [ ] Taxa simbólica ou valor simbólico contabilizado.
- [ ] Provável valor de obra/contrato contabilizado.
- [ ] Provável honorário técnico contabilizado.
- [ ] Valor extremo sinalizado.
- [ ] Informação insuficiente contabilizada.

## 7. Municípios

- [ ] Município original preservado.
- [ ] Município padronizado criado, quando correspondência segura.
- [ ] Código IBGE preenchido somente com fonte oficial.
- [ ] Inconsistências e distritos sinalizados.
- [ ] Municípios fora da Bahia preservados e sinalizados, quando aplicável.
- [ ] De-para CREA-BA aplicado somente com fonte oficial.

## 8. Outliers

- [ ] Regra de outlier documentada.
- [ ] Registros extremos não apagados sem justificativa.
- [ ] Impacto sobre n registrado.
- [ ] Impacto sobre mediana registrado.
- [ ] Impacto sobre Q1 e Q3 registrado.
- [ ] Impacto sobre mínimo e máximo registrado.
- [ ] Impacto sobre média registrado, se média for usada.

## 9. Agregação

- [ ] Agregação por serviço executada.
- [ ] Agregação por ano executada.
- [ ] Agregação por município executada, quando permitido.
- [ ] Regra `n >= 5` aplicada para referência monetária.
- [ ] Serviços com `n < 5` marcados como `Informação insuficiente para verificar.`
- [ ] Serviços novos separados de referência consolidada.
- [ ] Lacunas SENGE separadas de correspondência confirmada.

## 10. Publicação

- [ ] Apenas dados agregados enviados ao GitHub.
- [ ] Nenhum `id_art` publicado.
- [ ] Nenhuma linha individual de ART publicada.
- [ ] Nenhum ranking de profissional, empresa ou contratante publicado.
- [ ] JSON/CSV público validado.
- [ ] `index.html` carregando após build.

## 11. Relatório final

- [ ] Relatório anual gerado.
- [ ] Limitações registradas.
- [ ] Arquivos de entrada listados.
- [ ] Arquivos públicos listados.
- [ ] Arquivos locais não publicados listados.
- [ ] Próximas pendências descritas sem presunção.
