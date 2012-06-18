#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

import pygplus

setup(name="PyGooglePlus",
    version=pygplus.__version__,
    description="Google+ Unofficial API for Python",
    license=pygplus.__license__,
    author=pygplus.__author__,
    url=pygplus.__url__,
    packages = find_packages(),
    keywords= "",
    zip_safe = True,
    install_requires=[
        'beautifulsoup4',
        'simplejson'
    ]
)