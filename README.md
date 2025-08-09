# 🤖 Smart Agent

A Python AI agent using Ollama's LLaMA 3.1 model to analyze CSV and Markdown files via CLI and REST API.

## ✨ Features

- **🧠 AI Analysis**: LLaMA 3.1:8b model via Ollama for intelligent content processing
- **📊 CSV Tool**: Reads CSV files, extracts metadata (row count, columns, data preview)
- **📝 Markdown Tool**: Reads markdown files, extracts headers and content structure
- **💻 CLI Interface**: Complete command-line interface with query, info, and server commands
- **🌐 REST API**: FastAPI-based web server with health checks
- **🚀 Async Support**: Fully asynchronous operations for better performance
- **📋 Testing**: 88% test coverage with comprehensive test suite

## 🛠️ Available Tools

### CSV Tool
- Reads CSV files and extracts data
- Provides row count, column names, and content preview
- Handles file not found errors gracefully
- Returns structured data with metadata

### Markdown Tool
- Reads and analyzes markdown files
- Extracts headers (lines starting with #)
- Provides content summary and statistics
- Supports Unicode and special characters

## 🚀 Installation

### Option 1: Install as CLI Tool (Recommended)

Build and install the wheel package for system-wide CLI access:

```bash
# Clone and build
git clone <repository-url> && cd smart_agent
pip install build
python3 -m build

# Install the wheel
pip install dist/smart_agent-1.0.0-py3-none-any.whl

# Now use directly without poetry run
smart-agent info health
smart-agent query --text "analyze data.csv"
```

### Option 2: Development Installation

For development or if you prefer Poetry:

```bash
git clone <repository-url> && cd smart_agent
poetry install

# Use with poetry run
poetry run smart-agent info health
```

### Prerequisites Setup

Install Ollama and the required model:

```bash
# Install Ollama (follow instructions at https://ollama.ai/)
ollama pull llama3.1:8b
ollama serve
```

Verify installation:
```bash
smart-agent info health  # or: poetry run smart-agent info health
```

## 💻 Usage

### Command Line Interface

```bash
# One-time query
smart-agent query --text "analyze data.csv"

# Start REST API server
smart-agent run --host 0.0.0.0 --port 8000

# Check system info and health
smart-agent info health

# List available tools
smart-agent tools list
```

### REST API

Start the server and make requests:
```bash
smart-agent run
curl -X POST http://localhost:8000/answer -H "Content-Type: application/json" -d '{"query": "analyze test.csv"}'
```

### Programmatic Usage

```python
from smart_agent.agent import SmartAgent
agent = SmartAgent()
response = await agent.run("analyze data.csv")
```

## 🧪 Testing

```bash
./run_tests.sh tools           # Run tests
./run_tests.sh tools-cov       # With coverage
```

Current test coverage: **88%** overall.

## 🏗️ Architecture

- **Agent Layer**: `SmartAgent` orchestrates LLM interactions and tool calls
- **LLM Layer**: `LLaMA3Client` handles communication with Ollama
- **Tool Layer**: Modular tools implementing `BaseTool` interface
- **CLI Layer**: Typer-based command interface
- **API Layer**: FastAPI-based REST server

Tools are automatically discovered via entry points defined in `pyproject.toml`.

## 🔧 Development

### Adding New Tools

1. Create a new tool class inheriting from `BaseTool`
2. Add to `pyproject.toml` entry points
3. Add tests in `tests/tools/`

### Code Quality

```bash
./scripts/lint.sh      # Check
./scripts/format.sh    # Fix
```

## 📋 Dependencies

**Runtime**: ollama, aiofiles, fastapi, typer, uvicorn  
**Development**: pytest, pytest-cov, pytest-asyncio, ruff, black, isort, mypy

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


