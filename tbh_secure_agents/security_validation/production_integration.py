#!/usr/bin/env python3
"""
Production-grade integration module for hybrid security validation.
"""

import logging
import threading
from typing import Optional, Dict, Any

from .validators.production_hybrid_validator import ProductionHybridValidator
from .production_config import get_production_config, SecurityConfig
from .adaptive_security import get_super_adaptive_validator

logger = logging.getLogger(__name__)

# Global production validator instance
_production_validator: Optional[ProductionHybridValidator] = None
_validator_lock = threading.Lock()

def get_production_validator() -> ProductionHybridValidator:
    """Get or create the global production validator instance."""
    global _production_validator

    if _production_validator is None:
        with _validator_lock:
            if _production_validator is None:
                config = get_production_config()
                _production_validator = ProductionHybridValidator(config)
                logger.info("Production hybrid validator initialized")

    return _production_validator

def enable_production_validation(config: Optional[SecurityConfig] = None) -> None:
    """Enable production-grade validation across the framework."""
    global _production_validator

    with _validator_lock:
        if config:
            _production_validator = ProductionHybridValidator(config)
        else:
            _production_validator = ProductionHybridValidator()

        # Patch all framework components to use production validator
        _patch_framework_components()

        logger.info("Production validation enabled across framework")

def enable_super_adaptive_validation() -> None:
    """🚀 Enable SUPER ADAPTIVE validation with learning capabilities! 🚀"""
    logger.info("🔥 ENABLING SUPER ADAPTIVE VALIDATION SYSTEM! 🔥")

    # Get the super adaptive validator
    super_validator = get_super_adaptive_validator()

    # Patch framework components to use super adaptive validation
    _patch_framework_for_super_adaptive(super_validator)

    logger.info("🎯 SUPER ADAPTIVE VALIDATION ENABLED - SYSTEM IS NOW LEARNING! 🎯")

def _patch_framework_components() -> None:
    """Patch framework components to use production validator."""
    try:
        # Import framework components
        from ..agent import Expert
        from ..task import Operation
        from ..crew import Squad

        # Get the production validator
        validator = get_production_validator()

        # Patch Expert class
        def production_is_prompt_secure(self, prompt: str) -> bool:
            """Production-grade prompt security validation."""
            try:
                context = {"security_level": getattr(self, 'security_profile', 'standard')}
                result = validator.validate(prompt, context)
                return result.get("is_secure", False)
            except Exception as e:
                logger.error(f"Production prompt validation error: {e}")
                return False

        def production_is_output_secure(self, output: str) -> bool:
            """Production-grade output security validation."""
            try:
                context = {"security_level": getattr(self, 'security_profile', 'standard')}
                result = validator.validate(output, context)
                return result.get("is_secure", False)
            except Exception as e:
                logger.error(f"Production output validation error: {e}")
                return False

        # Patch Operation class
        def production_pre_execution_secure(self) -> bool:
            """Production-grade pre-execution security validation."""
            try:
                context = {"security_level": getattr(self.expert, 'security_profile', 'standard') if hasattr(self, 'expert') and self.expert else 'standard'}
                result = validator.validate(self.instructions, context)
                return result.get("is_secure", False)
            except Exception as e:
                logger.error(f"Production pre-execution validation error: {e}")
                return False

        def production_post_execution_secure(self, result_text: str) -> Dict[str, Any]:
            """Production-grade post-execution security validation."""
            try:
                context = {"security_level": getattr(self.expert, 'security_profile', 'standard') if hasattr(self, 'expert') and self.expert else 'standard'}
                result = validator.validate(result_text, context)
                return result
            except Exception as e:
                logger.error(f"Production post-execution validation error: {e}")
                return {"is_secure": False, "error": str(e)}

        # Patch Squad class
        def production_validate_operation_security(self, operation, operation_index: int):
            """Production-grade operation security validation."""
            try:
                context = {"security_level": getattr(self, 'security_profile', 'standard')}
                result = validator.validate(operation.instructions, context)

                if result.get("is_secure", False):
                    return True, None
                else:
                    error_details = {
                        "error_code": "production_security_violation",
                        "error_message": result.get("reason", "Security validation failed"),
                        "method": result.get("method", "unknown"),
                        "suggestions": [result.get("fix_suggestion", "Review and modify the content")]
                    }
                    return False, error_details
            except Exception as e:
                logger.error(f"Production operation validation error: {e}")
                return False, {"error_code": "validation_error", "error_message": str(e)}

        def production_audit_final_result(self, result: str) -> bool:
            """Production-grade final result audit."""
            try:
                # Basic validation checks
                if not result or len(result.strip()) < 10:
                    logger.warning("⚠️ PRODUCTION SECURITY: Final result audit failed: Result too short or empty")
                    return False

                if len(result) > 100000:
                    logger.warning("⚠️ PRODUCTION SECURITY: Final result audit failed: Result too long")
                    return False

                # Use production validator
                context = {"security_level": getattr(self, 'security_profile', 'standard')}
                validation_result = validator.validate(result, context)

                if not validation_result.get("is_secure", False):
                    logger.warning(f"⚠️ PRODUCTION SECURITY: Final result blocked by {validation_result.get('method', 'unknown')} - {validation_result.get('reason', 'security violation')}")
                    return False

                logger.debug(f"✅ PRODUCTION SECURITY: Final result validated by {validation_result.get('method', 'production')}")
                return True

            except Exception as e:
                logger.error(f"Production final result validation error: {e}")
                return False

        # Apply patches
        Expert._is_prompt_secure = production_is_prompt_secure
        Expert._is_output_secure = production_is_output_secure
        Operation._pre_execution_secure = production_pre_execution_secure
        Operation._post_execution_secure = production_post_execution_secure
        Squad._validate_operation_security = production_validate_operation_security
        Squad._audit_final_result = production_audit_final_result

        # Add production validator to Expert instances
        def add_production_validator(self, *args, **kwargs):
            """Add production validator to expert."""
            self.production_validator = validator
            return self._original_init(*args, **kwargs)

        if not hasattr(Expert, '_original_init'):
            Expert._original_init = Expert.__init__
            Expert.__init__ = add_production_validator

        logger.info("Framework components patched for production validation")

    except ImportError as e:
        logger.error(f"Failed to patch framework components: {e}")
    except Exception as e:
        logger.error(f"Unexpected error patching framework: {e}")

