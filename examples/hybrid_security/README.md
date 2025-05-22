# Hybrid Security Validation Demo

This example demonstrates the hybrid security validation approach for the TBH Secure Agents framework. It shows how to use the hybrid validation with different security levels and content types.

## Overview

The hybrid security validation approach combines regex, machine learning, and large language models to provide comprehensive security validation with an optimal user experience. It uses a progressive approach, starting with fast regex checks and only using more sophisticated methods when necessary.

## Features

- **Multiple Validation Methods**: Demonstrates regex, ML, and LLM validation
- **Different Security Levels**: Shows how validation behaves with different security levels
- **Safe vs. Unsafe Content**: Compares validation results for safe and unsafe content
- **Original vs. Hybrid Validation**: Compares the original validation approach with the hybrid approach

## Running the Demo

```bash
# Run the full demo
python hybrid_validation_demo.py

# Run with specific test
python hybrid_validation_demo.py --test hybrid

# Run with API key
python hybrid_validation_demo.py --api-key YOUR_API_KEY
```

## Available Tests

- **original**: Run with the original validation approach
- **hybrid**: Run with the hybrid validation approach
- **levels**: Run with different security levels
- **safe**: Run with safe content
- **all**: Run all tests (default)

## Requirements

- Python 3.8+
- Google Generative AI Python SDK (for LLM validation)
- scikit-learn (for ML validation)

## API Key

The LLM validation requires an API key for the Google Generative AI service. You can provide it in one of two ways:

1. As a command-line argument: `--api-key YOUR_API_KEY`
2. As an environment variable: `GOOGLE_API_KEY=YOUR_API_KEY`

If no API key is provided, the LLM validation will be skipped.

## Expected Output

The demo will show how the hybrid validation approach handles different security levels and content types. It will display:

- Security validation progress
- Validation results (pass/fail)
- Detailed error messages for failed validations
- Suggestions for fixing security issues
- Performance metrics

## Integration with the Framework

The demo shows how to integrate the hybrid validation approach with the existing framework using the `enable_hybrid_validation()` function. This function monkey-patches the relevant methods in the Expert and Squad classes to use the hybrid validation approach.

## Next Steps

After running the demo, you can:

1. Explore the hybrid validation code in `tbh_secure_agents/security_validation/`
2. Run the test script in `tbh_secure_agents/security_validation/tests/test_hybrid_validation.py`
3. Integrate the hybrid validation approach into your own projects
