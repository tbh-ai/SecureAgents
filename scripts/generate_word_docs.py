#!/usr/bin/env python3
"""
Generate Word Documents from Markdown Files

This script converts all Markdown files in the docs directory to Word documents.
It requires Pandoc to be installed on the system.
"""

import os
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define paths
DOCS_DIR = Path("docs")
WORD_DOCS_DIR = Path("docs/word_docs")

def check_pandoc():
    """Check if Pandoc is installed."""
    try:
        subprocess.run(["pandoc", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def convert_markdown_to_word(md_file, docx_file):
    """Convert a Markdown file to a Word document using Pandoc."""
    try:
        logger.info(f"Converting {md_file} to {docx_file}")
        subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "docx", str(md_file), "-o", str(docx_file)],
            check=True,
            capture_output=True
        )
        logger.info(f"Successfully converted {md_file} to {docx_file}")
        return True
    except subprocess.SubprocessError as e:
        logger.error(f"Failed to convert {md_file} to {docx_file}: {e}")
        return False

def main():
    """Main function."""
    # Check if Pandoc is installed
    if not check_pandoc():
        logger.error("Pandoc is not installed. Please install Pandoc and try again.")
        logger.error("Installation instructions: https://pandoc.org/installing.html")
        return

    # Create the word_docs directory if it doesn't exist
    os.makedirs(WORD_DOCS_DIR, exist_ok=True)

    # Get all Markdown files in the docs directory
    md_files = list(DOCS_DIR.glob("*.md"))
    
    if not md_files:
        logger.warning(f"No Markdown files found in {DOCS_DIR}")
        return

    logger.info(f"Found {len(md_files)} Markdown files to convert")

    # Convert each Markdown file to a Word document
    success_count = 0
    for md_file in md_files:
        docx_file = WORD_DOCS_DIR / f"{md_file.stem}.docx"
        if convert_markdown_to_word(md_file, docx_file):
            success_count += 1

    # Log summary
    logger.info(f"Conversion complete: {success_count} of {len(md_files)} files converted successfully")
    logger.info(f"Word documents are available in {WORD_DOCS_DIR}")

if __name__ == "__main__":
    main()
