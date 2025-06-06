"""
TBH Secure Agents v5.0 - Memory System Configuration

This module defines configuration constants, default settings, and 
configuration utilities for the memory system.
"""

from datetime import timedelta
from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass, field

from .models import MemoryType, MemoryPriority, MemoryAccess


class StorageBackend(Enum):
    """Available storage backend types"""
    MEMORY = "memory"           # In-memory storage (development/testing)
    SQLITE = "sqlite"          # SQLite database
    POSTGRESQL = "postgresql"  # PostgreSQL database
    REDIS = "redis"           # Redis cache/storage
    HYBRID = "hybrid"         # Hybrid storage (fast + persistent)
    CHROMA = "chroma"         # Chroma vector database


class IndexingBackend(Enum):
    """Available indexing backend types"""
    SIMPLE = "simple"         # Simple text search
    ELASTICSEARCH = "elasticsearch"  # Elasticsearch
    VECTOR = "vector"         # Vector-based semantic search
    HYBRID = "hybrid"         # Multiple indexing strategies


@dataclass
class MemoryLimits:
    """Memory system limits and quotas"""
    max_entries_per_user: int = 10000
    max_entry_size_bytes: int = 1024 * 1024  # 1MB
    max_total_memory_mb: int = 100  # 100MB per user
    max_session_entries: int = 1000
    max_long_term_entries: int = 5000
    max_working_entries: int = 500
    max_pattern_entries: int = 2000
    max_preference_entries: int = 500


@dataclass
class SecurityConfig:
    """Security configuration for memory system"""
    enable_content_scanning: bool = True
    enable_access_validation: bool = True
    require_validation_for_types: list = field(
        default_factory=lambda: [MemoryType.LONG_TERM, MemoryType.PATTERN]
    )
    validation_timeout_seconds: float = 5.0
    max_validation_retries: int = 3
    security_log_level: str = "INFO"
    enable_encryption: bool = True
    encryption_key_rotation_days: int = 30


@dataclass
class PerformanceConfig:
    """Performance configuration for memory system"""
    async_operation_timeout: float = 30.0
    batch_size: int = 100
    cache_size: int = 1000
    cache_ttl_seconds: int = 300  # 5 minutes
    index_update_batch_size: int = 50
    cleanup_interval_minutes: int = 60
    stats_update_interval_minutes: int = 15


@dataclass
class RetentionConfig:
    """Memory retention configuration"""
    default_session_ttl: timedelta = field(default_factory=lambda: timedelta(hours=24))
    default_working_ttl: timedelta = field(default_factory=lambda: timedelta(hours=2))
    default_pattern_ttl: timedelta = field(default_factory=lambda: timedelta(days=30))
    
    # Priority-based retention
    critical_min_retention: timedelta = field(default_factory=lambda: timedelta(days=365))
    high_min_retention: timedelta = field(default_factory=lambda: timedelta(days=90))
    normal_min_retention: timedelta = field(default_factory=lambda: timedelta(days=30))
    low_min_retention: timedelta = field(default_factory=lambda: timedelta(days=7))
    temporary_max_retention: timedelta = field(default_factory=lambda: timedelta(hours=1))
    
    # Auto-cleanup settings
    enable_auto_cleanup: bool = True
    cleanup_batch_size: int = 1000
    aggressive_cleanup_threshold: float = 0.8  # When to start aggressive cleanup


@dataclass
class StorageConfig:
    """Storage backend configuration"""
    backend: StorageBackend = StorageBackend.SQLITE
    connection_string: Optional[str] = None
    sqlite_path: str = "memory_system.db"  # Default SQLite path
    connection_pool_size: int = 10
    connection_timeout: float = 10.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    enable_compression: bool = True
    backup_enabled: bool = True
    backup_interval_hours: int = 24
    
    # Chroma-specific configuration
    chroma_collection: Optional[str] = None
    chroma_persist_directory: Optional[str] = None
    chroma_host: str = "localhost"
    chroma_port: int = 8000


@dataclass
class IndexingConfig:
    """Indexing configuration"""
    backend: IndexingBackend = IndexingBackend.SIMPLE
    enable_semantic_search: bool = False
    semantic_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_dimensions: int = 384
    similarity_threshold: float = 0.7
    rebuild_index_on_startup: bool = False
    index_update_mode: str = "realtime"  # realtime, batch, manual


