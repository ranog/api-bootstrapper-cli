# Guia genérico para adoção do GitHub Spec Kit

Este guia permite replicar o Spec Kit em projetos novos ou existentes. Ele foi
escrito para times que mantêm APIs, workers e serviços backend, mas o fluxo serve
para outros tipos de software.

Comandos verificados com `specify-cli 0.15.2` em 2026-08-05. Antes de aplicar em
outro projeto, execute `specify version` e confira se a versão instalada oferece as
mesmas opções.

## 1. Entender o que será instalado

O Spec Kit adiciona ao projeto:

- `.specify/`: configuração, templates, scripts, constituição e seleção da feature;
- `specs/`: especificações, planos, pesquisas, tarefas e guias de validação;
- arquivos da integração do agente, como `.agents/skills/speckit-*` para Codex;
- opcionalmente extensões e presets, somente quando solicitados.

O Spec Kit não exige GitHub nem cria branch automaticamente por padrão. A extensão
Git é opt-in. Criar issues também é uma etapa separada e opcional.

## 2. Tomar as decisões de adoção

Antes de inicializar, alinhar:

1. O uso será individual/local ou compartilhado pelo time?
2. Qual agente será utilizado: Codex, Copilot, Claude ou outro?
3. Qual versão do `specify-cli` será padronizada?
4. O Spec Kit ficará na raiz do repositório ou em um serviço específico?
5. Quais documentos são fontes autoritativas: ADRs, contratos, `AGENTS.md`, README,
   padrões de teste e runbooks?

### Projeto único

Inicializar na raiz do projeto.

### Monorepo

Quando os módulos são implantados e mantidos de forma independente, preferir uma
instalação por serviço. Uma configuração única na raiz só é adequada quando as
features, decisões e validações realmente atravessam o monorepo como uma unidade.

## 3. Escolher o modo de persistência

### Opção A — Uso local

Use para piloto individual ou quando os artefatos ainda não devem fazer parte do
repositório compartilhado.

Antes da inicialização, adicionar ao `.git/info/exclude` do repositório:

```gitignore
# Spec Kit local
/.specify/
/specs/
/.agents/skills/speckit-*/
```

O último padrão é específico do Codex. Para outros agentes, usar somente o diretório
gerado pela integração, por exemplo:

```gitignore
# GitHub Copilot em modo skills
/.github/skills/speckit-*/

# Claude Code
/.claude/skills/speckit-*/
```

Não excluir `.github/`, `.agents/` ou `.claude/` inteiros, pois esses diretórios
podem conter arquivos legítimos do projeto.

Arquivos de task também podem permanecer locais. Nesse caso, adicionar cada caminho
exato ao `.git/info/exclude`, evitando padrões amplos como `task-*.md` quando o
repositório já versiona documentos semelhantes.

### Opção B — Uso compartilhado pelo time

Não adicionar os artefatos ao `.git/info/exclude`. Inicializar em uma branch própria,
revisar todos os arquivos gerados e entregar a adoção em uma mudança separada do
código de produto.

O time deve decidir se também versionará os arquivos específicos de cada agente.
Quando pessoas usam agentes diferentes, instalar somente integrações declaradas como
compatíveis com multi-install ou manter um padrão oficial para o repositório.

## 4. Instalar o Specify CLI

Pré-requisitos:

- Python 3.11 ou superior;
- `uv` ou `pipx`;
- agente de codificação compatível;
- Git somente se o projeto ou a extensão Git precisarem dele.

### Instalação simples pelo PyPI

```bash
uv tool install specify-cli
```

### Instalação fixada em uma release oficial

Recomendada quando o time precisa reproduzir a mesma versão:

```bash
uv tool install specify-cli \
  --from git+https://github.com/github/spec-kit.git@vX.Y.Z
```

Substituir `vX.Y.Z` pela versão aprovada, mantendo o prefixo `v`.

### Verificação

```bash
specify version
specify check
specify integration list
```

`specify check` verifica as ferramentas locais. `specify self check` consulta se há
uma versão mais nova do CLI, mas não modifica a instalação.

## 5. Preparar um projeto existente

Antes de inicializar:

```bash
git status --short --branch
```

Preservar ou concluir alterações existentes. Não executar `--force` sobre um working
tree cujo conteúdo ainda não foi compreendido.

