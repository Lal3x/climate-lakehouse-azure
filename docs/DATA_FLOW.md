# Fluxo de dados

## 1. Extração

### INMET

O ADF consulta as tabelas públicas:

- `basedosdados.br_inmet_bdmep.estacao`;
- `basedosdados.br_inmet_bdmep.microdados`.

A estação é filtrada por `id_estacao`. Os microdados também são filtrados por ano, com execução paralela de até dez iterações.

### Visual Crossing

O ADF obtém a chave da API no Azure Key Vault usando Managed Identity. Há dois modos:

- diário: consulta a data atual para uma cidade;
- histórico: percorre o intervalo entre `started_date` e `ended_date`, com até dez datas em paralelo.

## 2. Landing

Os dados são gravados no ADLS Gen2:

- INMET em CSV;
- Visual Crossing em JSON;
- nomes de arquivos contendo origem, estação ou cidade e timestamp.

A landing é imutável do ponto de vista lógico: transformações devem ocorrer nas camadas seguintes.

## 3. Bronze

O notebook genérico `databricks/bronze/ingest_raw.ipynb` recebe parâmetros de origem, caminho, formato, tabela, schema location, checkpoint e data de ingestão. As tarefas carregam:

- `climate.bronze.inmet_estacao_raw`;
- `climate.bronze.inmet_microdados_raw`;
- `climate.bronze.visual_crossing_raw`.

## 4. Silver

Os notebooks específicos padronizam as fontes:

- INMET → `climate.silver.climate_inmet`;
- Visual Crossing → `climate.silver.climate_visual_crossing`;
- união → `climate.silver.climate_unified`.

A tabela unificada normaliza nomes de cidades e utiliza escrita Delta por `data_ingestao`.

## 5. Gold

A Gold cria seis produtos analíticos:

1. perfil mensal consolidado por cidade;
2. perfil mensal por estação meteorológica;
3. perfil por estação do ano;
4. anomalias climatológicas;
5. ranking de meses extremos;
6. tendência interanual mensal.

## 6. Consumo

O dashboard `monitoramento_climatico_brasil.lvdash.json` consulta as tabelas Gold por meio de um SQL Warehouse.
