import logging
from importlib.metadata import entry_points

logger = logging.getLogger(__name__)


def load_tools():
    eps = entry_points()
    selected_eps = eps.select(group="smart_agent.tools")
    tool_instances = []
    for ep in selected_eps:
        tool_class = ep.load()
        tool_instances.append(tool_class())

    # Log loaded tools
    for tool in tool_instances:
        logger.info(f"Loaded tool: {tool.get_name()}")

    return tool_instances


# Load tools when module is imported
all_tools = load_tools()
