# Segurança

## Identidades

Use Managed Identity para o ADF acessar Key Vault e ADLS. No Databricks, prefira Access Connector/Managed Identity e external locations governadas pelo Unity Catalog.

## Segredos

- Nunca versione chaves, tokens, connection strings ou credenciais.
- Armazene a chave da Visual Crossing no Key Vault.
- Evite fixar a versão do segredo na URL; prefira buscar a versão atual quando possível.
- Marque entradas e saídas de atividades sensíveis como seguras quando puderem registrar valores.
- Não exponha segredos em logs, notebooks ou parâmetros de job.

## Menor privilégio

| Identidade | Acesso mínimo |
| --- | --- |
| ADF Managed Identity | Ler segredo necessário e gravar na landing |
| Databricks | Ler landing e gerenciar tabelas/volumes autorizados |
| Usuários analíticos | Consultar apenas schemas Gold necessários |
| CI/CD | Publicar somente nos recursos e ambientes definidos |

## Pontos a revisar no estado atual

- As pipelines exportadas contêm URL e versão específicas do segredo.
- Algumas atividades possuem `secureOutput: false`.
- O workflow usa placeholders para assinante, warehouse ID e dashboard ID; preencha-os apenas no ambiente de destino.
- Nomes de recursos de desenvolvimento aparecem nos artefatos.
- O repositório permanece privado; antes de torná-lo público, faça secret scanning.

## Checklist antes de publicar

- executar busca por chaves, tokens e connection strings;
- revisar o histórico Git, não apenas os arquivos atuais;
- remover IDs ou e-mails que não devam ser públicos;
- substituir valores de ambiente por placeholders;
- habilitar proteção de branch, Dependabot e secret scanning;
- documentar dados e licenças das fontes.
