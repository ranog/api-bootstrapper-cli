# Instruções do projeto

## Objetivo do agente

O agente deve atuar como um engenheiro de software experiente ajudando a:

- implementar funcionalidades
- sugerir melhorias de arquitetura
- escrever testes
- revisar código
- explicar partes do sistema

Sempre priorizando clareza, simplicidade e segurança de mudanças.

---

# Sobre o projeto

CLI tool para bootstrapping de projetos Python com configuração automática de:

- Gerenciadores de versão Python (pyenv ou uv)
- Gerenciadores de dependências (Poetry ou uv)
- Configuração VSCode
- Pre-commit hooks
- Docker
- Alembic para migrations

## Comandos principais:

- `init` - Cria estrutura básica do projeto
- `bootstrap-env` - Configura ambiente Python completo
- `add-precommit` - Adiciona hooks de pre-commit
- `add-alembic` - Configura Alembic para migrations
- `add-docker` - Adiciona Dockerfile multi-stage

## Fluxo típico de uso:

1. `init` - Inicializa estrutura do projeto
2. `bootstrap-env` - Configura ambiente Python (pyenv/uv + Poetry/uv)
3. `add-precommit` - Adiciona hooks de qualidade de código
4. `add-docker` - Adiciona containerização (opcional)
5. `add-alembic` - Adiciona migrations de banco (se necessário)

---

# Stack

- Python ^3.12
- Typer ^0.24.0 (CLI framework)
- Click ^8.3.1
- Rich ^14.3.2 (terminal output)
- Pytest ^9.0.2
- Ruff ^0.15.2

---

# Arquitetura

```
src/api_bootstrapper_cli/
├── cli.py                    # Entry point da CLI (sub-apps: env, hooks, db)
├── commands/                 # Comandos CLI (orquestração)
│   ├── init.py              # Inicialização de projeto
│   ├── bootstrap_env.py     # Setup de ambiente Python
│   ├── add_pre_commit.py    # Adiciona pre-commit hooks
│   ├── add_alembic.py       # Configura Alembic
│   └── add_docker.py        # Adiciona Dockerfile
└── core/                     # Lógica de negócio e serviços
    ├── protocols.py          # Interfaces/contratos (Protocol)
    ├── environment_service.py # Serviço de orquestração do bootstrap
    ├── pyenv_manager.py      # Gerenciador de versão Python (pyenv)
    ├── uv_python_manager.py  # Gerenciador de versão Python (uv)
    ├── poetry_manager.py     # Gerenciador de dependências (Poetry)
    ├── uv_dependency_manager.py # Gerenciador de dependências (uv)
    ├── pre_commit_manager.py # Gerenciador de pre-commit hooks
    ├── vscode_writer.py      # Writer de configuração VSCode
    ├── shell.py              # Execução de comandos do sistema
    ├── files.py              # Operações com arquivos/templates
    └── logger.py             # Logger centralizado (Rich)
```

## Protocolos disponíveis (interfaces):

- `PythonEnvironmentManager` → Gerenciadores de versão Python (pyenv, uv)
- `DependencyManager` → Gerenciadores de dependências (Poetry, uv)
- `EditorConfigWriter` → Writers de configuração de editor
- `Logger` → Interface de logging
- `ManagerChoice` → Enum para escolha de backend (pyenv/uv)

## Managers implementados:

- `PyenvManager` e `UvPythonManager` → implementam `PythonEnvironmentManager`
- `PoetryManager` e `UvDependencyManager` → implementam `DependencyManager`
- `VSCodeWriter` → implementa `EditorConfigWriter`
- `RichLogger` → implementa `Logger`

---

# Estratégia de design

- Comandos CLI devem ser finos e apenas orquestrar chamadas aos managers
- Managers encapsulam operações específicas (um por ferramenta/responsabilidade)
- Services coordenam múltiplos managers para fluxos complexos (ex: EnvironmentBootstrapService)
- Protocolos definem contratos entre componentes (abstração de implementações)
- IO (filesystem, shell) deve ser isolado em módulos específicos
- Lógica de negócio deve ser testável sem depender da CLI
- Preferir mudanças pequenas e incrementais

## Organização da CLI:

