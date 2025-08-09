# 🤖 Smart Agent

A powerful AI agent built with Python that leverages Ollama's LLaMA 3.1 model to intelligently process and analyze various file types. The agent uses a plugin-based tool system to extend its capabilities and provide comprehensive data analysis.

## ✨ Features

- **🧠 AI-Powered Analysis**: Uses LLaMA 3.1:8b model via Ollama for intelligent content processing
- **🔧 Extensible Tool System**: Plugin-based architecture for easy tool addition
- **📊 CSV Analysis**: Comprehensive CSV file analysis with statistics and metadata
- **📝 Markdown Processing**: Advanced markdown file parsing with header extraction
- **🚀 Async Support**: Fully asynchronous operations for better performance
- **📋 Comprehensive Testing**: 88% test coverage with pytest and coverage reporting
- **🎯 Type Hints**: Full type annotation support for better code quality

## 🛠️ Tools Available

### CSV Tool
- Analyzes CSV files and extracts metadata
- Provides row count, column information, and data preview
- Handles malformed files gracefully
- Returns structured data with comprehensive metadata

### Markdown Tool
- Reads and analyzes markdown files
- Extracts headers and document structure
- Provides content summary and statistics
- Supports special characters and Unicode

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- [Ollama](https://ollama.ai/) with LLaMA 3.1:8b model

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart_agent
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Install and start Ollama with LLaMA 3.1**
   ```bash
   # Install Ollama (follow instructions at https://ollama.ai/)
   ollama pull llama3.1:8b
   ```

4. **Run the agent**
   ```bash
   poetry run python -m smart_agent.agent
   ```

## 💻 Usage

### Basic Usage

```python
import asyncio
from smart_agent.agent import SmartAgent, LLaMA3Client
from smart_agent.registery import all_tools

async def main():
    llm_client = LLaMA3Client()
    agent = SmartAgent(llm_client, all_tools)
    
    # Analyze a CSV file
    response = await agent.run("give me information about data.csv")
    print(response)
    
    # Analyze a markdown file
    response = await agent.run("summarize the content of README.md")
    print(response)

asyncio.run(main())
```

### Example Queries

- `"give me information about test.csv"`
- `"i want to understand the story.md in detail"`
- `"analyze the structure of my data file"`
- `"what are the main sections in documentation.md"`

## 🧪 Testing

The project includes comprehensive test coverage with pytest.

### Running Tests

```bash
# Run all tool tests
./run_tests.sh tools

# Run tests with coverage
./run_tests.sh tools-cov

# Generate HTML coverage report
./run_tests.sh tools-html

# Or use poetry directly
poetry run pytest tests/tools/ --cov=src/smart_agent/tools --cov-report=term-missing
```

### Test Coverage

- **Overall Coverage**: 88%
- **Base Tool**: 82% coverage
- **CSV Tool**: 90% coverage
- **Markdown Tool**: 90% coverage

See `TESTING.md` for detailed testing documentation.

## 📁 Project Structure

```
smart_agent/
├── docs/                     # UML diagrams and documentation
│   ├── README.md            # UML documentation guide
│   ├── class_diagram.puml   # Class structure diagram
│   ├── sequence_diagram.puml # Interaction flow diagram
│   ├── component_diagram.puml # System components diagram
│   ├── activity_diagram.puml # Workflow diagram
│   ├── architecture_diagram.puml # System architecture
│   └── deployment_diagram.puml # Deployment structure
├── scripts/                  # Development scripts
│   ├── lint.sh              # Code quality checks
│   └── format.sh            # Auto-formatting script
├── src/
│   └── smart_agent/
│       ├── __init__.py
│       ├── agent.py          # Main agent implementation
│       ├── exceptions.py     # Custom exceptions
│       ├── logger.py         # Logging configuration
│       ├── registery.py      # Tool registry
│       ├── response.py       # Response handling
│       └── tools/            # Tool implementations
│           ├── __init__.py
│           ├── base_tool.py  # Abstract base tool
│           ├── csv_tool.py   # CSV analysis tool
│           └── md_tool.py    # Markdown analysis tool
├── tests/                    # Test suite
│   └── tools/                # Tool tests
├── pyproject.toml           # Project configuration
├── run_tests.sh            # Test runner script
├── TESTING.md              # Testing documentation
└── README.md               # This file
```

## 🏗️ Architecture & Design

The Smart Agent follows a **plugin-based architecture** with clear separation of concerns:

### System Architecture
- **Agent Layer**: Main orchestrator (`SmartAgent`)
- **LLM Layer**: Communication with Ollama (`LLaMA3Client`)
- **Tool Layer**: Extensible plugin system (`BaseTool` implementations)
- **Data Layer**: Structured results (`ToolResult`)

### Design Patterns
- **Abstract Factory**: `BaseTool` for tool creation
- **Strategy Pattern**: Different tools for different file types
- **Observer Pattern**: Logging system
- **Async/Await**: Non-blocking operations

### UML Documentation
Comprehensive UML diagrams are available in the `docs/` directory:
- **Class Diagram**: Object-oriented structure
- **Sequence Diagram**: Runtime interaction flow
- **Component Diagram**: System components and relationships
- **Activity Diagram**: Workflow and decision logic
- **Architecture Diagram**: High-level system design
- **Deployment Diagram**: Runtime environment setup

See `docs/README.md` for detailed diagram documentation and viewing instructions.

## 🔧 Development

### Adding New Tools

1. Create a new tool class inheriting from `BaseTool`:

```python
from smart_agent.tools.base_tool import BaseTool, ToolResult

class MyTool(BaseTool):
    def get_name(self) -> str:
        return "My Tool"
    
    async def run(self, **kwargs) -> ToolResult:
        # Your tool logic here
        return ToolResult(data="result", meta={"info": "metadata"})
    
    def to_ollama_tool(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.get_name(),
                "description": "Tool description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param": {"type": "string", "description": "Parameter description"}
                    },
                    "required": ["param"]
                }
            }
        }
```

2. Register your tool in `registery.py`
3. Add comprehensive tests in `tests/tools/test_my_tool.py`

### Code Quality

The project includes comprehensive code quality tools and linting:

```bash
# Run all linting checks
./scripts/lint.sh

# Auto-fix linting issues
./scripts/format.sh

# Or use poetry directly
poetry run ruff check .          # Fast Python linter
poetry run black .               # Code formatter
poetry run isort .               # Import sorter
poetry run mypy src/smart_agent  # Type checker
```

#### Linting Tools
- **Ruff**: Fast Python linter with comprehensive rules
- **Black**: Uncompromising code formatter
- **isort**: Import statement organizer
- **mypy**: Static type checker

#### Code Standards
- **Line Length**: 88 characters (Black default)
- **Import Organization**: First-party imports separated
- **Type Hints**: Required for all public functions
- **Error Handling**: Proper exception chaining with `from` clause

- **Type Hints**: All code uses type annotations
- **Async/Await**: Proper async programming patterns
- **Error Handling**: Comprehensive error handling with logging
- **Testing**: High test coverage with edge case handling

## 📋 Requirements

### Runtime Dependencies
- `ollama`: Ollama Python client
- `aiofiles`: Async file operations

### Development Dependencies
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `pytest-asyncio`: Async test support
- `ruff`: Fast Python linter
- `black`: Code formatter
- `isort`: Import organizer
- `mypy`: Static type checker

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run code quality checks (`./scripts/lint.sh`)
6. Auto-fix any formatting issues (`./scripts/format.sh`)
7. Ensure tests pass (`./run_tests.sh tools-cov`)
8. Commit your changes (`git commit -m 'Add amazing feature'`)
9. Push to the branch (`git push origin feature/amazing-feature`)
10. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for providing the LLM infrastructure
- [LLaMA](https://ai.meta.com/llama/) for the underlying language model
- The Python community for excellent async and testing tools

## 📞 Support

If you encounter any issues or have questions:

1. Check the `TESTING.md` file for testing help
2. Review the error logs for debugging information
3. Create an issue with detailed reproduction steps

---

**Made with ❤️ by sagi5060**