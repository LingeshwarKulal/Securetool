#!/usr/bin/env python3
"""
Setup script for Secure File Encryption Tool
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="secure-file-encryption-tool",
    version="1.0.0",
    author="Security Application Team",
    author_email="team@securityapp.com",
    description="A desktop application for secure file and folder encryption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/securityteam/secure-file-encryption-tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "gui": [
            "tkinter-dev>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "secure-encrypt=main:main",
        ],
        "gui_scripts": [
            "secure-encrypt-gui=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "docs/*"],
    },
    zip_safe=False,
    keywords="encryption, security, file protection, AES, cryptography",
    project_urls={
        "Bug Reports": "https://github.com/securityteam/secure-file-encryption-tool/issues",
        "Source": "https://github.com/securityteam/secure-file-encryption-tool",
        "Documentation": "https://github.com/securityteam/secure-file-encryption-tool/wiki",
    },
)
