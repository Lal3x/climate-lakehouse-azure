# Implantação

## Pré-requisitos

- assinatura Azure;
- Resource Group;
- Azure Data Factory;
- ADLS Gen2;
- Azure Key Vault;
- Azure Databricks com Unity Catalog;
- SQL Warehouse;
- acesso ao BigQuery/Base dos Dados;
- chave da Visual Crossing;
- permissões para publicar pipelines, jobs e dashboard.

## Ordem recomendada

1. Criar o Storage e habilitar namespace hierárquico.
2. Criar containers/volumes de landing e camadas do lakehouse.
3. Criar o Key Vault e armazenar a chave da Visual Crossing.
4. Habilitar Managed Identity no ADF.
5. Conceder ao ADF leitura do segredo e escrita no Storage.
6. Importar linked services e testar conexões.
7. Importar datasets, pipelines e trigger.
8. Configurar Databricks, Unity Catalog e credenciais para ADLS.
9. Criar catálogo e schemas `climate.bronze`, `climate.silver` e `climate.gold`.
10. Atualizar o YAML do workflow para os caminhos atuais.
11. Importar o dashboard e substituir seus IDs no workflow.
12. Executar um smoke test de ponta a ponta.

## Variáveis específicas do ambiente

Não promova diretamente os valores de desenvolvimento. Parametrize:

- nomes do Storage Account, container e Key Vault;
- URL/versionamento do segredo;
- catálogo, schemas e external locations;
- cidade, estação e intervalos;
- URL e branch do Git;
- warehouse ID e dashboard ID;
- destinatários de notificações;
- agenda e fuso do trigger.

## Smoke test

Use uma cidade, uma estação e uma única data. Valide:

- arquivo criado na landing;
- três tabelas Bronze acessíveis;
- tabelas Silver com registros da data;
- `climate_unified` não vazia;
- tabelas Gold atualizadas;
- consultas do dashboard executando sem erro.

## Promoção

Adote artefatos separados ou parâmetros para `dev`, `hml` e `prd`. Para produção, prefira infraestrutura como código e identidades distintas por ambiente.
