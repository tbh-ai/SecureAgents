# tbh_secure_agents - Secure Multi-Agent Framework by TBH.AI
# Author: Saish

import logging

__version__ = "0.3.0"

# Import logging configuration
from .logging_config import configure_logging

# Configure logging with the terminal UI
configure_logging(level=logging.INFO, use_terminal_ui=True)

# Expose core classes
from .agent import Expert
from .task import Operation
from .crew import Squad

# Expose terminal UI for direct use in applications
from .logging_config import get_terminal

__all__ = ['Expert', 'Operation', 'Squad', '__version__', 'get_terminal']
