import logging
from importlib.metadata import entry_points

from smart_agent.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

_TOOLS_CACHE: list[BaseTool] | None = None


def load_tools() -> list[BaseTool]:
    """Load all registered tools from entry points."""
    global _TOOLS_CACHE
    if _TOOLS_CACHE is not None:
        return _TOOLS_CACHE

    eps = entry_points()
    selected_eps = eps.select(group="smart_agent.tools")
    tool_instances: list[BaseTool] = []

    for ep in selected_eps:
        tool_class = ep.load()
        tool_instances.append(tool_class())

    # Log loaded tools (now occurs after CLI logging setup)
    for tool in tool_instances:
        logger.debug(f"Loaded tool: {tool.get_name()}")

    _TOOLS_CACHE = tool_instances
    return tool_instances
