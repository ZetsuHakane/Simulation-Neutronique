#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='MonteCarloApp',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.1',  # Ensure compatibility with Python 3.1 and higher
    install_requires=[
        'openmc',
        'customtkinter',
        'numpy',
        'matplotlib',
        'glob2'
        # Add any additional dependencies here as needed
    ],
    entry_points={
        'console_scripts': [
            'main=main:main',  # Replace 'main' with the actual entry point of your application
        ],
    },
    author='Zetsu',  # Replace with your name
    description='Monte Carlo Simulation Application',  # Add a description of your application
    url='https://github.com/ZetsuHakane/Simulation-Neutronique.git',  # Replace with your GitHub repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

