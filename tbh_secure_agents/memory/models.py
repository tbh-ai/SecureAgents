"""
TBH Secure Agents v5.0 - Memory System Data Models

This module defines the core data models for the memory system, including
memory entries, types, and metadata structures.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union
import uuid


class MemoryType(Enum):
    """Memory type classifications for TBH Secure Agents v5.0"""
    SESSION = "session"           # Short-term session memory
    LONG_TERM = "long_term"      # Persistent cross-session memory
    WORKING = "working"          # Task-specific active memory
    PATTERN = "pattern"          # Learned behavioral patterns
    PREFERENCE = "preference"    # User preferences and settings


class MemoryPriority(Enum):
    """Memory priority levels for retention and retrieval"""
    CRITICAL = "critical"        # Never expire, highest retrieval priority
    HIGH = "high"               # Long retention, high retrieval priority
    NORMAL = "normal"           # Standard retention and priority
    LOW = "low"                 # Short retention, lower priority
    TEMPORARY = "temporary"     # Very short retention


class MemoryAccess(Enum):
    """Memory access control levels"""
    PUBLIC = "public"           # Accessible to all agents for this user
    PRIVATE = "private"         # Accessible only to creating agent
    SHARED = "shared"           # Accessible to specific agents/operations
    SYSTEM = "system"           # System-level memories


@dataclass
class MemoryMetadata:
    """Metadata for memory entries"""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    creator_id: str = "system"
    tags: List[str] = field(default_factory=list)
    priority: MemoryPriority = MemoryPriority.NORMAL
    access_level: MemoryAccess = MemoryAccess.PRIVATE
    expires_at: Optional[datetime] = None
    security_validated: bool = False
    validation_timestamp: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary"""
        return {
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'accessed_at': self.accessed_at.isoformat(),
            'access_count': self.access_count,
            'creator_id': self.creator_id,
            'tags': self.tags,
            'priority': self.priority.value,
            'access_level': self.access_level.value,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'security_validated': self.security_validated,
            'validation_timestamp': self.validation_timestamp.isoformat() if self.validation_timestamp else None
        }


@dataclass
class MemoryEntry:
    """Core memory entry model for TBH Secure Agents v5.0"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    memory_type: MemoryType = MemoryType.SESSION
    key: str = ""
    value: Any = None
    content: str = ""  # String representation of value for storage
    content_hash: str = ""  # Hash of content for integrity checking
    tags: List[str] = field(default_factory=list)
    metadata: MemoryMetadata = field(default_factory=MemoryMetadata)
    version: int = 1
    is_encrypted: bool = False
    
    def __post_init__(self):
        """Post-initialization validation and setup"""
        if not self.user_id:
            raise ValueError("user_id is required for memory entries")
        if not self.key:
            raise ValueError("key is required for memory entries")
        
        # Auto-generate content and hash if not provided
        if not self.content and self.value is not None:
            import json
            import hashlib
            self.content = json.dumps(self.value, default=str)
            self.content_hash = hashlib.sha256(self.content.encode()).hexdigest()
        elif self.content and not self.content_hash:
            import hashlib
            self.content_hash = hashlib.sha256(self.content.encode()).hexdigest()
    
    def is_expired(self) -> bool:
        """Check if memory entry has expired"""
        if self.metadata.expires_at is None:
            return False
        return datetime.now() > self.metadata.expires_at
    
    def update_access(self):
        """Update access metadata when memory is accessed"""
        self.metadata.accessed_at = datetime.now()
        self.metadata.access_count += 1
    
    def set_ttl(self, seconds: int):
        """Set time-to-live for this memory entry"""
        self.metadata.expires_at = datetime.now() + timedelta(seconds=seconds)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory entry to dictionary for serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'memory_type': self.memory_type.value,
            'key': self.key,
            'value': self.value,
            'content': self.content,
            'content_hash': self.content_hash,
            'tags': self.tags,
            'version': self.version,
            'is_encrypted': self.is_encrypted,
            'metadata': {
                'created_at': self.metadata.created_at.isoformat(),
                'updated_at': self.metadata.updated_at.isoformat(),
                'accessed_at': self.metadata.accessed_at.isoformat(),
                'access_count': self.metadata.access_count,
                'creator_id': self.metadata.creator_id,
                'tags': self.metadata.tags,
                'priority': self.metadata.priority.value,
                'access_level': self.metadata.access_level.value,
                'expires_at': self.metadata.expires_at.isoformat() if self.metadata.expires_at else None,
                'security_validated': self.metadata.security_validated,
                'validation_timestamp': self.metadata.validation_timestamp.isoformat() if self.metadata.validation_timestamp else None
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create memory entry from dictionary"""
        metadata_data = data.get('metadata', {})
        metadata = MemoryMetadata(
            created_at=datetime.fromisoformat(metadata_data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(metadata_data.get('updated_at', datetime.now().isoformat())),
            accessed_at=datetime.fromisoformat(metadata_data.get('accessed_at', datetime.now().isoformat())),
            access_count=metadata_data.get('access_count', 0),
            creator_id=metadata_data.get('creator_id', 'system'),
            tags=metadata_data.get('tags', []),
            priority=MemoryPriority(metadata_data.get('priority', 'normal')),
            access_level=MemoryAccess(metadata_data.get('access_level', 'private')),
            expires_at=datetime.fromisoformat(metadata_data['expires_at']) if metadata_data.get('expires_at') else None,
            security_validated=metadata_data.get('security_validated', False),
            validation_timestamp=datetime.fromisoformat(metadata_data['validation_timestamp']) if metadata_data.get('validation_timestamp') else None
        )
        
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            user_id=data['user_id'],
            memory_type=MemoryType(data.get('memory_type', 'session')),
            key=data['key'],
            value=data.get('value'),
            content=data.get('content', ''),
            content_hash=data.get('content_hash', ''),
            tags=data.get('tags', []),
            version=data.get('version', 1),
            is_encrypted=data.get('is_encrypted', False),
            metadata=metadata
        )


