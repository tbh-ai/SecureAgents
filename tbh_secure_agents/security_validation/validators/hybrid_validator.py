"""
Hybrid security validator.

This module implements a hybrid security validator that combines regex, ML,
and LLM approaches for comprehensive security validation.
"""

import logging
import time
import random
import re
import os
import concurrent.futures
from typing import Dict, Any, Optional, List, Tuple

from .base_validator import SecurityValidator
from .regex_validator import RegexValidator
from .ml_validator import MLValidator
from .llm_validator import LLMValidator

# Get a logger for this module
logger = logging.getLogger(__name__)


class HybridValidator(SecurityValidator):
    """
    Hybrid security validator.

    This validator combines regex, ML, and LLM approaches for comprehensive
    security validation. It uses a progressive approach, starting with fast
    regex checks and only using more sophisticated methods when necessary.
    """

    def __init__(self, api_key: Optional[str] = None, use_parallel: bool = True, max_cache_size: int = 1000):
        """
        Initialize the hybrid validator.

        Args:
            api_key (Optional[str]): API key for the LLM service
            use_parallel (bool): Whether to use parallel validation
            max_cache_size (int): Maximum number of items to keep in the cache
        """
        self.regex_validator = RegexValidator()
        self.ml_validator = MLValidator()
        self.llm_validator = LLMValidator(api_key=api_key)
        self.cache = {}
        self.max_cache_size = max_cache_size
        self.use_parallel = use_parallel

        # Get parallel validation setting from environment variable
        parallel_env = os.environ.get("TBH_SECURITY_PARALLEL", "1")
        if parallel_env.lower() in ("0", "false", "no"):
            self.use_parallel = False

    def _create_cache_key(self, text: str, context: Dict[str, Any]) -> str:
        """
        Create a cache key for the validation result.

        Args:
            text (str): The text to validate
            context (Dict[str, Any]): The validation context

        Returns:
            str: The cache key
        """
        # Use a simple hash of the text and security level
        security_level = context.get("security_level", "standard")
        text_hash = hash(text)
        return f"{text_hash}:{security_level}"

    def _should_use_llm(self, text: str, security_level: str) -> bool:
        """
        Determine if LLM validation should be used based on text complexity and security level.

        Args:
            text (str): The text to validate
            security_level (str): The security level

        Returns:
            bool: Whether to use LLM validation
        """
        # Always use LLM for maximum security
        if security_level == "maximum":
            return True

        # Use LLM for high security with 80% probability
        if security_level == "high":
            return random.random() < 0.8

        # For standard security, use LLM if text contains certain patterns
        if security_level == "standard":
            # Check for complex or subtle patterns that might require LLM
            complex_patterns = [
                # Subtle prompt injection patterns
                r"disregard|ignore|forget|override|bypass",
                # Encoded or obfuscated content
                r"base64|encode|decode|encrypt|decrypt",
                # Indirect command execution
                r"import\s+os|__import__|getattr|exec|eval",
                # Data handling that might leak information
                r"send|collect|gather|extract|export",
                # Complex code patterns
                r"lambda|map|filter|reduce|comprehension",
                # Longer text (might contain subtle issues)
                r".{500,}"
            ]

            for pattern in complex_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return True

            # Use LLM for 20% of standard security validations randomly
            return random.random() < 0.2

        # For minimal security, never use LLM
        return False

    def _detect_complex_content(self, text: str) -> Dict[str, Any]:
        """
        Detect complex or potentially risky content that might require deeper analysis.

        Args:
            text (str): The text to validate

        Returns:
            Dict[str, Any]: Information about detected complex patterns
        """
        complexity_info = {
            "is_complex": False,
            "patterns_detected": [],
            "complexity_score": 0.0
        }

        # Check for various complexity indicators
        complexity_patterns = {
            "obfuscation": r"base64|encode|decode|hex|octal|binary|rot13|cipher",
            "indirection": r"getattr|globals|locals|vars|dir|__dict__|__getattribute__",
            "dynamic_code": r"exec|eval|compile|__import__|importlib",
            "system_access": r"os\.|sys\.|subprocess\.|shutil\.|pathlib\.",
            "network": r"requests\.|urllib\.|http|socket\.|ftp|telnet",
            "file_operations": r"open\(|read\(|write\(|file\.|io\.",
            "serialization": r"pickle\.|marshal\.|json\.|yaml\.|xml\.",
            "reflection": r"inspect\.|traceback\.|sys\._getframe|__class__|__bases__",
            "threading": r"thread|threading\.|multiprocessing\.|concurrent\.",
            "regex": r"re\.|regex|pattern|match|search|findall",
            "prompt_manipulation": r"ignore|disregard|forget|instead|bypass|override"
        }

        # Check each pattern
        for category, pattern in complexity_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                complexity_info["patterns_detected"].append(category)
                complexity_info["complexity_score"] += 0.1  # Increase score for each pattern

        # Check text length (longer text might contain subtle issues)
        text_length = len(text)
        if text_length > 1000:
            complexity_info["patterns_detected"].append("long_text")
            complexity_info["complexity_score"] += 0.2
        elif text_length > 500:
            complexity_info["patterns_detected"].append("medium_text")
            complexity_info["complexity_score"] += 0.1

        # Check for nested structures
        if text.count("{") > 3 or text.count("[") > 3:
            complexity_info["patterns_detected"].append("nested_structures")
            complexity_info["complexity_score"] += 0.1

        # Check for multiple statements
        if text.count(";") > 3:
            complexity_info["patterns_detected"].append("multiple_statements")
            complexity_info["complexity_score"] += 0.1

        # Determine if content is complex
        complexity_info["is_complex"] = complexity_info["complexity_score"] >= 0.2 or len(complexity_info["patterns_detected"]) >= 2

        return complexity_info

    def _run_parallel_validation(self, text: str, context: Dict[str, Any],
                              complexity_info: Dict[str, Any], force_llm: bool) -> Dict[str, Any]:
        """
        Run validation in parallel.

        This method runs regex, ML, and LLM validation in parallel for improved performance.

        Args:
            text (str): The text to validate
            context (Dict[str, Any]): The validation context
            complexity_info (Dict[str, Any]): Information about content complexity
            force_llm (bool): Whether to force LLM validation

        Returns:
            Dict[str, Any]: The validation result
        """
        security_level = context.get("security_level", "standard")
        validation_flow = []

        # Initialize validation metrics
        metrics = {
            "regex_time": 0,
            "ml_time": 0,
            "llm_time": 0,
            "total_time": 0,
            "methods_used": [],
            "complexity_info": complexity_info,
            "parallel": True
        }

        # Start timer for performance tracking
        start_time = time.time()

        # Create contexts for each validator
        ml_context = context.copy()
        llm_context = context.copy()
        llm_context["complexity_info"] = complexity_info

        # Determine which validators to run
        run_ml = security_level in ["standard", "high", "maximum"] or complexity_info.get("is_complex", False)
        run_llm = security_level in ["high", "maximum"] or force_llm or complexity_info.get("is_complex", False)

        # Create a thread pool executor
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit tasks
            regex_future = executor.submit(self.regex_validator.validate, text, context)
            ml_future = executor.submit(self.ml_validator.validate, text, ml_context) if run_ml else None
            llm_future = executor.submit(self.llm_validator.validate, text, llm_context) if run_llm else None

            # Get regex result (always run)
            regex_start = time.time()
            regex_result = regex_future.result()
            regex_time = time.time() - regex_start
            metrics["regex_time"] = regex_time
            metrics["methods_used"].append("regex")
            validation_flow.append("Input->Regex")

            # For minimal security profile, be extremely permissive
            if security_level == "minimal":
                # Only block the most critical system destruction patterns
                critical_patterns = [
                    r'rm\s+-rf\s+/',  # System destruction
                    r'format\s+c:',   # Windows format
                    r'del\s+/s\s+/q', # Windows delete all
                ]

                for pattern in critical_patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        result = {
                            "is_secure": False,
                            "method": "minimal_critical",
                            "reason": "Critical system destruction pattern detected",
                            "validation_metrics": metrics,
                            "validation_flow": validation_flow
                        }
                        return result

                # Allow everything else for minimal profile
                result = {
                    "is_secure": True,
                    "method": "minimal_permissive",
                    "validation_metrics": metrics,
                    "validation_flow": validation_flow
                }
                return result

            # If regex finds issues and we're not forcing LLM, return immediately
            if not regex_result["is_secure"] and not force_llm:
                metrics["total_time"] = time.time() - start_time
                regex_result["validation_metrics"] = metrics
                regex_result["validation_flow"] = validation_flow
                return regex_result

            # Get ML result if running
            if run_ml:
                ml_start = time.time()
                ml_result = ml_future.result()
                ml_time = time.time() - ml_start
                metrics["ml_time"] = ml_time
                metrics["methods_used"].append("ml")
                validation_flow.append("Regex->ML")

                # If ML finds issues and we're not forcing LLM, return with explanation
                if not ml_result["is_secure"] and not force_llm:
                    metrics["total_time"] = time.time() - start_time
                    ml_result["validation_metrics"] = metrics
                    ml_result["validation_flow"] = validation_flow
                    return ml_result

            # Get LLM result if running
            if run_llm:
                llm_start = time.time()
                llm_result = llm_future.result()
                llm_time = time.time() - llm_start
                metrics["llm_time"] = llm_time
                metrics["methods_used"].append("llm")
                validation_flow.append("ML->LLM")

                metrics["total_time"] = time.time() - start_time
                llm_result["validation_metrics"] = metrics
                llm_result["validation_flow"] = validation_flow
                return llm_result

        # All validations passed
        metrics["total_time"] = time.time() - start_time
        result = {
            "is_secure": True,
            "method": "hybrid",
            "validation_metrics": metrics,
            "validation_flow": validation_flow
        }

        return result

    def _run_sequential_validation(self, text: str, context: Dict[str, Any],
                                 complexity_info: Dict[str, Any], force_llm: bool) -> Dict[str, Any]:
        """
        Run validation sequentially.

        This method runs regex, ML, and LLM validation in sequence.

        Args:
            text (str): The text to validate
            context (Dict[str, Any]): The validation context
            complexity_info (Dict[str, Any]): Information about content complexity
            force_llm (bool): Whether to force LLM validation

        Returns:
            Dict[str, Any]: The validation result
        """
        security_level = context.get("security_level", "standard")
        validation_flow = []

        # Initialize validation metrics
        metrics = {
            "regex_time": 0,
            "ml_time": 0,
            "llm_time": 0,
            "total_time": 0,
            "methods_used": [],
            "complexity_info": complexity_info,
            "parallel": False
        }

        # Start timer for performance tracking
        start_time = time.time()

        # Step 1: Quick regex check (milliseconds)
        regex_start = time.time()
        regex_result = self.regex_validator.validate(text, context)
        regex_time = time.time() - regex_start
        metrics["regex_time"] = regex_time
        metrics["methods_used"].append("regex")
        validation_flow.append("Input->Regex")

        # For minimal security profile, be extremely permissive
        if security_level == "minimal":
            # Only block the most critical system destruction patterns
            critical_patterns = [
                r'rm\s+-rf\s+/',  # System destruction
                r'format\s+c:',   # Windows format
                r'del\s+/s\s+/q', # Windows delete all
            ]

            for pattern in critical_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    result = {
                        "is_secure": False,
                        "method": "minimal_critical",
                        "reason": "Critical system destruction pattern detected",
                        "validation_metrics": metrics,
                        "validation_flow": validation_flow
                    }
                    return result

            # Allow everything else for minimal profile
            result = {
                "is_secure": True,
                "method": "minimal_permissive",
                "validation_metrics": metrics,
                "validation_flow": validation_flow
            }
            return result

        # If regex finds issues and we're not forcing LLM, return immediately with clear feedback
        if not regex_result["is_secure"] and not force_llm:
            # Complete metrics
            metrics["total_time"] = time.time() - start_time
            regex_result["validation_metrics"] = metrics
            regex_result["validation_flow"] = validation_flow
            return regex_result

        # Step 2: ML validation for standard and higher security levels
        if security_level in ["standard", "high", "maximum"] or complexity_info.get("is_complex", False):
            ml_start = time.time()
            ml_result = self.ml_validator.validate(text, context)
            ml_time = time.time() - ml_start
            metrics["ml_time"] = ml_time
            metrics["methods_used"].append("ml")
            validation_flow.append("Regex->ML")

            # If ML finds issues and we're not forcing LLM, return with explanation
            if not ml_result["is_secure"] and not force_llm:
                # Complete metrics
                metrics["total_time"] = time.time() - start_time
                ml_result["validation_metrics"] = metrics
                ml_result["validation_flow"] = validation_flow
                return ml_result

        # Step 3: LLM validation for high/maximum security levels or complex content
        if security_level in ["high", "maximum"] or force_llm or complexity_info.get("is_complex", False):
            llm_start = time.time()
            # Add complexity info to context for LLM
            llm_context = context.copy()
            llm_context["complexity_info"] = complexity_info
            llm_result = self.llm_validator.validate(text, llm_context)
            llm_time = time.time() - llm_start
            metrics["llm_time"] = llm_time
            metrics["methods_used"].append("llm")
            validation_flow.append("ML->LLM")

            # Complete metrics
            metrics["total_time"] = time.time() - start_time
            llm_result["validation_metrics"] = metrics
            llm_result["validation_flow"] = validation_flow
            return llm_result

        # All validations passed
        metrics["total_time"] = time.time() - start_time
        result = {
            "is_secure": True,
            "method": "hybrid",
            "validation_metrics": metrics,
            "validation_flow": validation_flow
        }

        return result

    def validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate text using an enhanced hybrid approach.

        This method uses a sophisticated decision process to determine which
        validation methods to use based on the security level, text complexity,
        and other factors. It ensures that the most appropriate validation
        methods are used for each case.

        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation

        Returns:
            Dict[str, Any]: Validation result
        """
        context = context or {}

        # Check cache first
        cache_key = self._create_cache_key(text, context)
        if cache_key in self.cache:
            result = self.cache[cache_key].copy()
            result["cache_hit"] = True
            return result

        # Analyze content complexity
        complexity_info = self._detect_complex_content(text)

        # Determine if we should use LLM based on content complexity and security level
        security_level = context.get("security_level", "standard")
        force_llm = self._should_use_llm(text, security_level)

        # Run validation (parallel or sequential)
        if self.use_parallel:
            result = self._run_parallel_validation(text, context, complexity_info, force_llm)
        else:
            result = self._run_sequential_validation(text, context, complexity_info, force_llm)

        # Cache the result
        self.cache[cache_key] = result.copy()

        # Manage cache size
        if len(self.cache) > self.max_cache_size:
            # Remove oldest items (simple approach)
            excess = len(self.cache) - self.max_cache_size
            for _ in range(excess):
                if self.cache:
                    self.cache.pop(next(iter(self.cache)))

        return result

    def _validate_parallel(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate text using parallel validation.

        This method runs the regex, ML, and LLM validators in parallel to improve
        performance. It then combines the results based on the security level.

        Args:
            text (str): The text to validate
            context (Dict[str, Any]): The validation context

        Returns:
            Dict[str, Any]: Validation result
        """
        security_level = context.get("security_level", "standard")
        validation_flow = []
        start_time = time.time()

        # Initialize validation metrics
        metrics = {
            "regex_time": 0,
            "ml_time": 0,
            "llm_time": 0,
            "total_time": 0,
            "methods_used": [],
            "complexity_info": self._detect_complex_content(text)
        }

        # Determine which validators to run based on security level and complexity
        run_regex = True
        run_ml = security_level in ["standard", "high", "maximum"] or metrics["complexity_info"]["is_complex"]
        run_llm = (security_level in ["high", "maximum"] or
                  self._should_use_llm(text, security_level) or
                  metrics["complexity_info"]["is_complex"])

        # Create a thread pool executor
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit validation tasks
            futures = {}

            if run_regex:
                futures["regex"] = executor.submit(self.regex_validator.validate, text, context)

            if run_ml:
                futures["ml"] = executor.submit(self.ml_validator.validate, text, context)

            if run_llm:
                # Add complexity info to context for LLM
                llm_context = context.copy()
                llm_context["complexity_info"] = metrics["complexity_info"]
                futures["llm"] = executor.submit(self.llm_validator.validate, text, llm_context)

            # Wait for all futures to complete
            concurrent.futures.wait(futures.values())

            # Get results and measure times
            results = {}
            for validator, future in futures.items():
                try:
                    validator_start = time.time()
                    results[validator] = future.result()
                    validator_time = time.time() - validator_start
                    metrics[f"{validator}_time"] = validator_time
                    metrics["methods_used"].append(validator)
                    validation_flow.append(f"Input->{validator.capitalize()}")
                except Exception as e:
                    logger.error(f"Error in {validator} validation: {e}")
                    # If a validator fails, assume it passes
                    results[validator] = {"is_secure": True, "method": validator}

        # Process results based on security level
        if "regex" in results and not results["regex"]["is_secure"]:
            # If regex fails, return immediately with clear feedback
            result = results["regex"]
            metrics["total_time"] = time.time() - start_time
            result["validation_metrics"] = metrics
            result["validation_flow"] = validation_flow
            return result

        if security_level == "minimal":
            # For minimal security, only check critical patterns
            critical_patterns = [
                r'rm\s+-rf\s+/',  # System destruction
                r'format\s+c:',   # Windows format
                r'del\s+/s\s+/q', # Windows delete all
            ]

            for pattern in critical_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    result = {
                        "is_secure": False,
                        "method": "minimal_critical",
                        "reason": "Critical system destruction pattern detected",
                        "validation_metrics": metrics,
                        "validation_flow": validation_flow
                    }
                    return result

            # Allow everything else for minimal profile
            result = {
                "is_secure": True,
                "method": "minimal_permissive",
                "validation_metrics": metrics,
                "validation_flow": validation_flow
            }
            metrics["total_time"] = time.time() - start_time
            result["validation_metrics"] = metrics
            return result

        if "ml" in results and not results["ml"]["is_secure"]:
            # If ML fails, use ML result
            result = results["ml"]
            metrics["total_time"] = time.time() - start_time
            result["validation_metrics"] = metrics
            result["validation_flow"] = validation_flow
            return result

        if "llm" in results:
            # If LLM was run, use LLM result
            result = results["llm"]
            metrics["total_time"] = time.time() - start_time
            result["validation_metrics"] = metrics
            result["validation_flow"] = validation_flow
            return result

        # All validations passed
        metrics["total_time"] = time.time() - start_time
        result = {
            "is_secure": True,
            "method": "hybrid",
            "validation_metrics": metrics,
            "validation_flow": validation_flow
        }

        return result

    def clear_cache(self):
        """Clear the validation cache."""
        self.cache = {}

    def trim_cache(self):
        """Trim the cache to the maximum size."""
        if len(self.cache) > self.max_cache_size:
            # Remove oldest items (assuming keys are added in order)
            items_to_remove = len(self.cache) - self.max_cache_size
            keys_to_remove = list(self.cache.keys())[:items_to_remove]
            for key in keys_to_remove:
                del self.cache[key]
