# Security Mechanisms Examples

This folder contains examples demonstrating the advanced security mechanisms in tbh.ai SecureAgents framework.

## Features Demonstrated

### Security Profiles
- **Low Security Profile**: Balanced security with good usability
- Allows most legitimate operations while blocking obvious threats
- Suitable for development and testing environments

### Guardrails
- Expert-specific behavioral constraints
- Ensure experts operate within defined boundaries
- Maintain quality and consistency of outputs

### Result Destination
- Automatic saving of operation results to specified files
- Organized output management
- Easy result tracking and review

### Super Adaptive Security
- Real-time learning from attack patterns
- Multi-layer validation (Adaptive + Regex + ML + LLM)
- Palo Alto Unit 42 threat intelligence integration

## Examples

### ai_researcher_writer_example.py
Demonstrates AI researcher and writer collaboration with:
- Two specialized experts (Researcher and Writer)
- Sequential operations with result destinations
- Low security profile for development use
- Guardrails for quality control
- Professional workflow automation

## Usage

```bash
cd examples/security_mechanisms
python ai_researcher_writer_example.py
```

## Security Features

- **Threat Detection**: Blocks malicious prompts and code injection
- **Content Validation**: Ensures output quality and safety
- **Access Control**: Prevents unauthorized system access
- **Data Protection**: Safeguards sensitive information

## Output Files

Results are automatically saved to:
- `research_findings.md` - Research analysis results
- `llm_evolution_article.md` - Final written article

## Security Profiles Available

- **minimal**: Basic security checks
- **low**: Balanced security and usability
- **standard**: Recommended for most use cases
- **high**: Enhanced security for sensitive environments
- **maximum**: Maximum security for critical applications
