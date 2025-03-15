# Contributing to APIKI

Thank you for your interest in contributing to APIKI! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/eagurin/apika.git
   cd apika
   ```

2. Set up the development environment using Poetry:
   ```bash
   poetry install
   ```

3. Install pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```

## Code Style

We use the following tools to maintain code quality:

- **Black**: For code formatting with a line length of 79
- **isort**: For sorting imports
- **flake8**: For linting
- **mypy**: For static type checking

These tools are configured in `pyproject.toml` and `.pre-commit-config.yaml`.

## Testing

We use pytest for testing. To run tests:

```bash
poetry run pytest
```

To run tests with coverage:

```bash
poetry run pytest --cov=apiki
```

## Pull Request Process

1. Create a new branch for your feature or bugfix
2. Make your changes and ensure all tests pass
3. Create a pull request to the `main` branch
4. Wait for code review and address any comments

## Continuous Integration

We use GitHub Actions for continuous integration. Every pull request triggers:

- Linting checks
- Type checking
- Test runs across Python 3.10, 3.11, and 3.12

## License

By contributing to APIKI, you agree that your contributions will be licensed under the project's MIT License. 