Mapear ao menos:

- instruções do repositório;
- arquitetura e responsabilidades existentes;
- contratos públicos;
- comandos de teste, lint e formatação;
- integrações externas;
- regras de segurança, tenancy e observabilidade;
- ADRs e runbooks relevantes.

O Spec Kit não substitui esse contexto. Ele o transforma em restrições persistentes
para specification, plan, tasks e implementação.

## 6. Inicializar o projeto

### Projeto existente com Codex

Executar na raiz:

```bash
specify init \
  --here \
  --integration codex \
  --integration-options="--skills" \
  --script sh
```

Em diretório não vazio, o CLI solicitará confirmação para mesclar a infraestrutura
do Spec Kit. Ler o aviso e revisar o estado do repositório antes de responder.

### Projeto novo com Codex

```bash
specify init meu-projeto \
  --integration codex \
  --integration-options="--skills" \
  --script sh

cd meu-projeto
```

### Outros agentes

```bash
specify init --here --integration copilot --script sh
specify init --here --integration claude --script sh
specify init --here --integration gemini --script sh
```

Consultar as chaves disponíveis na versão instalada:

```bash
specify integration list
```

No Windows, usar `--script ps`. Para scripts Python multiplataforma, usar
`--script py`.

### Quando usar `--force`

```bash
specify init --here --force --integration codex
```

Usar somente como recuperação ou merge intencional em diretório não vazio, depois de
preservar o estado atual. Para atualizações rotineiras, preferir
`specify integration upgrade`.

## 7. Validar a inicialização

```bash
specify integration status
git status --short
```

Para uma instalação local com Codex:

```bash
git check-ignore -v .specify/memory/constitution.md
git check-ignore -v .agents/skills/speckit-constitution/SKILL.md
```

Confirmar que:

- `.specify/memory/constitution.md` existe;
- os templates e scripts foram instalados;
- as skills ou comandos do agente existem;
- `specify integration status` não informa arquivos ausentes ou inválidos;
- arquivos locais não aparecem em `git status`;
- arquivos compartilhados aparecem no diff esperado.

Reiniciar completamente o agente, IDE ou terminal se os comandos não forem
reconhecidos.

## 8. Criar a constituição do projeto

A constituição registra regras não negociáveis. Em projeto existente, ela deve
descrever a realidade atual e as decisões aprovadas, não uma arquitetura idealizada.

Com Codex:

```text
$speckit-constitution

Analise AGENTS.md, README, arquivos de dependências, código, testes, ADRs,
contratos e runbooks existentes.

Crie uma constituição curta, declarativa e verificável, cobrindo:
- limites arquiteturais;
- estabilidade de contratos;
- segurança e isolamento de dados;
- estratégia de testes;
- integrações que exigem validação real;
- qualidade, lint e formatação;
- tratamento de erros;
- documentação obrigatória;
- critérios para exceções.

Não altere código da aplicação.
Não invente capacidades ausentes.
Prefira referenciar documentos autoritativos a duplicar regras extensas.
```

Revisar `.specify/memory/constitution.md` antes de iniciar uma feature.

## 9. Criar uma feature

Usar uma pasta independente para cada task. Manter a descrição original em um
arquivo identificável, por exemplo:

```text
task-ABC-123-nome-da-feature.md
```

Executar:

```text
$speckit-specify

A feature está descrita em @task-ABC-123-nome-da-feature.md.

Crie uma nova feature independente e use a constituição atual.
Não altere artefatos de features anteriores.

Nesta etapa, descreva somente:
- problema e resultado esperado;
- atores;
- comportamentos observáveis;
- regras de negócio;
- cenários de aceite e erros;
- limites de escopo;
- critérios mensuráveis de sucesso.

Não escolha a solução técnica ainda.
```

## 10. Confirmar a feature ativa

```bash
sed -n '1,40p' .specify/feature.json
```

Exemplo:

```json
{
  "feature_directory": "specs/001-nome-da-feature"
}
```

Não executar os próximos comandos se o arquivo apontar para outra feature. A seleção
do projeto e a seleção da feature são independentes.

## 11. Clarificar requisitos

```text
$speckit-clarify
```

Práticas recomendadas:

