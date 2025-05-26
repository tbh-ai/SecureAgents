#!/usr/bin/env python3
"""
LLM-based recommendation generator for security validation.

This module provides a recommendation generator that uses LLM to generate
detailed, context-aware recommendations for security issues.
"""

import os
import json
import logging
import time
from typing import Dict, Any, List, Optional, Union
import hashlib

# Import Google's Generative AI library (same as used in the framework)
import google.generativeai as genai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class LLMRecommendationGenerator:
    """
    LLM-based recommendation generator for security validation.

    This class uses LLM to generate detailed, context-aware recommendations
    for security issues detected during validation.
    """

    def __init__(self,
                 cache_dir: Optional[str] = None,
                 api_key: Optional[str] = None,
                 model_name: str = "gemini-2.0-flash-lite"):
        """
        Initialize the LLM recommendation generator.

        Args:
            cache_dir (Optional[str]): Directory to cache recommendations
            api_key (Optional[str]): API key for Google Generative AI
            model_name (str): Model to use for recommendations
        """
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), "cache")
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.model_name = model_name

        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)

        # Initialize LLM client
        self.llm = self._initialize_llm()

        logger.info(f"Initialized LLM recommendation generator with model: {model_name}")

    def _initialize_llm(self):
        """
        Initialize the LLM.

        Returns:
            Any: The initialized LLM or None if initialization failed
        """
        if not self.api_key:
            logger.warning("No API key provided for LLM recommendation generator")
            return None

        try:
            genai.configure(api_key=self.api_key)
            return genai.GenerativeModel(self.model_name)
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            return None

    def _get_cache_key(self, input_text: str, threats: List[Dict[str, Any]]) -> str:
        """
        Generate a cache key for the recommendation.

        Args:
            input_text (str): The input text that was validated
            threats (List[Dict[str, Any]]): List of detected threats

        Returns:
            str: Cache key
        """
        # Create a string representation of the input
        threats_str = json.dumps(threats, sort_keys=True)
        cache_input = f"{input_text}|{threats_str}"

        # Generate a hash of the input
        return hashlib.md5(cache_input.encode()).hexdigest()

    def _get_cached_recommendation(self, cache_key: str) -> Optional[str]:
        """
        Get a cached recommendation if available.

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
                cache_time = cache_data.get("timestamp", 0)
                if time.time() - cache_time < 7 * 86400:
                    logger.info(f"Using cached recommendation for key: {cache_key}")
                    return cache_data.get("recommendation")

            except Exception as e:
                logger.warning(f"Error reading cache file: {e}")

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
            cache_data = {
                "timestamp": time.time(),
                "recommendation": recommendation
            }

            with open(cache_file, "w") as f:
                json.dump(cache_data, f)

            logger.info(f"Cached recommendation for key: {cache_key}")

        except Exception as e:
            logger.warning(f"Error caching recommendation: {e}")

    def _generate_prompt(self, input_text: str, threats: List[Dict[str, Any]]) -> str:
        """
        Generate a prompt for the LLM.

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

        prompt = f"""You are a cybersecurity expert specializing in the TBH Secure Agents framework. Provide framework-specific recommendations.

INPUT TEXT:
```
{input_text}
```

DETECTED SECURITY THREATS:
{threats_text}

Please provide your recommendation as bullet points only, focusing on TBH Secure Agents framework features:
• Explain why the input is insecure in the context of TBH Secure Agents
• Recommend specific TBH Secure Agents security profiles (minimal, low, standard, high, maximum)
• Suggest TBH Secure Agents features like hybrid validation, result_destination, or custom profiles
• Reference TBH Secure Agents documentation and best practices
• Mention framework-specific security capabilities (ML validation, LLM validation, etc.)

Your response should be in bullet point format only. Do NOT include any code examples or headers.
Focus on TBH Secure Agents framework-specific recommendations.
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
            # Return framework-specific recommendations in bullet points
            return """• Consider using TBH Secure Agents' minimal security profile for less restrictive validation
• System commands detected - recommend using standard or higher security profile for better protection
• TBH Secure Agents framework provides built-in security validation to prevent such operations
• Enable hybrid validation mode in TBH Secure Agents for comprehensive security checking
• Use TBH Secure Agents' result_destination feature to safely capture outputs
• Consider implementing custom security profiles in TBH Secure Agents for your specific use case
• TBH Secure Agents' ML and LLM validation layers can detect advanced security threats
• Review TBH Secure Agents documentation for secure coding best practices"""

        try:
            # Create system prompt
            system_prompt = "You are an elite cybersecurity expert specializing in the TBH Secure Agents framework. Always respond in bullet point format without code examples or headers. Focus on framework-specific recommendations."

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
            return f"Error generating recommendation: {str(e)}"

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
            return "No security issues detected. The input appears to be secure."

        # Generate cache key
        cache_key = self._get_cache_key(input_text, threats)

        # Check cache first
        cached_recommendation = self._get_cached_recommendation(cache_key)
        if cached_recommendation:
            return cached_recommendation

        # Generate prompt
        prompt = self._generate_prompt(input_text, threats)

        # Call LLM
        recommendation = self._call_llm(prompt)

        # Cache the recommendation
        self._cache_recommendation(cache_key, recommendation)

        return recommendation
