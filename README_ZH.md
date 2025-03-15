# 🚀 apiki - API 知识集成

> **释放 AI 的力量征服任何 API！** apiki 是一款革命性工具，通过尖端 LLM 技术弥合了自然语言和 API 之间的鸿沟。

apiki (API 知识集成) 是一个最先进的框架，它通过将 LangChain 代理的智能与 OpenAPI 规范的结构相结合，彻底改变了开发人员与 API 的交互方式，实现了前所未有的 API 交互能力。

## ✨ 超强功能

- 🧠 **AI 驱动的 API 代理**：通过先进的 LLM 驱动代理，使用自然语言与任何 API 通信
- 🔌 **无缝 API 客户端**：使用优雅简洁但功能强大的客户端界面以编程方式与 API 交互
- 💻 **智能命令行界面**：具有自然语言处理功能的命令行界面，用于 API 交互
- 📚 **OpenAPI 超能力**：自动发现并适应 API 功能，使用 OpenAPI 规范
- ⚡ **性能优化**：专为生产环境中的速度和可靠性而构建

## 🛠️ 快速安装

```bash
# 使用 poetry（推荐用于最大程度地控制依赖项）
poetry add apiki

# 使用 pip（用于快速集成）
pip install apiki
```

## 🚀 立即开始使用

### 🧠 释放 API 代理的力量

```python
import os
from dotenv import load_dotenv
from apiki.agent import APIAgent, APIAgentConfig

# 加载 OpenAI API 密钥的环境变量
load_dotenv()

# 配置代理
config = APIAgentConfig(
    openapi_url="http://localhost:7272/openapi.json",
    api_base_url="http://localhost:7272",
    api_key=os.getenv("OPENAI_API_KEY")
)

# 创建代理
agent = APIAgent(config)

# 向代理发送自然语言查询
response = agent.run("获取 API 中的所有项目列表")
print(response.output)
```

### 🔌 直接客户端界面

```python
from apiki.client import APIClient, APIClientConfig

# 配置客户端
config = APIClientConfig(
    openapi_url="http://localhost:7272/openapi.json",
    api_base_url="http://localhost:7272"
)

# 创建客户端
client = APIClient(config)

# 发送 API 请求
response = client.get("/api/items")
print(response.data)
```

### 💻 命令行魔法

```bash
# 使用代理模式（需要 OpenAI API 密钥）
python -m apiki.cli agent "列出所有可用资源"

# 使用客户端模式
python -m apiki.cli client get /api/items

# 创建资源
python -m apiki.cli client post /api/items --data '{"name": "测试项目", "description": "通过 CLI 创建"}'

# 获取有关可用端点的信息
python -m apiki.cli client endpoints
```

## 🔧 高级配置

### 🧠 API 代理配置

| 参数                     | 描述                                       | 默认值                             |
|-------------------------|-------------------------------------------|-----------------------------------|
| `openapi_url`           | OpenAPI 规范的 URL                          | `http://localhost:7272/openapi.json` |
| `api_base_url`          | API 的基本 URL                              | `http://localhost:7272`           |
| `model_name`            | 要使用的 OpenAI 模型名称                     | `gpt-3.5-turbo`                   |
| `temperature`           | 模型的温度                                   | `0.0`                             |
| `api_key`               | OpenAI API 密钥                             | `None`（使用环境变量）              |
| `headers`               | 要包含在 API 请求中的标头                     | `{}`                              |
| `allow_dangerous_requests` | 是否允许潜在危险的请求                      | `True`                            |
| `use_chat_model`        | 是否使用 ChatOpenAI 代替 OpenAI              | `True`                            |
| `timeout`               | API 请求的超时时间（秒）                      | `30`                              |
| `max_token_limit`       | 在 JsonSpec 中使用的最大令牌数                | `4000`                            |
| `verbose`               | 是否启用详细日志记录                          | `True`                            |

### 🔌 API 客户端配置

| 参数                     | 描述                                       | 默认值                             |
|-------------------------|-------------------------------------------|-----------------------------------|
| `openapi_url`           | OpenAPI 规范的 URL                          | `http://localhost:7272/openapi.json` |
| `api_base_url`          | API 的基本 URL                              | `http://localhost:7272`           |
| `headers`               | 要包含在 API 请求中的标头                     | `{}`                              |
| `timeout`               | API 请求的超时时间（秒）                      | `30`                              |
| `verify_ssl`            | 是否验证 SSL 证书                            | `True`                            |
| `verbose`               | 是否启用详细日志记录                          | `True`                            |

## 🔥 技术成就

- **零样本 API 交互**：apiki 可以在没有事先训练的情况下与任何 API 交互，仅使用 OpenAPI 规范
- **LLM 驱动的智能**：利用最先进的语言模型来理解和执行复杂的 API 操作
- **动态请求构建**：根据自然语言指令自动构建 API 请求
- **架构感知处理**：智能解析和验证 API 架构，实现准确交互
- **自适应错误处理**：强大的错误恢复和智能重试机制
- **高性能架构**：针对生产工作负载进行了优化，延迟最小
- **全面测试**：广泛的测试套件，确保在各种场景下的可靠性

## 📋 要求

- 🐍 Python 3.10+
- 🔗 LangChain 生态系统
- 🔑 OpenAI API 密钥（代理模式）
- 📄 具有 OpenAPI 规范的 API

## 🌟 为什么选择 apiki？

apiki 在 API 交互技术方面代表了质的飞跃。通过将先进的 LLM 能力与结构化 API 规范相结合，它使开发人员能够以前所未有的方式与 API 交互。无论您是构建复杂的集成、探索新的 API 还是自动化工作流程，apiki 都能提供掌握任何 API 挑战所需的智能和灵活性。

**准备好彻底改变您使用 API 的方式了吗？立即开始使用 apiki！**
