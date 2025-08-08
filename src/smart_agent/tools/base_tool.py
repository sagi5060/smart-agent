from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class ToolResult:
    data: str
    meta: dict[str, Any]

class BaseTool(ABC):
    """
    Abstract base class for tools that can be used by the agent.
    """

    @abstractmethod
    async def run(self, *args, **kwargs) -> ToolResult:
        """
        Execute the tool with the given arguments and return a ToolResult.
        
        Args:
            *args: Positional arguments for the tool.
            **kwargs: Keyword arguments for the tool.

        Returns:
            ToolResult: The result of the tool execution.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the tool.

        Returns:
            str: The name of the tool.
        """
        pass

    @abstractmethod
    def to_ollama_tool(self) -> dict[str, Any]:
        """
        Return this tool's JSON schema definition for Ollama chat tools parameter.
        Must return a dict like:
        {
          "type": "function",
          "function": {
            "name": "tool name",
            "description": "Describe what the tool does",
            "parameters": {
              "type": "object",
              "properties": {
                "input": {"type": "string", "description": "User query or filename"}
              },
              "required": ["input"]
            }
          }
        }
        """
        pass