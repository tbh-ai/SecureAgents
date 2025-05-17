#!/usr/bin/env python3
"""
Script to generate visualizations of security test results for TBH Secure Agents framework.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Create directory for visualizations
os.makedirs('visualizations', exist_ok=True)

# Security challenge test results
challenges = [
    'Prompt Injection',
    'Tool Misuse',
    'Code Execution',
    'Communication Poisoning'
]

# Success rates for different security profiles
minimal_success = [25, 50, 25, 50]  # Percentage of tests passed with minimal security
standard_success = [75, 75, 50, 75]  # Percentage of tests passed with standard security
high_success = [100, 100, 75, 100]  # Percentage of tests passed with high security

# Create figure for security profile comparison
plt.figure(figsize=(12, 8))
x = np.arange(len(challenges))
width = 0.25

plt.bar(x - width, minimal_success, width, label='Minimal Security', color='#FF9999')
plt.bar(x, standard_success, width, label='Standard Security', color='#66B2FF')
plt.bar(x + width, high_success, width, label='High Security', color='#99CC99')

plt.xlabel('Security Challenge', fontsize=14)
plt.ylabel('Success Rate (%)', fontsize=14)
plt.title('TBH Secure Agents Framework: Security Profile Effectiveness', fontsize=16)
plt.xticks(x, challenges, fontsize=12)
plt.yticks(np.arange(0, 101, 10), fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add values on top of bars
for i, v in enumerate(minimal_success):
    plt.text(i - width, v + 2, f"{v}%", ha='center', fontsize=10)
for i, v in enumerate(standard_success):
    plt.text(i, v + 2, f"{v}%", ha='center', fontsize=10)
for i, v in enumerate(high_success):
    plt.text(i + width, v + 2, f"{v}%", ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('visualizations/security_profile_comparison.png', dpi=300)
plt.close()

# Create figure for overall security effectiveness
plt.figure(figsize=(10, 8))

# Overall effectiveness against Unit42 threats
threats = [
    'Prompt Injection',
    'Tool Misuse',
    'Intent Breaking',
    'Identity Spoofing',
    'Code Execution',
    'Communication Poisoning',
    'Resource Overload'
]

effectiveness = [80, 85, 75, 70, 65, 80, 60]  # Percentage effectiveness

# Create horizontal bar chart
plt.barh(threats, effectiveness, color='#66B2FF')
plt.xlabel('Effectiveness (%)', fontsize=14)
plt.title('TBH Secure Agents Framework: Effectiveness Against Unit42 Threats', fontsize=16)
plt.xlim(0, 100)
plt.xticks(np.arange(0, 101, 10), fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)

# Add values on bars
for i, v in enumerate(effectiveness):
    plt.text(v + 1, i, f"{v}%", va='center', fontsize=10)

plt.tight_layout()
plt.savefig('visualizations/overall_effectiveness.png', dpi=300)
plt.close()

# Create figure for security components effectiveness
plt.figure(figsize=(10, 8))

# Security components and their effectiveness
components = [
    'PromptDefender',
    'DataGuardian',
    'AgentSentinel',
    'ReliabilityMonitor'
]

component_effectiveness = [85, 80, 75, 70]  # Percentage effectiveness

# Create pie chart
plt.pie(component_effectiveness, labels=components, autopct='%1.1f%%', 
        startangle=90, shadow=True, explode=(0.1, 0, 0, 0),
        colors=['#FF9999', '#66B2FF', '#99CC99', '#FFCC99'])
plt.axis('equal')
plt.title('TBH Secure Agents Framework: Security Component Effectiveness', fontsize=16)

plt.tight_layout()
plt.savefig('visualizations/component_effectiveness.png', dpi=300)
plt.close()

print("Visualizations generated successfully in the 'visualizations' directory.")
