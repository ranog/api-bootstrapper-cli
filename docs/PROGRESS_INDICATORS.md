# Progress Indicators

Este documento descreve os indicadores de progresso visuais implementados no CLI.

## 📊 Indicadores Implementados

O CLI usa **Rich** para fornecer feedback visual durante operações longas:

### 1. Instalação de Python via pyenv

```bash
api-bootstrapper bootstrap-env --python 3.12.12
```

**Output:**
```
[cyan]⠋ Installing Python 3.12.12 via pyenv...[/cyan]
```

**Quando:**
- `pyenv install` precisa baixar e compilar Python (pode levar minutos)

### 2. Instalação de Ferramentas Python (pip, poetry, etc)

```bash
# Durante: pip install --upgrade pip setuptools wheel poetry
```

**Output:**
```
[cyan]⠋ Installing pip, setuptools, wheel, poetry...[/cyan]
```

**Quando:**
- Instalação de pacotes base no Python do projeto

### 3. Instalação de Dependências com Poetry

```bash
# Durante: poetry install --no-root
```

**Output:**
```
[cyan]⠋ Installing dependencies with Poetry...[/cyan]
```

**Quando:**
- Poetry está instalando dependências do `pyproject.toml`

## 🎨 Tipos de Spinners

Todos os spinners usam `spinner="dots"` do Rich:

```
⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏
```

## 📝 Exemplo Completo de Output

```bash
$ api-bootstrapper bootstrap-env --python 3.12.12
[cyan]Setting up Python 3.12.12[/cyan]
[cyan]⠋ Installing Python 3.12.12 via pyenv...[/cyan]
[cyan]Configuring pyenv local version[/cyan]
[green]Python configured: /home/user/.pyenv/versions/3.12.12/bin/python[/green]

[cyan]Installing Python tooling[/cyan]
[cyan]⠋ Installing pip, setuptools, wheel, poetry...[/cyan]
[green]Python tooling installed[/green]

[cyan]Configuring Poetry environment[/cyan]
[cyan]Linking Poetry to Python version[/cyan]

[cyan]Installing project dependencies[/cyan]
[cyan]⠋ Installing dependencies with Poetry...[/cyan]
[green]Virtual environment ready: /path/to/project/.venv[/green]

[cyan]Writing VSCode configuration[/cyan]
[green]VSCode configured: /path/to/project/.vscode/settings.json[/green]

[bold green]✓[/bold green] [green]Environment ready![/green]
```

## 🛠️ Implementação Técnica

### Localização do Código

- **pyenv_manager.py**: `ensure_python()` e `install_pip_packages()`
- **poetry_manager.py**: `install_dependencies()`
- **environment_service.py**: Melhorias nas mensagens

### Exemplo de Uso

```python
from rich.console import Console

console = Console()

with console.status(
    f"[cyan]Installing Python {version} via pyenv...[/cyan]",
    spinner="dots",
):
    # Operação longa aqui
    exec_cmd(["pyenv", "install", "-s", version])
```

### Por que `console.status()`?

- ✅ Spinner animado automático
- ✅ Não interfere com output de subprocessos
- ✅ Limpa automaticamente ao terminar
- ✅ Funciona bem em CI/CD (desabilita animação em env não-interativos)

## 🚀 Benefícios para o Usuário

1. **Feedback Visual**: Usuário sabe que o CLI está trabalhando
2. **Contexto Claro**: Mensagem descreve exatamente o que está acontecendo
3. **Profissional**: Visual moderno e polido
4. **Não Intrusivo**: Não polui o terminal com output excessivo

## 📊 Comparação: Antes e Depois

### Antes

```
pyenv ensure python 3.12.12
... (sem feedback por minutos) ...
python /home/user/.pyenv/versions/3.12.12/bin/python
```

### Depois

```
Setting up Python 3.12.12
⠋ Installing Python 3.12.12 via pyenv...
Configuring pyenv local version
✓ Python configured: /home/user/.pyenv/versions/3.12.12/bin/python
```

## 🎯 Próximos Melhoramentos

Possíveis melhorias futuras:

- [ ] Barra de progresso real durante downloads grandes
- [ ] Mostrar velocidade de download para `pyenv install`
- [ ] Timer para operações longas (ex: "Installing... 2m 30s")
- [ ] Integração com `rich.progress.Progress` para múltiplas tasks paralelas
