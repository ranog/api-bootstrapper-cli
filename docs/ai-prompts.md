# Prompts úteis para usar com Codex no VSCode

Este documento contém prompts prontos para usar com o Codex em projetos que utilizam o arquivo `AGENTS.md`.

A ideia é sempre começar pedindo para o agente **ler o AGENTS.md** e seguir as regras arquiteturais do projeto.

---

# 1. Entender a arquitetura do projeto

Use quando estiver explorando o projeto ou quando o agente parecer sem contexto.

Prompt:

Leia o AGENTS.md e o contexto deste projeto.

Explique como a arquitetura está organizada, incluindo:

- papel do `cli.py`
- responsabilidade dos `commands`
- papel dos `managers`
- papel dos `services`
- papel dos `protocols`

Mostre também o fluxo de execução do comando `bootstrap-env` desde o CLI até os managers envolvidos.

---

# 2. Planejar uma implementação antes de codar

Evita código errado e ajuda o agente a pensar na arquitetura primeiro.

Prompt:

Leia o AGENTS.md e siga as regras arquiteturais do projeto.

Objetivo:
[descreva a feature]

Antes de implementar, proponha:

1. abordagem arquitetural
2. quais módulos serão alterados
3. se novos managers ou services são necessários
4. cenários de teste

Somente depois de validar o plano implemente a solução.

---

# 3. Implementar feature seguindo TDD

Esse prompt segue exatamente o fluxo descrito no AGENTS.md.

Prompt:

Leia o AGENTS.md e siga o fluxo de desenvolvimento esperado.

Objetivo:
[descreva a feature]

Passos:

1. identificar comportamento esperado
2. propor cenários de teste
3. escrever testes seguindo TDD e padrão AAA (separação visual com linhas em branco, sem comentários explícitos)
4. implementar a menor mudança possível para fazer os testes passarem
5. refatorar mantendo clareza

Ao final informe:

- arquivos alterados
- novos testes
- comandos para validação.

---

# 4. Criar testes para código existente

Útil quando um módulo não possui testes.

Prompt:

Leia o AGENTS.md e siga as diretrizes de testes do projeto.

Analise este módulo e proponha uma estratégia de testes.

Inclua:

1. cenários de comportamento
2. casos de erro
3. casos de borda

Depois escreva testes em pytest usando padrão AAA (separação visual com linhas em branco, sem comentários explícitos).

Evite acoplamento a detalhes internos.

---

# 5. Refatoração segura

Para melhorar código mantendo comportamento.

Prompt:

Leia o AGENTS.md.

Refatore este código preservando comportamento e respeitando as regras arquiteturais do projeto.

Garanta que:

- CLI continua fina
- managers mantêm responsabilidade única
- services coordenam fluxos
- IO permanece isolado

Explique primeiro o plano de refatoração antes de aplicar mudanças.

---

# 6. Revisão técnica de código

Ideal para revisar PRs ou mudanças grandes.

Prompt:

Leia o AGENTS.md e revise esta implementação.

Analise:

- respeito às regras arquiteturais
- separação de responsabilidades
- clareza do código
- possíveis bugs
- qualidade dos testes

Sugira melhorias mantendo mudanças pequenas e seguras.

---

# 7. Adicionar suporte a nova ferramenta

Muito comum para este projeto.

Prompt:

Leia o AGENTS.md.

Quero adicionar suporte a uma nova ferramenta.

Antes de implementar:

1. identifique se um novo manager é necessário
2. verifique se algum protocolo existente pode ser reutilizado
3. proponha estrutura de implementação
4. liste cenários de teste

Depois implemente seguindo TDD.

---

# 8. Analisar fluxo de um comando CLI

Muito útil para debugging.

Prompt:

Leia o AGENTS.md.

Explique o fluxo completo deste comando CLI:

- entry point
- command handler
- services envolvidos
- managers chamados
- operações de IO

Quero entender claramente cada camada da execução.

---

# 9. Melhorar cobertura de testes

Prompt:

Leia o AGENTS.md.

Analise os testes existentes e identifique lacunas de cobertura.

Sugira novos testes para:

- cenários de erro
- casos de borda
- comportamentos críticos

Implemente os testes seguindo padrão AAA (separação visual com linhas em branco, sem comentários explícitos).

---

# 10. Preparar um Pull Request

Muito útil ao finalizar uma task.

Prompt:

Leia o AGENTS.md.

Revise as mudanças feitas neste branch e prepare um resumo para PR.

Inclua:

- objetivo da mudança
- abordagem utilizada
- módulos alterados
- impacto na arquitetura
- novos testes adicionados
- comandos para validação local.

---

# Prompt universal

Este é um prompt genérico que funciona bem para quase qualquer tarefa.

Prompt:

Leia o AGENTS.md e siga as regras arquiteturais e de desenvolvimento do projeto.

Antes de codar:

1. explique rapidamente a abordagem
2. identifique cenários de teste
3. escreva testes (TDD) usando padrão AAA (separação visual com linhas em branco, sem comentários explícitos)

Depois implemente a menor mudança possível para satisfazer os testes.

Ao final informe:

- arquivos alterados
- testes adicionados
- comandos de validação.
