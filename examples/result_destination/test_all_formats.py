#!/usr/bin/env python3
"""
Test script for all supported result_destination file formats.

This script demonstrates saving operation results in all supported formats:
- Text (.txt)
- Markdown (.md)
- CSV (.csv)
- JSON (.json)
- HTML (.html)
- PDF (.pdf)
"""

import os
import sys
import time
import json

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad

# Create output directory if it doesn't exist
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get API key from environment variable or use a default one for testing
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyDYGDWiED84ZAL71xbT3QDBfUnCTrIPvpc")

def create_expert():
    """Create a test expert."""
    return Expert(
        specialty="Content Writer",
        objective="Create well-formatted content in various formats",
        background="Experienced in creating structured content",
        api_key=API_KEY
    )

def simulate_operation_result(format_type):
    """
    Simulate an operation result based on the requested format.
    In a real scenario, this would be the output from the LLM.
    """
    if format_type == 'txt':
        return """Benefits of Renewable Energy

Renewable energy sources offer numerous benefits:

1. Environmental Benefits
   - Reduced greenhouse gas emissions
   - Less air and water pollution
   - Conservation of natural resources

2. Economic Benefits
   - Job creation in renewable energy sector
   - Reduced energy costs over time
   - Energy independence and security

3. Social Benefits
   - Improved public health
   - Enhanced energy access in remote areas
   - Sustainable development"""

    elif format_type == 'md':
        return """# Benefits of Renewable Energy

Renewable energy sources offer numerous benefits for our environment, economy, and society.

## Environmental Benefits
- **Reduced Carbon Emissions**: Unlike fossil fuels, renewable energy produces minimal greenhouse gases
- **Cleaner Air and Water**: Less pollution means healthier ecosystems and communities
- **Preservation of Natural Resources**: Renewable sources are sustainable and won't deplete

## Economic Advantages
- **Job Creation**: The renewable sector creates more jobs per unit of energy than fossil fuels
- **Energy Independence**: Reduces reliance on imported fuels
- **Stable Energy Prices**: Once installed, costs remain relatively constant

## Technological Innovation
- **Driving New Technologies**: Spurs advancements in storage, grid management, and efficiency
- **Decentralized Energy**: Enables local production and resilience
- **Complementary Systems**: Different renewable sources can work together for reliable supply"""

    elif format_type == 'csv':
        return """Category,Benefit,Description
Environmental,Reduced Carbon Emissions,Unlike fossil fuels renewable energy produces minimal greenhouse gases
Environmental,Cleaner Air and Water,Less pollution means healthier ecosystems and communities
Environmental,Preservation of Natural Resources,Renewable sources are sustainable and won't deplete
Economic,Job Creation,The renewable sector creates more jobs per unit of energy than fossil fuels
Economic,Energy Independence,Reduces reliance on imported fuels
Economic,Stable Energy Prices,Once installed costs remain relatively constant
Social,Improved Public Health,Cleaner air and water leads to better health outcomes
Social,Enhanced Energy Access,Can provide power to remote areas without extensive infrastructure
Social,Sustainable Development,Meets present needs without compromising future generations"""

    elif format_type == 'json':
        data = {
            "topic": "Benefits of Renewable Energy",
            "categories": [
                {
                    "name": "Environmental Benefits",
                    "benefits": [
                        {"title": "Reduced Carbon Emissions", "description": "Unlike fossil fuels, renewable energy produces minimal greenhouse gases"},
                        {"title": "Cleaner Air and Water", "description": "Less pollution means healthier ecosystems and communities"},
                        {"title": "Preservation of Natural Resources", "description": "Renewable sources are sustainable and won't deplete"}
                    ]
                },
                {
                    "name": "Economic Benefits",
                    "benefits": [
                        {"title": "Job Creation", "description": "The renewable sector creates more jobs per unit of energy than fossil fuels"},
                        {"title": "Energy Independence", "description": "Reduces reliance on imported fuels"},
                        {"title": "Stable Energy Prices", "description": "Once installed, costs remain relatively constant"}
                    ]
                },
                {
                    "name": "Social Benefits",
                    "benefits": [
                        {"title": "Improved Public Health", "description": "Cleaner air and water leads to better health outcomes"},
                        {"title": "Enhanced Energy Access", "description": "Can provide power to remote areas without extensive infrastructure"},
                        {"title": "Sustainable Development", "description": "Meets present needs without compromising future generations"}
                    ]
                }
            ]
        }
        return json.dumps(data, indent=2)

    elif format_type == 'html':
        return """<h1>Benefits of Renewable Energy</h1>
<p>Renewable energy sources offer numerous benefits for our environment, economy, and society.</p>

<h2>Environmental Benefits</h2>
<ul>
    <li><strong>Reduced Carbon Emissions</strong>: Unlike fossil fuels, renewable energy produces minimal greenhouse gases</li>
    <li><strong>Cleaner Air and Water</strong>: Less pollution means healthier ecosystems and communities</li>
    <li><strong>Preservation of Natural Resources</strong>: Renewable sources are sustainable and won't deplete</li>
</ul>

<h2>Economic Advantages</h2>
<ul>
    <li><strong>Job Creation</strong>: The renewable sector creates more jobs per unit of energy than fossil fuels</li>
    <li><strong>Energy Independence</strong>: Reduces reliance on imported fuels</li>
    <li><strong>Stable Energy Prices</strong>: Once installed, costs remain relatively constant</li>
</ul>

<h2>Social Benefits</h2>
<ul>
    <li><strong>Improved Public Health</strong>: Cleaner air and water leads to better health outcomes</li>
    <li><strong>Enhanced Energy Access</strong>: Can provide power to remote areas without extensive infrastructure</li>
    <li><strong>Sustainable Development</strong>: Meets present needs without compromising future generations</li>
</ul>"""

    # For PDF, we'll use the same content as markdown
    elif format_type == 'pdf':
        return simulate_operation_result('md')

    return "Unsupported format"