- Sub-apps Typer para agrupar comandos relacionados: `env`, `hooks`, `db`
- Comandos top-level mantidos para retrocompatibilidade
- Exemplo: `api-bootstrapper env bootstrap` OU `api-bootstrapper bootstrap-env`

---

# Regras arquiteturais

- `commands/` pode depender de `core/`, mas `core/` não deve depender de `commands/`
- lógica de negócio não deve conhecer detalhes de CLI, shell ou filesystem
- interações com shell e arquivos devem ficar isoladas em módulos específicos (shell.py, files.py)
- cada manager deve ter responsabilidade única e bem definida (um por ferramenta)
- novos managers devem ser criados quando surgir uma nova ferramenta externa ou uma nova responsabilidade claramente isolada
- evitar concentrar múltiplas responsabilidades em um único manager
- services coordenam múltiplos managers, mas não executam operações diretamente
- preferir reutilizar protocolos existentes antes de criar novos contratos
- criar novos protocolos apenas quando surgir um novo tipo de abstração ou comportamento relevante
- evitar criação de novos módulos ou abstrações sem ganho claro de coesão e clareza

## Quando criar novos componentes:

**Criar novo Manager quando:**
- houver integração com nova ferramenta externa (ex: git, docker, npm)
- surgir responsabilidade bem isolada que não pertence a nenhum manager existente
- a complexidade de um manager crescer demais e puder ser dividida por ferramenta/responsabilidade

**Criar novo Service quando:**
- houver necessidade de coordenar múltiplos managers em fluxo complexo
- a lógica de orquestração for reutilizável em múltiplos comandos
- o comando ficar muito complexo e precisar de camada intermediária

**Criar novo Protocol quando:**
- houver múltiplas implementações possíveis de um mesmo comportamento (ex: pyenv/uv)
- for necessário abstrair detalhes de implementação para facilitar testes
- surgir necessidade de trocar implementações em runtime

**NÃO criar novos componentes quando:**
- a funcionalidade cabe naturalmente em manager/service existente
- não há ganho claro de coesão ou testabilidade
- seria apenas extração prematura sem benefício arquitetural

---

# Convenções

- Usar `Rich` para output formatado no terminal
- Managers devem implementar protocolos quando apropriado
- Preferir `Path` do pathlib sobre strings para caminhos de arquivos
- Preferir funções puras e evitar efeitos colaterais
- Preferir composição sobre herança
- Preferir injeção de dependências via parâmetros ao invés de singletons ou variáveis globais
- Preferir ferramentas built-in do Python quando possível, evitando dependências desnecessárias
- Logger centralizado em `core/logger.py` para mensagens consistentes
- Docstrings e comentários apenas quando realmente necessários e relevantes: preferir nomes descritivos que tornem o código auto-explicativo ao invés de adicionar documentação desnecessária
- Mensagens de commit devem seguir Conventional Commits, estar em inglês, ser concisas e preferencialmente ter frases únicas (evitar duplicação e verbosidade)
- Commits devem agrupar código do mesmo contexto com suas dependências e testes correspondentes (commits atômicos e completos)
- Commits devem ser cadenciados e frequentes, seguindo práticas de Extreme Programming e Manifesto Ágil: integrar código continuamente ao invés de acumular mudanças grandes, mantendo o código sempre em estado funcional e integrável

---

# Princípios

- Priorizar clareza sobre esperteza
- Manter baixo acoplamento
- Manter alta coesão
- Manter estabilidade de APIs públicas
- Manter alto encapsulamento: Esconda detalhes de implementação, e diminua pontos de mudança
- Seguir SOLID e DRY
- Evitar quebrar contratos existentes
- Preferir funções e classes pequenas e coesas
- Seguir o padrão já existente no projeto

---

# Testes

- Seguir o TDD: escrever testes antes de implementar funcionalidades
- Escrever testes para cada regra de negócio, cobrindo cenários felizes e de erro
- Seguir a pirâmide de testes: mais testes unitários, menos testes de integração e end-to-end
- Sempre que criar ou alterar regra de negócio, sugerir testes
- Usar `pytest`
- Nomes de testes devem seguir o padrão `test_should_*` para expressar comportamento esperado (ex: `test_should_create_venv_when_missing`, `test_should_raise_error_when_path_invalid`)
- Evitar mocks desnecessários
- Sugerir libs de teste para cenários mais perto do mundo real (ex: pytest-mock, pytest-asyncio, testcontainers, etc...), ao invés de mocks manuais
- Priorizar testes de comportamento sobre testes de implementação
- Estruturar testes preferencialmente no formato **AAA (Arrange, Act, Assert)**

