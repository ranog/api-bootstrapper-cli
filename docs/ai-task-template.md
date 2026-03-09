# Codex Task Template

Este documento define um template padrão para solicitar tarefas ao Codex neste projeto.

O objetivo é garantir que todas as mudanças:

- respeitem o `AGENTS.md`
- sigam TDD
- mantenham a arquitetura do projeto
- sejam pequenas e seguras

Sempre que iniciar uma tarefa, copie este template e preencha as seções.

---

# Template de tarefa

## Contexto

Leia o `AGENTS.md` e siga todas as regras arquiteturais e de desenvolvimento definidas no projeto.

---

## Objetivo da tarefa

Descreva claramente o que precisa ser feito.

Exemplo:

Adicionar suporte ao gerenciador de dependências `X` no bootstrap do projeto.

---

## Problema ou motivação

Explique por que essa mudança é necessária.

Exemplo:

Usuários do projeto precisam poder escolher entre diferentes gerenciadores de dependência.

---

## Requisitos

Liste o comportamento esperado.

Exemplo:

- permitir selecionar o novo gerenciador
- integrar com o fluxo de bootstrap existente
- manter compatibilidade com managers atuais

---

## Restrições arquiteturais

Siga as regras do `AGENTS.md`, especialmente:

- CLI deve permanecer fina
- managers devem ter responsabilidade única
- services coordenam fluxos complexos
- IO deve permanecer isolado
- evitar abstrações desnecessárias

---

## Plano esperado

Antes de implementar:

1. explique a abordagem
2. identifique os módulos que serão alterados
3. determine se novos managers ou services são necessários
4. identifique cenários de teste

---

## Estratégia de testes

Siga TDD.

1. identificar cenários de teste
2. escrever testes primeiro
3. usar padrão AAA (separação visual com linhas em branco, sem comentários explícitos)

Cobrir:

- cenário feliz
- cenários de erro
- casos de borda relevantes

---

## Implementação

Após definir os testes:

- implementar a menor mudança possível
- manter clareza e simplicidade
- respeitar responsabilidades arquiteturais

Evitar:

- duplicação de lógica
- novas abstrações desnecessárias
- lógica de negócio dentro da CLI

---

## Validação

Após implementar:

- garantir que todos os testes passam
- garantir que lint e type-check passam

Executar:

make format  
make test  
make check  

---

## Resultado esperado

Ao concluir a tarefa, informe:

- arquivos alterados
- novos testes criados
- impacto na arquitetura
- comandos para validar localmente