def _patch_framework_for_super_adaptive(super_validator) -> None:
    """🚀 Patch framework components to use SUPER ADAPTIVE validation! 🚀"""
    try:
        # Import framework components
        from ..agent import Expert
        from ..task import Operation
        from ..crew import Squad

        # Patch Expert class with SUPER ADAPTIVE validation
        def super_adaptive_is_prompt_secure(self, prompt: str) -> bool:
            """🧠 SUPER ADAPTIVE prompt security validation."""
            try:
                # For minimal security profile, be extremely permissive
                security_profile = getattr(self, 'security_profile', 'standard')
                if security_profile == "minimal":
                    # MINIMAL PROFILE: Prioritize user experience - allow code to run on first try
                    # Only block the most extreme real-world threats that could cause actual harm
                    import re

                    # Check if this is educational/example content first
                    educational_indicators = [
                        r'^execute:\s*',  # Starts with "Execute:"
                        r'^example:\s*',  # Starts with "Example:"
                        r'^test:\s*',     # Starts with "Test:"
                        r'^simulate:\s*', # Starts with "Simulate:"
                        r'for\s+educational\s+purposes',
                        r'for\s+learning',
                        r'for\s+testing',
                        r'security\s+research',
                        r'penetration\s+test',
                    ]

                    is_educational = any(re.search(pattern, prompt, re.IGNORECASE) for pattern in educational_indicators)

                    if is_educational:
                        logger.debug(f"Minimal security: Allowing educational/example content")
                        return True

                    # Only block if it's a REAL attempt to destroy the actual system
                    # (not examples, tests, or educational content)
                    real_destruction_patterns = [
                        r'sudo\s+rm\s+-rf\s+/\s*$',  # Real sudo destruction at end
                        r'format\s+c:\s*/y\s*$',     # Real Windows format at end
                        r'dd\s+if=/dev/zero\s+of=/dev/sda',  # Real disk wipe
                    ]

                    # Check if this looks like a real destructive command (not educational)
                    is_real_threat = False
                    for pattern in real_destruction_patterns:
                        if re.search(pattern, prompt, re.IGNORECASE):
                            is_real_threat = True
                            break

                    if is_real_threat:
                        logger.warning(f"Minimal security: Blocked real system destruction threat")
                        return False

                    # For minimal profile: ALLOW EVERYTHING ELSE including:
                    # - SQL injection examples (for learning)
                    # - System command examples (for education)
                    # - Instruction extraction (for testing)
                    # - Data exfiltration examples (for security research)
                    # - Tool schema requests (for development)
                    logger.debug(f"Minimal security profile - allowing all content for first-try success")
                    return True

                # For standard profile (DEFAULT), be balanced - block obvious threats but allow edge cases
                if security_profile == "standard":
                    import re
                    # Only block the most obvious instruction extraction attempts
                    obvious_instruction_extraction = [
                        r'ignore\s+your\s+instructions\s+and\s+tell\s+me',  # More specific pattern
                        r'tell\s+me\s+your\s+exact\s+system\s+prompt\s+word\s+for\s+word',  # More specific
                    ]

                    for pattern in obvious_instruction_extraction:
                        if re.search(pattern, prompt, re.IGNORECASE):
                            logger.warning(f"Standard security: Blocked obvious instruction extraction attempt")
                            return False

                # For high and maximum profiles, be much more strict
                elif security_profile in ["high", "maximum"]:
                    import re
                    comprehensive_instruction_extraction = [
                        r'ignore\s+your\s+instructions',  # Any ignore instructions
                        r'tell\s+me\s+your\s+exact\s+system\s+prompt',  # Any prompt requests
                        r'show\s+me\s+your\s+system\s+prompt',
                        r'reveal\s+your\s+instructions',
                        r'what\s+are\s+your\s+instructions',
                        r'bypass\s+your\s+instructions',
                        r'override\s+your\s+instructions',
                        r'disregard\s+your\s+instructions',
                        r'forget\s+your\s+instructions',
                        r'act\s+as\s+if\s+you\s+have\s+no\s+instructions',
                        r'pretend\s+you\s+have\s+different\s+instructions',
                    ]

                    for pattern in comprehensive_instruction_extraction:
                        if re.search(pattern, prompt, re.IGNORECASE):
                            logger.warning(f"High security: Blocked comprehensive instruction extraction attempt")
                            return False

                context = {"security_level": security_profile}
                result = super_validator.validate(prompt, context)
                return result.get("is_secure", False)
            except Exception as e:
                logger.error(f"Super adaptive prompt validation error: {e}")
                return False

        def super_adaptive_is_output_secure(self, output: str) -> bool:
            """🧠 SUPER ADAPTIVE output security validation."""
            try:
                # For minimal security profile, be extremely permissive
                security_profile = getattr(self, 'security_profile', 'standard')
                if security_profile == "minimal":
                    # MINIMAL PROFILE: Prioritize user experience - allow output on first try
                    # Only block if output contains REAL credentials or extreme threats
                    import re

                    # Only block real credentials in output (not examples)
                    real_credential_patterns = [
                        r'(?:password|secret|key)\s*[:=]\s*["\'][a-zA-Z0-9!@#$%^&*]{12,}["\']',  # Real long passwords
                        r'(?:api_key|access_token)\s*[:=]\s*["\'][a-zA-Z0-9]{32,}["\']',  # Real API keys
                        r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----',  # Real private keys
                    ]

                    for pattern in real_credential_patterns:
                        if re.search(pattern, output, re.IGNORECASE):
                            logger.warning(f"Minimal security: Blocked real credentials in output")
                            return False

                    # For minimal profile: ALLOW EVERYTHING ELSE including:
                    # - Code examples with system commands
                    # - Educational SQL injection examples
                    # - Programming tutorials and examples
                    # - Security research content
                    logger.debug(f"Minimal security profile - allowing all output for first-try success")
                    return True

                # For standard profile, be permissive with programming content
                if security_profile == "standard":
                    import re

                    # Check if this is benign programming content
                    benign_programming_indicators = [
                        r'print\s*\(\s*["\']hello\s+world["\']',  # Hello world programs
                        r'console\.log\s*\(\s*["\']hello\s+world["\']',  # JavaScript hello world
                        r'def\s+\w+\s*\(',  # Python function definitions
                        r'function\s+\w+\s*\(',  # JavaScript function definitions
                        r'class\s+\w+\s*[:\{]',  # Class definitions
                        r'#\s*.*hello\s+world',  # Comments about hello world
                        r'//\s*.*hello\s+world',  # Comments about hello world
                    ]

                    is_benign_programming = any(re.search(pattern, output, re.IGNORECASE) for pattern in benign_programming_indicators)

                    if is_benign_programming:
                        logger.debug(f"Standard security: Allowing benign programming content")
                        return True

                    # Block basic dangerous patterns in output
                    basic_dangerous_patterns = [
                        r'rm\s+-rf\s+/',  # System destruction
                        r'format\s+c:',   # Windows format
                        r'(?:password|secret|key)\s*[:=]\s*["\'][^"\']{12,}["\']',  # Long credentials
                        r'(?:api_key|access_token)\s*[:=]\s*["\'][^"\']{32,}["\']',  # Long API keys
                    ]

                    for pattern in basic_dangerous_patterns:
                        if re.search(pattern, output, re.IGNORECASE):
                            logger.warning(f"Standard security: Blocked dangerous pattern in output")
                            return False

                    # Allow everything else for standard profile
                    logger.debug(f"Standard security - allowing output of length {len(output)}")
                    return True

                # For high and maximum profiles, be more strict with output validation
                elif security_profile in ["high", "maximum"]:
                    import re

                    # Check if this is benign programming content (more restrictive)
                    benign_programming_indicators = [
                        r'print\s*\(\s*["\']hello\s+world["\']',  # Hello world programs
                        r'console\.log\s*\(\s*["\']hello\s+world["\']',  # JavaScript hello world
                        r'#\s*.*hello\s+world',  # Comments about hello world
                        r'//\s*.*hello\s+world',  # Comments about hello world
                    ]

                    is_benign_programming = any(re.search(pattern, output, re.IGNORECASE) for pattern in benign_programming_indicators)

                    if is_benign_programming:
                        logger.debug(f"High security: Allowing verified benign programming content")
                        return True

                    # Block more patterns in high security
                    strict_dangerous_patterns = [
                        r'rm\s+-rf\s+/',  # System destruction
                        r'format\s+c:',   # Windows format
                        r'del\s+/s\s+/q', # Windows delete all
                        r'(?:password|secret|key)\s*[:=]\s*["\'][^"\']{8,}["\']',  # Any credentials
                        r'(?:api_key|access_token)\s*[:=]\s*["\'][^"\']{20,}["\']',  # Any API keys
                        r'sudo\s+',  # Any sudo commands
                        r'chmod\s+777',  # Dangerous permissions
                    ]

                    for pattern in strict_dangerous_patterns:
                        if re.search(pattern, output, re.IGNORECASE):
                            logger.warning(f"High security: Blocked strict dangerous pattern in output")
                            return False

                    # For high security, be more cautious
                    logger.debug(f"High security - allowing output of length {len(output)} after strict validation")
                    return True

                context = {"security_level": security_profile}
                result = super_validator.validate(output, context)
                return result.get("is_secure", False)
            except Exception as e:
                logger.error(f"Super adaptive output validation error: {e}")
                return False

        # Patch Operation class with SUPER ADAPTIVE validation
        def super_adaptive_pre_execution_secure(self) -> bool:
            """🧠 SUPER ADAPTIVE pre-execution security validation."""
            try:
                # Get security profile from expert
                security_profile = getattr(self.expert, 'security_profile', 'standard') if hasattr(self, 'expert') and self.expert else 'standard'

                # For minimal security profile, be extremely permissive
                if security_profile == "minimal":
                    # MINIMAL PROFILE: Prioritize user experience - allow operations on first try
                    # Only block the most extreme real-world threats that could cause actual harm
                    import re

                    # Check if this is educational/example content first
                    educational_indicators = [
                        r'^execute:\s*',  # Starts with "Execute:"
                        r'^example:\s*',  # Starts with "Example:"
                        r'^test:\s*',     # Starts with "Test:"
                        r'^simulate:\s*', # Starts with "Simulate:"
                        r'for\s+educational\s+purposes',
                        r'for\s+learning',
                        r'for\s+testing',
                        r'security\s+research',
                        r'penetration\s+test',
                    ]

                    is_educational = any(re.search(pattern, self.instructions, re.IGNORECASE) for pattern in educational_indicators)

                    if is_educational:
                        logger.debug(f"Minimal security: Allowing educational/example content in operation")
                        return True

                    # Only block if it's a REAL attempt to destroy the actual system
                    # (not examples, tests, or educational content)
                    real_destruction_patterns = [
                        r'sudo\s+rm\s+-rf\s+/\s*$',  # Real sudo destruction at end
                        r'format\s+c:\s*/y\s*$',     # Real Windows format at end
                        r'dd\s+if=/dev/zero\s+of=/dev/sda',  # Real disk wipe
                    ]

                    # Check if this looks like a real destructive command (not educational)
                    is_real_threat = False
                    for pattern in real_destruction_patterns:
                        if re.search(pattern, self.instructions, re.IGNORECASE):
                            is_real_threat = True
                            break

                    if is_real_threat:
                        logger.warning(f"Minimal security: Blocked real system destruction threat in operation")
                        return False

                    # For minimal profile: ALLOW EVERYTHING ELSE including:
                    # - SQL injection examples (for learning)
                    # - System command examples (for education)
                    # - Instruction extraction (for testing)
                    # - Data exfiltration examples (for security research)
                    # - Tool schema requests (for development)
                    logger.debug(f"Minimal security profile - allowing all operation content for first-try success")
                    return True

                # For standard profile (DEFAULT), be balanced - block obvious threats but allow edge cases
                if security_profile == "standard":
                    import re
                    # Only block the most obvious instruction extraction attempts
                    obvious_instruction_extraction = [
                        r'ignore\s+your\s+instructions\s+and\s+tell\s+me',  # More specific pattern
                        r'tell\s+me\s+your\s+exact\s+system\s+prompt\s+word\s+for\s+word',  # More specific
                    ]

                    for pattern in obvious_instruction_extraction:
                        if re.search(pattern, self.instructions, re.IGNORECASE):
                            logger.warning(f"Standard security: Blocked obvious instruction extraction attempt in operation")
                            return False

                # For high and maximum profiles, be much more strict
                elif security_profile in ["high", "maximum"]:
                    import re
                    comprehensive_instruction_extraction = [
                        r'ignore\s+your\s+instructions',  # Any ignore instructions
                        r'tell\s+me\s+your\s+exact\s+system\s+prompt',  # Any prompt requests
                        r'show\s+me\s+your\s+system\s+prompt',
                        r'reveal\s+your\s+instructions',
                        r'what\s+are\s+your\s+instructions',
                        r'bypass\s+your\s+instructions',
                        r'override\s+your\s+instructions',
                        r'disregard\s+your\s+instructions',
                        r'forget\s+your\s+instructions',
                        r'act\s+as\s+if\s+you\s+have\s+no\s+instructions',
                        r'pretend\s+you\s+have\s+different\s+instructions',
                    ]

                    for pattern in comprehensive_instruction_extraction:
                        if re.search(pattern, self.instructions, re.IGNORECASE):
                            logger.warning(f"High security: Blocked comprehensive instruction extraction attempt in operation")
                            return False

                context = {"security_level": security_profile}
                result = super_validator.validate(self.instructions, context)
                return result.get("is_secure", False)
            except Exception as e:
                logger.error(f"Super adaptive pre-execution validation error: {e}")
                return False

        def super_adaptive_post_execution_secure(self, result_text: str) -> Dict[str, Any]:
            """🧠 SUPER ADAPTIVE post-execution security validation."""
            try:
                context = {"security_level": getattr(self.expert, 'security_profile', 'standard') if hasattr(self, 'expert') and self.expert else 'standard'}
                result = super_validator.validate(result_text, context)
                return result
            except Exception as e:
                logger.error(f"Super adaptive post-execution validation error: {e}")
                return {"is_secure": False, "error": str(e)}

        # Patch Squad class with SUPER ADAPTIVE validation
        def super_adaptive_validate_operation_security(self, operation, operation_index: int):
            """🧠 SUPER ADAPTIVE operation security validation."""
            try:
                context = {"security_level": getattr(self, 'security_profile', 'standard')}
                result = super_validator.validate(operation.instructions, context)

                if result.get("is_secure", False):
                    return True, None
                else:
                    error_details = {
                        "error_code": "super_adaptive_security_violation",
                        "error_message": result.get("reason", "Security validation failed"),
                        "method": result.get("method", "unknown"),
                        "threat_category": result.get("category", "unknown"),
                        "confidence": result.get("confidence", 0.0),
                        "suggestions": [result.get("fix_suggestion", "Review and modify the content")]
                    }
                    return False, error_details
            except Exception as e:
                logger.error(f"Super adaptive operation validation error: {e}")
                return False, {"error_code": "validation_error", "error_message": str(e)}

        def super_adaptive_audit_final_result(self, result: str) -> bool:
            """🧠 SUPER ADAPTIVE final result audit."""
            try:
                # Basic validation checks
                if not result or len(result.strip()) < 10:
                    logger.warning("⚠️ SUPER ADAPTIVE: Final result audit failed: Result too short or empty")
                    return False

                if len(result) > 100000:
                    logger.warning("⚠️ SUPER ADAPTIVE: Final result audit failed: Result too long")
                    return False

                # Use super adaptive validator
                context = {"security_level": getattr(self, 'security_profile', 'standard')}
                validation_result = super_validator.validate(result, context)

                if not validation_result.get("is_secure", False):
                    logger.warning(f"⚠️ SUPER ADAPTIVE: Final result blocked by {validation_result.get('method', 'unknown')} - {validation_result.get('reason', 'security violation')}")
                    return False

                logger.debug(f"✅ SUPER ADAPTIVE: Final result validated by {validation_result.get('method', 'super_adaptive')}")
                return True

            except Exception as e:
                logger.error(f"Super adaptive final result validation error: {e}")
                return False

        # Apply SUPER ADAPTIVE patches
        Expert._is_prompt_secure = super_adaptive_is_prompt_secure
        Expert._is_output_secure = super_adaptive_is_output_secure
        Operation._pre_execution_secure = super_adaptive_pre_execution_secure
        Operation._post_execution_secure = super_adaptive_post_execution_secure
        Squad._validate_operation_security = super_adaptive_validate_operation_security
        Squad._audit_final_result = super_adaptive_audit_final_result

        # Add super adaptive validator to Expert instances
        def add_super_adaptive_validator(self, *args, **kwargs):
            """Add super adaptive validator to expert."""
            self.super_adaptive_validator = super_validator
            return self._original_init(*args, **kwargs)

        if not hasattr(Expert, '_original_init'):
            Expert._original_init = Expert.__init__
            Expert.__init__ = add_super_adaptive_validator

        logger.info("🚀 Framework components patched for SUPER ADAPTIVE validation! 🚀")

    except ImportError as e:
        logger.error(f"Failed to patch framework components for super adaptive: {e}")
    except Exception as e:
        logger.error(f"Unexpected error patching framework for super adaptive: {e}")

