"""
TBH Secure Agents v5.0 - Memory System

This module provides comprehensive memory capabilities for the TBH Secure Agents framework,
enabling long-term and short-term memory for users while maintaining security-first principles.
"""

from .models import (
    MemoryEntry,
    MemoryType,
    MemoryPriority,
    MemoryAccess,
    MemoryMetadata,
    MemorySearchQuery,
    MemorySearchResult,
    MemoryOperationResult
)

from .interfaces import (
    MemoryStorageInterface,
    MemorySecurityInterface,
    MemoryIndexInterface,
    BaseMemoryStorage,
    BaseMemoryManager
)

from .memory_manager import MemoryManager

# Note: config module may not exist yet, importing conditionally
try:
    from .config import MemoryConfig
    HAS_CONFIG = True
except ImportError:
    MemoryConfig = None
    HAS_CONFIG = False

__version__ = "5.0.0"
__all__ = [
    # Models
    "MemoryEntry",
    "MemoryType", 
    "MemoryPriority",
    "MemoryAccess",
    "MemoryMetadata",
    "MemorySearchQuery",
    "MemorySearchResult",
    "MemoryOperationResult",
    
    # Core Manager
    "MemoryManager",
    
    # Interfaces
    "MemoryStorageInterface",
    "MemorySecurityInterface",
    "MemoryIndexInterface",
    "BaseMemoryStorage",
    "BaseMemoryManager",
    
    # Configuration (if available)
] + (["MemoryConfig"] if HAS_CONFIG else [])
