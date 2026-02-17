# Contributing to API Bootstrapper CLI

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/joaopnogueira/api-bootstrapper-cli.git
   cd api-bootstrapper-cli
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Install pre-commit hooks**
   ```bash
   poetry run pre-commit install
   poetry run pre-commit install --hook-type commit-msg
   ```

4. **Configure git commit template (optional)**
   ```bash
   git config commit.template .gitmessage
   ```

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/) specification. All commit messages must follow this format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Examples

```bash
feat(cli): add support for custom Python versions
fix(poetry): resolve dependency conflict with typer
docs(readme): update installation instructions
test(core): add unit tests for pyenv manager
chore(deps): update dependencies
```

## Making Commits

### Option 1: Interactive Commitizen (Recommended)

Use the helper script for an interactive commit experience:

```bash
# Stage your changes
git add .

# Use the commit helper script
bash scripts/commit.sh

# Or use commitizen directly
poetry run cz commit
```

### Option 2: Manual Commits

If you prefer to write commit messages manually:

```bash
git add .
git commit -m "feat(core): add new functionality"
```

⚠️ **Note**: The pre-commit hook will validate your commit message format.

## Changelog & Versioning

The changelog is automatically generated from commit messages using commitizen.

### Bumping Version

To bump the version and update the changelog:

```bash
# Auto-detect version bump from commits (feat → minor, fix → patch)
bash scripts/bump.sh

# Or specify version increment manually
bash scripts/bump.sh patch  # 0.1.0 → 0.1.1
bash scripts/bump.sh minor  # 0.1.0 → 0.2.0
bash scripts/bump.sh major  # 0.1.0 → 1.0.0

# Using commitizen directly
poetry run cz bump --changelog
poetry run cz bump --changelog --increment PATCH
```

This will:
1. Analyze all commits since last tag
2. Determine the appropriate version bump
3. Update `pyproject.toml` and `__init__.py`
4. Generate/update `CHANGELOG.md`
5. Create a git tag
6. Commit all changes

## Testing

Run tests before committing:

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test types
poetry run pytest -m unit
poetry run pytest -m integration
poetry run pytest -m e2e
```

## Code Style

This project uses:
- **Ruff**: For linting and formatting (compatible with Black and isort)
- **Pre-commit hooks**: Automatically run on every commit

```bash
# Format code
poetry run ruff format .

# Lint code
poetry run ruff check . --fix

# Run pre-commit manually
poetry run pre-commit run --all-files
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following the commit convention

3. **Ensure all tests pass**
   ```bash
   poetry run pytest
   ```

4. **Update documentation** if needed

5. **Push your branch**
   ```bash
   git push origin feat/your-feature-name
   ```

6. **Create a Pull Request** with:
   - Clear description of changes
   - Link to related issues
   - Screenshots (if applicable)

## Project Structure

```
api-bootstrapper-cli/
├── src/api_bootstrapper_cli/    # Main package
│   ├── cli.py                   # CLI entry point
│   ├── commands/                # Command implementations
│   └── core/                    # Core functionality
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── e2e/                     # End-to-end tests
├── scripts/                     # Helper scripts
├── .pre-commit-config.yaml      # Pre-commit hooks
├── .gitmessage                  # Commit template
└── pyproject.toml               # Project configuration
```

## Versioning Strategy

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (`1.0.0 → 2.0.0`): Breaking changes
- **MINOR** (`0.1.0 → 0.2.0`): New features (backwards compatible)
- **PATCH** (`0.1.0 → 0.1.1`): Bug fixes (backwards compatible)

The version bump is automatically determined from commit types:
- `feat:` → MINOR version bump
- `fix:` → PATCH version bump
- `feat!:` or `fix!:` (breaking change) → MAJOR version bump

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues and pull requests
- Read the [README](README.md) for usage instructions

## Code of Conduct

- Be respectful and inclusive
- Follow the Python community guidelines
- Provide constructive feedback

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
