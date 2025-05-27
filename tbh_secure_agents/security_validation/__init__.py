"""
Security validation package.

This package provides security validation for the TBH Secure Agents framework.
It includes validators for detecting security issues in text, as well as
utilities for displaying validation results and suggesting fixes.

The package uses a hybrid approach that combines regex, machine learning, and
large language models for comprehensive security validation. This approach
provides a balance between performance, accuracy, and user experience.

Key components:
- Validators: Different validation approaches (regex, ML, LLM, hybrid)
- SecurityValidator: Main interface for security validation
- SecurityUI: Minimal user interface for displaying validation results
- Integration: Functions for integrating with the existing framework
Pure security focus - no visualization bloat.
"""

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
