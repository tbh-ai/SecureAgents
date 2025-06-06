"""
TBH Secure Agents v5.0 - Memory System Interfaces

This module defines the core interfaces and abstract base classes for the 
memory system, ensuring consistent contract across all implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
from datetime import datetime

from .models import (
    MemoryEntry, MemoryType, MemoryPriority, MemoryAccess,
    MemorySearchQuery, MemorySearchResult, MemoryOperationResult
)


@runtime_checkable
class MemoryStorageInterface(Protocol):
    """Protocol defining the interface for memory storage backends"""
    
    async def store(self, entry: MemoryEntry) -> MemoryOperationResult:
        """Store a memory entry"""
        ...
    
    async def retrieve(self, user_id: str, key: str, memory_type: MemoryType) -> Optional[MemoryEntry]:
        """Retrieve a specific memory entry"""
        ...
    
    async def search(self, query: MemorySearchQuery) -> MemorySearchResult:
        """Search memory entries based on query criteria"""
        ...
    
    async def update(self, entry: MemoryEntry) -> MemoryOperationResult:
        """Update an existing memory entry"""
        ...
    
    async def delete(self, user_id: str, key: str, memory_type: MemoryType) -> MemoryOperationResult:
        """Delete a memory entry"""
        ...
    
    async def cleanup_expired(self, user_id: Optional[str] = None) -> MemoryOperationResult:
        """Clean up expired memory entries"""
        ...
    
    async def get_user_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get memory usage statistics for a user"""
        ...


