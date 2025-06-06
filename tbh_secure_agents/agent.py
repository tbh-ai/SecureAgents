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
import nltk
from typing import Optional, List, Any, Dict, Tuple, Set

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
        memory_duration (str, optional): Memory duration setting: "short_term", "long_term", "auto", "disabled". Defaults to "auto".
        user_id (str, optional): User ID for memory management. Auto-generated if not provided.
        enable_visualization (bool, optional): Enable automatic visualization and reporting. Defaults to False.
        auto_generate_reports (bool, optional): Automatically generate HTML reports for each task. Defaults to False.        visualization_output_dir (str, optional): Directory for saving visualization reports. Defaults to 'expert_reports'.
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
                 # Memory parameters
                 memory_duration: str = "auto",  # Memory duration: "short_term", "long_term", "auto", "disabled"
                 memory_enabled: Optional[bool] = None,  # Backward compatibility parameter
                 user_id: Optional[str] = None,  # User ID for memory management
                 # Visualization hyperparameters
                 enable_visualization: bool = False,
                 auto_generate_reports: bool = False,
                 visualization_output_dir: Optional[str] = None,
                 use_llm_recommendations: bool = True,
                 auto_open_reports: bool = False): # Add visualization parameters
        self.specialty = specialty
        self.objective = objective
        self.background = background
        self.llm_model_name = llm_model_name
        self.tools = tools or []
        self.security_profile_str = security_profile
        self.llm: Optional[genai.GenerativeModel] = None        # Set user ID for memory management
        self.user_id = user_id or f"user_{hashlib.md5(specialty.encode()).hexdigest()[:8]}"

        # Handle backward compatibility for memory_enabled parameter
        if memory_enabled is not None:
            if memory_enabled is False:
                # memory_enabled=False overrides any memory_duration setting
                memory_duration = "disabled"
            elif memory_enabled is True and memory_duration == "auto":
                # memory_enabled=True with default duration stays as auto
                pass
        
        # Initialize memory duration and validate
        self.memory_duration = self._validate_memory_duration(memory_duration)
        self.memory_enabled = self.memory_duration != "disabled"
        
        # Initialize memory manager based on memory duration
        self.memory_manager = None
        if self.memory_enabled:
            try:
                memory_config = self._create_memory_config_with_duration(self.memory_duration)                # Import memory manager here to avoid circular imports
                from .memory.memory_manager import MemoryManager
                from .memory.config import MemorySystemConfig
                  # Create memory system configuration
                config = MemorySystemConfig.from_dict(memory_config)
                
                self.memory_manager = MemoryManager(config)
                self.memory_manager.sync_initialize()
                logger.info(f"Memory manager initialized with {self.memory_duration} configuration")
                
            except Exception as e:
                logger.warning(f"Failed to initialize memory manager: {e}. Memory disabled.")
                self.memory_enabled = False
                self.memory_manager = None

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
             logger.warning(f"Expert '{self.specialty}' initialized WITHOUT a functional LLM (No API key found/provided).") # Use logger

        # Initialize other components like memory, potentially based on kwargs or profile
        self.memory = None # Placeholder for expert memory/chat history
        # TODO: Implement actual memory initialization (e.g., based on kwargs or a Memory class)
        logger.debug(f"Expert '{self.specialty}' memory initialized (placeholder).")

        # Initialize visualization components if enabled
        if self.enable_visualization:
            self._initialize_visualization(effective_api_key)

        # Initialize hybrid security validation by default
        self._initialize_hybrid_validation(effective_api_key)


    def execute_task(self, task_description: str, context: Optional[str] = None, inputs: Optional[Dict[str, Any]] = None) -> str:
        """
        Executes a given operation description using the configured Gemini LLM.
        This method will involve constructing a prompt, interacting with the LLM,
        potentially using tools (future implementation), and applying security checks.

        Args:
            task_description (str): The description of the operation to execute.
            context (Optional[str]): Relevant context from previous operations or external data.
            inputs (Optional[Dict[str, Any]]): Dynamic inputs that can be used to format the prompt.

        Returns:
            str: The result generated by the LLM or an error message.
        """
        if not self.llm:
            logger.error(f"Expert '{self.specialty}' cannot execute operation: LLM not initialized.") # Use logger
            return f"Error: Expert '{self.specialty}' cannot execute operation. LLM not initialized (check API key and configuration)."

        logger.info(f"Expert '{self.specialty}' starting operation execution: {task_description[:100]}...") # Use logger

        # Initialize inputs if not provided
        if inputs is None:
            inputs = {}

        # Generate a unique operation ID for monitoring
        operation_id = f"task_{str(uuid.uuid4())[:8]}"

        # Start monitoring this operation with ReliabilityMonitor
        self.reliability_monitor.monitor_execution(
            operation_id=operation_id,
            operation_type="expert_task",
            inputs={
                "task_description": task_description[:100] + "..." if len(task_description) > 100 else task_description,
                "context_provided": context is not None,
                "inputs_provided": bool(inputs)
            }
        )

        # --- Prompt Engineering ---
        # Construct a prompt incorporating specialty, objective, operation, context, and security constraints.
        # This is a crucial area for security: ensure prompts don't enable injection attacks
        # and guide the LLM towards secure and relevant outputs.

        # Format specialty, objective, and background with inputs if they contain template variables
        specialty = self._format_with_inputs(self.specialty, inputs)
        objective = self._format_with_inputs(self.objective, inputs)

        prompt = f"You are {specialty}. Your objective is {objective}."

        if self.background:
            background = self._format_with_inputs(self.background, inputs)
            prompt += f" Your background is: {background}."

        if context:
            # Check context for sensitive data before including it
            if self.security_profile in ['high_security', 'pii_protection', 'confidential']:
                # Sanitize context before including it
                formatted_context = self._format_with_inputs(context, inputs)
                sanitized_context = self.data_guardian.sanitize_text(formatted_context)
                prompt += f"\n\nRelevant context:\n{sanitized_context}"

                # Record if sanitization occurred
                if sanitized_context != formatted_context:
                    self.reliability_monitor.record_checkpoint(
                        operation_id=operation_id,
                        checkpoint_name="context_sanitization",
                        data={"sanitization_applied": True}
                    )
                    logger.info(f"Context was sanitized to remove sensitive information")
            else:
                formatted_context = self._format_with_inputs(context, inputs)
                prompt += f"\n\nRelevant context:\n{formatted_context}"

        # Format task description with inputs
        formatted_task = self._format_with_inputs(task_description, inputs)
        prompt += f"\n\nCurrent Operation: {formatted_task}"
        prompt += f"\n\nPlease provide the result for this operation, keeping in mind your specialty and objective."

        # Add security-specific instructions based on security profile
        if self.security_profile == 'high_security':
            prompt += f"\n\nIMPORTANT: Maintain high security standards. Do not reveal any sensitive information, credentials, or internal data. Sanitize all outputs."
        elif self.security_profile == 'pii_protection':
            prompt += f"\n\nIMPORTANT: Do not include any personally identifiable information (PII) in your response. Redact or generalize any PII."
        elif self.security_profile == 'code_restricted':
            prompt += f"\n\nIMPORTANT: Do not include any executable code, scripts, or commands in your response."

        # Record the prompt construction checkpoint
        self.reliability_monitor.record_checkpoint(
            operation_id=operation_id,
            checkpoint_name="prompt_construction",
            data={"prompt_length": len(prompt)}
        )

        # --- Security Check (Pre-LLM) ---
        # Use PromptDefender to check for security issues
        if not self._is_prompt_secure(prompt):
            logger.error(f"Prompt failed pre-execution security check for expert '{self.specialty}'. Operation aborted.") # Use logger

            # Record the security failure
            self.reliability_monitor.record_error(
                operation_id=operation_id,
                error_type="security_check_failure",
                error_message="Prompt failed pre-execution security check",
                error_data={"stage": "pre_execution"}
            )

            # Complete the operation with failure
            self.reliability_monitor.complete_execution(
                operation_id=operation_id,
                output="Error: Security check failed",
                metadata={"success": False}
            )

            return f"Error: Prompt failed pre-execution security check for expert '{self.specialty}'."

        # --- LLM Interaction ---
        # Basic retry logic implemented below
        max_retries = 1 # Example: Allow 1 retry
        attempts = 0
        llm_output = None # Initialize output variable

        while attempts <= max_retries:
            attempts += 1
            try:
                logger.debug(f"LLM interaction attempt {attempts} for expert '{self.specialty}'.")

                # Record the LLM interaction attempt
                self.reliability_monitor.record_checkpoint(
                    operation_id=operation_id,
                    checkpoint_name=f"llm_interaction_attempt_{attempts}",
                    data={"attempt": attempts}
                )

                # TODO: Implement actual use of chat history (self.memory) when generating content
                # Example: history = self.memory.get_history() ... self.llm.generate_content(prompt, history=history)
                # TODO: Pass configured generation_config/safety_settings to generate_content if implemented in __init__
                response = self.llm.generate_content(prompt)

                # --- Security Check (Post-LLM) ---
                # Enhanced security check with sanitization option
                llm_output = response.text # Accessing the text part of the response

                # Record the raw output
                self.reliability_monitor.record_checkpoint(
                    operation_id=operation_id,
                    checkpoint_name="raw_output",
                    data={
                        "output_length": len(llm_output),
                        "output_sample": llm_output[:100] + "..." if len(llm_output) > 100 else llm_output
                    }
                )

                if not self._is_output_secure(llm_output):
                    logger.warning(f"LLM output for expert '{self.specialty}' failed post-execution security check.")

                    # Record the security failure
                    self.reliability_monitor.record_error(
                        operation_id=operation_id,
                        error_type="security_check_failure",
                        error_message="Output failed post-execution security check",
                        error_data={"stage": "post_execution"}
                    )

                    # Attempt to sanitize the output based on security profile
                    if self.security_profile in ['pii_protection', 'translator_no_pii']:
                        # For PII-focused profiles, try sanitization instead of rejection
                        sanitized_output = self._sanitize_output(llm_output)
                        logger.info(f"Expert '{self.specialty}' sanitized potentially insecure output.")

                        # Record the sanitization
                        self.reliability_monitor.record_checkpoint(
                            operation_id=operation_id,
                            checkpoint_name="output_sanitization",
                            data={"sanitization_applied": True}
                        )

                        llm_output = sanitized_output
                    else:
                        # For other security profiles, reject the output entirely
                        logger.warning(f"Expert '{self.specialty}' output rejected due to security concerns.")

                        # Complete the operation with failure
                        self.reliability_monitor.complete_execution(
                            operation_id=operation_id,
                            output="Error: Security check failed",
                            metadata={"success": False}
                        )

                        return f"Error: Expert '{self.specialty}' generated an insecure response that could not be safely processed."

                # If successful, break the loop
                logger.info(f"Expert '{self.specialty}' successfully executed operation on attempt {attempts}.") # Use logger
                break # Exit the while loop on success

            except Exception as e:
                # Basic error logging implemented
                logger.error(f"Attempt {attempts}: Error during LLM interaction for expert '{self.specialty}': {e}", exc_info=(attempts > max_retries))

                # Record the error
                self.reliability_monitor.record_error(
                    operation_id=operation_id,
                    error_type="llm_interaction_error",
                    error_message=str(e),
                    error_data={"attempt": attempts}
                )

                if attempts > max_retries:
                    # If all retries failed, return an error
                    # Complete the operation with failure
                    self.reliability_monitor.complete_execution(
                        operation_id=operation_id,
                        output=f"Error: LLM interaction failed after {attempts} attempts",
                        metadata={"success": False}
                    )

                    return f"Error: Expert '{self.specialty}' failed to execute operation after {attempts} attempts due to LLM error: {e}"
                # Optional: Add delay before retry
                # import time
                # time.sleep(1)                # Continue to the next iteration (retry)
        
        # Complete the operation with success
        if llm_output is not None:
            # Complete the reliability monitoring
            self.reliability_monitor.complete_execution(
                operation_id=operation_id,
                output=llm_output[:100] + "..." if len(llm_output) > 100 else llm_output,
                metadata={"success": True, "attempts": attempts}
            )
            
            # AUTOMATIC MEMORY STORAGE - Store task and result without user intervention
            if self.memory_enabled and self.memory_manager:
                try:
                    from .memory.models import MemoryType
                    
                    # Determine memory type based on memory_duration setting
                    if self.memory_duration == "short_term":
                        auto_memory_type = MemoryType.SESSION
                    elif self.memory_duration == "long_term":
                        auto_memory_type = MemoryType.LONG_TERM
                    else:  # auto or default
                        auto_memory_type = MemoryType.WORKING
                    
                    # Store the task description as context (as vector embeddings in Chroma)
                    task_memory = f"Task: {task_description}"
                    if context:
                        task_memory += f" (Context: {context[:100]}...)" if len(context) > 100 else f" (Context: {context})"
                    
                    self.memory_manager.sync_store(
                        user_id=self.user_id,
                        content=task_memory,
                        memory_type=auto_memory_type,
                        tags=["task", "input", "auto_stored"]
                    )
                    
                    # Store the result/output (as vector embeddings in Chroma)
                    result_memory = f"Result: {llm_output}"
                    self.memory_manager.sync_store(
                        user_id=self.user_id,
                        content=result_memory,
                        memory_type=auto_memory_type, 
                        tags=["result", "output", "auto_stored"]
                    )
                    
                    logger.debug(f"Auto-stored task and result as {auto_memory_type} embeddings for expert '{self.specialty}'")
                    
                except Exception as e:
                    logger.warning(f"Failed to auto-store memories for expert '{self.specialty}': {e}")
                    # Don't fail the whole operation if memory storage fails

            return llm_output
        else:
            # This path indicates an issue with the loop logic or unexpected state
            logger.error(f"Expert '{self.specialty}' finished execution loop unexpectedly without success or final error.")

            # Complete the operation with failure
            self.reliability_monitor.complete_execution(
                operation_id=operation_id,
                output="Error: Unexpected execution failure",
                metadata={"success": False}
            )

            return f"Error: Expert '{self.specialty}' failed operation execution unexpectedly."


    # --- Placeholder Security Methods ---
    # These need significant implementation based on specific security requirements.

    @cache_security_validation
    def _is_prompt_secure(self, prompt: str) -> bool:
        """
        Enhanced security checks on prompts before they are sent to the LLM.
        Uses the PromptDefender component for comprehensive prompt injection detection.
        Security checks are applied based on the expert's security profile.
        Results are cached for improved performance.

        Args:
            prompt (str): The prompt to be checked

        Returns:
            bool: True if the prompt passes all security checks, False otherwise
        """
        logger.debug(f"Performing prompt security check for Expert '{self.specialty}', Profile '{self.security_profile}'")

        # For minimal security profile, just allow everything - NO LENGTH CHECKS AT ALL
        if self.security_profile == "minimal":
            logger.debug(f"Minimal security profile - allowing prompt of length {len(prompt)}")
            return True

        # Basic length check - allow very large prompts for modern AI applications
        if len(prompt) > 500000:  # Very generous limit for modern AI applications
            logger.warning(f"Prompt security check FAILED: Prompt exceeds maximum length ({len(prompt)} > 500000)")
            return False

        # For standard security profile, allow educational content
        if self.security_profile == "standard":
            # Only check for obvious attacks, allow educational content
            critical_pattern = r"(rm\s+-rf\s+/|system\s*\(\s*['\"].*rm\s+-rf|SELECT\s+\*\s+FROM\s+\w+\s+WHERE\s+['\"]?1['\"]?\s*=\s*['\"]?1['\"]?)"
            if get_cached_regex(critical_pattern).search(prompt):
                logger.warning(f"⚠️ SECURITY WARNING: Attack pattern detected in prompt")
                return False
            return True

        # Use HYBRID VALIDATION ONLY - but skip for minimal security profile
        if hasattr(self, 'hybrid_validator') and self.hybrid_validator and self.security_profile != "minimal":
            try:
                # Use our new hybrid security validation with correct method
                context = {"security_level": self.security_profile}
                result = self.hybrid_validator.validate(prompt, context)

                if not result['is_secure']:
                    logger.warning(f"⚠️ HYBRID SECURITY: Prompt blocked by {result.get('method', 'unknown')} - {result.get('reason', 'security violation')}")
                    return False

                logger.debug(f"✅ HYBRID SECURITY: Prompt validated by {result.get('method', 'hybrid')} - {result.get('reason', 'secure')}")
                return True

            except Exception as e:
                logger.warning(f"⚠️ HYBRID SECURITY ERROR: {e} - falling back to basic validation")
                # Continue to fallback validation below

        # Additional security profile-specific checks for HIGH and MAXIMUM profiles
        if self.security_profile in ["high", "maximum"]:
            # Check for code execution attempts in high security mode
            code_execution_patterns = [
                r"system\s*\(\s*['\"].*rm\s+-rf",
                r"exec\s*\(\s*['\"].*rm\s+-rf",
                r"eval\s*\(\s*['\"].*rm\s+-rf",
                r"subprocess.*rm\s+-rf",
            ]

            for pattern in code_execution_patterns:
                if get_cached_regex(pattern).search(prompt):
                    logger.warning(f"⚠️ SECURITY WARNING: Prompt security check FAILED: {self.security_profile} security profile detected unauthorized pattern: '{pattern}'")
                    return False

            # For MAXIMUM security, also check for PII extraction attempts
            if self.security_profile == "maximum":
                pii_patterns = [
                    r"(?:extract|collect|gather|find|identify)\s+(?:personal|private|sensitive|confidential)\s+(?:information|data|details)",
                    r"(?:email|phone|address|ssn|social security|credit card|passport|driver license|bank account)",
                    r"(?:dox|doxx|expose|reveal|unmask)\s+(?:person|individual|user|customer|client|patient)",
                ]

                for pattern in pii_patterns:
                    if get_cached_regex(pattern).search(prompt):
                        logger.warning(f"⚠️ SECURITY WARNING: Prompt security check FAILED: {self.security_profile} security profile detected unauthorized pattern: '{pattern}'")
                        return False

        # All checks passed
        logger.debug(f"Prompt security check PASSED for Expert '{self.specialty}'")
        return True

    def _detect_contextual_hijacking(self, prompt: str) -> bool:
        """
        Performs contextual analysis to detect sophisticated hijacking attempts
        that might bypass simple pattern matching.

        Args:
            prompt (str): The prompt to analyze

        Returns:
            bool: True if a contextual hijacking attempt is detected, False otherwise
        """
        # Split the prompt into sentences for analysis
        sentences = re.split(r'[.!?]\s+', prompt)

        # Check for sentence pairs that might indicate hijacking
        for i in range(len(sentences) - 1):
            current = sentences[i].lower()
            next_sentence = sentences[i + 1].lower()

            # Check for contradictory instructions pattern
            if (("instruction" in current or "guideline" in current or "rule" in current) and
                ("instead" in next_sentence or "rather" in next_sentence or "actually" in next_sentence)):
                return True

            # Check for redefinition pattern
            if (("you are" in current or "your role" in current or "your job" in current) and
                ("you are" in next_sentence or "your role" in next_sentence or "your job" in next_sentence) and
                current != next_sentence):
                return True

            # Check for negation pattern
            if ("not" in next_sentence or "don't" in next_sentence or "do not" in next_sentence) and (
                "follow" in next_sentence or "adhere" in next_sentence or "obey" in next_sentence) and (
                "instruction" in next_sentence or "guideline" in next_sentence or "rule" in next_sentence):
                return True

        # Check for structural indicators of hijacking
        sections = prompt.split("\n\n")
        if len(sections) >= 2:
            # Check if later sections contradict earlier ones
            first_section = sections[0].lower()
            for section in sections[1:]:
                section_lower = section.lower()
                if (("instruction" in first_section or "guideline" in first_section) and
                    ("ignore" in section_lower or "disregard" in section_lower or "forget" in section_lower)):
                    return True

        return False

    @cache_security_validation
    def _is_output_secure(self, output: str) -> bool:
        """
        HYBRID OUTPUT SECURITY VALIDATION - Uses our new hybrid system exclusively!
        No more old security components - pure hybrid validation only.

        Args:
            output (str): The LLM-generated output to be checked

        Returns:
            bool: True if the output passes all security checks, False otherwise
        """
        logger.debug(f"Performing HYBRID output security check for Expert '{self.specialty}', Profile '{self.security_profile}'")

        if not output:
            logger.warning("⚠️ SECURITY WARNING: Output security check FAILED: Empty output received")
            return False

        # Use HYBRID VALIDATION ONLY - no old security system
        if hasattr(self, 'hybrid_validator') and self.hybrid_validator:
            try:
                # Use our new hybrid security validation for output with correct method
                context = {"security_level": self.security_profile}
                result = self.hybrid_validator.validate(output, context)

                if not result['is_secure']:
                    logger.warning(f"⚠️ HYBRID SECURITY: Output blocked by {result.get('method', 'unknown')} - {result.get('reason', 'security violation')}")
                    return False

                logger.debug(f"✅ HYBRID SECURITY: Output validated by {result.get('method', 'hybrid')} - {result.get('reason', 'secure')}")
                return True

            except Exception as e:
                logger.warning(f"⚠️ HYBRID SECURITY ERROR: {e} - falling back to basic validation")
                # Continue to fallback validation below

        # FALLBACK: Basic validation only for extremely harmful content
        if self.security_profile == "minimal":
            # Only check for extremely harmful content
            extremely_harmful_patterns = [
                r'\b(?:bomb making|terrorist attack plan|mass shooting instructions)\b',
                r'\b(?:child exploitation|human trafficking instructions)\b',
                r'\b(?:detailed suicide method|specific self-harm technique)\b',
            ]

            for pattern in extremely_harmful_patterns:
                if get_cached_regex(pattern).search(output):
                    logger.warning(f"⚠️ SECURITY WARNING: Critical harmful content detected in output")
                    return False
            return True

        # For standard security profile, only perform basic checks
        if self.security_profile == "standard":
            # Check for obviously harmful content
            harmful_patterns = [
                r'\b(?:bomb|terrorist attack|mass shooting|genocide)\b',
                r'\b(?:child abuse|human trafficking|sex trafficking)\b',
                r'\b(?:suicide method|how to kill|self-harm)\b',
            ]

            for pattern in harmful_patterns:
                if get_cached_regex(pattern).search(output):
                    logger.warning(f"⚠️ SECURITY WARNING: Harmful content detected in output")
                    return False
            return True

        # Generate a unique operation ID for this check
        operation_id = f"output_check_{str(uuid.uuid4())[:8]}"

        # 1. Check for sensitive data using DataGuardian
        if self.security_checks.get("content_analysis", True):
            sensitivity_report = self.data_guardian.get_sensitivity_report(output)

            # Get the threshold based on security profile
            sensitive_data_threshold = self.security_thresholds.get("sensitive_data", 0.5)

            if sensitivity_report['has_sensitive_data'] and sensitivity_report.get('sensitivity_score', 0.0) > sensitive_data_threshold:
                # Log detailed information about the sensitive data
                sensitivity_score = sensitivity_report.get('sensitivity_score', 0.0)
                categories = sensitivity_report.get('categories', {})

                logger.warning(f"⚠️ SECURITY WARNING: Output security check FAILED: Sensitive data detected (score: {sensitivity_score:.2f})")

                for category, count in categories.items():
                    logger.warning(f"⚠️ SECURITY WARNING: Detected {count} instances of {category} data")

                # Log recommendations
                for i, recommendation in enumerate(sensitivity_report.get('recommendations', [])):
                    logger.info(f"Security recommendation {i+1}: {recommendation}")

                # In high or maximum security mode, block any output with sensitive data
                if self.security_profile in ["high", "maximum"]:
                    return False

        # 2. Check for harmful content
        harmful_content_patterns = [
            # Violence
            r'\b(?:bomb|explosive|terrorist|terrorism|attack plan|mass casualty|assassination)\b',
            r'\b(?:school shooting|mass shooting|genocide|ethnic cleansing|violent extremism)\b',

            # Illegal activities
            r'\b(?:child abuse|child exploitation|human trafficking|sex trafficking|slavery)\b',
            r'\b(?:drug trafficking|illegal weapons|money laundering|fraud scheme)\b',

            # Self-harm
            r'\b(?:suicide method|how to kill|self-harm technique|suicide instruction)\b',

            # Hate speech indicators
            r'\b(?:racial slur|ethnic slur|hate group|white supremacy|nazi|extremist group)\b',
        ]

        # Always check for harmful content regardless of security profile
        for pattern in harmful_content_patterns:
            if get_cached_regex(pattern).search(output):
                logger.warning(f"⚠️ SECURITY WARNING: Output security check FAILED: Detected potentially harmful content matching pattern: '{pattern}'")
                return False

        # 3. Check reliability using ReliabilityMonitor
        if self.security_checks.get("output_validation", True):
            # Start monitoring this output check
            self.reliability_monitor.monitor_execution(
                operation_id=operation_id,
                operation_type="output_security_check",
                inputs={"output_length": len(output)}
            )

            # Record a checkpoint
            self.reliability_monitor.record_checkpoint(
                operation_id=operation_id,
                checkpoint_name="initial_check",
                data={"output_sample": output[:100] + "..." if len(output) > 100 else output}
            )

            # Check for repetition and consistency issues
            words = re.findall(r'\b\w+\b', output.lower())
            sentences = re.split(r'[.!?]\s+', output)

            # Record these metrics
            self.reliability_monitor.record_checkpoint(
                operation_id=operation_id,
                checkpoint_name="content_analysis",
                data={
                    "word_count": len(words),
                    "sentence_count": len(sentences),
                    "unique_words": len(set(words))
                }
            )

            # Complete the reliability analysis
            reliability_analysis = self.reliability_monitor.complete_execution(
                operation_id=operation_id,
                output={"is_output_secure": True},
                metadata={
                    "security_profile": self.security_profile.value,
                    "expert_specialty": self.specialty
                }
            )

            # Get the threshold based on security profile
            reliability_threshold = self.security_thresholds.get("reliability_score", 0.5)

            # Check if the output is reliable
            if not reliability_analysis.get('is_reliable', True) and reliability_analysis.get('reliability_score', 1.0) < reliability_threshold:
                reliability_score = reliability_analysis.get('reliability_score', 0.0)
                issues = reliability_analysis.get('issues', [])

                logger.warning(f"⚠️ SECURITY WARNING: Output security check FAILED: Reliability issues detected (score: {reliability_score:.2f})")

                for issue in issues:
                    logger.warning(f"⚠️ SECURITY WARNING: Reliability issue: {issue}")

                # In high or maximum security mode, block unreliable output
                if self.security_profile in [SecurityProfile.HIGH, SecurityProfile.MAXIMUM]:
                    return False

        # 4. Additional security profile-specific checks
        if self.security_profile in [SecurityProfile.HIGH, SecurityProfile.CUSTOM]:
            # Check for code patterns
            code_patterns = [
                r'<script.*?>.*?</script>',
                r'javascript:',
                r'eval\(',
                r'`.*?`',  # Backticks for command execution
                r'\$\(.*?\)',  # Command substitution
                r'(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|UNION).*?(?:FROM|INTO|WHERE|TABLE|DATABASE)',
            ]

            for pattern in code_patterns:
                if get_cached_regex(pattern).search(output):
                    profile_name = self.custom_profile_name if self.security_profile == SecurityProfile.CUSTOM else self.security_profile.value
                    logger.warning(f"⚠️ SECURITY WARNING: Output security check FAILED: {profile_name} security profile detected code pattern: '{pattern}'")
                    return False

        # For MAXIMUM security and some CUSTOM profiles, perform additional checks
        if self.security_profile == SecurityProfile.MAXIMUM or (
            self.security_profile == SecurityProfile.CUSTOM and
            self.security_checks.get("format_validation", True) and
            self.security_checks.get("content_analysis", True)
        ):
            # Check for any potential code or command patterns
            extended_code_patterns = [
                r'<.*?>',  # Any HTML/XML tags
                r'function\s*\(',
                r'def\s+\w+\s*\(',
                r'class\s+\w+',
                r'import\s+\w+',
                r'require\s*\(',
                r'#include',
                r'sudo',
                r'apt',
                r'npm',
                r'pip',
                r'curl',
                r'wget',
            ]

            for pattern in extended_code_patterns:
                if get_cached_regex(pattern).search(output):
                    profile_name = self.custom_profile_name if self.security_profile == SecurityProfile.CUSTOM else self.security_profile.value
                    logger.warning(f"⚠️ SECURITY WARNING: Output security check FAILED: {profile_name} security profile detected potential code pattern: '{pattern}'")
                    return False

        # All checks passed
        logger.debug(f"Output security check PASSED for Expert '{self.specialty}'")
        return True

    def _sanitize_output(self, output: str) -> str:
        """
        Sanitizes output by redacting potential PII and sensitive information
        using the DataGuardian component.

        Args:
            output (str): The output to sanitize

        Returns:
            str: The sanitized output
        """
        # Use the DataGuardian to sanitize the output
        sanitized = self.data_guardian.sanitize_text(output)

        # Add a notice if redactions were made
        if sanitized != output:
            sanitized += "\n\n[NOTICE: This output has been automatically sanitized to remove potential sensitive information.]"

        return sanitized


    # TODO: Implement methods for tool validation, secure communication handling, etc.

    def _format_with_inputs(self, text: str, inputs: Dict[str, Any]) -> str:
        """
        Formats a string by replacing template variables with values from inputs.
        Template variables are in the format {variable_name}.

        Args:
            text (str): The text containing template variables
            inputs (Dict[str, Any]): Dictionary of input values to use for formatting

        Returns:
            str: The formatted text with template variables replaced
        """
        if not text or not inputs:
            return text

        # Create a copy of the text to avoid modifying the original
        formatted_text = text

        # Replace each template variable with its corresponding value
        for key, value in inputs.items():
            placeholder = "{" + key + "}"
            if placeholder in formatted_text:
                # Convert value to string if it's not already
                str_value = str(value) if not isinstance(value, str) else value
                formatted_text = formatted_text.replace(placeholder, str_value)

        return formatted_text

    def _initialize_visualization(self, api_key: Optional[str]):
        """
        Initialize the visualization components.

        Args:
            api_key (Optional[str]): API key for LLM recommendations
        """
        try:
            from .security_validation.visualization.enhanced_visualizer import EnhancedVisualizer

            # Create output directory
            os.makedirs(self.visualization_output_dir, exist_ok=True)

            # Initialize the visualizer
            self.visualizer = EnhancedVisualizer(
                output_dir=self.visualization_output_dir,
                auto_save=self.auto_generate_reports,
                use_llm_recommendations=self.use_llm_recommendations,
                llm_api_key=api_key if self.use_llm_recommendations else None
            )

            logger.info(f"Expert '{self.specialty}' visualization initialized with output directory: {self.visualization_output_dir}")

        except Exception as e:
            logger.warning(f"Failed to initialize visualization for expert '{self.specialty}': {e}")
            self.visualizer = None
            self.enable_visualization = False

    def generate_security_report(self, task_description: str, result: str, security_result: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Generate a security validation report for a task execution.

        Args:
            task_description (str): The task that was executed
            result (str): The result from the task execution
            security_result (Optional[Dict[str, Any]]): Security validation result

        Returns:
            Optional[str]: Path to the generated report, or None if visualization is disabled
        """
        if not self.enable_visualization or not self.visualizer:
            return None

        try:
            # Create a mock security result if none provided
            if security_result is None:
                security_result = {
                    'is_secure': True,
                    'method': 'expert_validation',
                    'reason': 'Expert task execution completed successfully',
                    'threats': [],
                    'validation_performance': {
                        'total_time_ms': 0.0,
                        'regex_time_ms': 0.0,
                        'ml_time_ms': 0.0,
                        'llm_time_ms': 0.0,
                        'methods_used': ['expert_validation']
                    }
                }

            # Generate the report
            report_path = self.visualizer.save_report(
                security_result,
                self.security_profile_str,
                task_description,
                "html"
            )            # Auto-open if enabled
            if self.auto_open_reports and report_path:
                try:
                    import webbrowser
                    webbrowser.open(f"file://{os.path.abspath(report_path)}")
                except Exception as e:
                    logger.warning(f"Could not auto-open report: {e}")
            
            return report_path

        except Exception as e:
            logger.warning(f"Failed to generate security report for expert '{self.specialty}': {e}")
            return None

    def _initialize_hybrid_validation(self, api_key: Optional[str]):
        """
        Initialize hybrid security validation by default.

        Args:
            api_key (Optional[str]): API key for LLM validation
        """
        try:
            from .security_validation import HybridValidator

            # Initialize the hybrid validator (lean and mean)
            self.hybrid_validator = HybridValidator(
                api_key=api_key
            )

            # Hybrid validator is now integrated directly into _is_prompt_secure and _is_output_secure
            # No need to override methods - they already use hybrid validation

            logger.info(f"Expert '{self.specialty}' hybrid security validation initialized")

        except Exception as e:
            logger.warning(f"Failed to initialize hybrid validation for expert '{self.specialty}': {e}")
            logger.info(f"Expert '{self.specialty}' will use standard security validation")
            self.hybrid_validator = None

    def _hybrid_prompt_validation(self, prompt: str) -> bool:
        """
        Hybrid prompt validation using multiple methods.

        Args:
            prompt (str): The prompt to validate

        Returns:
            bool: True if secure, False otherwise
        """
        if self.hybrid_validator:
            try:
                result = self.hybrid_validator.validate(prompt)
                return result.get('is_secure', True)
            except Exception as e:
                logger.warning(f"Hybrid prompt validation failed, falling back to standard: {e}")
                return self._original_is_prompt_secure(prompt)
        else:
            return self._original_is_prompt_secure(prompt)

    def _hybrid_output_validation(self, output: str) -> bool:
        """
        Hybrid output validation using multiple methods.

        Args:
            output (str): The output to validate

        Returns:
            bool: True if secure, False otherwise
        """
        if self.hybrid_validator:
            try:
                result = self.hybrid_validator.validate(output)
                return result.get('is_secure', True)
            except Exception as e:
                logger.warning(f"Hybrid output validation failed, falling back to standard: {e}")
                return self._original_is_output_secure(output)
        else:
            return self._original_is_output_secure(output)

    def _validate_memory_duration(self, memory_duration: str) -> str:
        """
        Validate and normalize memory duration parameter.
        
        Args:
            memory_duration: Memory duration option
            
        Returns:
            Validated memory duration string
        """        # Define valid options and aliases
        valid_options = ["short_term", "long_term", "auto", "disabled"]
        aliases = {
            "session": "short_term",
            "temporary": "short_term", 
            "temp": "short_term",
            "persistent": "long_term",
            "permanent": "long_term",
            "extended": "long_term",  # Added for validation
            "automatic": "auto",
            "smart": "auto",
            "adaptive": "auto",
            "default": "auto",  # Added for validation
            "disable": "disabled",
            "none": "disabled",
            "off": "disabled",
            "false": "disabled"  # Added for validation
        }
        
        # Handle invalid types gracefully
        if not isinstance(memory_duration, str):
            logger.error(f"Invalid memory_duration type '{type(memory_duration)}'. Defaulting to 'auto'.")
            return "auto"

        # Convert to lowercase for case-insensitive comparison
        duration = memory_duration.lower().strip() if memory_duration else "auto"

        # Check if it's a valid option
        if duration in valid_options:
            return duration

        # Check if it's an alias
        if duration in aliases:
            return aliases[duration]
            
        # Invalid option - log warning and default to auto
        logger.error(f"Invalid memory_duration '{memory_duration}'. Defaulting to 'auto'. Valid options: {valid_options} and aliases: {list(aliases.keys())}")
        return "auto"

    def _create_memory_config_with_duration(self, memory_duration: str) -> Dict[str, Any]:
        """
        Create memory configuration based on memory duration.
        
        Args:
            memory_duration: Validated memory duration option
            
        Returns:
            Configuration dictionary for memory system
        """
        from .memory.models import MemoryType
        
        configs = {
            "short_term": {
                "storage": {
                    "backend": "memory",
                    "sqlite_path": None
                },
                "memory_type_default": "SESSION",  # Updated to match expected value
                "limits": {
                    "max_entries_per_user": 200,
                    "max_entry_size_bytes": 10000
                },
                "security": {
                    "enable_encryption": False
                },
                "performance": {
                    "cache_size": 50
                }
            },            "long_term": {
                "storage": {
                    "backend": "chroma",
                    "chroma_collection": f"memory_{getattr(self, 'user_id', 'default')}_longterm",
                    "chroma_persist_directory": f"./chroma_db_{getattr(self, 'user_id', 'default')}"
                },
                "memory_type_default": "LONG_TERM",  # Updated to match expected value
                "limits": {
                    "max_entries_per_user": 2000,
                    "max_entry_size_bytes": 10000
                },
                "security": {
                    "enable_encryption": True
                },
                "performance": {
                    "cache_size": 100
                }
            },
            "auto": {
                "storage": {
                    "backend": "chroma",
                    "chroma_collection": f"memory_{getattr(self, 'user_id', 'default')}_auto",
                    "chroma_persist_directory": f"./chroma_db_{getattr(self, 'user_id', 'default')}"
                },
                "memory_type_default": "WORKING",  # Updated to match expected value
                "limits": {
                    "max_entries_per_user": 1000,
                    "max_entry_size_bytes": 10000
                },
                "security": {
                    "enable_encryption": True
                },
                "performance": {
                    "cache_size": 75
                }
            },
            "disabled": {
                "storage": {
                    "backend": None,
                    "sqlite_path": None
                },
                "memory_type_default": None,
                "limits": {
                    "max_entries_per_user": 0,
                    "max_entry_size_bytes": 0
                },
                "security": {
                    "enable_encryption": False
                },
                "performance": {
                    "cache_size": 0
                }
            }
        }
        
        config = configs.get(memory_duration, configs["auto"])
        
        # Ensure memory_type_default matches expected values
        if memory_duration == "short_term":
            config["memory_type_default"] = "SESSION"
        elif memory_duration == "long_term":
            config["memory_type_default"] = "LONG_TERM"
        elif memory_duration == "auto":
            config["memory_type_default"] = "WORKING"

        # Add common configuration elements if memory is enabled
        if memory_duration != "disabled":
            config.update({
                "user_id": getattr(self, 'user_id', 'default_user'),
                "security_profile": getattr(self, 'security_profile', 'standard'),
                "enable_search": True
            })
        
        return config

    def remember(self, content: str, memory_type: Optional[str] = None, priority: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store information in expert's memory.
        
        Args:
            content: The content to remember
            memory_type: Type of memory (MemoryType or string)
            priority: Memory priority (MemoryPriority or string)
            metadata: Additional metadata for the memory
            
        Returns:
            Memory ID if successful, error message if failed
        """
        if not self.memory_enabled or not self.memory_manager:
            return "memory_disabled"
        
        try:
            from .memory.models import MemoryType, MemoryPriority
            
            # Handle memory_type parameter
            if memory_type is None:
                mem_type = MemoryType.WORKING
            elif isinstance(memory_type, str):
                # Convert string to MemoryType enum
                try:
                    mem_type = getattr(MemoryType, memory_type.upper())
                except AttributeError:
                    mem_type = MemoryType.WORKING
            else:
                mem_type = memory_type
            
            # Handle priority parameter
            if priority is None:
                mem_priority = MemoryPriority.NORMAL
            elif isinstance(priority, str):
                # Convert string to MemoryPriority enum
                try:
                    mem_priority = getattr(MemoryPriority, priority.upper())
                except AttributeError:
                    mem_priority = MemoryPriority.NORMAL
            else:
                mem_priority = priority
              # Store the memory
            memory_id = self.memory_manager.sync_store(
                user_id=self.user_id,
                content=content,
                memory_type=mem_type,
                priority=mem_priority,
                tags=list(metadata.keys()) if metadata else None
            )
            
            return str(memory_id) if memory_id else "error_storing_memory"
            
        except Exception as e:
            logger.error(f"Error in remember method: {e}")
            return f"error_{str(e)[:50]}"
    
    def recall(self, query: str, limit: int = 10, memory_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve memories based on a query.
        
        Args:
            query: Search query for memories
            limit: Maximum number of memories to return
            memory_type: Filter by memory type (optional)
            
        Returns:
            List of memory dictionaries
        """
        if not self.memory_enabled or not self.memory_manager:
            return []
        
        try:
            from .memory.models import MemoryType
            
            # Handle memory_type filter
            mem_type_filter = None
            if memory_type:
                if isinstance(memory_type, str):
                    try:
                        mem_type_filter = getattr(MemoryType, memory_type.upper())
                    except AttributeError:
                        mem_type_filter = None
                else:
                    mem_type_filter = memory_type
              # Search memories
            memories = self.memory_manager.sync_retrieve(
                user_id=self.user_id,
                query=query,
                memory_types=[mem_type_filter] if mem_type_filter else None,
                limit=limit
            )
            
            # Convert memory objects to dictionaries
            result = []
            for memory in memories:
                memory_dict = {
                    'id': getattr(memory, 'id', 'unknown'),
                    'content': getattr(memory, 'content', ''),
                    'memory_type': getattr(memory, 'memory_type', None),
                    'priority': getattr(memory, 'priority', None),
                    'metadata': getattr(memory, 'metadata', {}),
                    'created_at': getattr(memory, 'created_at', None),
                    'tags': getattr(memory, 'tags', [])
                }
                result.append(memory_dict)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in recall method: {e}")
            return []
