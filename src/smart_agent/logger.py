"""
Simple logger configuration for the smart agent project.
"""

import logging
import sys
from typing import Optional

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with console output.
    
    Args:
        name (str): Name of the logger (usually __name__)
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    # Set level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

# Default logger for the smart_agent package
default_logger = setup_logger("smart_agent")
