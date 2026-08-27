# CONTRIBUTING - Como Contribuir (pt-BR)

Obrigado por contribuir com o projeto climate-lakehouse-azure! Abaixo as diretrizes para contribuições, ajustadas ao fluxo de trabalho com recursos gerenciados via Portal.

Fluxo de trabalho
1. Trabalhe em branches no repositório GitHub: crie uma branch a partir de `main` com nome descritivo, ex.: `feature/<descrição>` ou `fix/<descrição>`.
2. Ao propor mudanças que impliquem ajuste na infra via ADF Studio (Portal), documente no PR quais alterações foram feitas no Portal (ex.: novos Linked Services, datasets, triggers) e inclua export/ARM template quando aplicável.
3. Abra um Pull Request descrevendo o objetivo, passos para testar e screenshots ou export do ADF quando necessário.

Documentação de mudanças feitas no Portal
- Quando uma alteração for feita diretamente no ADF Studio (Portal), exporte o artefato (ARM template ou JSON do pipeline) e inclua o arquivo ou instruções no PR para possibilitar revisão e re-aplicação em outros ambientes.

Segurança
- Não comitar segredos. Sempre referencie segredos via Key Vault.
- Indique no PR quando houver necessidade de permissões novas (ex.: atribuir role ao Managed Identity), e documente os passos realizados no Portal.

Regras de commit
- Use mensagens no padrão: `tipo: descrição` (ex.: `docs: atualizar linked service para storage`, `fix: corrigir trigger de agendamento`).

Revisão e validação
- Teste pipelines via Debug no ADF Studio antes de abrir PR.
- Inclua instruções de validação no corpo do PR e atribua reviewers.

---

Arquivo gerado automaticamente. Ajuste conforme o processo e políticas internas da sua equipe.