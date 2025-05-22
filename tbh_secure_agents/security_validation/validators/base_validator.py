"""
Base validator interface for security validation.

This module defines the base interface for all security validators in the
TBH Secure Agents framework. All validators must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class SecurityValidator(ABC):
    """
    Base class for all security validators.
    
    All security validators must implement the validate method, which takes
    text to validate and optional context information, and returns a validation
    result dictionary.
    """
    
    @abstractmethod
    def validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate text for security issues.
        
        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation
                This may include:
                - security_level: The security level (minimal, standard, high, maximum)
                - validation_type: The type of validation (prompt, output, etc.)
                - expert_specialty: The specialty of the expert
                - operation_index: The index of the operation
                
        Returns:
            Dict[str, Any]: Validation result with at least an "is_secure" boolean
                The result should include:
                - is_secure: Whether the text passed validation
                - method: The validation method used
                - reason: The reason for failure (if is_secure is False)
                - Additional method-specific information
        """
        pass
    
    def get_name(self) -> str:
        """
        Get the name of the validator.
        
        Returns:
            str: The name of the validator
        """
        return self.__class__.__name__
