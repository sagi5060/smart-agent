import typer
import uvicorn
from fastapi import FastAPI, HTTPException

from smart_agent.agent import SmartAgent
from smart_agent.ollama_health import OllamaHealthError, validate_ollama_setup

app = typer.Typer(add_completion=False, invoke_without_command=True)


@app.callback()
def callback(
    ctx: typer.Context,
    host: str = typer.Option("0.0.0.0", "--host"),
    port: int = typer.Option(8000, "--port"),
    reload: bool = typer.Option(False, "--reload"),
    workers: int = typer.Option(1, "--workers"),
    log_level: str = typer.Option("info", "--log-level"),
):
    if ctx.invoked_subcommand is None:
        main(host=host, port=port, reload=reload, workers=workers, log_level=log_level)


def build_app() -> FastAPI:
    api = FastAPI(title="SmartAgent API")

    @api.get("/healthz")
    async def healthz():
        return {"status": "ok"}

    @api.post("/answer")
    async def answer(query: dict):
        # Replace with actual smart agent logic
        text = query.get("query", "")
        try:
            response = await SmartAgent().run(text)
            return {"answer": response}
        except OllamaHealthError as e:
            raise HTTPException(status_code=503, detail=str(e)) from e

    return api


def main(
    host: str = typer.Option("0.0.0.0", "--host"),
    port: int = typer.Option(8000, "--port"),
    reload: bool = typer.Option(False, "--reload"),
    workers: int = typer.Option(1, "--workers"),
    log_level: str = typer.Option("info", "--log-level"),
):
    # Check Ollama health before starting the server
    try:
        validate_ollama_setup()
        typer.echo("Ollama health check passed")
    except OllamaHealthError as e:
        typer.echo(f"Ollama health check failed: {e}", err=True)
        raise typer.Exit(1) from e

    # Logging is configured at root via CLI callback; emit a startup message
    uvicorn.run(
        "smart_agent.cli.commands.run:build_app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_level=log_level.lower(),
        factory=True,
    )
