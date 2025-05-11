#!/usr/bin/env python3
"""
Performance Test Script

This script tests the performance of the TBH Secure Agents framework with different security profiles.
It measures the execution time of security validations and other operations.
"""

import os
import sys
import time
import logging
import statistics
from typing import List, Dict, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_profiles import SecurityProfile, clear_caches

# Get API key from environment variable or use a default one for testing
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyDYGDWiED84ZAL71xbT3QDBfUnCTrIPvpc")

def time_execution(func, *args, **kwargs) -> Tuple[Any, float]:
    """
    Measure the execution time of a function.
    
    Args:
        func: The function to measure
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Tuple of (result, execution_time)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def create_test_expert(security_profile: str) -> Expert:
    """
    Create a test expert with the specified security profile.
    
    Args:
        security_profile: The security profile to use
        
    Returns:
        Expert instance
    """
    return Expert(
        specialty="Performance Tester",
        objective="Test framework performance",
        background="Expert in performance testing",
        security_profile=security_profile,
        api_key=API_KEY
    )

def create_test_operation(length: int = 1000) -> Operation:
    """
    Create a test operation with instructions of the specified length.
    
    Args:
        length: The approximate length of the instructions
        
    Returns:
        Operation instance
    """
    # Create instructions of approximately the specified length
    base_instruction = "Analyze the performance of the system and provide recommendations for improvement. "
    instructions = base_instruction * (length // len(base_instruction) + 1)
    instructions = instructions[:length]
    
    return Operation(
        instructions=instructions
    )

def test_security_profile_performance(profile: str, num_operations: int = 5, instruction_length: int = 1000) -> Dict[str, float]:
    """
    Test the performance of a specific security profile.
    
    Args:
        profile: The security profile to test
        num_operations: The number of operations to create
        instruction_length: The length of each operation's instructions
        
    Returns:
        Dictionary of performance metrics
    """
    logger.info(f"Testing {profile.upper()} security profile with {num_operations} operations")
    
    # Clear caches before each test
    clear_caches()
    
    # Create expert
    expert = create_test_expert(profile)
    
    # Create operations
    operations = []
    operation_creation_times = []
    
    for i in range(num_operations):
        operation, creation_time = time_execution(create_test_operation, instruction_length)
        operation.expert = expert
        operations.append(operation)
        operation_creation_times.append(creation_time)
    
    # Create squad
    squad, squad_creation_time = time_execution(
        Squad,
        experts=[expert],
        operations=operations,
        process="sequential",
        security_level=profile
    )
    
    # Validate squad security
    _, squad_validation_time = time_execution(squad._validate_squad_security)
    
    # Validate each operation
    operation_validation_times = []
    for i, operation in enumerate(operations):
        _, validation_time = time_execution(squad._validate_operation_security, operation, i)
        operation_validation_times.append(validation_time)
    
    # Calculate metrics
    metrics = {
        "profile": profile,
        "num_operations": num_operations,
        "instruction_length": instruction_length,
        "avg_operation_creation_time": statistics.mean(operation_creation_times),
        "squad_creation_time": squad_creation_time,
        "squad_validation_time": squad_validation_time,
        "avg_operation_validation_time": statistics.mean(operation_validation_times),
        "total_validation_time": squad_validation_time + sum(operation_validation_times),
    }
    
    logger.info(f"Results for {profile.upper()} profile:")
    logger.info(f"  Squad validation time: {metrics['squad_validation_time']:.6f} seconds")
    logger.info(f"  Average operation validation time: {metrics['avg_operation_validation_time']:.6f} seconds")
    logger.info(f"  Total validation time: {metrics['total_validation_time']:.6f} seconds")
    
    return metrics

def run_performance_tests() -> List[Dict[str, float]]:
    """
    Run performance tests for all security profiles.
    
    Returns:
        List of performance metrics for each profile
    """
    profiles = ["minimal", "low", "standard", "high", "maximum"]
    results = []
    
    for profile in profiles:
        # Test with 5 operations of 1000 characters each
        metrics = test_security_profile_performance(profile, num_operations=5, instruction_length=1000)
        results.append(metrics)
    
    return results

def print_performance_comparison(results: List[Dict[str, float]]) -> None:
    """
    Print a comparison of performance metrics for different security profiles.
    
    Args:
        results: List of performance metrics for each profile
    """
    print("\nPerformance Comparison")
    print("=" * 80)
    print(f"{'Profile':<10} {'Squad Validation':<20} {'Avg Op Validation':<20} {'Total Validation':<20}")
    print("-" * 80)
    
    for metrics in results:
        profile = metrics["profile"].upper()
        squad_time = f"{metrics['squad_validation_time']:.6f}s"
        op_time = f"{metrics['avg_operation_validation_time']:.6f}s"
        total_time = f"{metrics['total_validation_time']:.6f}s"
        
        print(f"{profile:<10} {squad_time:<20} {op_time:<20} {total_time:<20}")
    
    # Calculate speedup relative to maximum security
    max_metrics = next(m for m in results if m["profile"] == "maximum")
    min_metrics = next(m for m in results if m["profile"] == "minimal")
    
    speedup = max_metrics["total_validation_time"] / min_metrics["total_validation_time"]
    print("-" * 80)
    print(f"Speedup from MAXIMUM to MINIMAL: {speedup:.2f}x")
    print("=" * 80)

def main():
    """Run the performance tests."""
    print("TBH Secure Agents - Performance Test")
    print("=" * 50)
    
    # Run performance tests
    results = run_performance_tests()
    
    # Print comparison
    print_performance_comparison(results)
    
    print("\nPerformance test completed.")

if __name__ == "__main__":
    main()
