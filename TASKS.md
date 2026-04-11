# TASKS.md — Evolução de CLI para Plataforma (sem rewrite e sem microserviços agora)

## Direção Arquitetural (decisão)
- [x] Manter este repositório como base principal.
- [x] Preservar a CLI atual como adapter (retrocompatibilidade).
- [x] Evoluir o `core/` para ser o engine compartilhado.
- [x] Criar uma API única consumindo o mesmo engine (modular monolith).
- [ ] Adiar microserviços até haver necessidade comprovada (escala, times, domínio).

## Objetivo dos próximos 90 dias
Entregar uma base de plataforma para desenvolvedores com:
- engine reutilizável por CLI e API;
- contratos de entrada/saída claros por caso de uso;
- execução confiável com validações, logs e testes;
- caminho preparado para extensibilidade por plugins.

---

## Sprint 0 (Semana 1-2) — Alinhar arquitetura para engine compartilhado

### 1. Contratos e Casos de Uso
- [ ] Definir casos de uso explícitos (ex: `bootstrap_environment`, `add_pre_commit`, `add_docker`, `add_alembic`).
- [ ] Formalizar DTOs de request/response no `core/` para cada caso de uso principal.
- [ ] Garantir que comandos CLI só façam parsing de input e chamada de serviço.

### 2. Limites de Camada
- [ ] Revisar `commands/` e remover lógica de negócio residual.
- [ ] Garantir que `core/` não dependa de Typer/CLI.
- [ ] Centralizar operações de shell/filesystem apenas nos módulos já destinados a isso.

### 3. Testes de Segurança da Refatoração
- [ ] Adicionar/ajustar testes unitários para os casos de uso extraídos.
- [ ] Garantir cobertura de cenários felizes + falhas acionáveis (pré-requisitos ausentes, path inválido).
- [ ] Validar retrocompatibilidade dos comandos top-level existentes.

### Definition of Done — Sprint 0
- [ ] CLI continua funcionando com o mesmo contrato público.
- [ ] Casos de uso principais possuem contratos tipados e testes.
- [ ] Nenhuma regra de negócio relevante permanece em `commands/`.

---

## Sprint 1 (Semana 3-4) — Primeira API da plataforma (adapter HTTP)

### 1. API Base
- [ ] Criar app FastAPI em módulo separado (adapter HTTP).
- [ ] Adicionar endpoint `GET /health`.
- [ ] Adicionar endpoint `POST /bootstrap-env` consumindo o mesmo service da CLI.

### 2. Operação Segura
- [ ] Implementar validação de input com schema tipado.
- [ ] Retornar erros orientados à ação (mensagens objetivas para usuário).
- [ ] Registrar logs consistentes entre CLI e API.

### 3. Testes
- [ ] Testes unitários dos handlers/controladores HTTP.
- [ ] Teste de integração do endpoint principal com doubles dos managers.
- [ ] Cobrir código HTTP de sucesso + erro de validação + erro de requisito.

### Definition of Done — Sprint 1
- [ ] Um mesmo fluxo de bootstrap pode ser acionado por CLI e API.
- [ ] API responde com contratos estáveis e previsíveis.
- [ ] Testes de regressão garantem que a entrada HTTP não quebrou o core.

---

## Sprint 2 (Mês 2) — Confiabilidade operacional e DX

### 1. Diagnóstico e Idempotência
- [ ] Criar comando/caso de uso `doctor` para validar pré-requisitos.
- [ ] Tornar fluxos críticos idempotentes quando possível.
- [ ] Adicionar modo `dry-run` para operações de geração/configuração.

### 2. Experiência de Uso
- [ ] Padronizar mensagens de erro e next-steps.
- [ ] Consolidar formato de output (info/success/warning/error).
- [ ] Revisar help dos comandos para reduzir ambiguidade.

### 3. Pipeline de Qualidade
- [ ] Garantir `make check` + `make test` no CI.
- [ ] Adicionar smoke test do pacote/CLI após build.
- [ ] Publicar guideline de troubleshooting em `docs/`.

---

## Sprint 3 (Mês 3) — Base para extensibilidade sem quebrar contratos

### 1. Extensão por Plugins (MVP)
- [ ] Definir contrato mínimo de plugin/capability.
- [ ] Implementar registro e descoberta de plugins internos.
- [ ] Entregar 1 plugin de referência sem alterar contrato da CLI principal.

### 2. Templates e Perfis
- [ ] Definir contrato versionado de profile/template.
- [ ] Implementar 1 profile inicial (ex: FastAPI + Postgres + Alembic).
- [ ] Expor listagem de profiles via CLI (e opcionalmente via API).

### 3. Governança
- [ ] Documentar critérios para extrair microserviços no futuro.
- [ ] Definir versionamento de contratos da API e de profiles.

---

## Critérios para considerar microserviços (não antes disso)
- [ ] Times diferentes precisando deploy independente por contexto.
- [ ] Gargalo real de escala isolado em parte específica do domínio.
- [ ] Fronteiras de domínio estáveis com contratos maduros.
- [ ] Observabilidade e operação prontas para sistema distribuído.

---

## Métricas de sucesso (primeira fase)
- [ ] Tempo de bootstrap de projeto previsível e repetível.
- [ ] Redução de falhas de setup por erro de ambiente.
- [ ] Cobertura de testes mantendo regras críticas protegidas.
- [ ] Mesma regra de negócio acessível por CLI e API sem duplicação.

---

## Próximos passos imediatos (ação desta semana)
- [x] Escolher o primeiro caso de uso para extração formal (`bootstrap-env`).
- [x] Criar DTO de request/response desse caso de uso.
- [x] Ajustar comando CLI para usar apenas o caso de uso.
- [x] Escrever/ajustar testes unitários e de integração do fluxo.
- [ ] Rodar `make format && make check && make test`.
