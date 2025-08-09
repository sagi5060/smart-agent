# Testing Guide

## Overview

Pytest-based testing with coverage reporting for comprehensive tool validation.

## Running Tests

```bash
# Quick test commands
./run_tests.sh tools           # Basic tests
./run_tests.sh tools-cov       # With coverage
./run_tests.sh tools-html      # HTML coverage report

# Or with Poetry
poetry run pytest tests/tools/ --cov=src/smart_agent/tools --cov-report=term-missing
```

## Coverage Results

- **Overall: 88%**
- `base_tool.py`: 82%
- `csv_tool.py`: 90%  
- `md_tool.py`: 90%

## Test Features

**What's Tested:**
- Tool functionality and error handling
- File operations (valid, empty, missing files)
- Async operations and data validation
- Ollama tool format validation

## Adding New Tests

For new tools, create `tests/tools/test_new_tool.py`:

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

## Best Practices

1. Run tests before commits
2. Maintain >85% coverage
3. Test success and failure paths
4. Use descriptive test names
