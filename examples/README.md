# TBH Secure Agents Examples

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

This directory contains examples demonstrating various features and capabilities of the TBH Secure Agents framework. These examples are designed to help you understand how to use the framework effectively and securely.

## Directory Structure

- **basic/**: Simple examples demonstrating core functionality
- **advanced/**: More complex examples showcasing advanced features
- **security/**: Examples focused on security features
- **result_destination/**: Examples demonstrating the result_destination feature
- **guardrails/**: Examples showing how to use guardrails
- **output/**: Directory for storing output files from examples
- **colab_notebooks/**: Jupyter notebooks for interactive demonstrations

## Basic Examples

- **[basic/simple_features_demo.py](basic/simple_features_demo.py)**: Demonstrates the basic features of the framework
- **[basic/comprehensive_demo.py](basic/comprehensive_demo.py)**: A complete demonstration of multiple features including security profiles, guardrails, and multi-expert collaboration
- **[new_version_example.py](new_version_example.py)**: A simple, readable example demonstrating all the key features of the latest version (security profiles, guardrails, result destination)

## Security Examples

- **[security/security_profiles_demo.py](security/security_profiles_demo.py)**: Demonstrates how to use the different security profiles (minimal, low, standard, high, maximum)
- **[security/custom_security_profiles_demo.py](security/custom_security_profiles_demo.py)**: Shows how to create and use custom security profiles
- **[security/performance_test.py](security/performance_test.py)**: Tests the performance of different security profiles
- **[security/security_test.py](security/security_test.py)**: A comprehensive test of the framework's security features

## Result Destination Examples

- **[result_destination/result_destination_example.py](result_destination/result_destination_example.py)**: Demonstrates how to use the result_destination parameter
- **[result_destination/test_result_destination.py](result_destination/test_result_destination.py)**: Tests the result_destination feature with different file formats

## Guardrails Examples

- **[guardrails/easy_guardrails.py](guardrails/easy_guardrails.py)**: Simple example with basic template variables
- **[guardrails/medium_guardrails.py](guardrails/medium_guardrails.py)**: More complex example with conditional formatting
- **[guardrails/hard_guardrails.py](guardrails/hard_guardrails.py)**: Advanced example with nested conditional logic
- **[guardrails/security_guardrails.py](guardrails/security_guardrails.py)**: Example showing how to use guardrails for security
- **[guardrails/guardrails_with_result_destination.py](guardrails/guardrails_with_result_destination.py)**: Example combining guardrails with result_destination

## Advanced Examples

- **[advanced/code_security_review.py](advanced/code_security_review.py)**: Example of using the framework to perform a security code review
- **[advanced/flask_app_generation.py](advanced/flask_app_generation.py)**: Example of generating a Flask application
- **[advanced/information_extraction.py](advanced/information_extraction.py)**: Example of extracting structured information from text
- **[advanced/security_vulnerability_summary.py](advanced/security_vulnerability_summary.py)**: Example of summarizing security vulnerabilities
- **[advanced/story_concept_marketing.py](advanced/story_concept_marketing.py)**: Example of generating marketing content for a story concept

## Running the Examples

To run any of these examples, make sure you have set your Google API key as an environment variable:

```bash
export GOOGLE_API_KEY=your_api_key_here
```

Then run the example:

```bash
python examples/basic/simple_features_demo.py
```

## Output Files

Some examples save their output to files in the `output/` directory. You can view these files to see the results of the examples.

## Jupyter Notebooks

The `colab_notebooks/` directory contains Jupyter notebooks that demonstrate the framework's capabilities in an interactive format:

- **[colab_notebooks/TBH_Secure_Agents_Features_Demo.ipynb](colab_notebooks/TBH_Secure_Agents_Features_Demo.ipynb)**: A comprehensive demonstration of all the key features added in the latest version of the framework, including basic usage, security profiles, guardrails, and result destination.
- **[colab_notebooks/TBH_Secure_Agents_Demo.ipynb](colab_notebooks/TBH_Secure_Agents_Demo.ipynb)**: A general introduction to the framework, covering the basic concepts and usage.
- **[colab_notebooks/guardrails_example.ipynb](colab_notebooks/guardrails_example.ipynb)**: A focused demonstration of the guardrails feature.

You can run these notebooks in Google Colab or locally.

## Creating Your Own Examples

Feel free to modify these examples or create your own to explore the capabilities of the TBH Secure Agents framework. The examples are designed to be educational and to demonstrate best practices for secure multi-agent systems.
