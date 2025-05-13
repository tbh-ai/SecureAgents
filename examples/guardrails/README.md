# Guardrails Examples

<img width="618" alt="Main" src="https://github.com/user-attachments/assets/dbbf5a4f-7b0b-4f43-9b37-ef77dc761ff1" />

This folder contains examples demonstrating the guardrails feature in the TBH Secure Agents framework. Guardrails provide a powerful way to dynamically control and guide the behavior of experts without modifying your core code.

## Examples Overview

The examples are organized by complexity level:

### Basic Examples

- **[easy_guardrails.py](./easy_guardrails.py)**: Simple example showing basic template variables for a weather forecast
- **[basic_guardrails.py](./basic_guardrails.py)**: Basic example showing template variables for healthcare content

### Intermediate Examples

- **[medium_guardrails.py](./medium_guardrails.py)**: More complex example with multiple experts and conditional formatting for travel guides

### Advanced Examples

- **[advanced_guardrails.py](./advanced_guardrails.py)**: Advanced example with complex template variables and conditional formatting
- **[hard_guardrails.py](./hard_guardrails.py)**: Complex example with nested conditional logic and multiple interdependent experts
- **[security_guardrails.py](./security_guardrails.py)**: Security-focused example demonstrating how to use guardrails to implement dynamic security controls

## Running the Examples

To run any of these examples, make sure you have set your Google API key as an environment variable:

```bash
export GOOGLE_API_KEY=your_api_key_here  # Replace with your actual API key
```

Then run the example:

```bash
python examples/guardrails/easy_guardrails.py
```

## Example Outputs

Each example saves its output to a corresponding text file in the same directory:

- `easy_guardrails_output.txt`
- `basic_guardrails_output.txt`
- `medium_guardrails_output.txt`
- `advanced_guardrails_output.txt`
- `hard_guardrails_output.txt`
- `security_guardrails_output.txt`

## Key Features Demonstrated

These examples demonstrate various guardrails features:

1. **Template Variables**: Using variables like `{variable_name}` in expert profiles and operation instructions
2. **Conditional Formatting**: Using the select syntax for conditional content based on guardrail values
3. **Complex Data Structures**: Passing complex data structures as guardrail inputs
4. **Security Controls**: Using guardrails to implement dynamic security controls
5. **Multiple Experts**: Coordinating multiple experts with shared guardrail inputs
6. **Nested Logic**: Using nested conditional logic for complex decision-making

## Documentation

For more information about guardrails, see the [Comprehensive Guardrails Guide](../../docs/guardrails_comprehensive.md) in the documentation.
