# 🚀 apiki - api knowledge integration

> **Unleash the power of AI to conquer any API!** apiki is a revolutionary tool that bridges the gap between natural language and APIs with cutting-edge LLM technology.

apiki (api knowledge integration) is a state-of-the-art framework that transforms how developers interact with APIs, combining the intelligence of LangChain agents with the structure of OpenAPI specifications for unprecedented API interaction capabilities.

## ✨ Supercharged Features

- 🧠 **AI-Powered API Agent**: Communicate with any API using natural language through advanced LLM-driven agents
- 🔌 **Seamless API Client**: Programmatically interact with APIs using an elegantly simple yet powerful client interface
- 💻 **Intelligent CLI**: Command-line interface with natural language processing for API interactions
- 📚 **OpenAPI Superpowers**: Automatically discovers and adapts to API capabilities using OpenAPI specifications
- ⚡ **Performance Optimized**: Built for speed and reliability in production environments

## 🛠️ Quick Installation

```bash
# Using poetry (recommended for maximum dependency control)
poetry add apiki

# Using pip (for quick integration)
pip install apiki
```

## 🚀 Getting Started in Seconds

### 🧠 Unleash the API Agent

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

### 🔌 Direct Client Interface

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

### 💻 Command-line Magic

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

## 🔧 Advanced Configuration

### 🧠 API Agent Configuration

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

### 🔌 API Client Configuration

| Parameter               | Description                                       | Default                           |
|-------------------------|---------------------------------------------------|-----------------------------------|
| `openapi_url`           | URL to the OpenAPI specification                  | `http://localhost:7272/openapi.json` |
| `api_base_url`          | Base URL for the API                              | `http://localhost:7272`           |
| `headers`               | Headers to include in API requests                | `{}`                              |
| `timeout`               | Timeout for API requests in seconds               | `30`                              |
| `verify_ssl`            | Whether to verify SSL certificates                | `True`                            |
| `verbose`               | Whether to enable verbose logging                 | `True`                            |

## 🔥 Technical Achievements

- **Zero-Shot API Interaction**: apiki can interact with any API without prior training, using only the OpenAPI specification
- **LLM-Powered Intelligence**: Leverages state-of-the-art language models to understand and execute complex API operations
- **Dynamic Request Composition**: Automatically constructs API requests based on natural language instructions
- **Schema-Aware Processing**: Intelligently parses and validates API schemas for accurate interactions
- **Adaptive Error Handling**: Robust error recovery and intelligent retry mechanisms
- **High-Performance Architecture**: Optimized for production workloads with minimal latency
- **Comprehensive Testing**: Extensive test suite ensuring reliability across diverse scenarios

## 📋 Requirements

- 🐍 Python 3.10+
- 🔗 LangChain ecosystem
- 🔑 OpenAI API key (for agent mode)
- 📄 An API with an OpenAPI specification

## 🌟 Why apiki?

apiki represents a quantum leap in API interaction technology. By combining advanced LLM capabilities with structured API specifications, it enables developers to interact with APIs in ways previously thought impossible. Whether you're building complex integrations, exploring new APIs, or automating workflows, apiki provides the intelligence and flexibility needed to master any API challenge.

**Ready to revolutionize how you work with APIs? Start using apiki today!**
