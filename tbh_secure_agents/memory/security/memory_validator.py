"""
TBH Secure Agents v5.0 - Memory Content Validator

Integrates memory content validation with the existing 4-layer hybrid security
validation system (Regex + ML + LLM + Adaptive).
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models import MemoryEntry, MemoryType
from ..config import MemorySystemConfig

# Import existing security validation system
try:
    from ...security_validation.validators.hybrid_validator import HybridValidator
    from ...security_validation.validators.production_hybrid_validator import ProductionHybridValidator
    SECURITY_AVAILABLE = True
except ImportError:
    logging.warning("Security validation system not available - memory validation will be limited")
    SECURITY_AVAILABLE = False


logger = logging.getLogger(__name__)


class ContentValidationResult:
    """Result of content validation"""
    
    def __init__(
        self,
        is_secure: bool,
        method: str,
        confidence: float = 1.0,
        reason: Optional[str] = None,
        suggestions: Optional[List[str]] = None,
        validation_time: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.is_secure = is_secure
        self.method = method
        self.confidence = confidence
        self.reason = reason
        self.suggestions = suggestions or []
        self.validation_time = validation_time
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "is_secure": self.is_secure,
            "method": self.method,
            "confidence": self.confidence,
            "reason": self.reason,
            "suggestions": self.suggestions,
            "validation_time": self.validation_time,
            "metadata": self.metadata
        }


class MemoryValidator:
    """
    Memory content validator that integrates with the existing 4-layer
    hybrid security validation system.
    
    Provides content validation for memory entries using:
    - Regex validation for pattern-based threats
    - ML validation for learned threat detection
    - LLM validation for semantic understanding
    - Adaptive validation based on usage patterns
    """
    
    def __init__(self, config: MemorySystemConfig):
        self.config = config
        
        # Initialize hybrid validator if available
        if SECURITY_AVAILABLE:
            try:
                # Use production validator for better performance
                self.hybrid_validator = ProductionHybridValidator(
                    use_parallel=True,
                    enable_smart_routing=True
                )
                logger.info("Initialized MemoryValidator with ProductionHybridValidator")
            except Exception as e:
                logger.warning(f"Failed to initialize ProductionHybridValidator: {e}")
                try:
                    # Fallback to standard hybrid validator
                    self.hybrid_validator = HybridValidator(
                        use_parallel=True,
                        max_cache_size=self.config.performance.cache_size
                    )
                    logger.info("Initialized MemoryValidator with HybridValidator")
                except Exception as e2:
                    logger.error(f"Failed to initialize any hybrid validator: {e2}")
                    self.hybrid_validator = None
        else:
            self.hybrid_validator = None
        
        # Memory-specific validation patterns
        self._memory_threat_patterns = {
            'injection_attempts': [
                r'(?i)\b(drop|delete|insert|update|select)\s+.*\s+(table|from|where)',
                r'(?i)<script[^>]*>.*?</script>',
                r'(?i)javascript:[^"\']*',
                r'(?i)data:text/html',
                r'(?i)eval\s*\(',
                r'(?i)exec\s*\(',
            ],
            'sensitive_data_patterns': [
                r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card numbers
                r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email patterns
                r'\b(?:\d{1,3}\.){3}\d{1,3}\b',  # IP addresses
            ],
            'system_commands': [
                r'(?i)\b(rm|del|format|fdisk|mkfs)\b',
                r'(?i)\b(sudo|su|chmod|chown)\b',
                r'(?i)\b(curl|wget|nc|netcat)\b',
                r'(?i)\b(python|node|bash|sh|cmd|powershell)\b.*[;&|]',
            ]
        }
        
        # Memory type security mappings
        self._memory_type_security_levels = {
            MemoryType.SESSION: "minimal",
            MemoryType.WORKING: "standard",
            MemoryType.PREFERENCE: "standard", 
            MemoryType.LONG_TERM: "high",
            MemoryType.PATTERN: "high"
        }
    
    async def validate_content(
        self,
        content: str,
        memory_type: MemoryType,
        security_level: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ContentValidationResult:
        """
        Validate memory content using the hybrid security validation system.
        
        Args:
            content: The content to validate
            memory_type: Type of memory being validated
            security_level: Security level for validation
            context: Additional context for validation
            
        Returns:
            ContentValidationResult with validation details
        """
        start_time = datetime.now()
        context = context or {}
        
        try:
            # Perform memory-specific pre-validation
            pre_validation_result = await self._pre_validate_memory_content(
                content, memory_type, context
            )
            
            if not pre_validation_result.is_secure:
                return pre_validation_result
            
            # Use hybrid validator if available
            if self.hybrid_validator:
                # Prepare context for hybrid validation
                hybrid_context = {
                    "security_level": security_level,
                    "memory_type": memory_type.value,
                    "user_id": context.get("user_id"),
                    "memory_key": context.get("memory_key"),
                    "operation": context.get("operation", "store"),
                    **context
                }
                
                # Run hybrid validation
                hybrid_result = self.hybrid_validator.validate(content, hybrid_context)
                
                # Convert hybrid result to ContentValidationResult
                validation_time = (datetime.now() - start_time).total_seconds()
                return ContentValidationResult(
                    is_secure=hybrid_result.get("is_secure", True),
                    method=f"hybrid_{hybrid_result.get('method', 'unknown')}",
                    confidence=hybrid_result.get("confidence", 0.8),
                    reason=hybrid_result.get("reason"),
                    suggestions=hybrid_result.get("suggestions", []),
                    validation_time=validation_time,
                    metadata={
                        "hybrid_result": hybrid_result,
                        "memory_type": memory_type.value,
                        "security_level": security_level
                    }
                )
            else:
                # Fallback to basic pattern-based validation
                return await self._basic_content_validation(
                    content, memory_type, security_level, context
                )
                
        except Exception as e:
            logger.error(f"Content validation failed: {e}")
            validation_time = (datetime.now() - start_time).total_seconds()
            return ContentValidationResult(
                is_secure=False,
                method="validation_error",
                confidence=0.0,
                reason=f"Validation error: {str(e)}",
                suggestions=["Contact system administrator"],
                validation_time=validation_time,
                metadata={"error": str(e)}
            )
    
    async def _pre_validate_memory_content(
        self,
        content: str,
        memory_type: MemoryType,
        context: Dict[str, Any]
    ) -> ContentValidationResult:
        """
        Perform memory-specific pre-validation checks.
        
        This includes size limits, encoding validation, and memory-type
        specific content rules.
        """
        # Check content size limits
        max_content_size = self._get_max_content_size(memory_type)
        if len(content) > max_content_size:
            return ContentValidationResult(
                is_secure=False,
                method="memory_size_limit",
                reason=f"Content size ({len(content)}) exceeds limit for {memory_type.value} ({max_content_size})",
                suggestions=[f"Reduce content size to under {max_content_size} characters"]
            )
        
        # Check for null bytes and control characters
        if '\x00' in content or any(ord(c) < 32 and c not in '\t\n\r' for c in content):
            return ContentValidationResult(
                is_secure=False,
                method="memory_encoding_check",
                reason="Content contains null bytes or invalid control characters",
                suggestions=["Remove null bytes and control characters from content"]
            )
        
        # Memory type specific validation
        if memory_type == MemoryType.PATTERN:
            # Pattern memories should not contain executable code
            if any(pattern in content.lower() for pattern in ['import ', 'exec(', 'eval(', '__import__']):
                return ContentValidationResult(
                    is_secure=False,
                    method="memory_pattern_security",
                    reason="Pattern memory contains potentially executable code",
                    suggestions=["Store pattern data, not executable code"]
                )
        
        return ContentValidationResult(
            is_secure=True,
            method="memory_pre_validation",
            confidence=1.0
        )
    
    async def _basic_content_validation(
        self,
        content: str,
        memory_type: MemoryType,
        security_level: str,
        context: Dict[str, Any]
    ) -> ContentValidationResult:
        """
        Basic content validation when hybrid validator is not available.
        """
        start_time = datetime.now()
        
        # Check against memory-specific threat patterns
        for category, patterns in self._memory_threat_patterns.items():
            for pattern in patterns:
                import re
                if re.search(pattern, content):
                    validation_time = (datetime.now() - start_time).total_seconds()
                    return ContentValidationResult(
                        is_secure=False,
                        method="basic_pattern_match",
                        reason=f"Content matches {category} pattern",
                        suggestions=[f"Remove or sanitize {category} from content"],
                        validation_time=validation_time,
                        metadata={"category": category, "pattern": pattern}
                    )
        
        validation_time = (datetime.now() - start_time).total_seconds()
        return ContentValidationResult(
            is_secure=True,
            method="basic_validation",
            confidence=0.7,  # Lower confidence for basic validation
            validation_time=validation_time
        )
    
    def _get_max_content_size(self, memory_type: MemoryType) -> int:
        """Get maximum content size for memory type"""
        size_limits = {
            MemoryType.SESSION: 10240,      # 10KB for session data
            MemoryType.WORKING: 51200,      # 50KB for working memory
            MemoryType.PREFERENCE: 2048,    # 2KB for preferences
            MemoryType.LONG_TERM: 102400,   # 100KB for long-term memory
            MemoryType.PATTERN: 10240,      # 10KB for patterns
        }
        return size_limits.get(memory_type, 10240)
    
    async def scan_for_threats(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Scan content for specific threat categories.
        
        Returns a detailed threat analysis report.
        """
        threats_found = {}
        context = context or {}
        
        # Scan each threat category
        for category, patterns in self._memory_threat_patterns.items():
            matches = []
            for pattern in patterns:
                import re
                found_matches = re.finditer(pattern, content)
                for match in found_matches:
                    matches.append({
                        "pattern": pattern,
                        "match": match.group(0),
                        "position": (match.start(), match.end())
                    })
            
            if matches:
                threats_found[category] = {
                    "count": len(matches),
                    "matches": matches,
                    "severity": self._get_threat_severity(category)
                }
        
        return {
            "threats_found": threats_found,
            "total_threats": sum(len(t["matches"]) for t in threats_found.values()),
            "highest_severity": max(
                (t["severity"] for t in threats_found.values()),
                default="none"
            ),
            "scan_timestamp": datetime.now().isoformat()
        }
    
    def _get_threat_severity(self, category: str) -> str:
        """Get severity level for threat category"""
        severity_mapping = {
            "injection_attempts": "high",
            "sensitive_data_patterns": "medium",
            "system_commands": "high"
        }
        return severity_mapping.get(category, "low")
    
    async def validate_memory_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ContentValidationResult:
        """
        Validate memory search queries for injection attacks.
        """
        start_time = datetime.now()
        context = context or {}
        
        try:
            # Use hybrid validator for query validation if available
            if self.hybrid_validator:
                query_context = {
                    "security_level": "high",  # Always use high security for queries
                    "validation_type": "memory_query",
                    **context
                }
                
                result = self.hybrid_validator.validate(query, query_context)
                validation_time = (datetime.now() - start_time).total_seconds()
                
                return ContentValidationResult(
                    is_secure=result.get("is_secure", True),
                    method=f"query_hybrid_{result.get('method', 'unknown')}",
                    confidence=result.get("confidence", 0.8),
                    reason=result.get("reason"),
                    suggestions=result.get("suggestions", []),
                    validation_time=validation_time,
                    metadata={"hybrid_result": result}
                )
            else:
                # Basic query validation
                return await self._basic_query_validation(query, context)
                
        except Exception as e:
            logger.error(f"Query validation failed: {e}")
            validation_time = (datetime.now() - start_time).total_seconds()
            return ContentValidationResult(
                is_secure=False,
                method="query_validation_error",
                confidence=0.0,
                reason=f"Query validation error: {str(e)}",
                validation_time=validation_time,
                metadata={"error": str(e)}
            )
    
    async def _basic_query_validation(
        self,
        query: str,
        context: Dict[str, Any]
    ) -> ContentValidationResult:
        """Basic query validation without hybrid validator"""
        start_time = datetime.now()
        
        # Check for SQL injection patterns in queries
        sql_injection_patterns = [
            r'(?i)\b(union|select|insert|update|delete|drop|create|alter)\b',
            r'(?i)--.*',
            r'(?i)/\*.*?\*/',
            r'[\'"`].*[\'"`]',
            r'(?i)\bor\s+\d+\s*=\s*\d+',
            r'(?i)\band\s+\d+\s*=\s*\d+',
        ]
        
        for pattern in sql_injection_patterns:
            import re
            if re.search(pattern, query):
                validation_time = (datetime.now() - start_time).total_seconds()
                return ContentValidationResult(
                    is_secure=False,
                    method="basic_query_injection_check",
                    reason="Query contains potential injection pattern",
                    suggestions=["Use parameterized queries", "Sanitize query input"],
                    validation_time=validation_time,
                    metadata={"pattern": pattern}
                )
        
        validation_time = (datetime.now() - start_time).total_seconds()
        return ContentValidationResult(
            is_secure=True,
            method="basic_query_validation",
            confidence=0.7,
            validation_time=validation_time
        )
