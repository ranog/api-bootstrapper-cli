# AI Branch Sync Workflow

Este documento é um guia rápido para uso humano.

A execução oficial para agentes está na skill:
- `$api-bootstrapper-sync-branch`

## Como usar

Peça ao agente:

```text
Use $api-bootstrapper-sync-branch para sincronizar a branch atual.
```

Parâmetros úteis:
- `remote` (padrão: `origin`)
- `default_branch` (opcional; quando ausente, a skill detecta automaticamente)

## Fonte de verdade

O comportamento detalhado (passos, confirmação explícita e tratamento de conflito) está em:
- `skills/agentskills/api-bootstrapper-sync-branch/SKILL.md`
- `skills/agentskills/api-bootstrapper-sync-branch/references/parameters-and-errors.md`
