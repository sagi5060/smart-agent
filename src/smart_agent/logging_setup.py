import json
import logging
import sys

try:
    from systemd.journal import JournalHandler
except ImportError:
    JournalHandler = None


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "time": self.formatTime(record, self.datefmt),
                "name": record.name,
                "level": record.levelname,
                "message": record.getMessage(),
            }
        )


def configure_logging(
    level: str = "INFO", fmt: str = "color", to_journald: bool = False
) -> None:
    """Configure stdlib logging with optional journald and JSON format."""
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Clear and configure root logger
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(log_level)

    # Add journald handler if requested and available
    if to_journald and JournalHandler:
        try:
            jh = JournalHandler(SYSLOG_IDENTIFIER="smart-agent")
            jh.setLevel(log_level)
            root.addHandler(jh)
        except Exception:
            pass

    # Add console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(log_level)

    if fmt == "json":
        console.setFormatter(JsonFormatter())
    else:
        console.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        )

    root.addHandler(console)

    # Quiet noisy third-party loggers
    for name in ("urllib3", "botocore"):
        logging.getLogger(name).setLevel(max(log_level, logging.WARNING))
