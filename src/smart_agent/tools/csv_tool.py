"""
CSV Tool for retrieving CSV data from a file and metadata about it, such as row count and columns.
"""

import asyncio
import csv
import logging
import os
from typing import Any

from .base_tool import BaseTool, ToolResult

logger = logging.getLogger(__name__)


class CsvTool(BaseTool):
    async def run(self, file_path: str) -> ToolResult:
        """
        Run the CSV tool with the given arguments and return a ToolResult.
        """
        logger.debug(f"Reading CSV file: {file_path}")
        loop = asyncio.get_running_loop()
        try:
            data, columns = await loop.run_in_executor(None, self._read_csv, file_path)
            logger.info(
                f"Successfully read CSV file: {file_path} with {len(data)} rows"
            )
        except FileNotFoundError:
            logger.warning(f"CSV file not found: {file_path}")
            return ToolResult(data="", meta={"error": f"File '{file_path}' not found."})
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            return ToolResult(data="", meta={"error": str(e)})
        return ToolResult(
            data=data,
            meta={"columns": columns, "row_count": len(data), "file_path": file_path},
        )

    def _read_csv(self, file_path: str):
        if file_path[0] == "~":
            file_path = os.path.expanduser(file_path)
        with open(file_path) as f:
            reader = csv.DictReader(f)
            data = list(reader)
            return data, reader.fieldnames

    def get_name(self) -> str:
        """
        Get the name of the CSV tool.
        """
        return "CSV Tool"

    def to_ollama_tool(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.get_name(),
                "description": "Retrieves CSV data and metadata from a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Full or relative path to the CSV file",
                        }
                    },
                    "required": ["file_path"],
                },
            },
        }
