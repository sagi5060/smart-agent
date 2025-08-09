import pytest

from smart_agent.tools.base_tool import BaseTool, ToolResult


class TestToolResult:
    def test_tool_result_creation(self):
        result = ToolResult(data="test data", meta={"key": "value"})

        assert result.data == "test data"
        assert result.meta == {"key": "value"}

    def test_tool_result_defaults(self):
        result = ToolResult(data="error", meta={})

        assert result.data == "error"
        assert result.meta == {}

    def test_tool_result_with_complex_data(self):
        complex_data = [{"name": "John", "age": 25}, {"name": "Jane", "age": 30}]
        complex_meta = {"source": "database", "count": 2, "filters": {"active": True}}

        result = ToolResult(data=complex_data, meta=complex_meta)

        assert result.data == complex_data
        assert result.meta == complex_meta
        assert result.meta["count"] == 2
        assert result.meta["filters"]["active"] is True


class MockTool(BaseTool):
    def __init__(self, name="mock_tool", should_fail=False):
        self.name = name
        self.should_fail = should_fail

    def get_name(self) -> str:
        return self.name

    async def run(self, **kwargs) -> ToolResult:
        if self.should_fail:
            return ToolResult(data="", meta={"error": "Mock tool failed"})
        return ToolResult(data=f"Mock result: {kwargs}", meta={"success": True})

    def to_ollama_tool(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.get_name(),
                "description": "A mock tool for testing",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {"type": "string"},
                        "param2": {"type": "integer"},
                    },
                    "required": ["param1"],
                },
            },
        }


class TestBaseTool:
    @pytest.fixture
    def mock_tool(self):
        return MockTool()

    @pytest.fixture
    def failing_tool(self):
        return MockTool(name="failing_tool", should_fail=True)

    def test_get_name(self, mock_tool):
        assert mock_tool.get_name() == "mock_tool"

    @pytest.mark.asyncio
    async def test_run_success(self, mock_tool):
        result = await mock_tool.run(param1="test", param2=42)

        assert isinstance(result, ToolResult)
        assert "Mock result" in result.data
        assert result.meta["success"] is True

    @pytest.mark.asyncio
    async def test_run_failure(self, failing_tool):
        result = await failing_tool.run(param1="test")

        assert isinstance(result, ToolResult)
        assert result.data == ""
        assert "error" in result.meta
        assert "Mock tool failed" in result.meta["error"]

    def test_to_ollama_tool_structure(self, mock_tool):
        ollama_tool = mock_tool.to_ollama_tool()

        assert ollama_tool["type"] == "function"
        assert "function" in ollama_tool
        assert "name" in ollama_tool["function"]
        assert "description" in ollama_tool["function"]
        assert "parameters" in ollama_tool["function"]

        function = ollama_tool["function"]
        assert function["name"] == "mock_tool"
        assert function["description"] == "A mock tool for testing"

        parameters = function["parameters"]
        assert parameters["type"] == "object"
        assert "properties" in parameters
        assert "required" in parameters
        assert "param1" in parameters["properties"]
        assert "param2" in parameters["properties"]
        assert parameters["required"] == ["param1"]

    def test_tool_inheritance(self):
        # Test that MockTool properly inherits from BaseTool
        mock_tool = MockTool()
        assert isinstance(mock_tool, BaseTool)

    @pytest.mark.asyncio
    async def test_run_with_no_parameters(self, mock_tool):
        result = await mock_tool.run()

        assert isinstance(result, ToolResult)
        assert "Mock result: {}" in result.data

    @pytest.mark.asyncio
    async def test_run_with_complex_parameters(self, mock_tool):
        complex_params = {
            "string_param": "test string",
            "int_param": 123,
            "list_param": [1, 2, 3],
            "dict_param": {"nested": "value"},
        }

        result = await mock_tool.run(**complex_params)

        assert isinstance(result, ToolResult)
        assert "Mock result:" in result.data
        # The exact string representation may vary, but should contain the params
        assert str(complex_params) in result.data or "string_param" in result.data

    def test_multiple_tool_instances(self):
        tool1 = MockTool(name="tool1")
        tool2 = MockTool(name="tool2")

        assert tool1.get_name() == "tool1"
        assert tool2.get_name() == "tool2"
        assert tool1.get_name() != tool2.get_name()

    def test_ollama_tool_parameters_validation(self, mock_tool):
        ollama_tool = mock_tool.to_ollama_tool()
        params = ollama_tool["function"]["parameters"]

        # Check parameter types
        assert params["properties"]["param1"]["type"] == "string"
        assert params["properties"]["param2"]["type"] == "integer"

        # Check required parameters
        assert "param1" in params["required"]
        assert "param2" not in params["required"]
