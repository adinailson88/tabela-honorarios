# data/public

Diretório reservado para dados agregados que podem alimentar o painel publicado no GitHub Pages.

## Permitido

- JSON agregado para visualização;
- CSV agregado por serviço, ano, município ou grupo;
- estatísticas agregadas;
- contagens agregadas;
- metadados metodológicos sem identificação individual.

## Não permitido

- `id_art`;
- linha individual de ART;
- nome de profissional;
- nome de empresa;
- nome de contratante;
- valor individual por ART;
- município associado a registro individual;
- formação associada a registro individual.

## Observação

O arquivo `dados_tos_valor_municipio.json` ainda permanece na raiz por compatibilidade com o painel atual. Uma migração futura para esta pasta exige atualização e teste do script de build.
