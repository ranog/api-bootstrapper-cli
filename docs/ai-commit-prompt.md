# AI Commit Prompt

Este documento é um guia rápido para uso humano.

A execução oficial para agentes está na skill:
- `$api-bootstrapper-generate-commit-message`

## Como usar

Peça ao agente:

```text
Use $api-bootstrapper-generate-commit-message para sugerir a mensagem de commit com base no diff atual.
```

Parâmetros úteis:
- `scope_fallback` (padrão: `cli`)
- `prefer_staged` (padrão: `true`)

## Fonte de verdade

O comportamento detalhado (análise de diff, seleção do tipo e padrão de mensagem) está em:
- `skills/agentskills/api-bootstrapper-generate-commit-message/SKILL.md`
- `skills/agentskills/api-bootstrapper-generate-commit-message/references/parameters-and-errors.md`
