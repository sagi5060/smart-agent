import typer
import uvicorn
from fastapi import FastAPI

from smart_agent.agent import SmartAgent

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
        response = await SmartAgent().run(text)
        return {"answer": response}

    return api


def main(
    host: str = typer.Option("0.0.0.0", "--host"),
    port: int = typer.Option(8000, "--port"),
    reload: bool = typer.Option(False, "--reload"),
    workers: int = typer.Option(1, "--workers"),
    log_level: str = typer.Option("info", "--log-level"),
):
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
