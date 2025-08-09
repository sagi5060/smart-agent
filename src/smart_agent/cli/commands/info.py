import json
import os
import platform
import sys
from importlib import metadata

import typer

from smart_agent.ollama_health import (
    DEFAULT_MODEL,
    OllamaHealthError,
    check_ollama_service,
    get_available_models,
    validate_ollama_setup,
)
from smart_agent.registry import load_tools

app = typer.Typer(add_completion=False, invoke_without_command=True)


@app.command("health")
def health_check():
    """Check Ollama service and model availability."""
    try:
        validate_ollama_setup()
        typer.echo("Ollama health check passed", color=True)
        typer.echo("Service is running", color=True)
        typer.echo(f"Required model '{DEFAULT_MODEL}' is available", color=True)

        available_models = get_available_models()
        if len(available_models) > 1:
            other_models = [m for m in available_models if m != DEFAULT_MODEL]
            typer.echo(
                f"ℹ Other available models: {', '.join(other_models)}", color=True
            )

    except OllamaHealthError as e:
        typer.echo("Ollama health check failed:", err=True, color=True)
        typer.echo(str(e), err=True)
        raise typer.Exit(1) from e


@app.callback()
def callback(
    ctx: typer.Context, format: str = typer.Option("text", "--format", help="json|text")
):
    if ctx.invoked_subcommand is None:
        main(format=format)


def main(format: str = typer.Option("text", "--format", help="json|text")):
    # Gather Ollama information
    ollama_service_running = check_ollama_service()
    available_models = get_available_models() if ollama_service_running else []
    required_model_available = (
        DEFAULT_MODEL in available_models if ollama_service_running else False
    )

    ollama_status = (
        "healthy"
        if ollama_service_running and required_model_available
        else "unhealthy"
    )
    if not ollama_service_running:
        ollama_status = "service_not_running"
    elif not required_model_available:
        ollama_status = "model_not_available"

    data = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "package_version": metadata.version("smart-agent"),
        "env": {k: v for k, v in os.environ.items() if k.startswith("SMART_AGENT_")},
        "tools": [tool.get_name() for tool in load_tools()],
        "ollama": {
            "status": ollama_status,
            "service_running": ollama_service_running,
            "required_model": DEFAULT_MODEL,
            "required_model_available": required_model_available,
            "available_models": available_models,
        },
    }
    typer.echo(
        json.dumps(data, ensure_ascii=False, indent=None)
        if format == "json"
        else "\n".join(f"{k}: {v}" for k, v in data.items())
    )