@dataclass
class MemorySystemConfig:
    """Complete memory system configuration"""
    limits: MemoryLimits = field(default_factory=MemoryLimits)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    retention: RetentionConfig = field(default_factory=RetentionConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    indexing: IndexingConfig = field(default_factory=IndexingConfig)
    
    # Global settings
    enable_debug_mode: bool = False
    log_level: str = "INFO"
    enable_metrics: bool = True
    metrics_export_interval: int = 60
    environment: str = "development"  # Add missing environment field
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'limits': {
                'max_entries_per_user': self.limits.max_entries_per_user,
                'max_entry_size_bytes': self.limits.max_entry_size_bytes,
                'max_total_memory_mb': self.limits.max_total_memory_mb,
                'max_session_entries': self.limits.max_session_entries,
                'max_long_term_entries': self.limits.max_long_term_entries,
                'max_working_entries': self.limits.max_working_entries,
                'max_pattern_entries': self.limits.max_pattern_entries,
                'max_preference_entries': self.limits.max_preference_entries
            },
            'security': {
                'enable_content_scanning': self.security.enable_content_scanning,
                'enable_access_validation': self.security.enable_access_validation,
                'require_validation_for_types': [t.value for t in self.security.require_validation_for_types],
                'validation_timeout_seconds': self.security.validation_timeout_seconds,
                'max_validation_retries': self.security.max_validation_retries,
                'security_log_level': self.security.security_log_level,
                'enable_encryption': self.security.enable_encryption,
                'encryption_key_rotation_days': self.security.encryption_key_rotation_days
            },
            'performance': {
                'async_operation_timeout': self.performance.async_operation_timeout,
                'batch_size': self.performance.batch_size,
                'cache_size': self.performance.cache_size,
                'cache_ttl_seconds': self.performance.cache_ttl_seconds,
                'index_update_batch_size': self.performance.index_update_batch_size,
                'cleanup_interval_minutes': self.performance.cleanup_interval_minutes,
                'stats_update_interval_minutes': self.performance.stats_update_interval_minutes
            },
            'retention': {
                'default_session_ttl_seconds': int(self.retention.default_session_ttl.total_seconds()),
                'default_working_ttl_seconds': int(self.retention.default_working_ttl.total_seconds()),
                'default_pattern_ttl_seconds': int(self.retention.default_pattern_ttl.total_seconds()),
                'critical_min_retention_seconds': int(self.retention.critical_min_retention.total_seconds()),
                'high_min_retention_seconds': int(self.retention.high_min_retention.total_seconds()),
                'normal_min_retention_seconds': int(self.retention.normal_min_retention.total_seconds()),
                'low_min_retention_seconds': int(self.retention.low_min_retention.total_seconds()),
                'temporary_max_retention_seconds': int(self.retention.temporary_max_retention.total_seconds()),
                'enable_auto_cleanup': self.retention.enable_auto_cleanup,
                'cleanup_batch_size': self.retention.cleanup_batch_size,
                'aggressive_cleanup_threshold': self.retention.aggressive_cleanup_threshold
            },
            'storage': {
                'backend': self.storage.backend.value,
                'connection_string': self.storage.connection_string,
                'sqlite_path': self.storage.sqlite_path,
                'connection_pool_size': self.storage.connection_pool_size,
                'connection_timeout': self.storage.connection_timeout,
                'retry_attempts': self.storage.retry_attempts,
                'retry_delay': self.storage.retry_delay,
                'enable_compression': self.storage.enable_compression,
                'backup_enabled': self.storage.backup_enabled,
                'backup_interval_hours': self.storage.backup_interval_hours,
                'chroma_collection': self.storage.chroma_collection,
                'chroma_persist_directory': self.storage.chroma_persist_directory,
                'chroma_host': self.storage.chroma_host,
                'chroma_port': self.storage.chroma_port
            },
            'indexing': {
                'backend': self.indexing.backend.value,
                'enable_semantic_search': self.indexing.enable_semantic_search,
                'semantic_model': self.indexing.semantic_model,
                'vector_dimensions': self.indexing.vector_dimensions,
                'similarity_threshold': self.indexing.similarity_threshold,
                'rebuild_index_on_startup': self.indexing.rebuild_index_on_startup,
                'index_update_mode': self.indexing.index_update_mode
            },
            'global': {
                'enable_debug_mode': self.enable_debug_mode,
                'log_level': self.log_level,
                'enable_metrics': self.enable_metrics,
                'metrics_export_interval': self.metrics_export_interval
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemorySystemConfig':
        """Create configuration from dictionary"""
        config = cls()
        
        # Update limits
        if 'limits' in data:
            limits_data = data['limits']
            config.limits = MemoryLimits(**limits_data)
        
        # Update security
        if 'security' in data:
            security_data = data['security']
            if 'require_validation_for_types' in security_data:
                security_data['require_validation_for_types'] = [
                    MemoryType(t) for t in security_data['require_validation_for_types']
                ]
            config.security = SecurityConfig(**security_data)
        
        # Update performance
        if 'performance' in data:
            config.performance = PerformanceConfig(**data['performance'])
        
        # Update retention
        if 'retention' in data:
            retention_data = data['retention']
            # Convert seconds back to timedelta
            if 'default_session_ttl_seconds' in retention_data:
                retention_data['default_session_ttl'] = timedelta(seconds=retention_data.pop('default_session_ttl_seconds'))
            if 'default_working_ttl_seconds' in retention_data:
                retention_data['default_working_ttl'] = timedelta(seconds=retention_data.pop('default_working_ttl_seconds'))
            if 'default_pattern_ttl_seconds' in retention_data:
                retention_data['default_pattern_ttl'] = timedelta(seconds=retention_data.pop('default_pattern_ttl_seconds'))
            if 'critical_min_retention_seconds' in retention_data:
                retention_data['critical_min_retention'] = timedelta(seconds=retention_data.pop('critical_min_retention_seconds'))
            if 'high_min_retention_seconds' in retention_data:
                retention_data['high_min_retention'] = timedelta(seconds=retention_data.pop('high_min_retention_seconds'))
            if 'normal_min_retention_seconds' in retention_data:
                retention_data['normal_min_retention'] = timedelta(seconds=retention_data.pop('normal_min_retention_seconds'))
            if 'low_min_retention_seconds' in retention_data:
                retention_data['low_min_retention'] = timedelta(seconds=retention_data.pop('low_min_retention_seconds'))
            if 'temporary_max_retention_seconds' in retention_data:
                retention_data['temporary_max_retention'] = timedelta(seconds=retention_data.pop('temporary_max_retention_seconds'))
            
            config.retention = RetentionConfig(**retention_data)
        
        # Update storage
        if 'storage' in data:
            storage_data = data['storage']
            if 'backend' in storage_data:
                storage_data['backend'] = StorageBackend(storage_data['backend'])
            config.storage = StorageConfig(**storage_data)
        
        # Update indexing
        if 'indexing' in data:
            indexing_data = data['indexing']
            if 'backend' in indexing_data:
                indexing_data['backend'] = IndexingBackend(indexing_data['backend'])
            config.indexing = IndexingConfig(**indexing_data)
        
        # Update global settings
        if 'global' in data:
            global_data = data['global']
            config.enable_debug_mode = global_data.get('enable_debug_mode', config.enable_debug_mode)
            config.log_level = global_data.get('log_level', config.log_level)
            config.enable_metrics = global_data.get('enable_metrics', config.enable_metrics)
            config.metrics_export_interval = global_data.get('metrics_export_interval', config.metrics_export_interval)
        
        return config


# Default configurations for different environments
DEFAULT_CONFIG = MemorySystemConfig()

DEVELOPMENT_CONFIG = MemorySystemConfig(
    storage=StorageConfig(backend=StorageBackend.MEMORY),
    indexing=IndexingConfig(backend=IndexingBackend.SIMPLE),
    security=SecurityConfig(enable_encryption=False),
    enable_debug_mode=True,
    log_level="DEBUG"
)

PRODUCTION_CONFIG = MemorySystemConfig(
    storage=StorageConfig(
        backend=StorageBackend.POSTGRESQL,
        connection_pool_size=20,
        backup_enabled=True
    ),
    indexing=IndexingConfig(
        backend=IndexingBackend.ELASTICSEARCH,
        enable_semantic_search=True
    ),
    security=SecurityConfig(
        enable_encryption=True,
        enable_content_scanning=True,
        enable_access_validation=True
    ),
    performance=PerformanceConfig(
        cache_size=5000,
        batch_size=500
    ),
    enable_metrics=True,
    log_level="INFO"
)

TESTING_CONFIG = MemorySystemConfig(
    storage=StorageConfig(backend=StorageBackend.MEMORY),
    indexing=IndexingConfig(backend=IndexingBackend.SIMPLE),
    security=SecurityConfig(
        enable_content_scanning=False,
        enable_access_validation=False,
        enable_encryption=False
    ),
    retention=RetentionConfig(
        default_session_ttl=timedelta(minutes=5),
        default_working_ttl=timedelta(minutes=1),
        enable_auto_cleanup=False
    ),
    enable_debug_mode=True,
    log_level="DEBUG"
)


def get_config(environment: str = "default") -> MemorySystemConfig:
    """Get configuration for specified environment"""
    configs = {
        "default": DEFAULT_CONFIG,
        "development": DEVELOPMENT_CONFIG,
        "production": PRODUCTION_CONFIG,
        "testing": TESTING_CONFIG
    }
    
    return configs.get(environment.lower(), DEFAULT_CONFIG)


def validate_config(config: MemorySystemConfig) -> Dict[str, Any]:
    """Validate memory system configuration"""
    issues = []
    warnings = []
    
    # Validate limits
    if config.limits.max_entries_per_user <= 0:
        issues.append("max_entries_per_user must be positive")
    
    if config.limits.max_entry_size_bytes <= 0:
        issues.append("max_entry_size_bytes must be positive")
    
    # Validate performance settings
    if config.performance.async_operation_timeout <= 0:
        issues.append("async_operation_timeout must be positive")
    
    if config.performance.batch_size <= 0:
        issues.append("batch_size must be positive")
    
    # Validate security settings
    if config.security.validation_timeout_seconds <= 0:
        issues.append("validation_timeout_seconds must be positive")
    
    # Validate retention settings
    if config.retention.temporary_max_retention > config.retention.low_min_retention:
        warnings.append("temporary_max_retention is longer than low_min_retention")
    
    # Check for potential performance issues
    if config.limits.max_entries_per_user > 50000:
        warnings.append("High max_entries_per_user may impact performance")
    
    if config.performance.cache_size > 10000:
        warnings.append("Large cache_size may consume significant memory")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings
    }
