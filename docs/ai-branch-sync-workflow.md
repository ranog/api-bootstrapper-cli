# AI Branch Sync Workflow

Este documento define como agentes de IA devem sincronizar
a branch atual antes de criar commits.

---

# 1. Identificar branch atual

Executar:

```bash
git branch --show-current
```

---

# 2. Verificar árvore de trabalho limpa

Executar:

```bash
git status --porcelain
```

Se houver mudanças não commitadas:

1. não iniciar sync automaticamente
2. pedir confirmação ao usuário sobre como proceder
3. somente continuar após decisão explícita

---

# 3. Descobrir branch padrão remota

Executar:

```bash
git symbolic-ref --short refs/remotes/origin/HEAD
```

Esperado:

```text
origin/main
```

Extrair o nome da branch padrão remota (exemplo: `main`).

---

# 4. Sincronizar com o repositório remoto

Executar:

```bash
git fetch origin --prune
```

---

# 5. Atualizar branch atual

Se a branch atual for `<default_branch>`:

Executar:

```bash
git pull --ff-only origin <default_branch>
```

Se a branch atual NÃO for `<default_branch>`:

Executar:

```bash
git rebase origin/<default_branch>
```

---

# 6. Conflitos

Se ocorrer conflito:

1. listar arquivos em conflito
2. sugerir resolução
3. pedir confirmação antes de executar `git rebase --continue` ou `git rebase --abort`

Nunca finalizar automaticamente um rebase com conflitos.
