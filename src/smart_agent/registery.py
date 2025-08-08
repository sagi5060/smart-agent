from importlib.metadata import entry_points
from .logger import setup_logger

logger = setup_logger(__name__)

def load_tools():
    eps = entry_points()
    selected_eps = eps.select(group="smart_agent.tools")
    tool_instances = []
    for ep in selected_eps:
        tool_class = ep.load()
        tool_instances.append(tool_class())
    return tool_instances

all_tools = load_tools()
for tool in all_tools:
    logger.info(f"Loaded tool: {tool.get_name()}")