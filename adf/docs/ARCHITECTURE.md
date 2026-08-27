# ARCHITECTURE - Arquitetura (pt-BR)

Este documento descreve a arquitetura de alto nível usada pelo projeto climate com Azure Data Factory (visão focada em recursos criados via Portal).

Componentes principais
- Resource Group: grupo lógico onde os recursos são organizados.
- Storage Account / ADLS Gen2: armazenamento para landing/raw/processed/curated.
- Azure Key Vault: armazenamento seguro de segredos.
- Azure Data Factory (ADF): orquestrador de pipelines e integração com outros serviços.
- Integration Runtime: execução das atividades (Azure IR por padrão ou Self-hosted IR para redes privadas).
- (Opcional) Databricks / Synapse / Functions: motores de processamento quando necessário.

Fluxo de dados (resumo)
1. Arquivos ou dados são colocados na Landing Zone (Storage Account) — por upload direto no Portal, ingestão externa ou via outras aplicações.
2. ADF orquestra pipelines (definidos no ADF Studio) que copiam, transformam (chamando Databricks/Synapse/Functions quando necessário) e persistem dados nas camadas processed/curated.
3. Segredos e credenciais ficam no Key Vault; o ADF acessa os segredos conforme configuração de Linked Services (Key Vault references ou Managed Identity).
4. Monitoramento e logs: utilize a área "Monitor" no ADF Studio; exporte logs/telemetria para Log Analytics ou Storage se desejar centralizar.

Diagrama simplificado (Mermaid)

```mermaid
flowchart TD
  subgraph RG["Resource Group"]
    A[Storage (ADLS Gen2 - landing/raw/processed/curated)]
    B[ADF (Orquestração)]
    C[Integration Runtime (Azure IR / Self-hosted IR)]
    D[Key Vault (Segredos)]
    E[Databricks / Synapse / Functions]
    F[Log Analytics / Storage (Telemetria)]
  end

  A -->|dados brutos| B
  B -->|orquestra| C
  B -->|acessa segredos| D
  B -->|invoca processamento| E
  E -->|dados processados| A

  C -.->|acesso redes| A
  D -.->|fornece segredos| B
  B -.->|envia logs| F
'''

Observações
- Use rótulos em uma linha nos nós do Mermaid para garantir que o renderer do GitHub consiga parsear o diagrama.
- Se ainda houver problema de renderização, posso gerar uma imagem (PNG/SVG) do diagrama e adicioná-la em `docs/` para garantir visualização.

Considerações
- Separe ambientes (dev/test/prod) conforme governança — use Resource Groups e, se necessário, assinaturas diferentes.
- A separação em zonas (landing/raw/processed/curated) facilita governança, controle de acesso e ciclo de vida dos dados.

---

Atualize este documento com diagramas e detalhes específicos do ambiente caso deseje incluir redes, firewalls, VNETs ou integrações adicionais.