def test_format(format_type):
    """Test a specific file format."""
    print(f"\nTesting {format_type.upper()} format...")
    
    # Create an expert
    expert = create_expert()
    
    # Create the file path
    file_path = os.path.join(OUTPUT_DIR, f"result.{format_type}")
    
    # Create an operation with the specific result_destination
    operation = Operation(
        instructions=f"Create content about renewable energy benefits in {format_type.upper()} format",
        expert=expert,
        result_destination=file_path
    )
    
    # Create a squad with just this operation
    squad = Squad(
        experts=[expert],
        operations=[operation],
        process="sequential",
        security_level="minimal"  # Use minimal security for testing
    )
    
    # Mock the execution by directly setting the result
    # In a real scenario, this would be done by the LLM
    operation.result = simulate_operation_result(format_type)
    
    # Manually trigger the result saving
    success = operation._save_result_to_file(operation.result)
    
    # Check if the file was created
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        print(f"✓ Success! File created: {file_path}")
        print(f"  File size: {file_size} bytes")
        
        # Print a preview of the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            preview = content[:200] + "..." if len(content) > 200 else content
            print(f"  Preview: {preview}")
    else:
        print(f"✗ Failed to create file: {file_path}")
    
    return file_path

def main():
    """Run tests for all supported formats."""
    print("Testing all supported result_destination file formats")
    print("=" * 50)
    
    # List of formats to test
    formats = ['txt', 'md', 'csv', 'json', 'html', 'pdf']
    
    # Test each format
    created_files = []
    for format_type in formats:
        try:
            file_path = test_format(format_type)
            created_files.append(file_path)
        except Exception as e:
            print(f"Error testing {format_type} format: {e}")
    
    # Print summary
    print("\nTest Summary")
    print("=" * 50)
    print(f"Tested {len(formats)} formats")
    print(f"Successfully created {len(created_files)} files")
    
    # List all created files
    print("\nCreated files:")
    for file_path in created_files:
        if os.path.exists(file_path):
            print(f"- {os.path.basename(file_path)}")

if __name__ == "__main__":
    main()
