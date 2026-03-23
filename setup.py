#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup configuration for Saudi Gov Navigator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="saudi-gov-navigator",
    version="0.1.0",
    author="Aziz Al-Zahrani",
    author_email="aziz@example.com",
    description="دليل الخدمات الحكومية السعودية - Saudi Government Services Navigator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azizalzahrani/saudi-gov-navigator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: Arabic",
        "Natural Language :: English",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "saudi_gov": ["knowledge_base/*.json"],
    },
    entry_points={
        "console_scripts": [
            "saudi-gov-navigator=saudi_gov.chatbot:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/azizalzahrani/saudi-gov-navigator/issues",
        "Source": "https://github.com/azizalzahrani/saudi-gov-navigator",
        "Documentation": "https://github.com/azizalzahrani/saudi-gov-navigator#readme",
    },
)
