# AI Commit Prompt

Este documento define como gerar mensagens de commit
usando agentes de IA.

---

# Processo

Antes de gerar a mensagem:

1. identificar branch atual
2. verificar código de task no nome da branch
3. analisar mudanças no diff
4. escolher tipo de commit com base na mudança real

---

# Identificar branch

Executar:

```bash
git branch --show-current
```

---

# Detectar código de task

Procurar padrão:

```text
[A-Z]+-[0-9]+
```

Exemplo:

```text
AIPL-1293
```

---

# Analisar mudanças

Executar:

```bash
git diff --staged --name-only
git diff --staged
```

Se não houver nada staged, avaliar o diff não staged:

```bash
git diff --name-only
git diff
```

---

# Escolher tipo do commit

Usar o tipo conforme o impacto dominante:

- `feat`: nova funcionalidade
- `fix`: correção de bug
- `refactor`: refatoração sem mudança de comportamento
- `docs`: apenas documentação
- `test`: apenas testes
- `chore`: manutenção interna sem impacto funcional
- `perf`: melhoria de performance
- `build`: mudanças de build/dependências
- `ci`: mudanças de pipeline/CI

Não forçar `feat` quando o diff indicar outro tipo.

---

# Formato da mensagem

Se houver task:

```text
<type>(AIPL-1293): short message in English
```

Se não houver task:

```text
<type>(cli): short message in English
```

---

# Escopo do commit

Cada commit deve ser atômico e representar um único contexto lógico.

Regras:

- não misturar feature, refactor, docs e testes sem relação no mesmo commit
- agrupar apenas arquivos diretamente relacionados ao mesmo objetivo
- quando houver contextos diferentes, gerar commits separados
- se houver dúvida sobre o agrupamento, pedir confirmação ao usuário antes de commitar

---

# Regras da mensagem

- usar Conventional Commits
- descrição curta
- inglês
- modo imperativo
- não ser verboso
- não inventar mudanças
