"""
TBH Secure Agents v5.0 - Memory Storage Backends

This module provides various storage backend implementations for the 
memory system, supporting different deployment scenarios and performance requirements.
"""

from .sqlite_storage import SQLiteMemoryStorage
from .memory_storage import InMemoryStorage
from .chroma_storage import ChromaMemoryStorage

__all__ = [
    'SQLiteMemoryStorage',
    'InMemoryStorage',
    'ChromaMemoryStorage',
]

# Storage backend registry for dynamic loading
STORAGE_BACKENDS = {
    'sqlite': SQLiteMemoryStorage,
    'memory': InMemoryStorage,
    'chroma': ChromaMemoryStorage,
    # Future backends will be added here:
    # 'postgresql': PostgreSQLMemoryStorage,
    # 'redis': RedisMemoryStorage,
    # 'hybrid': HybridMemoryStorage,
}


def get_storage_backend(backend_name: str):
    """
    Get a storage backend class by name.
    
    Args:
        backend_name: Name of the storage backend
        
    Returns:
        Storage backend class
        
    Raises:
        ValueError: If backend is not found
    """
    backend_class = STORAGE_BACKENDS.get(backend_name.lower())
    if not backend_class:
        available = ', '.join(STORAGE_BACKENDS.keys())
        raise ValueError(f"Storage backend '{backend_name}' not found. Available: {available}")
    
    return backend_class
