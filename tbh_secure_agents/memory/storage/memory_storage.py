"""
TBH Secure Agents v5.0 - In-Memory Storage Backend

Simple in-memory storage implementation for short-term memory needs.
Data is stored in memory and does not persist across sessions.
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from collections import defaultdict

from ..interfaces import MemoryStorageInterface
from ..models import (
    MemoryEntry, MemoryType, MemoryPriority, MemoryAccess,
    MemorySearchQuery, MemorySearchResult, MemoryOperationResult,
    MemoryMetadata
)
from ..config import MemorySystemConfig


logger = logging.getLogger(__name__)


class InMemoryStorage(MemoryStorageInterface):
    """
    In-memory storage implementation for short-term memory.
    
    Features:
    - Fast access with in-memory data structures
    - No persistence (data lost when process ends)
    - Simple implementation optimized for session-based memory
    - Thread-safe operations with async locks
    """
    
    def __init__(self, config: MemorySystemConfig):
        self.config = config
        self._storage: Dict[str, Dict[str, MemoryEntry]] = defaultdict(dict)
        self._metadata: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._locks: Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)
        self._initialized = False
        
        logger.info("InMemoryStorage initialized for short-term memory")
    
    async def initialize(self) -> None:
        """Initialize the in-memory storage"""
        if not self._initialized:
            self._initialized = True
            logger.info("InMemoryStorage initialization complete")
    
    async def store(self, entry: MemoryEntry, searchable_content: Optional[str] = None, searchable_tags: Optional[str] = None) -> MemoryOperationResult:
        """Store a memory entry in memory (searchable_content and searchable_tags are ignored for in-memory storage)"""
        try:
            user_id = entry.user_id
            key = entry.key
            
            async with self._locks[user_id]:
                # Check storage limits
                user_storage = self._storage[user_id]
                max_entries = self.config.limits.max_entries_per_user
                
                if len(user_storage) >= max_entries and key not in user_storage:
                    # Remove oldest entry to make room
                    oldest_key = min(user_storage.keys(), 
                                   key=lambda k: user_storage[k].created_at)
                    del user_storage[oldest_key]
                    logger.debug(f"Removed oldest entry {oldest_key} for user {user_id}")
                
                # Store the entry
                user_storage[key] = entry
                
                # Update metadata
                self._metadata[user_id][key] = {
                    'stored_at': datetime.now(timezone.utc),
                    'access_count': 0,
                    'last_accessed': None
                }
                
                logger.debug(f"Stored memory entry {key} for user {user_id}")
                
                return MemoryOperationResult(
                    success=True,
                    operation="store",
                    entry_key=key,
                    message=f"Memory entry stored successfully",
                    metadata={'storage_type': 'memory', 'user_id': user_id}
                )
                
        except Exception as e:
            logger.error(f"Failed to store memory entry: {e}")
            return MemoryOperationResult(
                success=False,
                operation="store",
                entry_key=entry.key,
                error=str(e),
                message="Failed to store memory entry"
            )
    
    async def retrieve(self, user_id: str, key: str, memory_type: MemoryType) -> Optional[MemoryEntry]:
        """Retrieve a specific memory entry"""
        try:
            async with self._locks[user_id]:
                user_storage = self._storage[user_id]
                entry = user_storage.get(key)
                
                if entry and entry.memory_type == memory_type:
                    # Update access metadata
                    if key in self._metadata[user_id]:
                        self._metadata[user_id][key]['access_count'] += 1
                        self._metadata[user_id][key]['last_accessed'] = datetime.now(timezone.utc)
                    
                    logger.debug(f"Retrieved memory entry {key} for user {user_id}")
                    return entry
                
                return None
                
        except Exception as e:
            logger.error(f"Failed to retrieve memory entry {key} for user {user_id}: {e}")
            return None
    
    async def search(self, query: MemorySearchQuery) -> MemorySearchResult:
        """Search memory entries based on query criteria"""
        try:
            user_id = query.user_id
            search_text = query.query.lower() if query.query else ""
            memory_types = query.memory_types or list(MemoryType)
            limit = min(query.limit or 50, 1000)  # Cap at 1000 results
            
            matching_entries = []
            
            async with self._locks[user_id]:
                user_storage = self._storage[user_id]
                
                for entry in user_storage.values():
                    # Check memory type filter
                    if entry.memory_type not in memory_types:
                        continue
                    
                    # Check expiration
                    if entry.expires_at and datetime.now(timezone.utc) > entry.expires_at:
                        continue
                    
                    # Text search in content and tags
                    content_match = search_text in entry.content.lower() if search_text else True
                    tag_match = any(search_text in tag.lower() for tag in entry.tags) if search_text and entry.tags else False
                    
                    if content_match or tag_match or not search_text:
                        matching_entries.append(entry)
                
                # Sort by relevance (created_at for now, could be improved)
                matching_entries.sort(key=lambda e: e.created_at, reverse=True)
                
                # Apply limit
                matching_entries = matching_entries[:limit]
                
                logger.debug(f"Found {len(matching_entries)} matching entries for user {user_id}")
                
                return MemorySearchResult(
                    entries=matching_entries,
                    total_count=len(matching_entries),
                    query=query,
                    execution_time=0.001,  # In-memory is very fast
                    metadata={'storage_type': 'memory'}
                )
                
        except Exception as e:
            logger.error(f"Failed to search memories for user {query.user_id}: {e}")
            return MemorySearchResult(
                entries=[],
                total_count=0,
                query=query,
                execution_time=0.0,
                error=str(e)
            )
    
    async def update(self, entry: MemoryEntry) -> MemoryOperationResult:
        """Update an existing memory entry"""
        try:
            user_id = entry.user_id
            key = entry.key
            
            async with self._locks[user_id]:
                user_storage = self._storage[user_id]
                
                if key in user_storage:
                    # Update the entry
                    entry.updated_at = datetime.now(timezone.utc)
                    user_storage[key] = entry
                    
                    logger.debug(f"Updated memory entry {key} for user {user_id}")
                    
                    return MemoryOperationResult(
                        success=True,
                        operation="update",
                        entry_key=key,
                        message="Memory entry updated successfully"
                    )
                else:
                    return MemoryOperationResult(
                        success=False,
                        operation="update",
                        entry_key=key,
                        message="Memory entry not found"
                    )
                    
        except Exception as e:
            logger.error(f"Failed to update memory entry {entry.key}: {e}")
            return MemoryOperationResult(
                success=False,
                operation="update",
                entry_key=entry.key,
                error=str(e)
            )
    
    async def delete(self, user_id: str, key: str, memory_type: MemoryType) -> MemoryOperationResult:
        """Delete a memory entry"""
        try:
            async with self._locks[user_id]:
                user_storage = self._storage[user_id]
                
                if key in user_storage and user_storage[key].memory_type == memory_type:
                    del user_storage[key]
                    if key in self._metadata[user_id]:
                        del self._metadata[user_id][key]
                    
                    logger.debug(f"Deleted memory entry {key} for user {user_id}")
                    
                    return MemoryOperationResult(
                        success=True,
                        operation="delete",
                        entry_key=key,
                        message="Memory entry deleted successfully"
                    )
                else:
                    return MemoryOperationResult(
                        success=False,
                        operation="delete",
                        entry_key=key,
                        message="Memory entry not found"
                    )
                    
        except Exception as e:
            logger.error(f"Failed to delete memory entry {key}: {e}")
            return MemoryOperationResult(
                success=False,
                operation="delete",
                entry_key=key,
                error=str(e)
            )
    
    async def cleanup_expired(self, user_id: Optional[str] = None) -> MemoryOperationResult:
        """Clean up expired memory entries"""
        try:
            current_time = datetime.now(timezone.utc)
            deleted_count = 0
            
            user_ids = [user_id] if user_id else list(self._storage.keys())
            
            for uid in user_ids:
                async with self._locks[uid]:
                    user_storage = self._storage[uid]
                    expired_keys = []
                    
                    for key, entry in user_storage.items():
                        if entry.expires_at and current_time > entry.expires_at:
                            expired_keys.append(key)
                    
                    for key in expired_keys:
                        del user_storage[key]
                        if key in self._metadata[uid]:
                            del self._metadata[uid][key]
                        deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} expired memory entries")
            
            return MemoryOperationResult(
                success=True,
                operation="cleanup",
                message=f"Cleaned up {deleted_count} expired entries",
                metadata={'deleted_count': deleted_count}
            )
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired entries: {e}")
            return MemoryOperationResult(
                success=False,
                operation="cleanup",
                error=str(e)
            )
    
    async def get_user_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get memory usage statistics for a user"""
        try:
            async with self._locks[user_id]:
                user_storage = self._storage[user_id]
                user_metadata = self._metadata[user_id]
                
                total_entries = len(user_storage)
                total_size = sum(len(entry.content.encode('utf-8')) for entry in user_storage.values())
                
                # Count by memory type
                type_counts = {}
                for entry in user_storage.values():
                    type_name = entry.memory_type.value
                    type_counts[type_name] = type_counts.get(type_name, 0) + 1
                
                # Count by priority
                priority_counts = {}
                for entry in user_storage.values():
                    priority_name = entry.priority.value
                    priority_counts[priority_name] = priority_counts.get(priority_name, 0) + 1
                
                return {
                    'user_id': user_id,
                    'total_entries': total_entries,
                    'total_size_bytes': total_size,
                    'storage_type': 'memory',
                    'entries_by_type': type_counts,
                    'entries_by_priority': priority_counts,
                    'max_entries': self.config.limits.max_entries_per_user,
                    'usage_percentage': (total_entries / self.config.limits.max_entries_per_user) * 100
                }
                
        except Exception as e:
            logger.error(f"Failed to get memory stats for user {user_id}: {e}")
            return {
                'user_id': user_id,
                'error': str(e)
            }
