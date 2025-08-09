from importlib import metadata

import typer

from smart_agent.cli.commands import info, query, run, tools
from smart_agent.logging_setup import configure_logging

app = typer.Typer(
    add_completion=False,
    help="SmartAgent – unified CLI",
)


@app.callback(invoke_without_command=True)
def _root(
    ctx: typer.Context,
    log_level: str = typer.Option(
        "INFO", "--log-level", metavar="LEVEL", help="DEBUG|INFO|WARNING|ERROR|CRITICAL"
    ),
    log_format: str = typer.Option(
        "color", "--log-format", metavar="FMT", help="color|json"
    ),
    journald: bool = typer.Option(
        False, "--journald", help="Send logs to systemd-journald (Linux)"
    ),
    version: bool = typer.Option(False, "--version", help="Print version and exit"),
):
    if version:
        try:
            typer.echo(metadata.version("smart-agent"))
        except Exception:
            typer.echo("0.0.0")
        raise typer.Exit(code=0)

    # Configure logging once at the root
    configure_logging(level=log_level, fmt=log_format, to_journald=journald)

    # If no subcommand was invoked, show help
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)


app.add_typer(query.app, name="query", help="One-shot query (text/file)")
# app.add_typer(chat.app,  name="chat",  help="Interactive chat session")
app.add_typer(info.app, name="info", help="Diagnostics & config")
app.add_typer(run.app, name="run", help="Run FastAPI server (OpenAPI)")
app.add_typer(tools.app, name="tools", help="List/describe available Tools")
