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
        llm_model_name (str): The specific Gemini model to use (e.g., 'gemini-pro'). Defaults to 'gemini-pro'.
        tools (List[Any], optional): A list of tools available to the expert.
        security_profile (str, optional): Defines the security constraints and capabilities. Defaults to 'default'.
        # Add other relevant attributes like memory, max_iterations, etc.
    """
    def __init__(self,
                 specialty: str,
                 objective: str,
                 background: Optional[str] = None,
                 llm_model_name: str = 'gemini-2.0-flash-lite', # Updated default model name per user request
                 tools: Optional[List[Any]] = None,
                 security_profile: str = 'standard',
                 api_key: Optional[str] = None): # Add api_key parameter
        self.specialty = specialty
        self.objective = objective
        self.background = background
        self.llm_model_name = llm_model_name
        self.tools = tools or []
        self.security_profile_str = security_profile
        self.llm: Optional[genai.GenerativeModel] = None

        # Convert string security profile to enum
        # Map legacy profile names to new system
        if security_profile in ["default", "standard"]:
            self.security_profile = SecurityProfile.STANDARD
            self.custom_profile_name = None
        elif security_profile in ["minimal", "development", "testing"]:
            self.security_profile = SecurityProfile.MINIMAL
            self.custom_profile_name = None
        elif security_profile in ["low", "basic"]:
            self.security_profile = SecurityProfile.LOW
            self.custom_profile_name = None
        elif security_profile in ["high", "high_security", "code_restricted"]:
            self.security_profile = SecurityProfile.HIGH
            self.custom_profile_name = None
        elif security_profile in ["maximum", "maximum_security", "air_gapped"]:
            self.security_profile = SecurityProfile.MAXIMUM
            self.custom_profile_name = None
        else:
            # Check if it's a registered custom profile
            self.security_profile = SecurityProfile.from_string(security_profile)
            if self.security_profile == SecurityProfile.CUSTOM:
                self.custom_profile_name = security_profile
                logger.info(f"Using custom security profile: {security_profile}")
            else:
                self.custom_profile_name = None

        # Log information about the security profile
        log_security_profile_info(self.security_profile, self.custom_profile_name)

        # Get security level string for backward compatibility
        security_level = self.security_profile.value if self.security_profile != SecurityProfile.CUSTOM else "custom"

        # Get security thresholds and checks
        self.security_thresholds = get_security_thresholds(self.security_profile, self.custom_profile_name)
        self.security_checks = get_security_checks(self.security_profile, self.custom_profile_name)

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
                # time.sleep(1)
                # Continue to the next iteration (retry)

        # Complete the operation with success
        if llm_output is not None:
            # Complete the reliability monitoring
            self.reliability_monitor.complete_execution(
                operation_id=operation_id,
                output=llm_output[:100] + "..." if len(llm_output) > 100 else llm_output,
                metadata={"success": True, "attempts": attempts}
            )

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
        logger.debug(f"Performing prompt security check for Expert '{self.specialty}', Profile '{self.security_profile.value}'")

        # Skip most checks for minimal security profile
        if self.security_profile == SecurityProfile.MINIMAL:
            # Only check for critical exploits that could harm the system
            critical_pattern = r"(rm\s+-rf|format\s+[a-z]:|\bdd\s+if|mkfs|system\s*\(|exec\s*\()"
            if get_cached_regex(critical_pattern).search(prompt):
                logger.warning(f"⚠️ SECURITY WARNING: Critical exploit detected in prompt despite minimal security profile")
                return False
            return True

        # For low security profile, only perform basic checks
        if self.security_profile == SecurityProfile.LOW:
            # Check for obvious injection attempts
            injection_pattern = r"(ignore previous|forget instructions|disregard|you are now|new role|system prompt)"
            if get_cached_regex(injection_pattern).search(prompt):
                # For low security, warn but don't block
                logger.warning(f"⚠️ SECURITY WARNING: Potential prompt injection detected but allowed due to LOW security profile")
            return True

        # For standard and higher security profiles, use the PromptDefender
        analysis = self.prompt_defender.analyze_prompt(prompt)

        # Get the threshold based on security profile
        injection_threshold = self.security_thresholds.get("injection_score", 0.6)

        if not analysis['is_safe'] and analysis.get('threat_level', 0.0) > injection_threshold:
            # Log detailed information about the security issue
            detection_method = analysis.get('detection_method', 'unknown')
            threat_level = analysis.get('threat_level', 0.0)
            matched_pattern = analysis.get('matched_pattern', 'unknown pattern')

            logger.warning(f"⚠️ SECURITY WARNING: Prompt security check FAILED: {detection_method} detected (threat level: {threat_level:.2f})")

            if matched_pattern:
                logger.warning(f"⚠️ SECURITY WARNING: Matched pattern: '{matched_pattern}'")

            # Log recommendations
            recommendations = self.prompt_defender.get_recommendations(analysis)
            for i, recommendation in enumerate(recommendations):
                logger.info(f"Security recommendation {i+1}: {recommendation}")

            return False

        # Additional security profile-specific checks for HIGH, MAXIMUM, and CUSTOM profiles
        if self.security_profile in [SecurityProfile.HIGH, SecurityProfile.MAXIMUM, SecurityProfile.CUSTOM]:
            # Check for code execution attempts in high security mode
            code_execution_patterns = [
                r"execute code",
                r"run command",
                r"system\s*\(",
                r"exec\s*\(",
                r"eval\s*\(",
                r"os\.",
                r"subprocess",
                r"shell",
                r"bash",
                r"powershell",
                r"cmd",
                r"terminal",
            ]

            for pattern in code_execution_patterns:
                if get_cached_regex(pattern).search(prompt):
                    logger.warning(f"⚠️ SECURITY WARNING: Prompt security check FAILED: {self.security_profile.value} security profile detected unauthorized pattern: '{pattern}'")
                    return False

            # For MAXIMUM security and some CUSTOM profiles, also check for PII extraction attempts
            if self.security_profile == SecurityProfile.MAXIMUM or (
                self.security_profile == SecurityProfile.CUSTOM and
                self.security_checks.get("content_analysis", True)
            ):
                pii_patterns = [
                    r"(?:extract|collect|gather|find|identify)\s+(?:personal|private|sensitive|confidential)\s+(?:information|data|details)",
                    r"(?:email|phone|address|ssn|social security|credit card|passport|driver license|bank account)",
                    r"(?:dox|doxx|expose|reveal|unmask)\s+(?:person|individual|user|customer|client|patient)",
                ]

                for pattern in pii_patterns:
                    if get_cached_regex(pattern).search(prompt):
                        profile_name = self.custom_profile_name if self.security_profile == SecurityProfile.CUSTOM else self.security_profile.value
                        logger.warning(f"⚠️ SECURITY WARNING: Prompt security check FAILED: {profile_name} security profile detected unauthorized pattern: '{pattern}'")
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
        Enhanced security checks on LLM outputs before they are returned.
        Uses the DataGuardian and ReliabilityMonitor components for comprehensive security checks.
        Security checks are applied based on the expert's security profile.
        Results are cached for improved performance.

        Args:
            output (str): The LLM-generated output to be checked

        Returns:
            bool: True if the output passes all security checks, False otherwise
        """
        logger.debug(f"Performing output security check for Expert '{self.specialty}', Profile '{self.security_profile.value}'")

        if not output:
            logger.warning("⚠️ SECURITY WARNING: Output security check FAILED: Empty output received")
            return False

        # Skip most checks for minimal security profile
        if self.security_profile == SecurityProfile.MINIMAL:
            # Only check for extremely harmful content
            extremely_harmful_patterns = [
                r'\b(?:bomb making|terrorist attack plan|mass shooting instructions)\b',
                r'\b(?:child exploitation|human trafficking instructions)\b',
                r'\b(?:detailed suicide method|specific self-harm technique)\b',
            ]

            for pattern in extremely_harmful_patterns:
                if get_cached_regex(pattern).search(output):
                    logger.warning(f"⚠️ SECURITY WARNING: Critical harmful content detected in output despite minimal security profile")
                    return False
            return True

        # For low security profile, only perform basic checks
        if self.security_profile == SecurityProfile.LOW:
            # Check for obviously harmful content
            harmful_patterns = [
                r'\b(?:bomb|terrorist attack|mass shooting|genocide)\b',
                r'\b(?:child abuse|human trafficking|sex trafficking)\b',
                r'\b(?:suicide method|how to kill|self-harm)\b',
            ]

            for pattern in harmful_patterns:
                if get_cached_regex(pattern).search(output):
                    logger.warning(f"⚠️ SECURITY WARNING: Harmful content detected in output: '{pattern}'")
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
                if self.security_profile in [SecurityProfile.HIGH, SecurityProfile.MAXIMUM]:
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
