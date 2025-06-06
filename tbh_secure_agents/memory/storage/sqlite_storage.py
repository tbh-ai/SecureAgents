"""
TBH Secure Agents v5.0 - SQLite Memory Storage Backend

High-performance SQLite implementation with async support, optimized for
the TBH Secure Agents memory system. Provides ACID transactions, efficient
indexing, and comprehensive error handling.
"""

import asyncio
import aiosqlite
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from contextlib import asynccontextmanager

from ..interfaces import MemoryStorageInterface
from ..models import (
    MemoryEntry, MemoryType, MemoryPriority, MemoryAccess,
    MemorySearchQuery, MemorySearchResult, MemoryOperationResult,
    MemoryMetadata
)
from ..config import MemorySystemConfig


logger = logging.getLogger(__name__)


class SQLiteMemoryStorage(MemoryStorageInterface):
    """
    SQLite-based memory storage implementation with async support.
    
    Features:
    - Async operations with connection pooling
    - ACID transactions for data integrity
    - Optimized indexing for fast retrieval
    - Full-text search capabilities
    - Automatic schema migration
    - Comprehensive error handling
    """
    
    def __init__(self, config: MemorySystemConfig):
        self.config = config
        self.db_path = config.storage.sqlite_path
        self._connection_pool: Optional[aiosqlite.Connection] = None
        self._initialized = False
        self._lock = asyncio.Lock()
        
        # Ensure database directory exists
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    async def initialize(self) -> None:
        """Initialize the SQLite database and create tables"""
        async with self._lock:
            if self._initialized:
                return
            
            try:
                # Create database and tables
                await self._create_tables()
                await self._create_indexes()
                await self._enable_wal_mode()
                
                self._initialized = True
                logger.info(f"SQLite memory storage initialized at {self.db_path}")
                
            except Exception as e:
                logger.error(f"Failed to initialize SQLite storage: {e}")
                raise
    
    async def _create_tables(self) -> None:
        """Create the memory storage tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Main memory entries table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    access_level TEXT NOT NULL,
                    content TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    tags TEXT,  -- JSON array
                    metadata TEXT,  -- JSON object
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    accessed_at TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP,
                    version INTEGER DEFAULT 1,
                    is_encrypted BOOLEAN DEFAULT FALSE,
                    searchable_content TEXT,  -- Unencrypted searchable content
                    searchable_tags TEXT,     -- Unencrypted searchable tags
                    
                    UNIQUE(user_id, key, memory_type)
                )
            """)
            
            # Memory access log for analytics and security
            await db.execute("""
                CREATE TABLE IF NOT EXISTS memory_access_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    memory_key TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    action TEXT NOT NULL,  -- CREATE, READ, UPDATE, DELETE
                    timestamp TIMESTAMP NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    success BOOLEAN NOT NULL DEFAULT TRUE,
                    error_message TEXT
                )
            """)
            
            # Memory statistics table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS memory_stats (
                    user_id TEXT PRIMARY KEY,
                    total_entries INTEGER DEFAULT 0,
                    total_size_bytes INTEGER DEFAULT 0,
                    last_activity TIMESTAMP,
                    created_entries_today INTEGER DEFAULT 0,
                    last_cleanup TIMESTAMP
                )
            """)
            
            await db.commit()
    
    async def _create_indexes(self) -> None:
        """Create performance-optimized indexes"""
        async with aiosqlite.connect(self.db_path) as db:
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_user_type ON memory_entries(user_id, memory_type)",
                "CREATE INDEX IF NOT EXISTS idx_user_key ON memory_entries(user_id, key)",
                "CREATE INDEX IF NOT EXISTS idx_created_at ON memory_entries(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_updated_at ON memory_entries(updated_at)",
                "CREATE INDEX IF NOT EXISTS idx_expires_at ON memory_entries(expires_at)",
                "CREATE INDEX IF NOT EXISTS idx_priority ON memory_entries(priority)",
                "CREATE INDEX IF NOT EXISTS idx_tags ON memory_entries(tags)",
                "CREATE INDEX IF NOT EXISTS idx_access_log_user ON memory_access_log(user_id, timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_content_hash ON memory_entries(content_hash)"
            ]
            
            for index_sql in indexes:
                await db.execute(index_sql)
            
            # Create full-text search index for searchable content only
            await db.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                    user_id, key, searchable_content, searchable_tags,
                    content='memory_entries',
                    content_rowid='id'
                )
            """)
            
            # Create FTS triggers for automatic sync with searchable content
            await db.execute("""
                CREATE TRIGGER IF NOT EXISTS memory_fts_insert AFTER INSERT ON memory_entries BEGIN
                    INSERT INTO memory_fts(rowid, user_id, key, searchable_content, searchable_tags)
                    VALUES (new.id, new.user_id, new.key, new.searchable_content, new.searchable_tags);
                END
            """)
            
            await db.execute("""
                CREATE TRIGGER IF NOT EXISTS memory_fts_delete AFTER DELETE ON memory_entries BEGIN
                    DELETE FROM memory_fts WHERE rowid = old.id;
                END
            """)
            
            await db.execute("""
                CREATE TRIGGER IF NOT EXISTS memory_fts_update AFTER UPDATE ON memory_entries BEGIN
                    DELETE FROM memory_fts WHERE rowid = old.id;
                    INSERT INTO memory_fts(rowid, user_id, key, searchable_content, searchable_tags)
                    VALUES (new.id, new.user_id, new.key, new.searchable_content, new.searchable_tags);
                END
            """)
            
            await db.commit()
    
    async def _enable_wal_mode(self) -> None:
        """Enable WAL mode for better concurrent access"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA journal_mode=WAL")
            await db.execute("PRAGMA synchronous=NORMAL")
            await db.execute("PRAGMA cache_size=10000")
            await db.execute("PRAGMA temp_store=MEMORY")
            await db.commit()
    
    @asynccontextmanager
    async def _get_connection(self):
        """Get a database connection with proper error handling"""
        if not self._initialized:
            await self.initialize()
        
        try:
            conn = await aiosqlite.connect(self.db_path)
            conn.row_factory = aiosqlite.Row
            yield conn
        finally:
            await conn.close()
    
    def _extract_searchable_content(self, content: str, tags: Optional[List[str]] = None) -> Tuple[str, str]:
        """Extract searchable content from memory content.
        
        Args:
            content: The original content (may be encrypted)
            tags: Optional tags
            
        Returns:
            Tuple of (searchable_content, searchable_tags)
        """
        # For encrypted content, extract keywords before encryption
        # This is a simple keyword extraction - in production, you might want
        # more sophisticated NLP techniques
        
        if not content or len(content.strip()) == 0:
            return "", ""
        
        # Simple keyword extraction (first 200 characters for searchability)
        # Remove sensitive patterns and keep only general terms
        import re
        
        # Extract meaningful words (3+ characters, alphanumeric)
        words = re.findall(r'\b[a-zA-Z0-9]{3,}\b', content.lower())
        
        # Take first 50 words for searchability (limit to prevent bloat)
        searchable_words = words[:50]
        searchable_content = " ".join(searchable_words)
        
        # Prepare searchable tags
        searchable_tags = " ".join(tags) if tags else ""
        
        return searchable_content[:500], searchable_tags[:200]  # Limit lengths
    
    async def store(self, entry: MemoryEntry, searchable_content: Optional[str] = None, searchable_tags: Optional[str] = None) -> MemoryOperationResult:
        """Store a memory entry in SQLite with optional pre-extracted searchable content"""
        try:
            async with self._get_connection() as db:
                # Prepare data for storage
                tags_json = json.dumps(entry.tags) if entry.tags else None
                metadata_json = json.dumps(entry.metadata.to_dict()) if entry.metadata else None
                
                # Use provided searchable content or extract from entry (fallback for backward compatibility)
                # Only extract if BOTH searchable_content AND searchable_tags are None
                print(f"DEBUG STORAGE: Received searchable_content: '{(searchable_content or '')[:100]}...'")
                print(f"DEBUG STORAGE: Received searchable_tags: '{(searchable_tags or '')[:100]}...'")
                print(f"DEBUG STORAGE: Entry content: '{entry.content[:100]}...'")
                
                if searchable_content is None and searchable_tags is None:
                    print("DEBUG STORAGE: Both searchable_content and searchable_tags are None - extracting from entry content")
                    searchable_content, searchable_tags = self._extract_searchable_content(
                        entry.content, entry.tags
                    )
                    print(f"DEBUG STORAGE: Extracted searchable_content: '{searchable_content[:100]}...'")
                else:
                    print("DEBUG STORAGE: Using provided searchable content (not extracting from encrypted content)")
                    # Use provided values, but set defaults for None values to avoid fallback
                    if searchable_content is None:
                        searchable_content = ""
                    if searchable_tags is None:
                        searchable_tags = ""
                
                # Insert or replace the entry
                await db.execute("""
                    INSERT OR REPLACE INTO memory_entries 
                    (user_id, key, memory_type, priority, access_level, content, 
                     content_hash, tags, metadata, created_at, updated_at, 
                     accessed_at, expires_at, version, is_encrypted, 
                     searchable_content, searchable_tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    entry.user_id,
                    entry.key,
                    entry.memory_type.value,
                    entry.metadata.priority.value,
                    entry.metadata.access_level.value,
                    entry.content,
                    entry.content_hash,
                    tags_json,
                    metadata_json,
                    entry.metadata.created_at.isoformat(),
                    entry.metadata.updated_at.isoformat(),
                    entry.metadata.accessed_at.isoformat(),
                    entry.metadata.expires_at.isoformat() if entry.metadata.expires_at else None,
                    entry.version,
                    entry.is_encrypted,
                    searchable_content,
                    searchable_tags
                ))
                
                # Log the access
                await self._log_access(db, entry.user_id, entry.key, 
                                     entry.memory_type.value, "CREATE")
                
                # Update user statistics
                await self._update_user_stats(db, entry.user_id, 1, len(entry.content))
                
                await db.commit()
                
                return MemoryOperationResult(
                    success=True,
                    message="Memory entry stored successfully",
                    affected_count=1
                )
                
        except Exception as e:
            logger.error(f"Failed to store memory entry: {e}")
            return MemoryOperationResult(
                success=False,
                message=f"Storage failed: {str(e)}"
            )
    
    async def retrieve(self, user_id: str, key: str, memory_type: MemoryType) -> Optional[MemoryEntry]:
        """Retrieve a specific memory entry"""
        try:
            async with self._get_connection() as db:
                cursor = await db.execute("""
                    SELECT * FROM memory_entries 
                    WHERE user_id = ? AND key = ? AND memory_type = ?
                    AND (expires_at IS NULL OR expires_at > ?)
                """, (user_id, key, memory_type.value, datetime.now(timezone.utc).isoformat()))
                
                row = await cursor.fetchone()
                if not row:
                    return None
                
                # Update accessed_at timestamp
                await db.execute("""
                    UPDATE memory_entries 
                    SET accessed_at = ? 
                    WHERE user_id = ? AND key = ? AND memory_type = ?
                """, (datetime.now(timezone.utc).isoformat(), user_id, key, memory_type.value))
                
                # Log the access
                await self._log_access(db, user_id, key, memory_type.value, "READ")
                
                await db.commit()
                
                return self._row_to_memory_entry(row)
                
        except Exception as e:
            logger.error(f"Failed to retrieve memory entry: {e}")
            return None
    
    async def search(self, query: MemorySearchQuery) -> MemorySearchResult:
        """Search memory entries based on query criteria"""
        start_time = datetime.now()
        try:
            async with self._get_connection() as db:
                # Build the SQL query
                sql_parts = ["SELECT * FROM memory_entries WHERE 1=1"]
                params = []
                
                # User filter
                if query.user_id:
                    sql_parts.append("AND user_id = ?")
                    params.append(query.user_id)
                
                # Memory type filter
                if query.memory_types:
                    placeholders = ",".join("?" * len(query.memory_types))
                    sql_parts.append(f"AND memory_type IN ({placeholders})")
                    params.extend([mt.value for mt in query.memory_types])
                
                # Priority filter
                if query.min_priority:
                    priority_values = self._get_priority_values_above(query.min_priority)
                    placeholders = ",".join("?" * len(priority_values))
                    sql_parts.append(f"AND priority IN ({placeholders})")
                    params.extend(priority_values)
                
                # Date range filters
                if query.created_after:
                    sql_parts.append("AND created_at > ?")
                    params.append(query.created_after.isoformat())
                
                if query.created_before:
                    sql_parts.append("AND created_at < ?")
                    params.append(query.created_before.isoformat())
                
                # Tags filter
                if query.tags:
                    for tag in query.tags:
                        sql_parts.append("AND tags LIKE ?")
                        params.append(f'%"{tag}"%')
                
                # Content search using FTS on searchable content only
                if query.content_pattern:
                    # Use FTS for searchable content search
                    fts_sql = """
                        SELECT memory_entries.* FROM memory_entries
                        JOIN memory_fts ON memory_entries.id = memory_fts.rowid
                        WHERE memory_fts MATCH ?
                    """
                    if len(sql_parts) > 1:
                        # Combine with other filters by removing "AND" from beginning of each condition
                        where_conditions = []
                        for part in sql_parts[1:]:  # Skip "SELECT * FROM memory_entries WHERE 1=1"
                            condition = part.strip()
                            if condition.startswith("AND "):
                                condition = condition[4:]  # Remove "AND " prefix
                            where_conditions.append(condition)
                        
                        combined_sql = f"""
                            SELECT * FROM ({fts_sql}) AS fts_results
                            WHERE {' AND '.join(where_conditions)}
                        """
                        params = [query.content_pattern] + params
                    else:
                        combined_sql = fts_sql
                        params = [query.content_pattern]
                    
                    sql_parts = [combined_sql]
                
                # Exclude expired entries
                sql_parts.append("AND (expires_at IS NULL OR expires_at > ?)")
                params.append(datetime.now(timezone.utc).isoformat())
                
                # Ordering
                sql_parts.append("ORDER BY updated_at DESC")
                
                # Limit
                if query.limit:
                    sql_parts.append("LIMIT ?")
                    params.append(query.limit)
                
                # Execute query
                sql = " ".join(sql_parts)
                print(f"DEBUG STORAGE: Executing SQL: {sql}")
                print(f"DEBUG STORAGE: With parameters: {params}")
                cursor = await db.execute(sql, params)
                rows = await cursor.fetchall()
                print(f"DEBUG STORAGE: SQL returned {len(rows)} rows")
                
                # Convert rows to memory entries
                entries = [self._row_to_memory_entry(row) for row in rows]
                
                return MemorySearchResult(
                    entries=entries,
                    total_count=len(entries),
                    query_time_ms=(datetime.now() - start_time).total_seconds() * 1000
                )
                
        except Exception as e:
            logger.error(f"Failed to search memory entries: {e}")
            return MemorySearchResult(
                entries=[],
                total_count=0,
                query_time_ms=0.0
            )
    
    async def update(self, entry: MemoryEntry) -> MemoryOperationResult:
        """Update an existing memory entry"""
        try:
            # First check if entry exists
            existing = await self.retrieve(entry.user_id, entry.key, entry.memory_type)
            if not existing:
                return MemoryOperationResult(
                    success=False,
                    message="Memory entry not found for update"
                )
            
            # Update the entry (store handles INSERT OR REPLACE)
            entry.version = existing.version + 1
            entry.updated_at = datetime.now(timezone.utc)
            
            result = await self.store(entry)
            if result.success:
                result.message = "Memory entry updated successfully"
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to update memory entry: {e}")
            return MemoryOperationResult(
                success=False,
                message=f"Update failed: {str(e)}",
                error=str(e)
            )
    
    async def delete(self, user_id: str, key: str, memory_type: MemoryType) -> MemoryOperationResult:
        """Delete a memory entry"""
        try:
            async with self._get_connection() as db:
                # Get entry size for stats update
                cursor = await db.execute("""
                    SELECT LENGTH(content) as size FROM memory_entries 
                    WHERE user_id = ? AND key = ? AND memory_type = ?
                """, (user_id, key, memory_type.value))
                
                row = await cursor.fetchone()
                content_size = row['size'] if row else 0
                
                # Delete the entry
                cursor = await db.execute("""
                    DELETE FROM memory_entries 
                    WHERE user_id = ? AND key = ? AND memory_type = ?
                """, (user_id, key, memory_type.value))
                
                affected_count = cursor.rowcount
                
                if affected_count > 0:
                    # Log the access
                    await self._log_access(db, user_id, key, memory_type.value, "DELETE")
                    
                    # Update user statistics
                    await self._update_user_stats(db, user_id, -1, -content_size)
                
                await db.commit()
                
                return MemoryOperationResult(
                    success=affected_count > 0,
                    message=f"Deleted {affected_count} memory entry(ies)",
                    affected_count=affected_count
                )
                
        except Exception as e:
            logger.error(f"Failed to delete memory entry: {e}")
            return MemoryOperationResult(
                success=False,
                message=f"Deletion failed: {str(e)}",
                error=str(e)
            )
    
    async def cleanup_expired(self, user_id: Optional[str] = None) -> MemoryOperationResult:
        """Clean up expired memory entries"""
        try:
            async with self._get_connection() as db:
                # Build cleanup query
                sql = "DELETE FROM memory_entries WHERE expires_at IS NOT NULL AND expires_at <= ?"
                params = [datetime.now(timezone.utc).isoformat()]
                
                if user_id:
                    sql += " AND user_id = ?"
                    params.append(user_id)
                
                cursor = await db.execute(sql, params)
                deleted_count = cursor.rowcount
                
                # Update cleanup timestamp for affected users
                if user_id:
                    await db.execute("""
                        UPDATE memory_stats 
                        SET last_cleanup = ? 
                        WHERE user_id = ?
                    """, (datetime.now(timezone.utc).isoformat(), user_id))
                else:
                    await db.execute("""
                        UPDATE memory_stats 
                        SET last_cleanup = ?
                    """, (datetime.now(timezone.utc).isoformat(),))
                
                await db.commit()
                
                logger.info(f"Cleaned up {deleted_count} expired memory entries")
                
                return MemoryOperationResult(
                    success=True,
                    message=f"Cleaned up {deleted_count} expired entries",
                    affected_count=deleted_count
                )
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired entries: {e}")
            return MemoryOperationResult(
                success=False,
                message=f"Cleanup failed: {str(e)}",
                error=str(e)
            )
    
    async def get_user_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get memory usage statistics for a user"""
        try:
            async with self._get_connection() as db:
                # Get basic stats
                cursor = await db.execute("""
                    SELECT 
                        COUNT(*) as total_entries,
                        SUM(LENGTH(content)) as total_size_bytes,
                        MIN(created_at) as first_entry,
                        MAX(updated_at) as last_updated,
                        COUNT(CASE WHEN memory_type = 'SESSION' THEN 1 END) as session_entries,
                        COUNT(CASE WHEN memory_type = 'LONG_TERM' THEN 1 END) as long_term_entries,
                        COUNT(CASE WHEN memory_type = 'WORKING' THEN 1 END) as working_entries,
                        COUNT(CASE WHEN memory_type = 'PATTERN' THEN 1 END) as pattern_entries,
                        COUNT(CASE WHEN memory_type = 'PREFERENCE' THEN 1 END) as preference_entries,
                        COUNT(CASE WHEN expires_at IS NOT NULL AND expires_at <= ? THEN 1 END) as expired_entries
                    FROM memory_entries 
                    WHERE user_id = ?
                """, (datetime.now(timezone.utc).isoformat(), user_id))
                
                stats = dict(await cursor.fetchone())
                
                # Get recent activity
                cursor = await db.execute("""
                    SELECT COUNT(*) as recent_access_count
                    FROM memory_access_log 
                    WHERE user_id = ? AND timestamp > ?
                """, (user_id, (datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)).isoformat()))
                
                recent_stats = await cursor.fetchone()
                stats['today_access_count'] = recent_stats['recent_access_count']
                
                return stats
                
        except Exception as e:
            logger.error(f"Failed to get user memory stats: {e}")
            return {}
    
    async def _log_access(self, db: aiosqlite.Connection, user_id: str, 
                         memory_key: str, memory_type: str, action: str) -> None:
        """Log memory access for analytics and security"""
        try:
            await db.execute("""
                INSERT INTO memory_access_log 
                (user_id, memory_key, memory_type, action, timestamp, success)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, memory_key, memory_type, action, 
                  datetime.now(timezone.utc).isoformat(), True))
        except Exception as e:
            logger.warning(f"Failed to log memory access: {e}")
    
    async def _update_user_stats(self, db: aiosqlite.Connection, user_id: str, 
                                entry_delta: int, size_delta: int) -> None:
        """Update user memory statistics"""
        try:
            await db.execute("""
                INSERT OR REPLACE INTO memory_stats 
                (user_id, total_entries, total_size_bytes, last_activity)
                VALUES (
                    ?, 
                    COALESCE((SELECT total_entries FROM memory_stats WHERE user_id = ?), 0) + ?,
                    COALESCE((SELECT total_size_bytes FROM memory_stats WHERE user_id = ?), 0) + ?,
                    ?
                )
            """, (user_id, user_id, entry_delta, user_id, size_delta, 
                  datetime.now(timezone.utc).isoformat()))
        except Exception as e:
            logger.warning(f"Failed to update user stats: {e}")
    
    def _row_to_memory_entry(self, row: aiosqlite.Row) -> MemoryEntry:
        """Convert a database row to a MemoryEntry object"""
        # Parse JSON fields safely
        try:
            tags = json.loads(row['tags']) if row['tags'] else []
        except (json.JSONDecodeError, TypeError):
            tags = []
            
        try:
            metadata_dict = json.loads(row['metadata']) if row['metadata'] else {}
        except (json.JSONDecodeError, TypeError):
            metadata_dict = {}
        
        # Create metadata object with database timestamps
        metadata = MemoryMetadata(
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at']),
            accessed_at=datetime.fromisoformat(row['accessed_at']),
            access_count=metadata_dict.get('access_count', 0),
            creator_id=metadata_dict.get('creator_id', 'system'),
            tags=metadata_dict.get('tags', []),
            priority=MemoryPriority(row['priority']),
            access_level=MemoryAccess(row['access_level']),
            expires_at=datetime.fromisoformat(row['expires_at']) if row['expires_at'] else None,
            security_validated=metadata_dict.get('security_validated', False),
            validation_timestamp=datetime.fromisoformat(metadata_dict['validation_timestamp']) if metadata_dict.get('validation_timestamp') else None
        )
        
        return MemoryEntry(
            id=row['id'] if 'id' in row.keys() else str(uuid.uuid4()),
            user_id=row['user_id'],
            key=row['key'],
            memory_type=MemoryType(row['memory_type']),
            value=row['content'],  # Content is stored as plain text, not JSON
            content=row['content'],
            content_hash=row['content_hash'],
            tags=tags,
            version=row['version'],
            is_encrypted=bool(row['is_encrypted']),
            metadata=metadata
        )
    
    def _get_priority_values_above(self, min_priority: MemoryPriority) -> List[str]:
        """Get priority values at or above the minimum priority"""
        priority_order = [
            MemoryPriority.TEMPORARY,
            MemoryPriority.LOW,
            MemoryPriority.NORMAL,
            MemoryPriority.HIGH,
            MemoryPriority.CRITICAL
        ]
        
        min_index = priority_order.index(min_priority)
        return [p.value for p in priority_order[min_index:]]
    
    async def close(self) -> None:
        """Close the storage backend and cleanup resources"""
        self._initialized = False
        logger.info("SQLite memory storage closed")
