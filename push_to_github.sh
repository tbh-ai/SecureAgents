#!/bin/bash

# Push changes to GitHub
# This script commits and pushes changes to the GitHub repository

# Ensure the script exits if any command fails
set -e

# Check if the repository exists
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git remote add origin https://github.com/tbh-ai/SecureAgents.git
fi

# Add all files
echo "Adding files to Git..."
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Version 0.3.2: Enhanced error messages and user experience"

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "Changes pushed to GitHub successfully!"
