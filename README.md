# APIKI - API Knowledge Integration

APIKI (API Knowledge Integration) is a powerful package for interacting with APIs using LangChain agents and OpenAPI specifications.

## Features

- **API Agent**: Interact with any API using natural language through LangChain agents
- **Direct API Client**: Programmatically interact with APIs using a simple client interface
- **CLI Tool**: Command-line interface for interacting with APIs
- **OpenAPI Integration**: Automatically discovers API capabilities using OpenAPI specifications

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

## Requirements

- Python 3.8+
- LangChain
- OpenAI API key (for agent mode)
- An API with an OpenAPI specification 