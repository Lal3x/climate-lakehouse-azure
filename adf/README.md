# climate-lakehouse-azure

Repositório para pipelines implementados no Azure Data Factory (ADF) para o projeto "climate".

Esta documentação foi escrita considerando operações realizadas via Azure Portal (interface web). A pasta `docs/` contém guias de configuração, arquitetura, uso e contribuições em Português (pt-BR).

Arquivos principais
- docs/SETUP.md — Guia de configuração do ambiente pelo Azure Portal (Resource Group, Storage/ADLS Gen2, Key Vault, Data Factory) e observações sobre a nomenclatura CAF.
- docs/ARCHITECTURE.md — Visão da arquitetura, fluxo de dados e diagrama (Mermaid) com orientação para recursos criados via Portal.
- docs/USAGE.md — Como usar o ADF Studio: debug, triggers, monitoramento e import/export de pipelines.
- docs/CONTRIBUTING.md — Como documentar alterações feitas no Portal, fluxo de PR e convenções de commit.

Status
- Documentação inicial criada e atualizada (pt-BR). Diagrama Mermaid ajustado para garantir renderização no GitHub.

Segurança e boas práticas
- Não comitar segredos no repositório — utilize Azure Key Vault e referências a segredos em Linked Services.
- Prefira Managed Identity para autenticação entre recursos Azure.
- Siga a Cloud Adoption Framework (CAF) para padronização de nomenclatura dos recursos.

Como contribuir
- Faça alterações em branches a partir de `main` e abra Pull Requests com descrição clara e instruções de teste.
- Ao modificar recursos diretamente no ADF Studio (Portal), exporte o artefato (ARM/template JSON) e anexe ao PR para revisão e replay em outros ambientes.

Links úteis
- Azure Portal: https://portal.azure.com
- Azure Data Factory Studio: abrir via recurso ADF no Portal (Open Azure Data Factory Studio)

---

Se quiser, posso:
- adicionar templates de Issue/Pull Request;
- incluir um exemplo de export de pipeline em docs/;
- gerar uma imagem do diagrama Mermaid e anexá-la para garantir visualização.

