# tbh_secure_agents/task.py
# Author: Saish (TBH.AI)

"""
Defines the Operation class for the TBH Secure Agents framework.
Operations represent units of work to be performed by experts.
"""

import logging # Import logging
import re
import json
import time
import hashlib
import os
from typing import Optional, Any, Dict, List, Tuple
from collections import Counter
from .agent import Expert # Now we can import Expert

# Get a logger for this module
logger = logging.getLogger(__name__)

# Define custom exceptions
class SecurityError(Exception):
    """Exception raised for security-related issues in the Operation."""
    pass

class Operation:
    """
    Represents a specific operation to be executed by an expert.

    Attributes:
        instructions (str): A clear description of the operation instructions.
        output_format (str, optional): A description of the expected outcome or format.
        expert (Optional[Expert]): The expert assigned to this operation. Can be assigned later.
        context (Optional[str]): Additional context or data needed for the operation.
        result_destination (Optional[str]): File path where the operation result should be saved.
                                           Supports various formats including .txt, .md, .csv, .json, .html, and .pdf.
        # Add attributes like dependencies, priority, security_requirements, etc.
    """
    def __init__(self, instructions: str, output_format: Optional[str] = None, expert: Optional[Expert] = None,
                 context: Optional[str] = None, reliability_threshold: float = 0.7,
                 result_destination: Optional[str] = None, **kwargs):
        self.instructions = instructions
        self.output_format = output_format
        self.expert = expert
        self.context = context
        self.result: Optional[str] = None # To store the outcome after execution
        self.reliability_threshold = reliability_threshold # Threshold for reliability checks
        self.result_destination = result_destination # Path where the result should be saved
        self.execution_metrics = {
            'start_time': None,
            'end_time': None,
            'execution_duration': None,
            'reliability_score': None,
            'relevance_score': None,
            'consistency_score': None,
            'security_checks_passed': 0,
            'security_checks_failed': 0,
            'execution_attempts': 0,
        }
        # Initialize other relevant attributes

    def execute(self, guardrails: Optional[Dict[str, Any]] = None) -> str:
        """
        Executes the operation, likely by calling the assigned expert's execution method.
        Includes enhanced security checks before and after execution with reliability tracking.

        Args:
            guardrails (Optional[Dict[str, Any]]): Dynamic inputs that can be used as guardrails
                                                  during operation execution. These values can be
                                                  referenced in prompts and used for context.

        Returns:
            str: The result of the operation execution
        """
        if not self.expert:
            logger.error(f"Operation execution failed: No expert assigned to operation '{self.instructions[:50]}...'.") # Use logger
            raise ValueError("Operation cannot be executed without an assigned expert.")

        # Initialize guardrails if not provided
        if guardrails is None:
            guardrails = {}

        # Track execution metrics
        self.execution_metrics['start_time'] = time.time()
        self.execution_metrics['execution_attempts'] += 1

        # Enhanced pre-execution security check
        logger.debug(f"Performing pre-execution check for operation '{self.instructions[:50]}...'")
        if not self._pre_execution_secure():
            self.execution_metrics['security_checks_failed'] += 1
            logger.error(f"Operation pre-execution security check failed for '{self.instructions[:50]}...'. Aborting.")
            raise SecurityError(f"Operation failed pre-execution security check: '{self.instructions[:50]}...'")

        self.execution_metrics['security_checks_passed'] += 1
        logger.info(f"Operation '{self.instructions[:50]}...' starting execution by expert '{self.expert.specialty}'.") # Use logger

        # Execute the operation with retry capability for reliability
        max_attempts = 2  # Maximum number of retry attempts
        current_attempt = 0

        while current_attempt < max_attempts:
            try:
                # Prepare context with guardrails if available
                enhanced_context = self._prepare_context_with_guardrails(self.context, guardrails)

                # Pass the operation instructions, enhanced context, and guardrails to the expert
                self.result = self.expert.execute_task(
                    task_description=self.instructions,
                    context=enhanced_context,
                    inputs=guardrails
                )

                # Enhanced post-execution security and reliability check
                logger.debug(f"Performing post-execution check for operation '{self.instructions[:50]}...'")
                reliability_result = self._post_execution_secure(self.result)

                if isinstance(reliability_result, dict):  # New format returning metrics
                    is_secure = reliability_result.get('is_secure', False)
                    # Update metrics
                    for key, value in reliability_result.items():
                        if key in self.execution_metrics and key != 'is_secure':
                            self.execution_metrics[key] = value
                else:
                    is_secure = reliability_result  # Old boolean format for backward compatibility

                if not is_secure:
                    self.execution_metrics['security_checks_failed'] += 1
                    logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check failed for '{self.instructions[:50]}...'. Result may be compromised.")

                    # If this was the last attempt, handle the failure
                    if current_attempt == max_attempts - 1:
                        # Check if we have a reliability score to determine the cause
                        if self.execution_metrics.get('reliability_score', 0) < self.reliability_threshold:
                            logger.error(f"Operation reliability check failed with score {self.execution_metrics.get('reliability_score', 0)}")
                            self.result = f"Error: Expert '{self.expert.specialty}' generated an unreliable response. Please try again with clearer instructions."
                        else:
                            self.result = f"Error: Expert '{self.expert.specialty}' generated a response that failed security checks."
                    else:
                        # Try again with a more explicit instruction
                        current_attempt += 1
                        logger.info(f"Retrying operation (attempt {current_attempt+1}/{max_attempts})...")
                        continue
                else:
                    self.execution_metrics['security_checks_passed'] += 1

                # Record end time and duration
                self.execution_metrics['end_time'] = time.time()
                self.execution_metrics['execution_duration'] = self.execution_metrics['end_time'] - self.execution_metrics['start_time']

                logger.info(f"Operation '{self.instructions[:50]}...' finished execution successfully in {self.execution_metrics['execution_duration']:.2f} seconds.")

                # Generate operation fingerprint for verification
                self._generate_operation_fingerprint()

                # Save the result to the specified destination if provided
                if self.result and self.result_destination:
                    self._save_result_to_destination(self.result, guardrails)

                return self.result

            except Exception as e:
                # Record the failure
                current_attempt += 1
                logger.error(f"Error executing operation '{self.instructions[:50]}...' (attempt {current_attempt}/{max_attempts}): {e}", exc_info=True)

                # If this was the last attempt, re-raise the exception
                if current_attempt == max_attempts:
                    # Record end time and duration even for failed operations
                    self.execution_metrics['end_time'] = time.time()
                    self.execution_metrics['execution_duration'] = self.execution_metrics['end_time'] - self.execution_metrics['start_time']
                    raise  # Re-raise for now, allows Squad to handle it

    # --- Placeholder Security Methods ---

    def _pre_execution_secure(self) -> bool:
        """
        Performs security checks before executing an operation.
        Validates the operation instructions, context, and expert assignment to prevent exploitation.

        Returns:
            bool: True if the operation passes all security checks, False otherwise
        """
        logger.debug(f"Performing operation pre-execution check for '{self.instructions[:50]}...'")

        # 1. Check if operation has valid instructions
        if not self.instructions or len(self.instructions.strip()) < 10:
            logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: Instructions too short or empty")
            return False

        # 2. Check for excessive instruction length (potential resource exhaustion)
        if len(self.instructions) > 10000:
            logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: Instructions too long ({len(self.instructions)} chars)")
            return False

        # 3. Check if expert is properly assigned and has appropriate security profile
        if not self.expert:
            logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: No expert assigned")
            return False

        # Check if result_destination is secure
        if self.result_destination:
            # Check for suspicious file extensions only
            suspicious_extensions = ['.exe', '.bat', '.sh', '.py', '.js', '.php']
            if any(self.result_destination.endswith(ext) for ext in suspicious_extensions):
                logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: Suspicious file extension in result_destination")
                return False

        # 4. Check for potentially dangerous operations based on keywords
        dangerous_operation_patterns = [
            r'\b(?:system|exec|eval|subprocess)\s*\(',
            r'\b(?:rm\s+-rf|rmdir\s+/|format\s+[a-z]:)',
            r'\b(?:delete|remove)\s+(?:all|every|database)',
            r'\b(?:drop\s+table|drop\s+database)',
            r'\b(?:wipe|erase)\s+(?:disk|drive|data|database)',
            r'\b(?:hack|crack|exploit)\b',
        ]

        for pattern in dangerous_operation_patterns:
            if re.search(pattern, self.instructions, re.IGNORECASE):
                logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: Potentially dangerous operation detected")
                return False

        # 5. Check for operations that might lead to data exfiltration
        data_exfiltration_patterns = [
            r'\b(?:send|transmit|upload|post)\s+(?:data|file|information|content)\s+(?:to|on|at)\s+(?:http|ftp|external)',
            r'\b(?:export|extract|dump)\s+(?:database|data|credentials|secrets)',
            r'\b(?:leak|expose|reveal)\s+(?:data|information|secrets|credentials)',
        ]

        for pattern in data_exfiltration_patterns:
            if re.search(pattern, self.instructions, re.IGNORECASE):
                logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: Potential data exfiltration detected")
                return False

        # 6. Check for operations that might lead to privilege escalation
        privilege_escalation_patterns = [
            r'\b(?:sudo|su|runas|administrator|root)\b',
            r'\b(?:escalate|elevate)\s+(?:privilege|permission|access)',
            r'\b(?:gain|obtain)\s+(?:admin|administrator|root)\s+(?:access|privilege|permission)',
        ]

        for pattern in privilege_escalation_patterns:
            if re.search(pattern, self.instructions, re.IGNORECASE):
                logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: Potential privilege escalation detected")
                return False

        # 7. Check for operations that might lead to denial of service
        dos_patterns = [
            r'\b(?:infinite|endless|never-ending)\s+(?:loop|recursion|process)',
            r'\b(?:fork\s+bomb|while\s*\(\s*true\s*\))',
            r'\b(?:consume|exhaust)\s+(?:memory|cpu|resource|bandwidth)',
            r'\b(?:overload|flood|overwhelm)\s+(?:server|service|system|network)',
        ]

        for pattern in dos_patterns:
            if re.search(pattern, self.instructions, re.IGNORECASE):
                logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: Potential denial of service detected")
                return False

        # 8. Validate that the operation is appropriate for the expert's specialty
        # This is a basic implementation - in a real system, you would have a more sophisticated
        # mapping of operation types to expert specialties
        if hasattr(self.expert, 'specialty') and self.expert.specialty:
            specialty_operation_mismatch = False

            # Example specialty-based validation
            if 'security' in self.expert.specialty.lower() and 'create artwork' in self.instructions.lower():
                specialty_operation_mismatch = True
            elif 'writer' in self.expert.specialty.lower() and 'analyze code' in self.instructions.lower():
                specialty_operation_mismatch = True
            elif 'programmer' in self.expert.specialty.lower() and 'legal advice' in self.instructions.lower():
                specialty_operation_mismatch = True

            if specialty_operation_mismatch:
                logger.warning(f"⚠️ SECURITY WARNING: Operation pre-execution security check FAILED: Operation doesn't match expert specialty")
                return False

        # All checks passed
        logger.debug(f"Operation pre-execution security check PASSED for '{self.instructions[:50]}...'")
        return True

    def _generate_operation_fingerprint(self) -> str:
        """
        Generates a unique fingerprint for the operation execution for verification purposes.
        This helps detect tampering with operation results.

        Returns:
            str: A unique fingerprint for the operation execution
        """
        if not self.result:
            return ""

        # Create a fingerprint based on operation details and result
        fingerprint_data = {
            'instructions': self.instructions,
            'expert': self.expert.specialty if hasattr(self.expert, 'specialty') else str(self.expert),
            'result_hash': hashlib.sha256(self.result.encode()).hexdigest(),
            'timestamp': time.time()
        }

        # Generate the fingerprint
        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        fingerprint = hashlib.sha256(fingerprint_str.encode()).hexdigest()

        # Store the fingerprint with the operation
        self.execution_metrics['fingerprint'] = fingerprint

        logger.debug(f"Generated operation fingerprint: {fingerprint[:8]}...")
        return fingerprint

    def _post_execution_secure(self, result: Optional[str]) -> Dict:
        """
        Enhanced security and reliability checks on operation results after execution.
        Validates the output for reliability, consistency, and security concerns.

        Args:
            result (Optional[str]): The result of the operation execution

        Returns:
            Dict: A dictionary containing security check results and reliability metrics
        """
        logger.debug(f"Performing enhanced operation post-execution check for '{self.instructions[:50]}...'")

        # Initialize metrics
        metrics = {
            'is_secure': True,
            'reliability_score': 1.0,
            'relevance_score': 1.0,
            'consistency_score': 1.0,
            'security_issues': []
        }

        # 1. Check if result exists
        if not result:
            logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED: Empty result")
            metrics['is_secure'] = False
            metrics['reliability_score'] = 0.0
            metrics['security_issues'].append('empty_result')
            return metrics

        # 2. Check for excessive result length (potential resource exhaustion)
        if len(result) > 50000:  # Reasonable limit
            logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED: Result too long ({len(result)} chars)")
            metrics['is_secure'] = False
            metrics['security_issues'].append('excessive_length')
            return metrics

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
            r"I don't have (?:access to|information about)",
            r"(?:fictional|imaginary|made up) (?:information|data|details)",
            r"I'm (?:hallucinating|inventing|creating) this",
            r"I (?:can't|cannot) (?:access|retrieve|find|obtain)",
        ]

        hallucination_count = 0
        for pattern in hallucination_patterns:
            if re.search(pattern, result, re.IGNORECASE):
                hallucination_count += 1
                logger.warning(f"⚠️ SECURITY WARNING: Hallucination indicator detected: '{pattern}'")
                metrics['security_issues'].append('hallucination')

        # Calculate hallucination penalty
        if hallucination_count > 0:
            hallucination_penalty = min(0.8, hallucination_count * 0.2)  # Cap at 0.8
            metrics['reliability_score'] -= hallucination_penalty

            if hallucination_count >= 3:  # Multiple strong indicators
                logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED: Multiple hallucination indicators detected")
                metrics['is_secure'] = False

        # 4. Enhanced check for refusal or inability to complete the operation
        refusal_patterns = [
            r"I (?:can't|cannot|am unable to) (?:assist|help|provide|complete|do) (?:that|this)",
            r"I'm (?:sorry|afraid) (?:but|that) I (?:can't|cannot|am unable to)",
            r"I'm not (?:able|allowed|permitted) to",
            r"(?:This|That) (?:goes|is) (?:against|beyond) my (?:capabilities|programming|abilities)",
            r"I (?:don't|do not) have (?:access|permission|authorization) to",
            r"(?:against|violates) (?:my|ethical) (?:guidelines|programming|protocols)",
            r"I (?:don't|do not) have the (?:capability|ability|authorization)",
        ]

        refusal_count = 0
        for pattern in refusal_patterns:
            if re.search(pattern, result, re.IGNORECASE):
                refusal_count += 1
                logger.warning(f"⚠️ SECURITY WARNING: Refusal indicator detected: '{pattern}'")
                metrics['security_issues'].append('refusal')

        # Calculate refusal penalty
        if refusal_count > 0:
            refusal_penalty = min(0.8, refusal_count * 0.2)  # Cap at 0.8
            metrics['reliability_score'] -= refusal_penalty

            if refusal_count >= 2:  # Multiple refusal indicators
                logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED: Expert refused or was unable to complete operation")
                metrics['is_secure'] = False

        # 5. Enhanced check for format compliance if output_format is specified
        if self.output_format:
            format_compliance = True

            # Basic format compliance checks based on output_format specification
            if "json" in self.output_format.lower():
                try:
                    # Try to parse as JSON
                    json.loads(result.strip())
                except:
                    format_compliance = False
                    logger.warning(f"⚠️ SECURITY WARNING: Format compliance check: Result not in valid JSON format")
                    metrics['security_issues'].append('format_noncompliance')

            elif "list" in self.output_format.lower() and not any(line.strip().startswith(('-', '*', '1.', '2.')) for line in result.split('\n')):
                format_compliance = False
                logger.warning(f"⚠️ SECURITY WARNING: Format compliance check: Result not in expected list format")
                metrics['security_issues'].append('format_noncompliance')

            elif "table" in self.output_format.lower() and not ('|' in result or '\t' in result):
                format_compliance = False
                logger.warning(f"⚠️ SECURITY WARNING: Format compliance check: Result not in expected table format")
                metrics['security_issues'].append('format_noncompliance')

            # Apply format compliance penalty
            if not format_compliance:
                metrics['reliability_score'] -= 0.3
                metrics['consistency_score'] -= 0.3

                # Only fail the check for severe format issues
                if "json" in self.output_format.lower() and not format_compliance:
                    logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED: Result not in required JSON format")
                    metrics['is_secure'] = False

        # 6. Enhanced check for relevance to the operation instructions
        key_terms = self._extract_key_terms(self.instructions)
        if key_terms:
            # Calculate relevance score based on key term coverage
            result_lower = result.lower()
            matched_terms = [term for term in key_terms if term.lower() in result_lower and len(term) > 4]

            if len(key_terms) > 0:
                relevance_score = len(matched_terms) / len(key_terms)
                metrics['relevance_score'] = relevance_score

                # Check if the instructions contain template variables
                has_template_vars = '{' in self.instructions and '}' in self.instructions

                # Apply relevance penalty - be extremely lenient with template variables
                if has_template_vars:
                    # For instructions with template variables, only log warnings but don't fail
                    if relevance_score < 0.1:  # Less than 10% of key terms found
                        logger.warning(f"⚠️ SECURITY WARNING: Relevance check: Result may have low relevance to template instructions (score: {relevance_score:.2f})")
                        # Apply a very small penalty
                        metrics['reliability_score'] -= 0.05
                        metrics['security_issues'].append('low_relevance_template')

                        # Only add a warning to the log, but don't fail the check
                        if relevance_score == 0:
                            logger.warning(f"⚠️ SECURITY WARNING: Relevance check: No key terms matched in template-based instructions")
                            # Still don't fail the check for template variables
                else:
                    # For regular instructions, use the original thresholds
                    if relevance_score < 0.3:  # Less than 30% of key terms found
                        logger.warning(f"⚠️ SECURITY WARNING: Relevance check: Result may not be relevant to instructions (score: {relevance_score:.2f})")
                        metrics['reliability_score'] -= (0.3 - relevance_score)
                        metrics['security_issues'].append('low_relevance')

                        if relevance_score < 0.1:  # Very low relevance
                            logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED: Result not relevant to instructions")
                            metrics['is_secure'] = False

        # 7. Enhanced check for potentially harmful or inappropriate content
        harmful_content_patterns = [
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

        for pattern in harmful_content_patterns:
            if re.search(pattern, result, re.IGNORECASE):
                logger.warning(f"⚠️ SECURITY WARNING: Content safety check: Potentially harmful content detected matching pattern: '{pattern}'")
                metrics['is_secure'] = False
                metrics['security_issues'].append('harmful_content')
                return metrics

        # 8. NEW: Check for output consistency and coherence
        # This is a simple implementation - a more robust one would use NLP techniques
        words = re.findall(r'\b\w+\b', result.lower())
        if len(words) > 20:  # Only check substantial outputs
            # Check for repetitive content which might indicate a stuck loop
            word_counts = Counter(words)
            most_common_words = word_counts.most_common(5)

            # If the most common word appears too frequently, it might indicate repetition
            if most_common_words[0][1] > len(words) * 0.2:  # More than 20% of all words
                logger.warning(f"⚠️ SECURITY WARNING: Consistency check: Detected potentially repetitive content")
                metrics['consistency_score'] -= 0.3
                metrics['security_issues'].append('repetitive_content')

            # Check for sentence repetition
            sentences = re.split(r'[.!?]\s+', result)
            if len(sentences) > 5:  # Only check outputs with multiple sentences
                sentence_counts = Counter(sentences)
                most_common_sentence = sentence_counts.most_common(1)[0]

                # If the same sentence appears multiple times, it might indicate a loop
                if most_common_sentence[1] > 2 and len(most_common_sentence[0].split()) > 5:
                    logger.warning(f"⚠️ SECURITY WARNING: Consistency check: Detected repeated sentences")
                    metrics['consistency_score'] -= 0.4
                    metrics['security_issues'].append('repeated_sentences')

                    if most_common_sentence[1] > 3:  # Severe repetition
                        logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED: Severe sentence repetition detected")
                        metrics['is_secure'] = False

        # Calculate final reliability score based on all factors
        metrics['reliability_score'] = max(0.0, min(1.0, metrics['reliability_score']))

        # Check if reliability score is below threshold
        if metrics['reliability_score'] < self.reliability_threshold:
            logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED: Reliability score ({metrics['reliability_score']:.2f}) below threshold ({self.reliability_threshold:.2f})")
            metrics['is_secure'] = False
            metrics['security_issues'].append('low_reliability')

        # All checks passed or failed
        if metrics['is_secure']:
            logger.debug(f"Operation post-execution security check PASSED for '{self.instructions[:50]}...' with reliability score {metrics['reliability_score']:.2f}")
        else:
            logger.warning(f"⚠️ SECURITY WARNING: Operation post-execution security check FAILED for '{self.instructions[:50]}...' with reliability score {metrics['reliability_score']:.2f}")

        return metrics

    def _extract_key_terms(self, text: str) -> list:
        """
        Extract key terms from text to check for relevance.
        This is a simple implementation that could be enhanced with NLP techniques.
        Handles template variables in the format {variable_name}.

        Args:
            text (str): The text to extract key terms from

        Returns:
            list: A list of key terms
        """
        # Remove common stop words
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when', 'at', 'from', 'by', 'for',
                     'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
                     'below', 'to', 'of', 'in', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
                     'here', 'there', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
                     'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
                     'just', 'don', 'should', 'now', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                     'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
                     'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                     'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
                     'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
                     'would', 'should', 'could', 'ought', 'i\'m', 'you\'re', 'he\'s', 'she\'s', 'it\'s', 'we\'re',
                     'they\'re', 'i\'ve', 'you\'ve', 'we\'ve', 'they\'ve', 'i\'d', 'you\'d', 'he\'d', 'she\'d',
                     'we\'d', 'they\'d', 'i\'ll', 'you\'ll', 'he\'ll', 'she\'ll', 'we\'ll', 'they\'ll', 'isn\'t',
                     'aren\'t', 'wasn\'t', 'weren\'t', 'hasn\'t', 'haven\'t', 'hadn\'t', 'doesn\'t', 'don\'t',
                     'didn\'t', 'won\'t', 'wouldn\'t', 'shan\'t', 'shouldn\'t', 'can\'t', 'cannot', 'couldn\'t',
                     'mustn\'t', 'let\'s', 'that\'s', 'who\'s', 'what\'s', 'here\'s', 'there\'s', 'when\'s',
                     'where\'s', 'why\'s', 'how\'s'}

        # Handle template variables - replace them with placeholder text
        # This ensures that instructions with template variables still have meaningful key terms
        processed_text = text
        template_vars = re.findall(r'\{([^{}]+)\}', text)

        # Add template variable names as key terms
        additional_terms = []
        for var in template_vars:
            # Remove any formatting instructions (e.g., "select, true:...")
            clean_var = var.split(',')[0].strip() if ',' in var else var.strip()
            if clean_var and len(clean_var) > 3 and clean_var.lower() not in stop_words:
                additional_terms.append(clean_var)

            # Replace the template variable with a generic term for text processing
            processed_text = processed_text.replace(f"{{{var}}}", f"variable_{clean_var}")

        # Split text into words, convert to lowercase, and filter out stop words and short words
        words = processed_text.lower().split()
        key_terms = [word.strip('.,;:!?()[]{}"\'-') for word in words
                    if word.strip('.,;:!?()[]{}"\'-').lower() not in stop_words
                    and len(word.strip('.,;:!?()[]{}"\'-')) > 3]

        # Add the template variable names to the key terms
        key_terms.extend(additional_terms)

        return key_terms

    def _save_result_to_destination(self, result: str, guardrails: Optional[Dict[str, Any]] = None) -> bool:
        """
        Saves the operation result to the specified destination.

        Args:
            result (str): The result to save
            guardrails (Optional[Dict[str, Any]]): The guardrails used during execution

        Returns:
            bool: True if the result was successfully saved, False otherwise
        """
        if not self.result_destination:
            return False

        try:
            # Determine the file format based on the extension
            file_extension = os.path.splitext(self.result_destination)[1].lower()

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(self.result_destination)), exist_ok=True)

            # Handle different file formats
            if file_extension in ['.txt', '.md', '.markdown']:
                # Plain text format
                with open(self.result_destination, 'w', encoding='utf-8') as f:
                    # Write header with metadata
                    f.write(f"# Operation Result\n\n")
                    f.write(f"## Operation Details\n")
                    f.write(f"- Instructions: {self.instructions[:100]}...\n")
                    f.write(f"- Expert: {self.expert.specialty if self.expert else 'Unassigned'}\n")
                    f.write(f"- Execution Time: {self.execution_metrics.get('execution_duration', 0):.2f} seconds\n\n")

                    # Write guardrails if available
                    if guardrails:
                        f.write(f"## Guardrail Inputs\n")
                        for key, value in guardrails.items():
                            f.write(f"- {key}: {value}\n")
                        f.write("\n")

                    # Write the result
                    f.write(f"## Result\n\n")
                    f.write(result)

            elif file_extension == '.csv':
                # CSV format
                import csv
                with open(self.result_destination, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Write header row
                    writer.writerow(['Operation', 'Expert', 'Execution Time', 'Result'])
                    # Write data row
                    writer.writerow([
                        self.instructions[:100] + '...',
                        self.expert.specialty if self.expert else 'Unassigned',
                        f"{self.execution_metrics.get('execution_duration', 0):.2f}s",
                        result
                    ])

            elif file_extension == '.json':
                # JSON format
                import json
                data = {
                    'operation': {
                        'instructions': self.instructions,
                        'expert': self.expert.specialty if self.expert else 'Unassigned',
                        'output_format': self.output_format,
                    },
                    'execution_metrics': self.execution_metrics,
                    'guardrails': guardrails,
                    'result': result
                }
                with open(self.result_destination, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)

            elif file_extension == '.html':
                # HTML format - create a simple HTML file with the result
                # Prepare the data
                instructions_preview = self.instructions[:100] + "..." if len(self.instructions) > 100 else self.instructions
                expert_name = self.expert.specialty if self.expert else 'Unassigned'
                execution_time = f"{self.execution_metrics.get('execution_duration', 0):.2f}"

                # Create HTML content manually without using format or f-strings
                html_content = "<!DOCTYPE html>\n"
                html_content += "<html>\n"
                html_content += "<head>\n"
                html_content += "    <title>Operation Result</title>\n"
                html_content += "    <style>\n"
                html_content += "        body { font-family: Arial, sans-serif; margin: 20px; }\n"
                html_content += "        h1, h2 { color: #333; }\n"
                html_content += "        .metadata { background-color: #f5f5f5; padding: 10px; border-radius: 5px; }\n"
                html_content += "        .result { margin-top: 20px; }\n"
                html_content += "    </style>\n"
                html_content += "</head>\n"
                html_content += "<body>\n"
                html_content += "    <h1>Operation Result</h1>\n\n"
                html_content += "    <div class=\"metadata\">\n"
                html_content += "        <h2>Operation Details</h2>\n"
                html_content += "        <p><strong>Instructions:</strong> " + instructions_preview + "</p>\n"
                html_content += "        <p><strong>Expert:</strong> " + expert_name + "</p>\n"
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

                with open(self.result_destination, 'w', encoding='utf-8') as f:
                    f.write(html_content)

            elif file_extension == '.pdf':
                # PDF format (requires reportlab)
                try:
                    from reportlab.lib.pagesizes import letter
                    from reportlab.lib import colors
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.styles import getSampleStyleSheet

                    doc = SimpleDocTemplate(self.result_destination, pagesize=letter)
                    styles = getSampleStyleSheet()
                    elements = []

                    # Title
                    elements.append(Paragraph("Operation Result", styles['Title']))
                    elements.append(Spacer(1, 12))

                    # Operation Details
                    elements.append(Paragraph("Operation Details", styles['Heading2']))
                    elements.append(Paragraph(f"<b>Instructions:</b> {self.instructions[:100]}...", styles['Normal']))
                    elements.append(Paragraph(f"<b>Expert:</b> {self.expert.specialty if self.expert else 'Unassigned'}", styles['Normal']))
                    elements.append(Paragraph(f"<b>Execution Time:</b> {self.execution_metrics.get('execution_duration', 0):.2f} seconds", styles['Normal']))
                    elements.append(Spacer(1, 12))

                    # Guardrails
                    if guardrails:
                        elements.append(Paragraph("Guardrail Inputs", styles['Heading2']))
                        for key, value in guardrails.items():
                            elements.append(Paragraph(f"<b>{key}:</b> {value}", styles['Normal']))
                        elements.append(Spacer(1, 12))

                    # Result
                    elements.append(Paragraph("Result", styles['Heading2']))
                    elements.append(Paragraph(result.replace('\n', '<br/>'), styles['Normal']))

                    # Build the PDF
                    doc.build(elements)
                except ImportError:
                    logger.warning("reportlab package not installed. Saving result as text file instead.")
                    # Fall back to text file
                    with open(self.result_destination.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
                        f.write(f"# Operation Result\n\n")
                        f.write(f"## Operation Details\n")
                        f.write(f"- Instructions: {self.instructions[:100]}...\n")
                        f.write(f"- Expert: {self.expert.specialty if self.expert else 'Unassigned'}\n")
                        f.write(f"- Execution Time: {self.execution_metrics.get('execution_duration', 0):.2f} seconds\n\n")
                        if guardrails:
                            f.write(f"## Guardrail Inputs\n")
                            for key, value in guardrails.items():
                                f.write(f"- {key}: {value}\n")
                            f.write("\n")
                        f.write(f"## Result\n\n")
                        f.write(result)
            else:
                # Default to text file for unknown extensions
                with open(self.result_destination, 'w', encoding='utf-8') as f:
                    f.write(result)

            logger.info(f"Operation result saved to {self.result_destination}")
            return True

        except Exception as e:
            logger.error(f"Error saving operation result to {self.result_destination}: {e}", exc_info=True)
            return False

    def _prepare_context_with_guardrails(self, original_context: Optional[str], guardrails: Dict[str, Any]) -> str:
        # Prepares the context by incorporating guardrail inputs
        # original_context: The original context for the operation
        # guardrails: The guardrail inputs to incorporate
        # Returns: Enhanced context with guardrail inputs
        if not guardrails:
            return original_context or ""

        # Start with the original context
        enhanced_context = original_context or ""

        # Add guardrails section if we have guardrails
        if guardrails:
            # Add a separator if we already have context
            if enhanced_context:
                enhanced_context += "\n\n"

            # Add guardrails section header
            enhanced_context += "GUARDRAILS AND DYNAMIC INPUTS:\n"

            # Add each guardrail as a key-value pair
            for key, value in guardrails.items():
                # Format the value based on its type
                if isinstance(value, (dict, list)):
                    # For complex types, format as JSON
                    try:
                        formatted_value = json.dumps(value, indent=2)
                        enhanced_context += f"{key}: {formatted_value}\n"
                    except:
                        # Fallback for non-serializable objects
                        enhanced_context += f"{key}: {str(value)}\n"
                else:
                    # For simple types, just convert to string
                    enhanced_context += f"{key}: {str(value)}\n"

            # Add a note about how to use the guardrails
            enhanced_context += "\nPlease incorporate these guardrails and inputs into your response as appropriate."

        logger.debug(f"Enhanced context with {len(guardrails)} guardrail inputs")
        return enhanced_context

    def __str__(self):
        return f"Operation(instructions='{self.instructions}', expert='{self.expert.specialty if self.expert else 'Unassigned'}')"
