"""
Optimized LLM-based security validator.

This module implements an optimized LLM-based security validator that uses
caching and parallel processing to improve performance.
"""

import os
import re
import json
import time
import hashlib
import logging
import asyncio
import concurrent.futures
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
from functools import lru_cache

import aiohttp
import requests
from diskcache import Cache

from .llm_validator import LLMValidator

# Get a logger for this module
logger = logging.getLogger(__name__)


class OptimizedLLMValidator(LLMValidator):
    """
    Optimized LLM-based security validator.

    This validator uses caching and parallel processing to improve performance.
    It's a drop-in replacement for the standard LLMValidator.
    """

    def __init__(self, api_key: Optional[str] = None, cache_dir: Optional[str] = None,
                 cache_size_limit: int = 1024 * 1024 * 1024, cache_ttl: int = 86400 * 7):
        """
        Initialize the optimized LLM validator.

        Args:
            api_key (Optional[str]): API key for the LLM service
            cache_dir (Optional[str]): Directory to store the cache
            cache_size_limit (int): Maximum size of the cache in bytes
            cache_ttl (int): Time-to-live for cache entries in seconds
        """
        super().__init__(api_key)
        
        # Initialize cache
        self.cache_dir = cache_dir or os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "cache/llm_validation"
        )
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Initialize disk cache
        self.cache = Cache(
            directory=self.cache_dir,
            size_limit=cache_size_limit,
            eviction_policy='least-recently-used',
            statistics=True
        )
        
        # Set cache TTL
        self.cache_ttl = cache_ttl
        
        # Initialize thread pool for parallel processing
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        
        # Initialize async session
        self.session = None
        
        # Track cache statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_requests = 0
        
        logger.info(f"Initialized optimized LLM validator with cache at {self.cache_dir}")
    
    def _get_cache_key(self, text: str, security_level: str) -> str:
        """
        Generate a cache key for the given text and security level.
        
        Args:
            text (str): The text to validate
            security_level (str): The security level
            
        Returns:
            str: The cache key
        """
        # Create a hash of the text and security level
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        return f"{security_level}_{text_hash}"
    
    def _get_from_cache(self, text: str, security_level: str) -> Optional[Dict[str, Any]]:
        """
        Get a validation result from the cache.
        
        Args:
            text (str): The text to validate
            security_level (str): The security level
            
        Returns:
            Optional[Dict[str, Any]]: The cached validation result or None if not found
        """
        cache_key = self._get_cache_key(text, security_level)
        
        # Try to get the result from the cache
        result = self.cache.get(cache_key)
        
        # Update statistics
        self.total_requests += 1
        if result is not None:
            self.cache_hits += 1
            logger.debug(f"Cache hit for key: {cache_key}")
        else:
            self.cache_misses += 1
            logger.debug(f"Cache miss for key: {cache_key}")
        
        return result
    
    def _save_to_cache(self, text: str, security_level: str, result: Dict[str, Any]) -> None:
        """
        Save a validation result to the cache.
        
        Args:
            text (str): The text to validate
            security_level (str): The security level
            result (Dict[str, Any]): The validation result
        """
        cache_key = self._get_cache_key(text, security_level)
        
        # Save the result to the cache with TTL
        self.cache.set(cache_key, result, expire=self.cache_ttl)
        logger.debug(f"Saved to cache with key: {cache_key}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        hit_rate = self.cache_hits / self.total_requests if self.total_requests > 0 else 0
        
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "total": self.total_requests,
            "hit_rate": hit_rate,
            "size": self.cache.volume(),
            "max_size": self.cache.size_limit,
            "directory": self.cache_dir
        }
    
    def clear_cache(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        logger.info("Cache cleared")
    
    async def _async_validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Asynchronously validate text using the LLM.
        
        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation
                
        Returns:
            Dict[str, Any]: Validation result
        """
        context = context or {}
        security_level = context.get("security_level", "standard")
        
        # Check if the result is in the cache
        cached_result = self._get_from_cache(text, security_level)
        if cached_result is not None:
            return cached_result
        
        # If not in cache, perform the validation
        # Create async session if not already created
        if self.session is None:
            self.session = aiohttp.ClientSession()
        
        # Get the prompt for the security level
        prompt = self._get_prompt(text, security_level)
        
        # Make the API request
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 1000
            }
            
            start_time = time.time()
            
            async with self.session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                response_data = await response.json()
                
                end_time = time.time()
                elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                # Parse the response
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    response_text = response_data["choices"][0]["message"]["content"]
                    
                    # Parse the JSON response
                    try:
                        validation_result = json.loads(response_text)
                    except json.JSONDecodeError as e:
                        logger.error(f"Error parsing LLM response: {e}")
                        logger.error(f"Response text: {response_text}")
                        
                        # Try to extract JSON from the response
                        match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
                        if match:
                            try:
                                validation_result = json.loads(match.group(1))
                            except json.JSONDecodeError:
                                # If that fails, use a default result
                                validation_result = {
                                    "is_secure": False,
                                    "confidence": 0.2,
                                    "reason": "Error parsing LLM response"
                                }
                        else:
                            # If no JSON found, use a default result
                            validation_result = {
                                "is_secure": False,
                                "confidence": 0.2,
                                "reason": "Error parsing LLM response"
                            }
                    
                    # Add metadata to the result
                    result = {
                        "is_secure": validation_result.get("is_secure", False),
                        "method": "llm",
                        "confidence": validation_result.get("confidence", 0.5),
                        "threshold": self._get_threshold(security_level),
                        "reason": validation_result.get("reason", ""),
                        "response_time_ms": elapsed_time
                    }
                    
                    # Add optional fields if present
                    if "threats" in validation_result:
                        result["threats"] = validation_result["threats"]
                    
                    if "fix_suggestion" in validation_result:
                        result["fix_suggestion"] = validation_result["fix_suggestion"]
                    
                    # Save the result to the cache
                    self._save_to_cache(text, security_level, result)
                    
                    return result
                else:
                    logger.error(f"Error in LLM response: {response_data}")
                    return {
                        "is_secure": False,
                        "method": "llm",
                        "confidence": 0.2,
                        "threshold": self._get_threshold(security_level),
                        "reason": "Error in LLM response",
                        "response_time_ms": elapsed_time
                    }
        except Exception as e:
            logger.error(f"Error validating with LLM: {e}")
            return {
                "is_secure": False,
                "method": "llm",
                "confidence": 0.2,
                "threshold": self._get_threshold(security_level),
                "reason": f"Error validating with LLM: {e}"
            }
    
    def validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate text using the LLM with caching.
        
        Args:
            text (str): The text to validate
            context (Optional[Dict[str, Any]]): Additional context for validation
                
        Returns:
            Dict[str, Any]: Validation result
        """
        context = context or {}
        security_level = context.get("security_level", "standard")
        
        # Check if the result is in the cache
        cached_result = self._get_from_cache(text, security_level)
        if cached_result is not None:
            return cached_result
        
        # If not in cache, perform the validation
        return super().validate(text, context)
    
    async def validate_batch(self, texts: List[str], context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Validate multiple texts in parallel.
        
        Args:
            texts (List[str]): The texts to validate
            context (Optional[Dict[str, Any]]): Additional context for validation
                
        Returns:
            List[Dict[str, Any]]: Validation results
        """
        context = context or {}
        
        # Create tasks for each text
        tasks = [self._async_validate(text, context) for text in texts]
        
        # Run tasks in parallel
        results = await asyncio.gather(*tasks)
        
        return results
    
    def validate_batch_sync(self, texts: List[str], context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Validate multiple texts in parallel (synchronous version).
        
        Args:
            texts (List[str]): The texts to validate
            context (Optional[Dict[str, Any]]): Additional context for validation
                
        Returns:
            List[Dict[str, Any]]: Validation results
        """
        # Create an event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Run the async method in the event loop
            results = loop.run_until_complete(self.validate_batch(texts, context))
        finally:
            # Close the event loop
            loop.close()
        
        return results
    
    def __del__(self):
        """Clean up resources."""
        # Close the executor
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
        
        # Close the async session
        if hasattr(self, 'session') and self.session is not None:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.session.close())
            else:
                loop.run_until_complete(self.session.close())
