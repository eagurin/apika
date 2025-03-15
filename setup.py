#!/usr/bin/env python
"""Setup script for the apiki package."""

import os

from setuptools import find_packages, setup

# Read the contents of README.md
with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="apiki",
    version="0.1.0",
    description=(
        "API Knowledge Integration - Interact with APIs using LangChain agents"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/apiki",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "langchain>=0.0.335",
        "langchain-openai>=0.0.2",
        "langchain-community>=0.0.13",
        "langchain-core>=0.1.22",
        "langsmith>=0.0.87",
        "openai>=1.0.0",
        "pydantic>=2.5.3",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "numpy>=1.26.0",
    ],
    entry_points={"console_scripts": ["apiki=apiki.cli:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9,<3.13",
    license="MIT",
)
