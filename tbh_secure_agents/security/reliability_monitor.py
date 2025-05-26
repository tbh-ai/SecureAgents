"""
Reliability Monitoring System

This module provides tools for monitoring and ensuring the reliability of multi-agent systems,
including consistency checking, output validation, and execution monitoring.
"""

import logging
import time
import re
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import Counter

logger = logging.getLogger(__name__)

class ReliabilityMonitor:
    """
    System for monitoring and ensuring the reliability of multi-agent operations.
    Detects inconsistencies, validates outputs, and monitors execution patterns.
    """

    def __init__(self, security_level: str = "high"):
        """
        Initialize the ReliabilityMonitor with the specified security level.

        Args:
            security_level (str): The security level to use ('standard', 'high', or 'maximum')
        """
        self.security_level = security_level

        # Initialize monitoring systems
        self.execution_history = []
        self.reliability_metrics = {}

        # Initialize detection thresholds based on security level
        self._initialize_thresholds()

        logger.debug(f"ReliabilityMonitor initialized with security level: {security_level}")

    def _initialize_thresholds(self) -> None:
        """Initialize detection thresholds based on security level."""
        # Define thresholds for all security profiles
        profile_thresholds = {
            'minimal': {
                'consistency_threshold': 0.3,  # Very permissive for development
                'hallucination_threshold': 0.8,  # Allow more hallucinations
                'repetition_threshold': 0.5,  # Allow more repetition
                'contradiction_threshold': 0.5,  # Allow more contradictions
                'execution_time_threshold': 600,  # Longer execution time allowed
                'output_length_threshold': 500000,  # Very large output allowed
                'error_rate_threshold': 0.5,  # Higher error rate allowed
            },
            'low': {
                'consistency_threshold': 0.5,  # Permissive consistency
                'hallucination_threshold': 0.5,  # Moderate hallucination tolerance
                'repetition_threshold': 0.3,  # Moderate repetition tolerance
                'contradiction_threshold': 0.3,  # Moderate contradiction tolerance
                'execution_time_threshold': 450,  # Moderate execution time
                'output_length_threshold': 300000,  # Large output allowed
                'error_rate_threshold': 0.3,  # Moderate error rate
            },
            'standard': {
                'consistency_threshold': 0.7,  # Standard consistency requirement
                'hallucination_threshold': 0.3,  # Standard hallucination tolerance
                'repetition_threshold': 0.2,  # Standard repetition tolerance
                'contradiction_threshold': 0.2,  # Standard contradiction tolerance
                'execution_time_threshold': 300,  # Standard execution time
                'output_length_threshold': 100000,  # Standard output length
                'error_rate_threshold': 0.2,  # Standard error rate
            },
            'high': {
                'consistency_threshold': 0.8,  # High consistency requirement
                'hallucination_threshold': 0.2,  # Low hallucination tolerance
                'repetition_threshold': 0.15,  # Low repetition tolerance
                'contradiction_threshold': 0.15,  # Low contradiction tolerance
                'execution_time_threshold': 180,  # Shorter execution time
                'output_length_threshold': 50000,  # Smaller output length
                'error_rate_threshold': 0.15,  # Lower error rate
            },
            'maximum': {
                'consistency_threshold': 0.9,  # Very high consistency requirement
                'hallucination_threshold': 0.1,  # Very low hallucination tolerance
                'repetition_threshold': 0.1,  # Very low repetition tolerance
                'contradiction_threshold': 0.1,  # Very low contradiction tolerance
                'execution_time_threshold': 120,  # Very short execution time
                'output_length_threshold': 25000,  # Very small output length
                'error_rate_threshold': 0.1,  # Very low error rate
            }
        }

        # Set thresholds based on security level
        self.thresholds = profile_thresholds.get(self.security_level, profile_thresholds['standard'])

    def monitor_execution(self, operation_id: str, operation_type: str,
                         inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start monitoring an operation execution.

        Args:
            operation_id (str): Unique identifier for the operation
            operation_type (str): Type of operation being executed
            inputs (Dict[str, Any]): Input parameters for the operation

        Returns:
            Dict[str, Any]: Execution context with monitoring metadata
        """
        # Create execution context
        context = {
            'operation_id': operation_id,
            'operation_type': operation_type,
            'inputs': inputs,
            'start_time': time.time(),
            'status': 'running',
            'checkpoints': [],
            'errors': [],
            'warnings': [],
        }

        # Add to execution history
        self.execution_history.append(context)

        logger.debug(f"Started monitoring execution of operation '{operation_id}' of type '{operation_type}'")
        return context

    def record_checkpoint(self, operation_id: str, checkpoint_name: str,
                         data: Dict[str, Any]) -> None:
        """
        Record a checkpoint during operation execution.

        Args:
            operation_id (str): The operation ID
            checkpoint_name (str): Name of the checkpoint
            data (Dict[str, Any]): Data to record at this checkpoint
        """
        # Find the execution context
        context = self._get_execution_context(operation_id)
        if not context:
            logger.warning(f"Cannot record checkpoint: No execution context found for operation '{operation_id}'")
            return

        # Add checkpoint
        checkpoint = {
            'name': checkpoint_name,
            'timestamp': time.time(),
            'data': data,
            'elapsed_time': time.time() - context['start_time'],
        }

        context['checkpoints'].append(checkpoint)
        logger.debug(f"Recorded checkpoint '{checkpoint_name}' for operation '{operation_id}'")

    def record_error(self, operation_id: str, error_type: str,
                    error_message: str, error_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Record an error during operation execution.

        Args:
            operation_id (str): The operation ID
            error_type (str): Type of error
            error_message (str): Error message
            error_data (Optional[Dict[str, Any]]): Additional error data
        """
        # Find the execution context
        context = self._get_execution_context(operation_id)
        if not context:
            logger.warning(f"Cannot record error: No execution context found for operation '{operation_id}'")
            return

        # Add error
        error = {
            'type': error_type,
            'message': error_message,
            'timestamp': time.time(),
            'data': error_data or {},
            'elapsed_time': time.time() - context['start_time'],
        }

        context['errors'].append(error)
        logger.warning(f"Recorded error '{error_type}' for operation '{operation_id}': {error_message}")

    def complete_execution(self, operation_id: str, output: Any,
                          metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Complete an operation execution and analyze results.

        Args:
            operation_id (str): The operation ID
            output: The operation output
            metadata (Optional[Dict[str, Any]]): Additional metadata about the execution

        Returns:
            Dict[str, Any]: Reliability analysis of the execution
        """
        # Find the execution context
        context = self._get_execution_context(operation_id)
        if not context:
            logger.warning(f"Cannot complete execution: No execution context found for operation '{operation_id}'")
            return {'is_reliable': False, 'error': 'No execution context found'}

        # Update context
        context['end_time'] = time.time()
        context['execution_time'] = context['end_time'] - context['start_time']
        context['output'] = output
        context['metadata'] = metadata or {}
        context['status'] = 'completed'

        # Analyze reliability
        reliability_analysis = self.analyze_reliability(operation_id)

        # Store analysis in context
        context['reliability_analysis'] = reliability_analysis

        logger.debug(f"Completed execution of operation '{operation_id}' in {context['execution_time']:.2f}s with reliability score {reliability_analysis['reliability_score']:.2f}")
        return reliability_analysis

    def analyze_reliability(self, operation_id: str) -> Dict[str, Any]:
        """
        Analyze the reliability of an operation execution.

        Args:
            operation_id (str): The operation ID

        Returns:
            Dict[str, Any]: Reliability analysis results
        """
        # Find the execution context
        context = self._get_execution_context(operation_id)
        if not context:
            logger.warning(f"Cannot analyze reliability: No execution context found for operation '{operation_id}'")
            return {'is_reliable': False, 'error': 'No execution context found', 'reliability_score': 0.0}

        # Initialize analysis
        analysis = {
            'is_reliable': True,
            'reliability_score': 1.0,  # Start with perfect score and deduct for issues
            'issues': [],
            'warnings': [],
            'metrics': {},
        }

        # Check execution time
        if 'execution_time' in context:
            execution_time = context['execution_time']
            analysis['metrics']['execution_time'] = execution_time

            if execution_time > self.thresholds['execution_time_threshold']:
                analysis['is_reliable'] = False
                analysis['reliability_score'] -= min(0.3, (execution_time - self.thresholds['execution_time_threshold']) / 300)
                analysis['issues'].append(f"Execution time ({execution_time:.2f}s) exceeds threshold ({self.thresholds['execution_time_threshold']}s)")

        # Check for errors
        if 'errors' in context and context['errors']:
            error_count = len(context['errors'])
            analysis['metrics']['error_count'] = error_count

            if error_count > 0:
                analysis['reliability_score'] -= min(0.5, error_count * 0.1)
                analysis['issues'].append(f"Operation encountered {error_count} errors")

                # Include the most recent error in the analysis
                latest_error = context['errors'][-1]
                analysis['issues'].append(f"Latest error: {latest_error['type']} - {latest_error['message']}")

        # Check output if available
        if 'output' in context and isinstance(context['output'], str):
            output = context['output']

            # Check output length
            output_length = len(output)
            analysis['metrics']['output_length'] = output_length

            if output_length > self.thresholds['output_length_threshold']:
                analysis['reliability_score'] -= min(0.2, (output_length - self.thresholds['output_length_threshold']) / 10000)
                analysis['warnings'].append(f"Output length ({output_length} chars) exceeds threshold ({self.thresholds['output_length_threshold']} chars)")

            # Check for repetition
            repetition_score = self._check_repetition(output)
            analysis['metrics']['repetition_score'] = repetition_score

            if repetition_score > self.thresholds['repetition_threshold']:
                analysis['reliability_score'] -= min(0.3, repetition_score)
                analysis['issues'].append(f"Output contains significant repetition (score: {repetition_score:.2f})")

            # Check for consistency with inputs
            if 'inputs' in context and isinstance(context['inputs'], dict):
                consistency_score = self._check_consistency(output, context['inputs'])
                analysis['metrics']['consistency_score'] = consistency_score

                if consistency_score < self.thresholds['consistency_threshold']:
                    analysis['reliability_score'] -= min(0.4, 1.0 - consistency_score)
                    analysis['issues'].append(f"Output lacks consistency with inputs (score: {consistency_score:.2f})")

        # Ensure reliability score is within bounds
        analysis['reliability_score'] = max(0.0, min(1.0, analysis['reliability_score']))

        # Final reliability determination
        if analysis['reliability_score'] < 0.6:
            analysis['is_reliable'] = False

        return analysis

    def _check_repetition(self, text: str) -> float:
        """
        Check for repetitive content in text.

        Args:
            text (str): The text to analyze

        Returns:
            float: Repetition score (0.0-1.0, higher is more repetitive)
        """
        if not text or len(text) < 50:
            return 0.0

        # Split into sentences
        sentences = re.split(r'[.!?]\s+', text)

        # Count sentence occurrences
        sentence_counts = Counter(sentences)

        # Find the most common sentence and its count
        most_common_sentence = sentence_counts.most_common(1)[0] if sentence_counts else (None, 0)

        # Calculate repetition score
        if most_common_sentence[1] > 1 and len(sentences) > 3:
            repetition_score = most_common_sentence[1] / len(sentences)
            return min(1.0, repetition_score * 2)  # Scale up for sensitivity

        # Check for repeated phrases (n-grams)
        repetition_score = self._check_ngram_repetition(text)

        return repetition_score

    def _check_ngram_repetition(self, text: str) -> float:
        """
        Check for repetitive phrases (n-grams) in text.

        Args:
            text (str): The text to analyze

        Returns:
            float: Repetition score (0.0-1.0, higher is more repetitive)
        """
        words = text.split()
        if len(words) < 10:
            return 0.0

        # Check for repeated 3-grams, 4-grams, and 5-grams
        ngram_scores = []

        for n in [3, 4, 5]:
            if len(words) < n * 2:
                continue

            ngrams = [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]
            ngram_counts = Counter(ngrams)

            # Find the most common n-gram and its count
            most_common = ngram_counts.most_common(1)[0] if ngram_counts else (None, 0)

            if most_common[1] > 1:
                # Calculate score based on frequency and coverage
                frequency = most_common[1] / len(ngrams)
                coverage = (most_common[1] * n) / len(words)
                ngram_scores.append((frequency + coverage) / 2)

        return max(ngram_scores) if ngram_scores else 0.0

    def _check_consistency(self, output: str, inputs: Dict[str, Any]) -> float:
        """
        Check consistency between output and inputs.

        Args:
            output (str): The operation output
            inputs (Dict[str, Any]): The operation inputs

        Returns:
            float: Consistency score (0.0-1.0, higher is more consistent)
        """
        # Extract key terms from inputs
        input_terms = self._extract_key_terms(inputs)

        # Check if key terms from inputs appear in the output
        if not input_terms:
            return 1.0  # No terms to check

        # Count how many input terms appear in the output
        output_lower = output.lower()
        matched_terms = sum(1 for term in input_terms if term.lower() in output_lower)

        # Calculate consistency score
        consistency_score = matched_terms / len(input_terms) if input_terms else 1.0

        return consistency_score

    def _extract_key_terms(self, inputs: Dict[str, Any]) -> List[str]:
        """
        Extract key terms from input data.

        Args:
            inputs (Dict[str, Any]): The input data

        Returns:
            List[str]: List of key terms
        """
        key_terms = []

        # Process string inputs
        for key, value in inputs.items():
            if isinstance(value, str) and len(value) > 3:
                # Extract potential key terms (nouns, proper nouns, etc.)
                # In a real implementation, this would use NLP techniques
                words = re.findall(r'\b[A-Za-z][A-Za-z0-9_]{2,}\b', value)
                key_terms.extend(words)
            elif isinstance(value, dict):
                # Recursively process nested dictionaries
                key_terms.extend(self._extract_key_terms(value))
            elif isinstance(value, list):
                # Process list items
                for item in value:
                    if isinstance(item, str) and len(item) > 3:
                        words = re.findall(r'\b[A-Za-z][A-Za-z0-9_]{2,}\b', item)
                        key_terms.extend(words)
                    elif isinstance(item, dict):
                        key_terms.extend(self._extract_key_terms(item))

        # Remove duplicates while preserving order
        unique_terms = []
        seen = set()
        for term in key_terms:
            if term.lower() not in seen:
                seen.add(term.lower())
                unique_terms.append(term)

        return unique_terms

    def _get_execution_context(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the execution context for an operation.

        Args:
            operation_id (str): The operation ID

        Returns:
            Optional[Dict[str, Any]]: The execution context, or None if not found
        """
        for context in self.execution_history:
            if context['operation_id'] == operation_id:
                return context
        return None

    def get_reliability_report(self, time_period: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive reliability report for all monitored operations.

        Args:
            time_period (Optional[float]): Time period in seconds to include in the report (None for all)

        Returns:
            Dict[str, Any]: Reliability report
        """
        # Filter operations by time period if specified
        operations = self.execution_history
        if time_period is not None:
            current_time = time.time()
            operations = [op for op in operations if current_time - op.get('start_time', 0) <= time_period]

        # Count operations by status
        status_counts = {}
        for op in operations:
            status = op.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1

        # Calculate reliability metrics
        completed_ops = [op for op in operations if op.get('status') == 'completed']
        reliability_scores = [op.get('reliability_analysis', {}).get('reliability_score', 0.0)
                             for op in completed_ops if 'reliability_analysis' in op]

        avg_reliability = sum(reliability_scores) / len(reliability_scores) if reliability_scores else 0.0

        # Count issues by type
        issue_counts = {}
        for op in completed_ops:
            if 'reliability_analysis' in op and 'issues' in op['reliability_analysis']:
                for issue in op['reliability_analysis']['issues']:
                    # Extract issue type from the message
                    issue_type = issue.split(':')[0] if ':' in issue else issue
                    issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1

        # Generate report
        report = {
            'total_operations': len(operations),
            'status_counts': status_counts,
            'average_reliability_score': avg_reliability,
            'reliable_operations': sum(1 for op in completed_ops
                                     if op.get('reliability_analysis', {}).get('is_reliable', False)),
            'unreliable_operations': sum(1 for op in completed_ops
                                       if not op.get('reliability_analysis', {}).get('is_reliable', True)),
            'common_issues': issue_counts,
            'security_level': self.security_level,
            'timestamp': time.time()
        }

        return report

    def get_operation_history(self, operation_id: Optional[str] = None,
                             limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the execution history for operations.

        Args:
            operation_id (Optional[str]): Specific operation ID to retrieve, or None for all
            limit (int): Maximum number of operations to return

        Returns:
            List[Dict[str, Any]]: List of operation execution records
        """
        if operation_id:
            # Return specific operation
            context = self._get_execution_context(operation_id)
            return [context] if context else []
        else:
            # Return recent operations, most recent first
            sorted_history = sorted(self.execution_history,
                                   key=lambda x: x.get('end_time', x.get('start_time', 0)),
                                   reverse=True)
            return sorted_history[:limit]

    def clear_history(self, older_than: Optional[float] = None) -> int:
        """
        Clear execution history.

        Args:
            older_than (Optional[float]): Clear only operations older than this many seconds

        Returns:
            int: Number of operations cleared
        """
        if older_than is None:
            # Clear all history
            count = len(self.execution_history)
            self.execution_history = []
            return count
        else:
            # Clear only older operations
            current_time = time.time()
            original_count = len(self.execution_history)
            self.execution_history = [op for op in self.execution_history
                                     if current_time - op.get('start_time', 0) <= older_than]
            return original_count - len(self.execution_history)