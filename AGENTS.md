# AGENTS.md

Orientações obrigatórias para agentes de codificação neste repositório.

## Escopo do projeto

Este repositório publica o painel e os artefatos técnicos da proposta metodológica orientativa para a Tabela de Honorários do SENGE/BA, com uso de ARTs do CREA-BA como evidência agregada, auxiliar e indireta.

A ART não deve ser tratada automaticamente como contrato, nota fiscal, recibo ou prova isolada de honorário profissional. O valor declarado em ART pode ter naturezas distintas.

## Arquivos sensíveis

Não publicar dados linha a linha derivados das ARTs no GitHub Pages ou em pastas públicas do repositório.

Devem permanecer locais, salvo decisão formal documentada:

- bases com `id_art`;
- bases com município por registro individual;
- bases com formação por registro individual;
- bases com valor declarado por ART;
- arquivos brutos exportados do CREA-BA;
- planilhas anuais completas de ARTs.

Publicar somente dados agregados necessários ao painel e à reprodução visual.

## GitHub Pages

Não mover `index.html` da raiz sem atualizar e testar a configuração do GitHub Pages.

A organização documental pode ser feita em `docs/`, `data/`, `scripts/` e `outputs/`, mas a publicação atual depende do arquivo `index.html` na raiz.

## Regra metodológica mínima

Preservar a regra atual:

- exibir mediana e IQR monetários apenas para Classe A;
- natureza do valor igual a provável honorário técnico;
- `n >= 5`;
- quando a evidência for insuficiente, usar exatamente: `Informação insuficiente para verificar.`

Não inventar códigos TOS, serviços, grupos SENGE, unidades, regras de CUB, municípios, inspetorias, SUREGs ou classificações CREA-BA.

## TOS e universo de ARTs

A base atual distingue camada TOS e universo total. Antes de expandir TOS para novas planilhas ou para o universo completo, verificar campos disponíveis, regra de correspondência, perdas, inconsistências e rastreabilidade.

Quando não for possível aplicar TOS a um registro ou conjunto de registros, registrar a limitação em relatório de auditoria.

## Municípios

Padronizar municípios somente com fonte oficial. Preferencialmente usar IBGE para município e código IBGE. Para `município -> inspetoria -> SUREG -> CREA-BA`, usar apenas fonte oficial ou arquivo institucional validado.

Sem fonte oficial, registrar `Informação insuficiente para verificar.`

## Outliers e valores extremos

Não apagar registros sem regra documentada. Preservar o valor original, criar flags de tratamento e relatar impacto sobre n amostral, mediana, quartis, mínimo, máximo e média quando aplicável.

## Inclusão de novos anos

Ao acrescentar planilhas de outros anos, manter o mesmo pipeline metodológico:

1. ingestão padronizada;
2. validação de colunas obrigatórias;
3. deduplicação por ART;
4. classificação de confiabilidade;
5. mapeamento TOS;
6. classificação da natureza do valor;
7. padronização municipal;
8. tratamento documentado de outliers;
9. agregação por serviço, ano e município;
10. geração de relatórios de auditoria;
11. publicação apenas de dados agregados.

## Validação antes de concluir

Antes de finalizar qualquer alteração:

- executar o build disponível quando houver ambiente local;
- verificar se `index.html` continua carregando;
- validar JSON/CSV agregados;
- conferir se dados individualizados não foram publicados;
- atualizar documentação metodológica e limitações;
- registrar o que não pôde ser verificado.
