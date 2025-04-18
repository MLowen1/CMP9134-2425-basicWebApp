from setuptools import setup, find_packages

setup(
    name="basic_webapp",          # any name that is unique on PyPI
    version="0.1.0",
    packages=find_packages(),     # automatically finds 'backend', etc.
    python_requires=">=3.9",
)