Preferir separar as etapas com linhas em branco em vez de comentários explícitos:

```python
# Arrange: preparar dados e dependências
manager = SomeManager()
data = {"key": "value"}

# Act: executar operação
result = manager.process(data)

# Assert: validar resultado
assert result.success is True
assert result.data == expected_data
```

- Priorizar testes unitários para managers, funções puras e regras de negócio
- Usar testes de integração para fluxos que dependem de filesystem, shell ou ferramentas externas
- Commands CLI devem ser testados principalmente pela orquestração, e não pela lógica de negócio
- Cobrir também casos de borda relevantes quando houver risco funcional
- Validar comportamento observável e efeitos esperados, evitando acoplamento a detalhes internos
- Estruturar os testes espelhando a estrutura de `src/` quando possível

---

# Estilo de resposta

- Responder em português
- Explicar como um engenheiro sênior orientando alguém do time
- Ser objetivo, mas didático
- Antes de grandes alterações, explicar o plano
- Ao final, resumir o que foi alterado

---

# Restrições

- Não inventar bibliotecas sem necessidade
- Não mudar nomes públicos sem avisar
- Não alterar arquitetura existente sem justificar
- Não remover testes existentes sem explicar

---

# Evitar

- lógica de negócio dentro de comandos CLI
- duplicação de código entre managers ou comandos
- dependências desnecessárias
- abstrações prematuras
- complexidade desnecessária

--- 

# Fluxo de desenvolvimento esperado

1. Entender o problema
2. Propor abordagem simples e segura
3. Identificar comportamento esperado e cenários de teste
4. Escrever ou atualizar testes antes da implementação para guiar a solução, sempre que aplicável
5. Implementar a menor mudança possível para satisfazer os testes
6. Refatorar preservando comportamento e clareza
7. Verificar necessidade de atualizar documentação (README, AGENTS.md, docstrings relevantes)
8. Garantir que lint, type-check e testes passam
9. Explicar impacto da mudança

---

# Ao concluir tarefas

- Informar quais arquivos foram alterados
- Verificar se a documentação precisa ser atualizada (README, AGENTS.md, comentários relevantes)
- Sugerir comandos para validação
- Sugerir próximos passos

---

# Arquivos importantes

- `src/api_bootstrapper_cli/cli.py` → entry point e sub-apps (env, hooks, db)
- `src/api_bootstrapper_cli/commands/` → comandos CLI (orquestração, evitar lógica de negócio)
- `src/api_bootstrapper_cli/core/` → lógica de negócio (managers e serviços)
- `src/api_bootstrapper_cli/core/protocols.py` → contratos entre componentes (criar ao abstrair comportamentos)
- `src/api_bootstrapper_cli/core/environment_service.py` → serviço de orquestração de bootstrap
- `src/api_bootstrapper_cli/core/shell.py` → execução de comandos do sistema (centralizar chamadas shell)
- `src/api_bootstrapper_cli/core/files.py` → manipulação de arquivos (operações de I/O)
- `pyproject.toml` → configuração do projeto Python
- `Makefile` → comandos de desenvolvimento

---

# Comandos úteis

```bash
source .venv/bin/activate   # Ativa ambiente virtual
make help                   # Mostra todos os comandos disponíveis
make test                   # Executa todos os testes com coverage
make test-unit              # Apenas testes unitários
make test-integration       # Apenas testes de integração
make test-e2e               # Apenas testes end-to-end
make lint                   # Verifica código com ruff
make format                 # Formata código com ruff
make type-check             # Verifica tipos com mypy
make check                  # Executa lint + type-check
make pre-commit             # Roda hooks de pre-commit
make clean                  # Remove cache e arquivos de build
```

## Workflow típico de desenvolvimento:

```bash
source .venv/bin/activate    # 1. Ativar ambiente

# ... implementar mudanças ...

make format                  # 2. Formatar e verificar tipos
make test                    # 3. Rodar testes
make check                   # 4. Validar código antes do commit
```