@runtime_checkable
class MemorySecurityInterface(Protocol):
    """Protocol for memory security validation"""
    
    async def validate_memory_operation(
        self, 
        operation: str, 
        entry: MemoryEntry, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Validate memory operation through security layers"""
        ...
    
    async def validate_memory_access(
        self, 
        user_id: str, 
        entry: MemoryEntry,
        access_type: str = "read"
    ) -> bool:
        """Validate access to memory entry"""
        ...
    
    async def scan_memory_content(self, content: Any) -> Dict[str, Any]:
        """Scan memory content for security threats"""
        ...


@runtime_checkable
class MemoryIndexInterface(Protocol):
    """Protocol for memory indexing and search optimization"""
    
    async def index_entry(self, entry: MemoryEntry) -> bool:
        """Add entry to search index"""
        ...
    
    async def remove_from_index(self, entry_id: str) -> bool:
        """Remove entry from search index"""
        ...
    
    async def semantic_search(
        self, 
        user_id: str, 
        query: str, 
        limit: int = 10
    ) -> List[MemoryEntry]:
        """Perform semantic search on memory entries"""
        ...
    
    async def rebuild_index(self, user_id: Optional[str] = None) -> bool:
        """Rebuild search index"""
        ...


class BaseMemoryStorage(ABC):
    """Abstract base class for memory storage implementations"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the storage backend"""
        pass
    
    @abstractmethod
    async def close(self) -> bool:
        """Close and cleanup storage backend"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check storage backend health"""
        pass
    
    @abstractmethod
    async def store(self, entry: MemoryEntry) -> MemoryOperationResult:
        """Store a memory entry"""
        pass
    
    @abstractmethod
    async def retrieve(self, user_id: str, key: str, memory_type: MemoryType) -> Optional[MemoryEntry]:
        """Retrieve a specific memory entry"""
        pass
    
    @abstractmethod
    async def search(self, query: MemorySearchQuery) -> MemorySearchResult:
        """Search memory entries based on query criteria"""
        pass
    
    @abstractmethod
    async def update(self, entry: MemoryEntry) -> MemoryOperationResult:
        """Update an existing memory entry"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: str, key: str, memory_type: MemoryType) -> MemoryOperationResult:
        """Delete a memory entry"""
        pass
    
    @abstractmethod
    async def cleanup_expired(self, user_id: Optional[str] = None) -> MemoryOperationResult:
        """Clean up expired memory entries"""
        pass
    
    @abstractmethod
    async def get_user_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get memory usage statistics for a user"""
        pass
    
    async def bulk_store(self, entries: List[MemoryEntry]) -> MemoryOperationResult:
        """Store multiple memory entries (default implementation)"""
        success_count = 0
        total_time = 0.0
        
        for entry in entries:
            result = await self.store(entry)
            if result.success:
                success_count += 1
            total_time += result.operation_time_ms
        
        return MemoryOperationResult(
            success=success_count == len(entries),
            message=f"Stored {success_count}/{len(entries)} entries",
            affected_count=success_count,
            operation_time_ms=total_time
        )
    
    async def bulk_delete(self, entries: List[tuple]) -> MemoryOperationResult:
        """Delete multiple memory entries (default implementation)"""
        success_count = 0
        total_time = 0.0
        
        for user_id, key, memory_type in entries:
            result = await self.delete(user_id, key, memory_type)
            if result.success:
                success_count += 1
            total_time += result.operation_time_ms
        
        return MemoryOperationResult(
            success=success_count == len(entries),
            message=f"Deleted {success_count}/{len(entries)} entries",
            affected_count=success_count,
            operation_time_ms=total_time
        )


class BaseMemoryManager(ABC):
    """Abstract base class for memory managers"""
    
    def __init__(
        self, 
        storage: MemoryStorageInterface,
        security: Optional[MemorySecurityInterface] = None,
        indexer: Optional[MemoryIndexInterface] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.storage = storage
        self.security = security
        self.indexer = indexer
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the memory manager"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the memory manager"""
        pass
    
    async def _validate_security(
        self, 
        operation: str, 
        entry: MemoryEntry, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Internal security validation helper"""
        if self.security is None:
            return {
                'valid': True,
                'confidence': 1.0,
                'message': 'No security validation configured',
                'validation_time_ms': 0.0
            }
        
        return await self.security.validate_memory_operation(operation, entry, context)
    
    async def _index_entry(self, entry: MemoryEntry) -> bool:
        """Internal indexing helper"""
        if self.indexer is None:
            return True
        
        return await self.indexer.index_entry(entry)
    
    async def _remove_from_index(self, entry_id: str) -> bool:
        """Internal index removal helper"""
        if self.indexer is None:
            return True
        
        return await self.indexer.remove_from_index(entry_id)


class BaseMemoryIndex(ABC):
    """Abstract base class for memory indexing implementations"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the indexing system"""
        pass
    
    @abstractmethod
    async def close(self) -> bool:
        """Close and cleanup indexing system"""
        pass
    
    @abstractmethod
    async def index_entry(self, entry: MemoryEntry) -> bool:
        """Add entry to search index"""
        pass
    
    @abstractmethod
    async def remove_from_index(self, entry_id: str) -> bool:
        """Remove entry from search index"""
        pass
    
    @abstractmethod
    async def semantic_search(
        self, 
        user_id: str, 
        query: str, 
        limit: int = 10
    ) -> List[MemoryEntry]:
        """Perform semantic search on memory entries"""
        pass
    
    @abstractmethod
    async def rebuild_index(self, user_id: Optional[str] = None) -> bool:
        """Rebuild search index"""
        pass
    
    async def bulk_index(self, entries: List[MemoryEntry]) -> Dict[str, Any]:
        """Index multiple entries (default implementation)"""
        success_count = 0
        start_time = datetime.now()
        
        for entry in entries:
            if await self.index_entry(entry):
                success_count += 1
        
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            'success': success_count == len(entries),
            'indexed_count': success_count,
            'total_count': len(entries),
            'elapsed_ms': elapsed_ms
        }


class MemoryException(Exception):
    """Base exception for memory system errors"""
    pass


class MemoryValidationError(MemoryException):
    """Exception for memory validation errors"""
    pass


class MemorySecurityError(MemoryException):
    """Exception for memory security errors"""
    pass


class MemoryStorageError(MemoryException):
    """Exception for memory storage errors"""
    pass


class MemoryIndexError(MemoryException):
    """Exception for memory indexing errors"""
    pass
