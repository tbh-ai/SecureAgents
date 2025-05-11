#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup, find_packages

# Read the version from __init__.py
with open(os.path.join('tbh_secure_agents', '__init__.py'), 'r') as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

# Read the long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tbh-secure-agents",
    version=version,
    author="TBH.AI",
    author_email="info@tbh.ai",
    description="A secure multi-agent framework for building AI applications with a focus on security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tbh-ai/SecureAgents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    license="Apache-2.0",
    python_requires=">=3.8",
    install_requires=[
        "google-generativeai>=0.3.0",
        "tqdm>=4.65.0",
        "reportlab>=4.0.0",
    ],
    keywords="ai, agents, multi-agent, security, llm, generative-ai",
    project_urls={
        "Bug Tracker": "https://github.com/tbh-ai/SecureAgents/issues",
        "Documentation": "https://github.com/tbh-ai/SecureAgents/tree/main/docs",
        "Source Code": "https://github.com/tbh-ai/SecureAgents",
    },
)
