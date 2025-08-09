import typer

from smart_agent.registry import load_tools

app = typer.Typer(add_completion=False)


@app.command("list")
def list_(
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Show detailed information"
    )
):
    """List all available tools."""
    tools = [tool.to_ollama_tool() for tool in load_tools()]
    if not tools:
        typer.echo("No tools found.")
        raise typer.Exit(0)

    if verbose:
        for i, tool in enumerate(tools):
            if i > 0:
                typer.echo()  # Empty line between tools
            _print_tool_detailed(tool)
    else:
        # Simple list format
        width = max(len(tool["function"]["name"]) for tool in tools)
        for tool in tools:
            name = tool["function"]["name"]
            description = tool["function"]["description"]
            typer.echo(f"{name.ljust(width)}  {description}")


@app.command("describe")
def describe(name: str):
    """Describe a specific tool in detail."""
    tools = [tool.to_ollama_tool() for tool in load_tools()]

    for tool in tools:
        if tool["function"]["name"] == name:
            _print_tool_detailed(tool)
            return

    typer.echo(f"Tool '{name}' not found", err=True)
    raise typer.Exit(1)


def _print_tool_detailed(tool: dict):
    """Print detailed information about a tool in a user-friendly format."""
    function = tool["function"]
    name = function["name"]
    description = function["description"]

    typer.echo(f"📋 {name}")
    typer.echo(f"   {description}")

    if "parameters" in function and function["parameters"]:
        parameters = function["parameters"]

        if "properties" in parameters and parameters["properties"]:
            typer.echo("   Parameters:")

            for param_name, param_info in parameters["properties"].items():
                param_type = param_info.get("type", "unknown")
                param_desc = param_info.get("description", "No description")
                required = param_name in parameters.get("required", [])

                # Format the parameter line
                req_symbol = "●" if required else "○"
                typer.echo(f"     {req_symbol} {param_name} ({param_type})")
                typer.echo(f"       {param_desc}")

                # Show additional constraints if available
                constraints = []
                if "enum" in param_info:
                    constraints.append(f"Options: {', '.join(param_info['enum'])}")
                if "minimum" in param_info:
                    constraints.append(f"Min: {param_info['minimum']}")
                if "maximum" in param_info:
                    constraints.append(f"Max: {param_info['maximum']}")
                if "default" in param_info:
                    constraints.append(f"Default: {param_info['default']}")

                if constraints:
                    typer.echo(f"       {' | '.join(constraints)}")
        else:
            typer.echo("   No parameters required")
    else:
        typer.echo("   No parameters required")
