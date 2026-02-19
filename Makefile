.PHONY: help install test test-cov test-unit test-integration test-e2e lint format type-check check pre-commit clean

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies with Poetry"
	@echo "  make test             - Run all tests"
	@echo "  make test-cov         - Run tests with coverage report"
	@echo "  make test-unit        - Run only unit tests"
	@echo "  make test-integration - Run only integration tests"
	@echo "  make test-e2e         - Run only e2e tests"
	@echo "  make lint             - Check code with ruff"
	@echo "  make format           - Format code with ruff"
	@echo "  make type-check       - Run mypy type checking"
	@echo "  make check            - Run lint + type-check"
	@echo "  make pre-commit       - Run pre-commit hooks on all files"
	@echo "  make clean            - Remove cache and build files"

install:
	poetry install

test:
	poetry run pytest -n auto

test-cov:
	poetry run pytest -n auto --cov=src/api_bootstrapper_cli --cov-report=term-missing --cov-report=html

test-unit:
	poetry run pytest -n auto tests/unit

test-integration:
	poetry run pytest -n auto tests/integration

test-e2e:
	poetry run pytest -n auto tests/e2e

lint:
	poetry run ruff check src tests

format:
	poetry run ruff format src tests
	poetry run ruff check --fix src tests

type-check:
	poetry run mypy src tests

check: lint type-check

pre-commit:
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage coverage.xml
