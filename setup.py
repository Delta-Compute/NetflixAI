# The MIT License (MIT)
# Copyright © 2024 Your Organization

from setuptools import setup, find_packages
import os

# Read requirements
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    # Remove comments and empty lines
    requirements = [r for r in requirements if r and not r.startswith("#")]

# Read README
readme_path = "README.md"
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="subnet369",
    version="0.1.0",
    description="Subnet 369 - A Bittensor subnet template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Organization",
    author_email="your-email@example.com",
    url="https://github.com/yourusername/subnet369",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "subnet369-miner=neurons.miner:main",
            "subnet369-validator=neurons.validator:main",
        ],
    },
)