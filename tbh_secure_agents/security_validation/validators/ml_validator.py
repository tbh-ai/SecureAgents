"""
Machine Learning-based security validator.

This module implements a machine learning-based security validator that uses
a pre-trained model to detect security issues in text.
"""

import logging
import os
import pickle
import re
from typing import Dict, Any, Optional, List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .base_validator import SecurityValidator

# Get a logger for this module
logger = logging.getLogger(__name__)


class MLValidator(SecurityValidator):
    """
    Machine Learning-based security validator.

    This validator uses a pre-trained model to detect security issues in text.
    It's more sophisticated than regex and can detect novel threats, but
    requires a trained model.
    """

    def __init__(self, model_path: Optional[str] = None, vectorizer_path: Optional[str] = None,
                 pipeline_path: Optional[str] = None):
        """
        Initialize the ML validator.

        Args:
            model_path (Optional[str]): Path to a pickled model file
            vectorizer_path (Optional[str]): Path to a pickled vectorizer file
            pipeline_path (Optional[str]): Path to a pickled pipeline file
        """
        # Use environment variables if paths not provided
        pipeline_path = pipeline_path or os.environ.get(
            "TBH_SECURITY_PIPELINE_PATH",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "models/data/security_pipeline.pkl")
        )

        model_path = model_path or os.environ.get(
            "TBH_SECURITY_MODEL_PATH",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "models/data/security_model.pkl")
        )

        vectorizer_path = vectorizer_path or os.environ.get(
            "TBH_SECURITY_VECTORIZER_PATH",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "models/data/vectorizer.pkl")
        )

        # Try to load the pipeline first
        self.pipeline = self._load_pipeline(pipeline_path)

        # If pipeline is not available, load model and vectorizer separately
        if self.pipeline is None:
            self.model = self._load_model(model_path)
            self.vectorizer = self._load_vectorizer(vectorizer_path)
        else:
            # If we have a pipeline, extract model and vectorizer from it
            self.model = getattr(self.pipeline, 'named_steps', {}).get('classifier', None)
            self.vectorizer = getattr(self.pipeline, 'named_steps', {}).get('vectorizer', None)

            # If we couldn't extract them, load them separately
            if self.model is None:
                self.model = self._load_model(model_path)
            if self.vectorizer is None:
                self.vectorizer = self._load_vectorizer(vectorizer_path)

        # PERFECT Security level thresholds (correct order: permissive → strict)
        self.thresholds = {
            "minimal": 0.98,   # Most permissive - only block obvious attacks
            "standard": 0.9,   # Balanced - allow legitimate content
            "high": 0.75,      # Strict - block suspicious content
            "maximum": 0.6     # Most strict - block questionable content
        }
        self.categories = [
            "command_injection",
            "prompt_injection",
            "data_exfiltration",
            "privilege_escalation",
            "denial_of_service"
        ]

    def _load_pipeline(self, pipeline_path: Optional[str] = None):
        """
        Load a pre-trained pipeline.

        Args:
            pipeline_path (Optional[str]): Path to a pickled pipeline file

        Returns:
            Any: The loaded pipeline or None if not available
        """
        if pipeline_path and os.path.exists(pipeline_path):
            try:
                with open(pipeline_path, 'rb') as f:
                    pipeline = pickle.load(f)
                logger.info(f"Loaded pipeline from {pipeline_path}")
                return pipeline
            except Exception as e:
                logger.error(f"Error loading pipeline: {e}")

        logger.warning("No pipeline available")
        return None

    def _load_model(self, model_path: Optional[str] = None):
        """
        Load a pre-trained model or create a simple one.

        Args:
            model_path (Optional[str]): Path to a pickled model file

        Returns:
            Any: The loaded model or a simple placeholder
        """
        if model_path and os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                logger.info(f"Loaded model from {model_path}")
                return model
            except Exception as e:
                logger.error(f"Error loading model: {e}")

        # If no model is available, create a simple rule-based classifier
        # This is just a placeholder - in a real implementation, you would
        # use a properly trained ML model
        logger.warning("No ML model available, using simple rule-based classifier")
        return SimpleSecurity()

    def _load_vectorizer(self, vectorizer_path: Optional[str] = None):
        """
        Load a pre-trained vectorizer or create a simple one.

        Args:
            vectorizer_path (Optional[str]): Path to a pickled vectorizer file

        Returns:
            Any: The loaded vectorizer or a simple placeholder
        """
        if vectorizer_path and os.path.exists(vectorizer_path):
            try:
                with open(vectorizer_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.error(f"Error loading vectorizer: {e}")

        # If no vectorizer is available, create a simple one
        logger.warning("No vectorizer available, using simple TF-IDF vectorizer")
        return TfidfVectorizer(max_features=1000)

    def _get_threshold(self, security_level: str) -> float:
        """
        Get the threshold for a security level.

        Args:
            security_level (str): The security level

        Returns:
            float: The threshold for this security level
        """
        return self.thresholds.get(security_level, self.thresholds["standard"])

    def _extract_features(self, text: str) -> np.ndarray:
        """
        Extract features from text.

        Args:
            text (str): The text to extract features from

        Returns:
            np.ndarray: The extracted features
        """
        # Make sure text is a string
        if not isinstance(text, str):
            text = str(text)

        if hasattr(self.vectorizer, 'transform'):
            try:
                features = self.vectorizer.transform([text])
                # Test if features can be used with the model
                if hasattr(self.model, 'predict_proba'):
                    try:
                        self.model.predict_proba(features)
                        return features
                    except Exception as e:
                        logger.warning(f"Features not compatible with model: {e}")
                else:
                    return features
            except Exception as e:
                logger.warning(f"Error transforming text with vectorizer: {e}")
                try:
                    # If the vectorizer hasn't been fit yet, fit it on this text
                    self.vectorizer.fit([text])
                    return self.vectorizer.transform([text])
                except Exception as e:
                    logger.warning(f"Error fitting vectorizer: {e}")

        # If the vectorizer doesn't work, use a simple approach with more features
        return np.array([[
            len(text),
            len(re.findall(r'\b(?:system|exec|eval)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:rm|delete|drop)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:hack|exploit|bypass)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:sudo|root|admin)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:password|credential|token)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:ignore|disregard)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:send|upload|post)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:infinite|loop|while\s*\(\s*true\s*\))\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:validate|sanitize)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:secure|encrypt)\b', text, re.IGNORECASE)),
            len(re.findall(r'\b(?:authenticate|authorize)\b', text, re.IGNORECASE))
        ]])

    def _get_threat_categories(self, text: str, features: np.ndarray) -> List[Dict[str, Any]]:
        """
        Get threat categories for text.

        Args:
            text (str): The text to analyze
            features (np.ndarray): The extracted features

        Returns:
            List[Dict[str, Any]]: List of threat categories with scores
        """
        threats = []

        # If we have a real ML model with predict_proba, use it
        if hasattr(self.model, 'predict_proba'):
            try:
                # Try to get class probabilities
                probs = self.model.predict_proba(features)[0]

                # If we have a binary classifier (secure/insecure), use regex to determine categories
                if len(probs) <= 2:
                    insecure_prob = probs[1] if len(probs) > 1 else 1.0 - probs[0]

                    # Only add threats if the insecure probability is significant
                    if insecure_prob > 0.3:
                        # Use regex to determine specific threat categories
                        self._add_regex_based_threats(text, threats, base_score=insecure_prob)
                else:
                    # If we have a multi-class classifier with one class per threat category
                    # Map the probabilities to threat categories
                    for i, prob in enumerate(probs):
                        if prob > 0.3 and i < len(self.categories):
                            category = self.categories[i]
                            threats.append({
                                "category": category,
                                "score": float(prob),
                                "description": f"ML model detected potential {category.replace('_', ' ')}"
                            })
            except Exception as e:
                logger.warning(f"Error getting threat categories from ML model: {e}")
                # Fall back to regex-based approach
                self._add_regex_based_threats(text, threats)
        else:
            # Use the simple model and regex-based approach
            security_score = self.model.predict_security(text)
            insecure_score = 1.0 - security_score

            # Only add threats if the insecure score is significant
            if insecure_score > 0.3:
                self._add_regex_based_threats(text, threats, base_score=insecure_score)

        return threats

    def _add_regex_based_threats(self, text: str, threats: List[Dict[str, Any]], base_score: float = 0.7):
        """
        Add threats based on regex patterns.

        Args:
            text (str): The text to analyze
            threats (List[Dict[str, Any]]): The list to add threats to
            base_score (float): The base score to use for threats
        """
        # Check for command injection
        if re.search(r'\b(?:system|exec|eval|subprocess)\s*\(', text, re.IGNORECASE):
            threats.append({
                "category": "command_injection",
                "score": min(0.9, base_score + 0.1),
                "description": "Potential command injection detected"
            })

        # Check for prompt injection
        if re.search(r'\b(?:ignore|disregard)\s+(?:previous|instructions)', text, re.IGNORECASE):
            threats.append({
                "category": "prompt_injection",
                "score": min(0.9, base_score + 0.2),
                "description": "Potential prompt injection detected"
            })

        # Check for data exfiltration
        if re.search(r'\b(?:send|upload|post)\s+(?:data|file)', text, re.IGNORECASE):
            threats.append({
                "category": "data_exfiltration",
                "score": min(0.9, base_score),
                "description": "Potential data exfiltration detected"
            })

        # Check for privilege escalation
        if re.search(r'\b(?:sudo|su|admin|root)\b', text, re.IGNORECASE):
            threats.append({
                "category": "privilege_escalation",
                "score": min(0.9, base_score - 0.1),
                "description": "Potential privilege escalation detected"
            })

        # Check for denial of service
        if re.search(r'\b(?:infinite|loop|while\s*\(\s*true\s*\))', text, re.IGNORECASE):
            threats.append({
                "category": "denial_of_service",
                "score": min(0.9, base_score),
                "description": "Potential denial of service detected"
            })

    def _get_fix_suggestion(self, text: str, threats: List[Dict[str, Any]]) -> str:
        """
        Get a fix suggestion for the detected threats.

        Args:
            text (str): The original text
            threats (List[Dict[str, Any]]): The detected threats

        Returns:
            str: A suggestion for fixing the issues
        """
        if not threats:
            return ""

        # Get the highest scoring threat
        top_threat = max(threats, key=lambda x: x.get("score", 0))
        category = top_threat.get("category", "unknown")

        if category == "command_injection":
            return "Replace system commands with secure alternatives. For example:\n" + \
                   "Instead of: system('rm file.txt')\n" + \
                   "Use: os.remove('file.txt')"

        elif category == "prompt_injection":
            return "Remove instructions to ignore or disregard previous instructions.\n" + \
                   "These are common patterns in prompt injection attacks."

        elif category == "data_exfiltration":
            return "Use secure data handling methods instead of sending data directly.\n" + \
                   "Consider using authenticated APIs or secure file operations."

        elif category == "privilege_escalation":
            return "Avoid using privileged commands or operations.\n" + \
                   "Use proper permission management and least privilege principles."

        elif category == "denial_of_service":
            return "Avoid infinite loops or resource-intensive operations.\n" + \
                   "Use proper termination conditions and resource limits."

        return "Review and modify the flagged content to address security concerns."

    def validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate text using the ML model or pipeline.

        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation

        Returns:
            Dict[str, Any]: Validation result
        """
        context = context or {}
        security_level = context.get("security_level", "standard")
        complexity_info = context.get("complexity_info", {})

        # Skip ML validation for minimal security level unless content is complex
        if security_level == "minimal" and not complexity_info.get("is_complex", False):
            return {
                "is_secure": True,
                "method": "ml",
                "message": "ML validation skipped for minimal security level"
            }

        # Try to use the pipeline directly if available
        if self.pipeline is not None:
            try:
                # Make sure text is a string
                if not isinstance(text, str):
                    text = str(text)

                # Get prediction from pipeline
                # Pipeline handles both vectorization and classification
                probs = self.pipeline.predict_proba([text])[0]

                # Our pipeline is trained with 0=insecure, 1=secure
                if len(probs) > 1:
                    secure_prob = probs[1]  # Class 1 is secure
                    insecure_prob = probs[0]  # Class 0 is insecure
                else:
                    secure_prob = probs[0]
                    insecure_prob = 1.0 - secure_prob

                logger.info(f"Pipeline prediction: secure_prob={secure_prob:.4f}, insecure_prob={insecure_prob:.4f}")

                # Get threshold for this security level
                threshold = self._get_threshold(security_level)

                # Adjust threshold based on content complexity
                if complexity_info.get("is_complex", False):
                    # For complex content, lower the threshold (be more strict)
                    complexity_score = complexity_info.get("complexity_score", 0.0)
                    threshold_adjustment = min(0.2, complexity_score / 2)
                    adjusted_threshold = threshold - threshold_adjustment
                    logger.info(f"Adjusting threshold from {threshold} to {adjusted_threshold} due to content complexity")
                    threshold = adjusted_threshold

                # Check if the text is secure
                is_secure = secure_prob >= threshold

                # Get threat categories using regex patterns
                # Since we're using a binary classifier, we need to use regex to determine categories
                threats = []
                if not is_secure:
                    self._add_regex_based_threats(text, threats, base_score=insecure_prob)

                # If we have threats with high scores, consider the text insecure
                # regardless of the overall secure probability
                high_threat_detected = any(threat.get("score", 0) > 0.8 for threat in threats)
                if high_threat_detected and secure_prob < 0.9:
                    is_secure = False
                    logger.info("High-score threat detected, marking as insecure")

                if not is_secure:
                    # Get the fix suggestion
                    fix_suggestion = self._get_fix_suggestion(text, threats)

                    # Determine the reason based on the threats
                    if threats:
                        top_threat = max(threats, key=lambda x: x.get("score", 0))
                        reason = f"ML model detected potential {top_threat.get('category', 'security')} issue"
                    else:
                        reason = "ML model detected potential security issues"

                    return {
                        "is_secure": False,
                        "method": "ml_pipeline",
                        "confidence": secure_prob,
                        "threshold": threshold,
                        "reason": reason,
                        "threats": threats,
                        "fix_suggestion": fix_suggestion,
                        "complexity_adjusted": complexity_info.get("is_complex", False)
                    }

                return {
                    "is_secure": True,
                    "method": "ml_pipeline",
                    "confidence": secure_prob,
                    "threshold": threshold,
                    "complexity_adjusted": complexity_info.get("is_complex", False)
                }

            except Exception as e:
                logger.warning(f"Error using pipeline: {e}")
                logger.warning("Falling back to separate model and vectorizer")
                # Fall back to using model and vectorizer separately

        # If pipeline is not available or failed, use model and vectorizer separately
        # Extract features from text
        features = self._extract_features(text)

        # Get prediction from model
        if hasattr(self.model, 'predict_proba'):
            try:
                # Get probability of secure class (assumed to be class 1 for our trained model)
                probs = self.model.predict_proba(features)[0]

                # Our model is trained with 0=insecure, 1=secure
                if len(probs) > 1:
                    secure_prob = probs[1]  # Class 1 is secure
                    insecure_prob = probs[0]  # Class 0 is insecure
                else:
                    secure_prob = probs[0]
                    insecure_prob = 1.0 - secure_prob

                logger.info(f"ML prediction: secure_prob={secure_prob:.4f}, insecure_prob={insecure_prob:.4f}")
            except Exception as e:
                logger.warning(f"Error getting prediction from ML model: {e}")
                # If prediction fails, use a default value
                secure_prob = 0.5
                insecure_prob = 0.5
        else:
            # Use the simple model
            secure_prob = self.model.predict_security(text)
            insecure_prob = 1.0 - secure_prob

        # Get threshold for this security level
        threshold = self._get_threshold(security_level)

        # Adjust threshold based on content complexity
        if complexity_info.get("is_complex", False):
            # For complex content, lower the threshold (be more strict)
            complexity_score = complexity_info.get("complexity_score", 0.0)
            threshold_adjustment = min(0.2, complexity_score / 2)
            adjusted_threshold = threshold - threshold_adjustment
            logger.info(f"Adjusting threshold from {threshold} to {adjusted_threshold} due to content complexity")
            threshold = adjusted_threshold

        # Get threat categories
        threats = self._get_threat_categories(text, features)

        # Check if the text is secure
        is_secure = secure_prob >= threshold

        # If we have threats with high scores, consider the text insecure
        # regardless of the overall secure probability
        high_threat_detected = any(threat.get("score", 0) > 0.8 for threat in threats)
        if high_threat_detected and secure_prob < 0.9:
            is_secure = False
            logger.info("High-score threat detected, marking as insecure")

        if not is_secure:
            # Get the fix suggestion
            fix_suggestion = self._get_fix_suggestion(text, threats)

            # Determine the reason based on the threats
            if threats:
                top_threat = max(threats, key=lambda x: x.get("score", 0))
                reason = f"ML model detected potential {top_threat.get('category', 'security')} issue"
            else:
                reason = "ML model detected potential security issues"

            return {
                "is_secure": False,
                "method": "ml",
                "confidence": secure_prob,
                "threshold": threshold,
                "reason": reason,
                "threats": threats,
                "fix_suggestion": fix_suggestion,
                "complexity_adjusted": complexity_info.get("is_complex", False)
            }

        return {
            "is_secure": True,
            "method": "ml",
            "confidence": secure_prob,
            "threshold": threshold,
            "complexity_adjusted": complexity_info.get("is_complex", False)
        }


class SimpleSecurity:
    """
    Simple rule-based security classifier.

    This is a placeholder for a real ML model. It uses simple rules to
    classify text as secure or insecure.
    """

    def predict_security(self, text: str) -> float:
        """
        Predict the security score of text.

        Args:
            text (str): The text to analyze

        Returns:
            float: Security score between 0 and 1 (higher is more secure)
        """
        # Count potentially dangerous patterns
        dangerous_count = 0

        # Command execution
        dangerous_count += len(re.findall(r'\b(?:system|exec|eval|subprocess)\s*\(', text, re.IGNORECASE))

        # File operations
        dangerous_count += len(re.findall(r'\b(?:rm\s+-rf|rmdir\s+/|format\s+[a-z]:)', text, re.IGNORECASE))

        # Database operations
        dangerous_count += len(re.findall(r'\b(?:drop\s+table|drop\s+database)', text, re.IGNORECASE))

        # Hacking terminology
        dangerous_count += len(re.findall(r'\b(?:hack|crack|exploit)\b', text, re.IGNORECASE))

        # Prompt injection
        dangerous_count += len(re.findall(r'\b(?:ignore|disregard)\s+(?:previous|instructions)', text, re.IGNORECASE))

        # Calculate security score (inverse of danger)
        # More dangerous patterns = lower security score
        security_score = max(0, min(1, 1.0 - (dangerous_count * 0.2)))

        return security_score
