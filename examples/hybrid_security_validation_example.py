"""
Example demonstrating the hybrid security validation and visualization features.

This example shows how to use the hybrid security validation system and
generate HTML security reports with visualizations.

Note: These features are currently in beta and may change in future releases.
"""

import os
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_validation import HybridValidator
from tbh_secure_agents.visualization import generate_security_report

# Create output directories
os.makedirs("outputs/security_reports", exist_ok=True)

# Create an expert with hybrid security validation
security_expert = Expert(
    specialty="Security Analyst",
    objective="Analyze code for security vulnerabilities",
    security_profile="high",
    hybrid_validation=True  # Enable hybrid validation
)

# Sample code to analyze
sample_code = """
def process_user_input(user_input):
    # This function has a SQL injection vulnerability
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    
    # This function also has a command injection vulnerability
    import os
    os.system("echo " + user_input)
    
    return query
"""

# Create an operation with hybrid security validation
operation = Operation(
    instructions=f"Analyze this code for security vulnerabilities:\n\n{sample_code}",
    expert=security_expert,
    hybrid_validation_level="comprehensive"  # Options: "basic", "standard", "comprehensive"
)

# Execute the operation
print("Executing operation with hybrid security validation...")
result = operation.execute()
print("\nOperation result:")
print(result)

# Generate an HTML security report
print("\nGenerating HTML security report...")
report_path = generate_security_report(
    operation=operation,
    result=result,
    output_path="outputs/security_reports/hybrid_validation_report.html",
    include_visualizations=True
)

print(f"\nSecurity report generated at: {report_path}")

# Create a squad with multiple experts and operations
print("\nCreating a squad with multiple experts and operations...")

code_reviewer = Expert(
    specialty="Code Reviewer",
    objective="Review code for security best practices",
    security_profile="high",
    hybrid_validation=True
)

remediation_expert = Expert(
    specialty="Security Remediation Specialist",
    objective="Provide remediation steps for security vulnerabilities",
    security_profile="high",
    hybrid_validation=True
)

review_operation = Operation(
    instructions=f"Review this code for security best practices:\n\n{sample_code}",
    expert=code_reviewer,
    hybrid_validation_level="standard"
)

remediation_operation = Operation(
    instructions="Based on the security analysis, provide specific steps to fix the vulnerabilities",
    expert=remediation_expert,
    hybrid_validation_level="standard"
)

# Create and deploy a squad
security_squad = Squad(
    experts=[security_expert, code_reviewer, remediation_expert],
    operations=[operation, review_operation, remediation_operation],
    process="sequential",
    result_destination={
        "format": "html",
        "file_path": "outputs/security_reports/squad_security_report.html"
    }
)

print("Deploying security squad...")
squad_result = security_squad.deploy()

print("\nSquad deployment complete!")
print("Check the outputs/security_reports directory for the generated reports.")

# Additional information about the hybrid security validation system
print("\nHybrid Security Validation Components:")
print("1. Rule-based Validation: Uses regex patterns and heuristics")
print("2. ML-based Validation: Uses machine learning models")
print("3. LLM-based Validation: Uses large language models")

print("\nVisualization Features:")
print("1. HTML Reports: Detailed HTML reports with security validation results")
print("2. Security Score Visualizations: Visual representations of security scores")
print("3. Threat Detection Visualizations: Visual representations of detected threats")
print("4. Recommendation Visualizations: Visual representations of security recommendations")

print("\nNote: These features are currently in beta and may change in future releases.")
