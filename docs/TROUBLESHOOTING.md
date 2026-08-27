# Troubleshooting

| Sintoma | Causa provável | Verificação |
| --- | --- | --- |
| ADF recebe 401/403 do Key Vault | Managed Identity sem permissão ou URL incorreta | Revise RBAC/policy e a versão do segredo |
| Copy Activity não encontra dados INMET | Estação/ano inválidos ou conexão BigQuery | Execute a consulta parametrizada diretamente |
| Visual Crossing retorna erro | Chave, cidade, data ou limite da API | Teste uma data e verifique quota |
| Arquivo não aparece no ADLS | Dataset/caminho ou permissão de escrita | Teste o linked service e confira parâmetros |
| Bronze não encontra arquivos | `source_path` diverge da landing | Compare volume, container e diretório real |
| Workflow não encontra notebook | YAML ainda usa caminhos anteriores à reorganização | Atualize `notebook_path` para `databricks/...` |
| Git source falha | URL antiga após renomear o repositório | Use `Lal3x/climate-lakehouse-azure.git` |
| Silver fica vazia | `ingestion_date` não corresponde aos dados Bronze | Compare partições e parâmetros |
| `replaceWhere` falha | Coluna/valor de partição incompatível | Verifique schema e predicado |
| União das fontes falha | Colunas ou tipos incompatíveis | Compare os schemas antes de `unionByName` |
| Tendência Gold não retorna linhas | Menos de cinco anos de histórico | Verifique `anos_disponiveis` |
| Dashboard não atualiza | Gold falhou ou IDs do warehouse/dashboard mudaram | Execute consultas manualmente |
| Trigger diário não dispara | Data final expirada | Republique o trigger com vigência correta |

## Sequência de diagnóstico

1. Identifique a última camada bem-sucedida.
2. Confirme parâmetros e data da execução.
3. Valide existência e volume dos dados.
4. Compare schemas de entrada e destino.
5. Analise logs da atividade/tarefa que falhou.
6. Reprocesse apenas o menor recorte necessário.
7. Registre causa raiz e correção.