- responder uma pergunta por vez;
- fornecer ADRs, contratos ou decisões do produto como fonte;
- distinguir decisão confirmada de hipótese;
- manter decisões de implementação para o planejamento;
- concluir as ambiguidades de alto impacto antes do `$speckit-plan`.

## 12. Criar e revisar o plano

```text
$speckit-plan
```

O planejamento normalmente produz:

```text
specs/001-nome-da-feature/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
```

`contracts/` pode ser omitido quando a feature não expõe nem modifica interfaces.

Revisar:

- contexto técnico e arquivos afetados;
- aderência à constituição;
- decisões, justificativas e alternativas;
- entidades e transições de estado;
- contratos externos;
- riscos operacionais;
- estratégia de teste e validação;
- responsabilidades e dependências externas.

Não avançar com `NEEDS CLARIFICATION` ou violações injustificadas da constituição.

## 13. Gerar as tarefas

```text
$speckit-tasks
```

Revisar `tasks.md` e confirmar:

- dependências e ordem de execução;
- tarefas que podem ser paralelas;
- caminho exato dos arquivos;
- requisito ou história coberta por cada tarefa;
- testes antes das mudanças de comportamento;
- validação proporcional ao risco;
- ausência de trabalho fora do escopo.

## 14. Analisar consistência

```text
$speckit-analyze
```

O analyze é somente leitura. Ele compara constituição, `spec.md`, `plan.md` e
`tasks.md`, mas não aplica correções.

Depois do relatório:

```text
Com base no último relatório do $speckit-analyze:

1. Classifique os findings em obrigatórios, opcionais e descartáveis.
2. Priorize CRITICAL e HIGH.
3. Para cada correção obrigatória, informe o finding, arquivo, seção,
   menor alteração e impacto nos demais artefatos.
4. Preserve a constituição e o escopo original.
5. Não altere código da aplicação.
6. Não edite ainda; aguarde minha confirmação.
```

Após aprovar findings específicos:

```text
Aplique somente as correções aprovadas nos artefatos da feature.

Preserve a constituição e o escopo.
Não implemente código da aplicação.
Revalide o checklist da especificação.
Informe os arquivos e seções alterados.
Depois, execute novamente o $speckit-analyze em modo somente leitura.
```

Antes de implementar, resolver:

- todos os findings `CRITICAL`;
- findings `HIGH` que afetem comportamento, segurança ou cobertura;
- requisitos obrigatórios sem tarefa;
- conflitos com a constituição;
- tarefas sem requisito e sem justificativa.

## 15. Fazer o checkpoint antes da implementação

```text
Revise o tasks.md final e apresente:

- ordem de execução;
- dependências;
- paralelismo possível;
- arquivos que serão alterados;
- testes e validações previstos;
- riscos;
- responsabilidades externas.

Não implemente ainda.
```

Revisar e autorizar explicitamente o início da implementação.

## 16. Implementar

Para uma feature de código:

```text
$speckit-implement

Execute uma tarefa por vez seguindo Red-Green-Refactor.

Para cada mudança de comportamento:
1. Identifique o comportamento e o contrato afetado.
2. Escreva o menor teste AAA correspondente.
3. Execute o teste e apresente a evidência RED.
4. Aguarde confirmação antes de alterar código de produção.
5. Faça a menor implementação necessária para chegar ao GREEN.
6. Refatore somente se necessário e preserve o comportamento.
7. Execute testes focados e integrações reais quando aplicável.

Não faça refatorações fora do escopo.
Não implemente responsabilidades de outros times.
```

Para documentação, configuração ou infraestrutura, adaptar os gates sem inventar
RED artificial. Ainda assim, validar comandos, estrutura, contratos, exemplos,
segurança, lint, formatação e integrações relevantes.

## 17. Verificar convergência

```text
$speckit-converge
```

O converge compara a implementação com spec, plano e tarefas. Se adicionar novas
tarefas obrigatórias:

```text
$speckit-implement
$speckit-converge
```

Repetir até não restarem lacunas obrigatórias.

## 18. Encerrar a feature

Registrar:

- arquivos alterados;
- comportamento entregue;
- testes focados;
- integrações reais executadas;
- lint, formatação e verificações estruturais;
- testes não executados, travados ou limitados por infraestrutura;
- dependências externas abertas;
- riscos residuais.