@dataclass
class MemorySearchQuery:
    """Query model for memory search operations"""
    user_id: str
    query: Optional[str] = None
    memory_types: Optional[List[MemoryType]] = None  # Changed to None to search all types by default
    tags: List[str] = field(default_factory=list)
    limit: int = 10
    offset: int = 0
    include_expired: bool = False
    min_priority: MemoryPriority = MemoryPriority.LOW
    access_levels: List[MemoryAccess] = field(default_factory=lambda: [MemoryAccess.PUBLIC, MemoryAccess.PRIVATE])
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    content_pattern: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert search query to dictionary"""
        return {
            'user_id': self.user_id,
            'query': self.query,
            'memory_types': [mt.value for mt in self.memory_types] if self.memory_types else None,
            'tags': self.tags,
            'limit': self.limit,
            'offset': self.offset,
            'include_expired': self.include_expired,
            'min_priority': self.min_priority.value,
            'access_levels': [al.value for al in self.access_levels]
        }


@dataclass
class MemorySearchResult:
    """Result model for memory search operations"""
    entries: List[MemoryEntry] = field(default_factory=list)
    total_count: int = 0
    query_time_ms: float = 0.0
    has_more: bool = False
    query: Optional[str] = None  # Added query attribute
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert search result to dictionary"""
        return {
            'entries': [entry.to_dict() for entry in self.entries],
            'total_count': self.total_count,
            'query_time_ms': self.query_time_ms,
            'has_more': self.has_more,
            'query': self.query
        }


@dataclass
class MemoryOperationResult:
    """Result model for memory operations"""
    success: bool
    message: str = ""
    memory_id: Optional[str] = None
    affected_count: int = 0
    operation_time_ms: float = 0.0
    security_validated: bool = False
    operation: Optional[str] = None  # Added operation attribute
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert operation result to dictionary"""
        return {
            'success': self.success,
            'message': self.message,
            'memory_id': self.memory_id,
            'affected_count': self.affected_count,
            'operation_time_ms': self.operation_time_ms,
            'security_validated': self.security_validated,
            'operation': self.operation
        }
