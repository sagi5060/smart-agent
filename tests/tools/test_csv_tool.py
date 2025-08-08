import pytest
import tempfile
import os
import csv
from unittest.mock import patch, MagicMock
from smart_agent.tools.csv_tool import CsvTool
from smart_agent.tools.base_tool import ToolResult

class TestCsvTool:
    @pytest.fixture
    def csv_tool(self):
        return CsvTool()
    
    @pytest.fixture
    def sample_csv_file(self):
        # Create a temporary CSV file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\n")
            f.write("John,25,New York\n")
            f.write("Jane,30,London\n")
            f.write("Bob,35,Paris\n")
            temp_file = f.name
        yield temp_file
        os.unlink(temp_file)
    
    def test_get_name(self, csv_tool):
        assert csv_tool.get_name() == "CSV Tool"
    
    def test_to_ollama_tool(self, csv_tool):
        ollama_tool = csv_tool.to_ollama_tool()
        assert ollama_tool["type"] == "function"
        assert ollama_tool["function"]["name"] == "CSV Tool"
        assert "description" in ollama_tool["function"]
        assert "parameters" in ollama_tool["function"]
        assert "file_path" in ollama_tool["function"]["parameters"]["properties"]
    
    @pytest.mark.asyncio
    async def test_run_valid_csv(self, csv_tool, sample_csv_file):
        result = await csv_tool.run(file_path=sample_csv_file)
        
        assert isinstance(result, ToolResult)
        assert len(result.data) == 3  # 3 rows of data
        assert result.meta["columns"] == ["name", "age", "city"]
        assert result.meta["row_count"] == 3
        assert result.meta["file_path"] == sample_csv_file
        
        # Check first row data
        assert result.data[0]["name"] == "John"
        assert result.data[0]["age"] == "25"
        assert result.data[0]["city"] == "New York"
    
    @pytest.mark.asyncio
    async def test_run_nonexistent_file(self, csv_tool):
        result = await csv_tool.run(file_path="nonexistent.csv")
        
        assert isinstance(result, ToolResult)
        assert result.data == ""
        assert "error" in result.meta
        assert "not found" in result.meta["error"]
    
    @pytest.mark.asyncio
    async def test_run_empty_csv(self, csv_tool):
        # Create empty CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\n")  # Only headers
            empty_file = f.name
        
        try:
            result = await csv_tool.run(file_path=empty_file)
            assert isinstance(result, ToolResult)
            assert len(result.data) == 0
            assert result.meta["row_count"] == 0
            assert result.meta["columns"] == ["name", "age", "city"]
        finally:
            os.unlink(empty_file)
    
    @pytest.mark.asyncio
    async def test_run_malformed_csv(self, csv_tool):
        # Create malformed CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\n")
            f.write("John,25\n")  # Missing column
            f.write("Jane,30,London,Extra\n")  # Extra column
            malformed_file = f.name
        
        try:
            result = await csv_tool.run(file_path=malformed_file)
            assert isinstance(result, ToolResult)
            # Should handle gracefully - CSV reader is quite forgiving
            assert len(result.data) == 2
        finally:
            os.unlink(malformed_file)
    
    def test_read_csv_method(self, csv_tool, sample_csv_file):
        data, columns = csv_tool._read_csv(sample_csv_file)
        
        assert len(data) == 3
        assert columns == ["name", "age", "city"]
        assert data[0]["name"] == "John"
        assert data[1]["name"] == "Jane"
        assert data[2]["name"] == "Bob"
