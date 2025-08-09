import typer

from smart_agent.cli.commands import info, query, run, tools

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,  # נוסיף completion בשלב מאוחר יותר
    help="SmartAgent – unified CLI",
)

app.add_typer(query.app, name="query", help="One-shot query (text/file)")
# app.add_typer(chat.app,  name="chat",  help="Interactive chat session")
app.add_typer(info.app, name="info", help="Diagnostics & config")
app.add_typer(run.app, name="run", help="Run FastAPI server (OpenAPI)")
app.add_typer(tools.app, name="tools", help="List/describe available Tools")
