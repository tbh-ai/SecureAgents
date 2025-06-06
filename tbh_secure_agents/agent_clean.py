# tbh_secure_agents/agent.py
# Author: Saish (TBH.AI)

"""
Defines the core Expert class for the TBH Secure Agents framework.
Experts will encapsulate roles, goals, tools, and security contexts,
utilizing Google Gemini as the LLM.
"""

import google.generativeai as genai
import os
import re
import logging # Import logging
import json
import hashlib
import random
import string
import uuid
import asyncio
import nltk
from datetime import datetime, timedelta
from typing import Optional, List, Any, Dict, Tuple, Set

# Memory system imports
from .memory.memory_manager import MemoryManager
from .memory.models import MemoryType, MemoryPriority, MemoryAccess
from datetime import datetime, timedelta

# Import security components
from .security.prompt_defender import PromptDefender
from .security.data_guardian import DataGuardian
from .security.agent_sentinel import AgentSentinel
from .security.reliability_monitor import ReliabilityMonitor
from .security_profiles import (
    SecurityProfile, get_security_thresholds, get_security_checks,
    log_security_profile_info, get_cached_regex, cache_security_validation
)

# Get a logger for this module
logger = logging.getLogger(__name__)

# Configure the Gemini API key securely
# The library automatically looks for the GOOGLE_API_KEY environment variable.
# Ensure this variable is set in your environment.
# Example: export GOOGLE_API_KEY='YOUR_API_KEY'
# Configuration will now happen within Expert __init__ if key is provided

# Removed duplicate class definition here (already done)

