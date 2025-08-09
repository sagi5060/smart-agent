import json
import os
import platform
import sys
from importlib import metadata

import typer

from smart_agent.registry import load_tools

app = typer.Typer(add_completion=False, invoke_without_command=True)


@app.callback()
def callback(
    ctx: typer.Context, format: str = typer.Option("text", "--format", help="json|text")
):
    if ctx.invoked_subcommand is None:
        main(format=format)


def main(format: str = typer.Option("text", "--format", help="json|text")):
    data = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "package_version": metadata.version("smart-agent"),
        "env": {k: v for k, v in os.environ.items() if k.startswith("SMART_AGENT_")},
        "tools": [tool.get_name() for tool in load_tools()],
    }
    typer.echo(
        json.dumps(data, ensure_ascii=False, indent=None)
        if format == "json"
        else "\n".join(f"{k}: {v}" for k, v in data.items())
    )
