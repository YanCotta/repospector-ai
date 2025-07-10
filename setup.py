#!/usr/bin/env python3
"""
Setup script for RepoSpector AI
"""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="repospector-ai",
    version="0.1.0",
    author="YanCotta",
    author_email="yancotta@example.com",
    description="An AI-powered multi-agent system built with CrewAI that automatically reviews GitHub repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YanCotta/repospector-ai",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
)
