import pytest
import tempfile
import os
from smart_agent.tools.md_tool import MarkdownTool
from smart_agent.tools.base_tool import ToolResult

class TestMarkdownTool:
    @pytest.fixture
    def md_tool(self):
        return MarkdownTool()
    
    @pytest.fixture
    def sample_md_file(self):
        content = """# Main Title

This is a paragraph with some content.

## Subtitle 1

More content here with some details.

### Subsection

- List item 1
- List item 2
- List item 3

## Another Section

Final paragraph with conclusion."""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_file = f.name
        yield temp_file
        os.unlink(temp_file)
    
    @pytest.fixture
    def empty_md_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("")
            temp_file = f.name
        yield temp_file
        os.unlink(temp_file)
    
    def test_get_name(self, md_tool):
        assert md_tool.get_name() == "Markdown Tool"
    
    def test_to_ollama_tool(self, md_tool):
        ollama_tool = md_tool.to_ollama_tool()
        assert ollama_tool["type"] == "function"
        assert ollama_tool["function"]["name"] == "Markdown Tool"
        assert "description" in ollama_tool["function"]
        assert "parameters" in ollama_tool["function"]
        assert "file_path" in ollama_tool["function"]["parameters"]["properties"]
    
    @pytest.mark.asyncio
    async def test_run_valid_markdown(self, md_tool, sample_md_file):
        result = await md_tool.run(file_path=sample_md_file)
        
        assert isinstance(result, ToolResult)
        assert "# Main Title" in result.data
        assert "## Subtitle 1" in result.data
        assert "### Subsection" in result.data
        
        # Check metadata
        assert result.meta["file_path"] == sample_md_file
        assert result.meta["summary"] == "# Main Title"
        assert result.meta["length"] > 0
        assert result.meta["lines_count"] > 0
        assert result.meta["word_count"] > 0
        
        # Check headers extraction
        headers = result.meta["headers"]
        assert "# Main Title" in headers
        assert "## Subtitle 1" in headers
        assert "### Subsection" in headers
        assert "## Another Section" in headers
    
    @pytest.mark.asyncio
    async def test_run_empty_markdown(self, md_tool, empty_md_file):
        result = await md_tool.run(file_path=empty_md_file)
        
        assert isinstance(result, ToolResult)
        assert result.data == ""
        assert result.meta["file_path"] == empty_md_file
        assert result.meta["summary"] == "No content"
        assert result.meta["length"] == 0
        assert result.meta["lines_count"] == 0  # Empty file has no lines
        assert result.meta["word_count"] == 0
        assert result.meta["headers"] == []
    
    @pytest.mark.asyncio
    async def test_run_nonexistent_file(self, md_tool):
        result = await md_tool.run(file_path="nonexistent.md")
        
        assert isinstance(result, ToolResult)
        assert result.data == ""
        assert "error" in result.meta
        assert "not found" in result.meta["error"]
    
    @pytest.mark.asyncio
    async def test_run_markdown_with_special_characters(self, md_tool):
        content = """# Title with émojis 🚀

Content with **bold** and *italic* text.

```python
def hello():
    print("Hello, World!")
```

> This is a blockquote

[Link](https://example.com)
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(content)
            special_file = f.name
        
        try:
            result = await md_tool.run(file_path=special_file)
            assert isinstance(result, ToolResult)
            assert "émojis 🚀" in result.data
            assert "**bold**" in result.data
            assert "```python" in result.data
            assert result.meta["word_count"] > 0
        finally:
            os.unlink(special_file)
    
    def test_read_markdown_method(self, md_tool, sample_md_file):
        content = md_tool._read_markdown(sample_md_file)
        
        assert isinstance(content, str)
        assert "# Main Title" in content
        assert "## Subtitle 1" in content
        assert len(content) > 0
    
    @pytest.mark.asyncio
    async def test_headers_extraction(self, md_tool):
        content = """# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header

Regular text
Not a header #
# Another H1"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(content)
            header_file = f.name
        
        try:
            result = await md_tool.run(file_path=header_file)
            headers = result.meta["headers"]
            
            assert "# H1 Header" in headers
            assert "## H2 Header" in headers
            assert "### H3 Header" in headers
            assert "#### H4 Header" in headers
            assert "##### H5 Header" in headers
            assert "###### H6 Header" in headers
            assert "# Another H1" in headers
            assert "Not a header #" not in headers
            assert "Regular text" not in headers
        finally:
            os.unlink(header_file)