class Expert:
    """
    Represents an autonomous expert within the TBH Secure Agents framework.

    Attributes:
        specialty (str): The specialty of the expert (e.g., 'Security Analyst').
        objective (str): The primary objective of the expert.
        background (str, optional): A description of the expert's background.
        llm_model_name (str): The specific Gemini model to use (e.g., 'gemini-pro'). Defaults to 'gemini-2.0-flash-lite'.
        tools (List[Any], optional): A list of tools available to the expert.
        security_profile (str, optional): Defines the security constraints and capabilities. Defaults to 'standard'.
        api_key (str, optional): API key for Google Generative AI.
        memory_enabled (bool, optional): Enable TBH Secure Agents v5.0 memory system. Defaults to True.
        user_id (str, optional): User identifier for memory system. Defaults to 'default_user'.
        enable_visualization (bool, optional): Enable automatic visualization and reporting. Defaults to False.
        auto_generate_reports (bool, optional): Automatically generate HTML reports for each task. Defaults to False.
        visualization_output_dir (str, optional): Directory for saving visualization reports. Defaults to 'expert_reports'.
        use_llm_recommendations (bool, optional): Use LLM for generating security recommendations. Defaults to True.
        auto_open_reports (bool, optional): Automatically open generated reports in browser. Defaults to False.
    """
    
    def __init__(self,
                 specialty: str,
                 objective: str,
                 background: Optional[str] = None,
                 llm_model_name: str = 'gemini-2.0-flash-lite', # Updated default model name per user request
                 tools: Optional[List[Any]] = None,
                 security_profile: str = 'standard',
                 api_key: Optional[str] = None, # Add api_key parameter
                 # Memory system parameters for TBH Secure Agents v5.0
                 memory_enabled: bool = True,
                 user_id: str = 'default_user',
                 # Visualization hyperparameters
                 enable_visualization: bool = False,
                 auto_generate_reports: bool = False,
                 visualization_output_dir: Optional[str] = None,
                 use_llm_recommendations: bool = True,
                 auto_open_reports: bool = False):
        self.specialty = specialty
        self.objective = objective
        self.background = background
        self.llm_model_name = llm_model_name
        self.tools = tools or []
        self.security_profile_str = security_profile
        self.llm: Optional[genai.GenerativeModel] = None

        # Initialize visualization parameters
        self.enable_visualization = enable_visualization
        self.auto_generate_reports = auto_generate_reports
        self.visualization_output_dir = visualization_output_dir or "expert_reports"
        self.use_llm_recommendations = use_llm_recommendations
        self.auto_open_reports = auto_open_reports
        self.visualizer = None  # Will be initialized if visualization is enabled

        # PERFECT: Use string-based security profiles directly
        # Map legacy profile names to standardized names
        if security_profile in ["default"]:
            self.security_profile = "standard"
        elif security_profile in ["development", "testing"]:
            self.security_profile = "minimal"
        elif security_profile in ["basic"]:
            self.security_profile = "standard"
        elif security_profile in ["high_security", "code_restricted"]:
            self.security_profile = "high"
        elif security_profile in ["maximum_security", "air_gapped"]:
            self.security_profile = "maximum"
        else:
            # Use the profile as-is if it's one of the standard ones
            if security_profile in ["minimal", "standard", "high", "maximum"]:
                self.security_profile = security_profile
            else:
                # Default to standard for unknown profiles
                self.security_profile = "standard"
                logger.warning(f"Unknown security profile '{security_profile}', defaulting to 'standard'")

        # Set security level for backward compatibility
        security_level = self.security_profile

        # Set default security thresholds and checks
        self.security_thresholds = {"injection_score": 0.6, "sensitive_data": 0.5}
        self.security_checks = {"content_analysis": True, "output_validation": True}

        # Initialize security components with appropriate security level
        self.prompt_defender = PromptDefender(security_level=security_level)
        self.data_guardian = DataGuardian(security_level=security_level)
        self.agent_sentinel = AgentSentinel(security_level=security_level)
        self.reliability_monitor = ReliabilityMonitor(security_level=security_level)

        # Generate a unique ID for this expert
        self.expert_id = str(uuid.uuid4())

        # Register with agent sentinel
        self.security_token = self.agent_sentinel.register_agent(
            self.expert_id,
            {
                "specialty": self.specialty,
                "objective": self.objective,
                "security_profile": self.security_profile
            }
        )

        logger.info(f"Expert '{self.specialty}' security components initialized with level '{security_level}'")

        # --- Initialize Gemini LLM ---
        # Prioritize explicitly passed API key, fall back to environment variable
        effective_api_key = api_key or os.getenv("GOOGLE_API_KEY")

        if effective_api_key:
            try:
                # Configure the API key (Note: genai.configure is global)
                # In a multi-key scenario, this might need a more complex setup
                genai.configure(api_key=effective_api_key)
                logger.info("Gemini API configured.") # Use logger

                # Create the model instance
                # TODO: Add generation_config and safety_settings based on security_profile
                self.llm = genai.GenerativeModel(self.llm_model_name)
                logger.info(f"Expert '{self.specialty}' initialized with Gemini model '{self.llm_model_name}' and security profile '{self.security_profile}'.") # Use logger

            except Exception as e:
                logger.error(f"Error initializing Gemini model for expert '{self.specialty}': {e}", exc_info=True) # Use logger, add traceback
                self.llm = None # Ensure llm is None if initialization fails
        else:
            logger.warning(f"Expert '{self.specialty}' initialized WITHOUT a functional LLM (No API key found/provided).")

        # Initialize TBH Secure Agents v5.0 Memory System
        self.memory_enabled = memory_enabled
        self.user_id = user_id
        self.memory_manager = None
        
        if self.memory_enabled:
            try:
                from .memory import MemoryManager, MemorySystemConfig
                
                # Create memory configuration based on security profile
                memory_config = self._create_memory_config()
                
                # Initialize memory manager
                self.memory_manager = MemoryManager(memory_config)
                
                # Store memory initialization as async task for later completion
                self._memory_init_task = asyncio.create_task(self._complete_memory_initialization())
                
                logger.info(f"Expert '{self.specialty}' memory system initialized for user '{self.user_id}'")
                
            except Exception as e:
                logger.warning(f"Expert '{self.specialty}' memory initialization failed: {e}")
                self.memory_enabled = False
                self.memory_manager = None
        else:
            logger.debug(f"Expert '{self.specialty}' memory disabled by configuration")
        
        # Initialize memory performance tracking
        if self.memory_enabled:
            self._initialize_memory_performance_tracking()
        
        logger.debug(f"Expert '{self.specialty}' memory initialization completed.")

        # Initialize visualization components if enabled
        if self.enable_visualization:
            self._initialize_visualization(effective_api_key)

        # Initialize hybrid security validation by default
        self._initialize_hybrid_validation(effective_api_key)

    # ...existing execute_task method...

    # ...existing security methods...

    # ==================== MEMORY OPERATIONS ====================
    
    async def remember(self, key: str, value: str, memory_type: str = "general", 
                      priority: str = "normal", tags: List[str] = None) -> bool:
        """
        Store information in the memory system with enterprise-level error handling.
        
        Args:
            key: Unique identifier for the memory
            value: Content to store
            memory_type: Type of memory (preference, task, context, etc.)
            priority: Priority level (low, normal, high, critical)
            tags: Optional tags for categorization
            
        Returns:
            bool: True if successfully stored, False otherwise
        """
        if not self.memory_enabled or not self.memory_manager:
            return False
            
        start_time = datetime.now()
        
        try:
            # Track the operation
            self._track_memory_operation("remember", True, 0)
            
            # Convert priority string to enum
            priority_map = {
                "low": MemoryPriority.LOW,
                "normal": MemoryPriority.NORMAL,
                "high": MemoryPriority.HIGH,
                "critical": MemoryPriority.CRITICAL
            }
            priority_enum = priority_map.get(priority, MemoryPriority.NORMAL)
            
            # Convert memory_type string to enum
            type_map = {
                "general": MemoryType.EPISODIC,
                "preference": MemoryType.PREFERENCE,
                "task": MemoryType.TASK,
                "context": MemoryType.SEMANTIC,
                "procedural": MemoryType.PROCEDURAL
            }
            type_enum = type_map.get(memory_type, MemoryType.EPISODIC)
            
            # Store the memory
            result = await self.memory_manager.store(
                content=value,
                memory_type=type_enum,
                priority=priority_enum,
                tags=tags or [],
                metadata={
                    "key": key,
                    "timestamp": datetime.now().isoformat(),
                    "user_id": self.user_id,
                    "specialist": self.specialty
                }
            )
            
            # Track successful operation
            duration = (datetime.now() - start_time).total_seconds()
            self._track_memory_operation("remember", True, duration)
            
            # Log the operation
            if hasattr(self, 'reliability_monitor') and self.reliability_monitor:
                self.reliability_monitor.log_metric('memory_store_success', 1)
                
            return result
            
        except Exception as e:
            # Track failed operation
            duration = (datetime.now() - start_time).total_seconds()
            self._track_memory_operation("remember", False, duration)
            
            logger.error(f"Memory storage failed for key '{key}': {e}")
            
            if hasattr(self, 'reliability_monitor') and self.reliability_monitor:
                self.reliability_monitor.log_error('memory_store_error', str(e))
                
            return False
        
    async def recall(self, query: str, memory_type: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve information from memory with advanced filtering and caching.
        
        Args:
            query: Search query
            memory_type: Optional type filter
            limit: Maximum number of results
            
        Returns:
            List[Dict]: Retrieved memories with metadata
        """
        if not self.memory_enabled or not self.memory_manager:
            return []
            
        start_time = datetime.now()
        
        try:
            # Check cache first
            cache_key = f"recall_{hash(query)}_{memory_type}_{limit}"
            cached_result = self._cached_memory_recall(cache_key)
            if cached_result:
                self._track_memory_operation("recall_cached", True, 0)
                return cached_result
            
            # Convert memory_type string to enum if provided
            type_filter = None
            if memory_type:
                type_map = {
                    "general": MemoryType.EPISODIC,
                    "preference": MemoryType.PREFERENCE,
                    "task": MemoryType.TASK,
                    "context": MemoryType.SEMANTIC,
                    "procedural": MemoryType.PROCEDURAL
                }
                type_filter = type_map.get(memory_type)
            
            # Search memories
            memories = await self.memory_manager.search_memories(
                query=query,
                memory_type=type_filter,
                limit=limit,
                user_id=self.user_id
            )
            
            # Format results
            results = []
            for memory in memories:
                results.append({
                    "content": memory.content,
                    "type": memory.memory_type.value if hasattr(memory.memory_type, 'value') else str(memory.memory_type),
                    "priority": memory.priority.value if hasattr(memory.priority, 'value') else str(memory.priority),
                    "tags": memory.tags,
                    "metadata": memory.metadata,
                    "relevance_score": getattr(memory, 'relevance_score', 0.0),
                    "timestamp": memory.created_at.isoformat() if hasattr(memory, 'created_at') else None
                })
            
            # Cache the results
            if hasattr(self, 'memory_cache'):
                self.memory_cache[cache_key] = {
                    'data': results,
                    'timestamp': datetime.now()
                }
            
            # Track successful operation
            duration = (datetime.now() - start_time).total_seconds()
            self._track_memory_operation("recall", True, duration)
            
            if hasattr(self, 'reliability_monitor') and self.reliability_monitor:
                self.reliability_monitor.log_metric('memory_recall_success', len(results))
                
            return results
            
        except Exception as e:
            # Track failed operation
            duration = (datetime.now() - start_time).total_seconds()
            self._track_memory_operation("recall", False, duration)
            
            logger.error(f"Memory recall failed for query '{query}': {e}")
            
            if hasattr(self, 'reliability_monitor') and self.reliability_monitor:
                self.reliability_monitor.log_error('memory_recall_error', str(e))
                
            return []
        
    async def execute_with_memory(self, task: str, context: Dict[str, Any] = None) -> str:
        """
        Execute a task with full memory-enhanced processing including context merging and learning.
        
        Args:
            task: Task description
            context: Additional context information
            
        Returns:
            str: Task result enhanced with memory insights
        """
        if not self.memory_enabled or not self.memory_manager:
            # Fallback to standard execution
            return self.execute_task(task, context)
            
        start_time = datetime.now()
        
        try:
            # Phase 1: Recall relevant context
            relevant_context = await self._recall_relevant_context(task)
            user_preferences = await self._get_user_preferences("task_execution")
            historical_patterns = await self._get_historical_task_patterns(self._classify_task(task))
            
            # Phase 2: Merge contexts
            all_contexts = [context or {}, relevant_context, user_preferences, historical_patterns]
            merged_context = self._merge_contexts_advanced(all_contexts)
            
            # Phase 3: Execute with enhanced context
            enhanced_prompt = self._create_memory_enhanced_prompt(task, merged_context)
            result = self.execute_task(enhanced_prompt, merged_context)
            
            # Phase 4: Learn from execution
            await self._learn_from_memory_execution(task, result, merged_context)
            
            # Track successful operation
            duration = (datetime.now() - start_time).total_seconds()
            self._track_memory_operation("execute_with_memory", True, duration)
            
            if hasattr(self, 'reliability_monitor') and self.reliability_monitor:
                self.reliability_monitor.log_metric('memory_enhanced_execution_success', 1)
                
            return result
            
        except Exception as e:
            # Track failed operation and fallback
            duration = (datetime.now() - start_time).total_seconds()
            self._track_memory_operation("execute_with_memory", False, duration)
            
            logger.error(f"Memory-enhanced execution failed, falling back to standard execution: {e}")
            
            if hasattr(self, 'reliability_monitor') and self.reliability_monitor:
                self.reliability_monitor.log_error('memory_execution_error', str(e))
                
            # Fallback to standard execution
            return self.execute_task(task, context)

    # ==================== MEMORY HELPER METHODS ====================
    
    async def _recall_relevant_context(self, task: str) -> Dict[str, Any]:
        """Recall context relevant to the current task."""
        try:
            # Search for related memories
            related_memories = await self.recall(task, limit=5)
            
            # Extract relevant context
            context = {
                "related_tasks": [],
                "relevant_knowledge": [],
                "success_patterns": []
            }
            
            for memory in related_memories:
                if memory.get("type") == "task":
                    context["related_tasks"].append(memory["content"])
                elif memory.get("type") == "context":
                    context["relevant_knowledge"].append(memory["content"])
                elif "success" in memory.get("tags", []):
                    context["success_patterns"].append(memory["content"])
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to recall relevant context: {e}")
            return {}
    
    async def _get_user_preferences(self, category: str = "general") -> Dict[str, Any]:
        """Retrieve user preferences for the specified category."""
        try:
            preferences = await self.recall(f"user preference {category}", "preference", limit=10)
            
            parsed_preferences = {}
            for pref in preferences:
                # Parse preference content
                content = pref.get("content", "")
                if ":" in content:
                    key, value = content.split(":", 1)
                    parsed_preferences[key.strip()] = value.strip()
            
            return {"user_preferences": parsed_preferences}
            
        except Exception as e:
            logger.error(f"Failed to get user preferences: {e}")
            return {}
    
    async def _get_historical_task_patterns(self, task_type: str) -> Dict[str, Any]:
        """Retrieve historical patterns for similar tasks."""
        try:
            patterns = await self.recall(f"task pattern {task_type}", "task", limit=5)
            
            return {
                "historical_patterns": [p.get("content", "") for p in patterns],
                "task_type": task_type,
                "pattern_count": len(patterns)
            }
            
        except Exception as e:
            logger.error(f"Failed to get historical patterns: {e}")
            return {}

    def _merge_contexts_advanced(self, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple context dictionaries with conflict resolution."""
        merged = {}
        
        for context in contexts:
            if not isinstance(context, dict):
                continue
                
            for key, value in context.items():
                if key not in merged:
                    merged[key] = value
                elif isinstance(value, list) and isinstance(merged[key], list):
                    # Merge lists and remove duplicates
                    merged[key] = list(set(merged[key] + value))
                elif isinstance(value, dict) and isinstance(merged[key], dict):
                    # Recursively merge dictionaries
                    merged[key] = {**merged[key], **value}
                else:
                    # For other types, keep the most recent value
                    merged[key] = value
        
        return merged
    
    async def _learn_from_memory_execution(self, task: str, result: str, context: Dict[str, Any]) -> None:
        """Learn from task execution and store patterns for future use."""
        try:
            # Classify task and result quality
            task_type = self._classify_task(task)
            result_quality = self._assess_result_quality(result)
            
            # Store task execution pattern
            pattern_content = f"Task: {task_type}, Quality: {result_quality}, Context: {len(context)} items"
            await self.remember(
                f"execution_pattern_{datetime.now().isoformat()}",
                pattern_content,
                memory_type="task",
                priority="normal",
                tags=["pattern", task_type, result_quality]
            )
            
            # Update user preferences based on successful patterns
            if result_quality in ["high", "excellent"]:
                await self._update_user_preferences(task, context, result)
            
            # Store successful methodologies
            if result_quality in ["high", "excellent"]:
                methodology = self._extract_methodology(task, context, result)
                await self.remember(
                    f"successful_methodology_{task_type}",
                    methodology,
                    memory_type="procedural",
                    priority="high",
                    tags=["success", "methodology", task_type]
                )
                
        except Exception as e:
            logger.error(f"Failed to learn from execution: {e}")

    def _classify_task(self, task: str) -> str:
        """Classify the task type for pattern recognition."""
        task_lower = task.lower()
        
        if any(keyword in task_lower for keyword in ["analyze", "analysis", "examine"]):
            return "analysis"
        elif any(keyword in task_lower for keyword in ["security", "vulnerability", "threat"]):
            return "security"
        elif any(keyword in task_lower for keyword in ["report", "document", "write"]):
            return "documentation"
        elif any(keyword in task_lower for keyword in ["recommend", "suggest", "advice"]):
            return "recommendation"
        else:
            return "general"
    
    def _assess_result_quality(self, result: str) -> str:
        """Assess the quality of the task result."""
        if not result or len(result) < 50:
            return "low"
        elif len(result) < 200:
            return "medium"
        elif len(result) < 500:
            return "high"
        else:
            return "excellent"

    async def _update_user_preferences(self, task: str, context: Dict[str, Any], result: str) -> None:
        """Update user preferences based on successful task patterns."""
        try:
            # Extract preference indicators from successful execution
            if "detailed" in result.lower() and len(result) > 300:
                await self.remember(
                    "user_prefers_detailed_responses",
                    "User prefers detailed and comprehensive responses",
                    memory_type="preference",
                    priority="normal",
                    tags=["preference", "detail"]
                )
            
            # Store context preferences
            if context.get("user_preferences"):
                for pref_key, pref_value in context["user_preferences"].items():
                    await self.remember(
                        f"user_preference_{pref_key}",
                        f"{pref_key}: {pref_value}",
                        memory_type="preference",
                        priority="normal",
                        tags=["preference", pref_key]
                    )
                    
        except Exception as e:
            logger.error(f"Failed to update user preferences: {e}")
    
    def _extract_methodology(self, task: str, context: Dict[str, Any], result: str) -> str:
        """Extract successful methodology from task execution."""
        return f"Successful approach for {self._classify_task(task)}: Used context with {len(context)} elements, produced {len(result)} character result with high quality indicators."
    
    def _create_memory_enhanced_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Create an enhanced prompt incorporating memory context."""
        base_prompt = task
        
        # Add relevant context
        if context.get("relevant_knowledge"):
            base_prompt += f"\n\nRelevant knowledge: {'; '.join(context['relevant_knowledge'][:3])}"
        
        # Add user preferences
        if context.get("user_preferences"):
            prefs = [f"{k}: {v}" for k, v in list(context["user_preferences"].items())[:3]]
            base_prompt += f"\n\nUser preferences: {'; '.join(prefs)}"
        
        # Add success patterns
        if context.get("success_patterns"):
            base_prompt += f"\n\nPrevious successful approaches: {'; '.join(context['success_patterns'][:2])}"
        
        return base_prompt
    
    def _create_memory_config(self) -> Dict[str, Any]:
        """Create memory configuration based on security profile and requirements."""
        base_config = {
            "user_id": self.user_id,
            "encryption_enabled": True,
            "retention_days": 30,
            "max_memories": 10000,
            "compression_enabled": True
        }
        
        # Adjust config based on security profile
        if hasattr(self, 'security_profile'):
            if self.security_profile == "maximum":
                base_config.update({
                    "encryption_enabled": True,
                    "retention_days": 7,
                    "max_memories": 5000,
                    "audit_logging": True
                })
            elif self.security_profile == "high":
                base_config.update({
                    "encryption_enabled": True,
                    "retention_days": 14,
                    "max_memories": 7500
                })
        
        return base_config

    # ==================== MEMORY QUALITY ASSURANCE METHODS ====================
    
    async def cleanup_memory_resources(self, force: bool = False) -> Dict[str, Any]:
        """Comprehensive memory resource cleanup with monitoring."""
        cleanup_results = {
            "status": "completed",
            "cleaned_items": 0,
            "freed_memory": 0,
            "errors": []
        }
        
        try:
            # Clear performance tracking cache if force cleanup
            if force and hasattr(self, 'memory_cache'):
                cache_size = len(self.memory_cache)
                self.memory_cache.clear()
                cleanup_results["cleaned_items"] += cache_size
                
        except Exception as e:
            cleanup_results["status"] = "failed"
            cleanup_results["errors"].append(str(e))
            logger.error(f"Memory cleanup failed: {e}")
        
        return cleanup_results
    
    def get_memory_health_status(self) -> Dict[str, Any]:
        """Get comprehensive memory system health status."""
        health_status = {
            "overall_health": "unknown",
            "memory_enabled": self.memory_enabled,
            "manager_status": "unknown",
            "cache_status": "unknown",
            "performance_metrics": {}
        }
        
        try:
            # Check memory manager status
            if self.memory_enabled and self.memory_manager:
                health_status["manager_status"] = "active"
                health_status["overall_health"] = "healthy"
            elif self.memory_enabled:
                health_status["manager_status"] = "enabled_but_inactive"
                health_status["overall_health"] = "degraded"
            else:
                health_status["manager_status"] = "disabled"
                health_status["overall_health"] = "disabled"
            
            # Check cache status
            if hasattr(self, 'memory_cache'):
                cache_size = len(self.memory_cache)
                health_status["cache_status"] = f"active_{cache_size}_entries"
            else:
                health_status["cache_status"] = "not_initialized"
                
        except Exception as e:
            health_status["overall_health"] = "error"
            health_status["error"] = str(e)
            logger.error(f"Memory health check failed: {e}")
        return health_status
    
    def get_memory_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed memory performance metrics."""
        if not hasattr(self, 'memory_performance'):
            return {"error": "Performance tracking not initialized"}
        
        metrics = self.memory_performance.copy()
        
        # Calculate derived metrics
        try:
            total_operations = sum([
                metrics.get('remember_count', 0),
                metrics.get('recall_count', 0),
                metrics.get('execute_with_memory_count', 0)
            ])
            
            total_successes = sum([
                metrics.get('remember_success', 0),
                metrics.get('recall_success', 0),
                metrics.get('execute_with_memory_success', 0)
            ])
            
            # Calculate rates
            if total_operations > 0:
                metrics['overall_success_rate'] = total_successes / total_operations
            else:
                metrics['overall_success_rate'] = 0.0
            
            # Add timestamp
            metrics['last_updated'] = datetime.now().isoformat()
            
        except Exception as e:
            metrics['calculation_error'] = str(e)
            logger.error(f"Error calculating performance metrics: {e}")
        return metrics
    
    async def optimize_memory_performance(self) -> Dict[str, Any]:
        """Optimize memory system performance through various strategies."""
        optimization_results = {
            "status": "completed",
            "optimizations_applied": ["cache_cleanup", "storage_optimization"],
            "performance_improvement": {},
            "recommendations": []
        }
        
        try:
            initial_metrics = self.get_memory_performance_metrics()
            
            # Clean expired cache entries
            if hasattr(self, 'memory_cache'):
                cleaned_entries = await self._cleanup_expired_memories()
                if cleaned_entries == 0:
                    optimization_results["optimizations_applied"].remove("cache_cleanup")
            
            # Compare performance
            final_metrics = self.get_memory_performance_metrics()
            optimization_results["performance_improvement"] = {
                "optimization_timestamp": datetime.now().isoformat()
            }
            
            # Generate recommendations
            if final_metrics.get('overall_success_rate', 1.0) < 0.9:
                optimization_results['recommendations'].append('Review error handling and fallback mechanisms')
            
        except Exception as e:
            optimization_results['status'] = 'failed'
            optimization_results['error'] = str(e)
            logger.error(f"Memory performance optimization failed: {e}")
        return optimization_results

    # ==================== MEMORY SUPPORTING METHODS ====================
    
    def _initialize_memory_performance_tracking(self) -> None:
        """Initialize memory performance tracking infrastructure."""
        self.memory_performance = {
            'remember_count': 0,
            'remember_success': 0,
            'recall_count': 0,
            'recall_success': 0,
            'execute_with_memory_count': 0,
            'execute_with_memory_success': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_operation_time': 0.0,
            'average_operation_time': 0.0
        }
        self.memory_cache = {}

    def _track_memory_operation(self, operation: str, success: bool, duration: float) -> None:
        """Track memory operation metrics."""
        if not hasattr(self, 'memory_performance'):
            return
        
        count_key = f"{operation}_count"
        success_key = f"{operation}_success"
        
        self.memory_performance[count_key] = self.memory_performance.get(count_key, 0) + 1
        if success:
            self.memory_performance[success_key] = self.memory_performance.get(success_key, 0) + 1
        
        # Update timing
        self.memory_performance['total_operation_time'] += duration
        total_ops = sum([
            self.memory_performance.get('remember_count', 0),
            self.memory_performance.get('recall_count', 0),
            self.memory_performance.get('execute_with_memory_count', 0)
        ])
        if total_ops > 0:
            self.memory_performance['average_operation_time'] = self.memory_performance['total_operation_time'] / total_ops

    def _cached_memory_recall(self, cache_key: str) -> Optional[List[Dict[str, Any]]]:
        """Retrieve memories from cache if available and not expired."""
        if not hasattr(self, 'memory_cache'):
            return None
        
        cached_data = self.memory_cache.get(cache_key)
        if not cached_data:
            return None
        
        # Check if cache entry has expired (5 minute TTL)
        if isinstance(cached_data, dict) and 'timestamp' in cached_data:
            cache_age = (datetime.now() - cached_data['timestamp']).total_seconds()
            if cache_age > 300:  # 5 minutes
                del self.memory_cache[cache_key]
                return None
            
            # Track cache hit
            if hasattr(self, 'memory_performance'):
                self.memory_performance['cache_hits'] = self.memory_performance.get('cache_hits', 0) + 1
            
            return cached_data.get('data')
        return None
    
    async def _cleanup_expired_memories(self) -> int:
        """Clean up expired memory entries and return count of cleaned items."""
        cleaned_count = 0
        
        try:
            # Clean local cache
            if hasattr(self, 'memory_cache'):
                expired_keys = []
                current_time = datetime.now()
                
                for key, cached_data in list(self.memory_cache.items()):
                    if isinstance(cached_data, dict) and 'timestamp' in cached_data:
                        cache_age = (current_time - cached_data['timestamp']).total_seconds()
                        if cache_age > 300:  # 5 minutes TTL
                            expired_keys.append(key)
                
                for key in expired_keys:
                    del self.memory_cache[key]
                
                cleaned_count += len(expired_keys)
                
        except Exception as e:
            logger.error(f"Error cleaning expired memories: {e}")
        return cleaned_count
    
    async def _optimize_memory_storage(self) -> Dict[str, Any]:
        """Optimize memory storage and return optimization results."""
        optimization_result = {
            "optimized": False,
            "freed_bytes": 0,
            "compression_applied": False
        }
        
        try:
            # Optimize local cache
            if hasattr(self, 'memory_cache') and len(self.memory_cache) > 100:
                # Remove oldest entries if cache is too large
                cache_items = list(self.memory_cache.items())
                cache_items.sort(key=lambda x: x[1].get('timestamp', datetime.min) if isinstance(x[1], dict) else datetime.min)
                
                # Keep only the newest 100 entries
                entries_to_remove = len(cache_items) - 100
                if entries_to_remove > 0:
                    for i in range(entries_to_remove):
                        key = cache_items[i][0]
                        if key in self.memory_cache:
                            del self.memory_cache[key]
                    
                    optimization_result["optimized"] = True
                    optimization_result["freed_bytes"] += entries_to_remove * 1024  # Estimated
                    
        except Exception as e:
            logger.error(f"Error optimizing memory storage: {e}")
        
        return optimization_result

    # ...existing methods (execute_task, security methods, etc.)...
