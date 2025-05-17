#!/bin/bash

# Build and publish the package to PyPI
# This script builds the package and uploads it to PyPI

# Ensure the script exits if any command fails
set -e

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies if not already installed
echo "Installing build dependencies..."
pip install --upgrade pip
pip install --upgrade build twine

# Build the package
echo "Building the package..."
python -m build

# Check the package
echo "Checking the package..."
twine check dist/*

# Upload to PyPI
echo "Uploading to PyPI..."
twine upload dist/*

echo "Package published successfully!"
