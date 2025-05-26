#!/usr/bin/env python3
"""
Production-grade configuration management for hybrid security validation.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class SecurityConfig:
    """Production security configuration."""
    
    # Core settings
    security_level: str = "standard"
    enable_caching: bool = True
    cache_ttl: int = 3600  # 1 hour
    max_cache_size: int = 10000
    
    # Validation settings
    use_parallel_validation: bool = True
    max_validation_time: float = 30.0  # seconds
    enable_smart_routing: bool = True
    
    # Regex settings
    regex_timeout: float = 5.0
    regex_max_patterns: int = 1000
    
    # ML settings
    ml_confidence_threshold: float = 0.7
    ml_model_path: Optional[str] = None
    ml_enable_training: bool = False
    
    # LLM settings
    llm_api_key: Optional[str] = None
    llm_model: str = "gemini-1.5-flash"
    llm_max_tokens: int = 1000
    llm_temperature: float = 0.1
    llm_timeout: float = 15.0
    llm_retry_attempts: int = 3
    llm_retry_delay: float = 1.0
    
    # Monitoring settings
    enable_metrics: bool = True
    metrics_export_interval: int = 60  # seconds
    enable_performance_logging: bool = True
    
    # Security thresholds by level
    security_thresholds: Dict[str, float] = None
    
    def __post_init__(self):
        """Initialize default security thresholds."""
        if self.security_thresholds is None:
            self.security_thresholds = {
                "minimal": 0.95,    # Very permissive
                "standard": 0.85,   # Balanced
                "high": 0.7,        # Strict
                "maximum": 0.5      # Very strict
            }
    
    @classmethod
    def from_file(cls, config_path: str) -> 'SecurityConfig':
        """Load configuration from file."""
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            return cls(**data)
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
            return cls()
    
    @classmethod
    def from_env(cls) -> 'SecurityConfig':
        """Load configuration from environment variables."""
        config = cls()
        
        # Core settings
        config.security_level = os.getenv("TBH_SECURITY_LEVEL", config.security_level)
        config.enable_caching = os.getenv("TBH_ENABLE_CACHING", "true").lower() == "true"
        config.cache_ttl = int(os.getenv("TBH_CACHE_TTL", str(config.cache_ttl)))
        config.max_cache_size = int(os.getenv("TBH_MAX_CACHE_SIZE", str(config.max_cache_size)))
        
        # Validation settings
        config.use_parallel_validation = os.getenv("TBH_PARALLEL_VALIDATION", "true").lower() == "true"
        config.max_validation_time = float(os.getenv("TBH_MAX_VALIDATION_TIME", str(config.max_validation_time)))
        config.enable_smart_routing = os.getenv("TBH_SMART_ROUTING", "true").lower() == "true"
        
        # LLM settings
        config.llm_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("TBH_LLM_API_KEY")
        config.llm_model = os.getenv("TBH_LLM_MODEL", config.llm_model)
        config.llm_timeout = float(os.getenv("TBH_LLM_TIMEOUT", str(config.llm_timeout)))
        
        # Monitoring
        config.enable_metrics = os.getenv("TBH_ENABLE_METRICS", "true").lower() == "true"
        config.enable_performance_logging = os.getenv("TBH_PERFORMANCE_LOGGING", "true").lower() == "true"
        
        return config
    
    def save_to_file(self, config_path: str) -> None:
        """Save configuration to file."""
        try:
            Path(config_path).parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(asdict(self), f, indent=2)
            logger.info(f"Configuration saved to {config_path}")
        except Exception as e:
            logger.error(f"Failed to save config to {config_path}: {e}")
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        errors = []
        
        # Validate security level
        if self.security_level not in ["minimal", "standard", "high", "maximum"]:
            errors.append(f"Invalid security_level: {self.security_level}")
        
        # Validate timeouts
        if self.max_validation_time <= 0:
            errors.append("max_validation_time must be positive")
        
        if self.llm_timeout <= 0:
            errors.append("llm_timeout must be positive")
        
        # Validate cache settings
        if self.max_cache_size <= 0:
            errors.append("max_cache_size must be positive")
        
        if self.cache_ttl <= 0:
            errors.append("cache_ttl must be positive")
        
        # Validate thresholds
        for level, threshold in self.security_thresholds.items():
            if not 0 <= threshold <= 1:
                errors.append(f"Invalid threshold for {level}: {threshold}")
        
        if errors:
            logger.error(f"Configuration validation failed: {errors}")
            return False
        
        return True

class ProductionConfigManager:
    """Manages production configuration with hot reloading."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_path = config_path or os.getenv("TBH_CONFIG_PATH", "config/security.json")
        self._config = None
        self._last_modified = 0
        
    def get_config(self) -> SecurityConfig:
        """Get current configuration with hot reloading."""
        if self._should_reload():
            self._reload_config()
        
        if self._config is None:
            self._config = SecurityConfig.from_env()
            
        return self._config
    
    def _should_reload(self) -> bool:
        """Check if configuration should be reloaded."""
        if not os.path.exists(self.config_path):
            return False
            
        try:
            current_modified = os.path.getmtime(self.config_path)
            return current_modified > self._last_modified
        except OSError:
            return False
    
    def _reload_config(self) -> None:
        """Reload configuration from file."""
        try:
            self._config = SecurityConfig.from_file(self.config_path)
            self._last_modified = os.path.getmtime(self.config_path)
            
            if self._config.validate():
                logger.info(f"Configuration reloaded from {self.config_path}")
            else:
                logger.error("Configuration validation failed, keeping previous config")
                self._config = SecurityConfig.from_env()
                
        except Exception as e:
            logger.error(f"Failed to reload configuration: {e}")
            self._config = SecurityConfig.from_env()

# Global configuration manager
_config_manager = ProductionConfigManager()

def get_production_config() -> SecurityConfig:
    """Get the current production configuration."""
    return _config_manager.get_config()

def set_config_path(path: str) -> None:
    """Set the configuration file path."""
    global _config_manager
    _config_manager = ProductionConfigManager(path)
