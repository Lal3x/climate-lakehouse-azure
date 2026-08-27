# Azure Data Factory

## Artefatos

```text
adf/
├── datasets/
├── linked-services/
├── pipelines/
├── triggers/
└── docs/
```

## Pipelines

| Pipeline versionado | Finalidade | Parâmetros |
| --- | --- | --- |
| `pl_ingest_inmet_estacao_landing_dev` | Copiar cadastro de uma estação do BigQuery | `id_estacao`, `ano` |
| `pl_ingest_inmet_microdados_landing_dev` | Copiar microdados por estação e intervalo anual | `id_estacao`, `startYear`, `endYear` |
| `pl_ingest_visualcrossing_landing_dev_daily` | Capturar o dia corrente para uma cidade | `city` |
| `pl_ingest_visualcrossing_landing_dev_history` | Capturar um intervalo de datas | `city`, `started_date`, `ended_date` |

Os nomes internos exportados ainda usam `lading` em alguns pontos. O nome correto é `landing`; consulte o roadmap antes de alterar referências no ADF publicado.

## Linked services

- `ls_adlsg2_climate_dev`: acesso ao ADLS Gen2;
- `ls_akv_climate_dev`: integração com Azure Key Vault;
- `ls_bigquery_climate_dev`: conexão com BigQuery;
- `ls_http_visualcrossing`: endpoint HTTP da Visual Crossing.

## Datasets

Os datasets usam parâmetros para construir os caminhos de origem e destino. Antes do deploy, valide:

- containers e diretórios do ADLS;
- delimitador, cabeçalho e encoding dos CSVs;
- URL base e parâmetros da API;
- autenticação do BigQuery;
- referências dos linked services.

## Trigger diário

O artefato `tr_daily_visualcrossing_dev` foi configurado para:

- frequência diária;
- 07:00;
- fuso `E. South America Standard Time`;
- cidade `recife`.

A configuração versionada possui início em 5 de agosto de 2026 e término em 6 de agosto de 2026. Portanto, ela deve ser revisada e republicada para permanecer ativa.

## Execução manual

1. Publique linked services e datasets.
2. Teste cada conexão.
3. Execute primeiro o pipeline diário com uma cidade.
4. Confirme o arquivo na landing.
5. Execute um intervalo histórico pequeno.
6. Só então amplie o intervalo ou a quantidade de estações.

## Concorrência

Os pipelines históricos usam `batchCount: 10`. Ajuste esse valor considerando limites da API, Integration Runtime, BigQuery e Storage.
