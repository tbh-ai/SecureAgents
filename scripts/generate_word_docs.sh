#!/bin/bash
# Generate Word documents from Markdown files

# Change to the project root directory
cd "$(dirname "$0")/.." || exit

# Check if Pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "Error: Pandoc is not installed. Please install Pandoc and try again."
    echo "Installation instructions: https://pandoc.org/installing.html"
    exit 1
fi

# Create the word_docs directory if it doesn't exist
mkdir -p docs/word_docs

# Convert each Markdown file to a Word document
echo "Converting Markdown files to Word documents..."

# Get all Markdown files in the docs directory
md_files=$(find docs -maxdepth 1 -name "*.md")

# Count the number of files
file_count=$(echo "$md_files" | wc -l)
echo "Found $file_count Markdown files to convert"

# Convert each file
success_count=0
for md_file in $md_files; do
    # Get the filename without the path and extension
    filename=$(basename "$md_file" .md)
    
    # Skip README.md files
    if [[ "$filename" == "README" ]]; then
        echo "Skipping $md_file"
        continue
    fi
    
    # Create the output file path
    docx_file="docs/word_docs/${filename}.docx"
    
    echo "Converting $md_file to $docx_file"
    
    # Convert the file
    if pandoc -f markdown -t docx "$md_file" -o "$docx_file"; then
        echo "Successfully converted $md_file to $docx_file"
        ((success_count++))
    else
        echo "Failed to convert $md_file to $docx_file"
    fi
done

# Print summary
echo "Conversion complete: $success_count of $file_count files converted successfully"
echo "Word documents are available in docs/word_docs"
