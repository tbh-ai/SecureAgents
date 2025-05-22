#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build script for the TBH Secure Agents package.
This script helps with building and publishing the package to PyPI.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_directories():
    """Clean build directories."""
    print("Cleaning build directories...")
    directories = ["build", "dist", "tbh_secure_agents.egg-info"]
    for directory in directories:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"  Removed {directory}")

def build_package():
    """Build the package."""
    print("Building package...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "wheel", "twine"], check=True)
    subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], check=True)
    print("Package built successfully.")

def check_package():
    """Check the package with twine."""
    print("Checking package...")
    subprocess.run([sys.executable, "-m", "twine", "check", "dist/*"], check=True)
    print("Package check completed.")

def upload_to_pypi():
    """Upload the package to PyPI."""
    print("Uploading package to PyPI...")
    response = input("Are you sure you want to upload to PyPI? (y/n): ")
    if response.lower() == "y":
        subprocess.run([sys.executable, "-m", "twine", "upload", "dist/*"], check=True)
        print("Package uploaded to PyPI successfully.")
    else:
        print("Upload cancelled.")

def push_to_github():
    """Push the package to GitHub."""
    print("Pushing to GitHub...")
    response = input("Are you sure you want to push to GitHub? (y/n): ")
    if response.lower() == "y":
        # Check if the repository is already initialized
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/tbh-ai/SecureAgents.git"], check=True)
        
        # Add all files
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit changes
        commit_message = input("Enter commit message: ")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push to GitHub
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("Changes pushed to GitHub successfully.")
    else:
        print("Push cancelled.")

def main():
    """Main function."""
    print("TBH Secure Agents - Build Script")
    print("================================")
    
    while True:
        print("\nOptions:")
        print("1. Clean build directories")
        print("2. Build package")
        print("3. Check package")
        print("4. Upload to PyPI")
        print("5. Push to GitHub")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            clean_build_directories()
        elif choice == "2":
            build_package()
        elif choice == "3":
            check_package()
        elif choice == "4":
            upload_to_pypi()
        elif choice == "5":
            push_to_github()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
