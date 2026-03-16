# Documentação para agentes de IA

Esta pasta contém recursos para auxiliar agentes de IA (como Codex, ChatGPT e GitHub Copilot) a trabalhar de forma mais eficiente e consistente neste projeto.

## Propósito

Facilitar o trabalho de agentes de IA fornecendo:
- **Prompts prontos** para tarefas comuns
- **Workflows detalhados** com passos e exemplos
- **Templates estruturados** para tarefas complexas
- **Modo staff engineer** para revisões críticas
- **Guias de Git** para sincronização de branch e geração de commits

## Estrutura dos arquivos

### [ai-prompts.md](ai-prompts.md)
**10 prompts prontos para uso imediato**

Use quando precisar de um ponto de partida rápido para tarefas comuns:
- Entender arquitetura do projeto
- Implementar features com TDD
- Refatorar código existente
- Criar testes
- Revisar código
- Preparar PR

**Como usar:** Copie o prompt desejado, ajuste os detalhes específicos (nomes de arquivos, features, etc.) e cole no chat com o agente.

---

### [ai-workflows.md](ai-workflows.md)
**8 workflows detalhados com passos e sugestões de prompts**

Use quando precisar de um guia passo a passo para fluxos mais complexos:

| Workflow | Quando usar |
|----------|-------------|
| 1. Entender código existente | Explorar funcionalidade desconhecida ou documentar componente |
| 2. Implementar nova funcionalidade | Desenvolver feature completa com TDD |
| 3. Refatorar código | Melhorar estrutura/qualidade sem alterar comportamento |
| 4. Criar testes | Adicionar cobertura de testes para código existente |
| 5. Debugar problema | Investigar e corrigir bugs ou comportamentos inesperados |
| 6. Adicionar ferramenta externa | Integrar nova dependência ou tool |
| 7. Revisar código | Code review antes de commit/PR |
| 8. Preparar PR | Validar mudanças e preparar descrição |

**Como usar:** Identifique o workflow adequado na tabela acima, siga os passos sequencialmente e use os prompts sugeridos adaptados ao seu contexto.

Workflows com execução oficial via skill:
- Workflow 4 (Criar testes) → `$api-bootstrapper-create-tests`
- Workflow 5 (Debug) → `$api-bootstrapper-debug-issue`
- Workflow 7 (Revisão técnica) → `$api-bootstrapper-review-code`

---

### [ai-task-template.md](ai-task-template.md)
**Template estruturado para tarefas complexas**

Use quando a tarefa for complexa, ambígua ou envolver múltiplas etapas interdependentes.

**Estrutura do template:**
1. **Contexto** - Situação atual e motivação
2. **Objetivo** - O que precisa ser alcançado
3. **Problema/Desafio** - Restrições e dificuldades
4. **Requisitos** - Funcionalidades e critérios obrigatórios
5. **Plano de execução** - Passos incrementais
6. **Testes** - Cenários de validação
7. **Implementação** - Checklist de entrega
8. **Validação** - Comandos e verificações finais

**Como usar:** Preencha o template com informações do seu contexto específico e forneça ao agente como instrução completa.

---

### [ai-staff-engineer-mode.md](ai-staff-engineer-mode.md)
**Modo staff engineer para revisões críticas**

Use quando precisar de:
- Revisão arquitetural rigorosa antes de grandes mudanças
- Análise de impacto e riscos de decisões técnicas
- Validação de design de componentes críticos
- Feedback sênior sobre abordagem técnica

**Como usar:** Invoque este modo explicitamente antes de solicitar análise crítica, revisão de arquitetura ou decisões técnicas importantes.

---

### [ai-commit-prompt.md](ai-commit-prompt.md)
**Guia para mensagens de commit com IA**

Use quando precisar padronizar mensagens de commit com Conventional Commits.

**Como usar:** Invoque a skill `$api-bootstrapper-generate-commit-message`.

**Fonte de verdade:** `skills/agentskills/api-bootstrapper-generate-commit-message/SKILL.md`.

---

### [ai-branch-sync-workflow.md](ai-branch-sync-workflow.md)
**Workflow de sincronização de branch antes de commitar**

Use quando for sincronizar a branch local com o remoto antes de criar novos commits.

**Como usar:** Invoque a skill `$api-bootstrapper-sync-branch`.

**Fonte de verdade:** `skills/agentskills/api-bootstrapper-sync-branch/SKILL.md`.

---

## Relação com AGENTS.md

- **AGENTS.md**: Instruções permanentes e estrutura do projeto (arquitetura, convenções, regras)
- **docs/**: Recursos práticos para execução de tarefas específicas (prompts, workflows, templates e fluxos de Git)

O agente sempre segue as regras do AGENTS.md, mas pode usar docs/ como referência para estruturar o trabalho de forma mais eficiente.

---

## Ordem de consulta recomendada

Para tarefas simples:
1. Consulte **ai-prompts.md** → copie e adapte o prompt adequado

Para tarefas intermediárias:
1. Identifique o workflow em **ai-workflows.md**
2. Siga os passos e use os prompts sugeridos

Para tarefas complexas:
1. Preencha **ai-task-template.md** com contexto completo
2. Forneça ao agente como instrução estruturada

Para revisões críticas:
1. Invoque **ai-staff-engineer-mode.md** explicitamente
2. Solicite análise ou revisão técnica

Para criação de testes, debug e review técnico com execução padronizada:
1. Use `api-bootstrapper-create-tests` para cobrir lacunas de teste
2. Use `api-bootstrapper-debug-issue` para fluxo reproduzir → testar → corrigir
3. Use `api-bootstrapper-review-code` para revisão por severidade e riscos

Para tarefas de commit/sincronização de branch:
1. Siga **ai-branch-sync-workflow.md** antes de sincronizar
2. Use **ai-commit-prompt.md** para gerar mensagens de commit consistentes

---

## Contribuindo

Ao adicionar novos recursos nesta pasta:
- Mantenha consistência com estrutura existente
- Adicione exemplos práticos sempre que possível
- Atualize este README.md com o novo conteúdo
- Valide que os exemplos seguem as convenções do AGENTS.md