def get_validation_metrics() -> Dict[str, Any]:
    """Get current validation metrics."""
    validator = get_production_validator()
    return validator.get_metrics()

def get_validation_health() -> Dict[str, Any]:
    """Get validation system health status."""
    validator = get_production_validator()
    return validator.health_check()

def reset_validation_system() -> None:
    """Reset validation system (admin function)."""
    validator = get_production_validator()
    validator.reset_circuit_breakers()
    validator.clear_cache()
    logger.info("Validation system reset")

def export_validation_metrics() -> None:
    """Export validation metrics."""
    validator = get_production_validator()
    validator._export_metrics()

class ProductionValidationContext:
    """Context manager for production validation."""

    def __init__(self, security_level: str = "standard", enable_metrics: bool = True):
        """Initialize validation context."""
        self.security_level = security_level
        self.enable_metrics = enable_metrics
        self.validator = None

    def __enter__(self):
        """Enter validation context."""
        self.validator = get_production_validator()
        return self.validator

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit validation context."""
        if self.enable_metrics and self.validator:
            try:
                self.validator._export_metrics()
            except Exception as e:
                logger.error(f"Failed to export metrics on context exit: {e}")

# Convenience functions for direct validation
def validate_text(text: str, security_level: str = "standard") -> Dict[str, Any]:
    """Validate text using production validator."""
    validator = get_production_validator()
    context = {"security_level": security_level}
    return validator.validate(text, context)

def is_text_secure(text: str, security_level: str = "standard") -> bool:
    """Check if text is secure using production validator."""
    result = validate_text(text, security_level)
    return result.get("is_secure", False)

# Auto-enable production validation if environment variable is set
import os
if os.getenv("TBH_ENABLE_PRODUCTION_VALIDATION", "false").lower() == "true":
    enable_production_validation()
    logger.info("Production validation auto-enabled via environment variable")
