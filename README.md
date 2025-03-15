# APIKI - API Knowledge Integration

APIKI (API Knowledge Integration) is a powerful package for interacting with APIs using LangChain agents and OpenAPI specifications.

## Features

- **API Agent**: Interact with any API using natural language through LangChain agents
- **Direct API Client**: Programmatically interact with APIs using a simple client interface
- **CLI Tool**: Command-line interface for interacting with APIs
- **OpenAPI Integration**: Automatically discovers API capabilities using OpenAPI specifications
- **Docker Support**: Run APIKI in a containerized environment
- **Just Command Runner**: Simplified development workflow with just commands

## Installation

```bash
# Using poetry
poetry add apiki

# Using pip
pip install apiki
```

## Quick Start

### Using the API Agent

```python
import os
from dotenv import load_dotenv
from apiki.agent import APIAgent, APIAgentConfig

# Load environment variables for OpenAI API key
load_dotenv()

# Configure the agent
config = APIAgentConfig(
    openapi_url="http://localhost:7272/openapi.json",
    api_base_url="http://localhost:7272",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create the agent
agent = APIAgent(config)

# Send a natural language query to the agent
response = agent.run("Get a list of all items from the API")
print(response.output)
```

### Using the Direct Client

```python
from apiki.client import APIClient, APIClientConfig

# Configure the client
config = APIClientConfig(
    openapi_url="http://localhost:7272/openapi.json",
    api_base_url="http://localhost:7272"
)

# Create the client
client = APIClient(config)

# Make API requests
response = client.get("/api/items")
print(response.data)
```

### Using the CLI

```bash
# Using agent mode (requires OpenAI API key)
python -m apiki.cli agent "List all available resources"

# Using client mode
python -m apiki.cli client get /api/items

# Create a resource
python -m apiki.cli client post /api/items --data '{"name": "Test Item", "description": "Created via CLI"}'

# Get information about available endpoints
python -m apiki.cli client endpoints
```

### Using Docker

```bash
# Build the Docker image
docker build -t apiki .

# Run APIKI in a Docker container
docker run --rm -e OPENAI_API_KEY=your_api_key apiki agent "List all available endpoints"

# Using Docker Compose
docker-compose up --build
```

### Using Just Command Runner

```bash
# Install Just (macOS)
brew install just

# Install Just (using Cargo)
cargo install just

# List all available commands
just

# Run tests
just test

# Format code and run linting
just check

# Build and run with Docker
just docker-build
just docker-run agent "List all available endpoints"
```

## Configuration

### API Agent Configuration

| Parameter               | Description                                       | Default                           |
|-------------------------|---------------------------------------------------|-----------------------------------|
| `openapi_url`           | URL to the OpenAPI specification                  | `http://localhost:7272/openapi.json` |
| `api_base_url`          | Base URL for the API                              | `http://localhost:7272`           |
| `model_name`            | Name of the OpenAI model to use                   | `gpt-3.5-turbo`                   |
| `temperature`           | Temperature for the model                         | `0.0`                             |
| `api_key`               | OpenAI API key                                    | `None` (uses env var)             |
| `headers`               | Headers to include in API requests                | `{}`                              |
| `allow_dangerous_requests` | Whether to allow potentially dangerous requests | `True`                            |
| `use_chat_model`        | Whether to use ChatOpenAI instead of OpenAI        | `True`                            |
| `timeout`               | Timeout for API requests in seconds               | `30`                              |
| `max_token_limit`       | Maximum number of tokens to use in the JsonSpec   | `4000`                            |
| `verbose`               | Whether to enable verbose logging                 | `True`                            |

### API Client Configuration

| Parameter               | Description                                       | Default                           |
|-------------------------|---------------------------------------------------|-----------------------------------|
| `openapi_url`           | URL to the OpenAPI specification                  | `http://localhost:7272/openapi.json` |
| `api_base_url`          | Base URL for the API                              | `http://localhost:7272`           |
| `headers`               | Headers to include in API requests                | `{}`                              |
| `timeout`               | Timeout for API requests in seconds               | `30`                              |
| `verify_ssl`            | Whether to verify SSL certificates                | `True`                            |
| `verbose`               | Whether to enable verbose logging                 | `True`                            |

## Development

### Using Just Command Runner

The project includes a `justfile` with common development tasks:

```bash
# Install dependencies
just install

# Run tests
just test

# Check code quality (format, lint, type check)
just check

# Build Docker image
just docker-build

# Run in Docker
just docker-run <command>
```

See the `justfile` for a complete list of available commands.

## Requirements

- Python 3.10+
- LangChain
- OpenAI API key (for agent mode)
- An API with an OpenAPI specification
- Docker (optional, for containerized usage)
- Just command runner (optional, for simplified development workflow)
