from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="engcare",
    version="1.0.0",
    description="AI-Powered Engineer Wellness Platform - Mental Health & Burnout Prevention",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sakshi Tiwari",
    author_email="tiwarishakshi318@gmail.com",
    url="https://github.com/Sakshi983-cmd/EngCare-AI-Wellness",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Enterprise",
        "Topic :: Utilities"
    ],
    keywords=[
        "mental-health",
        "ai",
        "wellness", 
        "burnout-prevention",
        "employee-wellbeing",
        "workplace-health",
        "llm",
        "streamlit"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "engcare=app:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/Sakshi983-cmd/EngCare-AI-Wellness/issues",
        "Source": "https://github.com/Sakshi983-cmd/EngCare-AI-Wellness",
        "Documentation": "https://github.com/Sakshi983-cmd/EngCare-AI-Wellness#readme"
    },
)
