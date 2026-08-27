# Documentação — Climate Lakehouse Azure

Esta pasta reúne a documentação técnica e operacional da plataforma de dados climáticos.

## Índice

| Documento | Conteúdo |
| --- | --- |
| [Arquitetura](ARCHITECTURE.md) | Componentes, responsabilidades e decisões arquiteturais |
| [Fluxo de dados](DATA_FLOW.md) | Jornada dos dados da origem até o dashboard |
| [Azure Data Factory](ADF.md) | Pipelines, datasets, linked services, parâmetros e triggers |
| [Azure Databricks](DATABRICKS.md) | Camadas Bronze, Silver e Gold e workflow |
| [Catálogo de dados](DATA_CATALOG.md) | Tabelas, granularidade e principais campos |
| [Implantação](DEPLOYMENT.md) | Pré-requisitos e roteiro de configuração |
| [Operação](OPERATIONS.md) | Execução, reprocessamento, monitoramento e validação |
| [Segurança](SECURITY.md) | Identidades, segredos, permissões e checklist |
| [Troubleshooting](TROUBLESHOOTING.md) | Diagnóstico dos problemas mais comuns |
| [Pendências e evolução](ROADMAP.md) | Limitações conhecidas e próximos passos |

## Escopo

A solução ingere dados meteorológicos do INMET, por meio do conjunto público Base dos Dados no BigQuery, e da API Visual Crossing. O ADF grava os arquivos no ADLS Gen2; o Databricks processa as camadas Bronze, Silver e Gold em Delta Lake; um dashboard Databricks SQL apresenta os indicadores climáticos.

## Ambientes

Os artefatos versionados foram criados para desenvolvimento e contêm o sufixo `dev`. Para outros ambientes, parametrize nomes de recursos, caminhos, identidades, endpoints e agendas. Não reutilize IDs ou URLs específicos de desenvolvimento sem validação.
