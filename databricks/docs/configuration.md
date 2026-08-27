# Configuração no Azure Databricks

Este documento detalha as configurações típicas necessárias para rodar o projeto Climate Lakehouse Azure em um ambiente Azure Databricks.

1) Cluster
- Escolha do runtime: use um Databricks Runtime compatível com Python 3.x. Se houver workloads de ML, considere o Databricks Runtime ML.
- Tipo de instância: selecione VMs conforme necessidade de memória/CPU. Para processamento pesado de Spark, prefira instâncias com mais memória.
- Autoscaling: habilite autoscaling para otimizar custo/performance quando aplicável.
- Init scripts / Libraries: instale bibliotecas customizadas no cluster (ex.: pandas, pyarrow, delta-spark) via UI ou init scripts.

2) Armazenamento
- Preferível usar Azure Data Lake Storage Gen2 (ADLS Gen2) para dados de produção.
- Opções de acesso:
  - Mounts (dbfs:/mnt/...): monte containers usando credenciais seguras.
  - abfss://...: acesse diretamente com OAuth/managed identity ou SAS.

Exemplo de mount usando SAS (não versionar chaves):

```python
# Exemplo simplificado
configs = {
  "fs.azure.account.auth.type": "SAS",
  "fs.azure.sas.token.provider.type": "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider",
  "fs.azure.sas.fixed.token": "<SAS_TOKEN_SENSITIVE>"
}

dbutils.fs.mount(
  source = "abfss://<container>@<account>.dfs.core.windows.net/",
  mount_point = "/mnt/<nome_mount>",
  extra_configs = configs
)
```

3) Segredos e credenciais
- Use Azure Key Vault + Databricks Secret Scope para armazenar segredos.
- Não incluir credenciais em notebooks ou arquivos versionados.

Criar scope apontando para Key Vault (exemplo CLI):
```
databricks secrets create-scope --scope my-scope --scope-backend-type AZURE_KEYVAULT --resource-id <keyvault-resource-id> --dns-name <keyvault-dns>
```

No notebook, acessar segredo:
```python
storage_account_key = dbutils.secrets.get(scope="my-scope", key="storage-account-key")
```

4) Jobs e agendamento
- Crie Jobs no Databricks a partir de notebooks ou tasks em Jobs API.
- Configure parâmetros (notebook parameters) para tornar notebooks reutilizáveis.

5) Rede e Segurança
- Use VNet injection se for necessário isolar o workspace.
- Habilite private endpoints para acesso ao Storage/Key Vault quando necessário.

6) Monitoramento e Logs
- Configure logging e exporte métricas (ex.: via Azure Monitor)
- Use alertas em jobs para falhas e tempos de execução anormais.

7) Boas práticas adicionais
- Versionar código reutilizável em /src e importar nos notebooks.
- Testar pipelines localmente quando possível (pandas, pytest) antes de executar em cluster.
- Documentar parâmetros esperados dos notebooks no topo de cada notebook.
