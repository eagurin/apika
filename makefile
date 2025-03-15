.PHONY: install venv test coverage format sort-imports lint type-check check docker-build docker-run docker-compose-run clean pre-commit-install pre-commit-run

# Install dependencies
install:
	poetry install

# Create and activate virtual environment
venv:
	poetry shell

# Run tests
test:
	poetry run pytest

# Run tests with coverage
coverage:
	poetry run pytest --cov=apiki --cov-report=term --cov-report=html

# Format code with black
format:
	poetry run black apiki

# Sort imports with isort
sort-imports:
	poetry run isort apiki

# Run linting with flake8
lint:
	poetry run flake8 apiki

# Type check with mypy
type-check:
	poetry run mypy apiki

# Run all code quality checks
check: format sort-imports lint type-check

# Clean up build artifacts and cache
clean:
	rm -rf dist build *.egg-info .coverage htmlcov .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

# Install pre-commit hooks
pre-commit-install:
	poetry run pre-commit install

# Run pre-commit hooks on all files
pre-commit-run:
	poetry run pre-commit run --all-files

# Help
help:
	@echo "Available targets:"
	@echo "  install              - Install dependencies"
	@echo "  venv                 - Create and activate virtual environment"
	@echo "  test                 - Run tests"
	@echo "  coverage             - Run tests with coverage"
	@echo "  format               - Format code with black"
	@echo "  sort-imports         - Sort imports with isort"
	@echo "  lint                 - Run linting with flake8"
	@echo "  type-check           - Type check with mypy"
	@echo "  check                - Run all code quality checks"
	@echo "  docker-build         - Build Docker image"
	@echo "  docker-run ARGS=args - Run in Docker"
	@echo "  docker-compose-run   - Run with Docker Compose"
	@echo "  clean                - Clean up build artifacts and cache"
	@echo "  pre-commit-install   - Install pre-commit hooks"
	@echo "  pre-commit-run       - Run pre-commit hooks on all files"
	@echo "  help                 - Show this help message" 