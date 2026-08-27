# Notebooks — Boas práticas e templates

Este arquivo descreve recomendações para estruturar e padronizar notebooks no projeto.

Estrutura sugerida de um notebook
- Cabeçalho com objetivo, autor, data e parâmetros esperados
- Seção de dependências (instalação/imports)
- Seção de configuração (leitura de segredos, paths, mounts)
- Pipeline dividido em passos (ingestão, limpeza, transformação, escrita)
- Seção de testes/validação (pequenas asserções ou amostras)
- Seção de limpeza (encerrar conexões, liberar recursos)

Exemplo de cabeçalho (template):
```python
# Notebook: ingest_data
# Objetivo: Ingestão de dados brutos do container X para o bronze
# Autor: <Nome>
# Data: 2026-08-07

# Parâmetros esperados:
# - input_path: caminho de origem (ex: abfss://...)
# - output_path: caminho de saída (ex: /mnt/bronze/...)
```

Sobre modularização
- Evite colocar toda a lógica diretamente no notebook quando possível.
- Coloque funções reutilizáveis em /src e importe via sys.path ou pacotes instaláveis.

Questões sobre execução
- Prefira notebooks pequenos e idempotentes para facilitar reruns e debugging.
- Use widgets/parameters do Databricks para tornar notebooks configuráveis ao rodar como Jobs.

Exemplo rápido: leitura de parâmetro com widgets
```python
dbutils.widgets.text("input_path", "")
input_path = dbutils.widgets.get("input_path")
```

Manter exemplos
- Para cada fluxo (ex.: ingestão, transformação, modelo) mantenha um notebook de exemplo com dados de amostra para desenvolvedores.

