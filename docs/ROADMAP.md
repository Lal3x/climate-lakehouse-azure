# Pendências e evolução

## Prioridade alta

- Revisar a vigência do trigger diário.
- Tornar seguras as entradas/saídas que possam conter a chave da API.
- Parametrizar nomes de recursos Azure por ambiente.
- Validar a migração dos recursos existentes de `climate` para os novos nomes antes do deploy.

## Qualidade

- Adicionar testes automatizados para transformações PySpark.
- Implementar testes de schema, unicidade, faixa e completude.
- Gerar relatório de qualidade por `ingestion_date`.
- Adicionar CI para validar JSON, notebooks, YAML e Python.

## Infraestrutura

- Provisionar recursos com Terraform ou Bicep.
- Parametrizar ambientes `dev`, `hml` e `prd`.
- Automatizar deploy de ADF e Databricks Asset Bundles.
- Adicionar políticas de cluster e budgets.

## Observabilidade

- Centralizar logs no Azure Monitor/Log Analytics.
- Criar alertas de atraso, falha e volume anormal.
- Registrar lineage e SLAs dos datasets.
- Publicar métricas de custo e duração por execução.

## Portfólio

- Adicionar imagem do dashboard ao README.
- Incluir exemplos de consultas e resultados.
- Publicar um diagrama de arquitetura renderizado.
- Disponibilizar dados sintéticos ou amostras reproduzíveis.
- Adicionar licença e descrição curta do repositório.
