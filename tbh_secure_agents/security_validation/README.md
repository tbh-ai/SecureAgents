# Hybrid Security Validation System

This package provides a sophisticated hybrid approach to security validation for the TBH Secure Agents framework. It combines regex pattern matching, machine learning, and large language models to provide comprehensive security validation with an optimal user experience.

## Key Features

- **Hybrid Validation**: Combines multiple validation approaches for robust security
- **Progressive Validation**: Starts with fast checks and only uses more sophisticated methods when necessary
- **UX-Optimized**: Provides clear feedback and suggestions for fixing security issues
- **Configurable Security Levels**: Supports different security levels with appropriate validation methods
- **Performance Optimized**: Uses caching and early returns for optimal performance
- **Easy Integration**: Seamlessly integrates with the existing framework
- **Content Complexity Analysis**: Automatically detects complex content that might require deeper analysis
- **Visualization Tools**: Provides tools for visualizing the validation process and results
- **Advanced ML Model**: Uses a sophisticated machine learning model trained on diverse security examples
- **Enhanced LLM Integration**: Uses advanced prompting techniques for better security analysis

## Components

### Validators

- **RegexValidator**: Fast pattern-based validation for known security issues
- **MLValidator**: Machine learning-based validation for detecting novel threats
- **LLMValidator**: LLM-based validation for complex semantic understanding
- **HybridValidator**: Combines all approaches for comprehensive validation with intelligent routing

### User Interface

- **SecurityUI**: Provides a user-friendly interface for security validation
  - Progress indicators
  - Colorized output
  - Interactive fix suggestions
  - Detailed validation reports

### Visualization

- **ValidationVisualizer**: Visualizes the validation process and results
  - Validation flow diagrams
  - Performance metrics reports
  - JSON export for further analysis

### ML Model Training

- **SecurityDatasetGenerator**: Generates diverse datasets for model training
- **SecurityModelTrainer**: Trains and evaluates ML models for security validation

### Integration

- **SecurityValidator**: Main interface for security validation
- **Integration Functions**: Easy integration with the existing framework

## Security Levels

The hybrid validation approach supports different security levels:

- **Minimal**: Basic security checks only, allows most operations to run
- **Standard**: Balanced security and usability, uses regex and ML validation
- **High**: Enhanced security checks, uses regex, ML, and LLM validation
- **Maximum**: Maximum security protection, uses all available validation methods with strict thresholds

## Usage

### Basic Usage

```python
from tbh_secure_agents.security_validation import SecurityValidator

# Create a security validator
validator = SecurityValidator(api_key="your-llm-api-key")

# Validate a prompt
is_secure, error_details = validator.validate_prompt(
    "Use system('rm -rf /tmp/data') to clean up temporary files",
    security_level="standard"
)

if not is_secure:
    print(f"Security validation failed: {error_details['error_message']}")
    print(f"Suggestion: {error_details['suggestions'][0]}")
```

### Advanced Usage with Visualization

```python
from tbh_secure_agents.security_validation import SecurityValidator
from tbh_secure_agents.security_validation.utils import ValidationVisualizer

# Create a security validator
validator = SecurityValidator(api_key="your-llm-api-key")

# Create a visualizer
visualizer = ValidationVisualizer(output_dir="validation_visualizations")

# Validate a prompt
is_secure, error_details = validator.validate_prompt(
    "Use system('rm -rf /tmp/data') to clean up temporary files",
    security_level="high"
)

# Get the raw validation result
result = validator.validator.validate(
    "Use system('rm -rf /tmp/data') to clean up temporary files",
    {"security_level": "high"}
)

# Visualize the validation flow
flow_diagram = visualizer.visualize_validation_flow(result, "validation_flow.md")
print(f"Validation flow diagram saved to: {flow_diagram}")

# Collect multiple results for performance analysis
results = []
for i in range(5):
    result = validator.validator.validate(
        f"Example text {i}",
        {"security_level": "standard"}
    )
    results.append(result)

# Visualize performance metrics
metrics_report = visualizer.visualize_performance_metrics(results, "performance_metrics.md")
print(f"Performance metrics report saved to: {metrics_report}")
```

### Integration with the Framework

```python
from tbh_secure_agents.agent import Expert
from tbh_secure_agents.task import Operation
from tbh_secure_agents.crew import Squad
from tbh_secure_agents.security_validation import enable_hybrid_validation

# Enable hybrid validation with API key
enable_hybrid_validation(api_key="your-llm-api-key")

# Create an expert with standard security profile
expert = Expert(
    specialty="Data Analyst",
    objective="Analyze customer data",
    security_profile="standard"
)

# Create an operation
operation = Operation(
    instructions="Process the customer data and generate insights",
    expert=expert
)

# Create a squad
squad = Squad(
    experts=[expert],
    operations=[operation],
    process="sequential"
)

# Deploy the squad
result = squad.deploy()
```

