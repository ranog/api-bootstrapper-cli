# Codex Workflows

Este documento descreve fluxos de trabalho recomendados para utilizar o Codex no VSCode neste projeto.

Todos os workflows assumem que o agente deve seguir as regras descritas no arquivo `AGENTS.md`.

Sempre que iniciar uma tarefa com Codex, peça explicitamente para ele:

- ler o `AGENTS.md`
- seguir as regras arquiteturais
- respeitar o fluxo de desenvolvimento definido

---

# Workflow 1 — Entender uma parte do sistema

Use quando estiver explorando código ou quando precisar entender um fluxo existente.

## Passos

1. Peça ao Codex para ler o `AGENTS.md`
2. Peça para explicar a arquitetura envolvida
3. Peça para descrever o fluxo de execução
4. Identifique os módulos relevantes antes de fazer mudanças

## Prompt sugerido

Leia o AGENTS.md e o contexto deste projeto.

Explique:

- arquitetura desta parte do sistema
- quais comandos CLI estão envolvidos
- quais managers e services participam
- onde ocorre IO (filesystem, shell, etc.)

Quero entender o fluxo completo antes de modificar o código.

---

# Workflow 2 — Implementar uma nova feature

Este é o fluxo recomendado para adicionar funcionalidades.

## Passos

1. Entender o problema
2. Planejar a abordagem
3. Identificar cenários de teste
4. Escrever testes (TDD)
5. Implementar a solução mínima
6. Refatorar
7. Validar

## Prompt sugerido

Leia o AGENTS.md e siga o fluxo de desenvolvimento esperado.

Objetivo:
[descreva a feature]

Primeiro proponha:

- abordagem arquitetural
- módulos a serem alterados
- necessidade de novos managers ou services
- cenários de teste

Depois escreva os testes seguindo TDD e padrão AAA (separação visual com linhas em branco, sem comentários explícitos).

Somente depois implemente a solução.

---

# Workflow 3 — Refatoração segura

Use quando precisar melhorar a estrutura do código.

## Passos

1. Entender a implementação atual
2. Identificar problemas
3. Propor plano de refatoração
4. Garantir que comportamento não muda
5. Atualizar testes se necessário

## Prompt sugerido

Leia o AGENTS.md.

Refatore este código mantendo comportamento e respeitando as regras arquiteturais do projeto.

Garanta que:

- CLI permanece fina
- managers mantêm responsabilidade única
- services coordenam fluxos
- IO continua isolado

Explique o plano antes de aplicar as mudanças.

---

# Workflow 4 — Criar testes para código existente

Use quando um módulo não possui testes.

## Passos

1. Analisar o comportamento do código
2. Identificar cenários importantes
3. Criar testes de comportamento
4. Cobrir erros e bordas

## Prompt sugerido

Leia o AGENTS.md.

Analise este módulo e proponha testes para:

- cenários felizes
- cenários de erro
- casos de borda

Implemente os testes usando pytest e padrão AAA (separação visual com linhas em branco, sem comentários explícitos).

Priorize testes de comportamento.

---

# Workflow 5 — Debug de problema

Use quando um bug é identificado.

## Passos

1. Reproduzir o problema
2. Analisar fluxo de execução
3. Identificar causa provável
4. Criar teste que reproduz o bug
5. Corrigir
6. Validar

## Prompt sugerido

Leia o AGENTS.md.

Analise este erro e identifique possíveis causas.

Depois:

1. proponha um teste que reproduza o bug
2. implemente o teste usando padrão AAA (separação visual com linhas em branco, sem comentários explícitos)
3. corrija o código
4. valide que os testes passam

Explique o raciocínio usado para encontrar a causa.

---

# Workflow 6 — Adicionar suporte a nova ferramenta

Esse projeto frequentemente integra novas ferramentas.

## Passos

1. Verificar protocolos existentes
2. Identificar necessidade de novo manager
3. Implementar manager
4. Atualizar service
5. Criar testes

## Prompt sugerido

Leia o AGENTS.md.

Quero adicionar suporte a uma nova ferramenta.

Analise:

- se um protocolo existente pode ser reutilizado
- se um novo manager deve ser criado
- como o service deve coordenar a nova ferramenta

Depois proponha a estrutura e os testes necessários.

---

# Workflow 7 — Revisão técnica de código

Use antes de abrir PR ou ao revisar código de outra pessoa.

## Passos

1. Verificar arquitetura
2. Analisar clareza do código
3. Verificar responsabilidades
4. Avaliar testes
5. Sugerir melhorias

## Prompt sugerido

Leia o AGENTS.md.

Revise esta implementação considerando:

- regras arquiteturais
- separação de responsabilidades
- clareza e simplicidade
- cobertura de testes

Sugira melhorias mantendo mudanças pequenas.

---

# Workflow 8 — Preparar Pull Request

Use ao finalizar uma feature.

## Passos

1. Revisar mudanças
2. Garantir que testes passam
3. Validar arquitetura
4. Preparar descrição de PR

## Prompt sugerido

Leia o AGENTS.md.

Revise as mudanças feitas neste branch e gere uma descrição para PR contendo:

- objetivo da mudança
- abordagem utilizada
- módulos alterados
- impacto arquitetural
- novos testes
- comandos de validação.

---

# Workflow universal

Este é um fluxo genérico que funciona para quase qualquer tarefa.

## Prompt universal

Leia o AGENTS.md e siga as regras arquiteturais e de desenvolvimento do projeto.

Antes de implementar:

1. explique rapidamente a abordagem
2. identifique cenários de teste
3. escreva testes usando padrão AAA (separação visual com linhas em branco, sem comentários explícitos)

Depois implemente a menor mudança possível para satisfazer os testes.

Ao final informe:

- arquivos alterados
- testes adicionados
- comandos de validação
- impacto arquitetural.

1. explique a abordagem
2. identifique cenários de teste
3. escreva testes seguindo TDD

Depois implemente a menor mudança possível para satisfazer os testes.

Ao final informe:

- arquivos alterados
- testes adicionados
- comandos para validação.
