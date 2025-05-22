#!/usr/bin/env python3
"""
Simple test script for LLM recommendation feature.

This script demonstrates the LLM recommendation feature by generating
a sample recommendation using Google's Generative AI.
"""

import os
import json
import logging
import time
import hashlib
from typing import Dict, Any, List, Optional

# Import Google's Generative AI library
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    print("Google Generative AI library not found. Install with: pip install google-generativeai")
    GENAI_AVAILABLE = False

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
        self.cache_dir = cache_dir or "recommendation_cache"
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

        if not GENAI_AVAILABLE:
            logger.warning("Google Generative AI library not available")
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

        prompt = f"""You are a cybersecurity expert providing recommendations to fix security issues in code or commands.

INPUT TEXT:
```
{input_text}
```

DETECTED SECURITY THREATS:
{threats_text}

Please provide a concise recommendation on how to fix these security issues. Format your response EXACTLY as follows:

## Why This Is Insecure
- Bullet point explaining the main security risk
- Bullet point explaining any additional risks
- Bullet point with any other relevant risks

## Recommended Solutions
- Bullet point with a specific solution (NO CODE EXAMPLES)
- Bullet point with an alternative approach if applicable
- Bullet point with any other relevant solutions

## Best Practices
- Bullet point with a key security principle
- Bullet point with another important practice
- Bullet point with a final recommendation

IMPORTANT GUIDELINES:
1. DO NOT include any code examples or code blocks
2. Keep all recommendations as bullet points
3. Be concise and specific
4. Focus on actionable advice
5. Use proper markdown formatting with "## " for headers and "- " for bullet points
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
            return "LLM not initialized. Please check your configuration."

        try:
            # Create system prompt
            system_prompt = "You are an elite cybersecurity expert providing recommendations to fix security issues."

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

def _generate_basic_recommendation(input_text: str, threats: List[Dict[str, Any]]) -> str:
    """
    Generate a basic recommendation for security issues.

    Args:
        input_text (str): The input text that was validated
        threats (List[Dict[str, Any]]): List of detected threats

    Returns:
        str: Basic recommendation
    """
    # If no threats, return a generic message
    if not threats:
        return "No security issues detected. The input appears to be secure."

    # Get the highest scoring threat
    highest_threat = max(threats, key=lambda x: x.get("score", 0.0))
    category = highest_threat.get("category", "unknown").replace("_", " ").title()

    # Generate a basic recommendation based on the threat category
    if "privilege_escalation" in category.lower():
        return """## Why This Is Insecure
- The command `rm -rf /tmp/data/*` uses a destructive operation that could delete important files if run with elevated privileges
- The wildcard pattern (*) increases the risk of unintended file deletion
- Shell commands bypass many security controls that programming languages provide

## Recommended Solutions
- Use programming language file operations instead of shell commands
- Implement proper error handling and validation before deletion
- Use specific paths rather than wildcards when possible

## Best Practices
- Always check if files/directories exist before attempting to delete them
- Use the principle of least privilege - only request the permissions you need
- Implement logging for sensitive operations like file deletion
- Consider using a more specific path rather than wildcard patterns"""

    elif "data_exfiltration" in category.lower():
        return """## Why This Is Insecure
- The command `rm -rf /tmp/data/*` could potentially delete sensitive data without proper verification
- There's no logging or audit trail of what was deleted
- The wildcard pattern could match more files than intended, leading to data loss

## Recommended Solutions
- Implement secure data handling with proper validation before deletion
- Add logging for all data deletion operations
- Use programming language file operations with explicit error handling

## Best Practices
- Always log data deletion operations for audit purposes
- Implement proper access controls for sensitive data
- Consider using secure deletion methods for highly sensitive information
- Verify the contents before deletion to prevent accidental data loss"""

    else:
        return f"""## Why This Is Insecure
- The command `rm -rf /tmp/data/*` contains potential security risks related to {category}
- Shell commands are inherently risky as they can have unintended consequences
- The recursive flag (-r) and force flag (-f) bypass safety checks

## Recommended Solutions
- Use programming language file operations instead of shell commands
- Implement proper validation and error handling
- Process files individually with appropriate checks

## Best Practices
- Avoid using shell commands when programming alternatives exist
- Always validate paths before performing operations
- Use specific paths rather than wildcards when possible
- Implement proper error handling and logging for all file operations"""

def test_llm_recommendation():
    """Test the LLM recommendation generator."""
    # Sample input text
    input_text = "rm -rf /tmp/data/*"

    # Sample threats
    threats = [
        {
            "category": "privilege_escalation",
            "score": 0.85,
            "description": "The command attempts to delete files with elevated privileges"
        },
        {
            "category": "data_exfiltration",
            "score": 0.78,
            "description": "The command could potentially leak sensitive data"
        }
    ]

    # Get API key from environment
    api_key = os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        print("No Google API key found in environment variables. Using fallback recommendation.")
        recommendation = _generate_basic_recommendation(input_text, threats)
    else:
        # Create recommendation generator
        generator = LLMRecommendationGenerator(api_key=api_key)

        # Generate recommendation
        print("\nGenerating recommendation using LLM...\n")
        recommendation = generator.generate_recommendation(input_text, threats)

    # Print recommendation
    print("\n=== RECOMMENDATION ===\n")
    print(recommendation)
    print("\n======================\n")

if __name__ == "__main__":
    test_llm_recommendation()
