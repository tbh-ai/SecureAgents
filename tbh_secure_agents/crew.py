# tbh_secure_agents/crew.py
# Author: Saish (TBH.AI)

"""
Defines the Squad class for the TBH Secure Agents framework.
A Squad manages a collection of experts and orchestrates the execution of operations.
"""

import logging
import time
import re
import json
import hashlib
import uuid
import random
import os
from typing import List, Optional, Dict, Any, Tuple, Set
from collections import Counter
from .agent import Expert
from .task import Operation
from .terminal_ui import terminal
from .security_profiles import (
    SecurityProfile, get_security_thresholds, get_security_checks,
    log_security_profile_info, get_cached_regex, cache_security_validation
)

# Get a logger for this module
logger = logging.getLogger(__name__)

# Define custom exceptions
class SecurityError(Exception):
    """Exception raised for security-related issues in the Squad."""
    pass

class Squad:
    """
    Manages a group of experts and orchestrates the execution of a sequence of operations.

    Attributes:
        experts (List[Expert]): A list of Expert objects part of this squad.
        operations (List[Operation]): A list of Operation objects to be executed by the squad.
        process (str): The execution process ('sequential', 'hierarchical', etc.). Defaults to 'sequential'.
        # Add attributes like memory, security_manager, etc.
    """
    def __init__(self, experts: List[Expert], operations: List[Operation], process: str = 'sequential',
                 security_level: str = 'standard', trust_verification: bool = False,
                 result_destination: Optional[Dict[str, str]] = None, **kwargs):
        self.experts = experts
        self.operations = operations
        self.process = process # Example: 'sequential', 'hierarchical'
        self.security_level_str = security_level  # Store original string value
        self.trust_verification = trust_verification  # Whether to verify trust between experts
        self.result_destination = result_destination  # Where to save the final result

        # Store additional configuration options
        self.config = kwargs

        # Convert string security level to enum
        # Map legacy security levels to new system
        if security_level in ["default", "standard"]:
            self.security_profile = SecurityProfile.STANDARD
            self.custom_profile_name = None
        elif security_level in ["minimal", "development", "testing"]:
            self.security_profile = SecurityProfile.MINIMAL
            self.custom_profile_name = None
        elif security_level in ["low", "basic"]:
            self.security_profile = SecurityProfile.LOW
            self.custom_profile_name = None
        elif security_level in ["high", "high_security"]:
            self.security_profile = SecurityProfile.HIGH
            self.custom_profile_name = None
        elif security_level in ["maximum", "maximum_security"]:
            self.security_profile = SecurityProfile.MAXIMUM
            self.custom_profile_name = None
        else:
            # Check if it's a registered custom profile
            self.security_profile = SecurityProfile.from_string(security_level)
            if self.security_profile == SecurityProfile.CUSTOM:
                self.custom_profile_name = security_level
                logger.info(f"Using custom security profile: {security_level}")
            else:
                self.custom_profile_name = None

        # Log information about the security profile
        log_security_profile_info(self.security_profile, self.custom_profile_name)

        # Get security thresholds and checks
        self.security_thresholds = get_security_thresholds(self.security_profile, self.custom_profile_name)
        self.security_checks = get_security_checks(self.security_profile, self.custom_profile_name)

        # For backward compatibility
        self.security_level = self.security_profile.value if self.security_profile != SecurityProfile.CUSTOM else "custom"

        # Initialize security context for the squad
        self.security_context = {
            'squad_id': str(uuid.uuid4()),  # Unique identifier for this squad
            'creation_time': time.time(),
            'security_level': self.security_level,
            'security_profile': self.security_profile.value,
            'custom_profile_name': self.custom_profile_name,  # Store custom profile name if used
            'expert_trust_levels': {},  # Will store trust levels between experts
            'operation_security_scores': {},  # Will store security scores for operations
            'execution_metrics': {},  # Will store execution metrics
            'security_incidents': [],  # Will store security incidents
        }

        # NEW: Initialize expert trust levels
        self._initialize_expert_trust_levels()

        if not experts:
            raise ValueError("Squad must have at least one expert.")
        if not operations:
            logger.error("Squad initialization failed: Must have at least one operation.") # Use logger
            raise ValueError("Squad must have at least one operation.")

        # NEW: Validate expert compatibility
        self._validate_expert_compatibility()

        logger.info(f"Squad initialized with {len(self.experts)} experts and {len(self.operations)} operations. "
                   f"Process: {self.process}, Security Level: {self.security_level}") # Use logger

    def deploy(self, guardrails: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Starts the execution of the operations by the experts in the squad.
        Includes security checks and orchestration controls to prevent exploitation.

        Args:
            guardrails (Optional[Dict[str, Any]]): Dynamic inputs that can be used as guardrails
                                                  during operation execution. These values can be
                                                  referenced in prompts and used for context.

        Returns:
            Optional[str]: The final output of the squad's execution, or None if there's no final output or an error occurred.
        """
        # Display squad deployment header
        terminal.print_header("TBH SECURE AGENTS - SQUAD DEPLOYMENT")

        # Display squad information
        terminal.print_squad_info(
            expert_count=len(self.experts),
            operation_count=len(self.operations),
            process=self.process,
            security_level=self.security_level
        )

        logger.info("Squad deployment initiated...")

        # Initialize guardrails if provided
        if guardrails is None:
            guardrails = {}
        else:
            # Display guardrails information
            terminal.print_guardrails_info(guardrails)

        # Start spinner for guardrail validation
        terminal.start_spinner("Validating guardrails for security")

        # Validate guardrails for security
        sanitized_guardrails = self._sanitize_guardrails(guardrails)

        # Store sanitized guardrails in security context for reference
        self.security_context['guardrails'] = sanitized_guardrails

        if sanitized_guardrails:
            logger.info(f"Squad deployment with guardrails: {list(sanitized_guardrails.keys())}")
            terminal.stop_spinner(True, f"Guardrails validated: {len(sanitized_guardrails)} parameters")
        else:
            terminal.stop_spinner(True, "No guardrails provided")

        # Security check: Validate squad configuration before execution
        terminal.start_spinner("Validating squad security configuration")
        if not self._validate_squad_security():
            logger.error("⚠️ SECURITY WARNING: Squad deployment aborted: Security validation failed")
            terminal.stop_spinner(False, "Squad security validation failed")
            terminal.print_error("Squad deployment aborted: Security validation failed")
            return "Error: Squad security validation failed. Deployment aborted."
        terminal.stop_spinner(True, "Squad security validation passed")

        # Initialize execution tracking
        final_output: Optional[str] = None
        # Store outputs to potentially pass as context to next operations
        # Key: Operation instructions (or a unique operation ID), Value: Operation result
        operation_outputs: Dict[str, str] = {}

        # Track execution metrics for security monitoring
        self.execution_metrics = {
            'start_time': time.time(),
            'operations_completed': 0,
            'operations_failed': 0,
            'total_operations': len(self.operations),
            'execution_path': []
        }

        # Display operations subheader
        terminal.print_subheader("OPERATIONS EXECUTION")

        for i, operation in enumerate(self.operations):
            # Record operation in execution path for auditing
            operation_record = {
                'index': i,
                'instructions': operation.instructions[:100] + ('...' if len(operation.instructions) > 100 else ''),
                'start_time': time.time(),
                'status': 'pending'
            }
            self.execution_metrics['execution_path'].append(operation_record)

            # Display operation information
            if operation.expert:
                terminal.print_operation_info(
                    instructions=operation.instructions,
                    expert_specialty=operation.expert.specialty
                )
            else:
                terminal.print_operation_info(
                    instructions=operation.instructions,
                    expert_specialty="Unassigned"
                )

            # Security check: Validate operation before assignment
            terminal.start_spinner(f"Validating operation {i+1}/{len(self.operations)}")
            logger.debug(f"Validating operation {i+1}/{len(self.operations)}: '{operation.instructions[:30]}...'")
            if not self._validate_operation_security(operation, i):
                logger.error(f"⚠️ SECURITY WARNING: Operation validation failed for operation {i+1}: '{operation.instructions[:30]}...'")
                terminal.stop_spinner(False, f"Operation {i+1} validation failed")
                operation_record['status'] = 'validation_failed'
                self.execution_metrics['operations_failed'] += 1
                if self.process == 'sequential':
                    terminal.print_error(f"Squad execution failed: Security validation failed for operation {i+1}")
                    return f"Squad execution failed: Security validation failed for operation {i+1}"
                else:
                    continue  # Skip this operation but continue with others for non-sequential processes
            terminal.stop_spinner(True, f"Operation {i+1} validation passed")

            # Assign expert if not already assigned
            if not operation.expert:
                terminal.start_spinner("Finding best expert for operation")
                # Implement more sophisticated expert assignment logic based on specialty matching
                best_expert = self._find_best_expert_for_operation(operation)
                if best_expert:
                    operation.expert = best_expert
                    logger.info(f"Assigning Operation '{operation.instructions[:30]}...' to Expert '{best_expert.specialty}'")
                    terminal.stop_spinner(True, f"Assigned to Expert: {best_expert.specialty}")
                    # Update the displayed operation info with the assigned expert
                    terminal.print_operation_info(
                        instructions=operation.instructions,
                        expert_specialty=best_expert.specialty
                    )
                else:
                    # Fallback to simple assignment if no good match
                    assigned_expert = self.experts[i % len(self.experts)]
                    operation.expert = assigned_expert
                    logger.info(f"Assigning Operation '{operation.instructions[:30]}...' to Expert '{assigned_expert.specialty}' (default assignment)")
                    terminal.stop_spinner(True, f"Assigned to Expert: {assigned_expert.specialty} (default)")
                    # Update the displayed operation info with the assigned expert
                    terminal.print_operation_info(
                        instructions=operation.instructions,
                        expert_specialty=assigned_expert.specialty
                    )
            else: # Expert was pre-assigned
                logger.info(f"Operation '{operation.instructions[:30]}...' already assigned to Expert '{operation.expert.specialty}'")

            # --- Context Passing with Security Checks ---
            if i > 0 and self.process == 'sequential':
                terminal.start_spinner("Processing context from previous operation")
                previous_operation = self.operations[i-1]
                if previous_operation.result:
                    # Check if previous result is safe to pass as context
                    if self._is_safe_for_context_passing(previous_operation.result, operation):
                        # Securely format and append previous result to current context
                        new_context = f"Output from previous operation ({previous_operation.instructions[:30]}...): {previous_operation.result}"
                        if operation.context:
                            operation.context += f"\n\n{new_context}"
                        else:
                            operation.context = new_context
                        logger.debug(f"Injecting context from previous operation into Operation '{operation.instructions[:30]}...'")
                        terminal.stop_spinner(True, "Context from previous operation added")
                    else:
                        logger.warning(f"⚠️ SECURITY WARNING: Context passing blocked: Previous result deemed unsafe for operation '{operation.instructions[:30]}...'")
                        terminal.stop_spinner(False, "Context passing blocked: Security check failed")
                else:
                    terminal.stop_spinner(True, "No context from previous operation")

            # Set operation timeout for safety
            operation_timeout = self._calculate_operation_timeout(operation)
            operation_start_time = time.time()

            try:
                # Execute the operation with timeout monitoring
                terminal.start_spinner(f"Executing operation {i+1}/{len(self.operations)}")
                logger.info(f"Executing operation {i+1}/{len(self.operations)}: '{operation.instructions[:30]}...'")

                # Execute the operation with guardrails if available
                output = operation.execute(guardrails=sanitized_guardrails if 'guardrails' in locals() else {})

                # Check execution time
                execution_time = time.time() - operation_start_time
                if execution_time > operation_timeout:
                    logger.warning(f"⚠️ SECURITY WARNING: Operation took longer than expected: {execution_time:.2f}s > {operation_timeout:.2f}s")
                    terminal.print_security_warning(f"Operation took longer than expected: {execution_time:.2f}s > {operation_timeout:.2f}s")

                # Update operation record
                operation_record['end_time'] = time.time()
                operation_record['execution_time'] = operation_record['end_time'] - operation_record['start_time']

                if output: # Store output only if execution was successful
                    # Perform additional security check on output
                    terminal.start_spinner("Validating operation output")
                    if self._is_output_safe(output, operation):
                        operation_outputs[operation.instructions] = output
                        final_output = output # Keep track of the last output as the final one (for sequential)
                        operation_record['status'] = 'completed'
                        self.execution_metrics['operations_completed'] += 1
                        logger.info(f"Operation {i+1} completed successfully in {operation_record['execution_time']:.2f}s")
                        terminal.stop_spinner(True, f"Operation {i+1} completed successfully in {operation_record['execution_time']:.2f}s")
                    else:
                        operation_record['status'] = 'unsafe_output'
                        self.execution_metrics['operations_failed'] += 1
                        logger.error(f"⚠️ SECURITY WARNING: Operation {i+1} produced unsafe output")
                        terminal.stop_spinner(False, f"Operation {i+1} produced unsafe output")
                        if self.process == 'sequential':
                            terminal.print_error(f"Squad execution failed: Operation {i+1} produced unsafe output")
                            return f"Squad execution failed: Operation {i+1} produced unsafe output"
                else:
                    operation_record['status'] = 'empty_output'
                    logger.warning(f"⚠️ SECURITY WARNING: Operation {i+1} produced empty output")
                    terminal.stop_spinner(False, f"Operation {i+1} produced empty output")

            except Exception as e:
                # Update operation record
                operation_record['end_time'] = time.time()
                operation_record['execution_time'] = operation_record['end_time'] - operation_record['start_time']
                operation_record['status'] = 'failed'
                operation_record['error'] = str(e)

                # Update metrics
                self.execution_metrics['operations_failed'] += 1

                # Log error
                logger.error(f"⚠️ SECURITY WARNING: Squad execution failed during operation {i+1}: '{operation.instructions[:50]}...': {e}", exc_info=True)
                terminal.stop_spinner(False, f"Operation {i+1} failed: {str(e)}")

                # Handle failure based on process type
                if self.process == 'sequential':
                    terminal.print_error(f"Squad execution failed: Error during operation {i+1}")
                    return f"Squad execution failed: Error during operation {i+1}: '{operation.instructions[:50]}...'"
                # For non-sequential processes, we might continue with other operations

        # Update execution metrics
        self.execution_metrics['end_time'] = time.time()
        self.execution_metrics['total_execution_time'] = self.execution_metrics['end_time'] - self.execution_metrics['start_time']

        # Log execution metrics for security monitoring
        logger.info(f"Squad deployment finished. Execution time: {self.execution_metrics['total_execution_time']:.2f}s, "
                   f"Operations completed: {self.execution_metrics['operations_completed']}, "
                   f"Operations failed: {self.execution_metrics['operations_failed']}")

        # Perform final security audit on results
        terminal.start_spinner("Performing final security audit on results")
        if not self._audit_squad_results(final_output):
            logger.warning("⚠️ SECURITY WARNING: Final squad result audit failed. Results may be compromised.")
            terminal.stop_spinner(False, "Final security audit failed")
            terminal.print_error("Squad result audit failed. Results may be compromised.")
            return "Error: Squad result audit failed. Results may be compromised."
        terminal.stop_spinner(True, "Final security audit passed")

        # Display the final result
        if final_output:
            terminal.print_result(
                result=final_output,
                execution_time=self.execution_metrics['total_execution_time']
            )

            # Save the result to the specified destination if provided
            if self.result_destination and final_output:
                self._save_result_to_destination(final_output, sanitized_guardrails)

            terminal.print_success(f"Squad deployment completed successfully in {self.execution_metrics['total_execution_time']:.2f}s")
        else:
            terminal.print_error("Squad deployment completed but produced no output")

        return final_output

    def _validate_squad_security(self) -> bool:
        """
        Validates the security of the squad configuration before execution.
        Checks for potential security issues in the squad setup.
        Security checks are applied based on the squad's security profile.

        Returns:
            bool: True if the squad passes all security checks, False otherwise
        """
        logger.debug(f"Validating squad security with profile {self.security_profile.value}...")

        # Skip most checks for minimal security profile
        if self.security_profile == SecurityProfile.MINIMAL:
            logger.info("Using MINIMAL security profile - performing only basic squad validation")
            # Only check if there are any experts and operations
            if not self.experts or not self.operations:
                logger.error("⚠️ SECURITY WARNING: Squad security validation failed: No experts or operations in squad")
                return False
            return True

        # For low security profile, only perform basic checks
        if self.security_profile == SecurityProfile.LOW:
            logger.info("Using LOW security profile - performing basic squad validation")

            # 1. Check if there are any experts and operations
            if not self.experts:
                logger.error("⚠️ SECURITY WARNING: Squad security validation failed: No experts in squad")
                return False

            if not self.operations:
                logger.error("⚠️ SECURITY WARNING: Squad security validation failed: No operations in squad")
                return False

            # 2. Check for proper process type
            valid_processes = ['sequential', 'hierarchical', 'parallel']
            if self.process not in valid_processes:
                logger.error(f"⚠️ SECURITY WARNING: Squad security validation failed: Invalid process type '{self.process}'")
                return False

            return True

        # For standard and higher security profiles, perform comprehensive checks

        # 1. Check if there are any experts and operations
        if not self.experts:
            logger.error("⚠️ SECURITY WARNING: Squad security validation failed: No experts in squad")
            return False

        if not self.operations:
            logger.error("⚠️ SECURITY WARNING: Squad security validation failed: No operations in squad")
            return False

        # 2. Check for expert security profiles
        security_profiles = [getattr(expert, 'security_profile', None) for expert in self.experts]
        if not all(security_profiles):
            logger.warning("⚠️ SECURITY WARNING: Squad security validation: Some experts have no security profile")
            # Warning only, not a failure

        # 3. Check for potential circular dependencies or infinite loops in operations
        # This is a simplified check - in a real system, you would have more sophisticated
        # dependency analysis
        if self.process == 'sequential' and len(self.operations) > 20:
            logger.warning("⚠️ SECURITY WARNING: Squad security validation: Large number of sequential operations may indicate inefficiency")
            # Warning only, not a failure

        # 4. Check for expert-operation compatibility
        for operation in self.operations:
            if operation.expert and not hasattr(operation.expert, 'execute_task'):
                logger.error(f"⚠️ SECURITY WARNING: Squad security validation failed: Expert assigned to operation '{operation.instructions[:30]}...' lacks execute_task method")
                return False

        # 5. Check for duplicate operations (potential redundancy attack)
        operation_instructions = [operation.instructions for operation in self.operations]
        if len(operation_instructions) != len(set(operation_instructions)):
            logger.warning("⚠️ SECURITY WARNING: Squad security validation: Duplicate operation instructions detected")
            # Warning only, not a failure

        # 6. Check for excessive resource usage
        total_instruction_length = sum(len(operation.instructions) for operation in self.operations)
        max_instruction_length = 100000  # Default limit

        # Adjust limit based on security profile
        if self.security_profile == SecurityProfile.HIGH:
            max_instruction_length = 50000
        elif self.security_profile == SecurityProfile.MAXIMUM:
            max_instruction_length = 20000
        elif self.security_profile == SecurityProfile.CUSTOM:
            # For custom profiles, use a limit based on the security thresholds
            # Lower thresholds mean stricter security, so we use a lower limit
            sensitivity_threshold = self.security_thresholds.get("sensitive_data", 0.5)
            # Scale the limit based on the threshold (inverse relationship)
            # 0.1 (strict) -> 20000, 0.9 (permissive) -> 100000
            max_instruction_length = int(20000 + (100000 - 20000) * sensitivity_threshold)

        if total_instruction_length > max_instruction_length:
            logger.error(f"⚠️ SECURITY WARNING: Squad security validation failed: Total operation instructions too long ({total_instruction_length} chars, limit {max_instruction_length})")
            return False

        # 7. Check for proper process type
        valid_processes = ['sequential', 'hierarchical', 'parallel']
        if self.process not in valid_processes:
            logger.error(f"⚠️ SECURITY WARNING: Squad security validation failed: Invalid process type '{self.process}'")
            return False

        # 8. For HIGH, MAXIMUM, and CUSTOM security profiles, perform additional checks
        if self.security_profile in [SecurityProfile.HIGH, SecurityProfile.MAXIMUM, SecurityProfile.CUSTOM]:
            # Check for security profile consistency
            if any(getattr(expert, 'security_profile', None) != self.security_profile for expert in self.experts):
                logger.warning("⚠️ SECURITY WARNING: Squad security validation: Not all experts have matching security profiles")

                # Warning only for HIGH and some CUSTOM profiles, failure for MAXIMUM
                if self.security_profile == SecurityProfile.MAXIMUM or (
                    self.security_profile == SecurityProfile.CUSTOM and
                    self.security_thresholds.get("reliability_score", 0.5) < 0.3  # Strict custom profile
                ):
                    profile_name = self.custom_profile_name if self.security_profile == SecurityProfile.CUSTOM else self.security_profile.value
                    logger.error(f"⚠️ SECURITY WARNING: Squad security validation failed: Security profile mismatch in {profile_name} security mode")
                    return False

        # All checks passed
        logger.debug("Squad security validation passed")
        return True

    def _audit_squad_results(self, final_output: Optional[str]) -> bool:
        """
        Performs a security audit on the final results of the squad execution.

        Args:
            final_output (Optional[str]): The final output of the squad execution

        Returns:
            bool: True if the results pass all security checks, False otherwise
        """
        logger.debug("Performing squad result audit...")

        # 1. Check if there is a final output
        if not final_output:
            logger.warning("⚠️ SECURITY WARNING: Squad result audit: No final output")
            return True  # Not necessarily a failure

        # 2. Check for excessive output length
        if len(final_output) > 100000:  # Arbitrary limit
            logger.warning("⚠️ SECURITY WARNING: Squad result audit failed: Final output too long")
            return False

        # 3. Check execution metrics for anomalies
        if hasattr(self, 'execution_metrics'):
            # Check for operations that took too long
            if self.execution_metrics.get('total_execution_time', 0) > 300:  # 5 minutes
                logger.warning("⚠️ SECURITY WARNING: Squad result audit: Execution took unusually long")
                # Warning only, not a failure

            # Check for failed operations
            if self.execution_metrics.get('operations_failed', 0) > 0:
                logger.warning(f"⚠️ SECURITY WARNING: Squad result audit: {self.execution_metrics.get('operations_failed')} operations failed")
                # Warning only, not a failure

            # Check for completion rate
            completed = self.execution_metrics.get('operations_completed', 0)
            total = self.execution_metrics.get('total_operations', 0)
            if total > 0 and completed / total < 0.5:
                logger.warning(f"⚠️ SECURITY WARNING: Squad result audit: Low operation completion rate ({completed}/{total})")
                # Warning only, not a failure

        # 4. Check for potentially harmful content in the final output
        harmful_content_patterns = [
            r'\b(?:bomb|explosive|terrorist|terrorism|attack plan)\b',
            r'\b(?:hack|exploit|vulnerability|attack vector|zero-day)\b',
            r'\b(?:child abuse|child exploitation)\b',
            r'\b(?:genocide|mass shooting|school shooting)\b',
            r'\b(?:suicide|self-harm)\b',
        ]

        # For custom profiles, adjust the check based on the security thresholds
        if self.security_profile == SecurityProfile.CUSTOM:
            # Skip this check for very permissive custom profiles
            if self.security_thresholds.get("sensitive_data", 0.5) > 0.8:
                logger.info(f"Squad result audit: Skipping harmful content check for permissive custom profile '{self.custom_profile_name}'")
            else:
                for pattern in harmful_content_patterns:
                    if get_cached_regex(pattern).search(final_output):
                        logger.warning(f"⚠️ SECURITY WARNING: Squad result audit failed: Potentially harmful content detected in final output (custom profile '{self.custom_profile_name}')")
                        return False
        else:
            # Standard check for built-in profiles
            for pattern in harmful_content_patterns:
                if get_cached_regex(pattern).search(final_output):
                    logger.warning("⚠️ SECURITY WARNING: Squad result audit failed: Potentially harmful content detected in final output")
                    return False

        # All checks passed
        logger.debug("Squad result audit passed")
        return True

    @cache_security_validation
    def _validate_operation_security(self, operation: Operation, index: int) -> bool:
        """
        Enhanced security validation of an operation before execution.
        Implements more sophisticated detection for dangerous operations and other security issues.
        Security checks are applied based on the squad's security profile.
        Results are cached for improved performance.

        Args:
            operation (Operation): The operation to validate
            index (int): The index of the operation in the task list (used for logging)

        Returns:
            bool: True if the operation passes all security checks, False otherwise
        """
        # Use index in logging for better traceability
        logger.debug(f"Validating operation at index {index} with security profile {self.security_profile.value}")

        # Skip most checks for minimal security profile
        if self.security_profile == SecurityProfile.MINIMAL:
            logger.info(f"Using MINIMAL security profile - performing only basic operation validation for operation {index+1}")
            # Only check if operation has valid instructions
            if not operation.instructions or len(operation.instructions.strip()) < 5:
                logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Instructions too short or empty")
                self._record_security_incident("invalid_instructions", operation, "too_short_or_empty")
                return False
            return True

        # For low security profile, only perform basic checks
        if self.security_profile == SecurityProfile.LOW:
            logger.info(f"Using LOW security profile - performing basic operation validation for operation {index+1}")

            # 1. Check if operation has valid instructions
            if not operation.instructions or len(operation.instructions.strip()) < 10:
                logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Instructions too short or empty")
                self._record_security_incident("invalid_instructions", operation, "too_short_or_empty")
                return False

            # 2. Check for excessive instruction length
            if len(operation.instructions) > 20000:  # More permissive limit for LOW security
                logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Instructions too long ({len(operation.instructions)} chars)")
                self._record_security_incident("excessive_instructions", operation, f"length={len(operation.instructions)}")
                return False

            # 3. Check for critical system commands only
            critical_patterns = [
                r'\b(?:rm\s+-rf\s+/|format\s+[a-z]:|\bdd\s+if)',
                r'\b(?:wipe|erase)\s+(?:disk|drive|all)',
                r'\b(?:drop\s+database|truncate\s+all)',
            ]

            for pattern in critical_patterns:
                if get_cached_regex(pattern).search(operation.instructions):
                    logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Critical system command detected matching pattern: '{pattern}'")
                    self._record_security_incident("critical_command", operation, pattern)
                    return False

            return True

        # For standard and higher security profiles, perform comprehensive checks

        # 1. Check if operation has valid instructions
        if not operation.instructions or len(operation.instructions.strip()) < 10:
            logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Instructions too short or empty")
            self._record_security_incident("invalid_instructions", operation, "too_short_or_empty")
            return False

        # 2. Check for excessive instruction length
        max_length = 10000  # Default for STANDARD
        if self.security_profile == SecurityProfile.HIGH:
            max_length = 5000
        elif self.security_profile == SecurityProfile.MAXIMUM:
            max_length = 2000

        if len(operation.instructions) > max_length:
            logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Instructions too long ({len(operation.instructions)} chars, limit {max_length})")
            self._record_security_incident("excessive_instructions", operation, f"length={len(operation.instructions)}")
            return False

        # 3. Enhanced check for potentially dangerous operations based on keywords
        if self.security_checks.get("critical_exploits", True):
            dangerous_patterns = [
                # System commands
                r'\b(?:system|exec|eval|subprocess)\s*\(',
                r'\b(?:os\.|subprocess\.|shell\.|bash\.|powershell\.|cmd\.|terminal\.|console\.)',

                # File system operations
                r'\b(?:rm\s+-rf|rmdir\s+/|format\s+[a-z]:)',
                r'\b(?:delete|remove)\s+(?:all|every|database|file|directory|folder)',
                r'\b(?:wipe|erase)\s+(?:disk|drive|data|database|file|directory|folder)',

                # Database operations
                r'\b(?:drop\s+table|drop\s+database|truncate\s+table)',
                r'\b(?:delete\s+from\s+\w+\s+where|update\s+\w+\s+set)',

                # Network operations
                r'\b(?:socket\.|connect\(|bind\(|listen\(|accept\()',
                r'\b(?:wget\s+|curl\s+|fetch\s+|download\s+)(?:http|https|ftp)',

                # Code execution
                r'\b(?:eval\(|setTimeout\(|setInterval\(|Function\()',
                r'\b(?:require\(|import\s+|from\s+\w+\s+import)',
            ]

            for pattern in dangerous_patterns:
                if get_cached_regex(pattern).search(operation.instructions):
                    logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Potentially dangerous operation detected matching pattern: '{pattern}'")
                    self._record_security_incident("dangerous_operation", operation, pattern)
                    return False

        # 4. Enhanced check for operations that might lead to data exfiltration
        if self.security_checks.get("content_analysis", True):
            exfiltration_patterns = [
                r'\b(?:send|transmit|upload|post|export)\s+(?:data|file|information|content|document)\s+(?:to|on|at)\s+(?:http|https|ftp|external|remote)',
                r'\b(?:email|mail|message|dm|direct message)\s+(?:data|file|information|content|document|report)\s+(?:to|at)',
                r'\b(?:share|transfer|copy)\s+(?:data|file|information|content|document)\s+(?:with|to)\s+(?:external|outside|third-party)',
                r'\b(?:api|endpoint|webhook|callback)\s+(?:send|post|put)\s+(?:data|information|content)',
            ]

            for pattern in exfiltration_patterns:
                if get_cached_regex(pattern).search(operation.instructions):
                    logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Potential data exfiltration detected matching pattern: '{pattern}'")
                    self._record_security_incident("data_exfiltration", operation, pattern)
                    return False

        # 5. Check for operations that might involve impersonation
        if self.security_profile in [SecurityProfile.STANDARD, SecurityProfile.HIGH, SecurityProfile.MAXIMUM]:
            impersonation_patterns = [
                r'\b(?:pretend|act|pose|impersonate)\s+(?:as|to be|like)\s+(?:another|different|other)\s+(?:expert|agent|user|person|entity)',
                r'\b(?:change|modify|alter|switch)\s+(?:identity|role|specialty|persona)',
                r'\b(?:fake|forge|falsify|spoof)\s+(?:identity|credentials|authorization|authentication)',
            ]

            for pattern in impersonation_patterns:
                if get_cached_regex(pattern).search(operation.instructions):
                    logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Potential impersonation attempt detected matching pattern: '{pattern}'")
                    self._record_security_incident("impersonation_attempt", operation, pattern)
                    return False

        # 6. Check for operations that might involve manipulation of other experts
        if self.security_profile in [SecurityProfile.HIGH, SecurityProfile.MAXIMUM]:
            manipulation_patterns = [
                r'\b(?:manipulate|trick|deceive|fool)\s+(?:other|another|different)\s+(?:expert|agent)',
                r'\b(?:bypass|circumvent|get around|evade)\s+(?:security|restriction|limitation|constraint)',
                r'\b(?:exploit|take advantage of|leverage)\s+(?:vulnerability|weakness|flaw|bug)',
            ]

            for pattern in manipulation_patterns:
                if get_cached_regex(pattern).search(operation.instructions):
                    logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Potential expert manipulation attempt detected matching pattern: '{pattern}'")
                    self._record_security_incident("expert_manipulation", operation, pattern)
                    return False

        # 7. Check for operations that might involve unauthorized access
        if self.security_profile in [SecurityProfile.HIGH, SecurityProfile.MAXIMUM]:
            unauthorized_access_patterns = [
                r'\b(?:access|retrieve|obtain|get)\s+(?:unauthorized|restricted|confidential|classified|private)\s+(?:data|information|content|document)',
                r'\b(?:hack|crack|break into|infiltrate)\s+(?:system|database|account|server)',
                r'\b(?:escalate|elevate|increase)\s+(?:privilege|permission|access|authorization)',
            ]

            for pattern in unauthorized_access_patterns:
                if get_cached_regex(pattern).search(operation.instructions):
                    logger.error(f"⚠️ SECURITY WARNING: Operation security validation failed: Potential unauthorized access attempt detected matching pattern: '{pattern}'")
                    self._record_security_incident("unauthorized_access", operation, pattern)
                    return False

        # 8. Verify operation authenticity if expert is assigned
        if self.security_checks.get("expert_validation", True) and hasattr(operation, 'expert') and operation.expert:
            if not self._verify_operation_authenticity(operation, operation.expert):
                logger.error(f"Operation security validation failed: Operation authenticity verification failed")
                self._record_security_incident("authenticity_failure", operation, "failed_expert_verification")
                return False

        # All checks passed
        return True

    def _find_best_expert_for_operation(self, operation: Operation) -> Optional[Expert]:
        """
        Finds the best expert for an operation based on specialty matching.

        Args:
            operation (Operation): The operation to find an expert for

        Returns:
            Optional[Expert]: The best matching expert, or None if no good match is found
        """
        if not self.experts:
            return None

        # Simple keyword matching between operation instructions and expert specialty
        # In a real system, you would use more sophisticated matching algorithms
        best_match = None
        best_score = 0

        for expert in self.experts:
            if not hasattr(expert, 'specialty') or not expert.specialty:
                continue

            # Calculate a simple match score based on word overlap
            expert_words = set(expert.specialty.lower().split())
            instruction_words = set(operation.instructions.lower().split())

            # Calculate intersection of words
            common_words = expert_words.intersection(instruction_words)
            score = len(common_words)

            # Bonus for security profile match if operation has security requirements
            if hasattr(expert, 'security_profile') and expert.security_profile:
                if 'secure' in operation.instructions.lower() and 'high' in expert.security_profile.lower():
                    score += 2

            if score > best_score:
                best_score = score
                best_match = expert

        # Only return if we have a reasonable match
        if best_score > 0:
            return best_match

        return None

    def _is_safe_for_context_passing(self, previous_result: str, next_operation: Operation) -> bool:
        """
        Enhanced security checks to determine if a previous operation's result is safe
        to pass as context to the next operation.

        Args:
            previous_result (str): The result of the previous operation
            next_operation (Operation): The next operation to receive the context

        Returns:
            bool: True if the result is safe to pass as context, False otherwise
        """
        # 1. Check for excessive length
        if len(previous_result) > 50000:
            logger.warning("Context passing check: Previous result too long")
            self._record_security_incident("excessive_context_length", next_operation, f"length={len(previous_result)}")
            return False

        # 2. Enhanced check for potentially harmful content
        harmful_patterns = [
            # Violence
            r'\b(?:bomb|explosive|terrorist|terrorism|attack plan|mass casualty|assassination)\b',
            r'\b(?:school shooting|mass shooting|genocide|ethnic cleansing|violent extremism)\b',

            # Cybersecurity exploits
            r'\b(?:hack|exploit|vulnerability|attack vector|zero-day|security hole|backdoor)\b',
            r'\b(?:malware|ransomware|spyware|rootkit|keylogger|botnet|trojan|worm)\b',

            # Illegal activities
            r'\b(?:child abuse|child exploitation|human trafficking|sex trafficking|slavery)\b',
            r'\b(?:drug trafficking|illegal weapons|money laundering|fraud scheme)\b',
        ]

        for pattern in harmful_patterns:
            if re.search(pattern, previous_result, re.IGNORECASE):
                logger.warning(f"Context passing check: Potentially harmful content detected matching pattern: '{pattern}'")
                self._record_security_incident("harmful_context", next_operation, pattern)
                return False

        # 3. Enhanced check for potential prompt injection attempts in the previous result
        injection_patterns = [
            # Direct injection attempts
            r"ignore (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            r"disregard (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            r"forget (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            r"don'?t (?:follow|adhere to|listen to|obey) (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",

            # Indirect injection attempts
            r"(?:from now on|starting now|beginning now|henceforth),? (?:you are|you're|you will be|you should be)",
            r"(?:let'?s|we should) (?:pretend|imagine|assume|say) (?:that|you are|you're)",
            r"(?:I want|I need|I would like) you to (?:pretend|imagine|assume|act) (?:as if|like|that)",

            # Authority-based injection
            r"(?:as|being) (?:your|an|the) (?:creator|developer|programmer|administrator|admin|supervisor|owner)",
            r"(?:I am|I'm) (?:your|an|the) (?:creator|developer|programmer|administrator|admin|supervisor|owner)",
        ]

        for pattern in injection_patterns:
            if re.search(pattern, previous_result, re.IGNORECASE):
                logger.warning(f"Context passing check: Potential prompt injection detected matching pattern: '{pattern}'")
                self._record_security_incident("prompt_injection", next_operation, pattern)
                return False

        # 4. NEW: Check for expert impersonation attempts
        if hasattr(next_operation, 'expert') and hasattr(next_operation.expert, 'specialty'):
            impersonation_patterns = [
                r"(?:I am|I'm) (?:a|an) {re.escape(next_operation.expert.specialty)}",
                r"(?:This is|Speaking as) (?:a|an) {re.escape(next_operation.expert.specialty)}",
                r"(?:As|Being) (?:a|an) {re.escape(next_operation.expert.specialty)}",
            ]

            for pattern in impersonation_patterns:
                if re.search(pattern, previous_result, re.IGNORECASE):
                    logger.warning(f"Context passing check: Potential expert impersonation detected")
                    self._record_security_incident("context_impersonation", next_operation, pattern)
                    return False

        # 5. NEW: Check for context relevance to next operation
        # Only apply this check in high or maximum security levels
        if self.security_level in ['high', 'maximum'] and hasattr(next_operation, 'instructions'):
            # Extract key terms from both the previous result and next operation
            result_words = set(re.findall(r'\b\w{4,}\b', previous_result.lower()))
            instruction_words = set(re.findall(r'\b\w{4,}\b', next_operation.instructions.lower()))

            # Calculate relevance score based on word overlap
            if instruction_words and result_words:
                common_words = instruction_words.intersection(result_words)
                relevance_score = len(common_words) / len(instruction_words)

                # Very low threshold - we just want to catch completely irrelevant context
                if relevance_score < 0.05:
                    logger.warning(f"Context passing check: Previous result appears irrelevant to next operation (score: {relevance_score:.2f})")
                    self._record_security_incident("irrelevant_context", next_operation, f"relevance_score={relevance_score:.2f}")
                    return False

        # 6. NEW: Check trust level between experts if trust verification is enabled
        if self.trust_verification and hasattr(next_operation, 'expert'):
            # Find the expert from the previous operation
            previous_expert = None
            for operation in self.operations:
                if operation.result == previous_result and hasattr(operation, 'expert'):
                    previous_expert = operation.expert
                    break

            if previous_expert and hasattr(previous_expert, 'specialty') and hasattr(next_operation.expert, 'specialty'):
                # Check if trust level is sufficient
                if previous_expert.specialty in self.security_context['expert_trust_levels'] and \
                   next_operation.expert.specialty in self.security_context['expert_trust_levels'][previous_expert.specialty]:
                    trust_level = self.security_context['expert_trust_levels'][previous_expert.specialty][next_operation.expert.specialty]

                    # Higher threshold for higher security levels
                    threshold = 0.3 if self.security_level == 'standard' else 0.5

                    if trust_level < threshold:
                        logger.warning(f"Context passing check: Insufficient trust level between experts ({trust_level:.2f} < {threshold:.2f})")
                        self._record_security_incident("insufficient_trust", next_operation, f"trust_level={trust_level:.2f}")
                        return False

        # All checks passed
        return True

    def _calculate_operation_timeout(self, operation: Operation) -> float:
        """
        Calculates an appropriate timeout for an operation based on its complexity.

        Args:
            operation (Operation): The operation to calculate a timeout for

        Returns:
            float: The timeout in seconds
        """
        # Base timeout
        timeout = 30.0  # 30 seconds base timeout

        # Adjust based on instruction length (proxy for complexity)
        instruction_length = len(operation.instructions)
        if instruction_length > 1000:
            timeout += min(30, instruction_length / 100)  # Add up to 30 seconds based on length

        # Adjust based on operation type (if we can infer it from instructions)
        if re.search(r'\b(?:analyze|research|investigate|study)\b', operation.instructions, re.IGNORECASE):
            timeout += 30  # Research operations may take longer

        if re.search(r'\b(?:generate|create|write|draft)\b', operation.instructions, re.IGNORECASE):
            timeout += 20  # Creative operations may take longer

        if re.search(r'\b(?:summarize|condense|shorten)\b', operation.instructions, re.IGNORECASE):
            timeout += 10  # Summarization operations may take a bit longer

        # Cap the timeout at a reasonable maximum
        max_timeout = 180  # 3 minutes maximum
        return min(timeout, max_timeout)

    def _initialize_expert_trust_levels(self) -> None:
        """
        Initializes trust levels between experts in the squad.
        Trust levels range from 0.0 (no trust) to 1.0 (full trust).
        """
        # Initialize trust levels matrix
        for expert1 in self.experts:
            self.security_context['expert_trust_levels'][expert1.specialty] = {}

            for expert2 in self.experts:
                # Default trust level based on security profiles
                if expert1 == expert2:
                    # An expert fully trusts itself
                    trust_level = 1.0
                elif hasattr(expert1, 'security_profile') and hasattr(expert2, 'security_profile'):
                    # Higher trust between experts with the same security profile
                    if expert1.security_profile == expert2.security_profile:
                        trust_level = 0.8
                    # Lower trust between experts with different security profiles
                    else:
                        # High security experts trust others less
                        if expert1.security_profile == 'high_security':
                            trust_level = 0.5
                        else:
                            trust_level = 0.7
                else:
                    # Default trust level if security profiles are not available
                    trust_level = 0.6

                self.security_context['expert_trust_levels'][expert1.specialty][expert2.specialty] = trust_level

        logger.debug(f"Initialized expert trust levels for {len(self.experts)} experts")

    def _validate_expert_compatibility(self) -> None:
        """
        Validates compatibility between experts in the squad.
        Raises a warning if incompatible experts are detected.
        """
        # Check for experts with conflicting security profiles
        security_profiles = [expert.security_profile for expert in self.experts if hasattr(expert, 'security_profile')]

        # Check for mixing high security with no security
        if 'high_security' in security_profiles and 'default' in security_profiles:
            logger.warning("Expert compatibility warning: Mixing high security experts with default security experts")

        # Check for experts with the same specialty (potential redundancy)
        specialties = [expert.specialty for expert in self.experts if hasattr(expert, 'specialty')]
        specialty_counts = Counter(specialties)

        for specialty, count in specialty_counts.items():
            if count > 1:
                logger.warning(f"Expert compatibility warning: {count} experts with the same specialty '{specialty}'")

        # Check for experts with potentially conflicting objectives
        for i, expert1 in enumerate(self.experts):
            if not hasattr(expert1, 'objective'):
                continue

            for j, expert2 in enumerate(self.experts[i+1:], i+1):
                if not hasattr(expert2, 'objective'):
                    continue

                # Simple check for conflicting keywords in objectives
                conflict_pairs = [
                    ('maximize', 'minimize'),
                    ('increase', 'decrease'),
                    ('promote', 'prevent'),
                    ('allow', 'block'),
                    ('enable', 'disable'),
                ]

                for word1, word2 in conflict_pairs:
                    if (word1 in expert1.objective.lower() and word2 in expert2.objective.lower()) or \
                       (word2 in expert1.objective.lower() and word1 in expert2.objective.lower()):
                        logger.warning(f"Expert compatibility warning: Potentially conflicting objectives between "
                                      f"'{expert1.specialty}' and '{expert2.specialty}'")
                        break

    def _update_expert_trust(self, expert1: Expert, expert2: Expert, outcome: str) -> None:
        """
        Updates trust level between two experts based on interaction outcome.

        Args:
            expert1 (Expert): The first expert
            expert2 (Expert): The second expert
            outcome (str): The outcome of their interaction ('success', 'failure', 'security_issue')
        """
        if not hasattr(expert1, 'specialty') or not hasattr(expert2, 'specialty'):
            return

        if expert1.specialty not in self.security_context['expert_trust_levels'] or \
           expert2.specialty not in self.security_context['expert_trust_levels'][expert1.specialty]:
            return

        current_trust = self.security_context['expert_trust_levels'][expert1.specialty][expert2.specialty]

        # Update trust based on outcome
        if outcome == 'success':
            # Increase trust on successful interaction
            new_trust = min(1.0, current_trust + 0.05)
        elif outcome == 'failure':
            # Decrease trust on failed interaction
            new_trust = max(0.2, current_trust - 0.1)
        elif outcome == 'security_issue':
            # Significantly decrease trust on security issues
            new_trust = max(0.0, current_trust - 0.3)
        else:
            return

        self.security_context['expert_trust_levels'][expert1.specialty][expert2.specialty] = new_trust
        logger.debug(f"Updated trust level between '{expert1.specialty}' and '{expert2.specialty}' to {new_trust:.2f}")

    def _verify_operation_authenticity(self, operation: Operation, claimed_expert: Expert) -> bool:
        """
        Verifies that an operation is authentically from the claimed expert.
        Helps prevent expert impersonation attacks.

        Args:
            operation (Operation): The operation to verify
            claimed_expert (Expert): The expert claimed to be the source

        Returns:
            bool: True if the operation is authentic, False otherwise
        """
        # Simple verification based on operation characteristics and expert specialty
        if not hasattr(claimed_expert, 'specialty'):
            return False

        # Check if operation instructions align with expert specialty
        specialty_words = set(claimed_expert.specialty.lower().split())
        instruction_words = set(operation.instructions.lower().split())

        # Calculate word overlap
        common_words = specialty_words.intersection(instruction_words)
        overlap_score = len(common_words) / max(1, len(specialty_words))

        # Check for security profile consistency
        security_consistent = True
        if hasattr(claimed_expert, 'security_profile') and claimed_expert.security_profile == 'high_security':
            # High security experts shouldn't request potentially dangerous operations
            dangerous_patterns = [
                r'\b(?:system|exec|eval|subprocess)\s*\(',
                r'\b(?:rm\s+-rf|rmdir\s+/|format\s+[a-z]:)',
                r'\b(?:delete|remove)\s+(?:all|every|database)',
                r'\b(?:drop\s+table|drop\s+database)',
                r'\b(?:wipe|erase)\s+(?:disk|drive|data|database)',
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, operation.instructions, re.IGNORECASE):
                    security_consistent = False
                    break

        # Combine factors for final decision
        # More flexible threshold for standard security level
        if self.security_level == 'standard':
            # For standard security, we're more permissive
            # Either have some word overlap or be security consistent
            return overlap_score > 0.1 or security_consistent
        else:
            # For high/maximum security, maintain stricter requirements
            threshold = 0.3 if self.security_level == 'high' else 0.5
            return overlap_score >= threshold and security_consistent

    def _is_output_safe(self, output: str, operation: Operation) -> bool:
        """
        Enhanced checks to determine if an operation's output is safe.
        Implements more sophisticated detection for harmful content and reliability issues.

        Args:
            output (str): The output to check
            operation (Operation): The operation that produced the output

        Returns:
            bool: True if the output is safe, False otherwise
        """
        # 1. Check for excessive length
        if len(output) > 50000:
            logger.warning("Output safety check: Output too long")
            return False

        # 2. Enhanced check for potentially harmful content
        harmful_patterns = [
            # Violence
            r'\b(?:bomb|explosive|terrorist|terrorism|attack plan|mass casualty|assassination)\b',
            r'\b(?:school shooting|mass shooting|genocide|ethnic cleansing|violent extremism)\b',

            # Cybersecurity exploits
            r'\b(?:hack|exploit|vulnerability|attack vector|zero-day|security hole|backdoor)\b',
            r'\b(?:malware|ransomware|spyware|rootkit|keylogger|botnet|trojan|worm)\b',

            # Illegal activities
            r'\b(?:child abuse|child exploitation|human trafficking|sex trafficking|slavery)\b',
            r'\b(?:drug trafficking|illegal weapons|money laundering|fraud scheme)\b',

            # Self-harm
            r'\b(?:suicide method|how to kill|self-harm technique|suicide instruction)\b',

            # Hate speech indicators
            r'\b(?:racial slur|ethnic slur|hate group|white supremacy|nazi|extremist group)\b',
        ]

        for pattern in harmful_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                logger.warning(f"Output safety check: Potentially harmful content detected matching pattern: '{pattern}'")
                self._record_security_incident("harmful_content", operation, pattern)
                return False

        # 3. Enhanced check for hallucination indicators
        hallucination_patterns = [
            r"I don't actually (?:know|have|possess)",
            r"I'm (?:making|just making) this up",
            r"I'm not (?:sure|certain) (?:about|of) this",
            r"This (?:might|may) not be (?:accurate|correct|right)",
            r"I (?:might be|may be|could be) (?:wrong|mistaken|incorrect)",
            r"I'm (?:guessing|speculating|hypothesizing)",
            r"I (?:can't|cannot) (?:verify|confirm) this",
            r"This is (?:fictional|made up|not real)",
        ]

        for pattern in hallucination_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                logger.warning(f"Output safety check: Potential hallucination detected matching pattern: '{pattern}'")
                self._record_security_incident("hallucination", operation, pattern)
                return False

        # 4. Enhanced check for refusal or inability to complete the operation
        refusal_patterns = [
            r"I (?:can't|cannot|am unable to) (?:assist|help|provide|complete|do) (?:that|this)",
            r"I'm (?:sorry|afraid) (?:but|that) I (?:can't|cannot|am unable to)",
            r"I'm not (?:able|allowed|permitted) to",
            r"(?:This|That) (?:goes|is) (?:against|beyond) my (?:capabilities|programming|abilities)",
            r"I (?:don't|do not) have (?:access|permission|authorization) to",
        ]

        for pattern in refusal_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                logger.warning(f"Output safety check: Expert refused or was unable to complete operation matching pattern: '{pattern}'")
                self._record_security_incident("refusal", operation, pattern)
                return False

        # 5. NEW: Check for expert impersonation attempts - but be more lenient with template variables
        if hasattr(operation, 'expert') and hasattr(operation.expert, 'specialty'):
            # Check if the operation uses template variables
            has_template_vars = '{' in operation.instructions and '}' in operation.instructions

            if not has_template_vars:
                # Only apply strict impersonation checks for operations without template variables
                impersonation_patterns = [
                    r"(?:I am|I'm) (?:actually|really) (?:a|an) (?!{re.escape(operation.expert.specialty)})",
                    r"(?:This is|Speaking as) (?!{re.escape(operation.expert.specialty)})",
                    r"(?:not|no longer) (?:a|an) {re.escape(operation.expert.specialty)}",
                ]

                for pattern in impersonation_patterns:
                    if re.search(pattern, output, re.IGNORECASE):
                        logger.warning(f"Output safety check: Potential expert impersonation detected")
                        self._record_security_incident("impersonation", operation, pattern)
                        return False

        # 6. NEW: Check for output consistency with operation
        if hasattr(operation, 'instructions') and len(operation.instructions) > 20:
            # Extract key terms from the operation instructions
            # Handle template variables in instructions
            processed_instructions = operation.instructions
            template_vars = re.findall(r'\{([^{}]+)\}', operation.instructions)

            # Process template variables
            for var in template_vars:
                # Remove any formatting instructions (e.g., "select, true:...")
                clean_var = var.split(',')[0].strip() if ',' in var else var.strip()
                # Replace the template variable with a generic term for text processing
                processed_instructions = processed_instructions.replace(f"{{{var}}}", f"variable_{clean_var}")

            # Extract words from processed instructions and output
            instruction_words = set(re.findall(r'\b\w{4,}\b', processed_instructions.lower()))
            output_words = set(re.findall(r'\b\w{4,}\b', output.lower()))

            # Add template variable names to instruction words
            for var in template_vars:
                clean_var = var.split(',')[0].strip() if ',' in var else var.strip()
                if len(clean_var) > 3:
                    instruction_words.add(clean_var.lower())

            # Calculate relevance score based on word overlap
            if instruction_words:
                common_words = instruction_words.intersection(output_words)
                relevance_score = len(common_words) / len(instruction_words)

                # Check if the operation uses template variables
                has_template_vars = '{' in operation.instructions and '}' in operation.instructions

                if has_template_vars:
                    # For operations with template variables, be extremely lenient
                    # Only fail if there's absolutely no overlap and the output is very short
                    if relevance_score == 0 and len(output_words) < 10:
                        logger.warning(f"Output safety check: Output appears completely irrelevant to operation (score: 0.00)")
                        self._record_security_incident("irrelevant_output", operation, "relevance_score=0.00")
                        return False
                else:
                    # For regular operations, use normal thresholds
                    threshold = 0.05 if self.security_level == 'standard' else 0.1
                    if relevance_score < threshold:
                        logger.warning(f"Output safety check: Output appears irrelevant to operation (score: {relevance_score:.2f})")
                        self._record_security_incident("irrelevant_output", operation, f"relevance_score={relevance_score:.2f}")
                        return False

        # All checks passed
        return True

    def _save_result_to_destination(self, result: str, guardrails: Optional[Dict[str, Any]] = None) -> bool:
        """
        Saves the squad's final result to the specified destination.

        Args:
            result (str): The result to save
            guardrails (Optional[Dict[str, Any]]): The guardrails used during execution

        Returns:
            bool: True if the result was successfully saved, False otherwise
        """
        if not self.result_destination:
            return False

        try:
            # Extract format and file_path from result_destination
            format_type = self.result_destination.get("format", "txt").lower()
            file_path = self.result_destination.get("file_path")

            if not file_path:
                logger.error("Result destination missing file_path")
                return False

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

            # Handle different file formats
            if format_type in ["txt", "md", "markdown"]:
                # Plain text format
                with open(file_path, 'w', encoding='utf-8') as f:
                    # Write header with metadata
                    f.write(f"# Squad Result\n\n")
                    f.write(f"## Squad Details\n")
                    f.write(f"- Experts: {len(self.experts)}\n")
                    f.write(f"- Operations: {len(self.operations)}\n")
                    f.write(f"- Process: {self.process}\n")
                    f.write(f"- Security Level: {self.security_level}\n")
                    f.write(f"- Execution Time: {self.execution_metrics.get('total_execution_time', 0):.2f} seconds\n\n")

                    # Write guardrails if available
                    if guardrails:
                        f.write(f"## Guardrail Inputs\n")
                        for key, value in guardrails.items():
                            f.write(f"- {key}: {value}\n")
                        f.write("\n")

                    # Write the result
                    f.write(f"## Result\n\n")
                    f.write(result)

            elif format_type == "csv":
                # CSV format
                import csv
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Write header row
                    writer.writerow(['Squad', 'Experts', 'Operations', 'Process', 'Security Level', 'Execution Time', 'Result'])
                    # Write data row
                    writer.writerow([
                        f"Squad-{self.security_context.get('squad_id', 'unknown')[:8]}",
                        len(self.experts),
                        len(self.operations),
                        self.process,
                        self.security_level,
                        f"{self.execution_metrics.get('total_execution_time', 0):.2f}s",
                        result
                    ])

            elif format_type == "json":
                # JSON format
                import json
                data = {
                    'squad': {
                        'experts': len(self.experts),
                        'operations': len(self.operations),
                        'process': self.process,
                        'security_level': self.security_level,
                    },
                    'execution_metrics': self.execution_metrics,
                    'guardrails': guardrails,
                    'result': result
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)

            elif format_type == "html":
                # HTML format - create a simple HTML file with the result
                # Prepare the data
                num_experts = str(len(self.experts))
                num_operations = str(len(self.operations))
                process_type = self.process
                security_level = self.security_level
                execution_time = f"{self.execution_metrics.get('total_execution_time', 0):.2f}"

                # Create HTML content manually without using format or f-strings
                html_content = "<!DOCTYPE html>\n"
                html_content += "<html>\n"
                html_content += "<head>\n"
                html_content += "    <title>Squad Result</title>\n"
                html_content += "    <style>\n"
                html_content += "        body { font-family: Arial, sans-serif; margin: 20px; }\n"
                html_content += "        h1, h2 { color: #333; }\n"
                html_content += "        .metadata { background-color: #f5f5f5; padding: 10px; border-radius: 5px; }\n"
                html_content += "        .result { margin-top: 20px; }\n"
                html_content += "    </style>\n"
                html_content += "</head>\n"
                html_content += "<body>\n"
                html_content += "    <h1>Squad Result</h1>\n\n"
                html_content += "    <div class=\"metadata\">\n"
                html_content += "        <h2>Squad Details</h2>\n"
                html_content += "        <p><strong>Experts:</strong> " + num_experts + "</p>\n"
                html_content += "        <p><strong>Operations:</strong> " + num_operations + "</p>\n"
                html_content += "        <p><strong>Process:</strong> " + process_type + "</p>\n"
                html_content += "        <p><strong>Security Level:</strong> " + security_level + "</p>\n"
                html_content += "        <p><strong>Execution Time:</strong> " + execution_time + " seconds</p>\n\n"
                html_content += "        <h2>Guardrail Inputs</h2>\n"
                html_content += "        <ul>\n"

                # Add guardrail items
                if guardrails:
                    for key, value in guardrails.items():
                        html_content += "            <li><strong>" + str(key) + ":</strong> " + str(value) + "</li>\n"

                html_content += "        </ul>\n"
                html_content += "    </div>\n\n"
                html_content += "    <div class=\"result\">\n"
                html_content += "        <h2>Result</h2>\n"

                # Replace newlines with <br> tags for HTML display
                result_html = result.replace('\n', '<br>')
                html_content += "        " + result_html + "\n"

                html_content += "    </div>\n"
                html_content += "</body>\n"
                html_content += "</html>"

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)

            elif format_type == "pdf":
                # PDF format
                try:
                    from reportlab.lib.pagesizes import letter
                    from reportlab.lib import colors
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

                    # Create the PDF document
                    doc = SimpleDocTemplate(file_path, pagesize=letter)
                    styles = getSampleStyleSheet()

                    # Create custom styles
                    title_style = styles["Heading1"]
                    heading_style = styles["Heading2"]
                    normal_style = styles["Normal"]

                    # Create the content
                    content = []

                    # Title
                    content.append(Paragraph("Squad Result", title_style))
                    content.append(Spacer(1, 12))

                    # Squad Details
                    content.append(Paragraph("Squad Details", heading_style))
                    content.append(Spacer(1, 6))

                    # Create a table for squad details
                    squad_data = [
                        ["Experts", str(len(self.experts))],
                        ["Operations", str(len(self.operations))],
                        ["Process", self.process],
                        ["Security Level", self.security_level],
                        ["Execution Time", f"{self.execution_metrics.get('total_execution_time', 0):.2f} seconds"]
                    ]

                    squad_table = Table(squad_data, colWidths=[100, 300])
                    squad_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))

                    content.append(squad_table)
                    content.append(Spacer(1, 12))

                    # Guardrails
                    if guardrails:
                        content.append(Paragraph("Guardrail Inputs", heading_style))
                        content.append(Spacer(1, 6))

                        # Create a table for guardrails
                        guardrail_data = [[key, str(value)] for key, value in guardrails.items()]

                        guardrail_table = Table(guardrail_data, colWidths=[100, 300])
                        guardrail_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ]))

                        content.append(guardrail_table)
                        content.append(Spacer(1, 12))

                    # Result
                    content.append(Paragraph("Result", heading_style))
                    content.append(Spacer(1, 6))

                    # Split the result into paragraphs
                    for paragraph in result.split('\n\n'):
                        if paragraph.strip():
                            content.append(Paragraph(paragraph.replace('\n', '<br/>'), normal_style))
                            content.append(Spacer(1, 6))

                    # Build the PDF
                    doc.build(content)

                except ImportError:
                    logger.warning("reportlab package not installed. Saving result as text file instead.")
                    # Fall back to text file
                    with open(file_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                        f.write(f"# Squad Result\n\n")
                        f.write(f"## Squad Details\n")
                        f.write(f"- Experts: {len(self.experts)}\n")
                        f.write(f"- Operations: {len(self.operations)}\n")
                        f.write(f"- Process: {self.process}\n")
                        f.write(f"- Security Level: {self.security_level}\n")
                        f.write(f"- Execution Time: {self.execution_metrics.get('total_execution_time', 0):.2f} seconds\n\n")
                        if guardrails:
                            f.write(f"## Guardrail Inputs\n")
                            for key, value in guardrails.items():
                                f.write(f"- {key}: {value}\n")
                            f.write("\n")
                        f.write(f"## Result\n\n")
                        f.write(result)
            else:
                # Default to text file for unknown formats
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result)

            logger.info(f"Squad result saved to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving squad result to {self.result_destination}: {e}", exc_info=True)
            return False

    def _sanitize_guardrails(self, guardrails: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes and validates guardrail inputs for security.

        Args:
            guardrails (Dict[str, Any]): The guardrail inputs to sanitize

        Returns:
            Dict[str, Any]: Sanitized guardrail inputs
        """
        if not guardrails:
            return {}

        logger.debug(f"Sanitizing guardrails: {list(guardrails.keys())}")

        sanitized = {}

        # Define patterns for potentially dangerous inputs
        dangerous_patterns = [
            # System commands
            r'\b(?:system|exec|eval|subprocess)\s*\(',
            r'\b(?:os\.|subprocess\.|shell\.|bash\.|powershell\.|cmd\.|terminal\.|console\.)',

            # Injection attempts
            r"ignore (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            r"disregard (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",
            r"forget (?:previous|prior|above|initial|original)(?:\s+|\s*-\s*)instructions",

            # Harmful content
            r'\b(?:bomb|explosive|terrorist|terrorism|attack plan|mass casualty|assassination)\b',
            r'\b(?:school shooting|mass shooting|genocide|ethnic cleansing|violent extremism)\b',
        ]

        # Process each guardrail input
        for key, value in guardrails.items():
            # Skip None values
            if value is None:
                continue

            # Convert to string for pattern matching if not already a string
            value_str = str(value) if not isinstance(value, str) else value

            # Check for dangerous patterns
            is_dangerous = False
            for pattern in dangerous_patterns:
                if re.search(pattern, value_str, re.IGNORECASE):
                    logger.warning(f"Guardrail input '{key}' contains potentially dangerous content matching pattern: '{pattern}'")
                    self._record_security_incident("dangerous_guardrail", None, f"key={key}, pattern={pattern}")
                    is_dangerous = True
                    break

            if is_dangerous:
                continue

            # Check for excessive length
            if len(value_str) > 10000:  # Arbitrary limit
                logger.warning(f"Guardrail input '{key}' exceeds maximum length ({len(value_str)} chars)")
                self._record_security_incident("excessive_guardrail", None, f"key={key}, length={len(value_str)}")
                continue

            # Sanitize the input - remove any HTML/script tags
            if isinstance(value, str):
                # Simple sanitization - remove HTML tags
                sanitized_value = re.sub(r'<[^>]*>', '', value)
                sanitized[key] = sanitized_value
            else:
                # For non-string values, keep as is
                sanitized[key] = value

        logger.debug(f"Sanitized guardrails: {list(sanitized.keys())}")
        return sanitized

    def _record_security_incident(self, incident_type: str, operation: Optional[Operation], details: str) -> None:
        """
        Records a security incident for later analysis.

        Args:
            incident_type (str): The type of security incident
            operation (Optional[Operation]): The operation involved in the incident, or None if not operation-specific
            details (str): Additional details about the incident
        """
        incident = {
            'timestamp': time.time(),
            'type': incident_type,
            'details': details,
        }

        if operation:
            incident['operation_info'] = {
                'instructions': operation.instructions[:100] + ('...' if len(operation.instructions) > 100 else ''),
            }
            if hasattr(operation, 'expert') and operation.expert:
                incident['operation_info']['expert'] = operation.expert.specialty if hasattr(operation.expert, 'specialty') else 'unknown'

        self.security_context['security_incidents'].append(incident)
        logger.debug(f"Recorded security incident: {incident_type}")

        # If we have too many incidents, consider taking action
        if len(self.security_context['security_incidents']) >= 3:
            logger.warning(f"Multiple security incidents detected ({len(self.security_context['security_incidents'])}). Consider reviewing squad configuration.")

            # In maximum security mode, abort the squad after multiple incidents
            if self.security_level == 'maximum' and len(self.security_context['security_incidents']) >= 5:
                logger.error("Too many security incidents. Aborting squad in maximum security mode.")
                raise SecurityError("Squad aborted due to multiple security incidents")
