# SETUP - Configuração do Ambiente (pt-BR)

Este documento descreve o passo a passo, usando o Azure Portal (interface web), para criar o ambiente necessário para rodar os pipelines do projeto climate no Azure Data Factory (ADF).

Observação importante: seguimos a Cloud Adoption Framework (CAF) para nomenclatura dos recursos — adapte os exemplos conforme o padrão CAF da sua organização.

Pré-requisitos
- Conta com assinatura Azure com permissões para criar recursos (Contributor/Owner) na assinatura/escopo desejado.
- Acesso ao Azure Portal (https://portal.azure.com) com a conta apropriada.

Recursos a serem criados
- Resource Group (RG)
- Storage Account (Azure Blob / ADLS Gen2)
- Key Vault (armazenar segredos e credenciais)
- Azure Data Factory (ADF)

Passo a passo pelo Azure Portal

1) Criar Resource Group
- Acesse o Azure Portal (https://portal.azure.com).
- No menu lateral, clique em "Resource groups" e depois em "+ Create".
- Selecione a Subscription correta, informe o nome do Resource Group seguindo o padrão CAF (ex.: rg-dev-climate-brazilsouth) e escolha a região (ex.: Brazil South).
- Clique em "Review + create" e em seguida "Create".

2) Criar Storage Account (ADLS Gen2)
- No Azure Portal, no menu lateral, clique em "Storage accounts" e em "+ Create".
- Selecione a Subscription e o Resource Group criado anteriormente.
- Informe o nome da Storage Account (respeitando regras de nomenclatura: apenas letras minúsculas e números), por exemplo: stdevclimate001.
- Em "Performance" e "Replication" escolha conforme sua necessidade; em "Advanced" habilite "Hierarchical namespace" para ADLS Gen2, se for necessário.
- Clique em "Review + create" e depois em "Create".

3) Criar Key Vault
- No Azure Portal, busque por "Key Vaults" e clique em "+ Create".
- Selecione a Subscription e Resource Group corretos.
- Defina um nome (ex.: kv-dev-climate-01) seguindo a política CAF.
- Configure acesso (política de acesso baseada em RBAC ou Access Policies, conforme o modelo da sua organização).
- Clique em "Review + create" e depois em "Create".
- Para adicionar segredos: abra o Key Vault criado, vá em "Secrets" e clique em "+ Generate/Import" para criar segredos como strings de conexão.

4) Criar Azure Data Factory
- No Azure Portal, busque por "Data Factories" e clique em "+ Create".
- Escolha a Subscription e o Resource Group criados.
- Informe um nome (ex.: adf-dev-climate-01) e a região.
- Siga os passos do assistente e clique em "Review + create" e "Create".

Configurar integrações e permissões pelo Portal

- Managed Identity (Identidade Gerenciada):
  - Abra o recurso Data Factory criado, vá em "Identity" (ou "Managed identities"). Habilite a System-assigned managed identity se desejar que o ADF tenha uma identidade no Azure AD.

- Conceder permissões no Storage Account:
  - Abra a Storage Account, vá em "Access control (IAM)" e clique em "+ Add role assignment".
  - Atribua a role "Storage Blob Data Contributor" (ou a role adequada) ao principal (Managed Identity do ADF ou ao Service Principal que for usar).

- Conceder acesso ao Key Vault:
  - Se estiver usando Access Policies: abra o Key Vault -> "Access policies" -> "+ Add Access Policy" e conceda as permissões de "Get" e "List" para Secrets ao principal (Managed Identity do ADF).
  - Se estiver usando RBAC para Key Vault: vá em "Access control (IAM)" do Key Vault e atribua a role adequada ao principal.

- Configurar Linked Services no ADF para usar Key Vault:
  - No ADF Studio (abrir via "Open Azure Data Factory Studio" no blade do recurso), ao criar um Linked Service (ex.: Azure Blob Storage/ADLS Gen2), selecione a opção para usar Azure Key Vault ou Managed Identity para referenciar segredos em vez de colocar credenciais em claro.

Considerações de segurança
- Não armazene segredos no repositório. Utilize o Key Vault e referências a segredos nas Linked Services do ADF.
- Prefira Managed Identity (identidade gerenciada) para atribuir permissões a recursos Azure ao invés de usar credenciais estáticas.

Boas práticas de nomenclatura (CAF)
- Resource Group: rg-{env}-{aplicacao}-{location}
- Storage Account: st{aplicacao}{env}{nn}
- Key Vault: kv-{env}-{aplicacao}-{nn}
- Data Factory: adf-{env}-{aplicacao}-{nn}

Adapte as regras conforme o padrão CAF da sua organização (prefixos, sufixos, tags, etc.).

---

Este arquivo foi criado para documentar os passos realizados via Azure Portal. Ajuste os detalhes conforme as políticas e nomes da sua organização.