"""
Chroma Vector Database Memory Storage Implementation
Production-ready memory system using Chroma vector database
"""

import chromadb
from chromadb.config import Settings
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path
import asyncio
import logging

from ..models import MemoryEntry, MemorySearchQuery, MemorySearchResult, MemoryType
from ..interfaces import MemoryStorageInterface
from ..config import MemorySystemConfig

logger = logging.getLogger(__name__)


class ChromaMemoryStorage(MemoryStorageInterface):
    """
    Production-ready memory storage using Chroma vector database.
    Handles semantic search, encryption, and scalability concerns.
    """
    
    def __init__(self, config: MemorySystemConfig):
        """
        Initialize Chroma memory storage.
        
        Args:
            config: Memory system configuration containing Chroma settings
        """
        self.config = config
        self.collection_name = config.storage.chroma_collection or "secure_memories"
        self.persist_directory = config.storage.chroma_persist_directory or str(Path.home() / ".tbh_secure_agents" / "chroma_db")
        
        logger.info(f"ChromaMemoryStorage initializing with collection: {self.collection_name}")
        logger.info(f"ChromaMemoryStorage persist directory: {self.persist_directory}")
        
        # Ensure persist directory exists
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize Chroma client
        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            logger.info(f"ChromaDB client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB client: {e}")
            raise
        
        # Get or create collection
        try:
            logger.info(f"Attempting to get existing collection: {self.collection_name}")
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Loaded existing Chroma collection: {self.collection_name}")
        except Exception as e:
            # Collection doesn't exist, create it
            logger.info(f"Collection {self.collection_name} doesn't exist (error: {e}), creating new one...")
            try:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "TBH Secure Agents Memory Storage"}
                )
                logger.info(f"Created new Chroma collection: {self.collection_name}")
            except Exception as create_error:
                logger.error(f"Failed to create collection {self.collection_name}: {create_error}")
                raise
    
    async def initialize(self) -> bool:
        """Initialize the storage system."""
        try:
            # Test the collection
            self.collection.count()
            logger.info("Chroma memory storage initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Chroma storage: {e}")
            return False
    
    async def store(self, entry: MemoryEntry, searchable_content: Optional[str] = None, 
                   searchable_tags: Optional[str] = None) -> Any:
        """
        Store a memory entry in Chroma.
        
        Args:
            entry: The memory entry to store
            searchable_content: Content for semantic search (plain text)
            searchable_tags: Tags for search (plain text)
        """
        try:
            # Use searchable content for embeddings, fallback to entry content
            content_for_embedding = searchable_content or entry.content
            
            # Create document metadata
            metadata = {
                "user_id": entry.user_id,
                "memory_type": entry.memory_type.value,
                "priority": entry.metadata.priority.value,
                "access_level": entry.metadata.access_level.value,
                "created_at": entry.metadata.created_at.isoformat(),
                "updated_at": entry.metadata.updated_at.isoformat(),
                "tags": json.dumps(entry.tags),
                "version": entry.version,
                "is_encrypted": entry.is_encrypted,
                "content_hash": entry.content_hash
            }
            
            # Add entry to collection
            self.collection.add(
                documents=[content_for_embedding],
                metadatas=[metadata],
                ids=[entry.key]
            )
            
            # Store the actual (possibly encrypted) content separately in metadata
            # This allows us to do semantic search on plain text while storing encrypted content
            self.collection.update(
                ids=[entry.key],
                metadatas=[{**metadata, "encrypted_content": entry.content}]
            )
            
            logger.info(f"Stored memory {entry.key} in Chroma collection")
            
            # Return success result
            from ..storage.sqlite_storage import MemoryOperationResult
            return MemoryOperationResult(success=True, message="Memory stored successfully")
            
        except Exception as e:
            logger.error(f"Failed to store memory in Chroma: {e}")
            from ..storage.sqlite_storage import MemoryOperationResult
            return MemoryOperationResult(success=False, message=f"Storage failed: {str(e)}")
    
    async def search(self, query: MemorySearchQuery) -> MemorySearchResult:
        """
        Search memories using semantic similarity.
        
        Args:
            query: The search query
            
        Returns:
            Search results with matching memories
        """
        try:
            start_time = datetime.now()
            
            # Build where clause for filtering
            where_clause = {}
            
            if query.user_id:
                where_clause["user_id"] = query.user_id
            
            if query.memory_types:
                # Chroma doesn't support IN queries directly, so we'll filter after
                pass
            
            # Perform semantic search
            results = self.collection.query(
                query_texts=[query.content_pattern] if query.content_pattern else [""],
                n_results=query.limit or 10,
                where=where_clause if where_clause else None
            )
            
            # Convert results to MemoryEntry objects
            entries = []
            if results["documents"]:
                for i in range(len(results["documents"][0])):
                    metadata = results["metadatas"][0][i]
                    
                    # Filter by memory types if specified
                    if query.memory_types:
                        memory_type_values = [mt.value for mt in query.memory_types]
                        if metadata["memory_type"] not in memory_type_values:
                            continue
                    
                    # Create MemoryEntry from results
                    from ..models import MemoryMetadata, MemoryPriority, MemoryAccess
                    
                    memory_metadata = MemoryMetadata(
                        created_at=datetime.fromisoformat(metadata["created_at"]),
                        updated_at=datetime.fromisoformat(metadata["updated_at"]),
                        priority=MemoryPriority(metadata["priority"]),
                        access_level=MemoryAccess(metadata["access_level"])
                    )
                    
                    entry = MemoryEntry(
                        key=results["ids"][0][i],
                        user_id=metadata["user_id"],
                        memory_type=MemoryType(metadata["memory_type"]),
                        content=metadata.get("encrypted_content", results["documents"][0][i]),
                        content_hash=metadata["content_hash"],
                        tags=json.loads(metadata["tags"]) if metadata["tags"] else [],
                        metadata=memory_metadata,
                        version=metadata["version"],
                        is_encrypted=metadata["is_encrypted"]
                    )
                    
                    entries.append(entry)
            
            search_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return MemorySearchResult(
                entries=entries,
                total_count=len(entries),
                query_time_ms=search_time
            )
            
        except Exception as e:
            logger.error(f"Failed to search memories in Chroma: {e}")
            return MemorySearchResult(entries=[], total_count=0, query_time_ms=0.0)
    
    async def retrieve(self, user_id: str, key: str, memory_type: MemoryType) -> Optional[MemoryEntry]:
        """Retrieve a specific memory by key."""
        try:
            results = self.collection.get(
                ids=[key],
                where={"user_id": user_id}
            )
            
            if not results["documents"]:
                return None
            
            metadata = results["metadatas"][0]
            
            # Verify memory type matches
            if metadata["memory_type"] != memory_type.value:
                return None
            
            # Create MemoryEntry
            from ..models import MemoryMetadata, MemoryPriority, MemoryAccess
            
            memory_metadata = MemoryMetadata(
                created_at=datetime.fromisoformat(metadata["created_at"]),
                updated_at=datetime.fromisoformat(metadata["updated_at"]),
                priority=MemoryPriority(metadata["priority"]),
                access_level=MemoryAccess(metadata["access_level"])
            )
            
            entry = MemoryEntry(
                key=key,
                user_id=metadata["user_id"],
                memory_type=MemoryType(metadata["memory_type"]),
                content=metadata.get("encrypted_content", results["documents"][0]),
                content_hash=metadata["content_hash"],
                tags=json.loads(metadata["tags"]) if metadata["tags"] else [],
                metadata=memory_metadata,
                version=metadata["version"],
                is_encrypted=metadata["is_encrypted"]
            )
            
            return entry
            
        except Exception as e:
            logger.error(f"Failed to retrieve memory {key}: {e}")
            return None
    
    async def delete(self, user_id: str, key: str, memory_type: MemoryType) -> Any:
        """Delete a memory entry."""
        try:
            # Verify the memory exists and belongs to the user
            existing = await self.retrieve(user_id, key, memory_type)
            if not existing:
                from ..storage.sqlite_storage import MemoryOperationResult
                return MemoryOperationResult(success=False, message="Memory not found")
            
            # Delete from collection
            self.collection.delete(ids=[key])
            
            logger.info(f"Deleted memory {key} from Chroma collection")
            
            from ..storage.sqlite_storage import MemoryOperationResult
            return MemoryOperationResult(success=True, message="Memory deleted successfully")
            
        except Exception as e:
            logger.error(f"Failed to delete memory {key}: {e}")
            from ..storage.sqlite_storage import MemoryOperationResult
            return MemoryOperationResult(success=False, message=f"Delete failed: {str(e)}")
    
    async def update(self, entry: MemoryEntry) -> Any:
        """Update an existing memory entry."""
        try:
            # Delete the old entry
            self.collection.delete(ids=[entry.key])
            
            # Store the updated entry
            return await self.store(entry)
            
        except Exception as e:
            logger.error(f"Failed to update memory {entry.key}: {e}")
            from ..storage.sqlite_storage import MemoryOperationResult
            return MemoryOperationResult(success=False, message=f"Update failed: {str(e)}")
    
    def reset(self):
        """Reset the collection (for testing)."""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "TBH Secure Agents Memory Storage"}
            )
            logger.info("Reset Chroma collection")
        except Exception as e:
            logger.error(f"Failed to reset collection: {e}")
