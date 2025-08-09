"""
Simple logger configuration for the smart agent project.
"""

import logging


def set_global_log_level(level: str = "INFO") -> None:
    """
    Set the global logging level for the entire application.

    Args:
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,  # Override any existing configuration
    )


# Set default logging level
set_global_log_level("INFO")
