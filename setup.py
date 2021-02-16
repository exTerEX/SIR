#!/usr/bin/env python
"""
Distutils setup file, used to install or test 'SIR'
"""
from setuptools import setup  # pyright: reportMissingImports=false

if __name__ == "__main__":
    setup(
        name="SIR",
        version="0.1.0",
        author="Andreas Sagen",
        license="AFL-3.0",
        install_requires=[
            "numpy==1.20.1",
            "scipy==1.6.0",
            "matplotlib==3.3.4"
        ],
        zip_safe=False,
        extras_require={
            "test": ["pytest"]
        },
        packages=["source"]
    )
