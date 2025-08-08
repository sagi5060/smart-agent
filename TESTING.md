# Testing Guide for Smart Agent

## Overview

This project uses pytest for testing with coverage reporting. The test suite covers all tools and provides comprehensive validation of functionality.

## Test Structure

```
tests/
├── __init__.py
└── tools/
    ├── __init__.py
    ├── test_base_tool.py    # Tests for BaseTool and ToolResult
    ├── test_csv_tool.py     # Tests for CsvTool
    └── test_md_tool.py      # Tests for MarkdownTool
```

## Running Tests

### Quick Commands

```bash
# Run all tool tests
poetry run pytest tests/tools/ -v

# Run with coverage (terminal output)
poetry run pytest tests/tools/ --cov=src/smart_agent/tools --cov-report=term-missing

# Run with HTML coverage report
poetry run pytest tests/tools/ --cov=src/smart_agent/tools --cov-report=html
```

### Using the Test Runner Script

```bash
# Make script executable (one time)
chmod +x run_tests.sh

# Run tool tests only
./run_tests.sh tools

# Run tool tests with coverage
./run_tests.sh tools-cov

# Run tool tests with HTML coverage report
./run_tests.sh tools-html

# Run all tests with full coverage
./run_tests.sh all-cov
```

## Coverage Results

Current coverage for tools:
- **Overall Coverage: 88%**
- `base_tool.py`: 82% coverage
- `csv_tool.py`: 90% coverage  
- `md_tool.py`: 90% coverage

### Missing Coverage Areas

The uncovered lines are primarily:
- Abstract method implementations that can't be tested directly
- Exception handling paths that are difficult to trigger
- Some edge cases in error handling

## Test Features

### What's Tested ✅

- **Functionality**: All main tool operations
- **Error Handling**: File not found, invalid data
- **Edge Cases**: Empty files, malformed data
- **Async Operations**: All async methods properly tested
- **Tool Integration**: Ollama tool format validation
- **Data Validation**: Input/output validation

### Test Types

1. **Unit Tests**: Individual method testing
2. **Integration Tests**: Tool workflow testing
3. **Error Tests**: Exception and error handling
4. **Edge Case Tests**: Boundary conditions

## Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = ["--strict-markers", "--verbose"]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
show_missing = true
exclude_lines = ["pragma: no cover", "if __name__ == .__main__."]
```

## Dependencies

- `pytest`: Test framework
- `pytest-cov`: Coverage reporting
- `pytest-asyncio`: Async test support

Install with:
```bash
poetry install
```

## Viewing Results

### Terminal Coverage
Shows missing lines directly in terminal output.

### HTML Coverage Report
- Generated in `htmlcov/` directory
- Open `htmlcov/index.html` in browser
- Interactive line-by-line coverage view
- Click on files to see detailed coverage

## Best Practices

1. **Run tests before commits**
2. **Maintain >85% coverage**
3. **Test both success and failure paths**
4. **Use descriptive test names**
5. **Mock external dependencies**
6. **Test edge cases and boundary conditions**

## Adding New Tests

When adding new tools:

1. Create test file: `tests/tools/test_new_tool.py`
2. Follow existing patterns
3. Test all public methods
4. Include error handling tests
5. Add to coverage reporting

Example test structure:
```python
import pytest
from smart_agent.tools.new_tool import NewTool

class TestNewTool:
    @pytest.fixture
    def new_tool(self):
        return NewTool()
    
    def test_get_name(self, new_tool):
        assert new_tool.get_name() == "expected_name"
    
    @pytest.mark.asyncio
    async def test_run_success(self, new_tool):
        result = await new_tool.run(param="value")
        assert result.success is True
```
