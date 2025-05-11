# tbh_secure_agents/logging_config.py
# Author: Saish (TBH.AI)

"""
Logging configuration for TBH Secure Agents framework.

This module provides a centralized configuration for logging
that integrates with the TerminalUI for polished output.
"""

import logging
import sys
from typing import Optional, Dict, Any
from .terminal_ui import TerminalUILogHandler, terminal

def configure_logging(level: int = logging.INFO, 
                     use_terminal_ui: bool = True,
                     log_to_file: bool = False,
                     log_file: Optional[str] = None) -> None:
    """
    Configure logging for the TBH Secure Agents framework.
    
    Args:
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG)
        use_terminal_ui (bool): Whether to use the TerminalUI for logging output
        log_to_file (bool): Whether to log to a file
        log_file (Optional[str]): The path to the log file (if log_to_file is True)
    """
    # Create a root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatters
    if use_terminal_ui:
        # Simple format for terminal UI (the UI adds its own formatting)
        terminal_format = logging.Formatter('%(message)s')
    else:
        # Standard format for regular console output
        terminal_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Detailed format for file logging
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s')
    
    # Add console handler
    if use_terminal_ui:
        console_handler = TerminalUILogHandler()
    else:
        console_handler = logging.StreamHandler(sys.stdout)
    
    console_handler.setFormatter(terminal_format)
    root_logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        if log_file is None:
            log_file = "tbh_secure_agents.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_format)
        root_logger.addHandler(file_handler)
    
    # Configure the framework's loggers
    framework_loggers = [
        logging.getLogger("tbh_secure_agents"),
        logging.getLogger("tbh_secure_agents.agent"),
        logging.getLogger("tbh_secure_agents.task"),
        logging.getLogger("tbh_secure_agents.crew"),
        logging.getLogger("tbh_secure_agents.security")
    ]
    
    for logger in framework_loggers:
        logger.setLevel(level)
        # Don't propagate to avoid duplicate logs
        logger.propagate = False
        
        # Add handlers directly to these loggers
        if use_terminal_ui:
            terminal_handler = TerminalUILogHandler()
            terminal_handler.setFormatter(terminal_format)
            logger.addHandler(terminal_handler)
        else:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(terminal_format)
            logger.addHandler(console_handler)
        
        if log_to_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)

def get_terminal() -> Any:
    """
    Get the global terminal UI instance.
    
    Returns:
        Any: The global terminal UI instance
    """
    return terminal
