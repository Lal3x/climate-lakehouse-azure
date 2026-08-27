# Operação

## Execução diária

1. Verifique o trigger do ADF.
2. Confirme a chegada do JSON da Visual Crossing na landing.
3. Execute ou acompanhe o workflow Databricks para a mesma `ingestion_date`.
4. Confirme as contagens Bronze e Silver.
5. Valide a atualização das tabelas Gold e do dashboard.

## Carga histórica

Para Visual Crossing, informe `city`, `started_date` e `ended_date`. Para INMET, informe `id_estacao`, `startYear` e `endYear`. Comece com intervalo curto para observar limites e custos.

## Reprocessamento

A Silver grava a partição da data usando `replaceWhere`. Para reprocessar:

1. confirme os arquivos da landing;
2. reutilize a mesma `ingestion_date`;
3. execute Bronze e Silver na ordem;
4. recalcule a Gold;
5. compare contagens e métricas antes e depois.

## Validações mínimas

- contagem maior que zero em cada tabela esperada;
- ausência de datas futuras;
- temperatura máxima maior ou igual à mínima;
- umidade entre 0 e 100;
- precipitação não negativa;
- unicidade coerente com o grão;
- cobertura temporal por cidade;
- divergências entre fontes monitoradas.

## Monitoramento

No ADF, acompanhe duração, volume lido/escrito e falhas de Copy Activity. No Databricks, acompanhe duração por tarefa, retries, volume processado, falhas de schema e custo de compute.

## Evidências operacionais

Registre para cada execução:

- run ID do ADF;
- job run ID do Databricks;
- `ingestion_date`;
- arquivos processados;
- contagens por camada;
- status final;
- erro e ação corretiva, quando aplicável.
