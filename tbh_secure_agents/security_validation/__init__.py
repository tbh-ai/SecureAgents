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
- SecurityUI: User interface for displaying validation results
- ReportGenerator: HTML report generation for security validation results
- RecommendationGenerator: LLM-based recommendation generation
- Integration: Functions for integrating with the existing framework
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
from .report_generator import SecurityReportGenerator
from .recommendation_generator import LLMRecommendationGenerator, generate_basic_recommendation
from .integration import (
    integrate_with_expert,
    integrate_with_squad,
    enable_hybrid_validation
)
from .hybrid_validator_improvements import enable_improved_hybrid_validation

__all__ = [
    'SecurityValidator',
    'BaseSecurityValidator',
    'RegexValidator',
    'MLValidator',
    'LLMValidator',
    'HybridValidator',
    'SecurityUI',
    'SecurityReportGenerator',
    'LLMRecommendationGenerator',
    'generate_basic_recommendation',
    'integrate_with_expert',
    'integrate_with_squad',
    'enable_hybrid_validation',
    'enable_improved_hybrid_validation'
]
