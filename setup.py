#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="web-snake",
      version="0.7.1",
      description="A simple web crawler in Python that crawls and returns the urls.",
      author="Alexi Rahman",
      author_email="alexi.rahman@r76.se",
      url="http://github.com/odynvolk/web-snake",
      install_requires=["requests>=2.5.0"],
      packages=find_packages(),
      keywords="web crawler",
      zip_safe=True)


