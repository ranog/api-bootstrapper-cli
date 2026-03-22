# API Bootstrapper CLI Roadmap

Este documento descreve a evolução planejada do `api-bootstrapper-cli` com foco em entregas incrementais, baixo risco e manutenção da arquitetura atual.

## Objetivo

Evoluir o CLI para cobrir o ciclo completo de bootstrap de APIs Python com:

- setup de ambiente consistente
- geração de configurações de qualidade e DX
- suporte a perfis de projeto reutilizáveis
- integração gradual com workflows de IA

## Estado atual (março/2026)

Entregas já disponíveis:

- ✅ `init` para scaffolding inicial
- ✅ `bootstrap-env` com suporte a `pyenv` e `uv`
- ✅ `add-pre-commit`, `add-docker`, `add-alembic` e `add-mypy`
- ✅ comandos agrupados por sub-apps (`env`, `hooks`, `db`) com retrocompatibilidade no topo
- ✅ instalação de skills (`install-skills`, `install-agent-skills`)

Gap principal identificado no próprio projeto:

- ⬜ perfis prontos (ex: `fastapi-postgres-clean-arch`)

## Fase 1 - Perfis de projeto (prioridade alta)

Objetivo: reduzir tempo de setup com templates opinativos e consistentes.

### Itens

- [ ] definir contrato de profile (estrutura, variáveis e arquivos opcionais)
- [ ] implementar profile inicial `fastapi-postgres-clean-arch`
- [ ] suportar seleção de profile no fluxo de `init`
- [ ] adicionar testes cobrindo geração e fallback quando profile não existir

### Critério de pronto

Um usuário consegue iniciar projeto com profile e executar fluxo completo (`init` → `bootstrap-env` → `add-*`) sem ajustes manuais obrigatórios.

## Fase 2 - Robustez operacional (prioridade alta)

Objetivo: tornar o CLI mais previsível em ambientes reais (local/CI).

### Itens

- [ ] comando `doctor` para validar pré-requisitos (pyenv/uv/poetry/docker)
- [ ] validações antecipadas de caminho/projeto antes de executar managers
- [ ] padronização de mensagens de erro orientadas à ação
- [ ] testes de integração para cenários de erro recorrentes

### Critério de pronto

Falhas comuns são detectadas no início do fluxo e retornam mensagem objetiva com próximo passo claro.

## Fase 3 - Extensibilidade (prioridade média)

Objetivo: facilitar evolução sem quebrar contratos existentes.

### Itens

- [ ] consolidar interface para novos templates/módulos opcionais
- [ ] mapear pontos de extensão sem acoplamento com `commands/`
- [ ] expandir cobertura de testes para novos managers via protocolos existentes

### Critério de pronto

Novos recursos conseguem ser adicionados por manager/service com mudanças pequenas e localizadas.

## Fase 4 - Produtividade com IA (prioridade média)

Objetivo: integrar melhor o CLI com os fluxos de trabalho já documentados em `docs/` e `skills/`.

### Itens

- [ ] revisar catálogo de prompts e workflows para refletir features atuais
- [ ] adicionar guias de uso por cenário (novo projeto, manutenção, migração)
- [ ] validar consistência entre `AGENTS.md`, `docs/` e skills instaláveis

### Critério de pronto

Documentação e skills apontam para o mesmo fluxo, sem duplicidade nem conflito de instruções.

## Princípios de execução

- manter comandos CLI finos e orquestradores
- preservar lógica em managers/services e contratos em protocols
- entregar mudanças pequenas, com testes de comportamento
- evitar expansão de escopo sem necessidade clara

## Como usar este roadmap

- revisar prioridades a cada release
- converter cada item em issues pequenas e atômicas
- atualizar este documento quando uma fase mudar de status
