.PHONY: install venv test coverage format sort-imports lint type-check check docker-build docker-run docker-compose-run clean pre-commit-install pre-commit-run help dev-setup code-quality full-test ci-pipeline release deploy all

install:
	poetry install

venv:
	poetry shell

test:
	poetry run pytest

coverage:
	poetry run pytest --cov=apiki --cov-report=term --cov-report=html

format:
	poetry run black apiki

sort-imports:
	poetry run isort apiki

lint:
	poetry run flake8 apiki

type-check:
	poetry run mypy apiki

check: format sort-imports lint type-check

clean:
	rm -rf dist build *.egg-info .coverage htmlcov .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

pre-commit-install:
	poetry run pre-commit install

pre-commit-run:
	poetry run pre-commit run --all-files

dev-setup: install pre-commit-install venv
	@echo "Development environment set up successfully!"

code-quality: format sort-imports lint type-check
	@echo "Code quality checks completed!"

full-test: clean code-quality test coverage
	@echo "All tests completed with coverage!"

ci-pipeline: install code-quality test coverage
	@echo "CI pipeline completed successfully!"

docker-build:
	docker build -t apiki .

docker-run:
	docker run --rm apiki $(ARGS)

docker-compose-run:
	docker-compose up --build

deploy: docker-build docker-compose-run
	@echo "Application deployed successfully!"

release: clean code-quality test docker-build
	@echo "Release preparation completed!"

all: dev-setup code-quality full-test release
	@echo "All tasks completed successfully!"

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
	@echo "  clean                - Clean up build artifacts and cache"
	@echo "  pre-commit-install   - Install pre-commit hooks"
	@echo "  pre-commit-run       - Run pre-commit hooks on all files"
	@echo "  dev-setup            - Set up development environment"
	@echo "  code-quality         - Run all code quality checks (alias for check)"
	@echo "  full-test            - Run clean, code quality checks, tests with coverage"
	@echo "  ci-pipeline          - Run full CI pipeline"
	@echo "  docker-build         - Build Docker image"
	@echo "  docker-run ARGS=args - Run in Docker"
	@echo "  docker-compose-run   - Run with Docker Compose"
	@echo "  deploy               - Build and deploy with Docker"
	@echo "  release              - Prepare for release"
	@echo "  all                  - Run all tasks"
	@echo "  help                 - Show this help message"