No modo local, encerrar sem issue, commit, push ou PR. No modo compartilhado, usar o
processo normal do time somente após revisão dos artefatos e da implementação.

## 19. Iniciar a próxima feature

Não executar novamente `specify init`.

Criar um novo arquivo de task e repetir a partir de `$speckit-specify`. O comando
criará uma nova pasta sequencial em `specs/` e atualizará `.specify/feature.json`.

## 20. Atualizar o Spec Kit

O CLI e os arquivos instalados no projeto possuem ciclos separados.

### Verificar e atualizar o CLI

```bash
specify self check
specify self upgrade --dry-run
specify self upgrade
```

Para usar uma versão aprovada:

```bash
specify self upgrade --tag vX.Y.Z
```

### Atualizar os arquivos do projeto

Dentro de cada projeto:

```bash
specify integration status
specify integration upgrade codex
specify extension update
```

Substituir `codex` pela integração instalada. Em projetos com várias integrações,
atualizar cada uma separadamente.

`specify integration upgrade` preserva specs, planos, tasks, constituição, código e
histórico Git. Ele bloqueia quando encontra arquivos gerenciados modificados; revisar
antes de considerar `--force`.

Usar `specify init --here --force` apenas como recuperação quando os manifests ou
metadados de integração estiverem ausentes ou corrompidos.

## 21. Diagnóstico rápido

### Comandos do agente não aparecem

```bash
specify integration status
specify check
```

Confirmar que os arquivos da integração existem e reiniciar completamente o agente
ou IDE.

### Feature errada está ativa

```bash
sed -n '1,40p' .specify/feature.json
```

Corrigir a seleção antes de executar comandos que escrevem artefatos. Para automação,
`SPECIFY_FEATURE_DIRECTORY` pode selecionar explicitamente a pasta da feature.

### `speckit-analyze` encontrou problemas

O comando não corrige arquivos. Classificar findings, propor alterações, obter
aprovação, editar os artefatos e executar o analyze novamente.

### Diretório existente exibe aviso de merge

É esperado em projeto brownfield. Cancelar se o estado não estiver seguro. Não usar
`--force` apenas para eliminar o aviso.

### Catálogo remoto indisponível

Os templates usados pelo `specify init` vêm do pacote instalado e a inicialização
normal não depende da rede. Consultas a catálogos e atualização do CLI podem exigir
acesso externo.

## Checklist de adoção por repositório

- [ ] Modo local ou compartilhado decidido.
- [ ] Integração e versão do CLI definidas.
- [ ] Working tree conhecido e preservado.
- [ ] Repositório ou serviço correto selecionado.
- [ ] `specify init` executado uma única vez.
- [ ] `specify integration status` sem erros.
- [ ] Regras de exclusão local validadas, quando aplicável.
- [ ] Agente reconhece os comandos ou skills.
- [ ] Constituição revisada pelo responsável técnico.
- [ ] Primeira feature possui pasta independente.
- [ ] Feature ativa confirmada em `.specify/feature.json`.
- [ ] Analyze reexecutado após remediações.
- [ ] Implementação segue os gates do projeto.
- [ ] Converge não possui lacunas obrigatórias.
- [ ] Limites de validação e dependências externas foram registrados.

## Fluxo resumido

```text
instalar CLI
   ↓
decidir local ou compartilhado
   ↓
specify init (uma vez por projeto)
   ↓
$speckit-constitution
   ↓
nova task
   ↓
$speckit-specify
   ↓
$speckit-clarify
   ↓
$speckit-plan
   ↓
$speckit-tasks
   ↓
$speckit-analyze
   ↓
remediar e analisar novamente
   ↓
checkpoint humano
   ↓
$speckit-implement
   ↓
$speckit-converge
```

## Referências oficiais

- [Installation Guide](https://github.github.com/spec-kit/installation.html)
- [Core Commands](https://github.github.com/spec-kit/reference/core.html)
- [Integrations](https://github.github.com/spec-kit/reference/integrations.html)
- [Quick Start](https://github.github.com/spec-kit/quickstart.html)
- [Upgrade Guide](https://github.github.com/spec-kit/upgrade.html)
