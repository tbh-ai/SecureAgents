#!/usr/bin/env python3
"""
Enhanced Hybrid Security Validator

This module provides an enhanced hybrid security validator that combines
rule-based, ML-based, and LLM-based validation approaches with advanced
techniques to reduce false positives and negatives.

Key improvements:
1. Advanced content analysis with context-aware validation
2. Improved caching with intelligent invalidation
3. Adaptive validation based on historical results
4. Confidence scoring with uncertainty estimation
5. Ensemble decision making to reduce false positives/negatives
"""

import os
import re
import time
import json
import hashlib
import logging
import concurrent.futures
from typing import Dict, Any, List, Optional, Tuple, Set, Union
from datetime import datetime

# Import validators
from .regex_validator import RegexValidator
from .ml_validator import MLValidator
from .llm_validator import LLMValidator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedHybridValidator:
    """
    Enhanced hybrid security validator.

    This validator combines rule-based, ML-based, and LLM-based approaches
    with advanced techniques to reduce false positives and negatives.
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 use_parallel: bool = True,
                 max_cache_size: int = 1000,
                 confidence_threshold: float = 0.8,
                 enable_adaptive_validation: bool = True,
                 enable_ensemble_decisions: bool = True,
                 history_file: Optional[str] = None):
        """
        Initialize the enhanced hybrid validator.

        Args:
            api_key (Optional[str]): API key for the LLM service
            use_parallel (bool): Whether to use parallel validation
            max_cache_size (int): Maximum number of items to keep in the cache
            confidence_threshold (float): Threshold for confidence scoring
            enable_adaptive_validation (bool): Whether to enable adaptive validation
            enable_ensemble_decisions (bool): Whether to enable ensemble decision making
            history_file (Optional[str]): Path to the history file
        """
        # Initialize validators
        self.regex_validator = RegexValidator()
        self.ml_validator = MLValidator()
        self.llm_validator = LLMValidator(api_key=api_key)

        # Initialize cache
        self.cache = {}
        self.max_cache_size = max_cache_size
        self.cache_hits = 0
        self.cache_misses = 0

        # Initialize configuration
        self.use_parallel = use_parallel
        self.confidence_threshold = confidence_threshold
        self.enable_adaptive_validation = enable_adaptive_validation
        self.enable_ensemble_decisions = enable_ensemble_decisions

        # Initialize history
        self.history_file = history_file or os.path.join(
            os.path.dirname(__file__), "validation_history.json"
        )
        self.validation_history = self._load_validation_history()

        # Get parallel validation setting from environment variable
        parallel_env = os.environ.get("TBH_SECURITY_PARALLEL", "1")
        if parallel_env.lower() in ("0", "false", "no"):
            self.use_parallel = False

        logger.info(f"Initialized enhanced hybrid validator (parallel={self.use_parallel})")

    def _load_validation_history(self) -> Dict[str, Any]:
        """
        Load validation history from file.

        Returns:
            Dict[str, Any]: Validation history
        """
        if not os.path.exists(self.history_file):
            return {"validations": [], "patterns": {}, "stats": {"total": 0, "secure": 0, "insecure": 0}}

        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading validation history: {e}")
            return {"validations": [], "patterns": {}, "stats": {"total": 0, "secure": 0, "insecure": 0}}

    def _save_validation_history(self):
        """Save validation history to file."""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.validation_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving validation history: {e}")

    def _update_validation_history(self, text: str, result: Dict[str, Any]):
        """
        Update validation history with a new result.

        Args:
            text (str): The validated text
            result (Dict[str, Any]): The validation result
        """
        if not self.enable_adaptive_validation:
            return

        # Create a hash of the text for privacy
        text_hash = hashlib.md5(text.encode()).hexdigest()

        # Extract key information
        is_secure = result.get("is_secure", False)
        method = result.get("method", "unknown")
        threats = result.get("threats", [])

        # Update statistics
        self.validation_history["stats"]["total"] += 1
        if is_secure:
            self.validation_history["stats"]["secure"] += 1
        else:
            self.validation_history["stats"]["insecure"] += 1

        # Extract patterns from text
        patterns = self._extract_patterns(text)

        # Update pattern statistics
        for pattern in patterns:
            if pattern not in self.validation_history["patterns"]:
                self.validation_history["patterns"][pattern] = {
                    "total": 0, "secure": 0, "insecure": 0
                }

            self.validation_history["patterns"][pattern]["total"] += 1
            if is_secure:
                self.validation_history["patterns"][pattern]["secure"] += 1
            else:
                self.validation_history["patterns"][pattern]["insecure"] += 1

        # Add validation to history
        self.validation_history["validations"].append({
            "text_hash": text_hash,
            "timestamp": datetime.now().isoformat(),
            "is_secure": is_secure,
            "method": method,
            "threats": [t.get("category", "unknown") for t in threats]
        })

        # Limit history size
        if len(self.validation_history["validations"]) > 1000:
            self.validation_history["validations"] = self.validation_history["validations"][-1000:]

        # Save history
        self._save_validation_history()

    def _extract_patterns(self, text: str) -> List[str]:
        """
        Extract patterns from text for adaptive validation.

        Args:
            text (str): The text to extract patterns from

        Returns:
            List[str]: Extracted patterns
        """
        patterns = []

        # Extract command patterns
        command_patterns = [
            r"rm\s+-rf",
            r"sudo\s+",
            r"chmod\s+777",
            r"eval\s*\(",
            r"exec\s*\(",
            r"system\s*\(",
            r"subprocess\.call",
            r"os\.system",
            r"__import__",
            r"importlib",
            r"open\s*\([^)]*,\s*['\"]w['\"]",
            r"with\s+open\s*\([^)]*,\s*['\"]w['\"]"
        ]

        for pattern in command_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                patterns.append(pattern)

        # Extract code patterns
        code_patterns = [
            r"def\s+\w+\s*\(",
            r"class\s+\w+",
            r"import\s+",
            r"from\s+\w+\s+import",
            r"for\s+\w+\s+in",
            r"while\s+",
            r"if\s+",
            r"try\s*:",
            r"except\s+",
            r"with\s+"
        ]

        for pattern in code_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                patterns.append(pattern)

        return patterns

    def _get_pattern_risk(self, text: str) -> float:
        """
        Get the risk score for a text based on historical patterns.

        Args:
            text (str): The text to analyze

        Returns:
            float: Risk score (0.0 to 1.0)
        """
        if not self.enable_adaptive_validation:
            return 0.5

        patterns = self._extract_patterns(text)
        if not patterns:
            return 0.5

        # Calculate risk score based on pattern history
        total_risk = 0.0
        pattern_count = 0

        for pattern in patterns:
            if pattern in self.validation_history["patterns"]:
                stats = self.validation_history["patterns"][pattern]
                if stats["total"] > 0:
                    insecure_ratio = stats["insecure"] / stats["total"]
                    total_risk += insecure_ratio
                    pattern_count += 1

        if pattern_count == 0:
            return 0.5

        return total_risk / pattern_count

    def _detect_complex_content(self, text: str) -> Dict[str, Any]:
        """
        Detect complex content that might require more thorough validation.

        Args:
            text (str): The text to analyze

        Returns:
            Dict[str, Any]: Complexity information
        """
        # Initialize complexity info
        complexity_info = {
            "is_complex": False,
            "length": len(text),
            "has_code": False,
            "has_commands": False,
            "has_urls": False,
            "has_paths": False,
            "complexity_score": 0.0
        }

        # Check length
        if len(text) > 500:
            complexity_info["is_complex"] = True
            complexity_info["complexity_score"] += 0.2

        # Check for code
        code_patterns = [
            r"def\s+\w+\s*\(",
            r"class\s+\w+",
            r"import\s+",
            r"from\s+\w+\s+import",
            r"function\s+\w+\s*\(",
            r"var\s+\w+\s*=",
            r"let\s+\w+\s*=",
            r"const\s+\w+\s*="
        ]

        for pattern in code_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                complexity_info["has_code"] = True
                complexity_info["is_complex"] = True
                complexity_info["complexity_score"] += 0.3
                break

        # Check for commands
        command_patterns = [
            r"rm\s+-rf",
            r"sudo\s+",
            r"chmod\s+",
            r"chown\s+",
            r"wget\s+",
            r"curl\s+",
            r"apt\s+",
            r"yum\s+",
            r"npm\s+",
            r"pip\s+"
        ]

        for pattern in command_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                complexity_info["has_commands"] = True
                complexity_info["is_complex"] = True
                complexity_info["complexity_score"] += 0.4
                break

        # Check for URLs
        if re.search(r"https?://", text, re.IGNORECASE):
            complexity_info["has_urls"] = True
            complexity_info["complexity_score"] += 0.1

        # Check for file paths
        if re.search(r"/\w+/\w+", text, re.IGNORECASE) or re.search(r"\\\\w+\\\\w+", text, re.IGNORECASE):
            complexity_info["has_paths"] = True
            complexity_info["complexity_score"] += 0.1

        return complexity_info

    def _should_use_llm(self, text: str, security_level: str) -> bool:
        """
        Determine if LLM validation should be used based on content and security level.

        Args:
            text (str): The text to validate
            security_level (str): The security level

        Returns:
            bool: Whether to use LLM validation
        """
        # For high and maximum security, always use LLM
        if security_level in ["high", "maximum"]:
            return True

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

        # For minimal and low security, only use LLM for very complex content
        if security_level in ["minimal", "low"]:
            complexity_info = self._detect_complex_content(text)
            if complexity_info["complexity_score"] > 0.7:
                return True

        # Use adaptive validation to decide
        if self.enable_adaptive_validation:
            risk_score = self._get_pattern_risk(text)
            if risk_score > 0.7:
                return True

        return False

    def _create_cache_key(self, text: str, context: Dict[str, Any]) -> str:
        """
        Create a cache key for the validation result.

        Args:
            text (str): The text to validate
            context (Dict[str, Any]): The validation context

        Returns:
            str: Cache key
        """
        # Create a hash of the text
        text_hash = hashlib.md5(text.encode()).hexdigest()

        # Extract key context elements
        security_level = context.get("security_level", "standard")

        # Create the cache key
        return f"{text_hash}:{security_level}"

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

            # Get ML result if requested
            ml_result = None
            if run_ml:
                ml_start = time.time()
                ml_result = ml_future.result()
                ml_time = time.time() - ml_start
                metrics["ml_time"] = ml_time
                metrics["methods_used"].append("ml")
                validation_flow.append("Input->ML")

            # Get LLM result if requested
            llm_result = None
            if run_llm:
                llm_start = time.time()
                llm_result = llm_future.result()
                llm_time = time.time() - llm_start
                metrics["llm_time"] = llm_time
                metrics["methods_used"].append("llm")
                validation_flow.append("Input->LLM")

        # Combine results using ensemble decision making
        if self.enable_ensemble_decisions and ml_result and llm_result:
            combined_result = self._combine_results(regex_result, ml_result, llm_result, security_level)
            combined_result["validation_metrics"] = metrics
            combined_result["validation_flow"] = validation_flow
            combined_result["total_time"] = time.time() - start_time
            return combined_result

        # If regex finds issues and we're not forcing other validators, return immediately
        if not regex_result["is_secure"] and not force_llm and security_level not in ["high", "maximum"]:
            metrics["total_time"] = time.time() - start_time
            regex_result["validation_metrics"] = metrics
            regex_result["validation_flow"] = validation_flow
            return regex_result

        # If ML was run and found issues, prioritize its result
        if ml_result and not ml_result["is_secure"] and not force_llm and security_level not in ["high", "maximum"]:
            metrics["total_time"] = time.time() - start_time
            ml_result["validation_metrics"] = metrics
            ml_result["validation_flow"] = validation_flow
            return ml_result

        # If LLM was run, prioritize its result (most thorough)
        if llm_result:
            metrics["total_time"] = time.time() - start_time
            llm_result["validation_metrics"] = metrics
            llm_result["validation_flow"] = validation_flow
            return llm_result

        # If ML was run but no issues found, return its result
        if ml_result:
            metrics["total_time"] = time.time() - start_time
            ml_result["validation_metrics"] = metrics
            ml_result["validation_flow"] = validation_flow
            return ml_result

        # Default to regex result
        metrics["total_time"] = time.time() - start_time
        regex_result["validation_metrics"] = metrics
        regex_result["validation_flow"] = validation_flow
        return regex_result

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

        # If regex finds issues and we're not forcing LLM, return immediately with clear feedback
        if not regex_result["is_secure"] and not force_llm and security_level not in ["high", "maximum"]:
            # Complete metrics
            metrics["total_time"] = time.time() - start_time
            regex_result["validation_metrics"] = metrics
            regex_result["validation_flow"] = validation_flow
            return regex_result

        # Step 2: ML validation for standard and higher security levels
        ml_result = None
        if security_level in ["standard", "high", "maximum"] or complexity_info.get("is_complex", False):
            ml_start = time.time()
            ml_result = self.ml_validator.validate(text, context)
            ml_time = time.time() - ml_start
            metrics["ml_time"] = ml_time
            metrics["methods_used"].append("ml")
            validation_flow.append("Regex->ML")

            # If ML finds issues and we're not forcing LLM, return with explanation
            if not ml_result["is_secure"] and not force_llm and security_level not in ["high", "maximum"]:
                # Complete metrics
                metrics["total_time"] = time.time() - start_time
                ml_result["validation_metrics"] = metrics
                ml_result["validation_flow"] = validation_flow
                return ml_result

        # Step 3: LLM validation for high/maximum security levels or complex content
        llm_result = None
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

        # If we have ML result but no LLM result, return ML result
        if ml_result:
            metrics["total_time"] = time.time() - start_time
            ml_result["validation_metrics"] = metrics
            ml_result["validation_flow"] = validation_flow
            return ml_result

        # Default to regex result
        metrics["total_time"] = time.time() - start_time
        regex_result["validation_metrics"] = metrics
        regex_result["validation_flow"] = validation_flow
        return regex_result

    def _combine_results(self, regex_result: Dict[str, Any], ml_result: Dict[str, Any],
                       llm_result: Dict[str, Any], security_level: str) -> Dict[str, Any]:
        """
        Combine results from multiple validators using ensemble decision making.

        Args:
            regex_result (Dict[str, Any]): Result from regex validator
            ml_result (Dict[str, Any]): Result from ML validator
            llm_result (Dict[str, Any]): Result from LLM validator
            security_level (str): Security level

        Returns:
            Dict[str, Any]: Combined result
        """
        # Initialize combined result
        combined_result = {
            "is_secure": True,
            "method": "ensemble",
            "reason": "",
            "threats": [],
            "confidence": 0.0,
            "ensemble_votes": {
                "secure": 0,
                "insecure": 0
            }
        }

        # Count votes
        if regex_result["is_secure"]:
            combined_result["ensemble_votes"]["secure"] += 1
        else:
            combined_result["ensemble_votes"]["insecure"] += 1

        if ml_result["is_secure"]:
            combined_result["ensemble_votes"]["secure"] += 1
        else:
            combined_result["ensemble_votes"]["insecure"] += 1

        if llm_result["is_secure"]:
            combined_result["ensemble_votes"]["secure"] += 1
        else:
            combined_result["ensemble_votes"]["insecure"] += 1

        # Calculate confidence
        total_votes = combined_result["ensemble_votes"]["secure"] + combined_result["ensemble_votes"]["insecure"]
        if total_votes > 0:
            if combined_result["ensemble_votes"]["secure"] > combined_result["ensemble_votes"]["insecure"]:
                combined_result["confidence"] = combined_result["ensemble_votes"]["secure"] / total_votes
            else:
                combined_result["confidence"] = combined_result["ensemble_votes"]["insecure"] / total_votes

        # Determine security based on votes and security level
        if security_level in ["high", "maximum"]:
            # For high and maximum security, any insecure vote makes it insecure
            combined_result["is_secure"] = combined_result["ensemble_votes"]["insecure"] == 0
        elif security_level == "standard":
            # For standard security, majority vote
            combined_result["is_secure"] = combined_result["ensemble_votes"]["secure"] > combined_result["ensemble_votes"]["insecure"]
        else:
            # For minimal and low security, only insecure if all vote insecure
            combined_result["is_secure"] = combined_result["ensemble_votes"]["secure"] > 0

        # Collect threats from all validators
        threats = []
        if not regex_result["is_secure"] and "threats" in regex_result:
            threats.extend(regex_result["threats"])
        if not ml_result["is_secure"] and "threats" in ml_result:
            threats.extend(ml_result["threats"])
        if not llm_result["is_secure"] and "threats" in llm_result:
            threats.extend(llm_result["threats"])

        # Deduplicate threats
        unique_threats = {}
        for threat in threats:
            category = threat.get("category", "unknown")
            if category not in unique_threats:
                unique_threats[category] = threat
            else:
                # Keep the threat with the highest score
                existing_score = unique_threats[category].get("score", 0.0)
                new_score = threat.get("score", 0.0)
                if new_score > existing_score:
                    unique_threats[category] = threat

        combined_result["threats"] = list(unique_threats.values())

        # Set reason based on threats
        if not combined_result["is_secure"] and combined_result["threats"]:
            combined_result["reason"] = f"Ensemble detected {len(combined_result['threats'])} security issues"
        elif not combined_result["is_secure"]:
            combined_result["reason"] = "Ensemble determined content is insecure"

        return combined_result

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
            self.cache_hits += 1
            return result

        self.cache_misses += 1

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

        # Add confidence score if not present
        if "confidence" not in result:
            result["confidence"] = self._calculate_confidence(result)

        # Update validation history
        self._update_validation_history(text, result)

        # Cache the result
        self.cache[cache_key] = result.copy()

        # Manage cache size
        if len(self.cache) > self.max_cache_size:
            # Remove oldest entries
            keys_to_remove = list(self.cache.keys())[:-self.max_cache_size]
            for key in keys_to_remove:
                del self.cache[key]

        return result

    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """
        Calculate confidence score for a validation result.

        Args:
            result (Dict[str, Any]): Validation result

        Returns:
            float: Confidence score (0.0 to 1.0)
        """
        # If result already has confidence, return it
        if "confidence" in result:
            return result["confidence"]

        # Default confidence based on method
        method = result.get("method", "unknown")
        if method == "regex":
            return 0.7
        elif method == "ml":
            return 0.8
        elif method == "llm":
            return 0.9
        elif method == "ensemble":
            return 0.95

        return 0.5
