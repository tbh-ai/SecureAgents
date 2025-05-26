# tbh_secure_agents - Secure Multi-Agent Framework by TBH.AI
# Author: Saish

import logging

__version__ = "0.4.0"

# Import logging configuration
from .logging_config import configure_logging

# Configure logging with the terminal UI
configure_logging(level=logging.INFO, use_terminal_ui=True)

# Expose core classes
from .expert import Expert
from .operation import Operation
from .squad import Squad

# Expose security validation components (lean and mean)
from .security_validation import SecurityValidator

# Expose terminal UI for direct use in applications
from .logging_config import get_terminal

__all__ = [
    'Expert',
    'Operation',
    'Squad',
    'SecurityValidator',
    '__version__',
    'get_terminal'
]
