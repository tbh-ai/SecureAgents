#!/usr/bin/env python3
"""
Framework-Specific Recommendation Generator

This module provides a recommendation generator that creates detailed,
framework-specific security recommendations for the TBH Secure Agents framework.
"""

import os
import json
import time
import hashlib
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("Google Generative AI not available. Install with: pip install google-generativeai")

class FrameworkSpecificRecommendationGenerator:
    """
    Framework-specific recommendation generator.

    This class generates detailed security recommendations that reference
    the TBH Secure Agents framework and its features.
    """

    def __init__(self,
                 cache_dir: Optional[str] = None,
                 api_key: Optional[str] = None,
                 model_name: str = "gemini-2.0-flash-lite",
                 recommendation_style: str = "detailed",
                 include_code_examples: bool = True):
        """
        Initialize the framework-specific recommendation generator.

        Args:
            cache_dir (Optional[str]): Directory to cache recommendations
            api_key (Optional[str]): API key for Google Generative AI
            model_name (str): Model to use for recommendations
            recommendation_style (str): Style of recommendations (detailed, concise, bullet)
            include_code_examples (bool): Whether to include code examples
        """
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), "cache")
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.model_name = model_name
        self.recommendation_style = recommendation_style
        self.include_code_examples = include_code_examples

        # Cache statistics
        self.cache_hits = 0
        self.cache_misses = 0

        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)

        # Initialize LLM client
        self.llm = self._initialize_llm()

        logger.info(f"Initialized framework-specific recommendation generator with model: {model_name}")

    def _initialize_llm(self):
        """
        Initialize the LLM client.

        Returns:
            Any: LLM client
        """
        if not GENAI_AVAILABLE:
            logger.warning("Google Generative AI not available. Recommendations will be basic.")
            return None

        if not self.api_key:
            logger.warning("No API key provided. Recommendations will be basic.")
            return None

        try:
            # Configure the Generative AI library
            genai.configure(api_key=self.api_key)

            # Get the model
            model = genai.GenerativeModel(self.model_name)

            logger.info(f"Successfully initialized LLM with model: {self.model_name}")
            return model
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            return None

    def _get_cache_key(self, input_text: str, threats: List[Dict[str, Any]]) -> str:
        """
        Generate a cache key for the input text and threats.

        Args:
            input_text (str): The input text
            threats (List[Dict[str, Any]]): List of detected threats

        Returns:
            str: Cache key
        """
        # Create a hash of the input text
        text_hash = hashlib.md5(input_text.encode()).hexdigest()

        # Create a hash of the threats
        threats_str = json.dumps(threats, sort_keys=True)
        threats_hash = hashlib.md5(threats_str.encode()).hexdigest()

        # Create a hash of the configuration
        config_str = f"{self.recommendation_style}_{self.include_code_examples}"
        config_hash = hashlib.md5(config_str.encode()).hexdigest()

        # Combine the hashes
        return f"{text_hash}_{threats_hash}_{config_hash}"

    def _get_cached_recommendation(self, cache_key: str) -> Optional[str]:
        """
        Get a cached recommendation.

        Args:
            cache_key (str): Cache key

        Returns:
            Optional[str]: Cached recommendation or None
        """
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cache_data = json.load(f)

                # Check if cache is still valid (less than 7 days old)
                timestamp = cache_data.get("timestamp", 0)
                if time.time() - timestamp < 7 * 24 * 60 * 60:
                    self.cache_hits += 1
                    return cache_data.get("recommendation", "")
            except Exception as e:
                logger.error(f"Error reading cache: {e}")

        self.cache_misses += 1
        return None

    def _cache_recommendation(self, cache_key: str, recommendation: str):
        """
        Cache a recommendation.

        Args:
            cache_key (str): Cache key
            recommendation (str): Recommendation to cache
        """
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        try:
            with open(cache_file, "w") as f:
                json.dump({
                    "recommendation": recommendation,
                    "timestamp": time.time()
                }, f)
        except Exception as e:
            logger.error(f"Error writing cache: {e}")

    def _generate_framework_specific_prompt(self, input_text: str, threats: List[Dict[str, Any]]) -> str:
        """
        Generate a framework-specific prompt for the LLM.

        Args:
            input_text (str): The input text that was validated
            threats (List[Dict[str, Any]]): List of detected threats

        Returns:
            str: Prompt for the LLM
        """
        # Create a detailed prompt based on the threats
        threat_descriptions = []
        for threat in threats:
            category = threat.get("category", "unknown")
            score = threat.get("score", 0.0)
            description = threat.get("description", "")

            threat_descriptions.append(f"- {category.replace('_', ' ').title()} (Score: {score:.2f}): {description}")

        threats_text = "\n".join(threat_descriptions)

        # Determine recommendation style
        style_instruction = ""
        if self.recommendation_style == "concise":
            style_instruction = "Provide a concise recommendation with only the most important points."
        elif self.recommendation_style == "bullet":
            style_instruction = "Format your recommendation as a bullet point list with clear, actionable items."
        else:  # detailed
            style_instruction = "Provide a detailed recommendation with thorough explanations."

        # Determine code example instruction
        code_instruction = ""
        if self.include_code_examples:
            code_instruction = "Include specific code examples showing both the insecure code and the secure alternative."
        else:
            code_instruction = "Do not include code examples in your recommendation."

        # Create the prompt
        prompt = f"""You are a cybersecurity expert providing recommendations to fix security issues in code or commands, specifically for users of the TBH Secure Agents framework.

INPUT TEXT:
```
{input_text}
```

SECURITY ISSUES DETECTED:
{threats_text}

TASK:
Generate a security recommendation to address these issues. {style_instruction} {code_instruction}

Your recommendation should:
1. Clearly explain each security issue in a way that's easy to understand
2. Provide specific, actionable advice on how to fix each issue
3. Explain why the fix works and best practices for secure coding
4. Be diplomatic and educational rather than accusatory

IMPORTANT: Reference the TBH Secure Agents framework in your recommendations:
1. Mention how the framework's security validation helps prevent these issues
2. Suggest using appropriate security profiles (minimal, low, standard, high, maximum) based on the sensitivity of the operation
3. Reference framework features like Expert, Operation, and Squad when relevant
4. Suggest using the framework's built-in security features

FORMAT YOUR RESPONSE AS MARKDOWN with appropriate headings, bullet points, and code blocks.
"""

        return prompt

    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM to generate a recommendation.

        Args:
            prompt (str): Prompt for the LLM

        Returns:
            str: Generated recommendation
        """
        if self.llm is None:
            return self._generate_fallback_recommendation(prompt)

        try:
            # Create system prompt
            system_prompt = "You are an elite cybersecurity expert providing recommendations to fix security issues in the TBH Secure Agents framework."

            # Generate content using Google's Generative AI
            response = self.llm.generate_content(
                [
                    {"role": "system", "parts": [system_prompt]},
                    {"role": "user", "parts": [prompt]}
                ],
                generation_config={"temperature": 0.3, "max_output_tokens": 1000}
            )

            # Extract the response text
            return response.text
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return self._generate_fallback_recommendation(prompt)

    def _generate_fallback_recommendation(self, prompt: str) -> str:
        """
        Generate a fallback recommendation when LLM is unavailable.

        Args:
            prompt (str): The original prompt

        Returns:
            str: Fallback recommendation
        """
        # Extract threats from prompt
        threats = []
        in_threats_section = False
        for line in prompt.split("\n"):
            if line.strip() == "SECURITY ISSUES DETECTED:":
                in_threats_section = True
                continue
            elif line.strip() == "TASK:":
                in_threats_section = False
                continue

            if in_threats_section and line.strip().startswith("-"):
                threats.append(line.strip())

        # Generate a basic recommendation
        recommendation = "# Security Recommendation\n\n"

        if threats:
            recommendation += "## Issues Detected\n\n"
            for threat in threats:
                recommendation += f"{threat}\n"

            recommendation += "\n## Recommendations\n\n"
            recommendation += "To address these security issues, consider the following recommendations:\n\n"

            # Add framework-specific recommendations
            recommendation += "### TBH Secure Agents Framework Recommendations\n\n"

            recommendation += "1. **Use appropriate security profiles**\n"
            recommendation += "   - For development and testing, use the 'minimal' security profile\n"
            recommendation += "   - For general use, use the 'standard' security profile\n"
            recommendation += "   - For sensitive operations, use the 'high' or 'maximum' security profiles\n\n"

            recommendation += "2. **Leverage framework security features**\n"
            recommendation += "   - Use the `Expert` class with appropriate security profiles\n"
            recommendation += "   - Configure `Operation` objects with clear instructions\n"
            recommendation += "   - Organize operations in a `Squad` with appropriate security settings\n\n"

            recommendation += "3. **Follow secure coding practices**\n"
            recommendation += "   - Validate all inputs before processing\n"
            recommendation += "   - Use safe alternatives to dangerous functions\n"
            recommendation += "   - Follow the principle of least privilege\n\n"
        else:
            recommendation += "No specific security issues were detected, but it's always good practice to follow secure coding guidelines and use the TBH Secure Agents framework's security features appropriately.\n"

        return recommendation

    def generate_recommendation(self, input_text: str, threats: List[Dict[str, Any]]) -> str:
        """
        Generate a recommendation for security issues.

        Args:
            input_text (str): The input text that was validated
            threats (List[Dict[str, Any]]): List of detected threats

        Returns:
            str: Generated recommendation
        """
        # If no threats, return a generic message
        if not threats:
            return "# Security Assessment\n\nNo security issues were detected. The input appears to be secure.\n\nHowever, it's always good practice to follow secure coding guidelines and use the TBH Secure Agents framework's security features appropriately."

        # Generate cache key
        cache_key = self._get_cache_key(input_text, threats)

        # Check cache first
        cached_recommendation = self._get_cached_recommendation(cache_key)
        if cached_recommendation:
            return cached_recommendation

        # Generate prompt
        prompt = self._generate_framework_specific_prompt(input_text, threats)

        # Call LLM
        recommendation = self._call_llm(prompt)

        # Cache the recommendation
        self._cache_recommendation(cache_key, recommendation)

        return recommendation
