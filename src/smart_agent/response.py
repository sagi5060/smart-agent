from dataclasses import dataclass
from typing import Any


@dataclass
class AgentResponse:
    """
    Represents a response from the agent.

    Attributes:
        content (str): The main content of the response.
        tool_name (str): The name of the tool used to generate the response.
        meta (dict): Additional metadata about the response.
        duration_ms (int): The duration of the response in milliseconds.
    """

    content: str
    tool_name: str
    meta: dict[str, Any]
    duration_ms: int
