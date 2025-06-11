"""
TBH SecureAgents - Enterprise-grade secure multi-agent framework

Version: 0.5.4

This package provides a secure multi-agent framework with ML-powered security validation.
It includes validators for detecting security issues in text, as well as
utilities for displaying validation results and suggesting fixes.

The framework uses a hybrid approach that combines regex, machine learning, and
large language models for comprehensive security validation. This approach
provides a balance between performance, accuracy, and user experience.

Key components:
- Validators: Different validation approaches (regex, ML, LLM, hybrid)
- SecurityValidator: Main interface for security validation
- Expert Agents: Specialized AI agents with configurable security profiles
- Squad Operations: Orchestrate multiple agents with secure communication
- Memory Systems: Advanced memory capabilities with automatic storage
- Dynamic Guardrails: Runtime security controls and constraint enforcement

Example usage:
    >>> from tbh_secure_agents import Expert, Squad
    >>> expert = Expert(specialty="Security Analyst", security_profile="high")
    >>> response = expert.analyze("Check this code for security issues")
"""

__version__ = "0.5.4"

from .validators import (
    SecurityValidator as BaseSecurityValidator,
    RegexValidator,
    MLValidator,
    LLMValidator,
    HybridValidator
)
from .utils import SecurityUI
from .security_validator import SecurityValidator
from .integration import (
    integrate_with_expert,
    integrate_with_squad,
    enable_hybrid_validation
)
from .adaptive_security import (
    get_next_gen_adaptive_validator,
    get_next_gen_adaptive_engine,
    NextGenAdaptiveValidator,
    NextGenAdaptiveSecurityEngine
)

__all__ = [
    'SecurityValidator',
    'BaseSecurityValidator',
    'RegexValidator',
    'MLValidator',
    'LLMValidator',
    'HybridValidator',
    'SecurityUI',
    'integrate_with_expert',
    'integrate_with_squad',
    'enable_hybrid_validation',
    'get_next_gen_adaptive_validator',
    'get_next_gen_adaptive_engine',
    'NextGenAdaptiveValidator',
    'NextGenAdaptiveSecurityEngine'
]
