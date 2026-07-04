# data/local

Diretório reservado para arquivos locais, brutos, intermediários ou linha a linha.

## Regra

Esta pasta não deve ser usada para publicar dados no GitHub Pages.

Arquivos reais desta pasta devem permanecer fora do versionamento quando contiverem dados individualizados de ARTs.

## Exemplos de arquivos que devem permanecer locais

- planilhas anuais completas de ARTs;
- CSVs linha a linha;
- bases com `id_art`;
- bases com valor individual declarado;
- bases com município por registro individual;
- bases com formação por registro individual;
- bases intermediárias de deduplicação;
- relatórios operacionais com dados sensíveis.

## Como usar

Manter neste diretório apenas este `README.md` versionado. Os demais arquivos locais devem ser protegidos pelo `.gitignore`.
