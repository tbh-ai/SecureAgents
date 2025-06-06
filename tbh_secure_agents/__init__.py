# tbh_secure_agents - Secure Multi-Agent Framework by TBH.AI
# Author: Saish

import logging

__version__ = "0.4.1"

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

# Expose memory system components (NEW v5.0)
from .memory.memory_manager import MemoryManager
from .memory.models import MemoryEntry, MemoryType, MemoryPriority, MemoryAccess
from .memory.config import MemorySystemConfig, StorageConfig, SecurityConfig

# Expose terminal UI for direct use in applications
from .logging_config import get_terminal

__all__ = [
    'Expert',
    'Operation',
    'Squad',
    'SecurityValidator',
    'MemoryManager',
    'MemorySystemConfig',
    'MemoryEntry',
    'MemoryType',
    'MemoryPriority',
    'MemoryAccess',
    '__version__',
    'get_terminal'
]
