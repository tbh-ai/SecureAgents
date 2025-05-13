#!/usr/bin/env python3
"""
Simple Features Demo of TBH Secure Agents Framework

This example demonstrates all key features with minimal security settings:
- Terminal UI
- Result destination (saving results to files)
- Security profiles (minimal security)
- Performance optimization with caching
- Guardrails for dynamic inputs
- Multi-expert collaboration

The scenario is a simple content creation pipeline that:
1. Generates a story outline
2. Writes a short story based on the outline
3. Creates a summary of the story
"""

import os
import sys
import time
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the TBH Secure Agents framework
from tbh_secure_agents import Expert, Operation, Squad
from tbh_secure_agents.security_profiles import (
    register_custom_profile, list_custom_profiles, get_custom_profile, clear_caches
)

# Get API key from environment variable or use a default one for testing
API_KEY = os.environ.get("GOOGLE_API_KEY", "")

def register_creative_profile():
    """Register a custom security profile for creative writing."""
    return register_custom_profile(
        name="creative",
        thresholds={
            "injection_score": 0.9,       # Very permissive injection detection
            "sensitive_data": 0.9,        # Very permissive sensitive data detection
            "relevance_score": 0.0,       # Disable relevance check completely
            "reliability_score": 0.0,     # Disable reliability check completely
            "consistency_score": 0.0,     # Disable consistency check completely
        },
        checks={
            "critical_exploits": False,   # Skip critical exploits check
            "system_commands": False,     # Skip system commands check
            "content_analysis": False,    # Skip content analysis
            "format_validation": False,   # Skip format validation
            "context_validation": False,  # Skip context validation
            "output_validation": False,   # Skip output validation
            "expert_validation": False,   # Skip expert validation
        },
        description="Custom security profile for creative writing with no restrictions"
    )

def create_story_outline_expert():
    """Create an expert for generating story outlines."""
    return Expert(
        specialty="Story Outline Creator",
        objective="Create engaging story outlines",
        background="Expert in narrative structure and storytelling",
        security_profile="creative",  # Use our custom creative profile
        api_key=API_KEY
    )

def create_story_writer_expert():
    """Create an expert for writing stories."""
    return Expert(
        specialty="Story Writer",
        objective="Write engaging short stories based on outlines",
        background="Expert in creative writing and narrative development",
        security_profile="creative",  # Use our custom creative profile
        api_key=API_KEY
    )

def create_story_summarizer_expert():
    """Create an expert for summarizing stories."""
    return Expert(
        specialty="Content Summarizer",
        objective="Create concise summaries of stories",
        background="Expert in content summarization and key point extraction",
        security_profile="creative",  # Use our custom creative profile
        api_key=API_KEY
    )

def create_outline_operation(genre, theme):
    """Create an operation for generating a story outline."""
    return Operation(
        instructions=f"""
        Create a detailed outline for a short story with the following:
        - Genre: {genre}
        - Theme: {theme}
        - Include 3-5 main plot points
        - Include 2-3 character descriptions
        - Include a setting description
        - Include a suggested title

        Format the outline with clear sections and bullet points.
        """
    )

def create_story_operation():
    """Create an operation for writing a story based on the outline."""
    return Operation(
        instructions="""
        Write a short story based on the outline provided. The story should:
        - Be approximately 500-800 words
        - Follow the plot points in the outline
        - Develop the characters as described
        - Use the setting as described
        - Use the suggested title or create a better one

        Write the story in an engaging and creative style appropriate for the genre.
        """
    )

def create_summary_operation():
    """Create an operation for summarizing the story."""
    return Operation(
        instructions="""
        Create a concise summary of the story provided. The summary should:
        - Be approximately 100-150 words
        - Capture the main plot points
        - Mention the key characters
        - Convey the theme and tone of the story

        Write the summary in an engaging style that would make someone want to read the full story.
        """
    )

def run_story_creation_pipeline(genre, theme, output_format="markdown"):
    """
    Run the complete story creation pipeline.

    Args:
        genre: The genre of the story
        theme: The theme of the story
        output_format: The format for the final output (markdown, json, html, or txt)

    Returns:
        The final story and summary
    """
    print(f"Starting Story Creation Pipeline: {genre} story about {theme}")
    print("=" * 50)

    # Register our custom security profile
    register_creative_profile()
    print("Registered custom 'creative' security profile")

    # Create experts
    outline_expert = create_story_outline_expert()
    writer_expert = create_story_writer_expert()
    summarizer_expert = create_story_summarizer_expert()
    print("Created specialized experts for each stage of the pipeline")

    # Create operations
    outline_operation = create_outline_operation(genre, theme)
    story_operation = create_story_operation()
    summary_operation = create_summary_operation()

    # Assign experts to operations
    outline_operation.expert = outline_expert
    story_operation.expert = writer_expert
    summary_operation.expert = summarizer_expert

    # Create guardrails for dynamic inputs
    guardrails = {
        "author_name": "A. I. Writer",
        "target_audience": "General readers",
        "tone": "Engaging and thoughtful",
        "include_moral": True
    }

    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")

    # Measure execution time to demonstrate performance
    start_time = time.time()

    # Create and deploy the squad
    squad = Squad(
        experts=[outline_expert, writer_expert, summarizer_expert],
        operations=[outline_operation, story_operation, summary_operation],
        process="sequential",  # Process operations in sequence
        security_level="creative",  # Use our custom creative profile with no restrictions
        result_destination={
            "format": output_format,
            "file_path": os.path.join(output_dir, f"story_{genre}_{theme}.{output_format}")
        }
    )

    # Deploy the squad with guardrails
    result = squad.deploy(guardrails=guardrails)

    # Calculate execution time
    execution_time = time.time() - start_time

    print(f"\nStory creation pipeline completed in {execution_time:.2f} seconds")
    output_file = os.path.join(output_dir, f"story_{genre}_{theme}.{output_format}")
    print(f"Results saved to {output_file}")

    # Clear caches to free memory
    clear_caches()
    print("Performance optimization: Caches cleared")

    return result

def main():
    """Run the simple features demo."""
    # Define story genres and themes
    story_combinations = [
        ("fantasy", "friendship"),
        ("mystery", "redemption"),
        ("science_fiction", "discovery"),
        ("romance", "second_chances")
    ]

    # Run the story creation pipeline for each combination
    for genre, theme in story_combinations:
        print(f"\n\nCreating {genre.upper()} story about {theme.upper()}")
        print("-" * 50)

        try:
            result = run_story_creation_pipeline(genre, theme)
            print(f"\nSuccessfully created {genre} story about {theme}")
        except Exception as e:
            print(f"Error creating story: {e}")

    print("\n\nSimple Features Demo Completed")
    print("=" * 50)
    print("Features demonstrated:")
    print("1. Terminal UI - You saw the interactive terminal output")
    print("2. Result Destination - Stories saved in markdown format")
    print("3. Security Profiles - Used minimal and custom security profiles")
    print("4. Performance Optimization - Used caching for improved performance")
    print("5. Guardrails - Used dynamic inputs for story creation")
    print("6. Multi-Expert Collaboration - Used specialized experts for each task")

if __name__ == "__main__":
    main()
