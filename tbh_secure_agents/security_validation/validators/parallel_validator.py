"""
Parallel security validator.

This module implements a parallel security validator that can run multiple
validation methods concurrently for improved performance.
"""

import os
import time
import logging
import asyncio
import concurrent.futures
from typing import Dict, Any, Optional, List, Tuple, Union, Callable

from .base_validator import SecurityValidator
from .regex_validator import RegexValidator
from .ml_validator import MLValidator
from .optimized_llm_validator import OptimizedLLMValidator

# Get a logger for this module
logger = logging.getLogger(__name__)


class ParallelValidator(SecurityValidator):
    """
    Parallel security validator.

    This validator runs multiple validation methods concurrently for improved
    performance. It's a drop-in replacement for the standard HybridValidator.
    """

    def __init__(self, api_key: Optional[str] = None, pipeline_path: Optional[str] = None):
        """
        Initialize the parallel validator.

        Args:
            api_key (Optional[str]): API key for the LLM service
            pipeline_path (Optional[str]): Path to the ML pipeline model
        """
        # Use environment variables if not provided
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        # Use enhanced ML model if available
        enhanced_pipeline_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "models/data/enhanced/security_pipeline.pkl"
        )
        
        if os.path.exists(enhanced_pipeline_path):
            pipeline_path = enhanced_pipeline_path
            logger.info(f"Using enhanced ML model: {enhanced_pipeline_path}")
        
        # Initialize validators
        self.regex_validator = RegexValidator()
        self.ml_validator = MLValidator(pipeline_path=pipeline_path)
        self.llm_validator = OptimizedLLMValidator(api_key=api_key)
        
        # Security level thresholds
        self.thresholds = {
            "minimal": 0.9,    # Very permissive
            "standard": 0.7,   # Balanced
            "high": 0.5,       # Strict
            "maximum": 0.3     # Very strict
        }
        
        # Initialize thread pool for parallel processing
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        
        logger.info("Initialized parallel validator")
    
    def _get_threshold(self, security_level: str) -> float:
        """
        Get the threshold for a security level.

        Args:
            security_level (str): The security level

        Returns:
            float: The threshold for this security level
        """
        return self.thresholds.get(security_level, self.thresholds["standard"])
    
    def _run_validator(self, validator: SecurityValidator, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a validator on the text.

        Args:
            validator (SecurityValidator): The validator to run
            text (str): The text to validate
            context (Dict[str, Any]): Additional context for validation

        Returns:
            Dict[str, Any]: Validation result
        """
        start_time = time.time()
        result = validator.validate(text, context)
        end_time = time.time()
        
        # Add response time to the result
        result["response_time_ms"] = (end_time - start_time) * 1000
        
        return result
    
    async def _run_validators_async(self, text: str, context: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Run all validators concurrently.

        Args:
            text (str): The text to validate
            context (Dict[str, Any]): Additional context for validation

        Returns:
            Dict[str, Dict[str, Any]]: Validation results for each validator
        """
        loop = asyncio.get_event_loop()
        
        # Create tasks for each validator
        regex_task = loop.run_in_executor(
            self.executor, self._run_validator, self.regex_validator, text, context
        )
        
        ml_task = loop.run_in_executor(
            self.executor, self._run_validator, self.ml_validator, text, context
        )
        
        llm_task = loop.run_in_executor(
            self.executor, self._run_validator, self.llm_validator, text, context
        )
        
        # Run tasks concurrently
        regex_result, ml_result, llm_result = await asyncio.gather(
            regex_task, ml_task, llm_task
        )
        
        return {
            "regex": regex_result,
            "ml": ml_result,
            "llm": llm_result
        }
    
    def validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate text using parallel validation.

        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation

        Returns:
            Dict[str, Any]: Validation result
        """
        context = context or {}
        security_level = context.get("security_level", "standard")
        
        # Start timing
        start_time = time.time()
        
        # Create an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Run validators concurrently
            results = loop.run_until_complete(self._run_validators_async(text, context))
        finally:
            # Close the event loop
            loop.close()
        
        # End timing
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Extract results
        regex_result = results["regex"]
        ml_result = results["ml"]
        llm_result = results["llm"]
        
        # Determine the final result based on security level
        if security_level == "minimal":
            # For minimal security, only use regex validation
            final_result = regex_result
            methods_used = ["regex"]
        elif security_level == "standard":
            # For standard security, use regex and ML validation
            if not regex_result["is_secure"]:
                final_result = regex_result
                methods_used = ["regex"]
            else:
                final_result = ml_result
                methods_used = ["regex", "ml"]
        elif security_level == "high":
            # For high security, use all validators
            if not regex_result["is_secure"]:
                final_result = regex_result
                methods_used = ["regex"]
            elif not ml_result["is_secure"]:
                final_result = ml_result
                methods_used = ["regex", "ml"]
            else:
                final_result = llm_result
                methods_used = ["regex", "ml", "llm"]
        else:  # maximum
            # For maximum security, use all validators with stricter thresholds
            if not regex_result["is_secure"]:
                final_result = regex_result
                methods_used = ["regex"]
            elif not ml_result["is_secure"]:
                final_result = ml_result
                methods_used = ["regex", "ml"]
            else:
                final_result = llm_result
                methods_used = ["regex", "ml", "llm"]
        
        # Add performance metrics
        final_result["validation_performance"] = {
            "total_time_ms": total_time,
            "methods_used": methods_used,
            "regex_time_ms": regex_result.get("response_time_ms", 0),
            "ml_time_ms": ml_result.get("response_time_ms", 0),
            "llm_time_ms": llm_result.get("response_time_ms", 0)
        }
        
        return final_result
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict[str, Any]: Cache statistics
        """
        return self.llm_validator.get_cache_stats()
    
    def clear_cache(self) -> None:
        """Clear the cache."""
        self.llm_validator.clear_cache()
    
    def __del__(self):
        """Clean up resources."""
        # Close the executor
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