### Training and Using a Custom ML Model

```python
import os
from tbh_secure_agents.security_validation.models import generate_security_dataset, train_security_model

# Generate a dataset
dataset_path = "security_dataset.json"
generate_security_dataset.main([
    "--output", dataset_path,
    "--command-injection", "100",
    "--prompt-injection", "100",
    "--data-exfiltration", "100",
    "--privilege-escalation", "100",
    "--denial-of-service", "100",
    "--secure", "500"
])

# Train a model
model_dir = "security_models"
os.makedirs(model_dir, exist_ok=True)
train_security_model.main([
    "--dataset", dataset_path,
    "--model-type", "random_forest",
    "--output-dir", model_dir
])

# Use the custom model
from tbh_secure_agents.security_validation import SecurityValidator
from tbh_secure_agents.security_validation.validators import MLValidator

# Create a custom ML validator with the trained model
ml_validator = MLValidator(model_path=f"{model_dir}/security_model.pkl")

# Create a security validator with the custom ML validator
validator = SecurityValidator(ml_validator=ml_validator)

# Validate a prompt
is_secure, error_details = validator.validate_prompt(
    "Your prompt text here",
    security_level="standard"
)
```

## Testing

The package includes a comprehensive test suite with multiple test scripts:

### Basic Testing

```bash
# Run the basic test script
python -m tbh_secure_agents.security_validation.tests.test_hybrid_validation

# Run with specific test
python -m tbh_secure_agents.security_validation.tests.test_hybrid_validation --test levels
python -m tbh_secure_agents.security_validation.tests.test_hybrid_validation --test content
python -m tbh_secure_agents.security_validation.tests.test_hybrid_validation --test performance

# Run in non-interactive mode
python -m tbh_secure_agents.security_validation.tests.test_hybrid_validation --non-interactive
```

### Advanced Testing

```bash
# Run the advanced test script
python -m tbh_secure_agents.security_validation.tests.test_advanced_validation

# Run with specific test
python -m tbh_secure_agents.security_validation.tests.test_advanced_validation --test prompt
python -m tbh_secure_agents.security_validation.tests.test_advanced_validation --test data
python -m tbh_secure_agents.security_validation.tests.test_advanced_validation --test command
python -m tbh_secure_agents.security_validation.tests.test_advanced_validation --test complex

# Run with API key
python -m tbh_secure_agents.security_validation.tests.test_advanced_validation --api-key YOUR_API_KEY
```

### Visualization Testing

```bash
# Run the visualization test script
python -m tbh_secure_agents.security_validation.tests.test_visualization

# Run with specific test
python -m tbh_secure_agents.security_validation.tests.test_visualization --test flow
python -m tbh_secure_agents.security_validation.tests.test_visualization --test metrics

# Specify output directory
python -m tbh_secure_agents.security_validation.tests.test_visualization --output-dir visualizations
```

## Demo

The package includes a demo script:

```bash
# Run the demo
python -m SecureAgents.examples.hybrid_security.hybrid_validation_demo

# Run with specific test
python -m SecureAgents.examples.hybrid_security.hybrid_validation_demo --test hybrid
python -m SecureAgents.examples.hybrid_security.hybrid_validation_demo --test levels
python -m SecureAgents.examples.hybrid_security.hybrid_validation_demo --test safe

# Run with API key
python -m SecureAgents.examples.hybrid_security.hybrid_validation_demo --api-key YOUR_API_KEY
```

## Requirements

- Python 3.8+
- numpy (for ML validation)
- scikit-learn (for ML validation)
- google-generativeai (for LLM validation)

## Installation

The package is included in the TBH Secure Agents framework. No additional installation is required.

To install the required dependencies:

```bash
pip install numpy scikit-learn google-generativeai
```

## Configuration

The package can be configured through environment variables:

- `GOOGLE_API_KEY`: API key for the Google Generative AI service (for LLM validation)
- `TBH_SECURITY_INTERACTIVE`: Set to "0" to disable interactive features
- `TBH_SECURITY_COLORS`: Set to "0" to disable colorized output
- `TBH_SECURITY_MODEL_PATH`: Path to a custom ML model
- `TBH_SECURITY_VECTORIZER_PATH`: Path to a custom vectorizer
- `TBH_SECURITY_CACHE_SIZE`: Maximum number of items to keep in the validation cache

## License

This package is part of the TBH Secure Agents framework and is subject to the same license.
