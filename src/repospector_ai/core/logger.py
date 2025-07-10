"""
Centralized logging configuration for RepoSpector AI.

This module provides structured logging with JSON formatting and configurable
log levels throughout the application.
"""

import logging
import sys
from typing import Any, Dict

from pythonjsonlogger import jsonlogger

from repospector_ai.core.config import settings


class StructuredFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging."""

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        """Add custom fields to log records."""
        super().add_fields(log_record, record, message_dict)
        
        # Add application context
        log_record["app_name"] = settings.app_name
        log_record["app_version"] = settings.app_version
        
        # Ensure timestamp is always present
        if "timestamp" not in log_record:
            log_record["timestamp"] = record.created
            
        # Add log level as string
        log_record["level"] = record.levelname


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Set up and configure a logger with structured output.
    
    Args:
        name: Logger name, typically __name__ from calling module
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Set log level
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Configure formatter based on settings
    if settings.log_format.lower() == "json":
        formatter = StructuredFormatter(
            fmt="%(timestamp)s %(level)s %(name)s %(message)s"
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


# Application-wide logger instance
logger = setup_logger("repospector_ai")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name, typically __name__
        
    Returns:
        Configured logger instance
    """
    return setup_logger(name)
