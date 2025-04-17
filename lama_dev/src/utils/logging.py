"""
src/utils/logging.py: Configures logging for the text-to-SQL application.
- Sets up a logger with the specified level from config.py.
"""

import logging
from src.config.config import CONFIG

def setup_logging(name: str) -> logging.Logger:
    """Set up and return a logger with the specified name."""
    logging.basicConfig(level=getattr(logging, CONFIG["log_level"]))
    return logging.getLogger(name)