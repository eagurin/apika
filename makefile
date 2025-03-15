.PHONY: install venv test coverage format sort-imports lint type-check check docker-build docker-run docker-compose-run clean pre-commit-install pre-commit-run setup dev-setup full-check build-and-run deploy all

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

# Build Docker image
docker-build:
	docker build -t apiki .

# Run in Docker
docker-run:
	docker run --rm apiki $(ARGS)

# Run with Docker Compose
docker-compose-run:
	docker-compose up --build

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

# --- Grouped Commands for Sequential Tasks ---

# Initial setup: install dependencies and setup pre-commit
setup: install pre-commit-install
	@echo "✅ Setup completed."

# Complete development setup: dependencies, pre-commit, and virtual environment
dev-setup: clean install pre-commit-install venv
	@echo "✅ Development environment setup completed."

# Run full code quality check and tests with coverage
full-check: check coverage
	@echo "✅ All checks passed."

# Build and run the application in Docker
build-and-run: docker-build docker-run
	@echo "✅ Application built and running in Docker."

# Deploy: run checks, build and run in Docker
deploy: check test docker-build docker-compose-run
	@echo "✅ Application deployed with Docker Compose."

# Run all steps: setup, check, test, and deploy
all: setup check test coverage deploy
	@echo "✅ All tasks completed successfully."

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
	@echo ""
	@echo "Grouped commands for sequential tasks:"
	@echo "  setup                - Install dependencies and setup pre-commit"
	@echo "  dev-setup            - Complete development environment setup"
	@echo "  full-check           - Run all code quality checks and tests with coverage"
	@echo "  build-and-run        - Build and run the application in Docker"
	@echo "  deploy               - Run checks, tests, build and run with Docker Compose"
	@echo "  all                  - Run all steps: setup, check, test, and deploy"
	@echo "  help                 - Show this help message" 