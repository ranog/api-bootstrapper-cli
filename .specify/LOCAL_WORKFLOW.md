# Fluxo local do Spec Kit no `dta-events`

Este guia descreve como iniciar e executar uma nova task usando o Spec Kit apenas
localmente. Os artefatos em `.specify/` e `specs/` estão ignorados pelo Git e não
devem ser enviados ao GitHub.

## Princípios do fluxo

- Não executar novamente `specify init` para cada task.
- Reutilizar a constituição em `.specify/memory/constitution.md`.
- Criar uma pasta independente em `specs/` para cada feature.
- Confirmar a feature ativa antes de executar os comandos seguintes.
- Revisar e aprovar os artefatos antes de alterar código da aplicação.
- Não usar `$speckit-taskstoissues`, pois o trabalho deve permanecer local.

## 1. Preparar a nova task

Criar um arquivo com nome específico, sem sobrescrever tasks anteriores:

```text
task-nome-da-feature.md
```

Se o arquivo também precisar permanecer exclusivamente local, verificar se ele está
ignorado pelo Git:

```bash
git check-ignore -v task-nome-da-feature.md
```

Caso não esteja ignorado, adicionar o caminho exato ao `.git/info/exclude` local.

## 2. Criar uma feature independente

Enviar ao Codex:

```text
$speckit-specify

A nova feature está descrita em @task-nome-da-feature.md.

Crie uma nova feature independente.
Não altere os artefatos de features anteriores.
Use a constituição atual do projeto.

Nesta etapa, descreva somente:
- comportamento esperado;
- usuários ou atores;
- regras de negócio;
- cenários de aceite;
- erros e casos-limite;
- critérios mensuráveis de sucesso.

Não defina ainda a implementação técnica.
```

O Spec Kit deve criar a próxima pasta sequencial:

```text
specs/
├── 001-feature-anterior/
└── 002-nome-da-feature/
    ├── spec.md
    └── checklists/
```

## 3. Confirmar a feature ativa

Antes de executar qualquer outro comando:

```bash
sed -n '1,40p' .specify/feature.json
```

O `feature_directory` deve apontar para a pasta da nova feature:

```json
{
  "feature_directory": "specs/002-nome-da-feature"
}
```

Se apontar para outra pasta, não executar `plan`, `tasks`, `analyze` ou `implement`
até corrigir a seleção da feature.

## 4. Clarificar requisitos

Executar:

```text
$speckit-clarify
```

Responder uma pergunta por vez. Sempre que houver ADR, contrato, runbook ou outro
documento autoritativo, fornecê-lo como fonte das respostas.

Concluir esta etapa antes do planejamento, salvo quando uma exploração consciente
justificar o risco de retrabalho.

## 5. Criar e revisar o plano

Executar:

```text
$speckit-plan
```

O planejamento pode gerar:

```text
specs/002-nome-da-feature/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
```

Revisar:

- escopo e arquivos afetados;
- decisões e alternativas em `research.md`;
- entidades e estados em `data-model.md`;
- contratos externos, quando aplicável;
- comandos e cenários de validação em `quickstart.md`;
- conformidade com a constituição;
- responsabilidades de outros times;
- riscos e limitações de validação.

Não avançar enquanto houver `NEEDS CLARIFICATION` ou violação injustificada da
constituição.

## 6. Gerar tarefas executáveis

Executar:

```text
$speckit-tasks
```

Revisar `tasks.md` e confirmar:

- ordem de execução;
- dependências;
- tarefas paralelizáveis;
- arquivos afetados;
- requisitos cobertos por cada tarefa;
- estratégia de testes e validação;
- ausência de trabalho fora do escopo.

## 7. Analisar consistência

Executar:

```text
$speckit-analyze
```

O comando é estritamente somente leitura. Ele não corrige os arquivos.

Depois do relatório, solicitar uma proposta de remediação:

```text
Com base no último relatório do $speckit-analyze:

1. Classifique os findings em obrigatórios, opcionais e descartáveis.
2. Priorize CRITICAL e HIGH.
3. Para cada correção obrigatória, informe:
   - finding afetado;
   - arquivo e seção;
   - menor alteração necessária;
   - impacto nos demais artefatos.
4. Preserve a constituição e o escopo original da feature.
5. Não altere código da aplicação.
6. Não edite os arquivos ainda; aguarde minha confirmação.
```

Após revisar a proposta, autorizar apenas os findings selecionados:

```text
Aprovado. Aplique somente as correções obrigatórias dos findings selecionados.

Atualize apenas spec.md, plan.md e tasks.md quando necessário.
Preserve a constituição, o escopo da feature e as responsabilidades externas.
Não implemente código da aplicação.

Depois das alterações:
- valide a consistência dos artefatos;
- revalide o checklist da especificação;
- informe os arquivos e seções alterados;
- execute novamente o $speckit-analyze em modo somente leitura.
```

Repetir análise e correção até que:

- não existam findings `CRITICAL`;
- não existam findings `HIGH` que afetem comportamento ou segurança;
- todos os requisitos obrigatórios tenham tarefas;
- não existam conflitos com a constituição;
- tarefas sem requisito estejam justificadas ou removidas.

Findings `LOW` puramente editoriais não precisam bloquear a implementação.

## 8. Fazer o último checkpoint

Antes de implementar:

```text
Revise o tasks.md final e apresente:

- ordem de execução;
- dependências entre tarefas;
- tarefas que podem ser paralelas;
- arquivos que serão alterados;
- validações previstas;
- responsabilidades externas.

Não implemente ainda.
```

## 9. Implementar uma feature de código com TDD

Após aprovar os artefatos:

```text
$speckit-implement

Execute uma tarefa por vez seguindo Red-Green-Refactor.

Para cada mudança de comportamento:

1. Identifique o comportamento esperado e o contrato afetado.
2. Escreva o menor teste AAA correspondente.
3. Execute o teste e apresente a evidência RED.
4. Aguarde minha confirmação antes de alterar código de produção.
5. Faça a menor implementação necessária para chegar ao GREEN.
6. Refatore somente se necessário, preservando comportamento.
7. Execute testes focados e integrações reais quando aplicável.
8. Avisar quando devemos commitar e fornecer frase de commit.

Não realize refatorações fora do escopo.
Não implemente tarefas pertencentes a outros times.
```

Para mudanças exclusivamente documentais, RED não é obrigatório, mas comandos,
links, exemplos, estrutura e consistência devem ser validados.

## 10. Verificar convergência

Após a implementação:

```text
$speckit-converge
```

Se novas tarefas obrigatórias forem adicionadas:

```text
$speckit-implement
$speckit-converge
```

Repetir até não restarem lacunas obrigatórias entre implementação, `spec.md`,
`plan.md` e `tasks.md`.

## 11. Encerrar localmente

Revisar e registrar:

- arquivos alterados;
- testes focados executados;
- testes de integração reais executados;
- lint e formatação;
- verificações que não rodaram, falharam ou ficaram bloqueadas;
- riscos residuais e dependências externas.

Como o fluxo é local, não é necessário criar issue, commit, push ou pull request.

## Referência rápida

```text
nova task
   ↓
task-nome-da-feature.md
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
corrigir artefatos e analisar novamente
   ↓
revisar tasks.md
   ↓
$speckit-implement
   ↓
$speckit-converge
```
