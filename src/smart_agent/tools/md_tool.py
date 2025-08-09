"""
Markdown Tool for reading and summarizing markdown files.
"""

import asyncio
import logging
from typing import Any

from .base_tool import BaseTool, ToolResult

logger = logging.getLogger(__name__)


class MarkdownTool(BaseTool):
    async def run(self, file_path: str) -> ToolResult:
        """
        Run the Markdown tool with the given file path and return a ToolResult.

        Args:
            file_path (str): The path to the markdown file to read and summarize.

        Returns:
            ToolResult: The result of the tool execution containing the summary and metadata.
        """
        logger.debug(f"Reading Markdown file: {file_path}")
        loop = asyncio.get_running_loop()
        try:
            content = await loop.run_in_executor(None, self._read_markdown, file_path)
            logger.info(
                f"Successfully read Markdown file: {file_path} ({len(content)} characters)"
            )
        except FileNotFoundError:
            logger.warning(f"Markdown file not found: {file_path}")
            return ToolResult(data="", meta={"error": f"File '{file_path}' not found."})
        except Exception as e:
            logger.error(f"Error reading Markdown file {file_path}: {str(e)}")
            return ToolResult(data="", meta={"error": str(e)})

        # Simple summary logic (could be replaced with a more complex algorithm)
        lines = content.splitlines()
        summary = lines[0] if lines else "No content"

        # Extract headers (lines starting with #)
        headers = [line for line in lines if line.startswith("#")]

        meta = {
            "file_path": file_path,
            "length": len(content),
            "summary": summary,
            "lines_count": len(lines),
            "headers": headers,
            "word_count": len(content.split()),
        }
        return ToolResult(data=content, meta=meta)

    def _read_markdown(self, file_path: str) -> str:
        """
        Read markdown file content.

        Args:
            file_path (str): Path to the markdown file.

        Returns:
            str: Content of the markdown file.
        """
        with open(file_path, encoding="utf-8") as f:
            return f.read()

    def get_name(self) -> str:
        """
        Get the name of the Markdown tool.

        Returns:
            str: The name of the tool.
        """
        return "Markdown Tool"

    def to_ollama_tool(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.get_name(),
                "description": "Reads and analyzes markdown files, extracting content and metadata.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the markdown file to read",
                        }
                    },
                    "required": ["file_path"],
                },
            },
        }
