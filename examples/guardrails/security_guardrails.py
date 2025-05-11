#!/usr/bin/env python3
# examples/guardrails/security_guardrails.py
# Author: Saish (TBH.AI)

"""
Example demonstrating security-focused guardrails with TBH Secure Agents.
This example shows how to use guardrails to implement dynamic security controls.
"""

import os
import sys
import logging
import json

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    """
    Main function demonstrating security-focused guardrails with TBH Secure Agents.
    """
    print("\n" + "="*80)
    print("TBH SECURE AGENTS - SECURITY GUARDRAILS EXAMPLE".center(80))
    print("="*80 + "\n")

    # Set your API key
    # You can also set this as an environment variable: GOOGLE_API_KEY
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("Please set your GOOGLE_API_KEY environment variable.")
        return

    print("Creating security-focused experts with template variables...\n")

    # Create a security analyst expert with template variables
    security_analyst = Expert(
        specialty="Security Analyst specializing in {security_domain}",
        objective="Identify and analyze {threat_type} threats in {system_type} systems",
        background="You have expertise in security analysis and threat detection with a focus on {security_domain}.",
        security_profile="high_security",  # Using high security profile
        api_key=api_key
    )

    # Create a data privacy expert with template variables
    privacy_expert = Expert(
        specialty="Data Privacy Expert with focus on {privacy_standard}",
        objective="Ensure data handling complies with {privacy_standard} requirements",
        background="You have deep knowledge of privacy regulations and data protection practices.",
        security_profile="pii_protection",  # Using PII protection profile
        api_key=api_key
    )

    # Create a secure code reviewer with template variables
    code_reviewer = Expert(
        specialty="Secure Code Reviewer for {language} applications",
        objective="Identify security vulnerabilities in {application_type} code",
        background="You have expertise in secure coding practices and vulnerability detection.",
        security_profile="code_restricted",  # Using code restricted profile
        api_key=api_key
    )

    print("Creating operations with security-focused template variables...\n")

    # Create a threat analysis operation with security controls
    threat_analysis_operation = Operation(
        instructions="""
        Perform a {assessment_type} threat assessment for a {system_type} system in the {industry} sector.
        
        {security_level, select, 
          maximum:Apply the most stringent security analysis. Consider all threat vectors regardless of likelihood.|
          high:Focus on significant threats with moderate to high likelihood of occurrence.|
          standard:Focus on common threats with established mitigation strategies.
        }
        
        {threat_scope, select,
          external:Focus on external threat actors and attack vectors.|
          internal:Focus on insider threats and internal vulnerabilities.|
          comprehensive:Consider both external and internal threat vectors.
        }
        
        {include_mitigations, select,
          detailed:Provide detailed mitigation strategies for each identified threat.|
          basic:Provide basic mitigation guidance.|
          none:Focus only on threat identification without mitigations.
        }
        
        Security classification: {security_classification}
        """,
        output_format="A comprehensive threat assessment report",
        expert=security_analyst
    )

    # Create a privacy impact assessment operation
    privacy_assessment_operation = Operation(
        instructions="""
        Conduct a privacy impact assessment for a {system_type} that processes {data_type} data.
        
        {privacy_standard, select, 
          GDPR:Apply GDPR requirements including data minimization, purpose limitation, and data subject rights.|
          HIPAA:Apply HIPAA requirements for protected health information.|
          CCPA:Apply CCPA requirements including disclosure obligations and opt-out rights.
        }
        
        {data_sensitivity, select,
          high:The system processes highly sensitive personal data requiring maximum protection.|
          medium:The system processes moderately sensitive personal data.|
          low:The system processes minimally sensitive personal data.
        }
        
        {processing_scope, select,
          collection:Focus on data collection practices.|
          storage:Focus on data storage and retention.|
          processing:Focus on data processing and usage.|
          sharing:Focus on data sharing and third-party transfers.|
          complete:Cover the complete data lifecycle.
        }
        """,
        output_format="A structured privacy impact assessment compliant with {privacy_standard}",
        expert=privacy_expert
    )

    # Create a secure code review operation
    code_review_operation = Operation(
        instructions="""
        Review the following {language} code snippet for security vulnerabilities:
        
        ```{language}
        {code_snippet}
        ```
        
        {vulnerability_focus, select, 
          injection:Focus on identifying injection vulnerabilities.|
          authentication:Focus on authentication and session management issues.|
          access_control:Focus on access control vulnerabilities.|
          cryptography:Focus on cryptographic implementation issues.|
          comprehensive:Perform a comprehensive security review.
        }
        
        {severity_threshold, select, 
          critical:Report only critical vulnerabilities that could lead to system compromise.|
          high:Report critical and high severity vulnerabilities.|
          all:Report all vulnerabilities regardless of severity.
        }
        
        {secure_coding_standard, select,
          OWASP:Apply OWASP secure coding practices.|
          CERT:Apply CERT secure coding standards.|
          NIST:Apply NIST secure coding guidelines.
        }
        """,
        output_format="A security code review report highlighting vulnerabilities and recommendations",
        expert=code_reviewer
    )

    print("Creating a security-focused squad...\n")

    # Create a squad with the security experts and operations
    security_squad = Squad(
        experts=[security_analyst, privacy_expert, code_reviewer],
        operations=[threat_analysis_operation, privacy_assessment_operation, code_review_operation],
        process="sequential",  # Operations run in sequence
        security_level="high"  # Using high security level for the squad
    )

    print("Defining security-focused guardrail inputs...\n")

    # Define security-focused guardrail inputs
    security_guardrails = {
        # Security analyst guardrails
        "security_domain": "cloud infrastructure",
        "threat_type": "advanced persistent",
        "system_type": "multi-tenant SaaS application",
        "industry": "financial services",
        "assessment_type": "comprehensive",
        "security_level": "high",
        "threat_scope": "comprehensive",
        "include_mitigations": "detailed",
        "security_classification": "confidential",
        
        # Privacy expert guardrails
        "privacy_standard": "GDPR",
        "data_type": "personal financial",
        "data_sensitivity": "high",
        "processing_scope": "complete",
        
        # Code reviewer guardrails
        "language": "Python",
        "application_type": "web API",
        "vulnerability_focus": "comprehensive",
        "severity_threshold": "high",
        "secure_coding_standard": "OWASP",
        "code_snippet": """
def authenticate_user(username, password):
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    result = database.execute(query)
    if result:
        session['authenticated'] = True
        session['username'] = username
        return True
    return False

def get_user_data(user_id):
    data = database.execute("SELECT * FROM user_data WHERE user_id = " + user_id)
    return data

def update_profile(user_id, data):
    # Update user profile
    database.execute("UPDATE users SET data = '" + data + "' WHERE user_id = " + user_id)
    return True
        """,
        
        # Global security parameters
        "security_controls": {
            "input_validation": "strict",
            "output_sanitization": "enabled",
            "context_validation": "enabled",
            "pii_detection": "comprehensive",
            "threat_intelligence": "enabled"
        },
        "audit_level": "detailed",
        "security_logging": "verbose"
    }

    print("Security guardrail inputs defined. Here are some key security parameters:")
    print(f"  - Security domain: {security_guardrails['security_domain']}")
    print(f"  - System type: {security_guardrails['system_type']}")
    print(f"  - Security level: {security_guardrails['security_level']}")
    print(f"  - Privacy standard: {security_guardrails['privacy_standard']}")
    print(f"  - Vulnerability focus: {security_guardrails['vulnerability_focus']}")
    print(f"  - Audit level: {security_guardrails['audit_level']}")

    print("\nDeploying the squad with security-focused guardrail inputs...\n")

    # Deploy the squad with the security guardrails
    try:
        result = security_squad.deploy(guardrails=security_guardrails)

        print("\n" + "="*80)
        print("FINAL RESULT".center(80))
        print("="*80 + "\n")
        print(result)
        print("\n" + "="*80)

        # Save the output to a file
        output_file = os.path.join(os.path.dirname(__file__), "security_guardrails_output.txt")
        with open(output_file, "w") as f:
            f.write("TBH SECURE AGENTS - SECURITY GUARDRAILS EXAMPLE\n\n")
            f.write("Security guardrail inputs (selected):\n")
            for key in ["security_domain", "system_type", "security_level", "privacy_standard", 
                       "vulnerability_focus", "audit_level"]:
                f.write(f"  - {key}: {security_guardrails[key]}\n")
            f.write("\nResult:\n\n")
            f.write(result)
        
        print(f"\nOutput saved to {output_file}")

    except Exception as e:
        print(f"Error during squad deployment: {e}")

if __name__ == "__main__":
    main()
