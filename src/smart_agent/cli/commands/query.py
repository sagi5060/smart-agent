import asyncio
import json
import logging

import typer

from smart_agent.agent import SmartAgent

app = typer.Typer(add_completion=False, invoke_without_command=True)


@app.callback()
def callback(
    ctx: typer.Context,
    text: str | None = typer.Option(
        None, "--text", help="Inline text; use '-' for stdin"
    ),
    format: str = typer.Option("text", "--format", help="json|text"),
    timeout: float = typer.Option(30.0, "--timeout", min=0.1),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    if ctx.invoked_subcommand is None:
        main(text=text, format=format, timeout=timeout, verbose=verbose)


def main(
    text: str | None = typer.Option(
        None, "--text", help="Inline text; use '-' for stdin"
    ),
    format: str = typer.Option("text", "--format", help="json|text"),
    timeout: float = typer.Option(30.0, "--timeout", min=0.1),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Run a single query through SmartAgent and print the result."""
    log = logging.getLogger(__name__)
    if verbose:
        log.debug("verbose mode enabled")
    query = text
    if not query:
        typer.echo(
            "insert your query and press Ctrl+D to submit",
            err=False,
            color=True,
        )
        query = typer.get_text_stream("stdin").read()

    async def _run():
        agent = SmartAgent()
        resp = await agent.run(query)
        return resp.to_dict() if hasattr(resp, "to_dict") else str(resp)

    try:
        result = asyncio.run(asyncio.wait_for(_run(), timeout=timeout))
        out = {"status": "success", "response": result}
        log.info("query completed", extra={"format": format, "timeout": timeout})
        typer.echo(
            json.dumps(out, ensure_ascii=False)
            if format == "json"
            else str(out["response"])
        )
    except asyncio.TimeoutError:
        err = {"status": "error", "error": "timeout"}
        log.warning("query timeout", extra={"timeout": timeout})
        typer.echo(
            json.dumps(err, ensure_ascii=False) if format == "json" else "timeout",
            err=(format != "json"),
        )
        raise typer.Exit(1) from None
    except Exception as e:
        err = {"status": "error", "error": str(e)}
        log.exception("query failed")
        typer.echo(
            json.dumps(err, ensure_ascii=False) if format == "json" else f"Error: {e}",
            err=True,
        )
        raise typer.Exit(1) from e
