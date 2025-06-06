"""
TBH Secure Agents v5.0 - Memory Security Manager

Provides comprehensive security management for the memory system by integrating
with the existing 4-layer hybrid security validation system.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass

from ..models import MemoryEntry, MemoryType, MemoryPriority, MemoryAccess
from ..config import MemorySystemConfig
from .memory_validator import MemoryValidator
from .encryption_manager import MemoryEncryptionManager
from .access_control import MemoryAccessController
from .audit_logger import MemoryAuditLogger


logger = logging.getLogger(__name__)


@dataclass
class SecurityValidationResult:
    """Result of memory security validation"""
    is_secure: bool
    validation_level: str
    method: str
    reason: Optional[str] = None
    suggestions: List[str] = None
    risk_score: float = 0.0
    validation_time: float = 0.0
    metadata: Dict[str, Any] = None


@dataclass
class MemorySecurityEvent:
    """Security event for memory operations"""
    event_type: str
    user_id: str
    memory_key: str
    memory_type: MemoryType
    event_time: datetime
    security_level: str
    success: bool
    details: Dict[str, Any]
    risk_score: float = 0.0


class MemorySecurityManager:
    """
    Comprehensive security manager for the memory system.
    
    Integrates with the existing TBH Secure Agents 4-layer hybrid security
    validation system to provide:
    - Content validation using Regex + ML + LLM + Adaptive layers
    - Encryption/decryption for sensitive memory content
    - Access control and authorization
    - Security event logging and monitoring
    - Risk assessment and threat detection
    """
    
    def __init__(self, config: MemorySystemConfig):
        self.config = config
        
        # Initialize security components
        self.validator = MemoryValidator(config)
        self.encryption_manager = MemoryEncryptionManager(config)
        self.access_controller = MemoryAccessController(config)
        self.audit_logger = MemoryAuditLogger(config)
        
        # Security state tracking
        self._security_events: List[MemorySecurityEvent] = []
        self._blocked_patterns: Set[str] = set()
        self._trusted_users: Set[str] = set()
        self._risk_scores: Dict[str, float] = {}
        
        logger.info("MemorySecurityManager initialized with hybrid validation")
    
    async def validate_memory_entry(
        self, 
        entry: MemoryEntry, 
        operation: str = "store"
    ) -> SecurityValidationResult:
        """
        Validate a memory entry using the 4-layer hybrid security system.
        
        Args:
            entry: The memory entry to validate
            operation: The operation being performed (store, retrieve, update, delete)
            
        Returns:
            SecurityValidationResult with validation details
        """
        start_time = datetime.now()
        
        try:
            # Determine security level based on memory type and configuration
            security_level = self._get_security_level(entry)
            
            # Validate content using hybrid security validation
            content_result = await self.validator.validate_content(
                content=entry.content,
                memory_type=entry.memory_type,
                security_level=security_level,
                context={
                    "user_id": entry.user_id,
                    "memory_key": entry.key,
                    "operation": operation,
                    "tags": entry.tags,
                    "priority": entry.metadata.priority.value
                }
            )
            
            # Validate access permissions
            access_result = await self.access_controller.validate_access(
                user_id=entry.user_id,
                memory_key=entry.key,
                memory_type=entry.memory_type,
                access_level=entry.metadata.access_level,
                operation=operation
            )
            
            # Calculate overall risk score
            risk_score = self._calculate_risk_score(
                content_result, access_result, entry, operation
            )
            
            # Determine if entry is secure
            is_secure = (
                content_result.is_secure and 
                access_result.is_allowed and
                risk_score < self.config.security.max_acceptable_risk_score
            )
            
            # Create validation result
            validation_time = (datetime.now() - start_time).total_seconds()
            result = SecurityValidationResult(
                is_secure=is_secure,
                validation_level=security_level,
                method=content_result.method,
                reason=content_result.reason if not is_secure else None,
                suggestions=content_result.suggestions or [],
                risk_score=risk_score,
                validation_time=validation_time,
                metadata={
                    "content_validation": content_result.to_dict(),
                    "access_validation": access_result.to_dict(),
                    "operation": operation
                }
            )
            
            # Log security event
            await self._log_security_event(
                event_type=f"memory_{operation}_validation",
                user_id=entry.user_id,
                memory_key=entry.key,
                memory_type=entry.memory_type,
                success=is_secure,
                security_level=security_level,
                details={
                    "validation_result": result.metadata,
                    "risk_score": risk_score
                },
                risk_score=risk_score
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Memory security validation failed: {e}")
            
            # Log failure event
            await self._log_security_event(
                event_type=f"memory_{operation}_validation_error",
                user_id=entry.user_id,
                memory_key=entry.key,
                memory_type=entry.memory_type,
                success=False,
                security_level="unknown",
                details={"error": str(e)},
                risk_score=1.0  # Maximum risk for errors
            )
            
            # Return secure=False on any error
            validation_time = (datetime.now() - start_time).total_seconds()
            return SecurityValidationResult(
                is_secure=False,
                validation_level="error",
                method="error_handler",
                reason=f"Security validation error: {str(e)}",
                suggestions=["Contact system administrator"],
                risk_score=1.0,
                validation_time=validation_time,
                metadata={"error": str(e)}
            )
    
    async def encrypt_memory_entry(self, entry: MemoryEntry) -> MemoryEntry:
        """Encrypt sensitive memory entry content"""
        if not self.config.security.enable_encryption:
            return entry
            
        if self._requires_encryption(entry):
            encrypted_entry = await self.encryption_manager.encrypt_entry(entry)
            
            # Log encryption event
            await self._log_security_event(
                event_type="memory_encryption",
                user_id=entry.user_id,
                memory_key=entry.key,
                memory_type=entry.memory_type,
                success=True,
                security_level=self._get_security_level(entry),
                details={"encryption_applied": True}
            )
            
            return encrypted_entry
        
        return entry
    
    async def decrypt_memory_entry(self, entry: MemoryEntry) -> MemoryEntry:
        """Decrypt memory entry content if encrypted"""
        if entry.is_encrypted:
            decrypted_entry = await self.encryption_manager.decrypt_entry(entry)
            
            # Log decryption event
            await self._log_security_event(
                event_type="memory_decryption",
                user_id=entry.user_id,
                memory_key=entry.key,
                memory_type=entry.memory_type,
                success=True,
                security_level=self._get_security_level(entry),
                details={"decryption_applied": True}
            )
            
            return decrypted_entry
            
        return entry
    
    async def validate_memory_access(
        self,
        user_id: str,
        memory_key: str,
        memory_type: MemoryType,
        operation: str
    ) -> Tuple[bool, str]:
        """
        Validate if a user can perform an operation on a memory entry.
        
        Returns:
            Tuple of (is_allowed, reason)
        """
        try:
            result = await self.access_controller.validate_operation(
                user_id=user_id,
                memory_key=memory_key,
                memory_type=memory_type,
                operation=operation
            )
            
            # Log access attempt
            await self._log_security_event(
                event_type=f"memory_access_{operation}",
                user_id=user_id,
                memory_key=memory_key,
                memory_type=memory_type,
                success=result.is_allowed,
                security_level="standard",
                details={
                    "operation": operation,
                    "access_result": result.to_dict()
                }
            )
            
            return result.is_allowed, result.reason
            
        except Exception as e:
            logger.error(f"Memory access validation failed: {e}")
            
            # Log error event
            await self._log_security_event(
                event_type=f"memory_access_error",
                user_id=user_id,
                memory_key=memory_key,
                memory_type=memory_type,
                success=False,
                security_level="error",
                details={"error": str(e)},
                risk_score=1.0
            )
            
            return False, f"Access validation error: {str(e)}"
    
    async def get_security_metrics(self) -> Dict[str, Any]:
        """Get comprehensive security metrics for the memory system"""
        return {
            "total_security_events": len(self._security_events),
            "blocked_operations": len([e for e in self._security_events if not e.success]),
            "average_risk_score": sum(self._risk_scores.values()) / len(self._risk_scores) if self._risk_scores else 0.0,
            "high_risk_users": [uid for uid, score in self._risk_scores.items() if score > 0.7],
            "security_levels_used": list(set(e.security_level for e in self._security_events)),
            "encryption_events": len([e for e in self._security_events if "encryption" in e.event_type]),
            "validation_errors": len([e for e in self._security_events if "error" in e.event_type]),
            "trusted_users": len(self._trusted_users),
            "blocked_patterns": len(self._blocked_patterns)
        }
    
    def _get_security_level(self, entry: MemoryEntry) -> str:
        """Determine security level based on memory type and configuration"""
        # Map memory types to security levels
        type_security_mapping = {
            MemoryType.SESSION: "minimal",
            MemoryType.WORKING: "standard", 
            MemoryType.PREFERENCE: "standard",
            MemoryType.LONG_TERM: "high",
            MemoryType.PATTERN: "high"
        }
        
        base_level = type_security_mapping.get(entry.memory_type, "standard")
        
        # Escalate security level based on priority
        if entry.metadata.priority in [MemoryPriority.CRITICAL, MemoryPriority.HIGH]:
            if base_level == "minimal":
                return "standard"
            elif base_level == "standard":
                return "high"
            elif base_level == "high":
                return "maximum"
        
        # Escalate for sensitive access levels
        if entry.metadata.access_level == MemoryAccess.PRIVATE:
            if base_level == "minimal":
                return "standard"
        
        return base_level
    
    def _requires_encryption(self, entry: MemoryEntry) -> bool:
        """Determine if memory entry requires encryption"""
        if not self.config.security.enable_encryption:
            return False
            
        # Always encrypt certain memory types
        encrypt_types = {MemoryType.LONG_TERM, MemoryType.PATTERN}
        if entry.memory_type in encrypt_types:
            return True
            
        # Encrypt high priority entries
        if entry.metadata.priority in [MemoryPriority.CRITICAL, MemoryPriority.HIGH]:
            return True
            
        # Encrypt private access level entries
        if entry.metadata.access_level == MemoryAccess.PRIVATE:
            return True
            
        return False
    
    def _calculate_risk_score(
        self,
        content_result: Any,
        access_result: Any,
        entry: MemoryEntry,
        operation: str
    ) -> float:
        """Calculate overall risk score for memory operation"""
        risk_score = 0.0
        
        # Content risk
        if hasattr(content_result, 'risk_score'):
            risk_score += content_result.risk_score * 0.6
        elif not content_result.is_secure:
            risk_score += 0.8
            
        # Access risk
        if hasattr(access_result, 'risk_score'):
            risk_score += access_result.risk_score * 0.2
        elif not access_result.is_allowed:
            risk_score += 0.3
            
        # Memory type risk
        type_risk = {
            MemoryType.SESSION: 0.1,
            MemoryType.WORKING: 0.2,
            MemoryType.PREFERENCE: 0.2,
            MemoryType.LONG_TERM: 0.3,
            MemoryType.PATTERN: 0.4
        }
        risk_score += type_risk.get(entry.memory_type, 0.2) * 0.1
        
        # Operation risk
        operation_risk = {
            "store": 0.2,
            "retrieve": 0.1,
            "update": 0.3,
            "delete": 0.4
        }
        risk_score += operation_risk.get(operation, 0.2) * 0.1
        
        # User history risk
        user_risk = self._risk_scores.get(entry.user_id, 0.0)
        risk_score += user_risk * 0.1
        
        return min(risk_score, 1.0)  # Cap at 1.0
    
    async def _log_security_event(
        self,
        event_type: str,
        user_id: str,
        memory_key: str,
        memory_type: MemoryType,
        success: bool,
        security_level: str,
        details: Dict[str, Any],
        risk_score: float = 0.0
    ):
        """Log security event for audit trail"""
        event = MemorySecurityEvent(
            event_type=event_type,
            user_id=user_id,
            memory_key=memory_key,
            memory_type=memory_type,
            event_time=datetime.now(),
            security_level=security_level,
            success=success,
            details=details,
            risk_score=risk_score
        )
        
        # Add to local tracking
        self._security_events.append(event)
        
        # Update user risk score
        if user_id not in self._risk_scores:
            self._risk_scores[user_id] = 0.0
            
        if not success:
            self._risk_scores[user_id] = min(
                self._risk_scores[user_id] + 0.1, 1.0
            )
        else:
            self._risk_scores[user_id] = max(
                self._risk_scores[user_id] - 0.01, 0.0
            )
        
        # Log to audit system
        await self.audit_logger.log_event(event)
        
        # Clean up old events (keep last 10000)
        if len(self._security_events) > 10000:
            self._security_events = self._security_events[-10000:]
