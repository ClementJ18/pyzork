#!/usr/bin/env python

from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('pyzork/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

extras_require = {
    'visualise': [
        'matplotlib', 
        'networkx'
    ],
    'docs': [
        'sphinx==1.8.3',
        'sphinx-autodoc-typehints==1.6.0'
    ]
}

setup(
    name = "pyzork",
    version = version,
    description = "An extensible python library for creating text adventures",
    author = "Clement Julia",
    author_email = "clement.julia13@gmail.com",
    url = "https://github.com/ClementJ18/pyzork",
    packages = ["pyzork"],
    install_requires=requirements,
    extras_require=extras_require
    )
